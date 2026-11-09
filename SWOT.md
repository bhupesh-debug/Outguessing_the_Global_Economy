# SWOT Analysis — Liquidity & Outgues, Part 18

Grounded in the Part 18 papers (full article v2 and condensed edition,
November 7, 2026). Every point traces to a stated finding, number, or
limitation in the papers. Data as of November 7, 2026.

## Strengths

- **A framework, not a forecast.** Three independent scores (Macro, Flow,
  Price/Valuation) plus a separately reported Strategic Expectation Score
  keep the judgemental and the strategic halves checkable against each
  other. A market can be macro-strong, flow-weak, and price-expensive at
  once — the system shows the tension instead of averaging it away.
- **Flow discipline.** Every flow claim is labelled ACTUAL FLOW, FLOW
  PROXY, or MARKET-INFERRED FLOW, and a rising price is never presented
  as proof that capital arrived. Monthly flow data is never presented as
  daily. Two source discrepancies (US CPI, Indian FPI totals) are resolved
  by stated standardisation, with the alternatives noted once.
- **Early-rotation detection, demonstrated.** The late-October FPI turn
  (~$1.2bn in 10 sessions, ACTUAL FLOW) preceded the November 6 Nifty
  surge (+2.01%) by a week — the early-rotation signature the system is
  built to detect, and the strongest single signal in the article.
- **The analogue component works.** In the backtest, the regime-analogue
  component has the strongest information coefficient (+0.298) of any
  component — the one part of the method with real predictive content.
  The analogue ranking is computed (13 standardised variables, RMS
  distance), not judged: top analogue October 2023, similarity 80.2.
- **Honest calibration.** Outperformance probabilities are empirical
  frequencies with sample sizes and Wilson 95% CIs (Tables 7 and 8),
  replacing the systematically inverted v1 model estimates.
- **Breadth of evidence.** Six strategic simulations (A–F), an
  expectation-gap analysis, a Bayesian worked example with the arithmetic
  shown, and an adversarial case stated in full.

## Weaknesses

- **The backtest fails — the central weakness.** Backtest Score v1's
  top-ranked asset beat the peer median in only 17.4% of 12-month windows
  (n=109) vs ~50% for a random pick; its top-1 portfolio compounded at
  −1.71% a year vs +8.07% equal-weight; Sharpe −0.33 vs +0.67; max
  drawdown −31.5% vs −11.8%; rank IC −0.202. The method's first test was
  negative.
- **The Macro component is anti-predictive.** IC −0.408 — the worst of any
  component, and it carries the largest weight (20%). Relative yield is
  next (−0.336) and Liquidity (−0.285). The components the method leans
  on most are the ones that fail most.
- **Proxies where series could not be obtained.** India bonds by
  policy-rate carry (no duration — misses the 2022 and 2026 duration
  moves); Flow neutral for US equities and India bonds (and for India
  equities before November 2021); RBI reserves proxied by USD/INR; India
  CPI ends March 2025 in the series used.
- **Thin analogues.** All five computed analogues are late-2023 months —
  one episode, not five independent ones. Best distinct episode,
  November 2018, scores only 61.6.
- **Judgemental scores, not validated signals.** The November 6 scores
  (India equities 59, USD 58, Gold 57, India bonds 57, US Treasuries 56,
  Silver 55, US equities 53) are judgements with a warning attached. Six
  of the nine Part 13 components are not published as numbers, so the
  Final score cannot be recomputed from the published inputs (see
  `src/scoring.py`).
- **The mechanical cross-check nearly reverses the ranking.** Backtest
  Score v1 on November 6 ranks the dollar first (55.2) and gold last
  (23.1); India equities sit fourth (47.3). The judgemental and the
  mechanical rankings disagree, and the paper prints both.
- **As-of staleness.** Data as of November 7, 2026. October US CPI
  (November 10) and the December 8–9 FOMC can change the regime
  classification; the scores have not been re-run on fresh data.

## Opportunities

- **Re-specification — the named next step.** Shrink the Macro and
  Relative-yield components, promote the analogue component, replace the
  neutral Flow components with real series, and re-run the backtest. The
  diagnosis points at exactly what to change; the work is scoped, not
  open-ended.
- **The India domestic-capital story.** Domestic institutions bought
  about $75bn while foreigners sold about $31bn — the Indian market of
  2026 is structurally different from 2013, and models that only watch
  FPI flows are watching the wrong crowd. That distinction is the India
  engine's central insight and the paper's most original claim.
- **Two live expectation gaps.** The December Fed hike (market ~76–78%
  vs a Fed that has given no guidance) and the India FPI return
  (consensus: foreigners left for good; flows: $1.2bn back in 10
  sessions). Gaps of that shape close violently, in one direction or the
  other — and the November 10 CPI print is the scheduled moment.
- **The rotation itself.** Out of crowded US growth, into dollars and
  short-duration safety, selectively into India: the direction of the
  rotation is the thing the model is most confident about, and a
  transition/rotation regime is where the analogue method shows the widest
  dispersion of outcomes — the largest edge for a strategist who reads
  the turn early.
- **Calendar catalysts.** November 10 CPI, November 18 TIC release,
  December 8–9 FOMC: three dated checkpoints that will score the thesis
  within a month.

## Threats

- **The invalidation trio (stated in advance).** Hot October CPI on
  November 10 + Brent above $110 + FPI negative again in November: any
  one weakens the thesis; all three together invalidate it.
- **The dollar thesis in disguise.** The strongest contrarian case: if
  the Fed hikes in December and Brent breaks $110, the dollar goes to
  105, the rupee to 97, the RBI is forced to 6.00%, and the $1.2bn
  late-October FPI turn is revealed as a positional trade. The domestic
  bid has never been tested in a genuine stress episode.
- **Model decay.** The model loses edge the moment opponents learn it —
  a limitation no backtest can fix.
- **The two-week flow turn is the most fragile assumption.** $1.2bn of
  buying against $31bn of selling: a rounding error dressed as a turn,
  or a regime change — the paper cannot tell yet, and neither can this
  project.
- **SIP-flow momentum risk.** The domestic bid is real but partly
  momentum-chasing: SIP flows continue while markets rise and stop when
  they fall, as in every prior Indian correction.
- **Data risk.** Fresh flow data (TIC to August 2026, CFTC to November 3)
  can change the Flow score without any change in the underlying economy;
  the FPI standardisation (CDSL vs NSDL vs NSE cash) moves the headline
  by tens of thousands of crores.
