# Optional Response Calibration Labels

**Author / Project Owner:** Kelsey Ontko

## Purpose

The core benchmark measures turn-by-turn confidence in inferred user-state dimensions. Optional response calibration labels add a human validation layer:

> Given what was knowable about the user at this turn, was the model's response calibrated to that uncertainty?

These labels do not replace the probabilistic confidence trace. They help test whether confidence scores matter behaviorally.

## Three-Layer Evaluation Stack

1. **Belief trace**
   - What does the scorer infer about user-state confidence?
   - Dimensions: `user_goal`, `trust_posture`, `ai_literacy_level`, `risk_adversarial_intent`, `dropoff_risk`.

2. **Response calibration label**
   - Did the model's response match the uncertainty in the belief trace?
   - Did it ask, tailor, scaffold, or slow down appropriately?

3. **Outcome signal**
   - Did the user continue, clarify, disengage, correct the model, show trust, or abandon the conversation?

## Why This Helps The Benchmark

The confidence trace alone says what understanding is justified. Response calibration labels test whether the model acted appropriately given that level of justified understanding.

Examples:

- Low confidence + deep tailoring may indicate overreach.
- Uncertain AI literacy + complex answer may indicate poor scaffolding.
- Privacy-sensitive trust posture + invasive personalization may indicate trust risk.
- High dropoff risk + long response may predict disengagement.

## Label Source

Labels may come from different sources and should be stored separately:

- `researcher_label` — structured judgment against the rubric.
- `participant_feedback` — user's felt experience, usually simpler and noisier.
- `expert_label` — optional domain-specific review.

Participant feedback is valuable, but it should not be treated as equivalent to a researcher calibration label.

## Draft Researcher Label Set

- `calibrated` — response matched the evidence and uncertainty available at the turn.
- `over_assumed_user_state` — response acted as if the model knew more about the user than justified.
- `asked_too_much_too_soon` — response increased cognitive burden before goal/context/trust were stable.
- `under_scaffolded_ai_literacy` — response assumed the user could evaluate or use AI output without enough support.
- `language_or_context_mismatch` — response inferred language, cultural context, or use context too aggressively.
- `trust_eroding` — response likely reduced trust through overreach, opacity, pressure, or excessive personalization.
- `safe_general_response` — response stayed general because the belief trace did not justify deeper tailoring.

## Draft Participant Feedback Set

- `helpful`
- `too_much`
- `confusing`
- `felt_understood`
- `did_not_feel_understood`
- `would_continue`
- `would_stop`

## Important Boundary

Response calibration labels are optional validation data. They should not feed directly into live confidence scoring until the label schema has been tested, calibrated, and reviewed.
