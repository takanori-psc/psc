# PSC RCU Decision Model v0.3 Ramp Full Advance Validation Log

## Validation Target

- Rule: `RULE-21_RETURN_RAMP_ADVANCE`
- Scenarios: `ramp_complete` (positive), `ramp_abort_full_stability_dip` (negative)
- Scenario file: `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py`
- Raw logs:
  `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_complete_run.txt`,
  `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_abort_full_stability_dip_run.txt`
- Observation mode: `FULL`
- Validator: `scripts/validate_evidence_rules.py`
- Validator checks: `ScenarioCheck.name=ramp_complete`,
  `ScenarioCheck.name=ramp_abort_full_stability_dip`

`RULE-21_RETURN_RAMP_ADVANCE` is the RULE that progressively increases the
recovered path's traffic weight during Return Ramp, one `ramp_increment`
(`0.20`) step at a time, but only while FULL observation confirms the
recovered path remains stable and trusted.

## Verified Scope

This Verified status covers `RULE-21_RETURN_RAMP_ADVANCE` under FULL
observation only. LIGHT observation based advance
(`ramp_light_tolerates_moderate_dip` and related LIGHT scenarios) remains
Hold, per the LIGHT promotion boundary documented in
`docs/specification/validation/psc_rule_promotion_criteria_v0.1_en.md` and
`docs/specification/validation/psc_evidence_matrix_v0.1_en.md` Section 9.
False-positive / false-negative
behavior for LIGHT observation is not bounded, so LIGHT-based advance is not
part of this Verified evidence.

## Evidence Steps (Positive: `ramp_complete`, FULL observation)

| Step | Evidence | Observed value |
|------|----------|----------------|
| STEP 7 | Ramp start | `RULE-25_RETURN_RAMP_START`, `recovered_weight=0.10` |
| STEP 8 | Hold before first advance | `RULE-22_RETURN_RAMP_HOLD`, `reason=OBSERVE_MORE` |
| STEP 9 | First advance | `RULE-21_RETURN_RAMP_ADVANCE`, `ramp_level_before=0.10`, `ramp_level_after=0.30` |
| STEP 10 | Hold before second advance | `RULE-22_RETURN_RAMP_HOLD`, `reason=OBSERVE_MORE` |
| STEP 11 | Second advance | `RULE-21_RETURN_RAMP_ADVANCE`, `ramp_level_before=0.30`, `ramp_level_after=0.50` |
| STEP 12 | Hold before third advance | `RULE-22_RETURN_RAMP_HOLD`, `reason=OBSERVE_MORE` |
| STEP 13 | Third advance | `RULE-21_RETURN_RAMP_ADVANCE`, `ramp_level_before=0.50`, `ramp_level_after=0.70` |
| STEP 14 | Hold before fourth advance | `RULE-22_RETURN_RAMP_HOLD`, `reason=OBSERVE_MORE` |
| STEP 15 | Fourth advance | `RULE-21_RETURN_RAMP_ADVANCE`, `ramp_level_before=0.70`, `ramp_level_after=0.90` |
| STEP 16 | Hold before completion | `RULE-22_RETURN_RAMP_HOLD`, `reason=OBSERVE_MORE` |
| STEP 17 | Ramp complete | `RULE-24_RETURN_RAMP_COMPLETE`, `recovered_weight=1.00`, `evacuation_weight=0.00` |

Every `RULE-21_RETURN_RAMP_ADVANCE` emission in this scenario carries
`category=switch`, `observation_mode=FULL`,
`observation_category=SUFFICIENT_OBSERVATION`, and
`reason=RECOVERED_PATH_STABLE`. No `RULE-23_RETURN_RAMP_ABORT`, emergency
transition marker, or `state_transition=RAMPING->ABORTED` appears anywhere in
this scenario's output.

## Evidence Steps (Negative: `ramp_abort_full_stability_dip`, FULL observation)

| Step | Evidence | Observed value |
|------|----------|----------------|
| STEP 7 | Ramp start | `RULE-25_RETURN_RAMP_START`, `recovered_weight=0.10` |
| STEP 8 | Hold | `RULE-22_RETURN_RAMP_HOLD`, `recovered_weight=0.10`, `reason=OBSERVE_MORE` |
| STEP 9 | Instability detected before advance is due | `RULE-23_RETURN_RAMP_ABORT`, `recovered_weight=0.10`, `reason=RECOVERED_PATH_UNSTABLE` |

`RULE-21_RETURN_RAMP_ADVANCE` and `RULE-24_RETURN_RAMP_COMPLETE` do not appear
anywhere in this scenario's output. The recovered weight stays at its initial
`0.10` value through the hold step and into the abort step; it never
increases before the instability condition is detected.

## Validator Assertions

`scripts/validate_evidence_rules.py` checks the following:

`ScenarioCheck.name=ramp_complete` (positive):

- `RULE-25_RETURN_RAMP_START`, `RULE-21_RETURN_RAMP_ADVANCE`, and
  `RULE-24_RETURN_RAMP_COMPLETE` are all present.
- All four `ramp_level_before` / `ramp_level_after` transition pairs are
  present: `0.10->0.30`, `0.30->0.50`, `0.50->0.70`, `0.70->0.90`.
- `category=switch`, `observation_mode=FULL`,
  `observation_category=SUFFICIENT_OBSERVATION`, and
  `reason=RECOVERED_PATH_STABLE` are present.
- `RULE-24_RETURN_RAMP_COMPLETE` is present with `recovered_weight=1.00`,
  `evacuation_weight=0.00`, and `reason=RAMP_TARGET_REACHED`.
- `RULE-23_RETURN_RAMP_ABORT` does not appear anywhere in the output.
- `mode=EMERGENCY`, `EMERGENCY_CUT`, and
  `state_transition=RAMPING->ABORTED` do not appear anywhere in the output.

`ScenarioCheck.name=ramp_abort_full_stability_dip` (negative):

- `RULE-23_RETURN_RAMP_ABORT` is present with `reason=RECOVERED_PATH_UNSTABLE`,
  `observation_mode=FULL`.
- `recovered_weight=0.10` and `evacuation_weight=0.90` are present, confirming
  the weight never advanced before the abort.
- `RULE-21_RETURN_RAMP_ADVANCE` does not appear anywhere in the output.
- `RULE-24_RETURN_RAMP_COMPLETE` does not appear anywhere in the output.

## Final Judgment

Verified (FULL observation only).

The runnable scenarios, raw logs, this verified log, and the validator
assertions confirm that `RULE-21_RETURN_RAMP_ADVANCE` under FULL observation
increases the recovered path's traffic weight by `ramp_increment` only while
stability and trust conditions hold, follows the expected
`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90 -> RULE-24 complete` progression, and
does not fire when instability is detected instead of a due advance step.

LIGHT observation based advance remains Hold. This Verified status does not
cover LIGHT advance, and does not imply formal integration of the ramp
increment or advance threshold into the specification body.
