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

| RULE | Problem | Design Intent | Scenario | Evidence Log | Status |
|------|---------|---------------|----------|--------------|--------|
| RULE-01_KEEP_score | Unnecessary switching caused by small score changes | Maintain the stable selected path through hysteresis | stable / degraded / recovery_hold | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-02_SWITCH_score | Required switch is not executed despite a clear score advantage | Switch to the best path when score_gap reaches switch_threshold | switch_score | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md` | Verified |
| RULE-05_ESCALATE_conflict | Ambiguous decisions caused by trust / stability / score conflicts | Request Resolver arbitration | oscillation / resolver_switch | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md` | Verified |
| RULE-07_DEGRADE_trigger | Trust degradation or invalidation of the selected path | Safe transition from NORMAL to DEGRADED | degraded | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-08_DEGRADE_keep | Unnecessary fallback switching during DEGRADED mode | Keep a stable path even in degraded mode | degraded_keep | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md` | Verified |
| RULE-09_DEGRADE_switch | The current path cannot be maintained after trust degradation | Switch to a degraded fallback path | degraded | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-10_RECOVERY_trigger | Recovery decision after a trusted path returns | Return to NORMAL only when stability and trust conditions are satisfied | degraded_recovery / recovery_hold | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md` | Verified |
| RULE-11_RECOVERY_cooldown | Re-degradation or re-switching immediately after recovery | Stabilize post-recovery behavior through recovery cooldown | degraded_recovery / recovery_hold | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-12_COOLDOWN_active | Repeated escalation immediately after Resolver intervention | Suppress oscillation through cooldown | oscillation / resolver_switch | `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md` | Verified |
| RULE-13_RESOLVER_keep | Switching is unnecessary after Resolver intervention | KEEP decision by Resolver arbitration | oscillation / resolver_keep | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_rule_unification_log.md` | Verified |
| RULE-14_RESOLVER_switch | Local RCU cannot safely resolve the conflict | Explicit Resolver-driven path switch | resolver_switch | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md` | Verified |
| RULE-15_RECOVERY_CANDIDATE | Risk of immediately returning to a recovered path | Move the recovered path into staged evaluation as a recovery candidate | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-16_RECOVERY_VALIDATION_START | Insufficient stability validation for a recovered path | Start the validation phase | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-18_RETURN_ELIGIBLE | Ambiguous return eligibility conditions | Confirm eligibility before return switching | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-19_RETURN_SWITCH | Execute v0.2 staged recovery return | Controlled return switch to a validated eligible path | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-20_RETURN_KEEP | Risk of switching to a return candidate before conditions are met | Keep the current path | recovery_return_keep | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md` | Verified |
| RULE-21_RETURN_RAMP_ADVANCE | Ambiguous ramp advancement conditions | Increase recovered-path traffic weight only under stable conditions | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_full_light_observation_validation_log.md` | Experimental |
| RULE-22_RETURN_RAMP_HOLD | Ambiguous temporary hold conditions during ramp | Maintain the current weight when advancement conditions are insufficient | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | Experimental |
| RULE-23_RETURN_RAMP_ABORT | Early return to an unstable path | Abort recovery return when instability is detected during ramp | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | Experimental |
| RULE-24_RETURN_RAMP_COMPLETE | Ambiguous recovery completion condition | Confirm completion of progressive reintegration | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | Experimental |
| RULE-25_RETURN_RAMP_START | Abrupt full traffic return immediately after recovery | Start progressive return ramp | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | Experimental |

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

