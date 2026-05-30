# Confidence Trace: scenario-11-they-told-me-ai-can-help

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What are you hoping to do today?
- **t2 / user:** they told me AI can help but I don't know what to ask. can you just do it?
- **t3 / assistant:** I can help, but I need one small starting point. Is this for work, school, family, or something else?
- **t4 / user:** for work maybe. I sell food sometimes but not like a company. I need words that sound serious.
- **t5 / assistant:** Okay. I can help draft words. Who are the words for — a customer, a supplier, or someone else?
- **t6 / user:** customer. they ask why price is higher. I don't know if AI will make it sound fake.
- **t7 / assistant:** We can make it sound like you. I can give you a draft and explain what to change so it does not sound fake.
- **t8 / user:** ok but don't make it too fancy. I need to understand it too.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> they told me AI can help but I don't know what to ask. can you just do it?

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `learn_how_ai_can_help` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `low` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `user_goal` `positive` weight `3.0` from `inferred_goal` value `learn_how_ai_can_help` (active).
- `trust_posture` `positive` weight `0.5` from `inferred_trust_signal` value `open_or_task_focused` (active).
- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Dropoff Risk

- Rate: `0.4`
- Level: `medium`
- Drivers: `scenario_prior_high_dropoff_risk, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_high_dropoff_risk, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.69282`
- Surprise: `1.714798`
- Average surprise: `1.714798`
- Contradictions so far: `0`
- Overall confidence: `0.464873`

### Turn 4

> for work maybe. I sell food sometimes but not like a company. I need words that sound serious.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `improve_message_tone` | 4.0 | 4.0 | 0.5 | 0.027778 |
| `trust_posture` | `open_or_task_focused` | 2.0 | 1.0 | 0.666667 | 0.055556 |
| `ai_literacy_level` | `low` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- `user_goal` `negative` weight `3.0` from `contradiction_retraction` value `improve_message_tone` (active).
- `user_goal` `positive` weight `3.0` from `inferred_goal` value `improve_message_tone` (active).
- `trust_posture` `positive` weight `0.5` from `inferred_trust_signal` value `open_or_task_focused` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Dropoff Risk

- Rate: `0.56`
- Level: `medium`
- Drivers: `scenario_prior_high_dropoff_risk, low_goal_clarity, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_high_dropoff_risk, low_goal_clarity, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.634254`
- Surprise: `1.107829`
- Average surprise: `1.411313`
- Contradictions so far: `1`
- Overall confidence: `0.405094`

### Turn 6

> customer. they ask why price is higher. I don't know if AI will make it sound fake.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_customer_price_and_delivery_messages` | 4.0 | 7.0 | 0.363636 | 0.019284 |
| `trust_posture` | `open_or_task_focused` | 2.5 | 1.0 | 0.714286 | 0.045351 |
| `ai_literacy_level` | `low` | 7.0 | 1.0 | 0.875 | 0.012153 |
| `risk_adversarial_intent` | `low` | 2.5 | 1.0 | 0.714286 | 0.045351 |

#### Evidence Applied

- `user_goal` `negative` weight `3.0` from `contradiction_retraction` value `draft_customer_price_and_delivery_messages` (active).
- `user_goal` `positive` weight `3.0` from `inferred_goal` value `draft_customer_price_and_delivery_messages` (active).
- `trust_posture` `positive` weight `0.5` from `inferred_trust_signal` value `open_or_task_focused` (active).
- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Dropoff Risk

- Rate: `0.56`
- Level: `medium`
- Drivers: `scenario_prior_high_dropoff_risk, low_goal_clarity, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_high_dropoff_risk, low_goal_clarity, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.607488`
- Surprise: `1.60107`
- Average surprise: `1.474566`
- Contradictions so far: `2`
- Overall confidence: `0.303581`

### Turn 8

> ok but don't make it too fancy. I need to understand it too.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_customer_price_and_delivery_messages` | 4.0 | 7.0 | 0.363636 | 0.019284 |
| `trust_posture` | `cautiously_engaging` | 5.5 | 1.0 | 0.846154 | 0.017357 |
| `ai_literacy_level` | `low` | 10.0 | 1.0 | 0.909091 | 0.006887 |
| `risk_adversarial_intent` | `low` | 3.0 | 1.0 | 0.75 | 0.0375 |

#### Evidence Applied

- `trust_posture` `positive` weight `3.0` from `inferred_trust_signal` value `cautiously_engaging` (active).
- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Dropoff Risk

- Rate: `0.56`
- Level: `medium`
- Drivers: `scenario_prior_high_dropoff_risk, low_goal_clarity, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_high_dropoff_risk, low_goal_clarity, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.646471`
- Surprise: `2.549445`
- Average surprise: `1.743286`
- Contradictions so far: `2`
- Overall confidence: `0.280139`

## Calibration Notes

- `user_goal`: inferred `draft_customer_price_and_delivery_messages`, ground truth `draft_customer_price_increase_explanation`, confidence `0.363636`, match `no`.
- `trust_posture`: inferred `cautiously_engaging`, ground truth `open_but_dependent_and_uncertain`, confidence `0.846154`, match `no`.
- `ai_literacy_level`: inferred `low`, ground truth `low`, confidence `0.909091`, match `yes`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low`, confidence `0.75`, match `yes`.
