# PSC RULE Promotion Criteria v0.1

## Document Information

| Item | Description |
|------|-------------|
| Document ID | `PSC-RULE-PROMOTION-CRITERIA-v0.1-en` |
| Title | PSC RULE-21 through RULE-24 Promotion Criteria |
| Version | v0.1 |
| Language | English |
| Status | Draft |
| Scope | `RULE-21_RETURN_RAMP_ADVANCE` through `RULE-24_RETURN_RAMP_COMPLETE` |
| Related Document | `docs/specification/validation/psc_evidence_matrix_v0.1_en.md` |

---

## 1. Purpose

This document defines the evidence required to promote the PSC v0.3
recovery ramp RULEs, `RULE-21_RETURN_RAMP_ADVANCE`,
`RULE-22_RETURN_RAMP_HOLD`, `RULE-23_RETURN_RAMP_ABORT`, and
`RULE-24_RETURN_RAMP_COMPLETE`, from Experimental to Verified, and defines
the current state of criteria satisfaction for each RULE.

This document is a draft that records the promotion criteria and their
satisfaction outcomes; it is not the authoritative source for RULE status.
The Evidence Matrix is the authoritative source for RULE status, and this
document does not override the status recorded there.

---

## 2. Current Status

The target RULEs are tracked in `psc_evidence_matrix_v0.1_en.md`.
`RULE-21_RETURN_RAMP_ADVANCE` is Verified for FULL observation evidence;
`RULE-22_RETURN_RAMP_HOLD` is Verified for the covered FULL-observation hold
evidence with `reason=INSUFFICIENT_OBSERVATION`; `RULE-23_RETURN_RAMP_ABORT` is
Verified for the `SOFT_ABORT` / `HARD_ABORT` / `EMERGENCY_CUT` /
`DEGRADED_ABORT` FULL abort class evidence; `RULE-24_RETURN_RAMP_COMPLETE` is
Verified for FULL observation completion and post-completion state evidence.

| RULE | Current Status | Current Position |
|------|----------------|------------------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Verified (FULL only) | RULE that progressively increases the recovered path traffic weight when ramp conditions are satisfied; current Verified scope is limited to FULL observation evidence. LIGHT-observation-based advance remains Hold |
| `RULE-22_RETURN_RAMP_HOLD` | Verified | RULE that keeps the current weight when ramp progress conditions are insufficient; current Verified scope is limited to FULL / `INSUFFICIENT_OBSERVATION` evidence |
| `RULE-23_RETURN_RAMP_ABORT` | Verified | RULE that aborts recovery when instability is detected during the ramp; current Verified scope is limited to `SOFT_ABORT` / `HARD_ABORT` / `EMERGENCY_CUT` / `DEGRADED_ABORT` FULL abort class evidence |
| `RULE-24_RETURN_RAMP_COMPLETE` | Verified (FULL only) | RULE that finalizes progressive reintegration into the recovered path; current Verified scope is limited to FULL observation completion and post-completion state evidence |

LIGHT observation evidence and evidence outside each RULE's current Verified
scope remain Hold or Experimental within their stated boundaries.

---

## 3. Common Promotion Conditions

Promotion to Verified and the current state of criteria satisfaction for each
RULE are evaluated against at least the following conditions.

| Required evidence | Requirement |
|-------------------|-------------|
| Scenario file | A reproducible scenario file exists that triggers the RULE either directly or as the clear primary target |
| Raw log | The scenario execution produces a raw log containing the RULE name, input state, decision reason, and final action |
| Expected result | The scenario expected result is explicitly defined as a category, reason, and final action |
| Validator check | The scenario execution or aggregate validator asserts the expected category, RULE name, and key safety conditions |
| Evidence Matrix mapping | The RULE, scenario, raw log, verified log, Evidence Step, and Trace Summary are organized at a granularity that is traceable in the Evidence Matrix |

Promotion to Verified requires reproducibility and traceability, not merely the
existence of logs.

---

## 4. RULE-21_RETURN_RAMP_ADVANCE Promotion Criteria

