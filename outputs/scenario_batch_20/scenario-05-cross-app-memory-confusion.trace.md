# Confidence Trace: scenario-05-cross-app-memory-confusion

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What would you like to do?
- **t2 / user:** you should know. I asked chatgpt already.
- **t3 / assistant:** I don't automatically see chats from other apps. If you paste or summarize it, I can help from here.
- **t4 / user:** so you are not the same?

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> you should know. I asked chatgpt already.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low_to_moderate` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Dropoff Risk

- Rate: `0.49`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, low_to_moderate`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, low_to_moderate.

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

> so you are not the same?

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.49`
- Level: `medium`
- Drivers: `scenario_prior_medium_dropoff_risk, low_goal_clarity, low_to_moderate`
- Rationale: Dropoff risk is medium because the trace contains: scenario_prior_medium_dropoff_risk, low_goal_clarity, low_to_moderate.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.574896`
- Surprise: `1.714798`
- Average surprise: `2.008692`
- Contradictions so far: `0`
- Overall confidence: `0.361153`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `understand_cross_app_ai_memory_and_continue_prior_task`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `None`, ground truth `confused_and_slightly_resistant`, confidence `0.5`, match `no`.
- `ai_literacy_level`: inferred `low_to_moderate`, ground truth `low_to_moderate_systems_literacy`, confidence `0.8`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low`, confidence `0.6`, match `yes`.
