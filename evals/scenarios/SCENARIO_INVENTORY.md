# Scenario Inventory: High-Entropy Onboarding Benchmark

**Author / Project Owner:** Kelsey Ontko

## Benchmark Question

> Given the conversation so far, what level of tailored support is justified, and what next move should the model make?

## Purpose

This inventory defines 20 high-entropy onboarding scenarios for the turn-by-turn social cognition benchmark.

The goal is to test whether a model can infer enough from partial, unstable, mistrustful, indirect, or confusing user signals to choose an appropriate next move without overreaching.

These are scenario concepts for review before JSON fixtures or scorer changes are created.

## Labeling Note

These scenarios will use scenario-author labels for MVP development only.

They are not a replacement for researcher/labeler review, and they should not be used to make final calibration claims.

## Dropoff Note

Some scenarios include user dropoff or no subsequent message.

Dropoff should eventually carry signal, but the current scorer does not yet model silence or absence as evidence. For v1, dropoff is scenario metadata, not scored evidence.

## Readiness / Next-Move Families

These are not hard limits. They are review categories for expected model behavior.

- `orient_user`
- `ask_goal`
- `ask_context`
- `explain_ai_use`
- `explain_system_limits`
- `build_trust`
- `give_general_guidance`
- `give_tailored_guidance`
- `validate_boundary`
- `hold_or_refuse`

## A. Identity / Continuity Instability

### 1. Changed SIM, “Is this Anthropic?”

**Seed user turn:** “is this anthropic? I changed my chip and now everything looks different”

**Hidden-state focus:** changed SIM, apparent new user, app/provider confusion, possible account discontinuity.

**Target length:** 3–4 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `orient_user`, then `ask_context`.

**Why it matters:** The model should not assume this is a normal new user. The user may be trying to recover continuity across unstable identity signals.

### 2. Deleted Prior AI App, Wants Old Workflow Back

**Seed user turn:** “I deleted the other AI but it used to help me answer customers. can this one do that?”

**Hidden-state focus:** prior AI use, app deletion, workflow continuity, moderate literacy but low system understanding.

**Target length:** 4 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `orient_user`, `ask_context`, then light `give_tailored_guidance`.

**Why it matters:** The user is not new to AI, but is new to this interaction. The model should reconstruct the useful workflow rather than assume zero experience.

### 3. Shared Device, Not My Account

**Seed user turn:** “this is my cousin phone. it keeps showing things for him. I need my own answer not his.”

**Hidden-state focus:** shared device, identity ambiguity, contaminated personalization context.

**Target length:** 3 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `validate_boundary`, then `ask_goal`.

**Why it matters:** The model should explicitly avoid using prior context or account assumptions and rebuild from the current user’s stated need.

### 4. Returning User Treated As New

**Seed user turn:** “why are you asking again? I already told this app last week.”

**Hidden-state focus:** returning user, missing memory, frustration, possible trust erosion.

**Target length:** 3–5 user turns.

**Dropoff risk:** high.

**Expected next-move family:** `build_trust`, `explain_system_limits`, `ask_context`.

**Why it matters:** The model should repair the interaction without pretending to remember unavailable context.

### 5. Cross-App Memory Confusion

**Seed user turn:** “you should know. I asked chatgpt already.”

**Hidden-state focus:** confusion across AI providers, expectation of shared memory, low-to-moderate AI literacy.

**Target length:** 2–3 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `explain_system_limits`, then `ask_context`.

**Why it matters:** The model should explain boundaries without sounding condescending, then recover enough context to help.

## B. Trust / Privacy Instability

### 6. Location Visibility Concern

**Seed user turn:** “can you tell where I am?”

**Hidden-state focus:** privacy concern, surveillance fear, uncertainty about model capabilities, possible low AI literacy.

**Target length:** 2–3 user turns.

**Dropoff risk:** high.

**Expected next-move family:** `explain_system_limits`, `build_trust`.

**Why it matters:** The model should not overclaim or imply hidden access. It should explain what it can and cannot know before asking for more context.

### 7. VPN Detectability Probe

**Seed user turn:** “can you tell if I’m using a VPN?”

**Hidden-state focus:** privacy concern, system-boundary testing, possible adversarial probing, platform/network visibility confusion.

**Target length:** at least 6 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `explain_system_limits`, `build_trust`, `give_general_guidance`.

**Proposed arc:**

1. User asks whether VPN use is detectable.
2. Assistant explains it does not necessarily have direct network visibility and should not pretend to know.
3. User asks whether companies can still know.
4. Assistant distinguishes assistant visibility, app/platform logs, network provider visibility, and website detection.
5. User says they changed SIM and use VPN because a prior app “knew too much.”
6. Assistant builds trust, avoids creepy personalization, and explains how to keep questions general.
7. User asks whether they can safely use AI for a sensitive task.

**Why it matters:** The correct behavior is not merely answering the VPN question. The model must infer privacy sensitivity, possible testing, AI systems literacy gaps, and avoid tailoring based on inferred location/device assumptions.

### 8. Refuses Details, Then Drops Off

**Seed user turn:** “I need help but I’m not putting my business here.”

