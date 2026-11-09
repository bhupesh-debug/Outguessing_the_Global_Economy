# Scenarios — Base, Bull, Bear, and the Surprise Overlays

Source: Part 18 v2, Table 9 (scenarios) and Table 13 (next three moves).
Scenario probabilities are **model estimates, November 6, 2026** — model
judgements, not market-implied odds. Per-asset ranges are computed by
`src/monte_carlo.py` from the Table 7 observed mean/SD with the stated
±0.5 SD regime shifts (`results/scenario_ranges.json`): Best = centre +
1.645 SD, Base = centre, Worst = centre − 1.645 SD (a 90% interval under
the Normal assumption). All figures are model estimates, not forecasts.

## The three scenarios (Table 9)

| Scenario | Probability | Trigger | Capital-flow consequence | Asset-price consequence |
|---|---:|---|---|---|
| **Bull: rotation completes** | 30% | Oct CPI soft Nov 10; Fed signals pause; FPI buying broadens | FPI returns to India at scale; dollar tops | India equities lead; gold recovers; US Treasuries rally |
| **Base: grinding transition** | 45% | CPI in line; Dec hike delivered; rotation stays selective | FPI trickle continues; DII anchors India | India equities grind higher; US equities range-bound; dollar firm |
| **Bear: hike + energy shock** | 25% | CPI hot; Brent breaks $110; Strait of Hormuz disruption | FPI reverses; flight to USD and cash | US equities fall; INR weakens; gold rises on safety, then falls on real yields |

## Per-asset 12-month ranges by scenario

Best / centre / worst, in percent. "Centre" is the scenario-adjusted mean;
worst and best are the 5th and 95th percentiles of that scenario's
distribution.

### Bull — rotation completes (30%)

| Asset | Worst (P5) | Centre | Best (P95) |
|---|---:|---:|---:|
| India equities | −13.9% | +18.1% | +50.2% |
| USD | −6.9% | +3.6% | +14.1% |
| Gold | −5.2% | +25.7% | +56.6% |
| India bonds | −3.2% | +3.8% | +10.9% |
| US Treasuries | −7.2% | +5.0% | +17.2% |
| Silver | −23.4% | +40.4% | +104.2% |
| US equities | −1.8% | +20.6% | +43.0% |

### Base — grinding transition (45%)

| Asset | Worst (P5) | Centre | Best (P95) |
|---|---:|---:|---:|
| India equities | −23.7% | +8.4% | +40.5% |
| USD | −10.1% | +0.4% | +10.9% |
| Gold | −14.6% | +16.3% | +47.2% |
| India bonds | −5.4% | +1.7% | +8.8% |
| US Treasuries | −10.9% | +1.3% | +13.5% |
| Silver | −42.8% | +21.0% | +84.8% |
| US equities | −8.6% | +13.8% | +36.2% |

### Bear — hike + energy shock (25%)

| Asset | Worst (P5) | Centre | Best (P95) |
|---|---:|---:|---:|
| India equities | −33.4% | −1.3% | +30.7% |
| USD | −13.3% | −2.8% | +7.7% |
| Gold | −24.0% | +6.9% | +37.8% |
| India bonds | −7.5% | −0.4% | +6.6% |
| US Treasuries | −14.6% | −2.4% | +9.8% |
| Silver | −62.2% | +1.6% | +65.4% |
| US equities | −15.4% | +7.0% | +29.4% |

Reading the tables: even in the Bear scenario, the centres for Gold
(+6.9%) and US equities (+7.0%) stay positive — the backtest decade was
kind to both, and the scenario shift (−0.5 SD) is not enough to drag
their centres below zero. Conversely, even in the Bull scenario, India
equities' worst case is −13.9%: a good regime does not remove the
asset's own volatility. Silver's Bull best (+104.2%) is the widest
single number in the project — a reminder that the ±38.8% SD behind it
is doing most of the work, not the scenario.

## The next three possible moves (Table 13)

