from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from user_model_confidence.scorer import score_conversation
from user_model_confidence.trace_writer import write_trace_outputs


DIMENSIONS = (
    "user_goal",
    "trust_posture",
    "ai_literacy_level",
    "risk_adversarial_intent",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run scenario fixtures through the scorer.")
    parser.add_argument("--fixtures-dir", type=Path, default=Path("evals/scenarios/fixtures"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/scenario_batch_20"))
    parser.add_argument("--report", type=Path, default=Path("reports/scenario_batch_20_diagnostic.md"))
    parser.add_argument("--csv", type=Path, default=Path("evals/results/scenario_batch_20_summary.csv"))
    args = parser.parse_args()

    fixture_paths = sorted(args.fixtures_dir.glob("*.json"))
    if not fixture_paths:
        print(f"No fixtures found in {args.fixtures_dir}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.csv.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for fixture_path in fixture_paths:
        request = json.loads(fixture_path.read_text(encoding="utf-8"))
        result = score_conversation(request)
        write_trace_outputs(request, result, args.output_dir)
        final = result["confidence_trace"][-1] if result["confidence_trace"] else {}
        labels = request.get("ground_truth_labels", {})
        inferred = final.get("inferred_values", {})
        decision = final.get("tailored_support_decision", {})
        row = {
            "fixture": fixture_path.name,
            "conversation_id": request["conversation_id"],
            "user_turns": sum(1 for turn in request["turns"] if turn["speaker"] == "user"),
            "session_outcome": request.get("conversation_metadata", {}).get("session_outcome", "not_specified"),
            "overall_confidence": final.get("overall_confidence"),
            "aggregate_confidence": final.get("aggregate_confidence"),
            "tailored_support_level": decision.get("tailored_support_level"),
            "recommended_next_move": decision.get("recommended_next_move"),
            "overreach_risk": decision.get("overreach_risk"),
        }
        mismatch_count = 0
        for dimension in DIMENSIONS:
            row[f"expected_{dimension}"] = labels.get(dimension)
            row[f"inferred_{dimension}"] = inferred.get(dimension)
            row[f"confidence_{dimension}"] = final.get("attribute_confidences", {}).get(dimension)
            if labels.get(dimension) != inferred.get(dimension):
                mismatch_count += 1
        row["dimension_mismatch_count"] = mismatch_count
        rows.append(row)

    write_csv(args.csv, rows)
    args.report.write_text(render_report(rows, args.output_dir, args.csv), encoding="utf-8")
    print(f"ran {len(rows)} scenarios")
    print(f"wrote traces: {args.output_dir}")
    print(f"wrote report: {args.report}")
    print(f"wrote csv: {args.csv}")
    return 0


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_report(rows: list[dict[str, object]], output_dir: Path, csv_path: Path) -> str:
    lines = []
    lines.append("# Scenario Batch 20 Diagnostic")
    lines.append("")
    lines.append("**Author / Project Owner:** Kelsey Ontko")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("Run the current scorer across all 20 synthetic high-entropy scenario fixtures before making additional scorer changes.")
    lines.append("")
    lines.append("These scenario-author labels are diagnostic only. They are not researcher/labeler calibration claims.")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    lines.append(f"- Trace directory: `{output_dir}`")
    lines.append(f"- CSV summary: `{csv_path}`")
    lines.append("")
    lines.append("## Batch Summary")
    lines.append("")
    total = len(rows)
    avg_mismatch = sum(int(row["dimension_mismatch_count"]) for row in rows) / total
    avg_overreach = sum(float(row["overreach_risk"] or 0) for row in rows) / total
    lines.append(f"- Scenarios run: `{total}`")
    lines.append(f"- Average dimension mismatch count: `{avg_mismatch:.2f}` of 4")
    lines.append(f"- Average overreach risk: `{avg_overreach:.2f}`")
    lines.append("")
    lines.append("## Scenario Table")
    lines.append("")
    lines.append("| Fixture | Turns | Mismatches | Support Level | Next Move | Overreach |")
    lines.append("|---|---:|---:|---|---|---:|")
    for row in rows:
        lines.append(
            f"| `{row['fixture']}` | {row['user_turns']} | {row['dimension_mismatch_count']} | "
            f"`{row['tailored_support_level']}` | `{row['recommended_next_move']}` | {row['overreach_risk']} |"
        )
    lines.append("")
    lines.append("## Highest Mismatch Cases")
    lines.append("")
    for row in sorted(rows, key=lambda item: int(item["dimension_mismatch_count"]), reverse=True)[:8]:
        lines.append(f"### `{row['fixture']}`")
        lines.append("")
        lines.append(f"- Mismatches: `{row['dimension_mismatch_count']}` of 4")
        lines.append(f"- Final next move: `{row['recommended_next_move']}`")
        lines.append(f"- Overreach risk: `{row['overreach_risk']}`")
        for dimension in DIMENSIONS:
            lines.append(
                f"- `{dimension}`: expected `{row[f'expected_{dimension}']}`, "
                f"inferred `{row[f'inferred_{dimension}']}`, "
                f"confidence `{row[f'confidence_{dimension}']}`"
            )
        lines.append("")
    lines.append("## Initial Interpretation")
    lines.append("")
    lines.append("Use this report to identify scorer update patterns across all scenarios instead of overfitting to one scenario.")
    lines.append("")
    lines.append("Likely areas to inspect:")
    lines.append("")
    lines.append("- Whether trust/privacy states are sticky enough across later cooperation.")
    lines.append("- Whether goal refinement is being treated as contradiction when it should be progressive clarification.")
    lines.append("- Whether AI-literacy signals are too broad or too sticky.")
    lines.append("- Whether risk labels need composite states for privacy probe plus sensitive benign use.")
    lines.append("- Whether dropoff metadata needs a future session-level evidence model.")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
