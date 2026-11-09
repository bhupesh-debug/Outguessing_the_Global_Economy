"""Consistency tests: every number printed in the Markdown docs and in
index.html must match the code's actual output (results/*.json).
If the code changes, the docs must be regenerated — these tests catch drift.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _norm(text: str) -> str:
    # Unicode minus (U+2212) and en-dash used in prose -> ASCII, and
    # collapse whitespace, so formatting differences don't mask real drift.
    return text.replace("\u2212", "-").replace("\u2013", "-")


def _load_json(name):
    return json.loads((ROOT / "results" / name).read_text())


def test_monte_carlo_md_matches_code_output():
    md = _norm((ROOT / "MONTE_CARLO.md").read_text())
    res = _load_json("monte_carlo_results.json")
    for asset, r in res["assets"].items():
        row = (
            f"| {asset} | +{r['median_12m_pct']:.2f}% | "
            f"+{r['mean_12m_pct']:.2f}% | {r['p_loss_pct']:.1f}% | "
            f"{r['p_outperform_pct']:.1f}% | {r['p5_pct']:.1f}% | "
            f"+{r['p95_pct']:.1f}% | {r['empirical_12m_outperform_pct']:.0f}% "
            f"[{r['empirical_ci'][0]:.0f}-{r['empirical_ci'][1]:.0f}] | "
            f"{r['sim_minus_empirical_pp']:+.1f}pp |"
        )
        assert row in md, f"MONTE_CARLO.md row drifted for {asset}:\n{row}"


def test_readme_mc_table_matches_code_output():
    md = _norm((ROOT / "README.md").read_text())
    res = _load_json("monte_carlo_results.json")
    for asset, r in res["assets"].items():
        row = (
            f"| {asset} | +{r['median_12m_pct']:.2f}% | "
            f"{r['p_loss_pct']:.1f}% | {r['p_outperform_pct']:.1f}% | "
            f"{r['p5_pct']:.1f}% | +{r['p95_pct']:.1f}% | "
            f"{r['empirical_12m_outperform_pct']:.0f}% |"
        )
        assert row in md, f"README.md MC row drifted for {asset}:\n{row}"


def test_scenarios_md_matches_code_output():
    md = _norm((ROOT / "SCENARIOS.md").read_text())
    ranges = _load_json("scenario_ranges.json")
    for asset, scen in ranges.items():
        for regime, vals in scen.items():
            row = (
                f"| {asset} | {vals['worst_p5_pct']:.1f}% | "
                f"{vals['base_centre_pct']:+.1f}% | "
                f"+{vals['best_p95_pct']:.1f}% |"
            )
            assert row in md, f"SCENARIOS.md range drifted for {asset}/{regime}:\n{row}"


def test_index_html_ranges_match_code_output():
    html = (ROOT / "index.html").read_text()
    ranges = _load_json("scenario_ranges.json")
    mc = _load_json("monte_carlo_results.json")
    for asset, scen in ranges.items():
        for regime in ("Bull", "Base", "Bear"):
            vals = scen[regime]
            for key in ("worst", "centre", "best"):
                src_key = {"worst": "worst_p5_pct", "centre": "base_centre_pct",
                           "best": "best_p95_pct"}[key]
                needle = f"{key}:{vals[src_key]}"
                assert needle in html, f"index.html missing {asset}/{regime}/{needle}"
    # Blended row in the page must equal the Python Monte Carlo output.
    for asset, r in mc["assets"].items():
        for key, val in (("worst", r["p5_pct"]), ("centre", r["median_12m_pct"]),
                         ("best", r["p95_pct"])):
            needle = f"{key}:{val}"
            assert needle in html, f"index.html Blended missing {asset}/{needle}"


def test_index_html_has_no_external_requests():
    html = (ROOT / "index.html").read_text()
    assert "http://" not in html and "https://" not in html
    assert "<img" not in html
    assert re.search(r"<link|@import|url\(|src=", html) is None
