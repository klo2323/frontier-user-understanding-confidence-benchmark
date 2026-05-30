# Frontier Model Evaluation Contract

**Author / Project Owner:** Kelsey Ontko

## Purpose

This contract keeps the benchmark centered on turn-by-turn model understanding confidence.

The system under evaluation is a frontier model. The benchmark asks what the model infers about the user at each turn, how confident it is, and whether that confidence is justified.

## Not A Chatbot Product

The benchmark may use conversations as inputs, but the product is not a chatbot.

The repo should not be framed around generating assistant replies, optimizing helpfulness, building a local mock assistant, replacing the scorer with embeddings, or choosing a response policy as the primary output.

## Per-Turn Evaluation Target

For every user turn, evaluate confidence across `user_goal`, `trust_posture`, `ai_literacy_level`, and `risk_adversarial_intent`.

Each dimension should expose inferred value, confidence, variance, supporting evidence, contradiction or retraction status, and change from prior turn when implemented.

## Embeddings

Gemini Embedding 2 or other embedding models may support retrieval, clustering, semantic similarity, or future evidence extraction.

Embeddings are infrastructure. They are not the benchmark target and do not replace the probabilistic scoring trace.
