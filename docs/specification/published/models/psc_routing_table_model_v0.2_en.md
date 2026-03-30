# PSC Routing Table Model v0.2

## Document Information

- Document Name: PSC Routing Table Model
- Version : v0.2
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane
- Document Type : Model Specification
- Status : Review
- Author : T. Hirose
- Created : 2026-03
- Last Updated : 2026-03
- Language : English

---

## 1. Overview

This document defines the **routing table model** used by the RCU (Routing Control Unit) in PSC Fabric.

This model integrates:

- multi-path structure
- policy / trust / congestion
- path state management (failover / degraded / recovery)
- explainable and reproducible routing decisions

---

## 2. Design Principles

### 2.1 Receiver-driven Routing

Routing decisions are controlled by the Fabric (RCU), not by the sender.

### 2.2 Explainable Decision Model

Routing decisions must be explainable and reproducible.

### 2.3 Multi-dimensional Evaluation

Routing evaluation integrates:

- topology
- congestion
- trust
- policy
- stability

### 2.4 Separation of Roles

- Routing Table : data storage
- RCU : decision making
- Resolver : exception handling

---

## 3. Data Model

PSC Routing Table adopts a two-layer structure:

```
Routing Table
 ├─ Destination Entry
 │   ├─ Path Entry
 │   ├─ Path Entry
 │   └─ Path Entry
```

---

## 4. Destination Entry

### 4.1 Overview

A Destination Entry represents aggregated routing information per destination.

### 4.2 Fields

- destination_id

- destination_prefix

- address_type

- reachable

- selected_path_id

- best_path_id

- fallback_path_id

- policy_profile

- trust_requirement

- entry_version

- last_updated

### 4.3 Description

- selected_path_id
  Currently active path

- best_path_id
  Best evaluated path

- fallback_path_id
  Failover candidate

### 4.4 policy_profile

Examples:

- latency
- stability
- trusted
- bulk

### 4.5 trust_requirement

Examples:

- off
- prefer_trusted
- require_trusted

---

## 5. Path Entry

### 5.1 Overview

A Path Entry represents an individual candidate route.

### 5.2 Identification

- path_id
- destination_id
- next_hop_port
- next_hop_node
- hop_count
- hop_list

### 5.3 Cost / Evaluation

- base_cost
- dynamic_cost
- total_score

Note:
Evaluation formula is defined in separate specifications
(Congestion Model / Policy Model / RCU Specification).

### 5.4 Trust

- trust_level
- trust_score

### 5.5 Congestion

- congestion_score

Represents congestion condition derived from telemetry.

### 5.6 State

- health_state
- availability_state
- path_state

#### health_state

- NORMAL
- WARNING
- CONGESTED
- DEGRADED
- FAILED

#### availability_state

- AVAILABLE
- LIMITED
- UNAVAILABLE

#### path_state

- SETUP
- ACTIVE
- STANDBY
- FAILOVER
- RECOVERY
- TEARDOWN

### 5.7 Performance Estimates

- bandwidth_estimate
- latency_estimate
- loss_estimate

### 5.8 Policy

- policy_flags

Examples:

- LOW_LATENCY
- STABILITY
- TRUST_REQUIRED
- BULK_TRANSFER
- SECURITY_RESTRICTED

### 5.9 Operational Flags

- is_selected
- is_backup
- valid_until
- last_evaluated

---

## 6. Routing Table Behavior

### 6.1 Route Selection

The routing table does not perform selection.
RCU performs decision making.

### 6.2 Best vs Selected

- best_path : optimal by evaluation
- selected_path : currently in use

### 6.3 Failover

When selected_path becomes unavailable:

- fallback_path
- or a degraded path

is used.

### 6.4 Degraded Operation

The system may allow:

- reduced trust
- reduced bandwidth
- increased latency

to maintain connectivity.

---

## 7. Interaction with RCU

RCU performs:

- path evaluation
- best path computation
- selected path control
- failover / recovery

---

## 8. Interaction with Resolver

Resolver intervenes when:

- no trusted path exists
- policy conflicts occur
- degraded continuation must be evaluated
- multiple decision criteria conflict

---

## 9. Indexing

### Primary

- destination_id

### Secondary

- next_hop_port
- path_state
- trust_level
- policy_flags

---

## 10. Lifecycle

- Creation (topology discovery / configuration)
- Update (telemetry / congestion / policy)
- Invalidation (failure / restriction)
- Removal (expiration / cleanup)

---

## 11. Example

### Destination Entry

```YAML
Destination Entry:
  destination_id: dst_mem_0042
  selected_path_id: path_02
  best_path_id: path_01
  fallback_path_id: path_03
  policy_profile: stability
  trust_requirement: prefer_trusted
```

---

### Path Entry

```YAML
Path Entry:
  path_id: path_02
  next_hop_port: port_3
  next_hop_node: node_07
  hop_count: 4

  base_cost: 12
  dynamic_cost: 5
  total_score: 17

  trust_level: TRUSTED
  congestion_score: 3

  health_state: NORMAL
  availability_state: AVAILABLE
  path_state: ACTIVE

  is_selected: true
```

---

## 12. Design Considerations

### 12.1 Logical vs Physical Separation

Logical routing (Port-based) is separated from physical routing (Node-based).

### 12.2 Scalability

Destination / Path separation enables scalable routing design.

### 12.3 Extensibility

Additional evaluation dimensions (AI, telemetry, optical characteristics) can be integrated.

---

## 13. Future Work

- Congestion Model integration
- Telemetry Model definition
- RCU evaluation function definition
- Hardware-optimized representation

---

## 14. Summary

PSC Routing Table Model v0.2 defines:

- Destination / Path two-layer structure
- multi-path routing
- policy / trust / congestion integration
- failover / degraded handling

This model serves as the core foundation of PSC routing behavior and control-plane decision logic.
