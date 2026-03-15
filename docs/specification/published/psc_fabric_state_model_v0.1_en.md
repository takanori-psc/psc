# PSC Fabric State Model v0.1

## Document Information

- Document Name   : PSC Fabric State Model
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

This document defines the **Fabric State Model** used in PSC Fabric.

The Fabric State Model represents the operational condition of PSC Fabric using a **simple and stable state representation**.  
These states serve as a common foundation for several control mechanisms, including:

- routing decisions
- congestion control
- fabric monitoring
- control node policies
- telemetry interpretation
- optimization interaction

PSC does not rely solely on numerical optimization.  
Instead, PSC adopts a **state-based control model**.

This design enables PSC Fabric to achieve:

- stable system behavior
- simplified control logic
- easier interpretation of fabric conditions

---

## 2. State Philosophy

Internally, PSC Fabric processes a large number of numerical metrics.

Examples include:

- link utilization
- queue depth
- latency
- packet retries
- error rates
- thermal conditions

However, PSC control decisions do not directly operate on these raw numerical values.  
Instead, they are converted into **Fabric States**.

```
Telemetry Metrics
↓
State Evaluation
↓
Fabric State
↓
Routing / Control / Policy
```

Fabric State evaluation may be performed by:

- PSC Fabric Nodes
- Routing Control Units (RCU)
- Control Nodes

This allows PSC Fabric to operate without relying on centralized control, enabling **distributed and autonomous state evaluation**.

This design helps PSC to:

- avoid excessive numerical optimization
- maintain control stability
- keep implementations simple

---

## 3. Official Fabric State Levels

PSC Fabric defines the following **four official fabric states**.

| State     | Description                                         |
|-----------|-----------------------------------------------------|
| CALM      | Fabric is stable with low load                      |
| WARM      | Fabric is operating under normal load               |
| HOT       | Fabric is under high load or approaching congestion |
| EMERGENCY | Fabric is experiencing severe congestion or failure |

These states are used by mechanisms such as:

- routing decisions
- congestion avoidance
- control node actions

---

## 4. Fabric State Meaning

### 4.1 CALM

The **CALM** state indicates that the fabric is operating under **low load and stable conditions**.

Characteristics:

- low utilization
- minimal congestion
- stable latency

Routing generally prefers CALM paths.

### 4.2 WARM

The **WARM** state represents the **normal operational state** of the fabric.

Characteristics:

- moderate utilization
- normal latency
- stable throughput

Normal PSC Fabric operation is expected to remain within this state.

### 4.3 HOT

The **HOT** state indicates that the fabric is under **high load conditions**.

Characteristics:

- high utilization
- queue buildup
- risk of congestion

Routing should avoid HOT paths when possible.

### 4.4 EMERGENCY

The **EMERGENCY** state represents **severe congestion or failure conditions**.

Characteristics:

- severe congestion
- packet loss
- link failure impact

Routing should not use EMERGENCY paths unless absolutely necessary.

---

## 5. Link State

In addition to Fabric State, PSC also defines **link-level states**.

| State    | Description         |
|----------|---------------------|
| NORMAL   | Normal operation    |
| DEGRADED | Reduced performance |
| FAILED   | Link failure        |

Link State is used as an input for Fabric State evaluation.

---

## 6. Node State

PSC nodes may also have the following states.

| State      | Description                      |
|------------|----------------------------------|
| NORMAL     | Normal operation                 |
| OVERLOADED | Node is under high load          |
| ISOLATED   | Node is isolated from the fabric |
| FAILED     | Node failure                     |

Node State is also considered when evaluating Fabric State.

---

## 7. State Transition

Fabric State changes dynamically based on telemetry information.

State evaluation may occur at:

- link level
- node level
- fabric-wide level

Typical escalation transitions include:
```
CALM → WARM
WARM → HOT
HOT → EMERGENCY
```
Recovery transitions include:
```
EMERGENCY → HOT
HOT → WARM
WARM → CALM
```

State transitions should include **hysteresis** to prevent frequent oscillations and to maintain routing and control stability.

---

## 8. Routing Interaction

The Routing Control Unit (RCU) uses Fabric State as an input for path selection.

General path preference order:
```
CALM > WARM > HOT > EMERGENCY
```

Paths in EMERGENCY state should normally not be used.

If CALM or WARM alternatives exist, routing should avoid HOT paths whenever possible.

---

## 9. Control Node Interaction

Control Nodes monitor Fabric State and use it to make decisions such as:

- congestion mitigation
- policy adjustment
- topology management

Control Nodes do not directly modify Fabric State.  
Instead, they influence fabric behavior through policies and configuration.

---

## 10. AI Interaction

AI-enabled Control Nodes may internally use more detailed state classifications.

Examples may include:

- ACTIVE
- BUSY
- CRITICAL

However, any control decisions affecting PSC Fabric must first be translated into the **official Fabric State model (CALM/WARM/HOT/EMERGENCY)**.

This design ensures that PSC:

- avoids dependency on specific AI implementations
- maintains stable state interpretation
- preserves compatibility across different AI systems

---

## 11. Design Principles

The PSC Fabric State Model follows these principles:

- state-based control
- stable interpretation
- human readability
- AI compatibility
- implementation simplicity

Fabric State acts as the **common control language** of PSC Fabric.