### 4.1 Meaning of the Promotion Target

`RULE-21_RETURN_RAMP_ADVANCE` is the RULE that progressively increases the
traffic weight of the recovered path when the recovered path is sufficiently
stable and advancing the return ramp is considered safe.

### 4.2 Required Evidence

| Required evidence | Criteria |
|-------------------|----------|
| Scenario file | A scenario exists in which ramp advance occurs only when stability conditions are satisfied based on FULL observation |
| Raw log | The log records `RULE-21_RETURN_RAMP_ADVANCE`, the weight before and after advance, the stability conditions, and the observation mode |
| Expected result | The expected category is ramp advance, and the weight increases by a defined step size |
| Validator check | The validator asserts that weight increases only when advance conditions are satisfied, and does not increase under hold / abort conditions |
| Evidence Matrix mapping | The mapping between `RULE-21_RETURN_RAMP_ADVANCE` and the FULL observation scenario / raw log / verified log is traceable |

### 4.3 Hold Conditions for LIGHT Observation

`RULE-21_RETURN_RAMP_ADVANCE` remains Hold for advance decisions based on
LIGHT observation.

Until false-positive / false-negative behavior under LIGHT observation is
sufficiently bounded, LIGHT observation must not be treated as Verified
evidence for `RULE-21_RETURN_RAMP_ADVANCE`. In particular, LIGHT advance is
outside the promotion target if any of the following remain undefined.

- The upper bound for false positives where LIGHT observation incorrectly treats an actually unstable path as stable
- The handling of false negatives where LIGHT observation incorrectly treats an actually stable path as unstable or insufficiently observed
- The conditions for escalating from LIGHT observation to FULL observation
- The boundary for selecting `RULE-22_RETURN_RAMP_HOLD` when LIGHT observation is insufficient

### 4.4 Promotion Outcome

`RULE-21_RETURN_RAMP_ADVANCE` is promoted to Verified for FULL observation
evidence, now that a dedicated scenario, raw log, verified log, and validator
checks asserting the advance sequence and a negative case are in place.

As positive evidence, the `ramp_complete` scenario shows four advance
transitions (`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90`) followed by
`RULE-24_RETURN_RAMP_COMPLETE`. As negative evidence, the
`ramp_abort_full_stability_dip` scenario shows that
`RULE-21_RETURN_RAMP_ADVANCE` never fires when instability is detected
immediately before a due advance step.

LIGHT-observation-based advance remains Hold until the conditions in Section
4.3 are satisfied. Formal integration of the ramp increment and advance
threshold into the specification body also remains separate work.

---

## 5. RULE-22_RETURN_RAMP_HOLD Promotion Criteria

### 5.1 Meaning of the Promotion Target

`RULE-22_RETURN_RAMP_HOLD` is the RULE that keeps the current traffic weight
during return ramp when advance conditions are insufficient, preventing early
return or unnecessary switching.

### 5.2 Required Evidence

| Required evidence | Criteria |
|-------------------|----------|
| Scenario file | A scenario exists in which ramp hold occurs due to insufficient observation under FULL observation |
| Raw log | The log records `RULE-22_RETURN_RAMP_HOLD`, the hold reason, observation condition, and weight before and after hold |
| Expected result | The expected category is hold, and the recovered path weight does not increase |
| Validator check | The validator asserts the hold reason and unchanged weight, and confirms there is no misclassification as advance / abort |
| Evidence Matrix mapping | The mapping between the FULL observation scenario, raw log, verified log, and Evidence Step is traceable |

### 5.3 Promotion Review Points

The current Verified scope for `RULE-22_RETURN_RAMP_HOLD` covers only the
`INSUFFICIENT_OBSERVATION` reason under FULL observation. LIGHT Observation
reasons remain available as evidence but are outside the current Verified
scope.

Future expansion of RULE-22 coverage should explicitly distinguish the
following hold reasons before treating them as part of the Verified scope.

