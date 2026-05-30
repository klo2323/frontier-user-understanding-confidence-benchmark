# Planning: User Model Confidence Scoring Engine

## Current Framing Note

This file is the original architecture plan for the confidence scoring engine. The current GitHub-facing MVP is recentered as a turn-by-turn benchmark for frontier-model user-understanding confidence. See `RESEARCH_POSITIONING.md`, `MVP_BRIEF.md`, and `README.md` for the current research framing.

**Author / Project Owner:** Kelsey Ontko  
**Work Attribution:** This planning document and research framework are Kelsey Ontko’s work.

## Project Summary

Build a scoring engine that measures how quickly and accurately an AI model forms a user profile inside a single conversation. The target use case is rapid ad/recommendation go/no-go decisions for high-entropy populations where long-term identity tracking is unreliable.

The engine outputs a turn-by-turn confidence trace for each conversation, emphasizing early accuracy by turns 3–8.

## Scenario Scope

### In Scope

- One fresh conversation per user.
- Rapid profiling within a single session.
- Per-turn confidence over user attributes.
- Explicit handling of contradictions and adversarial behavior.
- Optional human labels for calibration and partial evidence annotation.
- API wrapper for scoring raw or partially annotated transcripts.

### Out of Scope

- Long-term user memory.
- Cross-device identity resolution.
- Multi-session decay functions.
- Direct use of ground truth inside live confidence scoring.
- Revenue-tier scoring as part of the confidence formula.

## Core Question

Can the system measure, on each conversation turn, how confidently the model understands:

- whether the user is legitimate or adversarial;
- what the user needs;
- whether the model can predict the user’s next move;
- whether confidence is calibrated against actual accuracy?

## Primary Outputs

For each conversation, the engine should produce:

- `confidence_trace`: per-turn confidence values and supporting signals.
- `hidden_state`: inferred attributes, evidence ledger, contradictions, and probe results.
- `calibration_notes`: post-hoc notes when ground truth is supplied.

## Attribute Model

Each scored attribute uses a Beta distribution.

```text
alpha = 1 + sum(positive_evidence_weights)
beta = 1 + sum(negative_evidence_weights)
confidence = alpha / (alpha + beta)
variance = alpha * beta / ((alpha + beta)^2 * (alpha + beta + 1))
```

### Scored Attributes

| Attribute | Purpose | Live Scored |
|---|---|---|
| `business_legitimacy` | Whether the user appears to represent a real business or not. | Yes |
| `adversarial_intent` | Whether the user appears genuine, misleading, boundary-testing, or mistrustful. | Yes |
| `primary_user_need` | What the user appears to want from the conversation. | Yes |

### Metadata Attributes

| Attribute | Purpose | Live Scored |
|---|---|---|
| `business_sector` | Used for filtering, segmentation, and research cohort selection. | No |
| `revenue_tier` | Optional future metadata for filtering or study design. | No |

## Evidence Weights

| Signal | Update |
|---|---:|
| Explicit statement | `alpha += 3` |
| Reinforcement on later turn | `alpha += 1` |
| Implicit cue / inference | `alpha += 0.5` |
| User contradiction | `beta += 3` |
| Probe pass: surface recall | `alpha += 1` |
| Probe pass: synthesis | `alpha += 2` |
| Probe pass: counterfactual | `alpha += 3` |
| Probe pass: metacognitive | `alpha += 4` |
| Probe fail | `beta += 2` |
| Caught hallucination | `beta += 4` |

## Probe Depths

| Probe Depth | Definition | Weight |
|---|---|---:|
| `surface_recall` | User recalls a fact they previously stated. | `+1` |
| `synthesis` | User combines previous facts into a new inference. | `+2` |
| `counterfactual` | User reasons about a hypothetical that conflicts with stated facts. | `+3` |
| `metacognitive` | User reflects on their own reasoning, confidence, or what would change their mind. | `+4` |

Labeler-supplied probe labels override inferred labels. Missing probe labels are inferred by the same NLU pass used for evidence classification and predictive surprise.

## Contradiction Policy

Use Policy B: contradiction retraction.

When a new turn contradicts an earlier explicit statement on the same attribute:

1. Reverse the earlier positive evidence by subtracting its original `alpha` contribution.
2. Add negative evidence for the contradiction with `beta += 3`.
3. Record the retraction in the evidence ledger.
4. Recompute the attribute confidence immediately for the current turn.

Contradiction detection runs every turn against prior explicit statements for the same attribute.