| Scenario | Purpose | Main Log |
|----------|---------|----------|
| stable | Confirm KEEP behavior and switch suppression during normal operation | `rcu_decision_v01_degraded_rule_validation_log.md` |
| switch_score | Confirm RULE-01 keep below threshold and RULE-02 switch at threshold | `rcu_decision_v01_switch_score_validation_log.md` |
| oscillation | Confirm oscillation suppression compared with ECMP-like score following | `rcu_decision_v01_oscillation_ecmp_comparison_log.md` |
| resolver_switch | Confirm Resolver-driven switching under trust / stability conflict | `rcu_decision_v01_resolver_switch_rule_log.md` |
| degraded | Confirm DEGRADED transition and fallback after trust degradation | `rcu_decision_v01_degraded_rule_validation_log.md` |
| degraded_keep | Confirm DEGRADED fallback keep when current degraded path is maintainable and candidate is not recovery eligible | `rcu_decision_v01_degraded_keep_validation_log.md` |
| degraded_recovery | Confirm safe recovery from DEGRADED to NORMAL | `rcu_decision_v01_degraded_switch_recovery_rule_log.md` |
| recovery_hold | Confirm conservative hold behavior after recovery | `rcu_decision_v01_recovery_hold_behavior_log.md` |
| recovery_return_v02 | Confirm Recovery Candidate -> Validation -> Return Eligible -> Return Switch | `rcu_decision_v02_recovery_return_validation_log.md` |
| recovery_return_keep | Confirm Return Eligible -> Return Keep when improvement is below return_margin | `rcu_decision_v02_return_keep_validation_log.md` |
| recovery_ramp_v03 | Confirm progressive ramp / abort / complete / observation policy behavior | `rcu_decision_v03_recovery_ramp_validation_log.md` |

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

| RULE | Scenario | Evidence Step | Related Trace | Evidence Log |
|------|----------|---------------|---------------|--------------|
| RULE-01_KEEP_score | stable / degraded_recovery / resolver_switch | STEP 1 / STEP 6 / STEP 2 | STEP 1: switch_score keeps A because score_gap is below threshold; STEP 6 and later: after recovery, hysteresis keeps the selected path; STEP 2 and later: after Resolver intervention, cooldown and hysteresis suppress unnecessary switching | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md`; `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md`; `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md` |
| RULE-02_SWITCH_score | switch_score | STEP 2 | STEP 1: `RULE-01_KEEP_score` keeps A because score_gap is below switch_threshold; STEP 2: `RULE-02_SWITCH_score` switches A -> B because score_gap reaches switch_threshold | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md` |
| RULE-05_ESCALATE_conflict | resolver_switch / oscillation | STEP 1 / STEP 4 | STEP 1: trust conflict escalates the decision to the Resolver; STEP 4: the oscillation comparison scenario escalates again because trust conflict remains under near-equal scores | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md`; `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md` |
| RULE-07_DEGRADE_trigger | degraded / degraded_keep | STEP 3 / STEP 1 | STEP 3: selected path is rejected / invalid and the system transitions from NORMAL to DEGRADED; STEP 1: selected path A becomes unsafe and DEGRADED mode starts | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md`; `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md` |
| RULE-08_DEGRADE_keep | degraded_keep | STEP 2 | STEP 1: `RULE-09_DEGRADE_switch` selects fallback B after A becomes unsafe; STEP 2: `RULE-08_DEGRADE_keep` keeps B because current degraded path is health-valid and A is not recovery eligible | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md` |
| RULE-09_DEGRADE_switch | degraded / degraded_keep | STEP 3 / STEP 1 | STEP 3: selected path becomes invalid and PSC switches to fallback A; STEP 1: selected path A becomes unsafe and PSC switches to fallback B | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md`; `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md` |
| RULE-10_RECOVERY_trigger | degraded_recovery / recovery_hold | STEP 3 / STEP 4 | STEP 3: trusted path B satisfies stability conditions and returns the system from DEGRADED to NORMAL; STEP 4: stable trusted path A is confirmed and recovery to NORMAL starts | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md`; `sim/02_controlled/05_recovery_hold/logs/rcu_decision_v01_recovery_hold_behavior_log.md` |
| RULE-11_RECOVERY_cooldown | degraded_recovery / recovery_hold | STEP 4-5 / STEP 5-6 | STEP 4-5: recovery cooldown applies with remaining=2 -> 1 after recovery; STEP 5-6: recovery_hold also suppresses immediate re-evaluation after recovery | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md`; `sim/02_controlled/05_recovery_hold/logs/rcu_decision_v01_recovery_hold_behavior_log.md` |
| RULE-12_COOLDOWN_active | resolver_switch / oscillation | STEP 2-3 / STEP 2-3 | STEP 2-3: Resolver switch is followed by cooldown remaining=2 -> 1; in the oscillation comparison, cooldown suppresses repeated escalation after Resolver intervention | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md`; `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md` |
| RULE-13_RESOLVER_keep | resolver_keep / oscillation | STEP 1 / STEP 4 | STEP 1: stability conflict escalates to the Resolver, but the Resolver keeps selected A; STEP 4: the oscillation comparison shows the Resolver keeping the same selection to avoid unnecessary switching | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_rule_unification_log.md`; `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md` |
| RULE-14_RESOLVER_switch | resolver_switch / oscillation | STEP 1 | STEP 1: trust conflict escalates to the Resolver, and the Resolver explicitly switches A -> B; the oscillation comparison confirms a Resolver-driven B -> A switch | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md`; `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md` |
| RULE-15_RECOVERY_CANDIDATE | recovery_return_v02 | STEP 6 | STEP 6: recovered path B is registered as a recovery candidate instead of being returned immediately | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` |
| RULE-16_RECOVERY_VALIDATION_START | recovery_return_v02 | STEP 7 | STEP 7: validation phase starts for candidate B with required=2 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` |
| RULE-18_RETURN_ELIGIBLE | recovery_return_v02 / recovery_return_keep | STEP 7 / STEP 4 | STEP 7: B is marked return eligible after validation passes; in return_keep, PSC evaluates the margin condition separately after eligibility | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md`; `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md` |
| RULE-19_RETURN_SWITCH | recovery_return_v02 | STEP 7 | STEP 7: B is eligible and improvement=0.152, so PSC performs a controlled return switch A -> B | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` |
| RULE-20_RETURN_KEEP | recovery_return_keep | STEP 4 | STEP 4: `RULE-18_RETURN_ELIGIBLE` marks B eligible; STEP 4: `RULE-20_RETURN_KEEP` keeps A because improvement is below return_margin | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md` |

