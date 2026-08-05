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
| RULE-04_BLOCK_trust | Unsafe switching to a trust-blocked path | Block unsafe switch candidates even when score or trust-switch rules prefer them | trust_block_vs_switch | `LOG-TRUST-BLOCK-01` | Verified |
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
| RULE-21_RETURN_RAMP_ADVANCE | Ambiguous ramp advancement conditions | Increase recovered-path traffic weight only under stable conditions (FULL observation evidence) | ramp_complete / ramp_abort_full_stability_dip | `LOG-RAMP-FULL-ADV-01`; `RAW-RAMP-FULL-ADV-01`; `RAW-RAMP-ABORT-FULLDIP-01` | Verified |
| RULE-21_RETURN_RAMP_ADVANCE (LIGHT) | Risk of misjudged advance when observation is abbreviated | LIGHT-observation-based advance remains Hold | recovery_ramp_v03 | `LOG-RAMP-01` | Hold |
| RULE-22_RETURN_RAMP_HOLD | Ambiguous temporary hold conditions during ramp | Maintain the current weight when advancement conditions are insufficient | ramp_hold_insufficient_observation | `LOG-RAMP-HOLD-INSUFF-01`; `RAW-RAMP-HOLD-INSUFF-01` | Verified |
| RULE-23_RETURN_RAMP_ABORT | Early return to an unstable path | Abort recovery return when instability is detected during ramp (FULL abort class evidence) | soft_abort_hold_and_reobserve / hard_abort_ramp_down / emergency_cut_no_fallback / two_path_degraded_abort | `LOG-ABORT-01`; `RAW-ABORT-SOFT-01`; `RAW-ABORT-HARD-01`; `RAW-ABORT-EMERG-01`; `RAW-ABORT-2PATH-01` | Verified |
| RULE-23_RETURN_RAMP_ABORT | Instability detected in the recovered path inside the ramp engine | Abort trace emitted when the recovered path is judged invalid / unstable during ramp | recovery_ramp_v03 | `LOG-RAMP-03` | Experimental |
| RULE-24_RETURN_RAMP_COMPLETE | Ambiguous recovery completion condition | Confirm completion of progressive reintegration (FULL observation evidence) | ramp_complete | `LOG-RAMP-COMPLETE-01`; `RAW-RAMP-FULL-ADV-01` | Verified |
| RULE-25_RETURN_RAMP_START | Abrupt full traffic return immediately after recovery | Start progressive return ramp | recovery_ramp_v03 | `LOG-RAMP-02` | Experimental |

---

### 2.1 RULE-22 Verified Scope Note

`RULE-22_RETURN_RAMP_HOLD` is Verified for the covered FULL-observation hold
evidence with `reason=INSUFFICIENT_OBSERVATION`.

LIGHT Observation scenarios are excluded from this Verified scope.

This status does not imply verification of every RULE-22 reason, observation
mode, or the complete v0.3 Recovery Ramp behavior.

---

### 2.2 RULE-23 Verified Scope Note

`RULE-23_RETURN_RAMP_ABORT` is Verified for the four FULL-observation abort
classes (`SOFT_ABORT` / `HARD_ABORT` / `EMERGENCY_CUT` / `DEGRADED_ABORT`)
reproduced by `soft_abort_hold_and_reobserve`, `hard_abort_ramp_down`,
`emergency_cut_no_fallback`, and `two_path_degraded_abort`.

The abort traces emitted inside the v0.3 recovery ramp engine
(`reason=RECOVERED_PATH_UNSTABLE` and `reason=RECOVERED_PATH_INVALID` in the
`recovery_ramp_v03` scenario), and the `light_delayed_abort_stub.py` LIGHT
delayed abort design stub, are excluded from this Verified scope.

This status does not imply that abort threshold formal integration into the
specification body is complete.

---

### 2.3 RULE-21 Verified Scope Note

`RULE-21_RETURN_RAMP_ADVANCE` is Verified for FULL observation.

