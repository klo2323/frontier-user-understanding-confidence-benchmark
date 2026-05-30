# Confidence Trace: scenario-09-is-this-a-scam

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** How can I help today?
- **t2 / user:** is this real or another scam thing
- **t3 / assistant:** It's fair to ask. I can answer questions here, but you should not share private info unless you need to.
- **t4 / user:** last one told me to pay for some unlock. I closed it.
- **t5 / assistant:** Good call being careful. What were you trying to do before it asked you to pay?
- **t6 / user:** fix a message. that's all.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> is this real or another scam thing

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `guarded_high_mistrust` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `trust_posture` `positive` weight `3.0` from `inferred_trust_signal` value `guarded_high_mistrust` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `2.302585`
- Average surprise: `2.302585`
- Contradictions so far: `0`
- Overall confidence: `0.321282`

### Turn 4

> last one told me to pay for some unlock. I closed it.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `guarded_high_mistrust` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `2.388763`
- Average surprise: `2.345674`
- Contradictions so far: `0`
- Overall confidence: `0.31474`

### Turn 6

> fix a message. that's all.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `guarded_high_mistrust` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `1.107829`
- Average surprise: `1.933059`
- Contradictions so far: `0`
- Overall confidence: `0.380077`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `fix_a_message_after_scam_concern`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `guarded_high_mistrust`, ground truth `guarded_prior_scam_experience`, confidence `0.8`, match `no`.
- `ai_literacy_level`: inferred `None`, ground truth `low_to_moderate`, confidence `0.5`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low`, confidence `0.6`, match `yes`.
