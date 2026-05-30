# Confidence Trace: scenario-18-my-friend-said-proxy-framing

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What can I help with?
- **t2 / user:** my friend said I should ask AI if this message is okay.
- **t3 / assistant:** I can help check tone and clarity. Is the message from you or your friend?
- **t4 / user:** from me. but friend said it's too harsh.
- **t5 / assistant:** What do you want the message to achieve?
- **t6 / user:** tell cousin pay me back. not start fight.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> my friend said I should ask AI if this message is okay.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `cautiously_engaging` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `trust_posture` `positive` weight `3.0` from `inferred_trust_signal` value `cautiously_engaging` (active).
- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low_to_moderate` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.646576`
- Surprise: `1.427116`
- Average surprise: `1.427116`
- Contradictions so far: `0`
- Overall confidence: `0.494435`

### Turn 4

> from me. but friend said it's too harsh.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `cautiously_engaging` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `low_to_moderate` | 7.0 | 1.0 | 0.875 | 0.012153 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low_to_moderate` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.675838`
- Surprise: `2.302585`
- Average surprise: `1.864851`
- Contradictions so far: `0`
- Overall confidence: `0.431543`

### Turn 6

> tell cousin pay me back. not start fight.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `cautiously_engaging` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `low_to_moderate` | 7.0 | 1.0 | 0.875 | 0.012153 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.675838`
- Surprise: `2.388763`
- Average surprise: `2.039488`
- Contradictions so far: `0`
- Overall confidence: `0.40184`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `revise_repayment_message_to_avoid_conflict`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `cautiously_engaging`, ground truth `uncertain_and_proxy_framed`, confidence `0.8`, match `no`.
- `ai_literacy_level`: inferred `low_to_moderate`, ground truth `moderate`, confidence `0.875`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `sensitive_but_not_adversarial`, confidence `0.666667`, match `no`.
