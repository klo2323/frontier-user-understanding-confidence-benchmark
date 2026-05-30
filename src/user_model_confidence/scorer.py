from __future__ import annotations

import math
from typing import Any

from user_model_confidence.evidence import evidence_from_turn
from user_model_confidence.models import (
    DEFAULT_SALIENCE_WEIGHTS,
    EVIDENCE_WEIGHTS,
    SCORED_ATTRIBUTES,
    CalibrationConfig,
    ConversationState,
    EvidenceEntry,
)
from user_model_confidence.surprise import (
    classify_user_move,
    compute_surprise,
    predict_next_moves,
)
from user_model_confidence.validation import validate_score_request


def score_conversation(
    request: dict[str, Any],
    calibration_config: CalibrationConfig | None = None,
) -> dict[str, Any]:
    validate_score_request(request)

    config = calibration_config or CalibrationConfig()
    state = ConversationState()
    confidence_trace: list[dict[str, Any]] = []
    history: list[dict[str, Any]] = []

    for turn_index, turn in enumerate(request["turns"], start=1):
        if turn["speaker"] != "user":
            history.append(turn)
            continue

        prediction = predict_next_moves(history, state)
        observed_move = classify_user_move(turn["text"])
        surprise = compute_surprise(prediction, observed_move)
        state.surprise_trace.append(
            {
                "turn": turn_index,
                "observed_move": observed_move,
                "prediction": round_distribution(prediction),
                "surprise": round(surprise, 6),
            }
        )

        ledger_start_index = len(state.evidence_ledger)
        for entry in evidence_from_turn(turn, turn_index, state):
            apply_evidence_with_retraction(state, entry)
        evidence_applied = [
            entry.to_dict() for entry in state.evidence_ledger[ledger_start_index:]
        ]

        aggregate_confidence = compute_aggregate_confidence(
            state,
            salience_weights_from_turn(turn),
        )
        average_surprise = sum(item["surprise"] for item in state.surprise_trace) / len(
            state.surprise_trace
        )
        overall_confidence = compute_overall_confidence(
            aggregate_confidence=aggregate_confidence,
            average_surprise=average_surprise,
            contradiction_count=len(state.contradiction_events),
            config=config,
        )
        tailored_support_decision = compute_tailored_support_decision(state)

        confidence_trace.append(
            {
                "turn": turn_index,
                "user_input": turn["text"],
                "attribute_beliefs": {
                    name: state.beliefs[name].to_dict() for name in SCORED_ATTRIBUTES
                },
                "attribute_confidences": {
                    name: round(state.beliefs[name].confidence, 6)
                    for name in SCORED_ATTRIBUTES
                },
                "attribute_variances": {
                    name: round(state.beliefs[name].variance, 6)
                    for name in SCORED_ATTRIBUTES
                },
                "evidence_applied": evidence_applied,
                "inferred_values": {
                    name: state.beliefs[name].value for name in SCORED_ATTRIBUTES
                },
                "aggregate_confidence": round(aggregate_confidence, 6),
                "surprise": round(surprise, 6),
                "average_surprise": round(average_surprise, 6),
                "contradictions": len(state.contradiction_events),
                "overall_confidence": round(overall_confidence, 6),
                "tailored_support_decision": tailored_support_decision,
            }
        )

        history.append(turn)

    return {
        "conversation_id": request["conversation_id"],
        "confidence_trace": confidence_trace,
        "hidden_state": state.to_hidden_state(),
        "calibration_notes": calibration_notes(
            request.get("ground_truth_labels"),
            state,
        ),
    }


def apply_evidence_with_retraction(
    state: ConversationState,
    entry: EvidenceEntry,
) -> None:
    if (
        entry.direction == "positive"
        and entry.retractable
        and entry.value
        and entry.attribute in state.beliefs
    ):
        retract_conflicting_explicit_evidence(state, entry)

    apply_evidence(state, entry)
    recompute_attribute_value(state, entry.attribute)


