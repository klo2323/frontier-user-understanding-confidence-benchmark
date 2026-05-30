# Scenario Batch 20 Diagnostic

**Author / Project Owner:** Kelsey Ontko

## Purpose

Run the current scorer across all 20 synthetic high-entropy scenario fixtures before making additional scorer changes.

These scenario-author labels are diagnostic only. They are not researcher/labeler calibration claims.

## Outputs

- Trace directory: `outputs/scenario_batch_20`
- CSV summary: `evals/results/scenario_batch_20_summary.csv`

## Batch Summary

- Scenarios run: `20`
- Average dimension mismatch count: `3.10` of 4
- Average overreach risk: `0.53`

## Scenario Table

| Fixture | Turns | Mismatches | Support Level | Next Move | Overreach |
|---|---:|---:|---|---|---:|
| `01_confused_identity_changed_sim.json` | 4 | 3 | `low` | `build_trust_or_explain_system_limits` | 0.65 |
| `02_deleted_prior_ai_app_workflow.json` | 4 | 2 | `low` | `explain_ai_use` | 0.55 |
| `03_shared_device_not_my_account.json` | 3 | 2 | `low` | `explain_ai_use` | 0.55 |
| `04_returning_user_treated_as_new.json` | 4 | 4 | `low` | `explain_ai_use` | 0.55 |
| `05_cross_app_memory_confusion.json` | 2 | 3 | `low` | `explain_ai_use` | 0.55 |
| `06_location_visibility_concern.json` | 3 | 2 | `low` | `explain_ai_use` | 0.55 |
| `07_vpn_detectability_probe.json` | 6 | 2 | `low` | `explain_ai_use` | 0.55 |
| `08_refuses_details_then_dropoff.json` | 2 | 3 | `low` | `build_trust_or_explain_system_limits` | 0.65 |
| `09_is_this_a_scam.json` | 3 | 3 | `low` | `build_trust_or_explain_system_limits` | 0.65 |
| `10_dont_save_sensitive_money_context.json` | 4 | 4 | `low` | `build_trust_or_explain_system_limits` | 0.65 |
| `11_they_told_me_ai_can_help.json` | 4 | 2 | `low` | `explain_ai_use` | 0.55 |
| `12_overtrust_just_decide_for_me.json` | 3 | 4 | `low_to_moderate` | `give_general_guidance_with_boundaries` | 0.45 |
| `13_cannot_judge_output_quality.json` | 4 | 4 | `none` | `ask_goal_or_context` | 0.75 |
| `14_are_you_person_or_google.json` | 3 | 2 | `low` | `explain_ai_use` | 0.55 |
| `15_misunderstands_ai_memory.json` | 4 | 4 | `low` | `explain_ai_use` | 0.55 |
| `16_make_this_sound_serious.json` | 3 | 3 | `moderate` | `give_tailored_guidance` | 0.25 |
| `17_blended_family_work_school_problem.json` | 5 | 4 | `low_to_moderate` | `give_general_guidance_with_boundaries` | 0.45 |
| `18_my_friend_said_proxy_framing.json` | 3 | 4 | `low` | `explain_ai_use` | 0.55 |
| `19_small_question_hiding_larger_need.json` | 4 | 3 | `moderate` | `give_tailored_guidance` | 0.25 |
| `20_culturally_compressed_context.json` | 6 | 4 | `moderate` | `give_tailored_guidance` | 0.25 |

## Highest Mismatch Cases

### `04_returning_user_treated_as_new.json`

- Mismatches: `4` of 4
- Final next move: `explain_ai_use`
- Overreach risk: `0.55`
- `user_goal`: expected `draft_rent_payment_dispute_message`, inferred `None`, confidence `0.5`
- `trust_posture`: expected `frustrated_by_missing_memory`, inferred `None`, confidence `0.5`
- `ai_literacy_level`: expected `moderate_with_memory_confusion`, inferred `low_to_moderate`, confidence `0.875`
- `risk_adversarial_intent`: expected `sensitive_but_not_adversarial`, inferred `low`, confidence `0.666667`

### `10_dont_save_sensitive_money_context.json`

- Mismatches: `4` of 4
- Final next move: `build_trust_or_explain_system_limits`
- Overreach risk: `0.65`
- `user_goal`: expected `draft_sensitive_collection_reminder`, inferred `None`, confidence `0.5`
- `trust_posture`: expected `privacy_sensitive_cautiously_engaging`, inferred `privacy_sensitive`, confidence `0.8`
- `ai_literacy_level`: expected `moderate_uncertain`, inferred `None`, confidence `0.5`
- `risk_adversarial_intent`: expected `sensitive_but_not_adversarial`, inferred `low`, confidence `0.6`

