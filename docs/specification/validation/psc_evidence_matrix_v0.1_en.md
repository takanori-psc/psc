# PSC Evidence Matrix v0.1

## 1. Overview

This matrix is a validation traceability table for PSC design philosophy,
control RULEs, validation scenarios, and observation logs.

The RULE names in this file are primarily based on the `RULE-xx_NAME`
identifiers emitted by simulation traces under `sim/02_controlled`.
Because these identifiers may differ from the general rule numbering used
in published specification documents, this file prioritizes evidence that
can be directly confirmed in execution logs.

---

## 2. Validation Mapping

| RULE | Problem | Design Intent | Scenario | Log Ref | Status |
|------|---------|---------------|----------|--------------|--------|
| RULE-01_KEEP_score | Unnecessary switching caused by small score changes | Maintain the stable selected path through hysteresis | stable / degraded / recovery_hold | `LOG-DEG-01` | Verified |
| RULE-02_SWITCH_score | Required switch is not executed despite a clear score advantage | Switch to the best path when score_gap reaches switch_threshold | switch_score | `LOG-SW-01` | Verified |
| RULE-05_ESCALATE_conflict | Ambiguous decisions caused by trust / stability / score conflicts | Request Resolver arbitration | oscillation / resolver_switch | `LOG-RES-01` | Verified |
| RULE-07_DEGRADE_trigger | Trust degradation or invalidation of the selected path | Safe transition from NORMAL to DEGRADED | degraded | `LOG-DEG-01` | Verified |
| RULE-08_DEGRADE_keep | Unnecessary fallback switching during DEGRADED mode | Keep a stable path even in degraded mode | degraded_keep | `LOG-DEG-02` | Verified |
| RULE-09_DEGRADE_switch | The current path cannot be maintained after trust degradation | Switch to a degraded fallback path | degraded | `LOG-DEG-01` | Verified |
| RULE-10_RECOVERY_trigger | Recovery decision after a trusted path returns | Return to NORMAL only when stability and trust conditions are satisfied | degraded_recovery / recovery_hold | `LOG-REC-01` | Verified |
| RULE-11_RECOVERY_cooldown | Re-degradation or re-switching immediately after recovery | Stabilize post-recovery behavior through recovery cooldown | degraded_recovery / recovery_hold | `LOG-DEG-01` | Verified |
| RULE-12_COOLDOWN_active | Repeated escalation immediately after Resolver intervention | Suppress oscillation through cooldown | oscillation / resolver_switch | `LOG-OSC-01` | Verified |
| RULE-13_RESOLVER_keep | Switching is unnecessary after Resolver intervention | KEEP decision by Resolver arbitration | oscillation / resolver_keep | `LOG-RES-02` | Verified |
| RULE-14_RESOLVER_switch | Local RCU cannot safely resolve the conflict | Explicit Resolver-driven path switch | resolver_switch | `LOG-RES-01` | Verified |
| RULE-15_RECOVERY_CANDIDATE | Risk of immediately returning to a recovered path | Move the recovered path into staged evaluation as a recovery candidate | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-16_RECOVERY_VALIDATION_START | Insufficient stability validation for a recovered path | Start the validation phase | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-18_RETURN_ELIGIBLE | Ambiguous return eligibility conditions | Confirm eligibility before return switching | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-19_RETURN_SWITCH | Execute v0.2 staged recovery return | Controlled return switch to a validated eligible path | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-20_RETURN_KEEP | Risk of switching to a return candidate before conditions are met | Keep the current path | recovery_return_keep | `LOG-RR-02` | Verified |
| RULE-21_RETURN_RAMP_ADVANCE | Ambiguous ramp advancement conditions | Increase recovered-path traffic weight only under stable conditions | recovery_ramp_v03 | `LOG-RAMP-01` | Experimental |
| RULE-22_RETURN_RAMP_HOLD | Ambiguous temporary hold conditions during ramp | Maintain the current weight when advancement conditions are insufficient | recovery_ramp_v03 | `LOG-RAMP-02` | Experimental |
| RULE-23_RETURN_RAMP_ABORT | Early return to an unstable path | Abort recovery return when instability is detected during ramp | recovery_ramp_v03 | `LOG-RAMP-03` | Experimental |
| RULE-24_RETURN_RAMP_COMPLETE | Ambiguous recovery completion condition | Confirm completion of progressive reintegration | recovery_ramp_v03 | `LOG-RAMP-03` | Experimental |
| RULE-25_RETURN_RAMP_START | Abrupt full traffic return immediately after recovery | Start progressive return ramp | recovery_ramp_v03 | `LOG-RAMP-02` | Experimental |

---

## 3. Status Definitions

