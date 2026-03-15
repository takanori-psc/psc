# PSC Congestion Control Model v0.1

## Document Information

- Document Name   : PSC Congestion Control Model
- Version         : v0.1
- Project         : PSC / Photon System Controller
- Layer           : PSC Fabric
- Document Type   : Specification
- Status          : Draft
- Author          : T. Hirose
- Created         : 2026-03
- Last Updated    : 2026-03
- Language        : English

---

## 1. Purpose

This document defines the **Congestion Control Model** of PSC Fabric.

The Congestion Control Model specifies how PSC detects, represents, signals, and mitigates congestion inside the fabric in order to maintain:

- stable packet transfer
- predictable latency behavior
- fair resource usage
- routing adaptability
- overall fabric reliability

This model defines the **logical congestion handling framework** used by PSC nodes and control elements.

---

## 2. Scope

This specification covers the following aspects of congestion control:

- congestion detection
- congestion state representation
- congestion signaling
- routing adaptation under congestion
- flow control mechanisms
- fabric stability mechanisms

This document does not define:

- detailed security behaviors
- traffic policy enforcement
- fabric management operations

These topics are defined in separate specifications.

---

## 3. Design Goals

The PSC Congestion Control Model is designed with the following goals.

### 3.1 Fabric Stability

Congestion control must prioritize **fabric stability** over maximum short-term throughput.

### 3.2 Distributed Operation

PSC Fabric operates in a **distributed autonomous environment**, therefore congestion handling must not depend on centralized control.

### 3.3 Local-first Reaction

Nodes should primarily react to **locally observable conditions** while contributing to overall fabric stability.

### 3.4 Routing Cooperation

Congestion control must cooperate with the PSC routing system so that routing decisions can avoid overloaded paths.

### 3.5 Lightweight Signaling

Congestion signaling should remain compact and efficient to avoid unnecessary control overhead.

### 3.6 Oscillation Avoidance

The system must prevent route oscillation and unstable feedback loops by using hysteresis and damping mechanisms.

---

## 4. Congestion Concept

PSC treats congestion as a **fabric-level condition**, not only a per-port queue overflow event.

Congestion occurs when the traffic demand exceeds the sustainable forwarding or delivery capacity of some part of the fabric.

Possible causes include:

- output port contention
- path concentration
- destination-side limitations
- internal node resource limitations
- fault-induced traffic redirection

PSC congestion control is based on the following principles:

- detect congestion early
- represent congestion with stable states
- propagate congestion information in a limited scope
- adapt routing gradually
- reduce offered load when necessary
- recover conservatively

---

## 5. Congestion Observation Points

Congestion may be detected at several locations within a PSC node.

### 5.1 Port-level Observation

A port may observe congestion through:

- output queue growth
- repeated transmission deferral
- link utilization saturation
- reduced forwarding completion rate

### 5.2 Path-level Observation

Routing elements may infer congestion from:

- repeated downstream congestion reports
- increasing path latency
- route performance degradation
- packet accumulation trends

### 5.3 Node-level Observation

A node may detect internal congestion through:

- internal buffer pressure
- transfer scheduling backlog
- delayed execution in transfer engines
- internal resource exhaustion

### 5.4 Destination-side Observation

A receiver node may signal congestion when:

- receive buffers approach exhaustion
- storage commit capacity is insufficient
- processing capacity is temporarily reduced

---

## 6. Congestion State Model

PSC uses a simplified multi-level congestion state model.

### 6.1 Congestion States

Each observation point classifies congestion into one of the following states:

- **NORMAL**

  No congestion is observed.

- **WATCH**

  Early signs of pressure are detected but system operation remains stable.

- **CONGESTED**

  Congestion is affecting forwarding or delivery efficiency.

- **SEVERE**

  Congestion causes significant performance degradation and requires strong mitigation.

### 6.2 State Philosophy

PSC uses **state-based congestion classification** instead of relying purely on numerical optimization.

This simplifies routing and control decisions and improves system stability.

### 6.3 State Transition Principles

State transitions should follow the following rules:

- escalation requires persistent pressure
- recovery requires stronger evidence than escalation
- severe state requires sustained overload conditions

