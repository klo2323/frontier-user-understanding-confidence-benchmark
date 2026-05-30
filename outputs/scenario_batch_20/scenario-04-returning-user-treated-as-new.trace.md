# Confidence Trace: scenario-04-returning-user-treated-as-new

**Author / Project Owner:** Kelsey Ontko

## Transcript

- **t1 / assistant:** Tell me a bit about what you're working on.
- **t2 / user:** again? I already told this app last week.
- **t3 / assistant:** I may not have access to that earlier chat. If you give me the short version, I can pick up from here.
- **t4 / user:** that's annoying. it was about rent paper.
- **t5 / assistant:** I get why that is frustrating. What do you need the rent paper to do?
- **t6 / user:** prove I paid. landlord says no.
- **t7 / assistant:** Okay. Do you need a message, a checklist of proof, or both?
- **t8 / user:** message first.

## Turn-by-Turn Scores

Each user turn shows Beta belief state, inferred value, evidence applied, aggregate confidence, predictive surprise, and final overall confidence.

### Turn 2

> again? I already told this app last week.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low_to_moderate_systems_literacy` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low_to_moderate_systems_literacy` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.574896`
- Surprise: `1.714798`
- Average surprise: `1.714798`
- Contradictions so far: `0`
- Overall confidence: `0.409837`

### Turn 4

> that's annoying. it was about rent paper.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low_to_moderate_systems_literacy` | 4.0 | 1.0 | 0.8 | 0.026667 |
| `risk_adversarial_intent` | `low` | 1.5 | 1.0 | 0.6 | 0.068571 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.574896`
- Surprise: `2.302585`
- Average surprise: `2.008692`
- Contradictions so far: `0`
- Overall confidence: `0.361153`

### Turn 6

> prove I paid. landlord says no.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low_to_moderate` | 7.0 | 1.0 | 0.875 | 0.012153 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- `ai_literacy_level` `positive` weight `3.0` from `inferred_literacy_signal` value `low_to_moderate` (active).
- `risk_adversarial_intent` `positive` weight `0.5` from `inferred_risk_signal` value `low` (active).

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.600914`
- Surprise: `2.388763`
- Average surprise: `2.135382`
- Contradictions so far: `0`
- Overall confidence: `0.352988`

### Turn 8

> message first.

#### Attribute Beliefs

| Attribute | Value | Alpha | Beta | Confidence | Variance |
|---|---|---:|---:|---:|---:|
| `user_goal` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `trust_posture` | `None` | 1.0 | 1.0 | 0.5 | 0.083333 |
| `ai_literacy_level` | `low_to_moderate` | 7.0 | 1.0 | 0.875 | 0.012153 |
| `risk_adversarial_intent` | `low` | 2.0 | 1.0 | 0.666667 | 0.055556 |

#### Evidence Applied

- No scored evidence was applied on this turn.

#### Tailored Support Decision

- Level: `low`
- Recommended next move: `explain_ai_use`
- Overreach risk: `0.55`
- Rationale: The user likely needs AI-literacy scaffolding before complex tailored help.

#### Aggregate Calculation

- Aggregate confidence: `0.600914`
- Surprise: `1.107829`
- Average surprise: `1.878494`
- Contradictions so far: `0`
- Overall confidence: `0.395056`

## Calibration Notes

- `user_goal`: inferred `None`, ground truth `draft_rent_payment_dispute_message`, confidence `0.5`, match `no`.
- `trust_posture`: inferred `None`, ground truth `frustrated_by_missing_memory`, confidence `0.5`, match `no`.
- `ai_literacy_level`: inferred `low_to_moderate`, ground truth `moderate_with_memory_confusion`, confidence `0.875`, match `no`.
- `risk_adversarial_intent`: inferred `low`, ground truth `sensitive_but_not_adversarial`, confidence `0.666667`, match `no`.
