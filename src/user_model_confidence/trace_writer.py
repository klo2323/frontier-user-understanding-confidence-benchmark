from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_trace_outputs(
    request: dict[str, Any],
    result: dict[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    conversation_id = safe_filename(result["conversation_id"])
    json_path = output_dir / f"{conversation_id}.trace.json"
    markdown_path = output_dir / f"{conversation_id}.trace.md"

    json_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_markdown_trace(request, result),
        encoding="utf-8",
    )
    return json_path, markdown_path


def render_markdown_trace(request: dict[str, Any], result: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Confidence Trace: {result['conversation_id']}")
    lines.append("")
    lines.append("**Author / Project Owner:** Kelsey Ontko")
    lines.append("")
    lines.append("## Transcript")
    lines.append("")

    for turn in request.get("turns", []):
        turn_id = turn.get("turn_id", "unknown")
        speaker = turn.get("speaker", "unknown")
        text = turn.get("text", "")
        lines.append(f"- **{turn_id} / {speaker}:** {text}")

    lines.append("")
    lines.append("## Turn-by-Turn Scores")
    lines.append("")
    lines.append(
        "Each user turn shows Beta belief state, inferred value, evidence applied, "
        "aggregate confidence, predictive surprise, and final overall confidence."
    )
    lines.append("")

    for trace_item in result.get("confidence_trace", []):
        lines.extend(render_trace_item(trace_item))

    lines.append("## Calibration Notes")
    lines.append("")
    calibration_notes = result.get("calibration_notes") or []
    if not calibration_notes:
        lines.append("No ground truth labels were supplied, so no calibration notes were generated.")
    else:
        for note in calibration_notes:
            match = "yes" if note.get("matches_ground_truth") else "no"
            lines.append(
                f"- `{note['attribute']}`: inferred `{note.get('inferred_value')}`, "
                f"ground truth `{note.get('ground_truth')}`, "
                f"confidence `{note.get('confidence')}`, match `{match}`."
            )

    lines.append("")
    return "\n".join(lines)


def render_trace_item(trace_item: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    lines.append(f"### Turn {trace_item['turn']}")
    lines.append("")
    lines.append(f"> {trace_item['user_input']}")
    lines.append("")
    lines.append("#### Attribute Beliefs")
    lines.append("")
    lines.append("| Attribute | Value | Alpha | Beta | Confidence | Variance |")
    lines.append("|---|---|---:|---:|---:|---:|")

    for attribute, belief in trace_item.get("attribute_beliefs", {}).items():
        lines.append(
            f"| `{attribute}` | `{belief.get('value')}` | "
            f"{belief.get('alpha')} | {belief.get('beta')} | "
            f"{belief.get('confidence')} | {belief.get('variance')} |"
        )

    lines.append("")
    lines.append("#### Evidence Applied")
    lines.append("")
    evidence_applied = trace_item.get("evidence_applied") or []
    if not evidence_applied:
        lines.append("- No scored evidence was applied on this turn.")
    else:
        for evidence in evidence_applied:
            active = "active" if evidence.get("active") else "retracted"
            lines.append(
                f"- `{evidence['attribute']}` `{evidence['direction']}` "
                f"weight `{evidence['weight']}` from `{evidence['source']}` "
                f"value `{evidence.get('value')}` ({active})."
            )

    lines.append("")
    decision = trace_item.get("tailored_support_decision") or {}
    if decision:
        lines.append("#### Tailored Support Decision")
        lines.append("")
        lines.append(f"- Level: `{decision.get('tailored_support_level')}`")
        lines.append(f"- Recommended next move: `{decision.get('recommended_next_move')}`")
        lines.append(f"- Overreach risk: `{decision.get('overreach_risk')}`")
        lines.append(f"- Rationale: {decision.get('rationale')}")
        lines.append("")

    lines.append("#### Aggregate Calculation")
    lines.append("")
    lines.append(f"- Aggregate confidence: `{trace_item['aggregate_confidence']}`")
    lines.append(f"- Surprise: `{trace_item['surprise']}`")
    lines.append(f"- Average surprise: `{trace_item['average_surprise']}`")
    lines.append(f"- Contradictions so far: `{trace_item['contradictions']}`")
    lines.append(f"- Overall confidence: `{trace_item['overall_confidence']}`")
    lines.append("")
    return lines


def safe_filename(value: str) -> str:
    allowed = []
    for character in value:
        if character.isalnum() or character in {"-", "_"}:
            allowed.append(character)
        else:
            allowed.append("-")
    return "".join(allowed).strip("-") or "conversation"