The `ramp_complete` scenario is positive evidence confirming four advance
transitions (`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90`) followed by
`RULE-24_RETURN_RAMP_COMPLETE`. The `ramp_abort_full_stability_dip` scenario
is negative evidence confirming that `RULE-21_RETURN_RAMP_ADVANCE` never
fires when instability is detected immediately before a due advance step.

LIGHT observation based advance remains Hold. LIGHT-based advance must not be
treated as Verified evidence until false-positive / false-negative behavior
is sufficiently bounded.

This status does not imply that formal integration of the ramp increment or
advance threshold into the specification body is complete.

---

### 2.4 RULE-24 Verified Scope Note

`RULE-24_RETURN_RAMP_COMPLETE` is Verified for FULL observation.

The `ramp_complete` scenario (22 steps) confirms the advance sequence through
completion (`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90 -> 1.00`), plus the
post-completion state: `RULE-11_RECOVERY_cooldown` (STEP 18-19) followed by
`RULE-01_KEEP_score` with `mode=NORMAL` (STEP 20-21).
`RULE-24_RETURN_RAMP_COMPLETE` and `RULE-25_RETURN_RAMP_START` each appear
exactly once in the output, confirming no additional advance or repeated
ramp start occurs after completion.

This status does not imply that formal integration of the completion
threshold into the specification body is complete, and does not cover
completion behavior under LIGHT observation.

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
| trust_block_vs_switch | Confirm RULE-04 trust block takes priority over RULE-02 score switch and RULE-03 trust switch, producing BLOCK_SWITCH | `LOG-TRUST-BLOCK-01` |
| oscillation | Confirm oscillation suppression compared with ECMP-like score following | `LOG-OSC-01` |
| resolver_switch | Confirm Resolver-driven switching under trust / stability conflict | `LOG-RES-01` |
| degraded | Confirm DEGRADED transition and fallback after trust degradation | `LOG-DEG-01` |
| degraded_keep | Confirm DEGRADED fallback keep when current degraded path is maintainable and candidate is not recovery eligible | `LOG-DEG-02` |
| degraded_recovery | Confirm safe recovery from DEGRADED to NORMAL | `LOG-REC-01` |
| recovery_hold | Confirm conservative hold behavior after recovery | `LOG-HOLD-01` |
| recovery_return_v02 | Confirm Recovery Candidate -> Validation -> Return Eligible -> Return Switch | `LOG-RR-01` |
| recovery_return_keep | Confirm Return Eligible -> Return Keep when improvement is below return_margin | `LOG-RR-02` |
| recovery_ramp_v03 | Confirm progressive ramp / abort / complete / observation policy behavior | `LOG-RAMP-03` |
| ramp_hold_insufficient_observation | Confirm that mid-ramp `INSUFFICIENT_OBSERVATION` in `FULL` observation keeps recovered weight unchanged and suppresses same-step ramp advance / abort / complete / emergency transition | `LOG-RAMP-HOLD-INSUFF-01`; `RAW-RAMP-HOLD-INSUFF-01` |
| light_false_negative | Confirm LIGHT observation holds the ramp when actual instability is not detected | `LOG-LIGHT-HOLD-01`; `RAW-LIGHT-FN-01` |
| light_stale_telemetry | Confirm LIGHT observation holds the ramp when telemetry is outdated | `LOG-LIGHT-HOLD-01`; `RAW-LIGHT-ST-01` |
| light_masked_instability | Confirm LIGHT observation holds the ramp when sparse evidence masks instability | `LOG-LIGHT-HOLD-01`; `RAW-LIGHT-MI-01` |
| soft_abort_hold_and_reobserve | Confirm SOFT_ABORT holds allocation, increases observation, and triggers Resolver re-evaluation | `LOG-ABORT-01`; `RAW-ABORT-SOFT-01` |
| hard_abort_ramp_down | Confirm HARD_ABORT ramps down the suspect recovered path and notifies source-side PSC | `LOG-ABORT-01`; `RAW-ABORT-HARD-01` |
| emergency_cut_no_fallback | Confirm EMERGENCY_CUT excludes the unsafe path and blocks fallback transfer when capacity margin is insufficient | `LOG-ABORT-01`; `RAW-ABORT-EMERG-01` |
| two_path_degraded_abort | Confirm two-path degraded abort triggers Resolver least-bad arbitration when no safe alternate exists | `LOG-ABORT-01`; `RAW-ABORT-2PATH-01` |

