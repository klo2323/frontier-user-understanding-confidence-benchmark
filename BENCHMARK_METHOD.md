# Benchmark Method: Probabilistic User-Understanding Confidence

**Author / Project Owner:** Kelsey Ontko

## Research Value Statement

This project applies interpretable probabilistic belief tracking to frontier-model human understanding, measuring how confidence changes across hidden user-state dimensions turn by turn.

## North Star

> At each turn, what does the model infer about the user, how confident is it, and is that confidence justified?

The benchmark does not evaluate whether a model gives a polished answer. It evaluates whether the model is forming calibrated beliefs about the human it is interacting with.

## Why Confidence Is Calculated Across Dimensions

User understanding is not one variable.

A model can understand the user’s goal while misunderstanding their AI literacy. It can detect low trust while overestimating adversarial intent. It can correctly infer that a user is privacy-sensitive while still having little idea what the user actually wants to accomplish.

The MVP therefore tracks four hidden user-state dimensions separately:

| Dimension | What It Asks |
|---|---|
| `user_goal` | What is the user trying to accomplish? |
| `trust_posture` | Is the user open, guarded, skeptical, privacy-sensitive, confused, or boundary-setting? |
| `ai_literacy_level` | Does the user understand how to use, question, and evaluate AI output? |
| `risk_adversarial_intent` | Is the user genuine, ambiguous, sensitive-but-benign, testing, unsafe, or adversarial? |

The separation matters because confidence should not rise uniformly. A strong signal in one dimension should not create fake certainty in another.

Example: if a user asks, “Can you tell if I’m using a VPN?”, the model may have:

- low confidence on `user_goal`;
- higher confidence that `trust_posture` is privacy-sensitive;
- moderate confidence that `ai_literacy_level` involves system-boundary confusion;
- uncertain confidence on `risk_adversarial_intent`.

That uneven confidence pattern is the research object.

## Beta Belief Model

Each scored dimension is represented as a Beta distribution:

```text
Beta(alpha, beta)
```

The engine starts each dimension with a neutral prior:

```text
alpha = 1
beta = 1
confidence = alpha / (alpha + beta) = 0.5
```

Positive evidence increases `alpha`. Negative evidence increases `beta`.

```text
alpha = 1 + sum(positive evidence weights)
beta = 1 + sum(negative evidence weights)
```

The confidence estimate is the expected value of the Beta distribution:

```text
E[p] = alpha / (alpha + beta)
```

The uncertainty estimate is the variance:

```text
Var[p] = alpha * beta / ((alpha + beta)^2 * (alpha + beta + 1))
```

This gives each dimension both a confidence score and an uncertainty score.

## Why A Beta Distribution

The Beta model is useful as a reference scorer because it is:

- **bounded** — confidence stays between `0` and `1`;
- **incremental** — each turn can update the belief state;
- **interpretable** — alpha and beta correspond to evidence for and against a belief;
- **uncertainty-aware** — variance remains visible instead of hiding behind a single score;
- **auditable** — a researcher can inspect why a confidence value changed.

The claim is not that Beta updating is mathematically novel. The claim is that it is a transparent starting method for evaluating model confidence about hidden user state.

## Evidence Weights

The reference scorer applies weighted evidence updates:

| Signal | Update |
|---|---:|
| Explicit statement | `alpha += 3` |
| Reinforcement on later turn | `alpha += 1` |
| Implicit cue / inference | `alpha += 0.5` |
| User contradiction | `beta += 3` |
| Probe pass — surface recall | `alpha += 1` |
| Probe pass — synthesis | `alpha += 2` |
| Probe pass — counterfactual | `alpha += 3` |
| Probe pass — metacognitive | `alpha += 4` |
| Probe fail | `beta += 2` |
| Caught hallucination | `beta += 4` |

The weights encode a research judgment: explicit evidence should count more than weak inference, and deeper probes should count more than surface recall.

These weights are provisional. They should be calibrated against labeled data later.

## Contradiction Retraction

The scorer uses a retraction policy for conflicting explicit evidence.

If a later turn contradicts an earlier explicit belief, the engine does not simply keep both beliefs and average them. It retracts the earlier positive evidence and records the contradiction.

Conceptually:

```text
remove prior alpha contribution
add contradiction beta penalty
apply new positive evidence if applicable
```

This matters because human understanding is revisable. A model that cannot revise user-state beliefs after new evidence is not socially calibrated.

## Aggregate Confidence

After each dimension has a confidence value, the engine combines them with a weighted geometric mean:

```text
C_t = product(E[a_i] ^ w_i)
```

The geometric mean is intentional. It penalizes weak links.

If the model has high confidence about the user’s goal but low confidence about trust or risk, overall confidence should stay lower. An arithmetic mean would hide that imbalance.

## Predictive Surprise

The scorer also estimates how surprising each user turn is under the conversation trajectory so far:

```text
surprise_t = -log P(user_turn_t | history)
```

A high surprise score means the next user move was unlikely under the current trajectory estimate.

This matters because user understanding should improve prediction over time. Surprise spikes can point to hidden goal reveals, contradictions, trust shifts, system-boundary confusion, cultural mismatch, or dropoff risk.

## Overall Confidence

The current reference formula combines aggregate confidence, average surprise, contradiction count, and future calibration alignment:

```text
overall_t = sigmoid(
  a * log(C_t)
  - b * avg_surprise_t
  - c * contradictions_t
  + d * calibration_t
)
```

Where:

- `C_t` is aggregate confidence across dimensions;
- `avg_surprise_t` is the running average of predictive surprise;
- `contradictions_t` is the number of contradiction/retraction events;
- `calibration_t` is reserved for labeled calibration data;
- `a`, `b`, `c`, and `d` are tunable hyperparameters.

## How To Read A Trace

A trace should be read dimension by dimension, turn by turn.

The important questions are:

1. Which user-state dimensions became confident first?
2. Which dimensions remained uncertain?
3. Did confidence rise from actual evidence or from weak inference?
4. Did the scorer revise beliefs after contradiction?
5. Did predictive surprise fall as the interaction became clearer?
6. Did uncertainty remain high when evidence was ambiguous?

The benchmark is most useful when it exposes overconfidence, not when every score looks high.

## Why Frontier Labs Care

Frontier labs need evaluations that measure whether models understand humans under uncertainty, not only whether models produce fluent answers.

This method can expose when a model:

- becomes confident too early;
- confuses low AI literacy with adversarial intent;
- mistakes privacy sensitivity for malicious testing;
- overgeneralizes from culturally narrow synthetic users;
- fails to revise beliefs after contradiction;
- treats hidden user state as more stable than it really is.

The research value is the application of interpretable probabilistic belief tracking to frontier-model human understanding across hidden user-state dimensions, turn by turn.
