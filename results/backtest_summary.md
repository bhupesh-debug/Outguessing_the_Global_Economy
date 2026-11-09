## Backtest — the headline result (reproduced, not re-run)

Source: Part 18 v2, Appendix A / Table 14. Backtest Score v1, 120 monthly decisions, November 2016–October 2026. **The backtest fails, and the failure is the finding.**

| Metric | Top-1 portfolio | Equal-weight benchmark |
|---|---|---|
| CAGR | -1.71% | 8.07% |
| Sharpe ratio | -0.33 | 0.67 |
| Max drawdown | -31.5% | -11.8% |
| Top-1 hit rate, 12M | 17.4% (19 of 109) | ~50% (random pick) |
| Rank IC | -0.202 | — |

Derived gaps (arithmetic on the published figures only): hit-rate gap -32.6pp vs random; CAGR gap -9.78pp; Sharpe gap -1.0; drawdown gap -19.7pp.

Hit rate by horizon (top-ranked asset vs peer median):

| Horizon | Hit rate | n |
|---:|---:|---:|
| 1M | 31.7% | 120 |
| 3M | 29.7% | 118 |
| 6M | 26.1% | 115 |
| 12M | 17.4% | 109 |

Component information coefficients (vs forward 12M return):

| Component | IC |
|---|---:|
| Macro | -0.408 |
| Relative yield | -0.336 |
| Liquidity | -0.285 |
| Risk/reward | -0.080 |
| Flow | -0.060 |
| Currency | -0.030 |
| Momentum | +0.001 |
| Valuation | +0.147 |
| Analogue | +0.298 |

Strongest component: Analogue (+0.298). Worst: Macro (−0.408). The November 6 judgemental scores are unchanged by this test because they are judgements, not backtest outputs — and the backtest stands as a warning about them.