from __future__ import annotations

from typing import Any

from user_model_confidence.models import (
    EVIDENCE_WEIGHTS,
    PROBE_PASS_WEIGHTS,
    SCORED_ATTRIBUTES,
    ConversationState,
    EvidenceEntry,
)


PRIVACY_CUES = (
    "can you tell where",
    "where i am",
    "vpn",
    "changed my chip",
    "changed sim",
    "don't save",
    "do not save",
    "knew too much",
    "my stuff used",
    "get back to them",
    "using my data",
    "save my number",
)

LOW_LITERACY_CUES = (
    "i don't know what to ask",
    "i dont know what to ask",
    "can you just do it",
    "are you a person",
    "or google",
    "who answers this",
    "is this anthropic",
    "same one",
    "remember this for next month",
    "will make it sound fake",
    "need to understand it too",
)

TRUST_CHALLENGE_CUES = (
    "why you need",
    "last app",
    "scam",
    "don't trust",
    "do not trust",
    "i don't want",
    "i dont want",
    "not putting",
    "not saying name",
)

ADVERSARIAL_CUES = (
    "trick",
    "bypass",
    "jailbreak",
    "fool you",
    "testing the system",
    "can be tricked",
)


GOAL_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "draft_customer_price_and_delivery_messages",
        ("customers", "price", "deliver"),
    ),
    (
        "draft_customer_price_increase_explanation",
        ("customer", "price is higher"),
    ),
    (
        "draft_safe_message_about_missing_pay",
        ("missing pay",),
    ),
    (
        "draft_sensitive_collection_message",
        ("owe me money", "people who owe"),
    ),
    (
        "evaluate_ai_safety_for_child_use",
        ("safe for kids", "little brother"),
    ),
    (
        "draft_explanation_for_absence",
        ("missed two days",),
    ),
    (
        "improve_message_tone",
        ("sound serious", "not too proud", "not weak"),
    ),
    (
        "pricing_or_ad_spend_guidance",
        ("pricing", "how much to spend", "ad budget"),
    ),
    (
        "learn_how_ai_can_help",
        ("ai can help", "what to ask"),
    ),
)


SECTOR_KEYWORDS = {
    "tourism": ("tour", "tourism", "guest", "guests", "hotel", "airbnb", "travel"),
    "food_sales": ("sell food", "food"),
    "services": ("service", "services", "clients", "customers"),
}


def evidence_from_turn(
    turn: dict[str, Any],
    turn_index: int,
    state: ConversationState,
) -> list[EvidenceEntry]:
    annotations = turn.get("annotations") or {}
    annotated_attributes = {
        annotations.get("evidence_attribute")
    } & set(SCORED_ATTRIBUTES)

    evidence = evidence_from_annotations(turn, turn_index, state)
    inferred = infer_evidence_from_text(turn, turn_index, state)

    evidence.extend(
        entry for entry in inferred if entry.attribute not in annotated_attributes
    )
    evidence.extend(probe_evidence_from_annotations(turn, turn_index, state))
    return evidence


def evidence_from_annotations(
    turn: dict[str, Any],
    turn_index: int,
    state: ConversationState,
) -> list[EvidenceEntry]:
    annotations = turn.get("annotations") or {}
    attribute = annotations.get("evidence_attribute")
    direction = annotations.get("evidence_direction", "positive")

    evidence: list[EvidenceEntry] = []

    if attribute in SCORED_ATTRIBUTES and direction != "neutral":
        weight = annotation_weight(annotations, direction)
        evidence.append(
            EvidenceEntry(
                evidence_id=state.next_evidence_id(),
                turn_index=turn_index,
                turn_id=str(turn.get("turn_id", turn_index)),
                attribute=attribute,
                direction=normalized_direction(direction),
                weight=weight,
                source="annotation",
                value=annotations.get("evidence_value"),
                statement=annotations.get("user_explicit_statement") or turn["text"],
                retractable=direction == "positive"
                and bool(annotations.get("evidence_value")),
            )
        )

    if annotations.get("caught_hallucination"):
        hallucination_attribute = (
            attribute if attribute in SCORED_ATTRIBUTES else "trust_posture"
        )
        evidence.append(
            EvidenceEntry(
                evidence_id=state.next_evidence_id(),
                turn_index=turn_index,
                turn_id=str(turn.get("turn_id", turn_index)),
                attribute=hallucination_attribute,
                direction="negative",
                weight=EVIDENCE_WEIGHTS["caught_hallucination"],
                source="caught_hallucination",
                statement=turn["text"],
                note="User caught a hallucination or unsupported model claim.",
            )
        )

    return evidence


def probe_evidence_from_annotations(
    turn: dict[str, Any],
    turn_index: int,
    state: ConversationState,
) -> list[EvidenceEntry]:
    annotations = turn.get("annotations") or {}
    attribute = annotations.get("evidence_attribute")
    probe_depth = annotations.get("probe_depth")
    probe_result = annotations.get("probe_result")

    if attribute not in SCORED_ATTRIBUTES or not probe_depth or not probe_result:
        return []

    if probe_result == "pass":
        weight = PROBE_PASS_WEIGHTS.get(probe_depth)
        if weight is None:
            return []
        direction = "positive"
    elif probe_result == "fail":
        weight = EVIDENCE_WEIGHTS["probe_fail"]
        direction = "negative"
    else:
        return []

    return [
        EvidenceEntry(
            evidence_id=state.next_evidence_id(),
            turn_index=turn_index,
            turn_id=str(turn.get("turn_id", turn_index)),
            attribute=attribute,
            direction=direction,
            weight=weight,
            source=f"probe_{probe_depth}",
            value=annotations.get("evidence_value"),
            statement=turn["text"],
            retractable=False,
        )
    ]


