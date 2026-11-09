## Headline ranking — recomputed from the published scores

Source: Part 18 v2, Figure 3 (p. 17) / Table 5. Model estimates, November 6, 2026. The three-score mean is a diagnostic only — it is NOT the Final score (see `src/scoring.py`). The Strategic Expectation Score is supplementary and never enters the ranking.

| Rank | Asset | Macro | Flow | Price/Val. | 3-score mean | Strategic Exp. (sep.) | Final |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | India equities | 72 | 48 | 50 | 56.67 | 60 | 59 |
| 2 | USD | 60 | 58 | 50 | 56.00 | 57 | 58 |
| 3 | Gold | 60 | 62 | 48 | 56.67 | 58 | 57 |
| 4 | India bonds | 62 | 50 | 62 | 58.00 | 52 | 57 |
| 5 | US Treasuries | 55 | 60 | 55 | 56.67 | 54 | 56 |
| 6 | Silver | 55 | 55 | 55 | 55.00 | 55 | 55 |
| 7 | US equities | 58 | 52 | 45 | 51.67 | 52 | 53 |

Tie at 57 (Gold vs India bonds) broken by flow confirmation in favour of Gold, per the paper (Gold Flow 62 vs India bonds Flow 50).

Validation: all checks pass — recomputed ranking matches the paper's published rank.