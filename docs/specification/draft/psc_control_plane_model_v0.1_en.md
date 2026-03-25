# PSC Control Plane Model v0.1

## Document Information

- Document Name: PSC Control Plane Model
- Version: v0.1
- Project: PSC
- Layer: PSC Fabric
- Status: Draft
- Author: T. Hirose
- Language: English

---

## 1. Purpose

This document defines the responsibilities, control structure, component interactions, and fundamental control loop behavior of the PSC Fabric Control Plane.

In PSC, the Control Plane is not a standalone function, but a continuous control loop that observes Fabric state, evaluates conditions, applies control decisions, and re-observes the results.

This document specifically covers:

- Control structure for reacting to Fabric state changes
- Role separation of Resolver, RCU, TMU, and TEU
- Distinction between Local and Fabric-wide control
- Flow of trigger, decision, execution, and feedback

---

## 2. Scope

This document covers:

- Logical structure of the PSC Fabric Control Plane
- Responsibilities of major control components
- Flow of input, decision, execution, and reevaluation
- Role separation between Local and Fabric-wide control
- Relationship between Resolver and RCU

This document does not cover:

- Detailed routing algorithms
- Packet format definitions
- Physical implementation of transfer execution
- Telemetry message formats
- Bit-level definition of security policy fields

These are defined in separate specifications.

---

## 3. Design Principles

The PSC Control Plane shall follow the principles below.

### 3.1 Control Plane as a Control Loop

The Control Plane shall be implemented as a continuous control loop consisting of observation, evaluation, decision, execution, and feedback.

### 3.2 Separation of Responsibilities

Each component shall have clearly separated responsibilities:

- Resolver: higher-order decision and non-deterministic resolution
- RCU: route selection and switching decisions
- TMU: timing control, suppression, and reevaluation scheduling
- TEU: execution of transfer decisions
- Monitoring / Telemetry: state input and feedback

### 3.3 Event-driven Control

The Control Plane shall be event-driven.
Periodic reevaluation may be used to maintain stability.

### 3.4 Hierarchical Control Scope

The Control Plane shall distinguish between Local and Fabric-wide control.
Not all decisions shall be escalated to Fabric-wide scope.

### 3.5 Stability over Excessive Reactivity

The Control Plane shall prevent excessive reactions by applying hysteresis, hold-down time, and reevaluation thresholds.

---

## 4. Control Plane Overview

The PSC Control Plane is an integrated control system that observes Fabric state and adjusts routing, transfer behavior, and control policies accordingly.

It operates as the following control loop:

1. Receive state input
2. Evaluate state changes
3. Trigger Resolver or RCU when necessary
4. Apply timing control via TMU
5. Execute via TEU
6. Re-observe results via Telemetry
7. Repeat as necessary

This loop continuously operates during Fabric execution.

---

## 5. Functional Components

### 5.1 Resolver

The Resolver is a higher-order decision mechanism for resolving non-deterministic states. It is activated when the RCU cannot determine a valid decision or when exceptional conditions cannot be resolved by normal control.

The Resolver is responsible for:

- resolving competing policies
- deciding degraded mode transitions
- handling trust collapse scenarios
- handling policy violations
- resolving conditions not solvable by standard routing

The Resolver shall not operate as a continuous route computation engine.

---

### 5.2 Routing Control Unit (RCU)

The RCU is responsible for normal route selection and switching.

Responsibilities include:

- evaluation of available routes
- selection based on policy, trust, congestion, and stability
- maintenance of failover candidates
- route switching decisions
- re-selection upon route invalidation

The RCU handles time-critical decisions.

---

### 5.3 Transfer Management Unit (TMU)

The TMU manages temporal control.

Responsibilities include:

- trigger timing control
- hysteresis and hold-down
- retry and reevaluation timing
- periodic reevaluation scheduling
- escalation delay

The TMU shall function as a stability control mechanism, not just a timer.

---

### 5.4 Transfer Execution Unit (TEU)

The TEU executes Control Plane decisions in the Data Plane.

Responsibilities include:

- executing transfers based on selected routes
- reporting execution state
- notifying transfer failures
- feeding results back to the Control Plane

---

### 5.5 Monitoring and Telemetry

Monitoring / Telemetry provides input and feedback to the Control Plane.

Metrics may include:

- link utilization
- queue growth
- retransmissions
- credit starvation
- node reachability
- trust degradation
- policy violations
- latency growth
- error bursts
- fault notifications

---

## 6. Control Scope

### 6.1 Local Control

Control limited to a node or its immediate neighborhood.

Examples:

- link-level failover
- local congestion avoidance
- local rerouting
- port-level policy enforcement

---

### 6.2 Fabric-wide Control

Control based on global Fabric conditions.

Examples:

- global congestion response
- trust domain adjustments
- degraded mode transitions
- global routing policy changes

Fabric-wide control shall only be applied when necessary.

---

### 6.3 Scope Escalation

Escalation to Fabric-wide control may occur when:

- local control fails to stabilize the system
- multiple nodes are affected
- trust or policy conditions exceed local scope
- degraded mode is required

---

## 7. Trigger Conditions

Control processing shall be triggered under the following conditions:

- link down
- node unreachable
- severe congestion detection
- error burst detection
- trust collapse
- policy invalidation
- route score degradation
- transfer execution failure
- periodic reevaluation timer expiration

The Resolver shall be activated when the RCU cannot determine a valid decision.

Resolver activation conditions include:

- no route satisfies policy, trust, and reachability
- no policy-compliant route exists
- no trusted route exists
- multiple routes have equal evaluation and cannot be prioritized
- degraded mode transition is required
- the selected route repeatedly fails during execution

---

## 8. Control Loop Sequence

The Control Plane operates as follows:

1. Monitoring detects state changes
2. TMU determines processing timing
3. RCU performs route evaluation
4. Resolver performs higher-order decisions when required
5. TMU determines application timing
6. TEU executes the action
7. Results are fed back via Telemetry
8. The loop continues

---

## 9. Resolver and RCU Relationship

Resolver and RCU have distinct roles:

- RCU handles operational routing decisions
- Resolver handles exceptional and higher-order decisions

RCU shall be prioritized during normal operation.
Resolver shall only be invoked when necessary.

---

## 10. Stability Control

The Control Plane shall maintain stability using:

- hysteresis
- minimum hold time
- reevaluation interval
- switching suppression
- escalation thresholds
- recovery thresholds

Unnecessary route flapping must be avoided.

---

## 11. Failure Handling

The Control Plane shall handle:

- path invalidation
- repeated execution failure
- telemetry inconsistency
- unavailable trusted routes
- persistent congestion
- exhaustion of policy-compliant routes

Possible actions include:

- degraded mode transition
- fallback route selection
- route isolation
- temporary suppression
- resolver escalation

---

## 12. Future Extensions

Future extensions may include:

- multi-layer control hierarchy
- AI-assisted control
- predictive congestion handling
- regional coordination
- distributed control cooperation
- adaptive policy weighting

---

## 13. Summary

The PSC Control Plane is a continuous control loop that observes, evaluates, decides, executes, and re-evaluates Fabric behavior.

This model defines a structured separation of responsibilities across Resolver, RCU, TMU, TEU, and Monitoring, while connecting Local and Fabric-wide control into a unified architecture.

This specification establishes PSC Fabric as a self-regulating, fabric-centric distributed computer architecture.


