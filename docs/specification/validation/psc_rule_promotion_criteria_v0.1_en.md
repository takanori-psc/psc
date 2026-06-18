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
`RULE-24_RETURN_RAMP_COMPLETE`, from Experimental to Verified.

This document is a draft that defines promotion criteria. It does not change
the current status of any existing RULE. The Evidence Matrix is not edited in
this step.

---

## 2. Current Status

The target RULEs are currently treated as Experimental in
`psc_evidence_matrix_v0.1_en.md`.

| RULE | Current Status | Current Position |
|------|----------------|------------------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Experimental | Candidate RULE that progressively increases the recovered path traffic weight when ramp conditions are satisfied |
| `RULE-22_RETURN_RAMP_HOLD` | Experimental | Candidate RULE that keeps the current weight when ramp progress conditions are insufficient |
| `RULE-23_RETURN_RAMP_ABORT` | Experimental | Candidate RULE that aborts recovery when instability is detected during the ramp |
| `RULE-24_RETURN_RAMP_COMPLETE` | Experimental | Candidate RULE that finalizes progressive reintegration into the recovered path |

These RULEs already have partial behavioral evidence from experimental
scenarios and raw / verified logs. However, promotion to Verified requires
consistent scenario, log, expected result, validator check, and Evidence Matrix
mapping coverage.

---

## 3. Common Promotion Conditions

Each RULE must satisfy at least the following conditions before it can be
promoted to Verified.

| Required evidence | Requirement |
|-------------------|-------------|
| Scenario file | A reproducible scenario file exists that triggers the RULE either directly or as the clear primary target |
| Raw log | The scenario execution produces a raw log containing the RULE name, input state, decision reason, and final action |
| Expected result | The scenario expected result is explicitly defined as a category, reason, and final action |
| Validator check | The scenario execution or aggregate validator asserts the expected category, RULE name, and key safety conditions |
| Evidence Matrix mapping | The RULE, scenario, raw log, verified log, Evidence Step, and Trace Summary are organized at a granularity that can be added to the Evidence Matrix |

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
| Evidence Matrix mapping | The mapping between `RULE-21_RETURN_RAMP_ADVANCE` and the FULL observation scenario / raw log / verified log can be added |

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

---

## 5. RULE-22_RETURN_RAMP_HOLD Promotion Criteria

### 5.1 Meaning of the Promotion Target

`RULE-22_RETURN_RAMP_HOLD` is the RULE that keeps the current traffic weight
during return ramp when advance conditions are insufficient, preventing early
return or unnecessary switching.

### 5.2 Required Evidence

| Required evidence | Criteria |
|-------------------|----------|
| Scenario file | A scenario exists in which ramp hold occurs due to false negative, stale telemetry, masked instability, or insufficient observation |
| Raw log | The log records `RULE-22_RETURN_RAMP_HOLD`, the hold reason, observation condition, and weight before and after hold |
| Expected result | The expected category is hold, and the recovered path weight does not increase |
| Validator check | The validator asserts the hold reason and unchanged weight, and confirms there is no misclassification as advance / abort |
| Evidence Matrix mapping | The mapping between LIGHT observation scenarios, raw logs, verified logs, and Evidence Steps can be added |

### 5.3 Promotion Review Points

Promotion of `RULE-22_RETURN_RAMP_HOLD` to Verified requires at least the
following hold reasons to be explicitly distinguished.

| Hold reason | Required confirmation |
|-------------|-----------------------|
| `OBSERVATION_FALSE_NEGATIVE` | Hold occurs when actual instability is not sufficiently detected by LIGHT observation |
| `STALE_TELEMETRY` | Advance does not occur and hold is selected when telemetry is stale |
| `MASKED_INSTABILITY` | Hold occurs when instability is hidden by sparse evidence |
| `INSUFFICIENT_OBSERVATION` | Hold occurs when observation data required for the advance decision is insufficient |

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
| Evidence Matrix mapping | The mapping between abort handling scenarios, raw logs, verified logs, and Evidence Steps can be added |

### 6.3 Promotion Review Points

Promotion of `RULE-23_RETURN_RAMP_ABORT` to Verified requires that results for
each abort class are not conflated.

| Abort class | Expected result |
|-------------|-----------------|
| `SOFT_ABORT` | Keep allocation and proceed to observation reinforcement and Resolver re-evaluation |
| `HARD_ABORT` | Ramp down the suspect recovered path and notify the source-side PSC |
| `EMERGENCY_CUT` | Exclude the unsafe path and block fallback transfer when capacity margin is insufficient |
| `DEGRADED_ABORT` | When no safe alternate exists, Resolver performs least-bad arbitration |

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
| Validator check | The validator asserts completion threshold, final allocation, post-completion state, and that no additional advance is needed |
| Evidence Matrix mapping | The mapping between the complete scenario, raw log, verified log, and Evidence Step can be added |

### 7.3 Promotion Review Points

`RULE-24_RETURN_RAMP_COMPLETE` must not be marked Verified merely because the
weight reached the maximum value. The following conditions must also be met.

- The completion threshold is defined in the specification
- No abort condition holds immediately before completion
- The state after completion is stable
- No unnecessary additional advance occurs after completion

---

## 8. Promotion Review Order

Because RULE-21 through RULE-24 depend on each other, promotion review should
be performed in the following order.

1. Confirm the safe-side behavior of `RULE-22_RETURN_RAMP_HOLD` under insufficient observation.
2. Confirm the abnormal-condition abort behavior of `RULE-23_RETURN_RAMP_ABORT`.
3. Confirm FULL observation advance conditions for `RULE-21_RETURN_RAMP_ADVANCE`.
4. Confirm completion conditions for `RULE-24_RETURN_RAMP_COMPLETE`.

This order verifies the safe-side stop conditions provided by hold / abort
before validating advance / complete.

---

## 9. Non-Goals

This document does not perform the following.

- Change any existing RULE status from Experimental to Verified
- Edit `psc_evidence_matrix_v0.1_en.md`
- Define promotion criteria for RULE-25
- Treat `RULE-21_RETURN_RAMP_ADVANCE` based on LIGHT observation as Verified

---

## 10. Next Steps

The next steps for this draft are as follows.

1. Identify missing scenario files and raw logs for each RULE.
2. Define validator check assert items for each scenario.
3. Prepare Evidence Matrix mapping proposals in a separate step.
4. Define the false-positive / false-negative boundaries for LIGHT observation.
5. Review RULEs as Verified promotion candidates once the conditions are satisfied.