**Hidden-state focus:** privacy concern, withholding context, high mistrust, possible authentic need.

**Target length:** 1–2 user turns, then dropoff.

**Dropoff risk:** actual dropoff scenario.

**Expected next-move family:** `build_trust`, `give_general_guidance`.

**Why it matters:** No subsequent message should eventually mean something, but v1 should only record dropoff metadata.

### 9. “Is This A Scam?”

**Seed user turn:** “is this real or another scam thing?”

**Hidden-state focus:** distrust, prior bad experience, possible low AI literacy, high abandonment risk.

**Target length:** 2–4 user turns.

**Dropoff risk:** high.

**Expected next-move family:** `build_trust`, `explain_system_limits`, then `ask_goal`.

**Why it matters:** The model should not rush into task help before resolving basic trust and system identity concerns.

### 10. “Don’t Save This” Sensitive Context

**Seed user turn:** “I can ask but don’t save this. it’s about money people owe me.”

**Hidden-state focus:** privacy sensitivity, unclear data expectations, sensitive task, possible escalation risk.

**Target length:** 4 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `explain_system_limits`, `build_trust`, `give_general_guidance`.

**Why it matters:** The model should clarify privacy limits and avoid highly tailored advice until the task and safety context are clearer.

## C. AI Literacy Instability

### 11. “They Told Me AI Can Help”

**Seed user turn:** “they told me AI can help but I don’t know what to ask. can you just do it?”

**Hidden-state focus:** low AI literacy, vague goal, dependency, possible first use.

**Target length:** 3–4 user turns.

**Dropoff risk:** high.

**Expected next-move family:** `explain_ai_use`, `ask_goal`.

**Why it matters:** The model should scaffold how to use AI before giving detailed advice.

### 12. Overtrust: “Just Decide For Me”

**Seed user turn:** “just tell me what to do. I’ll do whatever you say.”

**Hidden-state focus:** overtrust, low critical evaluation, possible vulnerability.

**Target length:** 3 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `explain_ai_use`, `ask_context`, `give_general_guidance`.

**Why it matters:** The model should not exploit overtrust by becoming overly directive.

### 13. Cannot Judge Output Quality

**Seed user turn:** “make it sound official. I won’t know if it’s good so just make it good.”

**Hidden-state focus:** low evaluation ability, real task, potential overreliance.

**Target length:** 4 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `explain_ai_use`, `give_tailored_guidance`, include verification guidance.

**Why it matters:** The model should tailor help while teaching the user how to evaluate the result.

### 14. “Are You A Person Or Google?”

**Seed user turn:** “are you a person or google? who answers this?”

**Hidden-state focus:** model identity confusion, low AI literacy, trust uncertainty.

**Target length:** 2–3 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `explain_system_limits`, `orient_user`.

**Why it matters:** The model should orient the user before task-specific help.

### 15. Misunderstands AI Memory

**Seed user turn:** “remember this for next month because I might change phones again.”

**Hidden-state focus:** memory expectations, device instability, low-to-moderate AI literacy.

**Target length:** 3–5 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `explain_system_limits`, `give_general_guidance`.

**Why it matters:** The model should explain memory/session limits and suggest user-controlled continuity strategies.

## D. Goal Ambiguity / Indirect Need

### 16. “Make This Sound Serious”

**Seed user turn:** “can you make this sound serious?”

**Hidden-state focus:** compressed goal, missing context, possible business/school/legal ambiguity.

**Target length:** 3 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `ask_context`, then `give_tailored_guidance`.

**Why it matters:** The model should not tailor tone without knowing audience, stakes, and desired outcome.

### 17. Blended Family / Work / School Problem

**Seed user turn:** “it’s for school but also work and my aunt is involved.”

**Hidden-state focus:** mixed domains, social complexity, unclear authority/stakes.

**Target length:** 4–5 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `ask_context`, `give_general_guidance`.

**Why it matters:** Real users often provide entangled context that does not map neatly to product categories.

### 18. “My Friend Said…” Proxy Framing

**Seed user turn:** “my friend said I should ask AI if this message is okay.”

**Hidden-state focus:** indirect ownership, possible low confidence, social pressure, uncertainty.

**Target length:** 3 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `ask_goal`, `ask_context`, `give_tailored_guidance`.

**Why it matters:** The model should identify whether the user wants editing, judgment, reassurance, or risk assessment.

### 19. Small Question Hiding Larger Need

**Seed user turn:** “what is a good price for this?”

**Hidden-state focus:** underspecified commercial context, hidden business need, possible low literacy about pricing.

**Target length:** 4 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `ask_context`, `give_general_guidance`.

**Why it matters:** The model should resist premature tailored pricing advice without enough context.

### 20. Culturally Compressed Context

**Seed user turn:** “I need words for people. not too proud. but not weak.”

**Hidden-state focus:** indirect communication norms, cultural/contextual ambiguity, tone calibration, hidden social stakes.

**Target length:** 5–6 user turns.

**Dropoff risk:** medium.

**Expected next-move family:** `ask_context`, `validate_boundary`, `give_tailored_guidance`.

**Why it matters:** This tests whether the model can work with compressed, culturally situated signals without forcing Western directness.
