# Data sources

Every number in this project traces to one of two documents, both by
Bhupesh Chandra Dimri, Liquidity & Outgues program, Part 18:

- **Condensed edition (final paper, 29 pp):**
  `Liquidity_and_Outgues_Part18_Condensed_2026-11-07.pdf`
- **Full article v2 (39 pp):**
  `Liquidity_and_Outgues_Part18_Final_Article_v2_2026-11-07.pdf`

Data as of **November 7, 2026** (backtest and flow refresh); market scores
dated **November 6, 2026** (market closes).

| File | Source table / section |
|---|---|
| `scores.csv` | Full article v2, Figure 3 (p. 17) and Table 5 — three independent scores (Macro, Flow, Price/Valuation), Strategic Expectation Score (supplementary), Final score (Part 13 weights), paper rank. Model estimates, Nov 6, 2026. |
| `calibrated_probabilities.csv` | Full article v2, Table 8 (p. 21) — empirical 12-month (and 1/3/6-month) outperformance frequencies with Wilson 95% CIs, from the 10-year walk-forward backtest. Sample sizes: 1M n=120, 3M n=118, 6M n=115, 12M n=109. |
| `bull_base_bear.csv` | Full article v2, Table 7 (p. 20) — empirical bull/base/bear frequencies per asset (bull = 12M USD total return >5pp above peer median; bear = >5pp below; base = within ±5pp) plus observed mean and standard deviation of 12-month USD total returns in the backtest window, n=109. |
| `backtest_headline.csv` | Full article v2, Appendix A and Table 14 — Backtest Score v1, 120 monthly decisions, Nov 2016–Oct 2026. |
| `backtest_components.csv` | Full article v2, Appendix A, Diagnosis — component information coefficients vs forward 12-month return. |
| `mechanical_crosscheck_nov6.csv` | Full article v2, Appendix A, "The November 6 Cross-Check" — Backtest Score v1 scored on Nov 6, 2026. |
| `scenarios.csv` | Full article v2, Table 9 (p. 22) — bull/base/bear scenarios, model estimates Nov 6, 2026. |
| `next_moves.csv` | Full article v2, Table 13 (p. 36) — the next three possible moves, model judgements Nov 6, 2026. |
| `analogues.csv` | Full article v2, Table 6 (pp. 19–20) — computed regime analogues (13 standardised variables, RMS distance, similarity = 100 × (1 − d/d95), d95 = 2.200). Average 12-month return after the top five: US equities +30.2%, India equities +21.9%, Gold +33.4%, Silver +28.6%, USD −0.0%, US Treasuries +6.2%, India bonds +5.4%. Best distinct episode: November 2018 (similarity 61.6), followed by April–July 2018 (61.3–60.9). |

## Numbers deliberately NOT included

- **6-month India-equities outperformance of 60%.** The v2 article's prose
  (Bayesian worked example) states that 60% is "the model's 6-month
  outperformance probability for India equities in Table 8". Table 8 itself
  (p. 21) gives 50% [41–59] for India equities at 6 months (n=115), and the
  condensed edition's prose agrees with the table (50%). The table governs:
  60% is the *judgemental Bayesian posterior* from the worked example
  (prior 50%, likelihood ratio 1.5), not the empirical frequency. Both
  figures appear in HYPOTHESIS.md with the distinction explained; the 60%
  is never presented as the Table 8 frequency.
- **Component scores for the six non-published Part 13 components**
  (Liquidity, Momentum, Relative yield, Currency, Historical analogue,
  Risk/reward). The paper states the Final score is computed from them
  plus Figure 3, but does not tabulate them as numbers. They are not
  invented here; `src/scoring.py` documents the gap and verifies the
  ranking from the published Final scores instead.
- **Any figure dated after November 7, 2026.** October U.S. CPI prints
  November 10 and the Fed meets December 8–9; neither outcome is in this
  project.