---

## 5. RULE Definitions

| RULE | Summary |
|------|---------|
| RULE-01_KEEP_score | Keep the current path when the score gap or improvement is small |
| RULE-02_SWITCH_score | Switch to the best path when score_gap reaches switch_threshold |
| RULE-04_BLOCK_trust | Block switching when either explicit trust_block or below-threshold trust is detected. These are separate causes, but both produce the same safety outcome: block the switch before score- or trust-driven switch candidates can win |
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
| RULE-04_BLOCK_trust | trust_block_vs_switch | STEP 0 | Blocks B as trust-blocked and wins over `RULE-02_SWITCH_score` and `RULE-03_SWITCH_trust`, producing final action `BLOCK_SWITCH` | `LOG-TRUST-BLOCK-01` |
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
| RULE-21_RETURN_RAMP_ADVANCE | ramp_complete / ramp_abort_full_stability_dip | STEP 9 / STEP 11 / STEP 13 / STEP 15 / (none) | In `ramp_complete`, four advance transitions (`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90`) are emitted with `category=switch`, `observation_mode=FULL`, `observation_category=SUFFICIENT_OBSERVATION`, and `reason=RECOVERED_PATH_STABLE`, followed by `RULE-24_RETURN_RAMP_COMPLETE`. In `ramp_abort_full_stability_dip`, instability is detected immediately before a due advance step and `RULE-21_RETURN_RAMP_ADVANCE` never fires | `LOG-RAMP-FULL-ADV-01`; `RAW-RAMP-FULL-ADV-01`; `RAW-RAMP-ABORT-FULLDIP-01`; validator `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_complete`, `ScenarioCheck.name=ramp_abort_full_stability_dip`) |
| RULE-22_RETURN_RAMP_HOLD | light_false_negative / light_stale_telemetry / light_masked_instability | STEP 0 / STEP 0 / STEP 0 | Holds LIGHT recovery ramp when evidence is false-negative, stale, or masks instability; evidence available, outside the current Verified scope | `RAW-LIGHT-FN-01`; `RAW-LIGHT-ST-01`; `RAW-LIGHT-MI-01`; `LOG-LIGHT-HOLD-01` |
| RULE-22_RETURN_RAMP_HOLD | ramp_hold_insufficient_observation | STEP 9 -> STEP 10 | After STEP 9 emits `RULE-21_RETURN_RAMP_ADVANCE` and raises the ramp from `0.10` to `0.30`, STEP 10 emits `RULE-22_RETURN_RAMP_HOLD` with `category=hold`, `reason=INSUFFICIENT_OBSERVATION`, `observation_mode=FULL`, and `state_transition=RAMPING->RAMPING`; it keeps `recovered_weight_before=0.30` and `recovered_weight_after=0.30`, and does not emit advance / abort / complete / emergency transition markers in the same HOLD step | `LOG-RAMP-HOLD-INSUFF-01`; `RAW-RAMP-HOLD-INSUFF-01`; validator `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_hold_insufficient_observation`) |
| RULE-23_RETURN_RAMP_ABORT | soft_abort_hold_and_reobserve / hard_abort_ramp_down / emergency_cut_no_fallback / two_path_degraded_abort | STEP 0 / STEP 0 / STEP 0 / STEP 0 | Aborts the active Return Ramp attempt and applies stabilization, ramp-down, emergency cut, or two-path degraded arbitration according to abort class. The validator asserts abort_class, reason, post-abort state, and cross-class exclusion | `RAW-ABORT-SOFT-01`; `RAW-ABORT-HARD-01`; `RAW-ABORT-EMERG-01`; `RAW-ABORT-2PATH-01`; `LOG-ABORT-01`; validator `scripts/validate_evidence_rules.py` (`ScenarioCheck.name` in `soft_abort_hold_and_reobserve`, `hard_abort_ramp_down`, `emergency_cut_no_fallback`, `two_path_degraded_abort`) |
| RULE-24_RETURN_RAMP_COMPLETE | ramp_complete | STEP 17 | `recovered_weight` reaches `ramp_max_weight` (`1.00`) and `RULE-24_RETURN_RAMP_COMPLETE` is emitted with `observation_mode=FULL` and `reason=RAMP_TARGET_REACHED`. STEP 18-19 emit `RULE-11_RECOVERY_cooldown`, and STEP 20-21 emit `RULE-01_KEEP_score` with `mode=NORMAL`, showing the post-completion state is stable. `RULE-24_RETURN_RAMP_COMPLETE` and `RULE-25_RETURN_RAMP_START` each occur exactly once in the output, with no additional advance / completion afterward | `LOG-RAMP-COMPLETE-01`; `RAW-RAMP-FULL-ADV-01`; validator `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_complete`) |

