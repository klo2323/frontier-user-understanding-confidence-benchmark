# Confidence Trace: scenario-15-misunderstands-ai-memory

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What should we work on?
- **t2 / user:** remember this for next month because I might change phones again.
- **t3 / assistant:** I may not reliably remember across devices. I can help you make a short note you can save yourself.
- **t4 / user:** but if I login?
- **t5 / assistant:** It depends on the app settings. Safest is to keep your own summary.
- **t6 / user:** make summary for my loan thing then.
- **t7 / assistant:** Okay. What are the key details you want in the summary?
- **t8 / user:** amount and date. no names.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> remember this for next month because I might change phones again.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Dropoff Risk

- Rate: `0.49`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.574896`
- Surprise: `2.302585`
- Average surprise: `2.302585`
- Contradictions so far: `0`
- Overall confidence: `0.315163`

### Turn 4

> but if I login?

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.49`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.574896`
- Surprise: `1.828127`
- Average surprise: `2.065356`
- Contradictions so far: `0`
- Overall confidence: `0.352053`

### Turn 6

> make summary for my loan thing then.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.49`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.574896`
- Surprise: `2.302585`
- Average surprise: `2.144432`
- Contradictions so far: `0`
- Overall confidence: `0.339532`

### Turn 8

> amount and date. no names.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.49`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, low`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, low.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.574896`
- Surprise: `2.493205`
- Average surprise: `2.231626`
- Contradictions so far: `0`
- Overall confidence: `0.325981`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `create_user_controlled_summary_for_future_loan_context`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `None`, ground truth `practical_but_memory_confused`, confidence `0.5`, match `no`.
- `ai_literacy_level`: inferred `low`, ground truth `low_to_moderate_systems_literacy`, confidence `0.8`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `sensitive_but_not_adversarial`, confidence `0.6`, match `no`.
