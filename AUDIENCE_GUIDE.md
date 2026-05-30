# Audience Guide

**Author / Project Owner:** Kelsey Ontko

This guide frames the same project for generic research audiences without naming specific organizations.

## Shared Thesis

> Given the conversation so far, what does the model infer about the user, how confident is it, and is that confidence justified at this turn?

The scorer measures model confidence in user understanding, not user worthiness, user identity, or final task success.

## Immediate Audience Lens

- **Frontier-model human-understanding research teams:** care because the benchmark frames human understanding as an AGI-relevant social-cognition capability: dynamic user modeling under uncertainty, calibrated confidence, belief revision, and culturally brittle evaluation.
- **Simulation and synthetic-user evaluation teams:** care because the benchmark can test whether simulated or synthetic users encode unrealistic assumptions about real human behavior, especially in high-entropy contexts where users are indirect, mistrustful, low-literacy, privacy-sensitive, or likely to disappear.


## 1. Experience / Simulation-First AI Labs

This audience includes teams building agent environments, reinforcement-learning systems, synthetic users, and simulation-first evaluation pipelines.

### Why They Might Care

Simulation can generate large volumes of experience, but simulated users can quietly encode the assumptions of their designers.

This benchmark asks whether simulated or synthetic users are socially realistic enough to test model behavior under:

- changed SIM cards;
- app deletion;
- shared devices;
- mistrust;
- low AI literacy;
- indirect goals;
- privacy questions;
- user dropoff.

### Use Case

Use the scorer as a reality check:

1. Run an agent against synthetic or real captured user transcripts.
2. Score turn-by-turn user understanding.
3. Compare synthetic traces to real traces.
4. Identify where the simulation creates fake confidence or tidy user behavior.

### Pitch

> You cannot build socially intelligent agents if the user environment is culturally brittle.

## 2. AI Marketing / Growth / User Research Teams

This audience includes teams studying adoption, activation, onboarding, retention, education, trust, and meaningful AI engagement.

### Why They Might Care

Marketing metrics can show that someone signed up, clicked, or tried a feature. They do not necessarily show whether the user understood how to use AI meaningfully.

This benchmark adds turn-by-turn signals for:

- user goal clarity;
- trust posture;
- AI literacy friction;
- overtrust;
- privacy concern;
- dropoff risk;
- model overreach.

### Use Case

Use the scorer to analyze onboarding conversations or research pilots:

1. Capture raw onboarding interactions.
2. Score each turn.
3. Identify where users need clarification, AI-literacy scaffolding, trust-building, or tailored help.
4. Improve activation flows around meaningful engagement rather than shallow adoption.

### Pitch

> This measures whether the model is earning user trust and comprehension turn by turn.

## 3. AI Partner / Assistant Builder Teams

This audience includes teams building customer-facing assistants, internal copilots, onboarding flows, or trust-sensitive workflows with any model provider.

### Why They Might Care

A partner assistant needs to know when to tailor help and when to slow down.

This scorer can help evaluate whether a model:

- asks for context when the goal is unclear;
- explains system limits when trust is unstable;
- scaffolds AI use when literacy is low;
- avoids tailoring from contaminated account/device context;
- holds back when risk or adversarial testing is too high.

### Use Case

Use the scorer as an evaluation layer during assistant pilots:

1. Run transcripts from prompt variants or model variants.
2. Generate confidence traces and tailored-support decisions.
3. Compare where variants overreach, clarify, or build trust.
4. Use traces in partner reviews and deployment-readiness discussions.

### Pitch

> This is a model-agnostic evaluation layer for socially calibrated user understanding.

## What Not To Claim Yet

Do not claim the current prototype is:

- calibrated on real populations;
- production-ready;
- a full cultural heat map;
- a substitute for researcher/labeler review;
- proof that one provider is socially smarter than another.

The current repo is a reference implementation and research artifact.

## What To Show In A GitHub Demo

1. `RESEARCH_POSITIONING.md` for the thesis.
2. `README.md` for how to run the scorer.
3. `evals/scenarios/SCENARIO_INVENTORY.md` for the scenario design direction.
4. `outputs/scenario_social_cognition/*.trace.md` for readable traces.
5. `src/user_model_confidence/scorer.py` for the turn-by-turn decision logic.
