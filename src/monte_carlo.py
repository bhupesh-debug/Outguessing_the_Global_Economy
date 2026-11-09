"""Monte Carlo simulation of 12-month outcomes for the seven Part 18 assets.

WHAT THIS IS
------------
A transparent, deterministic simulation built ONLY on numbers published
in the Part 18 papers. It is a teaching and stress-testing tool, not a
forecast and not a trading signal. Every assumption is stated below and
in MONTE_CARLO.md; change any of them and the numbers change.

INPUTS (published, not invented)
-------------------------------
- Per-asset 12-month return distributions: the OBSERVED mean and standard
  deviation of 12-month USD total returns in the backtest window, from
  Table 7 of the full article v2 (n=109 monthly decisions, Nov 2016–
  Oct 2025). File: data/bull_base_bear.csv.
- Regime probabilities: Table 9 scenarios (model estimates, Nov 6, 2026).
  Bull 30%, Base 45%, Bear 25%. File: data/scenarios.csv.
- Comparison benchmark: Table 8 calibrated 12-month outperformance
  frequencies (empirical, Wilson 95% CIs). File:
  data/calibrated_probabilities.csv.

MODEL (stated assumptions — these are OURS, not the paper's)
----------------------------------------------------------
1. Each draw picks a regime from the Table 9 probabilities.
2. Within a regime, each asset's 12-month return is drawn from a Normal
   distribution with mean = observed mean + regime shift, SD = observed
   SD. Regime shifts: Bull +0.5 SD, Base 0, Bear -0.5 SD. The +/-0.5 SD
   shift is a modelling choice made here so the scenarios actually move
   the distribution; it is NOT published in the paper and is stated as
   an assumption everywhere the results appear.
3. Draws are INDEPENDENT across assets (no cross-asset correlation).
   This is the biggest simplification: real assets move together, and
   ignoring correlation widens the simulated spread of "who beats the
   peer median". The comparison table in the output shows exactly how
   far the simulated P(outperform) sits from the paper's empirical
   frequencies — read that gap as the price of the simplification.
4. Normality: real 12-month returns have fat tails; a Normal understates
   extremes. P5/P95 ranges are therefore narrower than history's.
5. Fixed seed (20261107) and 100,000 draws: fully deterministic — re-run
   and you get the same numbers to the last decimal.

OUTPUTS (per asset)
-------------------
- median / mean / sd of the simulated 12-month return
- P(loss): share of draws with return < 0
- P(outperform): share of draws in which the asset's return beats the
  cross-sectional median of the seven assets in that draw — the same
  "beat the peer median" definition Table 8 uses
- P5 / P95: the 5th and 95th percentiles ("worst" / "best" in the
  scenario tables)

The backtest warning applies here too: the method this simulation is
built on FAILED its first test (top-1 hit rate 17.4% at 12M). These
simulated distributions describe the backtest window's observed return
distributions under the paper's scenarios — they do not validate the
ranking.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

SEED = 20261107
N_DRAWS = 100_000

# Regime mean shifts, in units of each asset's own SD. Modelling choice
# made here (see module docstring); NOT published in the paper.
REGIME_SHIFTS_SD = {"Bull": 0.5, "Base": 0.0, "Bear": -0.5}

# Scenario labels in Table 9 mapped to the shift keys above.
SCENARIO_TO_REGIME = {
    "Bull: rotation completes": "Bull",
    "Base: grinding transition": "Base",
    "Bear: hike + energy shock": "Bear",
}


def load_return_params(path: str | Path = DATA_DIR / "bull_base_bear.csv") -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [
        {
            "asset": r["asset"],
            "bull_pct": float(r["bull_pct"]),
            "base_pct": float(r["base_pct"]),
            "bear_pct": float(r["bear_pct"]),
            "mean_12m_pct": float(r["mean_12m_return_pct"]),
            "sd_12m_pct": float(r["sd_12m_return_pct"]),
        }
        for r in rows
    ]


def load_scenario_probs(path: str | Path = DATA_DIR / "scenarios.csv") -> dict[str, float]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {
        SCENARIO_TO_REGIME[r["scenario"]]: float(r["probability_pct"]) / 100.0
        for r in rows
    }


def load_empirical_12m(path: str | Path = DATA_DIR / "calibrated_probabilities.csv") -> dict[str, dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {
        r["asset"]: {
            "pct": float(r["pct_12m"]),
            "ci_low": float(r["ci_12m_low"]),
            "ci_high": float(r["ci_12m_high"]),
        }
        for r in rows
    }


def scenario_ranges(params: list[dict]) -> dict[str, dict[str, dict[str, float]]]:
    """Best / base / worst 12-month return per asset per scenario.

    Centre = observed mean + regime shift (Bull +0.5 SD, Base 0,
    Bear -0.5 SD). Worst = centre - 1.645 SD, Best = centre + 1.645 SD
    (90% interval under the Normal assumption). All figures are model
    estimates built on the backtest window's observed distribution.
    """
    out: dict[str, dict[str, dict[str, float]]] = {}
    for p in params:
        out[p["asset"]] = {}
        for regime, shift in REGIME_SHIFTS_SD.items():
            centre = p["mean_12m_pct"] + shift * p["sd_12m_pct"]
            out[p["asset"]][regime] = {
                "worst_p5_pct": round(centre - 1.645 * p["sd_12m_pct"], 1),
                "base_centre_pct": round(centre, 1),
                "best_p95_pct": round(centre + 1.645 * p["sd_12m_pct"], 1),
            }
    return out


def simulate(n: int = N_DRAWS, seed: int = SEED) -> dict:
    """Run the Monte Carlo. Returns per-asset summary statistics."""
    params = load_return_params()
    probs = load_scenario_probs()
    regimes = ["Bull", "Base", "Bear"]
    regime_p = np.array([probs[r] for r in regimes])
    assert abs(regime_p.sum() - 1.0) < 1e-9, "scenario probabilities must sum to 1"

    rng = np.random.default_rng(seed)
    # One regime per draw, shared across assets (a regime is a world state).
    regime_idx = rng.choice(3, size=n, p=regime_p)
    shifts = np.array([REGIME_SHIFTS_SD[r] for r in regimes])[regime_idx]  # (n,)

    draws: dict[str, np.ndarray] = {}
    for p in params:
        mu = p["mean_12m_pct"] + shifts * p["sd_12m_pct"]
        draws[p["asset"]] = rng.normal(loc=mu, scale=p["sd_12m_pct"], size=n)

    # Cross-sectional median per draw (the peer median, Table 8's definition).
    matrix = np.vstack([draws[p["asset"]] for p in params])  # (7, n)
    peer_median = np.median(matrix, axis=0)

    results: dict[str, dict] = {}
    for p in params:
        d = draws[p["asset"]]
        results[p["asset"]] = {
            "median_12m_pct": round(float(np.median(d)), 2),
            "mean_12m_pct": round(float(np.mean(d)), 2),
            "sd_12m_pct": round(float(np.std(d, ddof=1)), 2),
            "p_loss_pct": round(float(np.mean(d < 0) * 100), 1),
            "p_outperform_pct": round(
                float(np.mean(d > peer_median) * 100), 1
            ),
            "p5_pct": round(float(np.percentile(d, 5)), 1),
            "p95_pct": round(float(np.percentile(d, 95)), 1),
        }

    empirical = load_empirical_12m()
    for asset, r in results.items():
        e = empirical[asset]
        r["empirical_12m_outperform_pct"] = e["pct"]
        r["empirical_ci"] = [e["ci_low"], e["ci_high"]]
        r["sim_minus_empirical_pp"] = round(r["p_outperform_pct"] - e["pct"], 1)

    return {
        "seed": seed,
        "n_draws": n,
        "regime_probabilities": {r: probs[r] for r in regimes},
        "regime_shifts_sd": dict(REGIME_SHIFTS_SD),
        "assets": results,
    }


def save_results(results: dict, out_dir: str | Path = RESULTS_DIR) -> tuple[Path, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "monte_carlo_results.json"
    csv_path = out_dir / "monte_carlo_results.csv"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "asset", "median_12m_pct", "mean_12m_pct", "sd_12m_pct",
            "p_loss_pct", "p_outperform_pct", "p5_pct", "p95_pct",
            "empirical_12m_outperform_pct", "empirical_ci_low",
            "empirical_ci_high", "sim_minus_empirical_pp",
        ])
        for asset, r in results["assets"].items():
            w.writerow([
                asset, r["median_12m_pct"], r["mean_12m_pct"], r["sd_12m_pct"],
                r["p_loss_pct"], r["p_outperform_pct"], r["p5_pct"], r["p95_pct"],
                r["empirical_12m_outperform_pct"], r["empirical_ci"][0],
                r["empirical_ci"][1], r["sim_minus_empirical_pp"],
            ])
    return json_path, csv_path


def save_scenario_ranges(out_dir: str | Path = RESULTS_DIR) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ranges = scenario_ranges(load_return_params())
    path = out_dir / "scenario_ranges.json"
    path.write_text(json.dumps(ranges, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    res = simulate()
    jp, cp = save_results(res)
    rp = save_scenario_ranges()
    print(f"Monte Carlo: {res['n_draws']:,} draws, seed {res['seed']}")
    print(f"wrote {jp}\n      {cp}\n      {rp}")
    for asset, r in res["assets"].items():
        print(
            f"{asset:15s} median {r['median_12m_pct']:>6.2f}%  "
            f"P(loss) {r['p_loss_pct']:>4.1f}%  "
            f"P(outperform) {r['p_outperform_pct']:>4.1f}% "
            f"(empirical {r['empirical_12m_outperform_pct']:.0f}%)  "
            f"P5 {r['p5_pct']:>6.1f}%  P95 {r['p95_pct']:>6.1f}%"
        )
