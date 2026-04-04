# Photon System Controller (PSC)

🇺🇸 English | 🇯🇵 日本語 → README_ja.md

A fabric-driven system that dynamically selects the most stable and trusted network path — not just the shortest one.

---

## Why PSC?

- Avoids unstable network paths automatically
- Prioritizes trust and stability over raw speed
- Adapts routing decisions in real time
- Moves decision-making into the network fabric

PSC is a **decision-driven routing system**, not just a data transport layer.

---

## Quick Demo

PSC provides two demo modes:

### 1. Static Demo (Basic Behavior)

Observe how PSC selects routes based on trust and cost.

**What you will see:**

- Basic trust-aware routing
- Stable path preference over shortest path

```bash
python3 sim/04_demo/run_psc_demo.py
```

---

### 2. Dynamic Demo (Adaptive Behavior)

Observe how PSC reacts to changing network conditions.

**What you will see:**

- Real-time routing adaptation
- Avoidance of unstable paths
- Trust-driven decision changes

```bash
python3 sim/04_demo/run_psc_dynamic_demo.py
```

---

## What is PSC?

PSC (Photon System Controller) is a fabric-centric computer architecture
that shifts system control and data movement away from traditional CPU-centric designs.

In PSC, the communication fabric itself becomes the core of coordination and data flow.

Instead of relying on a centralized controller,
PSC distributes decision-making across the fabric.

---

## Architecture Overview

PSC shifts system control from a centralized CPU to the communication fabric.

**Key idea:**

- Control is distributed across the fabric
- Data flow and decision-making are integrated

![PSC Architecture Concept](diagrams/concept/psc_concept_architecture_comparison_v0.1.png)

This diagram compares traditional CPU-centric architecture with PSC’s fabric-driven model.

---

### Resolver Control Model

This diagram shows how decision-making works inside PSC.

**Key behavior:**

- RCU operates autonomously under normal conditions
- Resolver intervenes only when escalation or override is required
- Decision control is separated from execution

![PSC Resolver Control Model](diagrams/control/psc_resolver_control_model_v0.1.png)

PSC is not just a data transport system —
it is a **decision-driven fabric architecture**.

---

## Transfer Flow

This diagram shows how data moves through the PSC fabric.

**What to focus on:**

- How data flows between components
- How routing decisions affect transfer behavior
- Interaction between control and execution layers

![PSC Transfer Flow](diagrams/fabric/psc_transfer_flow_v0.1.png)

---

## Fabric Internal Architecture

This diagram shows the internal structure of the PSC fabric.

**What to focus on:**

- Roles of each module (RCU, TMU, TEU, OMU)
- Separation of control and execution
- How components are connected inside the fabric

![PSC Fabric Internal Architecture](diagrams/fabric/psc_fabric_internal_architecture_v0.1.png)

---

## Core Architecture Components

PSC introduces dedicated control modules inside the fabric:

- Resolver (decision-control module)
- RCU (routing control unit)
- TMU (transfer management unit)
- TEU (transfer execution unit)
- OMU (optical monitoring unit)

Each component has a clearly defined role within the fabric.

The Resolver defines system-wide behavior,
while RCU operates autonomously under normal conditions.

---

## Documentation

Start here to understand PSC:

- [Architecture Overview](docs/architecture/psc_architecture_overview_en.md)
- [Architecture Map](docs/architecture/psc_architecture_map_v0.1_en.md)
- [Specification](docs/specification/)

---

## Specification

### Published Documents

- PSC AI Behavior Model v0.1

  - English: docs/specification/published/psc_ai_behavior_model_v0.1_en.md
  - Japanese: docs/specification/published/psc_ai_behavior_model_v0.1_ja.md

These documents represent stable and reference-level specifications.

---

### Draft Documents

- Routing Model
- Congestion Control Model

These are under active development and subject to change.

---

### Core Specification

- Resolver Specification v0.1
  → docs/specification/resolver/psc_resolver_spec_v0.1.md

The Resolver defines the decision-control model of PSC,
including state-based control, authority modes, and constraint-based outputs.

---

## Key Concepts

PSC is built around the following principles:

- Fabric-driven computer architecture
- Receiver-driven data transfer
- Chunk-based transport
- Congestion-aware routing
- Policy-aware routing
- Trust-aware routing
- Adaptive fabric control

---

## System Architecture

PSC introduces a communication fabric that connects:

- CPU
- GPU
- Memory
- Storage
- Network
- Accelerators

All communication flows through the PSC Fabric.

---

## Article

Read the concept:

[https://zenn.dev/takanori_psc/articles/73827700dc68a6](https://zenn.dev/takanori_psc/articles/73827700dc68a6)

---

## Project Status

PSC Fabric Specification v0.1 is currently under development.

---

## Author

T. Hirose
Independent architecture research project

---

## Contributing

Contributions, discussions, and ideas are welcome.

See `CONTRIBUTING.md`

---