---

### 6.1 Trust Switch Coverage Note

`RULE-03_SWITCH_trust` is active in the collision matrix, but is not promoted
to Verified in this Evidence Matrix version. It appears in
`trust_block_vs_switch` as a suppressed switch candidate, but no dedicated
validation scenario currently shows `RULE-03_SWITCH_trust` as the final switch
action.

---

## 7. LIGHT Observation Evidence Details

| Scenario | Scenario File | RULE | Expected Category | Reason | Raw Log | Verified Log | Coverage Status | Verified Scope |
|----------|---------------|------|-------------------|--------|---------|--------------|-----------------|----------------|
| light_false_negative | `sim/02_controlled/07_light_observation_stub/light_false_negative.py` | RULE-22_RETURN_RAMP_HOLD | hold | OBSERVATION_FALSE_NEGATIVE | `RAW-LIGHT-FN-01` | `LOG-LIGHT-HOLD-01` | Evidence available, outside the current Verified scope | Excluded |
| light_stale_telemetry | `sim/02_controlled/07_light_observation_stub/light_stale_telemetry.py` | RULE-22_RETURN_RAMP_HOLD | hold | STALE_TELEMETRY | `RAW-LIGHT-ST-01` | `LOG-LIGHT-HOLD-01` | Evidence available, outside the current Verified scope | Excluded |
| light_masked_instability | `sim/02_controlled/07_light_observation_stub/light_masked_instability.py` | RULE-22_RETURN_RAMP_HOLD | hold | MASKED_INSTABILITY | `RAW-LIGHT-MI-01` | `LOG-LIGHT-HOLD-01` | Evidence available, outside the current Verified scope | Excluded |

---

## 7.1 Return Ramp Hold Evidence Details

`RULE-22_RETURN_RAMP_HOLD` is Verified only for the FULL /
`INSUFFICIENT_OBSERVATION` coverage row below. LIGHT Observation coverage is
listed separately in Section 7 and remains outside the current Verified scope.

| Scenario | Scenario File | RULE | Expected Category | Reason | Observation Mode | Condition | Raw Log | Verified Log | Validator | Status | Note |
|----------|---------------|------|-------------------|--------|------------------|-----------|---------|--------------|-----------|--------|------|
| ramp_hold_insufficient_observation | `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | RULE-22_RETURN_RAMP_HOLD | hold | INSUFFICIENT_OBSERVATION | FULL | STEP 9 advances from `0.10` to `0.30`; STEP 10 holds `0.30 -> 0.30` with `state_transition=RAMPING->RAMPING` and no same-step advance / abort / complete / emergency transition | `RAW-RAMP-HOLD-INSUFF-01` | `LOG-RAMP-HOLD-INSUFF-01` | reason / category / observation mode / state transition / unchanged ramp level / previous-step advance / forbidden outcomes in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_hold_insufficient_observation`) | Verified | Runnable scenario, raw log, verified log, and validator assertion coverage are complete for this FULL-observation hold reason |

