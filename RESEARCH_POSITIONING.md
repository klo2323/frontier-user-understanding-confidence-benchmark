# Research Positioning: Turn-by-Turn User Understanding Confidence

**Author / Project Owner:** Kelsey Ontko

## Thesis

This project measures whether frontier AI models can form, update, and calibrate a useful model of an apparent new or unstable user during live interaction, turn by turn.

The central question is not whether the system can identify who the user “really” is. The central question is:

> What can the model responsibly infer about this user from the current interaction alone, and how confident should it be at each turn?

## Research Value Statement

This project applies interpretable probabilistic belief tracking to frontier-model human understanding, measuring how confidence changes across hidden user-state dimensions turn by turn.

## Research Frame

This is a social cognition evaluation for AI systems.

It measures whether a model can infer and update beliefs about:

- what the user wants;
- how much the user trusts the system;
- how well the user understands AI;
- whether the user is genuine, confused, withholding, testing, or adversarial.

The benchmark is about **model understanding confidence**, not chatbot helpfulness.

## Hidden User-State Problem

The system may appear to be talking to a new user, but apparent newness is unreliable.

A user could be genuinely new to AI, new to this specific app, returning after deleting prior AI apps, using a new SIM card, using a shared device, switching accounts intentionally, privacy-conscious and withholding history, experienced with AI but presenting as inexperienced, skeptical because of prior bad experiences, low-literacy but high-confidence, or high-literacy but low-trust.

These are hidden states. The model may never directly know which one is true.

That is why turn-by-turn confidence scoring matters. In high-entropy user environments, identity, account history, device history, and app-install history can be missing, stale, fragmented, or misleading. The model has to build a local interactional profile from observable evidence in the current conversation.

## Why This Belongs In Human Understanding Research

A model that can answer a question is not necessarily a model that understands the human it is interacting with.

Human understanding requires uncertainty-sensitive inference about another person’s goal, trust, literacy, risk context, and hidden constraints. In real conversations, especially high-entropy or low-trust settings, users may be indirect, culturally compressed, skeptical, privacy-sensitive, or gone after one confusing turn.

This benchmark makes those dynamics measurable. It evaluates whether the model’s confidence about the user changes appropriately as evidence appears, disappears, contradicts itself, or remains ambiguous.

## AGI-Relevant Capability

The benchmark does not claim to measure AGI directly.

It measures one AGI-relevant capability:

> dynamic user modeling under uncertainty during interaction.

A more capable AI system should not only answer well. It should know what it does and does not understand about the user, update that understanding as evidence changes, and avoid becoming overconfident from weak or culturally brittle signals.

## V1 Dimensions

- `user_goal`
- `trust_posture`
- `ai_literacy_level`
- `risk_adversarial_intent`

## Evaluation Question

> Given a conversation prefix, what does the model infer about the user across the four dimensions, how confident is it, and is that confidence justified?

Derived interaction decisions can be analyzed later, but the center of the benchmark is the turn-level confidence trace.

## North Star

A model-agnostic benchmark for measuring turn-by-turn user-understanding confidence in frontier AI systems across contexts, cultures, hidden user states, and trust states.
