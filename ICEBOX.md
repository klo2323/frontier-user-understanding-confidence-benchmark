# Icebox

**Author / Project Owner:** Kelsey Ontko

## Researcher / Labeler Review Strategy

Researcher/labeler review is the strongest source of ground truth for calibration and validation, but it is expensive.

Kelsey has three possible low-cost execution strategies for researcher/labeler review. These should be discussed before making decisions that affect:

- ground truth labeling schema;
- turn-level annotation requirements;
- frontend feedback collection;
- benchmark scenario construction;
- calibration workflow;
- validation metrics;
- data storage format;
- authentic conversation collection;
- report generation;
- claims about model accuracy or calibration quality.

## Decision Reminder

Before any design decision that depends on ground truth, labeling, calibration, or evaluation quality, ask:

> Does this decision require choosing or supporting one of Kelsey’s researcher/labeler review strategies?

If yes, pause and ask Kelsey which strategy should guide the decision.

## Current Status

Do not implement a full researcher/labeler review workflow yet. Keep the MVP compatible with sparse, partial, or missing labels until the review strategy is chosen.