---

## 7. Congestion Indicators

Congestion state decisions may be derived from one or more indicators.

### 7.1 Primary Indicators

Typical primary indicators include:

- queue occupancy ratio
- queue growth rate
- transmission stall duration
- forwarding delay
- retry frequency
- buffer pressure

### 7.2 Secondary Indicators

Secondary indicators may include:

- downstream congestion reports
- route imbalance trends
- latency variation
- destination backpressure signals

### 7.3 Composite Evaluation

PSC implementations may combine multiple indicators into a composite congestion evaluation.

The result must be mapped into the congestion state model defined in this document.

---

## 8. Congestion Signaling

Congestion information must be communicated between nodes in a controlled manner.

### 8.1 Signaling Purpose

Congestion signaling enables:

- upstream awareness of downstream pressure
- adaptive routing decisions
- traffic moderation
- fabric-wide stability

### 8.2 Signaling Characteristics

Congestion signaling should be:

- compact
- event-driven or periodic
- rate-limited
- suppressible when unchanged
- locally scoped when possible

### 8.3 Signaling Scope

Congestion information may be propagated to:

- upstream neighboring nodes
- routing control logic
- control-plane elements
- telemetry systems

### 8.4 Signaling Granularity

Congestion may be reported at the following levels:

- port level
- link level
- path level
- node level
- destination or service level

---

## 9. Routing Response to Congestion

Routing must cooperate with congestion control.

### 9.1 Basic Routing Reaction

Routing systems may respond to congestion by:

- reducing preference for congested paths
- selecting alternate routes
- distributing traffic across multiple paths
- temporarily avoiding unstable routes

### 9.2 Gradual Adaptation

Routing changes should occur gradually to avoid instability.

Large synchronized rerouting events should be avoided.

### 9.3 Path Penalty

Congested routes may receive temporary penalties in the routing evaluation process.

Penalty magnitude may depend on:

- congestion severity
- persistence duration
- downstream reports

### 9.4 Recovery Behavior

Recovery of routing preference should occur slowly and conservatively.

---

## 10. Flow Control Strategy

Routing adaptation alone may not be sufficient.

PSC supports flow moderation mechanisms.

### 10.1 Flow Control Purpose

Flow control prevents overload propagation across the fabric.

### 10.2 Flow Control Actions

Possible actions include:

- pacing transfer requests
- limiting outstanding transfers
- reducing burst sizes
- delaying non-critical traffic
- prioritizing control traffic

### 10.3 Receiver-aware Behavior

Because PSC follows a receiver-driven transfer concept, flow control may incorporate destination-side readiness signals.

### 10.4 Control Traffic Protection

Essential control traffic must be protected from starvation even during congestion.

---

## 11. Stability Mechanisms

PSC congestion control includes stability mechanisms to prevent oscillation.

### 11.1 Hysteresis

Different thresholds should be used for escalation and recovery.

### 11.2 Persistence Timers

State transitions should require minimum persistence durations.

### 11.3 Rate Limiting

Congestion signaling and routing adjustments must be rate-limited.

### 11.4 Damping

After a mitigation action, the system should wait for observation feedback before applying further reactions.

### 11.5 Local-first Mitigation

Mitigation actions should begin locally whenever possible.

---

## 12. Relationship with Other PSC Models

The Congestion Control Model interacts with the following PSC specifications:

- PSC Fabric State Model
- PSC Routing Model
- PSC Routing Table Model
- PSC Routing Algorithm
- PSC Routing Decision Pipeline
- PSC Control Plane Model
- PSC Telemetry Model

---

## 13. Future Extensions

Future versions may introduce:

- numeric threshold reference models
- class-based congestion handling
- policy-aware congestion control
- fairness mechanisms
- admission control
- hierarchical congestion domains
- multi-fabric congestion coordination

---

## 14. Summary

The PSC Congestion Control Model defines a distributed congestion handling framework for PSC Fabric.

Key principles include:

- early detection
- state-based congestion representation
- controlled signaling
- routing cooperation
- adaptive flow control
- hysteresis-based recovery

These mechanisms allow PSC Fabric to maintain stable operation under varying traffic conditions without relying on centralized control.
