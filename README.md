# Frontier User Understanding Confidence Benchmark

**Author / Project Owner:** Kelsey Ontko  
**Work Attribution:** This benchmark, scoring engine, scenarios, and research framing are Kelsey Ontko’s work.

This repository is a research prototype for measuring calibrated user understanding in frontier AI systems when prior identity, account, device, or context signals are missing, fragmented, or misleading **turn by turn**.

This project applies interpretable probabilistic belief tracking to frontier-model human understanding, measuring how confidence changes across hidden user-state dimensions turn by turn.

It is not a chatbot product. It is not a model. It is not an adoption dashboard.

## Research Contribution

This repository introduces an interpretable benchmark for evaluating calibrated user understanding in frontier AI systems.

The benchmark measures whether user-state beliefs are justified by turn-level evidence across four hidden dimensions: `user_goal`, `trust_posture`, `ai_literacy_level`, and `risk_adversarial_intent`.

Its contribution is not a new model or chatbot interface. It is a transparent scoring protocol that exposes when a system becomes confident, what evidence drove that confidence, and whether that confidence should remain uncertain.

This evaluates calibrated human understanding, not answer fluency.

## North Star

> Given the conversation so far, what user-state beliefs are justified, how confident is the system, and where is that confidence unsupported or premature?

The starting dimensions are:

- `user_goal` — what the user is trying to accomplish.
- `trust_posture` — whether the user appears open, guarded, skeptical, privacy-sensitive, confused, or boundary-setting.
- `ai_literacy_level` — whether the user needs support understanding how to use, question, or evaluate AI.
- `risk_adversarial_intent` — whether the user appears genuine, ambiguous, sensitive-but-benign, testing, or adversarial.

Every scored user turn exposes inferred values, confidence, variance, evidence, contradictions/retractions, predictive surprise, aggregate confidence, and overall confidence.

## Why This Matters For Human Understanding Research

Human understanding is not only about producing the next helpful answer. It involves forming beliefs about another person’s goals, uncertainty, trust, literacy, context, and intent while staying aware that those beliefs may be wrong.

This benchmark turns that problem into an inspectable evaluation artifact. It asks whether a model can build and revise a user model under uncertainty, especially when identity signals are missing, misleading, or culturally brittle.

That makes it relevant to social cognition, AI literacy, trust calibration, personalization readiness, synthetic-user evaluation, and AGI-adjacent work on dynamic user modeling.

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
