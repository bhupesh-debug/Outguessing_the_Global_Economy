"""Tests for src/scoring.py — the ranking must reproduce the paper."""

import scoring


def test_ranking_reproduces_paper():
    rows = scoring.load_scores()
    ranked = [r["asset"] for r in scoring.rank_assets(rows)]
    assert ranked == [
        "India equities",
        "USD",
        "Gold",
        "India bonds",
        "US Treasuries",
        "Silver",
        "US equities",
    ]


def test_tie_break_gold_over_india_bonds():
    rows = scoring.load_scores()
    ranked = list(scoring.rank_assets(rows))
    gold = next(r for r in ranked if r["asset"] == "Gold")
    bonds = next(r for r in ranked if r["asset"] == "India bonds")
    assert gold["final_score"] == bonds["final_score"] == 57
    assert gold["computed_rank"] == 3
    assert bonds["computed_rank"] == 4
    # The tie-break is flow confirmation: gold Flow 62 > bonds Flow 50.
    assert gold["flow"] > bonds["flow"]


def test_three_score_mean_is_diagnostic_only():
    rows = scoring.load_scores()
    india = next(r for r in rows if r["asset"] == "India equities")
    assert abs(scoring.three_score_mean(india) - (72 + 48 + 50) / 3) < 1e-9
    # The mean (56.67) is NOT the published Final score (59) — the gap is
    # the six unpublished Part 13 components. The test pins that fact so
    # nobody "fixes" the mean to match the Final score.
    assert scoring.three_score_mean(india) != india["final_score"]


def test_strategic_expectation_never_enters_ranking():
    rows = scoring.load_scores()
    base = [r["asset"] for r in scoring.rank_assets(rows)]
    for r in rows:
        r["strategic_expectation"] = 0  # zero out the supplementary score
    assert [r["asset"] for r in scoring.rank_assets(rows)] == base
    for r in rows:
        r["strategic_expectation"] = 100  # max it out instead
    assert [r["asset"] for r in scoring.rank_assets(rows)] == base


def test_validation_passes():
    rows = scoring.load_scores()
    assert scoring.validate(rows) == []


def test_scores_in_range():
    rows = scoring.load_scores()
    for r in rows:
        for f in scoring.ALL_SCORE_FIELDS:
            assert 0 <= r[f] <= 100
