# PSC RCU Decision Model v0.3 Ramp Complete Validation Log

## Validation Target

- Rule: `RULE-24_RETURN_RAMP_COMPLETE`
- Scenario: `ramp_complete`
- Scenario file: `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py`
- Raw log: `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_complete_run.txt`
- Observation mode: `FULL`
- Validator: `scripts/validate_evidence_rules.py`
- Validator check: `ScenarioCheck.name=ramp_complete`

`RULE-24_RETURN_RAMP_COMPLETE` is the RULE that confirms completion of the
Return Ramp once the recovered path's traffic weight reaches
`ramp_max_weight` (`1.00`), ending progressive reintegration and returning
PSC to NORMAL mode.

This log reuses the same `ramp_complete` scenario and raw log used for
`RULE-21_RETURN_RAMP_ADVANCE` Verified evidence
(`rcu_decision_v03_ramp_full_advance_validation_log.md`), extended from 18 to
22 steps to capture the post-completion tail.

## Evidence Steps

| Step | Evidence | Observed value |
|------|----------|----------------|
| STEP 15 | Final advance before completion | `RULE-21_RETURN_RAMP_ADVANCE`, `ramp_level_before=0.70`, `ramp_level_after=0.90` |
| STEP 16 | Hold before completion | `RULE-22_RETURN_RAMP_HOLD`, `recovered_weight=0.90`, `reason=OBSERVE_MORE` |
| STEP 17 | Ramp complete | `RULE-24_RETURN_RAMP_COMPLETE`, `selected=B`, `recovered_weight=1.00`, `evacuation_weight=0.00`, `observation_mode=FULL`, `reason=RAMP_TARGET_REACHED` |
| STEP 18 | Post-completion cooldown | `RULE-11_RECOVERY_cooldown`, `remaining=2`, `reason=RECOVERY_COOLDOWN` |
| STEP 19 | Post-completion cooldown | `RULE-11_RECOVERY_cooldown`, `remaining=1`, `reason=RECOVERY_COOLDOWN` |
| STEP 20 | Post-completion stable state | `RULE-01_KEEP_score`, `selected=B best=B`, `mode=NORMAL`, `reason=HYSTERESIS_HOLD` |
| STEP 21 | Post-completion stable state | `RULE-01_KEEP_score`, `selected=B best=B`, `mode=NORMAL`, `reason=HYSTERESIS_HOLD` |

## Completion Threshold

Completion fires when `recovery_ramp_weight` reaches `ramp_max_weight`
(`1.00`) after an advance step, per
`sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py`.
With `ramp_initial_weight=0.10` and `ramp_increment=0.20`, completion is
reached after exactly 5 successful advance steps
(`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90 -> 1.00`), each gated by FULL
observation and a preceding hold step. No abort condition is present at any
point before STEP 17 in this scenario, so completion is reached without an
intervening `RULE-23_RETURN_RAMP_ABORT`.

## Post-Completion State

After `RULE-24_RETURN_RAMP_COMPLETE` fires at STEP 17:

- `selected_path_name` is set to the recovered path (`B`) and `mode` returns
  to `NORMAL`.
- `recovery_cooldown_counter` is set to `recovery_cooldown_steps` (`2`),
  producing `RULE-11_RECOVERY_cooldown` at STEP 18 and STEP 19 before normal
  scoring resumes.
- All ramp state (`recovery_state`, `recovery_candidate_name`,
  `recovery_ramp_weight`, `recovery_ramp_hold_counter`) is reset, so the
  decision loop cannot re-enter `RAMPING` without a new recovery candidate
  and a new `RULE-25_RETURN_RAMP_START`.
- STEP 20 and STEP 21 show `RULE-01_KEEP_score` with `mode=NORMAL`, confirming
  the post-completion state is stable rather than triggering further
  switching.

## No Additional Advance

`RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`,
`RULE-23_RETURN_RAMP_ABORT`, and `RULE-24_RETURN_RAMP_COMPLETE` do not appear
anywhere in STEP 18 through STEP 21. `RULE-24_RETURN_RAMP_COMPLETE` and
`RULE-25_RETURN_RAMP_START` each appear exactly once in the full scenario
output, confirming the ramp completes once and does not re-enter or repeat.

## Validator Assertions

`scripts/validate_evidence_rules.py` checks the following for
`ScenarioCheck.name=ramp_complete` (`scenario_steps=22`):

- `RULE-25_RETURN_RAMP_START`, `RULE-21_RETURN_RAMP_ADVANCE`, and
  `RULE-24_RETURN_RAMP_COMPLETE` are all present.
- `RULE-24_RETURN_RAMP_COMPLETE` is present with `recovered_weight=1.00`,
  `evacuation_weight=0.00`, `observation_mode=FULL`, and
  `reason=RAMP_TARGET_REACHED`.
- Post-completion state is present: `RULE-11_RECOVERY_cooldown` with
  `remaining=2` and `remaining=1` and `reason=RECOVERY_COOLDOWN`, followed by
  `mode=NORMAL`.
- `RULE-25_RETURN_RAMP_START` and `RULE-24_RETURN_RAMP_COMPLETE` each occur
  exactly once in the output (`single_occurrence_patterns`), confirming no
  duplicate ramp start or completion.
- `RULE-23_RETURN_RAMP_ABORT` does not appear anywhere in the output.
- `mode=EMERGENCY`, `EMERGENCY_CUT`, and
  `state_transition=RAMPING->ABORTED` do not appear anywhere in the output.

## Final Judgment

Verified.

The runnable scenario, raw log, this verified log, and the validator
assertions confirm that `RULE-24_RETURN_RAMP_COMPLETE` under FULL observation
fires exactly once when the recovered path's weight reaches the completion
threshold (`1.00`), that no abort condition precedes completion in this
scenario, that the post-completion state is stable (cooldown followed by
NORMAL hysteresis hold), and that no additional or duplicate advance /
completion occurs afterward.

This Verified status does not imply that the completion threshold has been
formally integrated into the specification body, and does not cover
completion behavior under LIGHT observation.
