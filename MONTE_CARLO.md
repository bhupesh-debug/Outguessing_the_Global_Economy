# Monte Carlo — 12-Month Outcomes for the Seven Part 18 Assets

**Status: actually run in code.** `src/monte_carlo.py`, 100,000 draws, fixed
seed `20261107`, fully deterministic — re-run `python src/run_all.py` and
every number below reproduces exactly. Results:
`results/monte_carlo_results.json` and `results/monte_carlo_results.csv`.

> **Warning, carried from the paper:** the method this simulation is built
> on FAILED its first backtest (top-1 hit rate 17.4% at 12 months, top-1
> portfolio CAGR −1.71% vs +8.07% equal-weight). These distributions
> describe the backtest window's observed return distributions under the
> paper's scenarios. They do not validate the ranking, and they are not a
> forecast. This is research and education, not investment advice.

## Method

1. **Return distributions (published, not invented).** Each asset's 12-month
   return is drawn from a Normal distribution with the OBSERVED mean and
   standard deviation of 12-month USD total returns in the backtest window
   (Table 7, full article v2, n=109 monthly decisions, Nov 2016–Oct 2025):

   | Asset | Observed mean 12M | Observed SD |
   |---|---:|---:|
   | India equities | +8.4% | ±19.5% |
   | USD | +0.4% | ±6.4% |
   | Gold | +16.3% | ±18.8% |
   | India bonds | +1.7% | ±4.3% |
   | US Treasuries | +1.3% | ±7.4% |
   | Silver | +21.0% | ±38.8% |
   | US equities | +13.8% | ±13.6% |

2. **Regimes (published probabilities).** Each draw picks a regime from the
   Table 9 scenario probabilities (model estimates, Nov 6, 2026):
   Bull 30%, Base 45%, Bear 25%. One regime per draw, shared across assets
   (a regime is a world state, not an asset state).
3. **Regime shifts (our assumption, stated).** Within a regime the mean
   shifts by Bull +0.5 SD, Base 0, Bear −0.5 SD. The ±0.5 SD shift is a
   modelling choice made here so the scenarios actually move the
   distribution; it is NOT published in the paper.
4. **Independence (the biggest simplification).** Draws are independent
   across assets — no cross-asset correlation. Real assets move together,
   so this widens the simulated spread of "who beats the peer median".
   The comparison table below shows exactly how far the simulated
   P(outperform) sits from the paper's empirical frequencies; read that
   gap as the price of the simplification.
5. **Normality.** Real 12-month returns have fat tails; a Normal
   understates extremes, so the P5/P95 ranges are narrower than history's.

## Results — 100,000 draws, seed 20261107

P(outperform) = share of draws in which the asset's 12-month return beats
the cross-sectional median of the seven assets in that draw — the same
"beat the peer median" definition Table 8 uses. "Empirical" is the paper's
Table 8 calibrated 12-month frequency (n=109, Wilson 95% CI).

| Asset | Median 12M | Mean 12M | P(loss) | P(outperform) | P5 (worst) | P95 (best) | Empirical 12M | Sim − empirical |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| India equities | +8.96% | +8.90% | 33.5% | 50.4% | −25.3% | +43.1% | 44% [35–53] | +6.4pp |
| USD | +0.60% | +0.60% | 46.4% | 15.3% | −10.6% | +11.8% | 28% [20–37] | −12.7pp |
| Gold | +16.70% | +16.73% | 20.3% | 67.5% | −16.2% | +49.8% | 69% [60–77] | −1.5pp |
| India bonds | +1.81% | +1.80% | 34.7% | 17.1% | −5.8% | +9.4% | 13% [8–20] | +4.1pp |
| US Treasuries | +1.50% | +1.50% | 42.4% | 19.7% | −11.5% | +14.5% | 16% [10–24] | +3.7pp |
| Silver | +21.81% | +22.01% | 29.8% | 63.6% | −46.1% | +90.5% | 54% [45–63] | +9.6pp |
| US equities | +14.05% | +14.08% | 16.5% | 66.4% | −9.5% | +37.9% | 77% [68–84] | −10.6pp |

How to read it, in plain language: imagine replaying the next 12 months
100,000 times under the paper's scenarios. In about half of those replays
India equities beat the middle asset of the seven; in about a third they
lost money. US equities lose money in only about 1 in 6 replays — the
lowest loss rate in the set — but their simulated outperformance (66.4%)
still sits 10.6 points below the empirical 77%, because the independence
assumption ignores the way US equities and the peer median move together.
Gold is the closest match to its empirical frequency (−1.5pp). Silver has
the widest range in the set (−46.1% to +90.5%): the highest median return
and the most violent outcomes, which is exactly what a high-beta metal
looks like in a simulation. India bonds are the narrowest: a 1.8% median
with a −5.8% to +9.4% range — the carry proxy's missing duration shows up
here as understated volatility, a known limitation of the paper's data.

## What the comparison says

The simulation does not contradict the paper — it reproduces its shape.
The simulated ranking by P(outperform) is Gold (67.5%), US equities
(66.4%), Silver (63.6%), India equities (50.4%), US Treasuries (19.7%),
India bonds (17.1%), USD (15.3%). The empirical ranking is US equities
(77%), Gold (69%), Silver (54%), India equities (44%), USD (28%),
US Treasuries (16%), India bonds (13%). The two agree on the top three
and the bottom three; they disagree on the order within them, and the
largest gaps (USD −12.7pp, US equities −10.6pp, Silver +9.6pp) are the
size of the independence assumption, not evidence about the market.

Note also that the simulated SDs run slightly above the input SDs (India
equities 20.83% vs the input 19.5%) because mixing three regimes adds
variance on top of each asset's own volatility. That is expected, not an
error.

## Limitations

- The regime shifts (±0.5 SD) are our assumption, not the paper's.
- Independence across assets is false in reality; see the comparison
  gaps above.
- Normality understates tail risk; the worst historical 12-month
  outcomes in the backtest (e.g., India equities −15.3% picked June 2025,
  silver −10.9% picked April 2021) sit inside these ranges, but a fatter
  tail would widen them.
- The input distributions are backward-looking (2016–2026, a decade
  dominated by US equities and gold). The next 12 months need not
  resemble them.
- As-of staleness: October US CPI prints November 10, 2026 and the Fed
  meets December 8–9. Either can change the regime — and therefore every
  number here.
