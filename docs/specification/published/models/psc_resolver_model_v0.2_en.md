# PSC Resolver Model v0.2

## Document Information

- Document Name : PSC Resolver Model
- Version       : v0.2
- Project       : PSC / Photon System Controller
- Layer         : PSCOS (Control Layer)
- Document Type : Specification
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-03
- Last Updated  : 2026-04
- Language      : English

---

## 1. Purpose

This document defines the Resolver Model in the PSC Fabric.

The Resolver performs higher-level decision making when the RCU decision is insufficient for final decision making.

The Resolver is responsible for:

- handling exceptional routing decisions beyond RCU capability
- resolving conflicts across multiple conditions
- determining degraded fallback usage
- integrating policy, trust, and recovery conditions

The Resolver represents the **higher-level decision layer** of the PSC Fabric.

---

## 2. Scope

This model defines:

- Resolver responsibilities
- invocation conditions
- input structures
- output structures
- decision targets
- relationship between Resolver and RCU

This document does NOT define:

- RCU normal routing logic
- Routing Table structure
- Telemetry generation mechanisms
- physical data transfer
- AI inference implementation details

---

## 3. Design Principles

### 3.1 Separation of Responsibilities

- Telemetry: state generation
- Routing Table: state storage
- RCU: normal decision making
- Resolver: higher-level decision making

The Resolver does not replace RCU.
It is invoked when the RCU decision is insufficient for final decision making.

This includes cases where:

- RCU cannot determine a valid decision
- the RCU tentative decision is ambiguous
- multiple evaluation criteria are in conflict

The Resolver performs arbitration to produce the final decision.

### 3.2 Exceptional Invocation

The Resolver is not continuously active and is invoked only when necessary.

### 3.3 Multi-factor Decision

The Resolver integrates multiple factors:

- congestion
- health
- availability
- trust
- policy
- recovery condition

### 3.4 Explainability

All Resolver decisions must be explainable, with rationale provided.

---

## 4. Resolver Invocation Conditions

The Resolver is invoked under the following conditions.

### 4.1 No Valid Path

RCU cannot select a valid path.

Examples:

- all candidates are UNAVAILABLE
- trust_mode=require eliminates all candidates
- no degraded candidates exist

### 4.2 Policy Conflict

Multiple policy constraints conflict, and RCU cannot resolve them using simple scoring.

Examples:

- latency vs trust priority conflict
- stability vs failover urgency conflict

### 4.3 Ambiguous or Conflicting Candidate Set

The Resolver is invoked when candidate evaluation is ambiguous or conflicting.

Typical conditions include:

- `score_gap < epsilon`
- significant trust difference between candidates
- significant stability difference between candidates
- divergence between recovery-oriented selection and baseline evaluation

Examples:

- `return_score` selects one candidate while `final_score` prefers another
- candidates are close in baseline score but differ in trust
- candidates are close in baseline score but differ in stability

### 4.4 Degraded Fallback Decision

Decision is required on whether RESTRICTED or trust-constrained paths should be used.

### 4.5 Recovery Return Arbitration

The Resolver is invoked when a recovery candidate has become eligible, but final switching remains ambiguous.

This includes cases where:

- `RETURN_ELIGIBLE` has been reached
- the recovery-oriented selector identifies a return candidate
- the baseline evaluator prefers a different candidate
- trust / stability conflict remains unresolved by RCU alone

---

## 5. Resolver Inputs

The Resolver receives the following inputs.

### 5.1 Transfer Request

```text
TransferRequest {
    src
    dst
    class
    qos
    deadline
}
```

### 5.2 Candidate Paths

```text
ResolverCandidatePath {
    path_id
    hops[]
    link_ids[]
    node_ids[]
    base_cost
    estimated_cost
    current_rank
}
```

### 5.3 Telemetry Summary

```text
ResolverTelemetrySummary {
    congestion_score
    health_state
    availability_state
    trust_score_ref
    scope_level
    confidence
}
```

### 5.4 Routing Policy

```text
ResolverPolicyContext {
    mode
    hysteresis_margin
    trust_mode
    degraded_mode_allowed
    recovery_preference
}
```

### 5.5 RCU Context

```text
ResolverRCUContext {
    selected_path_id
    best_path_id
    tentative_decision
    escalation_reason
}
```

---

## 6. Resolver Outputs

The Resolver produces the following output.

