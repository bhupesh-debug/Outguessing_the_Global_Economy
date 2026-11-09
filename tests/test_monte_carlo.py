"""Tests for src/monte_carlo.py — determinism, bounds, ordering."""

import monte_carlo


def test_deterministic_with_fixed_seed():
    a = monte_carlo.simulate(n=5_000, seed=20261107)
    b = monte_carlo.simulate(n=5_000, seed=20261107)
    assert a == b


def test_different_seed_changes_output():
    a = monte_carlo.simulate(n=5_000, seed=1)
    b = monte_carlo.simulate(n=5_000, seed=2)
    assert a["assets"]["Gold"]["median_12m_pct"] != b["assets"]["Gold"]["median_12m_pct"]


def test_probabilities_in_range():
    res = monte_carlo.simulate(n=20_000)
    for asset, r in res["assets"].items():
        assert 0 <= r["p_loss_pct"] <= 100, asset
        assert 0 <= r["p_outperform_pct"] <= 100, asset
        assert r["p5_pct"] <= r["median_12m_pct"] <= r["p95_pct"], asset


def test_regime_probabilities_sum_to_one():
    probs = monte_carlo.load_scenario_probs()
    assert abs(sum(probs.values()) - 1.0) < 1e-9
    assert probs == {"Bull": 0.30, "Base": 0.45, "Bear": 0.25}


def test_scenario_ranges_ordered_and_formula_correct():
    params = monte_carlo.load_return_params()
    ranges = monte_carlo.scenario_ranges(params)
    for asset, scen in ranges.items():
        for regime, vals in scen.items():
            assert vals["worst_p5_pct"] <= vals["base_centre_pct"] <= vals["best_p95_pct"]
    # Spot-check the formula for India equities, Base: centre = mean 8.4,
    # worst = 8.4 - 1.645*19.5 = -23.7, best = 8.4 + 1.645*19.5 = 40.5.
    ind = ranges["India equities"]["Base"]
    assert ind["base_centre_pct"] == 8.4
    assert ind["worst_p5_pct"] == round(8.4 - 1.645 * 19.5, 1)
    assert ind["best_p95_pct"] == round(8.4 + 1.645 * 19.5, 1)
    # Bull centre is mean + 0.5 SD; Bear is mean - 0.5 SD.
    assert ranges["India equities"]["Bull"]["base_centre_pct"] == round(8.4 + 0.5 * 19.5, 1)
    assert ranges["India equities"]["Bear"]["base_centre_pct"] == round(8.4 - 0.5 * 19.5, 1)


def test_us_equities_outperform_more_often_than_india_equities():
    # Sanity: higher observed mean (13.8 vs 8.4) and lower SD (13.6 vs
    # 19.5) should give US equities a higher simulated P(outperform).
    res = monte_carlo.simulate(n=20_000)
    assert (
        res["assets"]["US equities"]["p_outperform_pct"]
        > res["assets"]["India equities"]["p_outperform_pct"]
    )


def test_simulated_vs_empirical_comparison_is_recorded():
    res = monte_carlo.simulate(n=20_000)
    for asset, r in res["assets"].items():
        assert "empirical_12m_outperform_pct" in r
        assert "sim_minus_empirical_pp" in r
        assert abs(r["p_outperform_pct"] - r["empirical_12m_outperform_pct"]
                   - r["sim_minus_empirical_pp"]) < 0.15