---

## 7.2 Return Ramp Advance Evidence Details

`RULE-21_RETURN_RAMP_ADVANCE` is Verified only for the FULL-observation
coverage rows below. LIGHT-observation-based advance remains Hold.

| Scenario | Scenario File | RULE | Expected Category | Observation Mode | Condition | Raw Log | Verified Log | Validator | Status | Note |
|----------|---------------|------|-------------------|------------------|-----------|---------|--------------|-----------|--------|------|
| ramp_complete | `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | RULE-21_RETURN_RAMP_ADVANCE | switch | FULL | Four advance transitions (`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90`) are emitted with `reason=RECOVERED_PATH_STABLE`, followed by `RULE-24_RETURN_RAMP_COMPLETE`. `RULE-23_RETURN_RAMP_ABORT` and emergency transition markers do not appear | `RAW-RAMP-FULL-ADV-01` | `LOG-RAMP-FULL-ADV-01` | ramp_level transition pairs / category / observation mode / observation category / reason / completion / forbidden abort in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_complete`) | Verified | Runnable scenario, raw log, verified log, and validator assertion coverage are complete for this FULL-observation advance sequence (positive evidence) |
| ramp_abort_full_stability_dip | `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | RULE-21_RETURN_RAMP_ADVANCE (negative) | abort | FULL | Instability is detected immediately before a due advance step and `RULE-23_RETURN_RAMP_ABORT` is emitted instead. `RULE-21_RETURN_RAMP_ADVANCE` never appears | `RAW-RAMP-ABORT-FULLDIP-01` | `LOG-RAMP-FULL-ADV-01` | forbidden RULE-21 / forbidden RULE-24 / abort reason / unchanged weight in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_abort_full_stability_dip`) | Verified | Negative evidence confirming advance does not occur under an instability condition |

---

## 7.3 Return Ramp Complete Evidence Details

`RULE-24_RETURN_RAMP_COMPLETE` is Verified only for the FULL-observation
coverage row below. The `ramp_complete` scenario runs with
`scenario_steps=22`, including the post-completion tail (STEP 18-21) after
completion at STEP 17.

| Scenario | Scenario File | RULE | Expected Category | Observation Mode | Condition | Raw Log | Verified Log | Validator | Status | Note |
|----------|---------------|------|-------------------|------------------|-----------|---------|--------------|-----------|--------|------|
| ramp_complete | `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | RULE-24_RETURN_RAMP_COMPLETE | switch | FULL | Completion is emitted at STEP 17 with `recovered_weight=1.00`, `evacuation_weight=0.00`, and `reason=RAMP_TARGET_REACHED`. STEP 18-19 emit `RULE-11_RECOVERY_cooldown`, and STEP 20-21 emit `RULE-01_KEEP_score` with `mode=NORMAL`. `RULE-24_RETURN_RAMP_COMPLETE` and `RULE-25_RETURN_RAMP_START` each occur exactly once in the output | `RAW-RAMP-FULL-ADV-01` | `LOG-RAMP-COMPLETE-01` | completion state / post-completion cooldown / NORMAL hysteresis / single-occurrence completion and ramp start / forbidden abort in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_complete`) | Verified | Runnable scenario, raw log, verified log, and validator assertion coverage are complete for this FULL-observation completion and post-completion state |

---

## 8. Recovery Abort Handling Evidence Details

`RULE-23_RETURN_RAMP_ABORT` is Verified only for the four FULL-observation
abort class coverage rows below. The v0.3 ramp engine's internal
`RECOVERED_PATH_UNSTABLE` / `RECOVERED_PATH_INVALID` abort trace remains
outside the Verified scope described in Section 2.2.

