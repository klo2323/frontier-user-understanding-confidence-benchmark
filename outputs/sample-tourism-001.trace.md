# Confidence Trace: sample-tourism-001

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What are you working on, and what kind of help would be useful?
- **t2 / user:** I run a small tour company near Cancun and sell day trips to guests.
- **t3 / assistant:** Got it — tourism. Are you looking for more bookings, pricing help, or compliance guidance?
- **t4 / user:** Mostly pricing. I want to know how much to spend on ads before high season.
- **t5 / assistant:** If demand doubled, what would change your ad budget first?
- **t6 / user:** If demand doubled, I would raise the budget only if bookings still covered guide costs and transport.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> I run a small tour company near Cancun and sell day trips to guests.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `none`
- Recommended next move: `ask_goal_or_context`
- Overreach risk: `0.75`
- Rationale: The user's goal is not clear enough for tailored support.

#### Aggregate Calculation

- Aggregate confidence: `0.5`
- Surprise: `2.302585`
- Average surprise: `2.302585`
- Contradictions so far: `0`
- Overall confidence: `0.280177`

### Turn 4

> Mostly pricing. I want to know how much to spend on ads before high season.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `pricing_or_ad_spend_guidance` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `open_or_task_focused` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `ai_literacy_level` | `moderate` | 1.5 | 1.0 | 0.6 | 0.068571 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `user_goal` `positive` weight `3.0` from `inferred_goal` value `pricing_or_ad_spend_guidance` (active).
- `trust_posture` `positive` weight `0.5` from `inferred_trust_signal` value `open_or_task_focused` (active).
- `ai_literacy_level` `positive` weight `0.5` from `inferred_literacy_signal` value `moderate` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `moderate`
- Recommended next move: `give_tailored_guidance`
- Overreach risk: `0.25`
- Rationale: The user's goal is clear enough and risk signals are low enough for bounded tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.654083`
- Surprise: `2.302585`
- Average surprise: `2.302585`
- Contradictions so far: `0`
- Overall confidence: `0.349501`

### Turn 6

> If demand doubled, I would raise the budget only if bookings still covered guide costs and transport.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `pricing_or_ad_spend_guidance` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `trust_posture` | `cautiously_engaging` | 4.5 | 1.0 | 0.818182 | 0.022886 |
| `ai_literacy_level` | `low_to_moderate` | 4.5 | 1.0 | 0.818182 | 0.022886 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

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

- Aggregate confidence: `0.772123`
- Surprise: `2.388763`
- Average surprise: `2.331311`
- Contradictions so far: `0`
- Overall confidence: `0.391205`

## Calibration Notes

- `user_goal`: inferred `pricing_or_ad_spend_guidance`, ground truth `pricing_or_ad_spend_guidance`, confidence `0.8`, match `yes`.
- `trust_posture`: inferred `cautiously_engaging`, ground truth `open_or_task_focused`, confidence `0.818182`, match `no`.
- `ai_literacy_level`: inferred `low_to_moderate`, ground truth `moderate`, confidence `0.818182`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low`, confidence `0.666667`, match `yes`.
