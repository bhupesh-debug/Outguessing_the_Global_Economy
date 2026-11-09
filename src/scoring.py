"""Recompute and verify the Part 18 headline ranking from the paper's
published scores.

Source: Liquidity & Outgues Part 18, full article v2, Figure 3 (p. 17) and
Table 5 — three independent scores (Macro, Flow, Price/Valuation, each
0-100), the supplementary Strategic Expectation Score (0-100), and the
Final Asset Attractiveness Score (Part 13 weights: Macro 20%, Liquidity
15%, Actual flows 15%, Valuation 10%, Momentum 10%, Relative yield 10%,
Currency 10%, Historical analogue 5%, Risk/reward 5%).

HONEST LIMIT, READ THIS FIRST
------------------------------
The paper publishes the three scores, the Strategic Expectation Score and
the Final score — but NOT the six other Part 13 components (Liquidity,
Momentum, Relative yield, Currency, Historical analogue, Risk/reward) as
numbers. The Final score therefore CANNOT be recomputed from the published
inputs, and this module does not pretend otherwise. What it does:

1. Loads the published scores from data/scores.csv (inputs shown, not
   hidden inside code).
2. Recomputes the ranking from the published Final scores, applying the
   paper's stated tie-break: the gold / India-bonds tie at 57 is broken
   by flow confirmation in favour of gold. Implemented as "higher Flow
   wins a tie" (gold Flow 62 vs India bonds Flow 50).
3. Verifies the recomputed ranking against the paper's published rank.
4. Computes the three-score mean as a DIAGNOSTIC ONLY and shows that it
   does NOT reproduce the Final score — the gap is the six unpublished
   components. The mean is never presented as the Final score.
5. Keeps the Strategic Expectation Score strictly separate: it is a
   fourth, supplementary dimension and never enters the ranking.

Every score is a model estimate dated November 6, 2026.
"""

from __future__ import annotations

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SCORE_FIELDS = ("macro", "flow", "price_valuation")
ALL_SCORE_FIELDS = SCORE_FIELDS + ("strategic_expectation", "final_score")


def load_scores(path: str | Path = DATA_DIR / "scores.csv") -> list[dict]:
    """Load the published Figure 3 / Table 5 scores from CSV."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        out.append(
            {
                "asset": r["asset"],
                "macro": int(r["macro"]),
                "flow": int(r["flow"]),
                "price_valuation": int(r["price_valuation"]),
                "strategic_expectation": int(r["strategic_expectation"]),
                "final_score": int(r["final_score"]),
                "paper_rank": int(r["paper_rank"]),
            }
        )
    return out


def three_score_mean(row: dict) -> float:
    """Simple mean of Macro, Flow and Price/Valuation.

    Diagnostic only. The paper's Final score is NOT this mean: it embeds
    six further assessed components (Liquidity, Momentum, Relative yield,
    Currency, Historical analogue, Risk/reward) that the paper does not
    tabulate as numbers. See module docstring.
    """
    return sum(row[f] for f in SCORE_FIELDS) / len(SCORE_FIELDS)


def rank_assets(rows: list[dict]) -> list[dict]:
    """Rank assets by published Final score, highest first.

    Tie-break (the paper's rule, Table 5 caption): a tie on the Final
    score is broken by flow confirmation — the asset with the higher Flow
    score ranks first. This reproduces the paper's gold (#3) over
    India bonds (#4) at 57.
    """
    ranked = sorted(rows, key=lambda r: (-r["final_score"], -r["flow"]))
    for i, row in enumerate(ranked, start=1):
        row = dict(row)
        row["computed_rank"] = i
        yield row


def validate(rows: list[dict]) -> list[str]:
    """Check the published scores for internal consistency.

    Returns a list of problems (empty = all checks pass).
    """
    problems = []
    for r in rows:
        for f in ALL_SCORE_FIELDS:
            if not 0 <= r[f] <= 100:
                problems.append(f"{r['asset']}: {f}={r[f]} outside 0-100")
    ranked = list(rank_assets(rows))
    for r in ranked:
        if r["computed_rank"] != r["paper_rank"]:
            problems.append(
                f"{r['asset']}: computed rank {r['computed_rank']} != "
                f"paper rank {r['paper_rank']}"
            )
    finals = [r["final_score"] for r in rows]
    if len(set(finals)) != len(finals):
        # A tie exists; the tie-break rule must resolve it.
        tied = sorted({f for f in finals if finals.count(f) > 1})
        for t in tied:
            tied_rows = [r for r in rows if r["final_score"] == t]
            flows = [r["flow"] for r in tied_rows]
            if len(set(flows)) != len(flows):
                problems.append(
                    f"Final-score tie at {t} cannot be broken by Flow: "
                    f"flows {flows} are also tied"
                )
    return problems


def ranking_table(rows: list[dict]) -> list[dict]:
    """One row per asset: published scores, three-score mean (diagnostic),
    Final score and both ranks — so a reader can see exactly where the
    mean and the Final score disagree."""
    out = []
    for r in rank_assets(rows):
        out.append(
            {
                "rank": r["computed_rank"],
                "asset": r["asset"],
                "macro": r["macro"],
                "flow": r["flow"],
                "price_valuation": r["price_valuation"],
                "three_score_mean": round(three_score_mean(r), 2),
                "strategic_expectation_sep": r["strategic_expectation"],
                "final_score": r["final_score"],
                "paper_rank": r["paper_rank"],
            }
        )
    return out


def as_markdown(rows: list[dict]) -> str:
    lines = [
        "## Headline ranking — recomputed from the published scores",
        "",
        "Source: Part 18 v2, Figure 3 (p. 17) / Table 5. Model estimates, "
        "November 6, 2026. The three-score mean is a diagnostic only — it "
        "is NOT the Final score (see `src/scoring.py`). The Strategic "
        "Expectation Score is supplementary and never enters the ranking.",
        "",
        "| Rank | Asset | Macro | Flow | Price/Val. | 3-score mean | "
        "Strategic Exp. (sep.) | Final |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in ranking_table(rows):
        lines.append(
            f"| {r['rank']} | {r['asset']} | {r['macro']} | {r['flow']} | "
            f"{r['price_valuation']} | {r['three_score_mean']:.2f} | "
            f"{r['strategic_expectation_sep']} | {r['final_score']} |"
        )
    lines.append("")
    lines.append(
        "Tie at 57 (Gold vs India bonds) broken by flow confirmation in "
        "favour of Gold, per the paper (Gold Flow 62 vs India bonds Flow 50)."
    )
    return "\n".join(lines)


if __name__ == "__main__":
    rows = load_scores()
    problems = validate(rows)
    print(as_markdown(rows))
    print()
    if problems:
        print("VALIDATION PROBLEMS:")
        for p in problems:
            print(" -", p)
    else:
        print("Validation: all checks pass — recomputed ranking matches "
              "the paper's published rank.")
