# Outguessing the Global Economy — Liquidity & Outgues, Part 18

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Data as of](https://img.shields.io/badge/data%20as%20of-Nov%207%2C%202026-informational)
![Tests](https://img.shields.io/badge/pytest-23%20passed-brightgreen)
![Research](https://img.shields.io/badge/research-not%20investment%20advice-red)

**One-line verdict:** the rotation has begun — out of crowded US growth,
into dollars and short-duration safety, selectively into India — but the
method that ranks the rotation **failed its first backtest**, so this
project reports the ranking and the failure side by side.

This is the code-and-simulation companion to *Outguessing the Global
Economy: Strategic Thinking, Behavioral Intelligence and Quantitative
Detection of Capital Migration Across the United States, India and Major
World Economies* (Part 18 of the Liquidity & Outgues program, November 7,
2026). It turns the paper into something you can run: the headline
ranking recomputed from the published scores, the backtest reproduced
from the published figures, a Monte Carlo that is actually executed, and
an interactive simulator that runs entirely in your browser.

> **Read this first.** The November 6 scores are model estimates —
> judgements, not validated signals. The 10-year walk-forward backtest
> (Appendix A of the paper) does **not** validate the scoring method: its
> top-ranked asset beat the peer median in only **17.4%** of 12-month
> windows (n=109) vs ~50% for a random pick, and its top-1 portfolio
> compounded at **−1.71%** a year vs **+8.07%** for equal-weight. This
> project prints that failure on the front page, in the simulator, and in
> every document — because a test that only gets published when it passes
> is not a test. Research and education, not investment advice.

## Headline ranking — November 6, 2026 (model estimates)

| Rank | Asset | Macro | Flow | Price/Val. | Strategic Exp. (supp.) | Final |
|---:|---|---:|---:|---:|---:|---:|
| 1 | India equities | 72 | 48 | 50 | 60 | **59** |
| 2 | USD | 60 | 58 | 50 | 57 | **58** |
| 3 | Gold | 60 | 62 | 48 | 58 | **57** |
| 4 | India bonds | 62 | 50 | 62 | 52 | **57** |
| 5 | US Treasuries | 55 | 60 | 55 | 54 | **56** |
| 6 | Silver | 55 | 55 | 55 | 55 | **55** |
| 7 | US equities | 58 | 52 | 45 | 52 | **53** |

Regime: **Transition / Rotation**. The gold / India-bonds tie at 57 is
broken by flow confirmation in favour of gold. The Strategic Expectation
Score is a fourth, supplementary dimension and never enters the ranking.
`src/scoring.py` recomputes this ranking from `data/scores.csv` and
verifies it against the paper — run it and see.

The headline is deliberately uncomfortable: the highest-ranked asset is
the one foreigners spent the year selling (about $31bn out) while
domestic Indian institutions bought about $75bn. The ranking says Indian
equities are the most attractive asset on the combined evidence, and
simultaneously that the foreign-flow evidence is the weakest part of the
case. Both halves are true, and this project keeps both visible.

## The backtest fails — reported as a finding

| Metric | Top-1 portfolio | Equal-weight |
|---|---:|---:|
| CAGR | −1.71% | +8.07% |
| Sharpe | −0.33 | +0.67 |
| Max drawdown | −31.5% | −11.8% |
| Top-1 hit rate, 12M | 17.4% (19 of 109) | ~50% (random pick) |
| Rank IC | −0.202 | — |

Hit rate by horizon: 1M 31.7%, 3M 29.7%, 6M 26.1%, 12M 17.4% — below
random at every horizon, worst at the horizon it is meant to serve.
Component diagnosis: Macro −0.408 (worst), Relative yield −0.336,
Liquidity −0.285, **Analogue +0.298 (best)**, Valuation +0.147,
Momentum +0.001. US equities were never ranked #1 in 120 decisions —
the asset that beat the peer median in 77% of 12-month windows.
Full reproduction: `src/backtest_summary.py`,
`results/backtest_summary.md`.

## Calibrated 12-month outperformance (empirical, n=109, Wilson 95% CI)

These replace the v1 model estimates, which were systematically inverted.

| Asset | 12M frequency |
|---|---:|
| US equities | **77%** [68–84] |
| Gold | **69%** [60–77] |
| Silver | 54% [45–63] |
| India equities | 44% [35–53] |
| USD | 28% [20–37] |
| US Treasuries | 16% [10–24] |
| India bonds | 13% [8–20] |

## Monte Carlo — actually run (100,000 draws, seed 20261107)

Simulated 12-month outcomes under the paper's scenarios (Bull 30% /
Base 45% / Bear 25%), using the Table 7 observed mean/SD per asset.
Full method, assumptions and limitations: [MONTE_CARLO.md](MONTE_CARLO.md).

| Asset | Median 12M | P(loss) | P(outperform) | P5 | P95 | Empirical 12M |
|---|---:|---:|---:|---:|---:|---:|
| India equities | +8.96% | 33.5% | 50.4% | −25.3% | +43.1% | 44% |
| USD | +0.60% | 46.4% | 15.3% | −10.6% | +11.8% | 28% |
| Gold | +16.70% | 20.3% | 67.5% | −16.2% | +49.8% | 69% |
| India bonds | +1.81% | 34.7% | 17.1% | −5.8% | +9.4% | 13% |
| US Treasuries | +1.50% | 42.4% | 19.7% | −11.5% | +14.5% | 16% |
| Silver | +21.81% | 29.8% | 63.6% | −46.1% | +90.5% | 54% |
| US equities | +14.05% | 16.5% | 66.4% | −9.5% | +37.9% | 77% |

## Scenarios

| Scenario | Probability | Trigger |
|---|---:|---|
| Bull: rotation completes | 30% | Oct CPI soft Nov 10; Fed signals pause; FPI buying broadens |
| Base: grinding transition | 45% | CPI in line; Dec hike delivered; rotation stays selective |
| Bear: hike + energy shock | 25% | CPI hot; Brent breaks $110; Strait of Hormuz disruption |

Per-asset best/base/worst ranges under each scenario, the next three
possible moves (35/45/20), and the surprise overlays:
[SCENARIOS.md](SCENARIOS.md).

## What's in this repo

| File | What it is |
|---|---|
| [index.html](index.html) | **Interactive calculation simulator** — adjust the Macro/Flow/Price scores, pick a scenario, run a seeded Monte Carlo in your browser. No external dependencies; open it or visit the GitHub Pages site. |
| [README.md](README.md) | This file. |
| [SWOT.md](SWOT.md) | Full SWOT analysis, grounded in the papers. |
| [HYPOTHESIS.md](HYPOTHESIS.md) | The testable hypothesis with confirm/falsify conditions and the invalidation trio. |
| [SCENARIOS.md](SCENARIOS.md) | All scenarios, ranges, next three moves, surprise overlays. |
| [SIMULATIONS.md](SIMULATIONS.md) | All six strategic simulations (A–F) from the research. |
| [MONTE_CARLO.md](MONTE_CARLO.md) | Monte Carlo method, assumptions, limitations, results. |
| [RECOMMENDATION.md](RECOMMENDATION.md) | Recommendation, what to avoid, conclusion. |
| `src/` | `scoring.py`, `backtest_summary.py`, `monte_carlo.py`, `run_all.py` |
| `tests/` | pytest suite (23 tests) — ranking, Monte Carlo, backtest. |
| `data/` | The paper's published tables as CSV, with `sources.md` tracing every number to paper, table and page. |
| `results/` | Generated output: ranking check, backtest summary, Monte Carlo results, scenario ranges. |

## How to run

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt   # numpy only
.venv/bin/python src/run_all.py             # runs everything, writes results/
.venv/bin/python -m pytest tests/ -q        # 23 tests
```

Or open `index.html` directly in a browser — the simulator is
self-contained and needs no server, no build step, and no internet.

## Limitations (the boundary of the claim)

- The backtest failed; the scores are judgements with a warning attached.
- Backtest proxies: India bonds by policy-rate carry (no duration), Flow
  neutral for US equities and India bonds, India CPI ends March 2025,
  RBI reserves proxied by USD/INR.
- Analogue ranking is thin: all five analogues are late-2023 months — one
  episode, not five independent ones.
- Calibrated probabilities are backward-looking (2016–2026, a decade
  dominated by US equities and gold).
- As-of staleness: data as of November 7, 2026. October US CPI prints
  November 10; the Fed meets December 8–9. Re-running the scores on fresh
  data is the only cure, and it has not happened yet.
- The model decays the moment opponents learn it — a limitation no
  backtest can fix.
- The Monte Carlo's regime shifts (±0.5 SD) are our stated assumption,
  its draws are independent across assets, and its inputs are Normal
  approximations of fat-tailed returns.

**Open next step (named in the papers, not done here):** re-specify the
method — shrink the Macro and Relative-yield components, promote the
analogue component, replace the neutral Flow components with real series
— and re-run the backtest.

## Author

**Bhupesh Chandra Dimri** — Financial Analyst, JPMorgan Chase (Jul
2025–present); M.S. Accounting Analytics & Data Technology, Pace
University (Dec 2025). GitHub: [bhupesh-debug](https://github.com/bhupesh-debug).
Contact: bhupesh7cd@gmail.com.

Liquidity & Outgues program, Part 18. Companion papers: *Outguessing the
Global Economy* (full article v2, 39 pp, and condensed edition, 29 pp),
November 7, 2026.