def retract_conflicting_explicit_evidence(
    state: ConversationState,
    new_entry: EvidenceEntry,
) -> None:
    for prior_entry in list(state.evidence_ledger):
        if not prior_entry.active:
            continue
        if not prior_entry.retractable:
            continue
        if prior_entry.direction != "positive":
            continue
        if prior_entry.attribute != new_entry.attribute:
            continue
        if prior_entry.value == new_entry.value:
            continue
        if prior_entry.turn_index >= new_entry.turn_index:
            continue

        contradiction_id = state.next_evidence_id()
        state.beliefs[prior_entry.attribute].retract_positive(prior_entry.weight)
        prior_entry.active = False
        prior_entry.retracted_by = contradiction_id

        contradiction_entry = EvidenceEntry(
            evidence_id=contradiction_id,
            turn_index=new_entry.turn_index,
            turn_id=new_entry.turn_id,
            attribute=new_entry.attribute,
            direction="negative",
            weight=EVIDENCE_WEIGHTS["user_contradiction"],
            source="contradiction_retraction",
            value=new_entry.value,
            statement=new_entry.statement,
            active=True,
            retractable=False,
            note=f"Retracted {prior_entry.evidence_id} with value {prior_entry.value}.",
        )
        apply_evidence(state, contradiction_entry)
        state.contradiction_events.append(
            {
                "turn": new_entry.turn_index,
                "attribute": new_entry.attribute,
                "previous_evidence_id": prior_entry.evidence_id,
                "previous_value": prior_entry.value,
                "new_value": new_entry.value,
                "contradiction_evidence_id": contradiction_id,
            }
        )


def apply_evidence(state: ConversationState, entry: EvidenceEntry) -> None:
    if entry.attribute not in state.beliefs:
        return

    existing_ids = {ledger_entry.evidence_id for ledger_entry in state.evidence_ledger}
    if not entry.evidence_id or entry.evidence_id in existing_ids:
        entry.evidence_id = state.next_evidence_id()

    if entry.direction == "positive":
        state.beliefs[entry.attribute].apply_positive(entry.weight)
    elif entry.direction == "negative":
        state.beliefs[entry.attribute].apply_negative(entry.weight)

    state.evidence_ledger.append(entry)


def recompute_attribute_value(state: ConversationState, attribute: str) -> None:
    if attribute not in state.beliefs:
        return

    active_positive_entries = [
        entry
        for entry in state.evidence_ledger
        if entry.attribute == attribute
        and entry.active
        and entry.direction == "positive"
        and entry.value
    ]

    if not active_positive_entries:
        state.beliefs[attribute].value = None
        return

    best_entry = max(
        active_positive_entries,
        key=lambda entry: (entry.weight, entry.turn_index),
    )
    state.beliefs[attribute].value = best_entry.value



