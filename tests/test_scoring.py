from __future__ import annotations

import json
import unittest
from pathlib import Path

from user_model_confidence.models import AttributeBelief, ConversationState
from user_model_confidence.scorer import (
    compute_aggregate_confidence,
    score_conversation,
)
from user_model_confidence.trace_writer import render_markdown_trace


class ScoringEngineTests(unittest.TestCase):
    def test_beta_belief_confidence_and_variance(self) -> None:
        belief = AttributeBelief("user_goal")

        self.assertEqual(belief.confidence, 0.5)

        belief.apply_positive(3)
        self.assertAlmostEqual(belief.confidence, 0.8)
        self.assertGreater(belief.variance, 0)

    def test_sample_fixture_scores_conversation(self) -> None:
        fixture_path = Path("fixtures/conversations/sample_tourism_user.json")
        request = json.loads(fixture_path.read_text(encoding="utf-8"))

        result = score_conversation(request)

        self.assertEqual(result["conversation_id"], "sample-tourism-001")
        self.assertEqual(len(result["confidence_trace"]), 3)
        final_trace = result["confidence_trace"][-1]
        self.assertEqual(
            final_trace["inferred_values"]["user_goal"],
            "pricing_or_ad_spend_guidance",
        )
        self.assertEqual(
            final_trace["inferred_values"]["risk_adversarial_intent"],
            "low",
        )
        self.assertEqual(
            result["hidden_state"]["metadata_inferences"]["business_sector"],
            "tourism",
        )
        self.assertIn("attribute_beliefs", final_trace)
        self.assertIn("evidence_applied", final_trace)
        self.assertIn("tailored_support_decision", final_trace)
        self.assertTrue(result["calibration_notes"])

    def test_contradiction_retracts_prior_explicit_evidence(self) -> None:
        request = {
            "conversation_id": "contradiction-001",
            "user_id": "anon-user-002",
            "turns": [
                {
                    "turn_id": "t1",
                    "speaker": "user",
                    "text": "I need help writing a customer price message.",
                    "timestamp": "2026-05-02T10:00:00Z",
                    "annotations": {
                        "evidence_attribute": "user_goal",
                        "evidence_direction": "positive",
                        "evidence_value": "draft_customer_price_message",
                    },
                },
                {
                    "turn_id": "t2",
                    "speaker": "user",
                    "text": "Actually, I need help asking about missing pay.",
                    "timestamp": "2026-05-02T10:00:30Z",
                    "annotations": {
                        "evidence_attribute": "user_goal",
                        "evidence_direction": "positive",
                        "evidence_value": "draft_safe_message_about_missing_pay",
                    },
                },
            ],
        }

        result = score_conversation(request)
        ledger = result["hidden_state"]["evidence_ledger"]
        retracted_entries = [
            entry
            for entry in ledger
            if entry["attribute"] == "user_goal" and not entry["active"]
        ]

        self.assertTrue(retracted_entries)
        self.assertEqual(len(result["hidden_state"]["contradictions"]), 1)
        self.assertEqual(
            result["confidence_trace"][-1]["inferred_values"]["user_goal"],
            "draft_safe_message_about_missing_pay",
        )

    def test_annotation_overrides_inferred_attribute(self) -> None:
        request = {
            "conversation_id": "annotation-001",
            "user_id": "anon-user-003",
            "turns": [
                {
                    "turn_id": "t1",
                    "speaker": "user",
                    "text": "I need pricing and cost details.",
                    "timestamp": "2026-05-02T10:00:00Z",
                    "annotations": {
                        "evidence_attribute": "user_goal",
                        "evidence_direction": "positive",
                        "evidence_value": "compare_cost_options",
                        "user_explicit_statement": "User needs cost comparison help.",
                    },
                }
            ],
        }

        result = score_conversation(request)

        self.assertEqual(
            result["confidence_trace"][-1]["inferred_values"]["user_goal"],
            "compare_cost_options",
        )

    def test_aggregate_confidence_penalizes_weak_links(self) -> None:
        state = ConversationState()
        state.beliefs["user_goal"].alpha = 10
        state.beliefs["trust_posture"].alpha = 10
        state.beliefs["ai_literacy_level"].alpha = 10
        state.beliefs["risk_adversarial_intent"].beta = 8

        aggregate = compute_aggregate_confidence(state)

        self.assertLess(aggregate, 0.8)

    def test_markdown_trace_renders_transcript_scores_and_decision(self) -> None:
        fixture_path = Path("fixtures/conversations/sample_tourism_user.json")
        request = json.loads(fixture_path.read_text(encoding="utf-8"))
        result = score_conversation(request)

        markdown = render_markdown_trace(request, result)

        self.assertIn("# Confidence Trace: sample-tourism-001", markdown)
        self.assertIn("## Transcript", markdown)
        self.assertIn("## Turn-by-Turn Scores", markdown)
        self.assertIn("I run a small tour company near Cancun", markdown)
        self.assertIn("Tailored Support Decision", markdown)
        self.assertIn("Aggregate confidence", markdown)

    def test_high_entropy_scenario_scores_new_dimensions(self) -> None:
        fixture_path = Path(
            "evals/scenarios/fixtures/07_vpn_detectability_probe.json"
        )
        request = json.loads(fixture_path.read_text(encoding="utf-8"))

        result = score_conversation(request)
        final_trace = result["confidence_trace"][-1]

        self.assertEqual(
            final_trace["inferred_values"]["user_goal"],
            "draft_safe_message_about_missing_pay",
        )
        self.assertIn(
            final_trace["inferred_values"]["trust_posture"],
            {"privacy_sensitive", "cautiously_engaging"},
        )
        self.assertIn("tailored_support_decision", final_trace)

    def test_strict_root_validation_rejects_extra_keys(self) -> None:
        request = {
            "conversation_id": "bad-001",
            "user_id": "anon-user-004",
            "unexpected": True,
            "turns": [
                {
                    "turn_id": "t1",
                    "speaker": "user",
                    "text": "Hello",
                    "timestamp": "2026-05-02T10:00:00Z",
                }
            ],
        }

        with self.assertRaises(ValueError):
            score_conversation(request)


if __name__ == "__main__":
    unittest.main()