| Hold reason | Required confirmation |
|-------------|-----------------------|
| `OBSERVATION_FALSE_NEGATIVE` | Hold occurs when actual instability is not sufficiently detected by LIGHT observation |
| `STALE_TELEMETRY` | Advance does not occur and hold is selected when telemetry is stale |
| `MASKED_INSTABILITY` | Hold occurs when instability is hidden by sparse evidence |
| `INSUFFICIENT_OBSERVATION` | Hold occurs when observation data required for the advance decision is insufficient |

### 5.4 Promotion Outcome

`RULE-22_RETURN_RAMP_HOLD` is promoted to Verified for
`reason=INSUFFICIENT_OBSERVATION` under FULL observation, now that the
scenario, raw log, verified log, and validator checks confirming the hold
reason, unchanged weight, and exclusion of advance / abort are in place.

LIGHT observation reasons and the hold reasons outside the current Verified
scope described in Section 5.3 remain Hold or Experimental until additional
validation is complete.

---

## 6. RULE-23_RETURN_RAMP_ABORT Promotion Criteria

### 6.1 Meaning of the Promotion Target

`RULE-23_RETURN_RAMP_ABORT` is the RULE that aborts the recovery attempt when
recovered path instability, a safety boundary violation, or fallback failure is
detected during return ramp.

### 6.2 Required Evidence

| Required evidence | Criteria |
|-------------------|----------|
| Scenario file | Scenarios exist that reproduce each abort class: soft abort, hard abort, emergency cut, and two-path degraded abort |
| Raw log | The log records `RULE-23_RETURN_RAMP_ABORT`, abort class, abort reason, fallback availability, and stabilization action |
| Expected result | The expected category is defined per abort class, and the return ramp attempt becomes aborted |
| Validator check | The validator asserts abort class, fallback block reason, stabilization action, and whether source notification is present |
| Evidence Matrix mapping | The mapping between abort handling scenarios, raw logs, verified logs, and Evidence Steps is traceable |

### 6.3 Promotion Review Points

Promotion of `RULE-23_RETURN_RAMP_ABORT` to Verified requires that results for
each abort class are not conflated.

| Abort class | Expected result |
|-------------|-----------------|
| `SOFT_ABORT` | Keep allocation and proceed to observation reinforcement and Resolver re-evaluation |
| `HARD_ABORT` | Ramp down the suspect recovered path and notify the source-side PSC |
| `EMERGENCY_CUT` | Exclude the unsafe path and block fallback transfer when capacity margin is insufficient |
| `DEGRADED_ABORT` | When no safe alternate exists, Resolver performs least-bad arbitration |

### 6.4 Promotion Outcome

`RULE-23_RETURN_RAMP_ABORT` is promoted to Verified for the
`SOFT_ABORT`, `HARD_ABORT`, `EMERGENCY_CUT`, and `DEGRADED_ABORT` FULL abort
class evidence, now that dedicated scenarios, raw logs, verified logs, and
validator checks asserting abort class, reason, post-abort state, and
cross-class exclusion are in place for all four classes.

The abort trace emitted inside the v0.3 recovery ramp engine
(`reason=RECOVERED_PATH_UNSTABLE` / `reason=RECOVERED_PATH_INVALID`), and the
LIGHT delayed abort design stub (`light_delayed_abort_stub.py`), remain
outside this Verified scope. Formal integration of the abort threshold into
the specification body also remains separate work.

---

## 7. RULE-24_RETURN_RAMP_COMPLETE Promotion Criteria

### 7.1 Meaning of the Promotion Target

`RULE-24_RETURN_RAMP_COMPLETE` is the RULE that finalizes return ramp
completion when progressive reintegration into the recovered path satisfies
the completion conditions.

### 7.2 Required Evidence

| Required evidence | Criteria |
|-------------------|----------|
| Scenario file | A scenario exists that reproduces ramp start, advance, successful hold checks, and complete |
| Raw log | The log records `RULE-24_RETURN_RAMP_COMPLETE`, final weight, completion condition, and NORMAL recovery state |
| Expected result | The expected category is ramp complete, and recovered path reintegration is complete |
| Validator check | The validator asserts `recovered_weight=1.00`, `evacuation_weight=0.00`, `reason=RAMP_TARGET_REACHED`, completion at the expected step, single occurrence of RULE-24, no post-completion advance / duplicate completion / abort, recovery cooldown, and transition to NORMAL |
| Evidence Matrix mapping | The mapping between the complete scenario, raw log, verified log, and Evidence Step is traceable |