## Aggregate Confidence

Aggregate confidence uses a weighted geometric mean over salient scored attributes.

```text
C_t = product(E[a_i] ^ w_i)
```

This intentionally penalizes weak links. A low-confidence core attribute should pull the whole score down even when other attributes look strong.

## Predictive Surprise

Before each user turn, the model emits a probability distribution over likely next user moves.

```text
surprise_t = -log(P_model(user_turn_t | history))
avg_surprise_t = running_average(surprise_1..surprise_t)
```

Lower surprise indicates better trajectory modeling. Spikes should appear around contradictions, topic shifts, or adversarial reveals.

## Overall Confidence

```text
overall_t = sigmoid(
  a * log(C_t)
  - b * avg_surprise_t
  - c * contradictions_t
  + d * calibration_t
)
```

Hyperparameters `a`, `b`, `c`, and `d` are tuned only on labeled calibration data.

## Ground Truth Schema

Ground truth is used for calibration and validation, not direct live scoring.

### Conversation-Level Labels

| Field | Values | Purpose |
|---|---|---|
| `business_legitimacy` | `legitimate_business`, `casual_browsing`, `adversarial_testing`, `scam_probe` | Calibrates legitimacy confidence. |
| `business_sector` | `agriculture`, `retail`, `hospitality`, `tourism`, `real_estate`, `property_management`, `services`, `manufacturing`, `transport`, `fintech`, `education`, `other` | Metadata for filtering cohorts. |
| `adversarial_intent` | `genuine_user`, `deliberately_misleading`, `testing_system`, `high_mistrust` | Primary ground truth signal. |
| `primary_user_need` | `product_discovery`, `pricing_info`, `compliance_help`, `market_validation`, `fraud_testing`, `learning_only` | Validates need inference. |

### Turn-Level Optional Labels

| Field | Purpose |
|---|---|
| `user_explicit_statement` | Human-supplied evidence statement, if present. |
| `evidence_attribute` | Attribute affected by the evidence. |
| `evidence_direction` | Positive, negative, contradiction, or neutral. |
| `evidence_weight_override` | Optional labeler override for engine defaults. |
| `probe_depth` | Human-supplied probe depth classification. |
| `probe_result` | Pass, fail, ambiguous, or not applicable. |

## API Plan

### Endpoint

```http
POST /score-conversation
```

### Input Shape

```json
{
  "conversation_id": "string",
  "user_id": "string",
  "conversation_metadata": {},
  "turns": [
    {
      "turn_id": "string",
      "speaker": "user",
      "text": "string",
      "timestamp": "string",
      "annotations": {
        "user_explicit_statement": "string",
        "evidence_attribute": "adversarial_intent",
        "probe_depth": "metacognitive",
        "probe_result": "pass"
      }
    }
  ],
  "ground_truth_labels": {}
}
```

### Output Shape

```json
{
  "conversation_id": "string",
  "confidence_trace": [
    {
      "turn": 3,
      "user_input": "I sell crafts online from my home.",
      "attribute_confidences": {
        "business_legitimacy": 0.72,
        "adversarial_intent": 0.89,
        "primary_user_need": 0.61
      },
      "aggregate_confidence": 0.70,
      "surprise": 0.18,
      "overall_confidence": 0.72
    }
  ],
  "hidden_state": {},
  "calibration_notes": []
}
```

## Schema Strictness

Use strict schemas for objects the scoring engine reads directly:

- root request object;
- `turns` items;
- `annotations`;
- explicit evidence objects.

Use flexible schemas for metadata objects expected to evolve:

- `conversation_metadata`;
- `ground_truth_labels`;
- future research tags.

## Implementation Phases

### Phase 1: Labeling Workflow

- Define transcript import format.
- Build or stub a labeling interface.
- Support conversation-level ground truth.
- Support optional turn-level evidence and probe labels.
- Label 30–50 conversations across sectors.
- Track inter-rater agreement for adversarial intent.

### Phase 2: Scoring Engine

- Implement Beta distribution state per scored attribute.
- Implement evidence ledger with reversible evidence entries.
- Implement Policy B contradiction retraction.
- Implement probe-depth-weighted updates.
- Compute per-turn aggregate confidence.
- Add hidden-state trace export for debugging.

### Phase 3: Predictive Surprise

- Define next-turn move taxonomy.
- Emit predicted distribution before each user turn.
- Score observed user turn against predicted distribution.
- Track running average surprise.
- Surface surprise spikes in the trace.

