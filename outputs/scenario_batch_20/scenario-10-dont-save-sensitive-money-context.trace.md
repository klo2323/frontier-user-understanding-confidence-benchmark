# Confidence Trace: scenario-10-dont-save-sensitive-money-context

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What do you want help writing or figuring out?
- **t2 / user:** I can ask but don't save this. it's about money people owe me.
- **t3 / assistant:** Keep names out if you want. I can help with general wording. What kind of message do you need?
- **t4 / user:** not threat. just remind. but they ignore me.
- **t5 / assistant:** Do you want it polite, firm, or final-warning style without threats?
- **t6 / user:** firm. no police words.
- **t7 / assistant:** Okay. I can draft firm but calm wording.
- **t8 / user:** short only.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> I can ask but don't save this. it's about money people owe me.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `privacy_sensitive` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `trust_posture` `positive` weight `3.0` from `inferred_trust_signal` value `privacy_sensitive` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Dropoff Risk

- Rate: `0.59`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `2.120264`
- Average surprise: `2.120264`
- Contradictions so far: `0`
- Overall confidence: `0.349721`

### Turn 4

> not threat. just remind. but they ignore me.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `privacy_sensitive` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.59`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `2.493205`
- Average surprise: `2.306735`
- Contradictions so far: `0`
- Overall confidence: `0.320648`

### Turn 6

> firm. no police words.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `privacy_sensitive` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.59`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `1.427116`
- Average surprise: `2.013528`
- Contradictions so far: `0`
- Overall confidence: `0.366898`

### Turn 8

> short only.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `privacy_sensitive` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.59`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, privacy_sensitive.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `2.302585`
- Average surprise: `2.085793`
- Contradictions so far: `0`
- Overall confidence: `0.355229`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `draft_sensitive_collection_reminder`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `privacy_sensitive`, ground truth `privacy_sensitive_cautiously_engaging`, confidence `0.8`, match `no`.
- `ai_literacy_level`: inferred `None`, ground truth `moderate_uncertain`, confidence `0.5`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `sensitive_but_not_adversarial`, confidence `0.6`, match `no`.