```text
ResolverDecision {
    final_decision_type   // ResolverDecisionType
    selected_path_id
    rationale {
        type
        details
    }
    override_policy {
        degraded_mode
        trust_exception
        recovery_hold
    }
}
```

---

## 7. Decision Targets

The Resolver evaluates the following decision targets.

### 7.1 Path Selection Override

Determine whether to override the RCU tentative decision and select a different path.

### 7.2 Degraded Path Approval

Determine whether restricted or constrained paths should be allowed.

### 7.3 No-route Determination

Determine whether no valid route exists and routing should fail.

### 7.4 Recovery Hold / Return Arbitration

Determine whether a validated recovery candidate should actually be selected,
or whether the current path should be maintained.

This target assumes:

- `RETURN_ELIGIBLE ≠ RETURN_SWITCH`
- final return decision may require Resolver arbitration

---

## 8. Resolver Decision Types

The Resolver defines the following decision types.

```text
ResolverDecisionType {
    KEEP
    SWITCH
    DEGRADED_SWITCH
    NO_ROUTE
    HOLD
    RETURN
}
```

### 8.1 Decision Type Definitions

#### KEEP

Maintain the current selected path.

#### SWITCH

Switch to a more appropriate path.

#### DEGRADED_SWITCH

Switch to a constrained path (RESTRICTED or trust-constrained).

#### NO_ROUTE

Determine that no valid path exists.

#### HOLD

Maintain the current state temporarily when recovery is uncertain.

#### RETURN

Return to the original path after recovery is confirmed.

---

## 9. Decision Model

The Resolver determines the final decision through the following steps.

### 9.1 Validate Escalation Reason

Validate the escalation reason from RCU.

- No valid path
- Policy conflict
- Ambiguous candidate
- Degraded decision required
- Recovery decision required

The reason determines the evaluation mode.

### 9.2 Re-evaluate Candidate Set

Re-evaluate candidate paths based on:

- availability_state
- trust constraints
- degraded allowance
- recovery condition
- telemetry confidence

### 9.3 Detect Ambiguity / Conflict

Determine whether the tentative RCU result is insufficient for final decision making.

Typical indicators include:

- small `score_gap`
- large `trust_gap`
- large `stability_gap`
- divergence between baseline evaluation and recovery-oriented selection

If ambiguity or conflict is detected, Resolver proceeds to arbitration.

### 9.4 Apply Policy Resolution

Resolve policy conflicts and determine priorities.

Examples:

- trust priority
- latency priority
- stability priority
- connectivity priority

Adjustments may include:

- allowing degraded mode
- relaxing trust constraints
- delaying recovery

### 9.5 Determine Final Action

Select one of the ResolverDecisionType values.

### 9.6 Output Construction

Construct the final decision output.

```text
ResolverDecision {
    final_decision_type   // ResolverDecisionType
    selected_path_id
    rationale {
        type
        details
    }
    override_policy {
        degraded_mode
        trust_exception
        recovery_hold
    }
}
```

---

## 10. Trust and Policy Handling

The Resolver treats trust and policy not only as penalties, but as final constraints.

Examples:

- strict enforcement of trust_mode=require
- allowing trust exceptions in degraded mode
- policy override for high-priority transfers
- stability prioritization during recovery

---

## 11. Recovery Considerations

The Resolver does not enforce immediate return upon recovery.

In particular:

- `RETURN_ELIGIBLE` does not guarantee `RETURN`
- recovery validation and final switching are separate phases
- final return may be overridden by conflict arbitration

---

## 12. Explainability Requirements

The Resolver must explain:

- why RCU decision was insufficient
- why the selected path was chosen
- why degraded paths were allowed
- why recovery was held or executed

---

## 13. Summary

The Resolver Model:

- receives escalated decisions from RCU
- integrates policy, trust, telemetry, and recovery conditions
- produces final high-level routing decisions

The Resolver enables:

- fast normal decisions (RCU)
- advanced exceptional decisions (Resolver)

---

## 14. Resolver Arbitration Extension (v0.2.x)

The Resolver role is extended from exceptional failure handling to ambiguity and conflict arbitration.

This extension is validated in the following cases:

- single-candidate recovery return
- multi-candidate recovery selection
- divergence between `return_score` and `final_score`

Core principle:

```text
RCU tentative decision ≠ Resolver final decision
```

Related recovery principle:

```text
RETURN_ELIGIBLE ≠ RETURN_SWITCH
RETURN_SWITCH ≠ FINAL_DECISION
```
---