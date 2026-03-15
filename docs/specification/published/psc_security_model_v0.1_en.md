# PSC Security Model v0.1

## Document Information

- Document Name   : PSC Security Model
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

This document defines the **Security Model** used in PSC Fabric.

The PSC Security Model provides a framework for evaluating and managing **trust and security conditions** across PSC Fabric.

Unlike traditional network security models that rely primarily on access control, PSC integrates **security evaluation directly into fabric behavior and routing decisions**.

The security model enables PSC Fabric to:

- evaluate node trustworthiness
- evaluate route trustworthiness
- detect abnormal or malicious behavior
- restrict unreliable fabric elements
- maintain overall fabric stability

---

## 2. Scope

This specification defines:

- the trust concept in PSC Fabric
- node trust evaluation
- route trust evaluation
- trust state representation
- interaction between security and routing systems

This document does not define:

- cryptographic protocols
- authentication mechanisms
- certificate infrastructures

These topics may be defined in separate specifications.

---

## 3. Design Principles

The PSC Security Model follows the principles below.

### 3.1 Trust-aware Fabric

PSC Fabric must consider **trust conditions** when making routing and control decisions.

Security evaluation becomes part of the overall fabric control process.

### 3.2 Behavior-based Evaluation

Trust evaluation should consider **observed behavior** rather than relying solely on static configuration.

### 3.3 Distributed Security

Security evaluation should operate in a **distributed manner** across PSC nodes.

Each node may independently evaluate trust conditions using local observations.

### 3.4 Stability Preservation

Security mechanisms must not destabilize the fabric.

Trust evaluation must operate in a controlled and predictable way.

---

## 4. Trust Concept

In PSC Fabric, **Trust represents the reliability and security condition of fabric components**.

Trust evaluation may apply to:

- nodes
- links
- routing paths
- fabric regions

Trust influences how PSC components interact with each other.

Lower trust levels may lead to restricted routing or complete isolation.

---

## 5. Trust Types

PSC defines two primary trust types.

| Trust Type  | Description                             |
|-------------|-----------------------------------------|
| Node Trust  | Trust evaluation of a specific PSC node |
| Route Trust | Trust evaluation of a routing path      |

Both trust types may influence routing and control behavior.

---

## 6. Trust Sources

Trust evaluation may use two sources of information.

| Source        | Description                                             |
|---------------|---------------------------------------------------------|
| Static Trust  | Trust defined by configuration or administrative policy |
| Dynamic Trust | Trust derived from runtime behavior observations        |

---

## 7. Trust State Model

PSC represents trust conditions using a simplified state model.

| Trust State | Description                     |
|-------------|---------------------------------|
| TRUSTED     | Highly trusted fabric component |
| NORMAL      | Standard trusted operation      |
| RESTRICTED  | Limited interaction permitted   |
| BLOCKED     | Fabric interaction prohibited   |

These states provide a simplified representation of trust conditions.

---

## 8. Node Trust Evaluation

Node trust may be influenced by factors such as:

- static administrative trust assignment
- node role and certification
- error rate anomalies
- abnormal traffic behavior
- telemetry inconsistencies
- repeated routing failures

Node trust evaluation may be performed locally by PSC nodes or by control components.

---

## 9. Route Trust Evaluation

Route trust evaluates the reliability of a path across PSC Fabric.

Route trust may depend on:

- trust level of intermediate nodes
- link stability
- error history
- routing anomalies
- suspicious traffic patterns

Routes passing through low-trust nodes may receive penalties or restrictions.

---

## 10. Trust Evaluation Process

Trust evaluation typically follows this flow.
```
Telemetry Observation
↓
Behavior Analysis
↓
Static Trust + Dynamic Trust
↓
Effective Trust State
```
Trust evaluation may occur continuously during fabric operation.

---

## 11. Interaction with Routing

Routing decisions may incorporate trust evaluation.

Typical routing decision inputs include:
```
Congestion State
+
Fabric State
+
Trust State
+
Policy
↓
Routing Decision
```

Routes containing low-trust elements may be avoided when possible.

---

## 12. Trust Recovery

Trust conditions may improve over time if abnormal behavior disappears.

Recovery mechanisms may include:

- observation stability periods
- decay of past anomaly penalties
- successful routing behavior

Trust recovery must be gradual to avoid oscillation.

---

## 13. Future Extensions

Future versions of the PSC Security Model may introduce:

- reputation systems
- anomaly detection algorithms
- AI-assisted trust evaluation
- inter-fabric trust exchange
- secure routing domains

---

## 14. Summary

The PSC Security Model defines a distributed trust-based security framework for PSC Fabric.

Key principles include:

- trust-aware routing
- behavior-based trust evaluation
- distributed security operation
- stable trust state representation

By integrating trust evaluation with routing and policy control, PSC Fabric can maintain reliable operation even in complex and dynamic environments.
