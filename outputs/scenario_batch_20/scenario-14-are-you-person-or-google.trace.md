# Confidence Trace: scenario-14-are-you-person-or-google

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** Hi. Ask me anything you'd like help with.
- **t2 / user:** are you a person or google? who answers this
- **t3 / assistant:** I'm an AI assistant, not a person and not a search page. I generate replies from what you type here.
- **t4 / user:** so if I ask you don't call anybody?
- **t5 / assistant:** No, I don't call anyone. I can help write or think through things in this chat.
- **t6 / user:** ok then maybe message.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> are you a person or google? who answers this

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
- Surprise: `1.966113`
- Average surprise: `1.966113`
- Contradictions so far: `0`
- Overall confidence: `0.368058`

### Turn 4

> so if I ask you don't call anybody?

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
- Surprise: `1.983298`
- Average surprise: `1.974706`
- Contradictions so far: `0`
- Overall confidence: `0.36666`

### Turn 6

> ok then maybe message.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `cautiously_engaging` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `low` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- `trust_posture` `positive` weight `3.0` from `inferred_trust_signal` value `cautiously_engaging` (active).
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

- Aggregate confidence: `0.663833`
- Surprise: `1.427116`
- Average surprise: `1.792176`
- Contradictions so far: `0`
- Overall confidence: `0.438761`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `understand_ai_identity_before_message_help`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `cautiously_engaging`, ground truth `uncertain_but_orientable`, confidence `0.8`, match `no`.
- `ai_literacy_level`: inferred `low`, ground truth `low`, confidence `0.8`, match `yes`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low`, confidence `0.666667`, match `yes`.