| Scenario | Scenario File | RULE | Expected Category | Abort Class | Fallback Block Reason | Raw Log | Verified Log | Validator | Status |
|----------|---------------|------|-------------------|-------------|-----------------------|---------|--------------|-----------|--------|
| soft_abort_hold_and_reobserve | `sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py` | RULE-23_RETURN_RAMP_ABORT | abort_and_stabilize | SOFT_ABORT | N/A | `RAW-ABORT-SOFT-01` | `LOG-ABORT-01` | abort_class / reason / post-abort state / cross-class exclusion in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=soft_abort_hold_and_reobserve`) | Verified |
| hard_abort_ramp_down | `sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py` | RULE-23_RETURN_RAMP_ABORT | hard_abort_ramp_down | HARD_ABORT | N/A | `RAW-ABORT-HARD-01` | `LOG-ABORT-01` | abort_class / reason / post-abort state / cross-class exclusion in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=hard_abort_ramp_down`) | Verified |
| emergency_cut_no_fallback | `sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py` | RULE-23_RETURN_RAMP_ABORT | emergency_cut_no_fallback | EMERGENCY_CUT | NO_CAPACITY_MARGIN | `RAW-ABORT-EMERG-01` | `LOG-ABORT-01` | abort_class / reason / post-abort state / cross-class exclusion in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=emergency_cut_no_fallback`) | Verified |
| two_path_degraded_abort | `sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py` | RULE-23_RETURN_RAMP_ABORT | two_path_degraded_arbitration | DEGRADED_ABORT | NO_SAFE_ALTERNATE | `RAW-ABORT-2PATH-01` | `LOG-ABORT-01` | abort_class / reason / post-abort state / cross-class exclusion in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=two_path_degraded_abort`) | Verified |

---

## 9. v0.3 Experimental RULE Integration Candidates

| RULE | Classification | Summary | Next |
|------|----------------|-----------|-----------|
| RULE-25_RETURN_RAMP_START | Formal integration candidate | v0.3 ramp entry point | Specify delta from RULE-19 |
| RULE-21_RETURN_RAMP_ADVANCE (FULL) | Formal integration candidate (Verified) | Increase weight only when stable | Integrate advance conditions into the specification text |
| RULE-22_RETURN_RAMP_HOLD | Formal integration candidate | Hold weight during observation | Define hold / advance / abort transitions |
| RULE-23_RETURN_RAMP_ABORT | Formal integration candidate | Abort return on instability | Define abort threshold |
| RULE-24_RETURN_RAMP_COMPLETE | Formal integration candidate (Verified) | Confirm reintegration completion | Integrate completion conditions into the specification text |
| RULE-21_RETURN_RAMP_ADVANCE (LIGHT) | Hold | Safety boundary is underspecified | Connect to Fast Mode spec |

Notes:

- v0.3 ramp behavior remains under formal specification integration. `RULE-22_RETURN_RAMP_HOLD` is Verified in this matrix for the covered hold evidence, including `INSUFFICIENT_OBSERVATION`. `RULE-23_RETURN_RAMP_ABORT` is Verified in this matrix for the `SOFT_ABORT` / `HARD_ABORT` / `EMERGENCY_CUT` / `DEGRADED_ABORT` FULL abort class evidence. `RULE-21_RETURN_RAMP_ADVANCE` is Verified in this matrix for FULL observation evidence (the `ramp_complete` advance sequence and the `ramp_abort_full_stability_dip` negative evidence). `RULE-24_RETURN_RAMP_COMPLETE` is Verified in this matrix for FULL observation completion and post-completion state evidence. Abort threshold, advance condition, and completion threshold specification integration remain separate work.
- Formal integration candidate means the behavior is worth integrating into the specification; this classification is independent of promotion to Verified, though `RULE-21_RETURN_RAMP_ADVANCE (FULL)` and `RULE-24_RETURN_RAMP_COMPLETE` now satisfy both.
- `RULE-19_RETURN_SWITCH` remains the Verified v0.2 direct return rule.
- `RULE-25_RETURN_RAMP_START` is the Experimental v0.3 ramp entry rule. It replaces the direct return execution point with progressive ramp start, but is not semantically identical to `RULE-19_RETURN_SWITCH`.
- `RULE-25_RETURN_RAMP_START` remains outside the `RULE-01` through `RULE-24` Verified namespace until formal integration is completed.
- `RULE-21_RETURN_RAMP_ADVANCE (FULL)` has been promoted to Verified for FULL observation evidence. Formal integration of the ramp increment and advance threshold into the specification text remains separate work.
- `RULE-24_RETURN_RAMP_COMPLETE` has been promoted to Verified for FULL observation completion and post-completion state evidence. Formal integration of the completion threshold into the specification text remains separate work. Completion behavior under LIGHT observation is not covered.
- `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` remains Hold. Current authoritative LIGHT policy is that LIGHT observation must emit or resolve to `RULE-22_RETURN_RAMP_HOLD` unless it is promoted to FULL observation or explicit LIGHT promotion gates are defined and satisfied.
- Historical v0.3 LIGHT advance logs, including `ramp_light_tolerates_moderate_dip`, are retained as experimental history and must not be treated as current expected LIGHT policy.
- Promotion to formal specification status requires transition conditions, thresholds, and FULL / LIGHT observation handling to be integrated into the specification text. This requirement is separate from evidence-based Verified status in this matrix.

