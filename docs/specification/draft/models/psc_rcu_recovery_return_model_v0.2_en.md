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

## 2. Objective

This document defines the staged recovery return behavior of PSC RCU.

While PSC RCU Decision Model v0.1 establishes conservative recovery hold behavior,
this model extends the decision process by introducing a controlled re-entry path
for recovered routes.

The goal is not immediate performance restoration.
The goal is stable and explainable re-admission of recovered paths.

---

## 3. Relationship to v0.1

This model does not replace v0.1 behavior.
It extends it.

### 3.1 v0.1 Behavior

In v0.1, PSC does not immediately return to a previously degraded path
even if that path later becomes the best-performing path again.

If the currently selected path remains stable and trusted,
PSC keeps the current path.

### 3.2 v0.2 Extension

v0.2 preserves the conservative design of v0.1,
but adds a staged re-entry mechanism.

Recovered paths are not immediately selected.
They must first pass validation before becoming eligible again.

---

## 4. Design Principles

### 4.1 Stability First

Recovery return must not undermine the stability achieved after failover.

### 4.2 Recovered Path != Immediately Reusable Path

A recovered path is treated as a candidate,
not as an immediate switch target.

### 4.3 Explainable Decision Process

Each recovery return decision must be traceable through explicit state transitions and rules.

### 4.4 Separation of Roles

- Routing Table : stores path state and candidate information
- Telemetry : provides evidence with confidence and freshness
- RCU : performs staged evaluation and return eligibility judgment
- Resolver : performs final arbitration only when ambiguity remains

---

## 5. Recovery Return State Model

The following additional recovery return states are introduced.

- RECOVERY_CANDIDATE
- VALIDATING
- RETURN_ELIGIBLE

These states are logical control states for the RCU decision process.

### 5.1 RECOVERY_CANDIDATE

A previously degraded or unavailable path has recovered
to a minimum acceptable condition.

### 5.2 VALIDATING

The recovered path is observed over a validation window.

### 5.3 RETURN_ELIGIBLE

The recovered path has passed validation
and may now be considered for selection.

Important:

RETURN_ELIGIBLE does not mean immediate switch.

---

## 6. Entry Conditions

A path may enter RECOVERY_CANDIDATE if all of the following conditions are satisfied:

- path was previously degraded, failed, limited, or excluded
- trust is above the recovery minimum threshold
- health is valid
- telemetry freshness is acceptable
- confidence is not below the minimum accepted level

---

## 7. Validation Conditions

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

## 8. Return Eligibility

A path becomes RETURN_ELIGIBLE only when the validation window is completed successfully.

Return eligibility means:

- the path may be reconsidered by RCU
- the path may compete again with the currently selected path
- the path may be submitted to Resolver if ambiguity exists

Return eligibility does not force selection.

---

## 9. Return Decision Policy

### 9.1 Basic Rule

If the currently selected path remains stable and trusted,
PSC does not switch back aggressively.

### 9.2 Controlled Return

A RETURN_ELIGIBLE path may be selected only if:

- the score improvement is meaningful
- return hysteresis conditions are satisfied
- stability risk is acceptable
- policy constraints permit re-entry

### 9.3 Ambiguous Case

If the recovered path is eligible but the return decision remains ambiguous,
the case may be escalated to Resolver.

Resolver is not responsible for validation itself.
Resolver only arbitrates after validation is complete.

---

## 10. Telemetry Requirements

Recovery return depends on telemetry as evidence.

The following telemetry properties are especially important:

- confidence
- freshness
- stability-related variance
- trend
- source reliability

Old or low-confidence telemetry must not justify aggressive return.

---

## 11. Interaction with Routing Table

The Routing Table may expose:

- current selected path
- best path
- fallback path
- path_state = RECOVERY
- trust and policy requirements

RCU uses this information,
but recovery return logic remains in the decision layer.

---

## 12. Rules (Conceptual)

- RULE-15_RECOVERY_CANDIDATE
- RULE-16_RECOVERY_VALIDATION_START
- RULE-17_RECOVERY_VALIDATION_PASS
- RULE-18_RETURN_ELIGIBLE
- RULE-19_RETURN_SWITCH
- RULE-20_RETURN_KEEP
- RULE-21_RETURN_ESCALATE

Rule names are provisional and may be refined during implementation.

---

## 13. Out of Scope

This model does not yet define:

- weighted traffic redistribution
- probabilistic return
- multi-path partial share re-entry
- full recovery confidence scoring model

These are future extensions beyond the minimum v0.2 scope.

---

## 14. Summary

PSC RCU Recovery Return Model v0.2 extends the conservative recovery hold behavior of v0.1
by introducing staged re-entry for recovered paths.

Recovered paths are treated as candidates first,
validated second,
and considered for return only after controlled eligibility is established.

This preserves PSC’s stability-first design
while opening a path toward future recovery-aware and multi-path-capable control.
