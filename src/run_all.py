"""Run the full pipeline end to end and write every generated artefact
into results/:

- results/ranking_check.md      — recomputed headline ranking + validation
- results/backtest_summary.md   — backtest headline table, reproduced
- results/monte_carlo_results.json / .csv — Monte Carlo output
- results/scenario_ranges.json  — best/base/worst ranges per asset/scenario

Deterministic: the Monte Carlo uses a fixed seed, so a clean re-run
reproduces every number.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import backtest_summary
import monte_carlo
import scoring

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    rows = scoring.load_scores()
    problems = scoring.validate(rows)
    ranking_md = scoring.as_markdown(rows)
    if problems:
        ranking_md += "\n\nVALIDATION PROBLEMS:\n" + "\n".join(
            f"- {p}" for p in problems
        )
    else:
        ranking_md += (
            "\n\nValidation: all checks pass — recomputed ranking matches "
            "the paper's published rank."
        )
    (RESULTS / "ranking_check.md").write_text(ranking_md, encoding="utf-8")

    (RESULTS / "backtest_summary.md").write_text(
        backtest_summary.as_markdown(), encoding="utf-8"
    )

    res = monte_carlo.simulate()
    jp, cp = monte_carlo.save_results(res, RESULTS)
    rp = monte_carlo.save_scenario_ranges(RESULTS)

    print("Pipeline complete.")
    print(f" - {RESULTS / 'ranking_check.md'}")
    print(f" - {RESULTS / 'backtest_summary.md'}")
    print(f" - {jp}")
    print(f" - {cp}")
    print(f" - {rp}")
    if problems:
        print("VALIDATION PROBLEMS:", problems)
    else:
        print("Ranking validation: PASS")


if __name__ == "__main__":
    main()
