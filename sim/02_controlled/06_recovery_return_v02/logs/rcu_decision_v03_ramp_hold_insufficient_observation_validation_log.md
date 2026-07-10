# PSC RCU Decision Model v0.3 Ramp Hold Insufficient Observation Validation Log

## Validation Target

- Rule: `RULE-22_RETURN_RAMP_HOLD`
- Scenario: `ramp_hold_insufficient_observation`
- Scenario file: `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py`
- Raw log: `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_hold_insufficient_observation_run.txt`
- Observation mode: `FULL`
- Validator: `scripts/validate_evidence_rules.py`
- Validator check: `ScenarioCheck.name=ramp_hold_insufficient_observation`

`RULE-22_RETURN_RAMP_HOLD` is the safe-side control used during Recovery Ramp
to keep the current ramp level when observation evidence is insufficient for
further recovery advancement.

## Evidence Steps

| Step | Evidence | Observed value |
|------|----------|----------------|
| STEP 9 | Previous ramp advancement | `RULE-21_RETURN_RAMP_ADVANCE` |
| STEP 9 | Observation mode | `observation_mode=FULL` |
| STEP 9 | Observation category | `observation_category=SUFFICIENT_OBSERVATION` |
| STEP 9 | Ramp level change | `ramp_level_before=0.10`, `ramp_level_after=0.30` |
| STEP 10 | Hold rule | `RULE-22_RETURN_RAMP_HOLD` |
| STEP 10 | Category | `category=hold` |
| STEP 10 | Reason | `reason=INSUFFICIENT_OBSERVATION` |
| STEP 10 | Recovery state | `recovery_state=RAMPING` |
| STEP 10 | State transition | `state_transition=RAMPING->RAMPING` |
| STEP 10 | Observation mode | `observation_mode=FULL` |
| STEP 10 | Observation category | `observation_category=INSUFFICIENT_OBSERVATION` |
| STEP 10 | Observation amount | `observation_samples=0`, `required_observation_samples=1` |
| STEP 10 | Observation window | `observation_window_steps=0`, `required_observation_window_steps=1` |
| STEP 10 | Ramp level hold | `ramp_level_before=0.30`, `ramp_level_after=0.30` |

## Expected Result

After a prior successful ramp advance, a later FULL-observation decision with
`INSUFFICIENT_OBSERVATION` must hold the current ramp level.

The same decision step must not advance, abort, complete, or enter emergency
handling.

## Observed Result

- STEP 9 advanced the ramp from `0.10` to `0.30`.
- STEP 10 emitted `RULE-22_RETURN_RAMP_HOLD`.
- STEP 10 recorded `reason=INSUFFICIENT_OBSERVATION`.
- STEP 10 kept `recovered_weight_before=0.30` and `recovered_weight_after=0.30`.
- STEP 10 kept `state_transition=RAMPING->RAMPING`.

## Validator Assertions

The validator checks the following items for this scenario:

- `RULE-22_RETURN_RAMP_HOLD` is emitted.
- `reason=INSUFFICIENT_OBSERVATION` is present in the target HOLD step.
- `category=hold` is present.
- `observation_mode=FULL` is present in the target HOLD step.
- `state_transition=RAMPING->RAMPING` is present.
- `recovered_weight_before=0.30` and `recovered_weight_after=0.30` are equal.
- `ramp_level_before=0.30` and `ramp_level_after=0.30` are equal.
- The previous step contains `RULE-21_RETURN_RAMP_ADVANCE`.
- The previous step advances from `ramp_level_before=0.10` to `ramp_level_after=0.30`.
- The target HOLD step does not contain `RULE-21_RETURN_RAMP_ADVANCE`.
- The target HOLD step does not contain `RULE-23_RETURN_RAMP_ABORT`.
- The target HOLD step does not contain `RULE-24_RETURN_RAMP_COMPLETE`.
- The target HOLD step does not contain emergency transition markers.

## Forbidden Transition Check

The target HOLD step was checked against the following forbidden outcomes:

- `RULE-21_RETURN_RAMP_ADVANCE`
- `RULE-23_RETURN_RAMP_ABORT`
- `RULE-24_RETURN_RAMP_COMPLETE`
- `state_transition=RAMPING->ABORTED`
- `state_transition=RAMPING->COMPLETE`
- `state_transition=RAMPING->EMERGENCY`
- `mode=EMERGENCY`
- `EMERGENCY_CUT`

None of these forbidden outcomes appeared in the target HOLD step.

## Final Judgment

Verified.

The runnable scenario, raw log, verified log, and validator assertions confirm
that `RULE-22_RETURN_RAMP_HOLD` holds the Recovery Ramp at the current level
when FULL observation evidence is insufficient.
