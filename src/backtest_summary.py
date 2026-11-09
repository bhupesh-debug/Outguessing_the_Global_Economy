"""Reproduce the Part 18 backtest headline table from the paper's figures.

Source: Liquidity & Outgues Part 18, full article v2, Appendix A and
Table 14 — Backtest Score v1, 120 monthly decisions, November 2016 to
October 2026. The backtest FAILS: this module reproduces the failure
exactly as published. It does not re-run the backtest (the underlying
monthly series are not in this repo) and it does not soften any number.

Headline figures (all from the paper):
- Top-1 hit rate, 12M: 17.4% (19 of 109) vs ~50% for a random pick
- Top-1 portfolio CAGR: -1.71% vs +8.07% equal-weight
- Sharpe: -0.33 vs +0.67
- Max drawdown: -31.5% vs -11.8%
- Rank IC: -0.202 (median -0.25; positive in 25.7% of months)
- US equities never ranked #1 in 120 decisions
"""

from __future__ import annotations

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _read_csv(name: str) -> list[dict]:
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def headline() -> dict:
    """Headline backtest figures as published (strings kept as in the
    paper; numeric parsing is done by the caller where needed)."""
    rows = _read_csv("backtest_headline.csv")
    return {r["metric"]: r for r in rows}


def components() -> list[dict]:
    """Component information coefficients vs forward 12-month return."""
    out = []
    for r in _read_csv("backtest_components.csv"):
        out.append(
            {"component": r["component"], "ic": float(r["information_coefficient"])}
        )
    return sorted(out, key=lambda r: r["ic"])


def hit_rates() -> list[dict]:
    """Top-1 hit rate by horizon, from the headline table."""
    h = headline()
    return [
        {"horizon_months": 1, "hit_rate_pct": float(h["hit_rate_1m_pct"]["top1_portfolio"]), "n": 120},
        {"horizon_months": 3, "hit_rate_pct": float(h["hit_rate_3m_pct"]["top1_portfolio"]), "n": 118},
        {"horizon_months": 6, "hit_rate_pct": float(h["hit_rate_6m_pct"]["top1_portfolio"]), "n": 115},
        {"horizon_months": 12, "hit_rate_pct": float(h["hit_rate_12m_pct"]["top1_portfolio"]), "n": 109},
    ]


def mechanical_crosscheck_nov6() -> list[dict]:
    """Backtest Score v1 scored on November 6, 2026 (Appendix A cross-check).

    Nearly the reverse of the judgemental ranking — the paper prints both
    and lets the reader weigh them.
    """
    out = []
    for r in _read_csv("mechanical_crosscheck_nov6.csv"):
        out.append(
            {"asset": r["asset"], "backtest_score_v1": float(r["backtest_score_v1_nov6"])}
        )
    return sorted(out, key=lambda r: -r["backtest_score_v1"])


def derived_gaps() -> dict:
    """Simple arithmetic on the published figures (not new data)."""
    h = headline()
    return {
        "hit_rate_gap_vs_random_pp": round(
            float(h["hit_rate_12m_pct"]["top1_portfolio"])
            - float(h["hit_rate_12m_pct"]["equal_weight_benchmark"]),
            1,
        ),
        "cagr_gap_pp": round(
            float(h["cagr_pct"]["top1_portfolio"])
            - float(h["cagr_pct"]["equal_weight_benchmark"]),
            2,
        ),
        "sharpe_gap": round(
            float(h["sharpe"]["top1_portfolio"])
            - float(h["sharpe"]["equal_weight_benchmark"]),
            2,
        ),
        "max_drawdown_gap_pp": round(
            float(h["max_drawdown_pct"]["top1_portfolio"])
            - float(h["max_drawdown_pct"]["equal_weight_benchmark"]),
            1,
        ),
    }


def as_markdown() -> str:
    h = headline()
    g = derived_gaps()
    lines = [
        "## Backtest — the headline result (reproduced, not re-run)",
        "",
        "Source: Part 18 v2, Appendix A / Table 14. Backtest Score v1, "
        "120 monthly decisions, November 2016–October 2026. "
        "**The backtest fails, and the failure is the finding.**",
        "",
        "| Metric | Top-1 portfolio | Equal-weight benchmark |",
        "|---|---|---|",
        f"| CAGR | {h['cagr_pct']['top1_portfolio']}% | "
        f"{h['cagr_pct']['equal_weight_benchmark']}% |",
        f"| Sharpe ratio | {h['sharpe']['top1_portfolio']} | "
        f"{h['sharpe']['equal_weight_benchmark']} |",
        f"| Max drawdown | {h['max_drawdown_pct']['top1_portfolio']}% | "
        f"{h['max_drawdown_pct']['equal_weight_benchmark']}% |",
        f"| Top-1 hit rate, 12M | {h['hit_rate_12m_pct']['top1_portfolio']}% "
        f"(19 of 109) | ~{float(h['hit_rate_12m_pct']['equal_weight_benchmark']):.0f}% "
        f"(random pick) |",
        f"| Rank IC | {h['rank_ic']['top1_portfolio']} | — |",
        "",
        "Derived gaps (arithmetic on the published figures only): "
        f"hit-rate gap {g['hit_rate_gap_vs_random_pp']}pp vs random; "
        f"CAGR gap {g['cagr_gap_pp']}pp; Sharpe gap {g['sharpe_gap']}; "
        f"drawdown gap {g['max_drawdown_gap_pp']}pp.",
        "",
        "Hit rate by horizon (top-ranked asset vs peer median):",
        "",
        "| Horizon | Hit rate | n |",
        "|---:|---:|---:|",
    ]
    for r in hit_rates():
        lines.append(f"| {r['horizon_months']}M | {r['hit_rate_pct']}% | {r['n']} |")
    lines.append("")
    lines.append("Component information coefficients (vs forward 12M return):")
    lines.append("")
    lines.append("| Component | IC |")
    lines.append("|---|---:|")
    for r in components():
        lines.append(f"| {r['component']} | {r['ic']:+.3f} |")
    lines.append("")
    lines.append(
        "Strongest component: Analogue (+0.298). Worst: Macro (−0.408). "
        "The November 6 judgemental scores are unchanged by this test "
        "because they are judgements, not backtest outputs — and the "
        "backtest stands as a warning about them."
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(as_markdown())
