from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


SCORED_ATTRIBUTES = (
    "user_goal",
    "trust_posture",
    "ai_literacy_level",
    "risk_adversarial_intent",
)

DEFAULT_SALIENCE_WEIGHTS = {
    "user_goal": 0.30,
    "trust_posture": 0.25,
    "ai_literacy_level": 0.20,
    "risk_adversarial_intent": 0.25,
}

EVIDENCE_WEIGHTS = {
    "explicit_statement": 3.0,
    "reinforcement": 1.0,
    "implicit_cue": 0.5,
    "user_contradiction": 3.0,
    "probe_surface_recall": 1.0,
    "probe_synthesis": 2.0,
    "probe_counterfactual": 3.0,
    "probe_metacognitive": 4.0,
    "probe_fail": 2.0,
    "caught_hallucination": 4.0,
}

PROBE_PASS_WEIGHTS = {
    "surface_recall": EVIDENCE_WEIGHTS["probe_surface_recall"],
    "synthesis": EVIDENCE_WEIGHTS["probe_synthesis"],
    "counterfactual": EVIDENCE_WEIGHTS["probe_counterfactual"],
    "metacognitive": EVIDENCE_WEIGHTS["probe_metacognitive"],
}

MOVE_TAXONOMY = (
    "goal_statement",
    "privacy_concern",
    "system_boundary_probe",
    "ai_literacy_confusion",
    "trust_challenge",
    "contradiction",
    "question",
    "other",
)


@dataclass
class AttributeBelief:
    name: str
    alpha: float = 1.0
    beta: float = 1.0
    value: str | None = None

    @property
    def confidence(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    @property
    def variance(self) -> float:
        total = self.alpha + self.beta
        return (self.alpha * self.beta) / ((total**2) * (total + 1))

    def apply_positive(self, weight: float) -> None:
        self.alpha += weight

    def apply_negative(self, weight: float) -> None:
        self.beta += weight

    def retract_positive(self, weight: float) -> None:
        self.alpha = max(1.0, self.alpha - weight)

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "alpha": round(self.alpha, 6),
            "beta": round(self.beta, 6),
            "confidence": round(self.confidence, 6),
            "variance": round(self.variance, 6),
        }


@dataclass
class EvidenceEntry:
    evidence_id: str
    turn_index: int
    turn_id: str
    attribute: str
    direction: str
    weight: float
    source: str
    value: str | None = None
    statement: str | None = None
    active: bool = True
    retractable: bool = False
    retracted_by: str | None = None
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "turn_index": self.turn_index,
            "turn_id": self.turn_id,
            "attribute": self.attribute,
            "direction": self.direction,
            "weight": self.weight,
            "source": self.source,
            "value": self.value,
            "statement": self.statement,
            "active": self.active,
            "retractable": self.retractable,
            "retracted_by": self.retracted_by,
            "note": self.note,
        }


@dataclass
class ConversationState:
    beliefs: dict[str, AttributeBelief] = field(
        default_factory=lambda: {
            attribute: AttributeBelief(attribute) for attribute in SCORED_ATTRIBUTES
        }
    )
    evidence_ledger: list[EvidenceEntry] = field(default_factory=list)
    contradiction_events: list[dict[str, Any]] = field(default_factory=list)
    surprise_trace: list[dict[str, Any]] = field(default_factory=list)
    metadata_inferences: dict[str, Any] = field(default_factory=dict)

    def next_evidence_id(self) -> str:
        return f"ev_{len(self.evidence_ledger) + 1:04d}"

    def to_hidden_state(self) -> dict[str, Any]:
        return {
            "attributes": {
                name: belief.to_dict() for name, belief in self.beliefs.items()
            },
            "evidence_ledger": [entry.to_dict() for entry in self.evidence_ledger],
            "contradictions": self.contradiction_events,
            "surprise_trace": self.surprise_trace,
            "metadata_inferences": self.metadata_inferences,
        }


@dataclass
class CalibrationConfig:
    a: float = 1.2
    b: float = 0.7
    c: float = 0.35
    d: float = 0.0
    bias: float = 1.5
    calibration_t: float = 0.0