| Status | Meaning |
|--------|---------|
| Verified | Behavior has been confirmed by scenario execution and logs |
| Experimental | Extension-stage behavior that remains under validation before specification integration |
| Implemented | Exists as an implementation-level RULE, but dedicated evidence logs are not yet fully organized |
| Planned | Planned for future validation |

---

## 4. Scenario Definitions

| Scenario | Purpose | Log Ref |
|----------|---------|----------|
| stable | Confirm KEEP behavior and switch suppression during normal operation | `LOG-DEG-01` |
| switch_score | Confirm RULE-01 keep below threshold and RULE-02 switch at threshold | `LOG-SW-01` |
| oscillation | Confirm oscillation suppression compared with ECMP-like score following | `LOG-OSC-01` |
| resolver_switch | Confirm Resolver-driven switching under trust / stability conflict | `LOG-RES-01` |
| degraded | Confirm DEGRADED transition and fallback after trust degradation | `LOG-DEG-01` |
| degraded_keep | Confirm DEGRADED fallback keep when current degraded path is maintainable and candidate is not recovery eligible | `LOG-DEG-02` |
| degraded_recovery | Confirm safe recovery from DEGRADED to NORMAL | `LOG-REC-01` |
| recovery_hold | Confirm conservative hold behavior after recovery | `LOG-HOLD-01` |
| recovery_return_v02 | Confirm Recovery Candidate -> Validation -> Return Eligible -> Return Switch | `LOG-RR-01` |
| recovery_return_keep | Confirm Return Eligible -> Return Keep when improvement is below return_margin | `LOG-RR-02` |
| recovery_ramp_v03 | Confirm progressive ramp / abort / complete / observation policy behavior | `LOG-RAMP-03` |

---

## 5. RULE Definitions

| RULE | Summary |
|------|---------|
| RULE-01_KEEP_score | Keep the current path when the score gap or improvement is small |
| RULE-02_SWITCH_score | Switch to the best path when score_gap reaches switch_threshold |
| RULE-05_ESCALATE_conflict | Delegate the decision to the Resolver when trust / stability / score conflicts occur |
| RULE-07_DEGRADE_trigger | Transition to DEGRADED when the currently selected path is rejected or invalid |
| RULE-08_DEGRADE_keep | In DEGRADED mode, keep the current fallback path if it remains maintainable |
| RULE-09_DEGRADE_switch | In DEGRADED mode, switch from an unmaintainable path to a fallback path |
| RULE-10_RECOVERY_trigger | Start recovery to NORMAL when a stable and trusted path is confirmed |
| RULE-11_RECOVERY_cooldown | Apply cooldown immediately after recovery to suppress re-switching |
| RULE-12_COOLDOWN_active | Suppress repeated escalation or switching during Resolver cooldown |
| RULE-13_RESOLVER_keep | Keep the current path when the Resolver determines that switching is unnecessary |
| RULE-14_RESOLVER_switch | Switch explicitly to a safer path based on Resolver arbitration |
| RULE-15_RECOVERY_CANDIDATE | Register the recovered path as a candidate and validate it before return |
| RULE-16_RECOVERY_VALIDATION_START | Start the validation phase for a recovery candidate |
| RULE-18_RETURN_ELIGIBLE | Mark a recovered path as return eligible after validation conditions are met |
| RULE-19_RETURN_SWITCH | Perform a v0.2 staged recovery switch to an eligible path |
| RULE-20_RETURN_KEEP | Keep the current path when return conditions are not satisfied |
| RULE-21_RETURN_RAMP_ADVANCE | Gradually increase the recovered path traffic weight when ramp conditions are satisfied |
| RULE-22_RETURN_RAMP_HOLD | Hold the current traffic weight when ramp advancement conditions are insufficient |
| RULE-23_RETURN_RAMP_ABORT | Abort recovery return when instability is detected in the recovered path during ramp |
| RULE-24_RETURN_RAMP_COMPLETE | Confirm completion of progressive reintegration to the recovered path |
| RULE-25_RETURN_RAMP_START | Start the v0.3 progressive recovery ramp |

---

## 6. STEP Traceability