Same probabilities as the scenarios, re-expressed as the outguessing
discipline demands — trigger, expected response, counterresponse,
consequences:

| # | Trigger | Probability | Expected response | Counterresponse | Capital-flow consequence | Asset-price consequence |
|---|---|---:|---|---|---|---|
| 1 | Oct CPI soft on Nov 10 | 35% | Fed signals pause; hike odds collapse | Investors rotate back into duration and growth | FPI returns to India at scale; dollar tops | India equities lead; gold recovers; US Treasuries rally |
| 2 | Dec hike delivered; CPI in line | 45% | Fed hikes 25bp; guidance neutral | Market absorbs it; rotation stays selective | FPI trickle continues; DII anchors India | India grinds higher; US equities range-bound; dollar firm |
| 3 | CPI hot + Brent above $110 | 20% | Fed hikes; RBI hikes again; risk-off | Flight to USD and cash; EM stress | FPI reverses; gold safety bid vs real-yield drag | US equities fall; INR weakens; gold volatile |

Note the difference between the two probability sets: Table 9's scenarios
(30/45/25) and Table 13's moves (35/45/20) are two framings of the same
judgement, not two independent estimates. Move 1 (soft CPI) is a little
more likely than the Bull scenario because a soft print helps even if the
rotation does not fully complete; Move 3 (hot CPI + Brent >$110) is a
little less likely than the Bear scenario because it requires two things
to go wrong at once.

## Surprise overlays — what is NOT in the three scenarios

The three scenarios cover the scheduled path (CPI, Fed, Brent). These
overlays are the paper's own named risks, stated qualitatively — **no
probability is published for them in the paper, and none is invented
here**:

1. **The Strait of Hormuz stays closed past March 2027.** The IMF's
   October 2026 outlook assumes it reopens by March 2027 and oil averages
   about $96 in 2026. If either assumption fails, the growth picture
   changes first in the oil importers, India prominent among them. Pushes
   toward Bear; the India engine's single most important external
   variable is the oil price.
2. **A December Fed hold — the dovish surprise.** The market prices a
   ~76–78% chance of a December hike; the Fed has given no such guidance.
   A hold would collapse hike odds, weaken the dollar, and rally duration
   and gold. Pushes toward Bull, and it is the mirror image of the
   expectation gap: the market is more certain than the Fed is.
3. **FPI returns to India at scale.** Simulation C's probability weighting
   is trickle-back 50%, return at scale 30%, continued exit 20%. A
   return at scale would confirm the early-rotation signal (flows changed
   before price) and push toward Bull; a renewed exit pushes toward Bear
   and is one leg of the invalidation trio.
4. **Faster US–China decoupling.** Tariffs, semiconductor competition and
   supply-chain diversification continue on a slow, grinding path in the
   paper's base case. An escalation would favour diversified manufacturing
   hubs (India, Southeast Asia) and gold as a hedge, and punish
   single-market exporters and tariff-exposed supply chains.
5. **A US tech earnings break.** The AI-concentration regime is the
   paper's central rotation story: crowded US growth is the #1 loser in
   the winners/losers ranking. An earnings break would accelerate the
   rotation out of it — toward dollars, short-duration safety, and
   selectively India — and would confirm the valuation regime the paper
   describes (a price problem, not a growth problem).

## What changes the call

- **November 10, 2026 — October US CPI.** The scheduled moment the
  expectation gap closes. Soft → Move 1 / Bull; in line → Move 2 / Base;
  hot → Move 3 / Bear, and one leg of the invalidation trio.
- **Brent crude vs $110.** Above it, with a hot CPI and renewed FPI
  selling, the thesis is invalidated (see HYPOTHESIS.md).
- **November FPI flows (NSDL/CDSL).** A negative month turns the
  late-October buying into a positional trade that reversed — the third
  leg of the invalidation trio.
- **December 8–9 FOMC.** Hike vs hold decides whether the market or the
  incentive was right about the Fed gap.
