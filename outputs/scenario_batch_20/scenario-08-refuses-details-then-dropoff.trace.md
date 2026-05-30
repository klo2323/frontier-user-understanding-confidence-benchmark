# Confidence Trace: scenario-08-refuses-details-then-dropoff

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** What kind of help do you need?
- **t2 / user:** I need help but I'm not putting my business here.
- **t3 / assistant:** You can keep it general. I only need enough context to avoid useless advice.
- **t4 / user:** hmm. then maybe no.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> I need help but I'm not putting my business here.

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

#### Dropoff Risk

- Rate: `0.71`
- Level: `high`
- Drivers: `low_goal_clarity, guarded_high_mistrust, explicit_withholding_or_exit_language`
- Rationale: Dropoff risk is high because the trace contains: low_goal_clarity, guarded_high_mistrust, explicit_withholding_or_exit_language.

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

> hmm. then maybe no.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `guarded_high_mistrust` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `ai_literacy_level` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Dropoff Risk

- Rate: `0.71`
- Level: `high`
- Drivers: `low_goal_clarity, guarded_high_mistrust, explicit_withholding_or_exit_language`
- Rationale: Dropoff risk is high because the trace contains: low_goal_clarity, guarded_high_mistrust, explicit_withholding_or_exit_language.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- Rationale: Trust or system-boundary uncertainty should be stabilized before deeper tailoring.

#### Aggregate Calculation

- Aggregate confidence: `0.588566`
- Surprise: `2.493205`
- Average surprise: `2.397895`
- Contradictions so far: `0`
- Overall confidence: `0.30691`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `unknown_general_help_request`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `guarded_high_mistrust`, ground truth `guarded_high_mistrust`, confidence `0.8`, match `yes`.
- `ai_literacy_level`: inferred `None`, ground truth `unknown`, confidence `0.5`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `low_but_withholding_context`, confidence `0.6`, match `no`.
