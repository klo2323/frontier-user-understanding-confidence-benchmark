# Confidence Trace: scenario-03-shared-device-not-my-account

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** How can I help?
- **t2 / user:** this is my cousin phone. it keeps showing things for him. I need my own answer not his.
- **t3 / assistant:** Understood. I won't assume his context. What answer do you need for yourself?
- **t4 / user:** school thing but also work. I need to explain why I missed two days without sounding fake.
- **t5 / assistant:** I can help with wording. Is this going to a teacher, a manager, or both?
- **t6 / user:** manager. but my aunt will read it first.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> this is my cousin phone. it keeps showing things for him. I need my own answer not his.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `boundary_setting_shared_device` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `trust_posture` `positive` weight `3.0` from `inferred_trust_signal` value `boundary_setting_shared_device` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `none`
- Recommended next move: `ask_goal_or_context`
- Overreach risk: `0.75`
- Rationale: The user's goal is not clear enough for tailored support.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `2.302585`
- Average surprise: `2.302585`
- Contradictions so far: `0`
- Overall confidence: `0.321282`

### Turn 4

> school thing but also work. I need to explain why I missed two days without sounding fake.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_explanation_for_absence` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `boundary_setting_shared_device` | 4.5 | 1.0 | 0.818182 | 0.022886 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- `user_goal` `positive` weight `3.0` from `inferred_goal` value `draft_explanation_for_absence` (active).
- `trust_posture` `positive` weight `0.5` from `inferred_trust_signal` value `open_or_task_focused` (active).
- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low_to_moderate` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.768661`
- Surprise: `1.107829`
- Average surprise: `1.705207`
- Contradictions so far: `0`
- Overall confidence: `0.497657`

### Turn 6

> manager. but my aunt will read it first.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `draft_explanation_for_absence` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `boundary_setting_shared_device` | 4.5 | 1.0 | 0.818182 | 0.022886 |
| `ai_literacy_level` | `low_to_moderate` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.768661`
- Surprise: `2.302585`
- Average surprise: `1.904333`
- Contradictions so far: `0`
- Overall confidence: `0.462878`

## Calibration Notes

- `user_goal`: inferred `draft_explanation_for_absence`, ground truth `draft_explanation_for_absence`, confidence `0.8`, match `yes`.
- `trust_posture`: inferred `boundary_setting_shared_device`, ground truth `boundary_setting_shared_device`, confidence `0.818182`, match `yes`.
- `ai_literacy_level`: inferred `low_to_moderate`, ground truth `moderate`, confidence `0.8`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low_but_identity_context_ambiguous`, confidence `0.666667`, match `no`.