### Phase 4: Calibration

- Run labeled conversations through the scorer.
- Compare predicted confidence to ground truth correctness.
- Fit calibration curve.
- Tune `a`, `b`, `c`, and `d`.
- Save calibration parameters as versioned artifacts.

### Phase 5: API Wrapper

- Implement `POST /score-conversation`.
- Validate strict request fields.
- Accept flexible metadata fields.
- Run inference fallback for missing annotations.
- Return confidence trace, hidden state, and calibration notes.

### Phase 6: Held-Out Validation

- Score held-out labeled conversations.
- Measure calibration error.
- Measure adversarial detection by turn 5.
- Measure sector inference separately as non-scored metadata.
- Compare labeled-rich vs. labeled-sparse trace quality.

## Engineering Task Breakdown

### Data Structures

- `AttributeBelief`: `alpha`, `beta`, `confidence`, `variance`.
- `EvidenceEntry`: turn id, attribute, direction, weight, source, retractable flag.
- `ConversationState`: active beliefs, evidence ledger, contradictions, surprise trace.
- `ConfidenceTraceItem`: user turn output with confidence fields.
- `CalibrationConfig`: hyperparameters and calibration metadata.

### Core Functions

- `initializeBeliefs(attributes)`
- `classifyEvidence(turn, history)`
- `classifyProbeDepth(turn, history)`
- `detectContradictions(turn, evidenceLedger)`
- `applyEvidence(state, evidenceEntry)`
- `retractEvidence(state, evidenceEntry)`
- `computeAggregateConfidence(attributeBeliefs, salienceWeights)`
- `computeSurprise(predictedDistribution, observedTurn)`
- `computeOverallConfidence(inputs, calibrationConfig)`
- `scoreConversation(request)`

### Suggested Module Layout

```text
src/
  scoring/
    beta.ts
    evidence.ts
    contradiction.ts
    aggregate.ts
    surprise.ts
    overall.ts
    scoreConversation.ts
  schemas/
    scoreConversationRequest.ts
    scoreConversationResponse.ts
  calibration/
    fitCalibration.ts
    metrics.ts
  labeling/
    types.ts
tests/
  scoring/
  calibration/
fixtures/
  conversations/
  labels/
```

## Test Plan

### Unit Tests

- Beta confidence and variance calculations.
- Evidence application by signal type.
- Probe-depth weight application.
- Contradiction retraction removes original alpha contribution.
- Aggregate confidence penalizes low-confidence attributes.
- Overall confidence responds correctly to surprise and contradictions.

### Fixture Tests

- Genuine user with consistent business details.
- Casual browser with vague need.
- Deliberately misleading user with mid-conversation contradiction.
- High-mistrust user who withholds details but answers metacognitive probes.
- Scam probe attempting to trigger overconfident recommendations.

### Calibration Tests

- Confidence bins match observed accuracy within target tolerance.
- Held-out calibration error is below `0.1`.
- Adversarial detection precision by turn 5 exceeds `0.85`.
- Labeled-sparse traces remain close to labeled-rich traces.

## Success Metrics

| Metric | Target |
|---|---:|
| Mean absolute calibration error | `< 0.1` |
| Adversarial detection precision by turn 5 | `> 0.85` |
| Sector accuracy by turn 6 for genuine users | Track only |
| Surprise behavior | Decreases smoothly unless contradiction/topic shift occurs |

## Key Risks

| Risk | Mitigation |
|---|---|
| Labeler disagreement on adversarial intent | Use inter-rater checks and adjudication. |
| Early deception leaves residual confidence | Use contradiction retraction instead of additive-only penalties. |
| Inference fallback drifts from human labels | Compare labeled-rich and labeled-sparse traces continuously. |
| Hyperparameters overfit one sector | Validate across sectors and consider sector-specific configs later. |
| Model becomes overconfident on vague users | Reward low confidence when evidence is insufficient. |

## Open Decisions

- Which implementation language and web framework should host the API?
- What taxonomy should predictive surprise use for “next user moves”?
- Should salience weights be fixed globally or inferred per conversation?
- How should ambiguous contradictions be represented before full retraction?
- What minimum trace quality is required before ad serving is allowed?
- Should `business_sector` ever influence salience weights while remaining unscored?

## Recommended Next Step

Start with a small TypeScript or Python prototype that scores annotated fixture conversations without an API. Once the scoring trace is stable and inspectable, add inference fallback and the HTTP wrapper.