| RULE | Scenario | Evidence Step | Trace Summary | Log Ref |
|------|----------|---------------|---------------|--------------|
| RULE-01_KEEP_score | stable / degraded_recovery / resolver_switch | STEP 1 / STEP 6 / STEP 2 | Hysteresis suppresses minor-improvement and cooldown-period switching | `LOG-SW-01`; `LOG-REC-01`; `LOG-RES-01` |
| RULE-02_SWITCH_score | switch_score | STEP 2 | Switches A -> B after score_gap reaches threshold | `LOG-SW-01` |
| RULE-05_ESCALATE_conflict | resolver_switch / oscillation | STEP 1 / STEP 4 | Escalates trust conflict / oscillation conditions to Resolver | `LOG-RES-01`; `LOG-OSC-01` |
| RULE-07_DEGRADE_trigger | degraded / degraded_keep | STEP 3 / STEP 1 | Rejected / unsafe selected path enters DEGRADED | `LOG-DEG-01`; `LOG-DEG-02` |
| RULE-08_DEGRADE_keep | degraded_keep | STEP 2 | Keeps health-valid degraded fallback | `LOG-DEG-02` |
| RULE-09_DEGRADE_switch | degraded / degraded_keep | STEP 3 / STEP 1 | Switches from unsafe / invalid path to fallback path | `LOG-DEG-01`; `LOG-DEG-02` |
| RULE-10_RECOVERY_trigger | degraded_recovery / recovery_hold | STEP 3 / STEP 4 | Returns to NORMAL after stable trusted path confirmation | `LOG-REC-01`; `LOG-HOLD-01` |
| RULE-11_RECOVERY_cooldown | degraded_recovery / recovery_hold | STEP 4-5 / STEP 5-6 | Suppresses immediate re-evaluation after recovery | `LOG-REC-01`; `LOG-HOLD-01` |
| RULE-12_COOLDOWN_active | resolver_switch / oscillation | STEP 2-3 / STEP 2-3 | Suppresses repeated escalation / switching after Resolver intervention | `LOG-RES-01`; `LOG-OSC-01` |
| RULE-13_RESOLVER_keep | resolver_keep / oscillation | STEP 1 / STEP 4 | Resolver keeps the same selection to avoid unnecessary switching | `LOG-RES-02`; `LOG-OSC-01` |
| RULE-14_RESOLVER_switch | resolver_switch / oscillation | STEP 1 | Resolver resolves conflict with explicit A/B switch | `LOG-RES-01`; `LOG-OSC-01` |
| RULE-15_RECOVERY_CANDIDATE | recovery_return_v02 | STEP 6 | Registers recovered path as a candidate before return | `LOG-RR-01` |
| RULE-16_RECOVERY_VALIDATION_START | recovery_return_v02 | STEP 7 | Starts validation phase for recovery candidate | `LOG-RR-01` |
| RULE-18_RETURN_ELIGIBLE | recovery_return_v02 / recovery_return_keep | STEP 7 / STEP 4 | Confirms return eligibility after validation passes | `LOG-RR-01`; `LOG-RR-02` |
| RULE-19_RETURN_SWITCH | recovery_return_v02 | STEP 7 | Performs controlled return switch to eligible path | `LOG-RR-01` |
| RULE-20_RETURN_KEEP | recovery_return_keep | STEP 4 | Keeps current path because return_margin is not met | `LOG-RR-02` |

---

## 7. v0.3 Experimental RULE Integration Candidates

| RULE | Classification | Summary | Next |
|------|----------------|-----------|-----------|
| RULE-25_RETURN_RAMP_START | Formal integration candidate | v0.3 ramp entry point | Specify delta from RULE-19 |
| RULE-21_RETURN_RAMP_ADVANCE (FULL) | Formal integration candidate | Increase weight only when stable | Define advance conditions |
| RULE-22_RETURN_RAMP_HOLD | Formal integration candidate | Hold weight during observation | Define hold / advance / abort transitions |
| RULE-23_RETURN_RAMP_ABORT | Formal integration candidate | Abort return on instability | Define abort threshold |
| RULE-24_RETURN_RAMP_COMPLETE | Formal integration candidate | Confirm reintegration completion | Define completion conditions |
| RULE-21_RETURN_RAMP_ADVANCE (LIGHT) | Hold | Safety boundary is underspecified | Connect to Fast Mode spec |

Notes:

- v0.3 RULEs remain Experimental for now.
- Formal integration candidate means the behavior is worth integrating into the specification; it does not mean promotion to Verified.
- Promotion to Verified requires transition conditions, thresholds, and FULL / LIGHT observation handling to be integrated into the specification text.

---

## 8. Log References

- `LOG-DEG-01`: `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md`
- `LOG-DEG-02`: `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md`
- `LOG-HOLD-01`: `sim/02_controlled/05_recovery_hold/logs/rcu_decision_v01_recovery_hold_behavior_log.md`
- `LOG-OSC-01`: `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md`
- `LOG-REC-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md`
- `LOG-RES-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md`
- `LOG-RES-02`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_rule_unification_log.md`
- `LOG-RR-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md`
- `LOG-RR-02`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md`
- `LOG-RAMP-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_full_light_observation_validation_log.md`
- `LOG-RAMP-02`: `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt`
- `LOG-RAMP-03`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md`
- `LOG-SW-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md`