### 7.3 Promotion Review Points

For evidence-based Verified status, `RULE-24_RETURN_RAMP_COMPLETE` must not be
marked Verified merely because a maximum-weight value appears. The executable
scenario and logs must explicitly show arrival at the completion target, and
the following outcomes must be asserted.

- `recovered_weight=1.00`, `evacuation_weight=0.00`, and
  `reason=RAMP_TARGET_REACHED` are emitted at the expected completion step
- `RULE-24_RETURN_RAMP_COMPLETE` occurs exactly once
- No additional advance, duplicate completion, or abort occurs after completion
- Recovery cooldown is followed by transition to the NORMAL state

Defining `ramp_max_weight=1.00` as the completion threshold in the formal
specification is separate Remaining Work and is not a condition for the
current evidence-based limited Verified scope.

### 7.4 Promotion Outcome

`RULE-24_RETURN_RAMP_COMPLETE` is Verified for the limited scope of FULL
observation completion and post-completion evidence, now that a dedicated
scenario (`ramp_complete`,
`scenario_steps=22`), raw log, verified log, and validator checks asserting
completion state, post-completion state, and no additional advance are in
place.

The executable scenario and log show completion at STEP 17 with
`recovered_weight=1.00`, `evacuation_weight=0.00`, and
`reason=RAMP_TARGET_REACHED`, and the validator asserts those emitted values
at that step. The validator does not assert the configuration value itself or
its definition in the formal specification. Defining `ramp_max_weight=1.00`
as the formal completion threshold remains separate work from evidence-based
Verified status.

That no abort condition holds immediately before completion is confirmed by
the validator asserting that `RULE-23_RETURN_RAMP_ABORT` does not appear
anywhere in the output. That the post-completion state is stable is
confirmed by `RULE-11_RECOVERY_cooldown` at STEP 18-19 and `RULE-01_KEEP_score`
(`mode=NORMAL`) at STEP 20-21. The validator also confirms that RULE-24 occurs
exactly once and that no additional advance, duplicate completion, or ramp
restart occurs after STEP 17.

Completion behavior under LIGHT observation is not covered by this Verified
scope.

---

## 8. Criteria-Satisfaction Review Order

Because RULE-21 through RULE-24 depend on each other, satisfaction of the
promotion criteria was confirmed in the following order.

1. Confirm the safe-side behavior of `RULE-22_RETURN_RAMP_HOLD` under insufficient observation.
2. Confirm the abnormal-condition abort behavior of `RULE-23_RETURN_RAMP_ABORT`.
3. Confirm FULL observation advance conditions for `RULE-21_RETURN_RAMP_ADVANCE`.
4. Confirm completion conditions for `RULE-24_RETURN_RAMP_COMPLETE`.

This order confirmed the safe-side stop conditions provided by hold / abort
before confirming criteria satisfaction for advance / complete.

---

## 9. Non-Goals

The following are outside the scope of this document.

- Independently determine or override RULE status for which the Evidence Matrix is authoritative
- Define promotion criteria for RULE-25
- Treat `RULE-21_RETURN_RAMP_ADVANCE` based on LIGHT observation as Verified

---

## 10. Next Steps

The remaining work is listed below. These items are treated as formal
specification integration or additional validation separate from
evidence-based Verified status.

1. Integrate RULE-21 through RULE-24 into the formal specification.
2. Formally specify the ramp_increment / advance threshold.
3. Formally specify the abort threshold.
4. Formally specify the completion threshold.
5. Perform additional validation of LIGHT observation boundaries.
6. Perform additional validation of the `RECOVERED_PATH_UNSTABLE` /
   `RECOVERED_PATH_INVALID` abort traces inside the ramp engine.