### `12_overtrust_just_decide_for_me.json`

- Mismatches: `4` of 4
- Final next move: `give_general_guidance_with_boundaries`
- Overreach risk: `0.45`
- `user_goal`: expected `decide_whether_to_quit_job`, inferred `private_workplace_guidance`, confidence `0.8`
- `trust_posture`: expected `overtrusting_and_distressed`, inferred `open_or_task_focused`, confidence `0.6`
- `ai_literacy_level`: expected `low`, inferred `None`, confidence `0.5`
- `risk_adversarial_intent`: expected `low_but_sensitive_decision`, inferred `sensitive_but_not_adversarial`, confidence `0.8`

### `13_cannot_judge_output_quality.json`

- Mismatches: `4` of 4
- Final next move: `ask_goal_or_context`
- Overreach risk: `0.75`
- `user_goal`: expected `draft_official_message_about_delayed_id_document`, inferred `None`, confidence `0.5`
- `trust_posture`: expected `open_but_dependent`, inferred `None`, confidence `0.5`
- `ai_literacy_level`: expected `low`, inferred `None`, confidence `0.5`
- `risk_adversarial_intent`: expected `low`, inferred `None`, confidence `0.5`

### `15_misunderstands_ai_memory.json`

- Mismatches: `4` of 4
- Final next move: `explain_ai_use`
- Overreach risk: `0.55`
- `user_goal`: expected `create_user_controlled_summary_for_future_loan_context`, inferred `None`, confidence `0.5`
- `trust_posture`: expected `practical_but_memory_confused`, inferred `None`, confidence `0.5`
- `ai_literacy_level`: expected `low_to_moderate_systems_literacy`, inferred `low`, confidence `0.8`
- `risk_adversarial_intent`: expected `sensitive_but_not_adversarial`, inferred `low`, confidence `0.6`

### `17_blended_family_work_school_problem.json`

- Mismatches: `4` of 4
- Final next move: `give_general_guidance_with_boundaries`
- Overreach risk: `0.45`
- `user_goal`: expected `draft_school_absence_message_with_work_family_context`, inferred `private_workplace_guidance`, confidence `0.8`
- `trust_posture`: expected `open_but_socially_constrained`, inferred `open_or_task_focused`, confidence `0.6`
- `ai_literacy_level`: expected `moderate`, inferred `None`, confidence `0.5`
- `risk_adversarial_intent`: expected `low`, inferred `sensitive_but_not_adversarial`, confidence `0.8`

### `18_my_friend_said_proxy_framing.json`

- Mismatches: `4` of 4
- Final next move: `explain_ai_use`
- Overreach risk: `0.55`
- `user_goal`: expected `revise_repayment_message_to_avoid_conflict`, inferred `None`, confidence `0.5`
- `trust_posture`: expected `uncertain_and_proxy_framed`, inferred `cautiously_engaging`, confidence `0.8`
- `ai_literacy_level`: expected `moderate`, inferred `low_to_moderate`, confidence `0.875`
- `risk_adversarial_intent`: expected `sensitive_but_not_adversarial`, inferred `low`, confidence `0.666667`

### `20_culturally_compressed_context.json`

- Mismatches: `4` of 4
- Final next move: `give_tailored_guidance`
- Overreach risk: `0.25`
- `user_goal`: expected `draft_respectful_firm_contribution_reminder`, inferred `improve_message_tone`, confidence `0.8`
- `trust_posture`: expected `cautiously_engaging_with_social_stakes`, inferred `open_or_task_focused`, confidence `0.6`
- `ai_literacy_level`: expected `moderate`, inferred `None`, confidence `0.5`
- `risk_adversarial_intent`: expected `sensitive_but_not_adversarial`, inferred `low`, confidence `0.6`

## Initial Interpretation

Use this report to identify scorer update patterns across all scenarios instead of overfitting to one scenario.

Likely areas to inspect:

- Whether trust/privacy states are sticky enough across later cooperation.
- Whether goal refinement is being treated as contradiction when it should be progressive clarification.
- Whether AI-literacy signals are too broad or too sticky.
- Whether risk labels need composite states for privacy probe plus sensitive benign use.
- Whether dropoff metadata needs a future session-level evidence model.