def compute_tailored_support_decision(state: ConversationState) -> dict[str, Any]:
    goal = state.beliefs["user_goal"]
    trust = state.beliefs["trust_posture"]
    literacy = state.beliefs["ai_literacy_level"]
    risk = state.beliefs["risk_adversarial_intent"]

    if risk.value in {"testing_system_or_adversarial"} and risk.confidence >= 0.6:
        return {
            "tailored_support_level": "hold",
            "recommended_next_move": "hold_or_refuse",
            "rationale": "Risk or adversarial intent is too high for tailored support.",
            "overreach_risk": 0.9,
        }

    if trust.value in {
        "privacy_sensitive",
        "guarded_high_mistrust",
        "uncertain_disoriented",
    } and trust.confidence >= 0.65:
        return {
            "tailored_support_level": "low",
            "recommended_next_move": "build_trust_or_explain_system_limits",
            "rationale": "Trust or system-boundary uncertainty should be stabilized before deeper tailoring.",
            "overreach_risk": 0.65,
        }

    if literacy.value in {"low", "low_to_moderate", "low_to_moderate_systems_literacy"} and literacy.confidence >= 0.65:
        return {
            "tailored_support_level": "low",
            "recommended_next_move": "explain_ai_use",
            "rationale": "The user likely needs AI-literacy scaffolding before complex tailored help.",
            "overreach_risk": 0.55,
        }

    if not goal.value or goal.confidence < 0.65:
        return {
            "tailored_support_level": "none",
            "recommended_next_move": "ask_goal_or_context",
            "rationale": "The user's goal is not clear enough for tailored support.",
            "overreach_risk": 0.75,
        }

    if risk.value in {
        "privacy_probe_not_clearly_malicious",
        "sensitive_but_not_adversarial",
        "safety_testing_not_clearly_malicious",
    }:
        return {
            "tailored_support_level": "low_to_moderate",
            "recommended_next_move": "give_general_guidance_with_boundaries",
            "rationale": "A goal is emerging, but privacy, safety, or sensitivity signals limit how deeply the model should tailor.",
            "overreach_risk": 0.45,
        }

    if goal.confidence >= 0.75 and risk.value == "low":
        return {
            "tailored_support_level": "moderate",
            "recommended_next_move": "give_tailored_guidance",
            "rationale": "The user's goal is clear enough and risk signals are low enough for bounded tailored help.",
            "overreach_risk": 0.25,
        }

    return {
        "tailored_support_level": "low",
        "recommended_next_move": "give_general_guidance_or_ask_context",
        "rationale": "Some user signal is available, but not enough for confident tailored support.",
        "overreach_risk": 0.5,
    }

def compute_aggregate_confidence(
    state: ConversationState,
    salience_weights: dict[str, float] | None = None,
) -> float:
    weights = salience_weights or DEFAULT_SALIENCE_WEIGHTS
    total_weight = sum(weights.get(attribute, 0.0) for attribute in SCORED_ATTRIBUTES)
    if total_weight <= 0:
        weights = DEFAULT_SALIENCE_WEIGHTS
        total_weight = sum(weights.values())

    weighted_log_sum = 0.0
    for attribute in SCORED_ATTRIBUTES:
        normalized_weight = weights.get(attribute, 0.0) / total_weight
        confidence = max(state.beliefs[attribute].confidence, 0.001)
        weighted_log_sum += normalized_weight * math.log(confidence)

    return math.exp(weighted_log_sum)


def compute_overall_confidence(
    aggregate_confidence: float,
    average_surprise: float,
    contradiction_count: int,
    config: CalibrationConfig,
) -> float:
    signal = (
        config.bias
        + config.a * math.log(max(aggregate_confidence, 0.001))
        - config.b * average_surprise
        - config.c * contradiction_count
        + config.d * config.calibration_t
    )
    return 1.0 / (1.0 + math.exp(-signal))


def salience_weights_from_turn(turn: dict[str, Any]) -> dict[str, float] | None:
    annotations = turn.get("annotations") or {}
    salience_weights = annotations.get("salience_weights")
    if not isinstance(salience_weights, dict):
        return None
    return {
        attribute: float(weight)
        for attribute, weight in salience_weights.items()
        if attribute in SCORED_ATTRIBUTES and isinstance(weight, int | float)
    }


def calibration_notes(
    ground_truth_labels: dict[str, Any] | None,
    state: ConversationState,
) -> list[dict[str, Any]]:
    if not ground_truth_labels:
        return []

    notes: list[dict[str, Any]] = []
    for attribute in SCORED_ATTRIBUTES:
        if attribute not in ground_truth_labels:
            continue

        inferred_value = state.beliefs[attribute].value
        ground_truth = ground_truth_labels[attribute]
        notes.append(
            {
                "attribute": attribute,
                "inferred_value": inferred_value,
                "ground_truth": ground_truth,
                "confidence": round(state.beliefs[attribute].confidence, 6),
                "matches_ground_truth": inferred_value == ground_truth,
            }
        )

    return notes


def round_distribution(distribution: dict[str, float]) -> dict[str, float]:
    return {key: round(value, 6) for key, value in distribution.items()}
