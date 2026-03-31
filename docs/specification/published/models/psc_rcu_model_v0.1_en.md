# PSC RCU Model v0.1

## Document Information

- Document Name : PSC Routing Control Unit Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSCOS (Control Layer)
- Document Type : Specification
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-03
- Last Updated  : 2026-03
- Language      : English

---

## 1. Purpose

This document defines the Routing Control Unit (RCU) Model in the PSC Fabric.

The RCU is responsible for:

- selecting optimal paths based on Routing Table and Telemetry states
- controlling path switching according to state changes

The RCU represents the **decision-making layer** of the PSC Fabric.

---

## 2. Scope

This model defines:

- RCU responsibilities
- input structures
- output structures
- decision pipeline
- path selection and switching logic

This document does NOT define:

- Routing Table structure
- Telemetry generation logic
- Resolver detailed specification
- physical data transfer mechanisms

---

## 3. Design Principles

### 3.1 Separation of Responsibilities

- Telemetry: state generation
- Routing Table: state storage
- RCU: decision making

### 3.2 Separation of Best vs Selected

RCU distinguishes between:

- Best Path: theoretically optimal path
- Selected Path: currently active path

This separation enables both stability and adaptability.

### 3.3 Stability over Aggressiveness

Frequent switching should be avoided. Stability is prioritized.

### 3.4 Explainability

All RCU decisions must be explainable.

---

## 4. RCU Inputs

The RCU receives the following inputs.

### 4.1 Routing Candidates (Routing Table)

```text
PathCandidate {
    path_id
    hops[]
    link_ids[]
    node_ids[]
    base_cost
    capacity
}
```

### 4.2 Telemetry Binding

```text
RoutingTelemetryBinding {
    target_id
    congestion_score
    health_state
    availability_state
    trust_score_ref
}
```

### 4.3 Routing Policy

```text
RoutingPolicy {
    mode                // latency / stability / trust
    hysteresis_margin
    trust_mode          // off / prefer / require
}
```

### 4.4 Transfer Request (TMU)

```text
TransferRequest {
    src
    dst
    class
    qos
    deadline
}
```

---

## 5. RCU Outputs

The RCU produces the following output.

```text
PathDecision {
    selected_path_id
    decision_type   // KEEP / SWITCH / DEGRADED_SWITCH / ESCALATE
    reason {
        type
        details
    }
}
```

---

## 6. Decision Pipeline

The RCU decision process consists of the following phases.

### 6.1 Phase 1: Candidate Filtering

Paths that are not eligible for routing are filtered out.

#### Availability Filter

- availability_state == UNAVAILABLE → reject
- availability_state == RESTRICTED → allow under degraded mode or policy constraints
- availability_state == AVAILABLE → allow

#### Trust Filter

- trust_mode == require → reject untrusted paths
- trust_mode == prefer → prefer trusted paths (no rejection)
- trust_mode == off → no filtering

### 6.2 Phase 2: Scoring

Each path is evaluated using at least the following components derived from telemetry and policy.

```text
total_cost =
    base_cost
  + congestion_penalty
  + trust_penalty
  + availability_penalty
```

### 6.3 Phase 3: Best Path Selection

The path with the lowest cost is selected as the Best Path.

### 6.4 Phase 4: Switching Decision

The Best Path is compared with the current Selected Path.

```text
if improvement > hysteresis_margin:
    SWITCH
else:
    KEEP
```

---

## 7. Decision Types

The RCU may produce the following decisions.

### 7.1 KEEP

Maintain the current path.

### 7.2 SWITCH

Switch to a better path.

### 7.3 DEGRADED_SWITCH

Switch to an alternative path under constrained conditions.

### 7.4 ESCALATE

Delegate the decision to the Resolver when RCU cannot determine a valid outcome.

---

## 8. Degraded Mode

RCU enters Degraded Mode under the following conditions:

- no valid paths are available
- paths are restricted by trust constraints
- overall performance degradation is observed

In Degraded Mode:

- constrained paths may be used
- maintaining connectivity is prioritized

---

## 9. Trust Handling

In RCU:

- trust is treated as a referenced input from telemetry
- behavior is controlled by trust_mode

Examples:

- off: ignore trust
- prefer: prioritize trusted paths
- require: enforce trust requirement

---

## 10. State Transition Considerations

RCU considers the following:

- hysteresis to prevent oscillation
- ignoring transient fluctuations
- conservative recovery decisions

---

## 11. Summary

The RCU Model:

- takes Telemetry and Routing Table as input
- evaluates candidate paths
- performs appropriate path selection and switching

It serves as the decision-making mechanism of the PSC Fabric.

The RCU enables:

- stability
- adaptability
- explainable routing behavior