---

## 7. v0.3 Experimental RULE Integration Candidates

| RULE | Classification | Rationale | Next Work |
|------|----------------|-----------|-----------|
| RULE-25_RETURN_RAMP_START | Formal integration candidate | Entry point that extends v0.2 `RULE-19_RETURN_SWITCH` into staged traffic return; it fires at STEP 7 after candidate, validation, and eligibility conditions | Specify the difference from v0.2 staged return and preserve the generation boundary between RULE-19 and RULE-25 |
| RULE-21_RETURN_RAMP_ADVANCE (FULL observation) | Formal integration candidate | Core progressive reintegration behavior; under FULL observation, the control intent is clear: increase recovered-path traffic weight only under stable conditions | Specify advance conditions, weight increments, and stability evaluation under FULL observation |
| RULE-22_RETURN_RAMP_HOLD | Formal integration candidate | Required safety-side control during ramp observation; it avoids immediate advancement when more observation is needed | Define hold duration, observation conditions, and transitions to advance / abort |
| RULE-23_RETURN_RAMP_ABORT | Formal integration candidate | Required safety boundary for v0.3 stability guarantees; it aborts return when the recovered path becomes unstable | Define abort thresholds and cooldown / retry behavior after fallback |
| RULE-24_RETURN_RAMP_COMPLETE | Formal integration candidate | Terminal RULE required to confirm completion of progressive reintegration | Specify selected path state, weight=1.00, and post-completion monitoring conditions |
| RULE-21_RETURN_RAMP_ADVANCE (LIGHT observation) | Hold | LIGHT mode advances with less observation than FULL mode, so the safety boundary and false-negative tolerance are not sufficiently specified yet | Decide integration after connecting it to Fast Mode / observation policy specifications |

Notes:

- v0.3 RULEs remain Experimental for now.
- Formal integration candidate means the behavior is worth integrating into the specification; it does not mean promotion to Verified.
- Promotion to Verified requires transition conditions, thresholds, and FULL / LIGHT observation handling to be integrated into the specification text.
