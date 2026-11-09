"""Tests for src/backtest_summary.py — the reproduced failure must match
the paper's figures exactly."""

import backtest_summary


def test_headline_figures_match_paper():
    h = backtest_summary.headline()
    assert float(h["cagr_pct"]["top1_portfolio"]) == -1.71
    assert float(h["cagr_pct"]["equal_weight_benchmark"]) == 8.07
    assert float(h["sharpe"]["top1_portfolio"]) == -0.33
    assert float(h["sharpe"]["equal_weight_benchmark"]) == 0.67
    assert float(h["max_drawdown_pct"]["top1_portfolio"]) == -31.5
    assert float(h["max_drawdown_pct"]["equal_weight_benchmark"]) == -11.8
    assert float(h["hit_rate_12m_pct"]["top1_portfolio"]) == 17.4
    assert float(h["rank_ic"]["top1_portfolio"]) == -0.202
    assert int(h["decisions"]["top1_portfolio"]) == 120
    assert int(h["us_equities_ranked_first_count"]["top1_portfolio"]) == 0


def test_hit_rates_by_horizon():
    rates = {r["horizon_months"]: r for r in backtest_summary.hit_rates()}
    assert rates[1] == {"horizon_months": 1, "hit_rate_pct": 31.7, "n": 120}
    assert rates[3] == {"horizon_months": 3, "hit_rate_pct": 29.7, "n": 118}
    assert rates[6] == {"horizon_months": 6, "hit_rate_pct": 26.1, "n": 115}
    assert rates[12] == {"horizon_months": 12, "hit_rate_pct": 17.4, "n": 109}


def test_component_ics():
    comps = {c["component"]: c["ic"] for c in backtest_summary.components()}
    assert comps["Macro"] == -0.408
    assert comps["Analogue"] == 0.298
    assert comps["Momentum"] == 0.001
    assert comps["Valuation"] == 0.147
    assert comps["Relative yield"] == -0.336
    assert comps["Liquidity"] == -0.285
    # Analogue best, Macro worst.
    ordered = backtest_summary.components()
    assert ordered[0]["component"] == "Macro"
    assert ordered[-1]["component"] == "Analogue"


def test_mechanical_crosscheck_is_near_reverse_of_judgemental_ranking():
    cc = backtest_summary.mechanical_crosscheck_nov6()
    assert cc[0] == {"asset": "USD", "backtest_score_v1": 55.2}
    assert cc[-1] == {"asset": "Gold", "backtest_score_v1": 23.1}
    # Judgemental #1 (India equities, 59) sits 4th mechanically at 47.3.
    india = next(c for c in cc if c["asset"] == "India equities")
    assert india["backtest_score_v1"] == 47.3


def test_derived_gaps():
    g = backtest_summary.derived_gaps()
    assert g["hit_rate_gap_vs_random_pp"] == -32.6
    assert g["cagr_gap_pp"] == -9.78
    assert g["sharpe_gap"] == -1.0
    assert g["max_drawdown_gap_pp"] == -19.7
