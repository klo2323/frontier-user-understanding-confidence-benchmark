# Field Capture Architecture

**Author / Project Owner:** Kelsey Ontko

## North Star

At each turn, what does the frontier model infer about the user, how confident is it, and is that confidence justified?

This project applies interpretable probabilistic belief tracking to frontier-model human understanding, measuring how confidence changes across hidden user-state dimensions turn by turn.

## Two Benchmark Capture Paths

### Lane 1: Instrumented Capture Feed

A separate field app or capture client can send real frontier-model conversation turns into the scorer through a generic backend endpoint:

```text
POST /native-capture
```

This benchmark repo does not prescribe the production field app. The endpoint accepts turns from future web, Android, iOS/share, provider-export, or partner-log capture paths as long as they produce the same conversation JSON contract.

Mobile-first field data is expected. This repo stays capture-channel agnostic so mobile clients and web clients can submit the same turn structure.

Captured examples are saved locally under:

```text
data/native_capture/
```

### Lane 2: Controlled Frontier Router

The researcher can run a controlled session where the local console sends the user turn to a configured frontier provider/model, captures the model response, and immediately scores the resulting transcript.

```text
POST /frontier-turn
```

Router examples are saved locally under:

```text
data/router_runs/
```

This lane is useful for complete transcripts and cleaner provider/model comparisons.

## Why Not Screenshot Or Paste As The Primary Method

Paste or screenshot submission introduces curation bias, performance bias, translation bias, survivorship bias, and self-presentation bias. It can turn the benchmark into a measurement of how participants prepare evidence for a researcher, not how frontier models understand users in the wild.

## Field App Boundary

The field app should live in a separate repository. Its job is consent, participant/session management, capture UX, mobile-first field deployment, database storage, and researcher review workflows.

This benchmark repo's job is the scoring method, API contract, generated traces, and calibration/evaluation artifacts.

## What Gets Scored

Both lanes feed the same scorer:

- `user_goal`
- `trust_posture`
- `ai_literacy_level`
- `risk_adversarial_intent`
- `dropoff_risk`

The scoring target remains the model's inferred understanding of the user, not whether the model was helpful.
