# PSC RCU Recovery Return Model v0.2

## 1. Document Information

- Document Name : PSC RCU Recovery Return Model
- Version : v0.2
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / RCU
- Document Type : Model Specification
- Status : Draft
- Author : T. Hirose
- Language : English

- Based on : PSC RCU Decision Model v0.1
- Related Models :
  - PSC Routing Table Model v0.2
  - PSC Telemetry Model v0.2

---

## 2. Recovery Return Model Overview

PSC v0.2 introduces a staged recovery return mechanism
that extends the conservative recovery hold behavior of v0.1.

Unlike v0.1, which maintains the current stable path after recovery,
v0.2 allows controlled return to a recovered path under specific conditions.

The recovery return process consists of the following stages:

- RECOVERY_CANDIDATE
  A recovered path is detected based on trust and stability thresholds

- VALIDATING
  The candidate path is continuously validated over multiple steps

- RETURN_ELIGIBLE
  The candidate satisfies validation requirements

- RETURN_SWITCH
  The system switches to the recovered path only if improvement is sufficient

- RETURN_KEEP
  Even if eligible, the system may retain the current path if switching conditions are not met

This staged approach ensures that recovery does not introduce instability,
while still allowing adaptive performance improvement.

---

## 3. Validation Status

The staged recovery return behavior has been implemented
and validated through controlled simulation.

Validated sequence:

- fallback to a safe path after degradation
- recovered path detection as `RECOVERY_CANDIDATE`
- validation window progression
- transition to `RETURN_ELIGIBLE`
- conditional `RETURN_SWITCH`
- recovery cooldown after return

Validation logs:

- Recovery validation:
  [log](sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md)

- v0.1 vs v0.2 comparison:
  [log](sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_vs_v01_recovery_hold_log.md)

---

## 4. Design Note (v0.2 Scope)

The current implementation validates staged recovery return
under a controlled single-candidate scenario.

Generalization of recovery candidates (multiple paths, dynamic tracking)
is considered future work beyond v0.2 scope.

---

## 5. Objective

This document defines the staged recovery return behavior of PSC RCU.

While PSC RCU Decision Model v0.1 establishes conservative recovery hold behavior,
this model extends the decision process by introducing a controlled re-entry path
for recovered routes.

The goal is not immediate performance restoration.
The goal is stable and explainable re-admission of recovered paths.

---

## 6. Relationship to v0.1

This model does not replace v0.1 behavior.
It extends it.

### 6.1 v0.1 Behavior

In v0.1, PSC does not immediately return to a previously degraded path
even if that path later becomes the best-performing path again.

If the currently selected path remains stable and trusted,
PSC keeps the current path.

### 6.2 v0.2 Extension

v0.2 preserves the conservative design of v0.1,
but adds a staged re-entry mechanism.

Recovered paths are not immediately selected.
They must first pass validation before becoming eligible again.

---

## 7. Design Principles

### 7.1 Stability First

Recovery return must not undermine the stability achieved after failover.

### 7.2 Recovered Path != Immediately Reusable Path

A recovered path is treated as a candidate,
not as an immediate switch target.

### 7.3 Explainable Decision Process

Each recovery return decision must be traceable through explicit state transitions and rules.

### 7.4 Separation of Roles

- Routing Table : stores path state and candidate information
- Telemetry : provides evidence with confidence and freshness
- RCU : performs staged evaluation and return eligibility judgment
- Resolver : performs final arbitration only when ambiguity remains

---

## 8. Recovery Return State Model

The following additional recovery return states are introduced.

- RECOVERY_CANDIDATE
- VALIDATING
- RETURN_ELIGIBLE

These states are logical control states for the RCU decision process.

### 8.1 RECOVERY_CANDIDATE

A previously degraded or unavailable path has recovered
to a minimum acceptable condition.

### 8.2 VALIDATING

The recovered path is observed over a validation window.

### 8.3 RETURN_ELIGIBLE

The recovered path has passed validation
and may now be considered for selection.

Important:

RETURN_ELIGIBLE does not mean immediate switch.

---

## 9. Entry Conditions

A path may enter RECOVERY_CANDIDATE if all of the following conditions are satisfied:

- path was previously degraded, failed, limited, or excluded
- trust is above the recovery minimum threshold
- health is valid
- telemetry freshness is acceptable
- confidence is not below the minimum accepted level

---

## 10. Validation Conditions

A path in RECOVERY_CANDIDATE enters VALIDATING and is observed for a fixed window.

Validation checks may include:

- trust remains above threshold
- stability remains above threshold
- health remains valid
- no rapid oscillation is detected
- telemetry confidence remains acceptable
- no policy restriction blocks re-entry

If validation fails, the path returns to RECOVERY_CANDIDATE or remains excluded.

---

## 11. Return Eligibility

A path becomes RETURN_ELIGIBLE only when the validation window is completed successfully.

Return eligibility means:

- the path may be reconsidered by RCU
- the path may compete again with the currently selected path
- the path may be submitted to Resolver if ambiguity exists

Return eligibility does not force selection.

---

## 12. Return Decision Policy

### 12.1 Basic Rule

If the currently selected path remains stable and trusted,
PSC does not switch back aggressively.

### 12.2 Controlled Return

A RETURN_ELIGIBLE path may be selected only if:

- the score improvement is meaningful
- return hysteresis conditions are satisfied
- stability risk is acceptable
- policy constraints permit re-entry

### 12.3 Ambiguous Case

If the recovered path is eligible but the return decision remains ambiguous,
the case may be escalated to Resolver.

Resolver is not responsible for validation itself.
Resolver only arbitrates after validation is complete.

---

## 13. Telemetry Requirements

Recovery return depends on telemetry as evidence.

The following telemetry properties are especially important:

- confidence
- freshness
- stability-related variance
- trend
- source reliability

Old or low-confidence telemetry must not justify aggressive return.

---

## 14. Interaction with Routing Table

The Routing Table may expose:

- current selected path
- best path
- fallback path
- path_state = RECOVERY
- trust and policy requirements

RCU uses this information,
but recovery return logic remains in the decision layer.

---

## 15. Rules (Conceptual)

- RULE-15_RECOVERY_CANDIDATE
- RULE-16_RECOVERY_VALIDATION_START
- RULE-17_RECOVERY_VALIDATION_PASS
- RULE-18_RETURN_ELIGIBLE
- RULE-19_RETURN_SWITCH
- RULE-20_RETURN_KEEP
- RULE-21_RETURN_ESCALATE

Rule names are provisional and may be refined during implementation.

---

## 16. Out of Scope

This model does not yet define:

- weighted traffic redistribution
- probabilistic return
- multi-path partial share re-entry
- full recovery confidence scoring model

These are future extensions beyond the minimum v0.2 scope.

---

## 17. Summary

PSC RCU Recovery Return Model v0.2 extends the conservative recovery hold behavior of v0.1
by introducing staged re-entry for recovered paths.

Recovered paths are treated as candidates first,
validated second,
and considered for return only after controlled eligibility is established.

This preserves PSC’s stability-first design
while opening a path toward future recovery-aware and multi-path-capable control.
