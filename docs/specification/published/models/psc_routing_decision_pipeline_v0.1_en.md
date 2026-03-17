# PSC Routing Decision Pipeline v0.1

## Document Information

- Document Name   : PSC Routing Decision Pipeline
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

This document defines the Routing Decision Pipeline in the PSC Fabric.

The Routing Decision Pipeline describes the decision process used by the
RCU (Routing Control Unit) when selecting a data transfer route.

Routing in PSC is not limited to simple shortest-path selection.
Instead, it is designed as a multi-stage decision model that considers:

- Fabric state
- Congestion conditions
- Policy constraints
- Security requirements
- Reliability considerations

This specification defines:

- Routing decision inputs
- Decision pipeline stages
- Route evaluation
- Final route selection

---

## 2. Scope

This specification covers the following:

Included:

- Routing decisions within the PSC Fabric
- Route selection processing performed by the RCU

Excluded:

- Routing Table structure (PSC Routing Table Model)
- Detailed routing algorithms
- Congestion control mechanisms

These topics are defined in separate specifications.

---

## 3. Routing Decision Concept

Routing decisions in PSC are executed through a multi-stage evaluation pipeline.

Basic structure:
```
Packet / Transfer Request
        ↓
Routing Context Construction
        ↓
Policy Evaluation
        ↓
Security Validation
        ↓
Congestion Evaluation
        ↓
Routing Table Lookup
        ↓
Route Scoring
        ↓
Final Route Selection
```
This structure enables PSC to achieve:

- Flexible routing control
- Adaptation to fabric conditions
- Integrated control of policy, trust, and congestion

---

## 4. Decision Inputs

The Routing Decision Pipeline uses the following information as input.

### 4.1 Packet Information

Packet header information:

- Destination Address
- Source Address
- Packet Type
- Transfer Class
- Priority

### 4.2 Routing Context

Before making a routing decision, the RCU constructs a Routing Context.

The Routing Context includes:

- Destination Node
- Source Node
- Current Node
- Transfer Type
- Priority Level

### 4.3 Fabric State

Fabric state information:

- Fabric Load
- Link State
- Node State
- Failure Status

This information is obtained through the Telemetry Model.

### 4.4 Policy Information

Control information defined by the Policy Model.

Examples include:

- Allowed nodes
- Forbidden nodes
- Preferred routes
- QoS policies

### 4.5 Security Information

Information defined by the Security Model.

Examples include:

- Trust Level
- Node Authentication
- Security Domain

---

## 5. Decision Pipeline Stages

The Routing Decision Pipeline processes routing decisions through the following stages.

### 5.1 Routing Context Construction

The RCU constructs the Routing Context from packet information.

This stage organizes information such as:

- Destination

- Transfer type

- Priority

### 5.2 Policy Evaluation

Policy control is applied by the Policy Engine.

Examples:

- Removing prohibited routes
- Enforcing preferred routes
- Applying QoS policies

### 5.3 Security Validation

Security checks are performed based on the Security Model, including:

- Trust domains
- Security policies
- Access control rules

Invalid or unauthorized routes are excluded.

### 5.4 Congestion Evaluation

Fabric telemetry is referenced to evaluate congestion conditions.

Evaluation targets:

- Link load
- Node load
- Queue depth

Highly congested routes may receive lower priority.

### 5.5 Routing Table Lookup

The Routing Table is consulted to obtain a set of candidate routes.

Based on the Routing Table Model, the following information is retrieved:

- Next hop
- Path cost
- Route attributes

### 5.6 Route Scoring

Each candidate route is evaluated through a scoring process.

Example evaluation factors:

- Path cost
- Congestion level
- Policy priority
- Trust level
- Reliability

Scores are calculated using the scoring method defined in the Routing Algorithm.

### 5.7 Final Route Selection

The optimal route is selected based on the scoring results.

Possible selection methods include:

- Best score selection
- Weighted random selection
- Load distribution

The final Next Hop is determined in this stage.
The selected Next Hop is forwarded to the transfer execution layer.

---

## 6. Interaction with Fabric Control

The Routing Decision Pipeline interacts with Fabric Control mechanisms.

Related modules include:

- Fabric State Model
- Congestion Control Model
- Telemetry Model
- Policy Model
- Security Model

By integrating information from these modules, PSC achieves
adaptive routing control.

---

## 7. Fault Handling

When failures occur, such as:

- Link failure
- Node failure
- Fabric partition

the RCU performs:

- Removal of affected routes
- Selection of alternative routes
- Routing Table updates

---

## 8. Future Extension

Future extensions may include:

- AI / learning-based routing
- Dynamic policy adaptation
- Predictive congestion avoidance
- Multi-path routing optimization
