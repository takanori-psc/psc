# PSC Control Plane Model v0.1

## Document Information

- Document Name   : PSC Control Plane Model
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

This document defines the structure and role of the **Control Plane** within PSC Fabric.

PSC adopts a **fabric-centric distributed computer architecture** in which fabric state management, control policies, and routing adjustments are coordinated through the Control Plane.

The Control Plane Model defines:

- the basic structure of fabric control
- the role of Control Nodes
- the concept of control messages
- the relationship with fabric state
- the distributed control architecture

The purpose of this specification is to ensure **stability, adaptability, and scalability** of PSC Fabric control.

---

## 2. Scope

This document covers:

- the logical structure of the PSC Control Plane
- fundamental responsibilities of Control Nodes
- relationships between the Control Plane and Fabric State
- the concept of Control Messages

This document does **not** define:

- detailed control message formats
- routing algorithm details
- telemetry collection mechanisms
- congestion control algorithms

These topics are defined in separate specifications.

---

## 3. Design Principles

PSC Control Plane follows the design principles below.

### 3.1 Distributed Control

PSC Fabric adopts a **distributed control model**.

Control Nodes coordinate fabric behavior, but decisions are not entirely centralized.  
Individual nodes maintain a level of autonomy.

### 3.2 Fabric Stability

The Control Plane prioritizes **fabric stability**.

Control actions should avoid sudden large-scale changes and instead promote stable convergence of fabric behavior.

### 3.3 Policy-driven Control

Control decisions in PSC Fabric are guided by **Policy**.

Policies may define:

- routing behavior
- priority rules
- traffic management

### 3.4 Scalability

The Control Plane must scale from small PSC systems to very large fabric environments.

---

## 4. Control Plane Overview

PSC Fabric defines three major operational planes.

| Plane            | Role                   |
|------------------|------------------------|
| Data Plane       | Data transfer          |
| Control Plane    | Fabric control         |
| Management Plane | Operational management |

The Control Plane manages fabric behavior and state convergence.

---

## 5. Control Node Role

Control Nodes provide the control functionality of PSC Fabric.

Primary responsibilities include:

- fabric state monitoring
- routing policy management
- distribution of control information
- assisting fabric state convergence
- processing control messages

Control Nodes coordinate control behavior across the fabric.

---

## 6. Control Message Model

The Control Plane uses **Control Messages** to coordinate fabric control.

Examples include:

- Fabric State Updates
- Routing Updates
- Policy Distribution
- Congestion Notifications

Detailed message formats are defined in separate specifications.

---

## 7. Control Scope

Control Scope defines the hierarchical scope of control operations in PSC Fabric.

Control scope may apply to different levels depending on fabric size and control objectives.

Example scopes include:

- **Node-level**  
  Control applied to an individual node or local area.

- **Fabric Region**  
  Control applied to a group of nodes within a fabric region.

- **Fabric-wide**  
  Control applied across the entire fabric.

This hierarchical structure enables scalable control across small and large PSC deployments.

---

## 8. Control Loop

PSC Fabric control follows a control loop:

Observe  
↓  
Analyze  
↓  
Decide  
↓  
Distribute  
↓  
Converge  

This loop allows the fabric to adapt to changing system conditions.

---

## 9. Control Plane and Fabric State

The Control Plane operates closely with the **PSC Fabric State Model**.

Fabric state represents conditions such as:

- load levels
- fault conditions
- congestion states

The Control Plane observes these states and applies appropriate control policies.

---

## 10. Summary

The PSC Control Plane Model defines the control structure of PSC Fabric.

The Control Plane performs:

- fabric state observation
- control policy decisions
- control information distribution
- fabric state convergence

By adopting a distributed control model, PSC enables scalable and stable fabric management.
