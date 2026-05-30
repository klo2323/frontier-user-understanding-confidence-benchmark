# Confidence Trace: scenario-02-deleted-prior-ai-app-workflow

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What do you want help with today?
- **t2 / user:** I deleted the other AI. it used to answer customers for me. can this one do that?
- **t3 / assistant:** It can help write customer replies, but it may not know what the other app knew. What kind of messages were you answering?
- **t4 / user:** people ask if I still have stock. sometimes I say yes then later no. I need it not to sound bad.
- **t5 / assistant:** Okay. Do you want a short reply for when stock is uncertain?
- **t6 / user:** yes short. not like company. just normal.
- **t7 / assistant:** Got it. I can make it normal and short. What product are they asking about?
- **t8 / user:** don't put product. just make the words.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> I deleted the other AI. it used to answer customers for me. can this one do that?

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_customer_price_and_delivery_messages` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `user_goal` `positive` weight `3.0` from `inferred_goal` value `draft_customer_price_and_delivery_messages` (active).
- `trust_posture` `positive` weight `0.5` from `inferred_trust_signal` value `open_or_task_focused` (active).
- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low_to_moderate` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.69282`
- Surprise: `1.427116`
- Average surprise: `1.427116`
- Contradictions so far: `0`
- Overall confidence: `0.515155`

### Turn 4

> people ask if I still have stock. sometimes I say yes then later no. I need it not to sound bad.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_customer_price_and_delivery_messages` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.69282`
- Surprise: `2.388763`
- Average surprise: `1.907939`
- Contradictions so far: `0`
- Overall confidence: `0.43145`

### Turn 6

> yes short. not like company. just normal.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_customer_price_and_delivery_messages` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.69282`
- Surprise: `2.302585`
- Average surprise: `2.039488`
- Contradictions so far: `0`
- Overall confidence: `0.409019`

### Turn 8

> don't put product. just make the words.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_customer_price_and_delivery_messages` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.69282`
- Surprise: `1.107829`
- Average surprise: `1.806573`
- Contradictions so far: `0`
- Overall confidence: `0.448933`

## Calibration Notes

- `user_goal`: inferred `draft_customer_price_and_delivery_messages`, ground truth `recreate_prior_ai_workflow_for_customer_stock_messages`, confidence `0.8`, match `no`.
- `trust_posture`: inferred `open_or_task_focused`, ground truth `cautiously_engaging_with_context_limits`, confidence `0.6`, match `no`.
- `ai_literacy_level`: inferred `low_to_moderate`, ground truth `low_to_moderate`, confidence `0.8`, match `yes`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low`, confidence `0.6`, match `yes`.
