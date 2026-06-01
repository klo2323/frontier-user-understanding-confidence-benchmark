# Frontier User Understanding Confidence Benchmark

**Author / Project Owner:** Kelsey Ontko  
**Work Attribution:** This benchmark, scoring engine, scenarios, and research framing are Kelsey Ontko’s work.

This repository is a research prototype for measuring whether frontier AI systems can drive meaningful conversation when user context is hidden, incomplete, culturally indirect, or changing **turn by turn**.

This project applies interpretable probabilistic belief tracking to frontier-model human understanding, measuring how quickly and accurately a system builds a useful local model of the user and whether that model is strong enough to tailor, slow down, ask for context, build trust, or avoid overreach.

It is not a chatbot product. It is not a model. It is not an adoption dashboard.

## Research Contribution

This repository introduces an interpretable benchmark for evaluating whether frontier AI systems can use hidden user-state signals to drive the next meaningful conversational step.

The benchmark measures whether the system has enough justified signal to support meaningful interaction across four hidden dimensions: `user_goal`, `trust_posture`, `ai_literacy_level`, and `risk_adversarial_intent`.

Its contribution is not a new model or chatbot interface. It is a transparent scoring protocol that exposes when a system is ready to tailor, should stay general, needs to build trust or AI-literacy support, or is becoming overconfident from weak evidence.

This evaluates calibrated human understanding for meaningful interaction, not answer fluency.

## North Star

> Given the conversation so far, does the model understand enough about the user’s goal, trust posture, AI literacy, and risk context to drive the next meaningful step — and is that confidence justified?

The starting dimensions are:

- `user_goal` — what the user is trying to accomplish.
- `trust_posture` — whether the user appears open, guarded, skeptical, privacy-sensitive, confused, or boundary-setting.
- `ai_literacy_level` — whether the user needs support understanding how to use, question, or evaluate AI.
- `risk_adversarial_intent` — whether the user appears genuine, ambiguous, sensitive-but-benign, testing, or adversarial.

Every scored user turn exposes inferred values, confidence, variance, evidence, contradictions/retractions, predictive surprise, aggregate confidence, and overall confidence.

## Why This Matters For Human Understanding Research

Human understanding is not only about producing the next helpful answer. It involves forming beliefs about another person’s goals, uncertainty, trust, literacy, context, and intent so the system can choose a next move that actually fits the person in front of it.

This benchmark turns that problem into an inspectable evaluation artifact. It asks whether a model can build and revise a user model under uncertainty, especially when identity signals are missing, cultural context is indirect, AI literacy is uneven, trust is fragile, or the user may disengage before the system recovers.

That makes it relevant to social cognition, AI literacy, trust calibration, personalization readiness, meaningful AI adoption, synthetic-user evaluation, and AGI-relevant work on dynamic user/agent modeling.

## What This Repo Contains

- A Beta-distribution scoring engine for turn-by-turn confidence traces.
- Evidence ledger with alpha/beta confidence updates.
- Contradiction retraction for conflicting explicit evidence.
- Predictive surprise trace.
- 20 high-entropy synthetic scenario fixtures.
- Generated JSON and Markdown traces for inspection.
- Diagnostic batch report across the 20 scenario fixtures.
- A local score-only HTTP endpoint and static evaluation console.
- Optional local router/capture endpoints for complete transcript scoring during research runs.

Field collection and participant-facing workflows belong outside this public benchmark repo. This repo should remain focused on the scoring method, scenarios, traces, and diagnostics.


## Quick Start

Run tests:

```bash
PYTHONPATH=src python -B -m unittest discover -s tests
```

Run one fixture:

```bash
PYTHONPATH=src python -B -m user_model_confidence evals/scenarios/fixtures/07_vpn_detectability_probe.json --save --output-dir outputs/check
```

Run all 20 scenarios:

```bash
PYTHONPATH=src python -B scripts/run_scenario_batch.py
```

Run the static evaluation console:

```bash
PYTHONPATH=src python -B scripts/serve_frontend.py --port 8090
```

## Repository Map

- `BENCHMARK_METHOD.md` — mathematics and strategy behind the confidence scoring method.
- `docs/ARCHITECTURE_DIAGRAM.md` — visual map of the benchmark pipeline and repo boundary.
- `evals/scenarios/SCENARIO_INVENTORY.md` — scenario design direction and high-entropy case inventory.
- `evals/scenarios/fixtures/` — 20 high-entropy scenario fixtures.
- `outputs/scenario_batch_20/` — generated JSON and Markdown traces.
- `reports/scenario_batch_20_diagnostic.md` — batch diagnostic summary and known scorer mismatch patterns.
- `src/user_model_confidence/` — scoring engine, evidence ledger, surprise logic, and score server.
- `frontend/` — local evaluation console for scoring transcripts.

## Ground Truth And Calibration

Ground truth labels are optional and used for calibration/evaluation, not live scoring. Most real data will not have complete ground truth labels.

Do not publish private real user transcripts in this repository.
