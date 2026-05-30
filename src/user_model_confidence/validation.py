from __future__ import annotations

from typing import Any


ROOT_ALLOWED_KEYS = {
    "conversation_id",
    "user_id",
    "conversation_metadata",
    "turns",
    "ground_truth_labels",
}

TURN_ALLOWED_KEYS = {
    "turn_id",
    "speaker",
    "text",
    "timestamp",
    "annotations",
}

ANNOTATION_ALLOWED_KEYS = {
    "user_explicit_statement",
    "evidence_attribute",
    "evidence_direction",
    "evidence_value",
    "evidence_weight_override",
    "probe_depth",
    "probe_result",
    "caught_hallucination",
    "salience_weights",
}

VALID_SPEAKERS = {"user", "assistant", "model", "system"}


def validate_score_request(request: dict[str, Any]) -> None:
    if not isinstance(request, dict):
        raise ValueError("Request must be a JSON object.")

    extra_root_keys = set(request) - ROOT_ALLOWED_KEYS
    if extra_root_keys:
        raise ValueError(f"Unexpected root keys: {sorted(extra_root_keys)}")

    if "conversation_id" not in request or not isinstance(
        request["conversation_id"], str
    ):
        raise ValueError("conversation_id is required and must be a string.")

    if "user_id" not in request or not isinstance(request["user_id"], str):
        raise ValueError("user_id is required and must be a string.")

    turns = request.get("turns")
    if not isinstance(turns, list):
        raise ValueError("turns is required and must be an array.")

    for index, turn in enumerate(turns, start=1):
        validate_turn(turn, index)


def validate_turn(turn: dict[str, Any], index: int) -> None:
    if not isinstance(turn, dict):
        raise ValueError(f"turns[{index}] must be an object.")

    extra_turn_keys = set(turn) - TURN_ALLOWED_KEYS
    if extra_turn_keys:
        raise ValueError(f"Unexpected keys in turns[{index}]: {sorted(extra_turn_keys)}")

    speaker = turn.get("speaker")
    if speaker not in VALID_SPEAKERS:
        raise ValueError(
            f"turns[{index}].speaker must be one of {sorted(VALID_SPEAKERS)}."
        )

    text = turn.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"turns[{index}].text is required and must be non-empty.")

    annotations = turn.get("annotations")
    if annotations is not None:
        validate_annotations(annotations, index)


def validate_annotations(annotations: dict[str, Any], turn_index: int) -> None:
    if not isinstance(annotations, dict):
        raise ValueError(f"turns[{turn_index}].annotations must be an object.")

    extra_annotation_keys = set(annotations) - ANNOTATION_ALLOWED_KEYS
    if extra_annotation_keys:
        raise ValueError(
            f"Unexpected keys in turns[{turn_index}].annotations: "
            f"{sorted(extra_annotation_keys)}"
        )