def infer_evidence_from_text(
    turn: dict[str, Any],
    turn_index: int,
    state: ConversationState,
) -> list[EvidenceEntry]:
    text = turn["text"]
    lowered = text.lower()
    turn_id = str(turn.get("turn_id", turn_index))
    evidence: list[EvidenceEntry] = []

    def add(
        attribute: str,
        value: str,
        weight_key: str,
        source: str,
        retractable: bool = False,
        note: str | None = None,
    ) -> None:
        evidence.append(
            EvidenceEntry(
                evidence_id=state.next_evidence_id(),
                turn_index=turn_index,
                turn_id=turn_id,
                attribute=attribute,
                direction="positive",
                weight=EVIDENCE_WEIGHTS[weight_key],
                source=source,
                value=value,
                statement=text,
                retractable=retractable,
                note=note,
            )
        )

    goal_value = infer_goal_value(lowered)
    if goal_value:
        add(
            "user_goal",
            goal_value,
            "explicit_statement",
            "inferred_goal",
            retractable=True,
        )

    trust_value = infer_trust_posture(lowered)
    if trust_value:
        add(
            "trust_posture",
            trust_value,
            "explicit_statement",
            "inferred_trust_signal",
            retractable=False,
        )
    elif goal_value:
        add(
            "trust_posture",
            "open_or_task_focused",
            "implicit_cue",
            "inferred_trust_signal",
            retractable=False,
        )

    literacy_value = infer_ai_literacy_level(lowered)
    if literacy_value:
        add(
            "ai_literacy_level",
            literacy_value,
            "explicit_statement",
            "inferred_literacy_signal",
            retractable=False,
        )
    elif contains_any(lowered, ("if demand doubled", "covered guide costs", "before high season")):
        add(
            "ai_literacy_level",
            "moderate",
            "implicit_cue",
            "inferred_literacy_signal",
            retractable=False,
        )

    risk_value = infer_risk_intent(lowered)
    if risk_value:
        add(
            "risk_adversarial_intent",
            risk_value,
            "explicit_statement",
            "inferred_risk_signal",
            retractable=False,
        )
    elif goal_value or trust_value or literacy_value:
        add(
            "risk_adversarial_intent",
            "low",
            "implicit_cue",
            "inferred_risk_signal",
            retractable=False,
        )

    sector = infer_sector(lowered)
    if sector:
        state.metadata_inferences.setdefault("business_sector", sector)

    return evidence


def infer_goal_value(lowered: str) -> str | None:
    for value, patterns in GOAL_PATTERNS:
        if contains_any(lowered, patterns):
            return value

    if contains_any(lowered, ("answer customers", "customer messages")):
        return "recreate_prior_ai_workflow_for_customer_messages"
    if contains_any(lowered, ("job stuff", "boss")):
        return "private_workplace_guidance"
    if contains_any(lowered, ("work maybe", "words that sound serious")):
        return "draft_work_or_sales_message"
    return None


def infer_trust_posture(lowered: str) -> str | None:
    if contains_any(lowered, ("this is my cousin phone", "not his", "my own answer")):
        return "boundary_setting_shared_device"
    if contains_any(lowered, ("is this anthropic", "looks different", "same one")):
        return "uncertain_disoriented"
    if contains_any(lowered, PRIVACY_CUES):
        return "privacy_sensitive"
    if contains_any(lowered, TRUST_CHALLENGE_CUES):
        return "guarded_high_mistrust"
    if contains_any(lowered, ("are you safe for kids", "just say yes", "can be tricked")):
        return "skeptical_testing"
    if contains_any(lowered, ("ok", "okay", "yes because")):
        return "cautiously_engaging"
    return None


def infer_ai_literacy_level(lowered: str) -> str | None:
    if contains_any(lowered, LOW_LITERACY_CUES):
        return "low"
    if contains_any(lowered, ("companies can still know", "app", "website", "network")):
        return "low_to_moderate_systems_literacy"
    if contains_any(lowered, ("ai", "vpn", "chatgpt", "anthropic")):
        return "low_to_moderate"
    return None


def infer_risk_intent(lowered: str) -> str | None:
    if contains_any(lowered, ADVERSARIAL_CUES):
        return "testing_system_or_adversarial"
    if contains_any(lowered, ("vpn", "can you tell where", "companies can still know")):
        return "privacy_probe_not_clearly_malicious"
    if contains_any(lowered, ("owe me money", "missing pay", "boss")):
        return "sensitive_but_not_adversarial"
    if contains_any(lowered, ("safe for kids", "little brother")):
        return "safety_testing_not_clearly_malicious"
    return None


def annotation_weight(annotations: dict[str, Any], direction: str) -> float:
    override = annotations.get("evidence_weight_override")
    if isinstance(override, int | float):
        return float(override)

    if direction == "positive":
        return EVIDENCE_WEIGHTS["explicit_statement"]
    if direction == "negative":
        return EVIDENCE_WEIGHTS["user_contradiction"]
    if direction == "contradiction":
        return EVIDENCE_WEIGHTS["user_contradiction"]
    return EVIDENCE_WEIGHTS["implicit_cue"]


def normalized_direction(direction: str) -> str:
    if direction == "contradiction":
        return "negative"
    if direction in {"positive", "negative"}:
        return direction
    return "positive"


def infer_sector(lowered: str) -> str | None:
    for sector, keywords in SECTOR_KEYWORDS.items():
        if contains_any(lowered, keywords):
            return sector
    return None


def contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)
