from __future__ import annotations

import math
from typing import Any

from user_model_confidence.evidence import contains_any
from user_model_confidence.models import MOVE_TAXONOMY, ConversationState


def classify_user_move(text: str) -> str:
    lowered = text.lower()

    if contains_any(
        lowered,
        (
            "actually",
            "i lied",
            "not true",
            "made that up",
            "instead",
            "rather than",
        ),
    ):
        return "contradiction"

    if contains_any(
        lowered,
        ("can you tell where", "vpn", "don't save", "knew too much", "my stuff used"),
    ):
        return "privacy_concern"

    if contains_any(
        lowered,
        ("is this anthropic", "are you a person", "or google", "same one", "changed my chip"),
    ):
        return "ai_literacy_confusion"

    if contains_any(
        lowered,
        ("safe for kids", "trick", "bypass", "jailbreak", "can be tricked"),
    ):
        return "system_boundary_probe"

    if contains_any(
        lowered,
        ("why you need", "scam", "don't trust", "do not trust", "last app"),
    ):
        return "trust_challenge"

    if contains_any(
        lowered,
        (
            "customer",
            "price",
            "missing pay",
            "words",
            "message",
            "work",
            "school",
            "boss",
            "safe for kids",
        ),
    ):
        return "goal_statement"

    if "?" in text:
        return "question"

    return "other"


def predict_next_moves(
    history: list[dict[str, Any]],
    state: ConversationState,
) -> dict[str, float]:
    distribution = {
        "goal_statement": 0.24,
        "privacy_concern": 0.12,
        "system_boundary_probe": 0.08,
        "ai_literacy_confusion": 0.14,
        "trust_challenge": 0.10,
        "contradiction": 0.04,
        "question": 0.18,
        "other": 0.10,
    }

    if not any(turn.get("speaker") == "user" for turn in history):
        return normalize(distribution)

    last_assistant_text = next(
        (
            turn.get("text", "").lower()
            for turn in reversed(history)
            if turn.get("speaker") in {"assistant", "model"}
        ),
        "",
    )

    if contains_any(last_assistant_text, ("what", "which", "kind", "context", "need")):
        distribution["goal_statement"] += 0.12
        distribution["question"] -= 0.03

    if contains_any(last_assistant_text, ("privacy", "details", "general", "save")):
        distribution["privacy_concern"] += 0.08
        distribution["trust_challenge"] += 0.04

    if state.contradiction_events:
        distribution["contradiction"] += 0.10
        distribution["trust_challenge"] += 0.05
        distribution["system_boundary_probe"] += 0.04

    return normalize(distribution)


def compute_surprise(distribution: dict[str, float], observed_move: str) -> float:
    probability = max(distribution.get(observed_move, 0.001), 0.001)
    return -math.log(probability)


def normalize(distribution: dict[str, float]) -> dict[str, float]:
    clipped = {key: max(value, 0.001) for key, value in distribution.items()}
    total = sum(clipped.values())
    return {key: clipped.get(key, 0.001) / total for key in MOVE_TAXONOMY}
