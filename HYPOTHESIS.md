# Hypothesis — Testable, With Confirm/Falsify Conditions

Source: Part 18 v2 (Sections 8–11, Appendix A) and the condensed edition.
Data as of November 7, 2026. Every probability below is either a published
figure or is labelled as a judgement.

## H1 — The ranking hypothesis (the paper's central claim)

**Statement.** Indian equities have the highest probability of
outperforming over the next 12 months, ranked #1 on the Final Asset
Attractiveness Score (59/100), ahead of the US dollar (58) and gold (57),
because growth (7.0%), domestic capital (about $75bn), momentum (Nifty
+2.01% on November 6, seventh straight gain) and relative yield outweigh
a foreign outflow that is fully counted in the Flow component (48).

**Plain-language version.** The crowd that matters in India has changed
nationality: foreigners sold about $31bn in 2026 while domestic
institutions bought about $75bn, and the market rose anyway. The bet is
that the domestic bid, plus a foreign trickle-back, carries Indian
equities further than the dollar, gold, or US equities over the next year.

### Confirm conditions (H1 gains support if, by end-December 2026)

- October US CPI (November 10) comes in soft or in line, and the Fed
  signals a pause or delivers a neutral December hike — Moves 1 or 2.
- FPI flows into Indian equities stay positive in November on NSDL/CDSL
  data (the late-October turn broadens rather than reverses).
- Brent crude stays below $110.
- The Nifty holds its November 6 level (25,030.35) into year-end while
  the S&P 500 stays range-bound — the rotation, not just a day's move.

### Falsify conditions (H1 loses support)

- **The invalidation trio, all three together: hot October CPI on
  November 10 + Brent above $110 + FPI negative again in November.**
  That combination invalidates the analysis outright, because it removes
  the three conditions the thesis rests on: a Fed that can pause, an oil
  price that lets the RBI breathe, and a foreign flow that has turned.
- Any ONE of the three weakens the thesis substantially.
- A December Fed hike to a hawkish path (10-year above 5.00%) combined
  with the rupee sliding toward 97 would confirm the contrarian thesis
  (the India thesis as a dollar thesis in disguise).

### What the evidence currently says about H1

- **Judgemental ranking: supports H1** (India equities #1 at 59).
- **Empirical frequencies: contradict H1.** The calibrated 12-month
  outperformance frequencies (Table 8, n=109) put US equities first at
  77% [68–84], gold second at 69% [60–77], and India equities at 44%
  [35–53]. The v1 model estimates (India equities 62%, Gold 58%, USD
  55%) were systematically inverted.
- **Backtest: contradicts the method behind H1.** The mechanical proxy's
  top-ranked asset beat the peer median in only 17.4% of 12-month
  windows. H1 is therefore a judgement with a warning attached, not a
  validated signal. This project reports both sides and does not resolve
  the contradiction — only new data can.

## H2 — The method hypothesis (does the combination improve prediction?)

**Statement.** Combining macro, flow and valuation signals with strategic
expectations improves the prediction of outperformance.

**Status: UNPROVEN — the first test failed.** The backtest (Appendix A)
shows the mechanical proxy of the three-score method did not improve the
ranking: top-1 hit rate 17.4% at 12 months, rank IC −0.202, and the
top-ranked portfolio compounded at −1.71% a year vs +8.07% equal-weight.
The one component with real signal was the historical analogue (+0.298),
not the macro score (−0.408).

**Confirm condition (for the re-specified method):** a re-run of the
walk-forward backtest on the re-specified method (shrunk Macro and
Relative-yield, promoted analogue, real Flow series) achieves a top-1
12-month hit rate above the ~50% random rate with a positive rank IC.

**Falsify condition:** the re-specified method also fails — top-1 hit
rate at or below ~50% and rank IC at or below zero — in which case the
framework is a reading tool, not a signal, and should be presented as
such.

## H3 — The Bayesian worked example (judgemental, not empirical)

**Statement.** India equities will outperform US equities over the next
6 months.

- Prior P(H): 50% (neutral — the two markets have traded leadership).
- Evidence (all verified): India GDP 7.0–7.1% vs US 2.3%; FPI turned
  positive in late October (~$1.2bn in 10 sessions); US real yields
  high (10-year real about 2.3–2.6%) and the dollar firming; Indian
  valuations reasonable relative to the growth gap (Sensex down 15.6% in
  2026 as of mid-October).
- Likelihood ratio: 1.5 (a judgement, stated as such, not a computed
  statistic).
- Posterior: P(H|E) = 1.5 × 50% / (1.5 × 50% + 1 × 50%) = **60%**.
  Confidence: Medium.

**A discrepancy to state plainly.** The v2 article's prose says that 60%
"is the model's 6-month outperformance probability for India equities in
Table 8". Table 8 itself gives **50% [41–59]** for India equities at 6
months (n=115), and the condensed edition's prose agrees with the table.
The table governs: 60% is the judgemental Bayesian posterior from this
worked example; 50% is the empirical frequency. They differ because one
is a judgemental update and the other is a historical frequency — and the
difference is the point. This project uses 50% wherever it cites Table 8.

**What would reverse H3:** a December Fed hike combined with Brent above
$110 and a fresh FPI selling streak in November would cut the posterior
below 50% — the same trio as H1's invalidation, because the update rests
on the same three conditions.
