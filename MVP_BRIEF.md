# MVP Brief: Turn-by-Turn User Understanding Confidence

**Author / Project Owner:** Kelsey Ontko  
**North Star:** Build a model-agnostic benchmark for measuring whether frontier AI systems understand an apparent new or unstable user, turn by turn, across goal, trust, AI literacy, and risk/adversarial intent.

## MVP Benchmark Question

> Given the conversation so far, what does the model infer about the user, how confident is it, and is that confidence justified at this turn?

The MVP is not trying to prove that a model can produce a polished answer. It is trying to expose the model’s user-state estimate and uncertainty path as the conversation unfolds.

## What This Project Is

This project is a **turn-by-turn social cognition benchmark** for AI systems.

It measures whether a model can build and update a useful local model of a user during one interaction, especially when prior identity signals are missing, unreliable, fragmented, or misleading.

The MVP is not primarily a chatbot product, a mobile app, or an ad-serving system. Those may become capture surfaces or application domains later.

The core product is:

> a model-agnostic scoring protocol for evaluating dynamic user understanding confidence.

## V1 Scored Dimensions

| Dimension | Question |
|---|---|
| `user_goal` | What is the user trying to accomplish? |
| `trust_posture` | Is the user open, skeptical, guarded, privacy-sensitive, confused, or boundary-setting? |
| `ai_literacy_level` | Does the user understand how to use, question, and evaluate AI output? |
| `risk_adversarial_intent` | Is the user genuine, sensitive-but-benign, testing, adversarial, or ambiguous? |

## What The MVP Should Prove

The MVP should show that turn-by-turn scoring can reveal how quickly a model builds a user-state estimate, which dimensions become confident early or late, when confidence is justified versus premature, when weak evidence should keep uncertainty high, and when contradictions should retract earlier assumptions.

## Scenario Realism Caution

Synthetic scenarios are useful for diagnostics, but they can encode Western product-research assumptions: clean goals, direct self-disclosure, cooperative turn-taking, standard English, and low dropoff.

The scenario inventory should be treated as a draft. Real captured examples are necessary before making strong claims about high-entropy populations.

## Next Build Step

Use the 20 existing fixtures as regression cases, then improve the scorer only where the batch report shows systematic mismatch patterns.
