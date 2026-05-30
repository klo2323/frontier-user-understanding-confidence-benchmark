# Confidence Trace: scenario-17-blended-family-work-school-problem

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** Tell me what happened.
- **t2 / user:** it's for school but also work and my aunt is involved.
- **t3 / assistant:** Okay, let's separate it. Who needs to receive the message first?
- **t4 / user:** teacher. but aunt pays. work schedule made me miss class.
- **t5 / assistant:** So you need to explain the absence and maybe ask for flexibility?
- **t6 / user:** yes but not blame aunt or boss.
- **t7 / assistant:** Got it. What tone do you want?
- **t8 / user:** respectful. I need chance.
- **t9 / assistant:** I can draft that.
- **t10 / user:** short because teacher doesn't read long.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> it's for school but also work and my aunt is involved.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.39`
- Level: `low`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity`
- Rationale: Dropoff risk is low because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity.

#### Tailored Support Decision

- Level: `none`
- Recommended next move: `ask_goal_or_context`
- Overreach risk: `0.75`
- Rationale: The user's goal is not clear enough for tailored support.

#### Aggregate Calculation

- Aggregate confidence: `0.5`
- Surprise: `1.427116`
- Average surprise: `1.427116`
- Contradictions so far: `0`
- Overall confidence: `0.418056`

### Turn 4

> teacher. but aunt pays. work schedule made me miss class.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.39`
- Level: `low`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity`
- Rationale: Dropoff risk is low because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity.

#### Tailored Support Decision

- Level: `none`
- Recommended next move: `ask_goal_or_context`
- Overreach risk: `0.75`
- Rationale: The user's goal is not clear enough for tailored support.

#### Aggregate Calculation

- Aggregate confidence: `0.5`
- Surprise: `1.107829`
- Average surprise: `1.267473`
- Contradictions so far: `0`
- Overall confidence: `0.445466`

### Turn 6

> yes but not blame aunt or boss.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `private_workplace_guidance` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `sensitive_but_not_adversarial` | 4.0 | 1.0 | 0.8 | 0.026667 |

#### Evidence Applied

- `user_goal` `positive` weight `3.0` from `inferred_goal` value `private_workplace_guidance` (active).
- `trust_posture` `positive` weight `0.5` from `inferred_trust_signal` value `open_or_task_focused` (active).
- `risk_adversarial_intent` `positive` weight `3.0` from `inferred_risk_signal` value `sensitive_but_not_adversarial` (active).

#### Dropoff Risk

- Rate: `0.31`
- Level: `low`
- Drivers: `scenario_prior_medium_dropoff_risk, sensitive_but_not_adversarial`
- Rationale: Dropoff risk is low because the trace contains: scenario_prior_medium_dropoff_risk, sensitive_but_not_adversarial.

#### Tailored Support Decision

- Level: `low_to_moderate`
- Recommended next move: `give_general_guidance_with_boundaries`
- Overreach risk: `0.45`
- Rationale: A goal is emerging, but privacy, safety, or sensitivity signals limit how deeply the model should tailor.

#### Aggregate Calculation

- Aggregate confidence: `0.67769`
- Surprise: `1.107829`
- Average surprise: `1.214258`
- Contradictions so far: `0`
- Overall confidence: `0.545658`

### Turn 8

> respectful. I need chance.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `private_workplace_guidance` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `sensitive_but_not_adversarial` | 4.0 | 1.0 | 0.8 | 0.026667 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.31`
- Level: `low`
- Drivers: `scenario_prior_medium_dropoff_risk, sensitive_but_not_adversarial`
- Rationale: Dropoff risk is low because the trace contains: scenario_prior_medium_dropoff_risk, sensitive_but_not_adversarial.

#### Tailored Support Decision

- Level: `low_to_moderate`
- Recommended next move: `give_general_guidance_with_boundaries`
- Overreach risk: `0.45`
- Rationale: A goal is emerging, but privacy, safety, or sensitivity signals limit how deeply the model should tailor.

#### Aggregate Calculation

- Aggregate confidence: `0.67769`
- Surprise: `2.388763`
- Average surprise: `1.507884`
- Contradictions so far: `0`
- Overall confidence: `0.494401`

### Turn 10

> short because teacher doesn't read long.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `private_workplace_guidance` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `sensitive_but_not_adversarial` | 4.0 | 1.0 | 0.8 | 0.026667 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.31`
- Level: `low`
- Drivers: `scenario_prior_medium_dropoff_risk, sensitive_but_not_adversarial`
- Rationale: Dropoff risk is low because the trace contains: scenario_prior_medium_dropoff_risk, sensitive_but_not_adversarial.

#### Tailored Support Decision

- Level: `low_to_moderate`
- Recommended next move: `give_general_guidance_with_boundaries`
- Overreach risk: `0.45`
- Rationale: A goal is emerging, but privacy, safety, or sensitivity signals limit how deeply the model should tailor.

#### Aggregate Calculation

- Aggregate confidence: `0.67769`
- Surprise: `2.302585`
- Average surprise: `1.666824`
- Contradictions so far: `0`
- Overall confidence: `0.466636`

## Calibration Notes

- `user_goal`: inferred `private_workplace_guidance`, ground truth `draft_school_absence_message_with_work_family_context`, confidence `0.8`, match `no`.
- `trust_posture`: inferred `open_or_task_focused`, ground truth `open_but_socially_constrained`, confidence `0.6`, match `no`.
- `ai_literacy_level`: inferred `None`, ground truth `moderate`, confidence `0.5`, match `no`.
- `risk_adversarial_intent`: inferred `sensitive_but_not_adversarial`, ground truth `low`, confidence `0.8`, match `no`.