---

## 10. Log References

- `LOG-DEG-01`: `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md`
- `LOG-DEG-02`: `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md`
- `LOG-ABORT-01`: `sim/02_controlled/08_recovery_abort_handling/logs/verified/recovery_abort_stabilization_validation_log.md`
- `LOG-HOLD-01`: `sim/02_controlled/05_recovery_hold/logs/rcu_decision_v01_recovery_hold_behavior_log.md`
- `LOG-LIGHT-HOLD-01`: `sim/02_controlled/07_light_observation_stub/logs/verified/light_observation_hold_validation_log.md`
- `LOG-OSC-01`: `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md`
- `LOG-REC-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md`
- `LOG-RES-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md`
- `LOG-RES-02`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_rule_unification_log.md`
- `LOG-RR-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md`
- `LOG-RR-02`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md`
- `LOG-RAMP-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_full_light_observation_validation_log.md`
- `LOG-RAMP-02`: `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt`
- `LOG-RAMP-03`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md`
- `LOG-RAMP-HOLD-INSUFF-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_ramp_hold_insufficient_observation_validation_log.md`
- `LOG-RAMP-FULL-ADV-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_ramp_full_advance_validation_log.md`
- `LOG-RAMP-COMPLETE-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_ramp_complete_validation_log.md`
- `LOG-SW-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md`
- `LOG-TRUST-BLOCK-01`: `sim/02_controlled/09_rule_collision_matrix/logs/trust_block_vs_switch_validation_log.md`
- `RAW-RAMP-HOLD-INSUFF-01`: `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_hold_insufficient_observation_run.txt`
- `RAW-RAMP-FULL-ADV-01`: `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_complete_run.txt`
- `RAW-RAMP-ABORT-FULLDIP-01`: `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_abort_full_stability_dip_run.txt`
- `RAW-LIGHT-FN-01`: `sim/02_controlled/07_light_observation_stub/logs/raw/light_false_negative_run.txt`
- `RAW-LIGHT-ST-01`: `sim/02_controlled/07_light_observation_stub/logs/raw/light_stale_telemetry_run.txt`
- `RAW-LIGHT-MI-01`: `sim/02_controlled/07_light_observation_stub/logs/raw/light_masked_instability_run.txt`
- `RAW-ABORT-SOFT-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/soft_abort_hold_and_reobserve_run.txt`
- `RAW-ABORT-HARD-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/hard_abort_ramp_down_run.txt`
- `RAW-ABORT-EMERG-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/emergency_cut_no_fallback_run.txt`
- `RAW-ABORT-2PATH-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/two_path_degraded_abort_run.txt`

---

## 11. Glossary References

- `GLOSSARY-LIGHT-EN-01`: `docs/specification/published/glossary/psc_light_observation_glossary_v0.1_en.md`
