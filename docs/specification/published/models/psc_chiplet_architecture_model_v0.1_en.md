# PSC Chiplet Architecture Model v0.1

## Document Information

- Document Name : PSC Chiplet Architecture Model
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Hardware
- Document Type : Specification
- Status : Draft
- Author : T. Hirose
- Created : 2026-03
- Last Updated : 2026-08
- Language : English

---

## 1. Purpose

This document defines the chiplet architecture shared by PSC Endpoint, PSC
Switch, and PSC Fabric Core devices. PSC is designed as a scalable fabric
device composed of functional chiplets rather than a single monolithic chip.

---

## 2. Design Philosophy

### 2.1 Modular Architecture

Functions are separated into reusable chiplets shared across product models.

### 2.2 Scalable Fabric

Port count, processing capacity, and control-core count can scale through the
chiplet configuration.

### 2.3 Unified Device Architecture

PSC Endpoint, PSC Switch, and PSC Fabric Core use the same base chiplet
architecture. Product roles are formed through port roles, chiplet count, and
control-core count.

---

## 3. PSC Chiplet Structure

The base PSC package structure is:

```text
PSC Package
├ Switching Core Chiplet
├ Port Chiplet(s)
├ Telemetry / Security Chiplet
└ RISC-V Control Cluster
```

Each chiplet performs specialized functions and communicates through the
Internal Interconnect.

---

## 4. Chiplet Types

### 4.1 Switching Core Chiplet

The data-plane core is responsible for:

- fabric switching
- packet forwarding
- internal routing
- crossbar / NoC management

### 4.2 Port Chiplet

The Port Chiplet provides logical PSC Fabric port interfaces and is
responsible for:

- logical port control
- link-state management
- port-buffer management
- Telemetry
- fault detection
- configurable port-role management

Example port roles include:

- Fabric Port
- Endpoint Port
- Storage Port
- Trusted Port
- Restricted Port
- External Domain Port

This model does not require the Port Chiplet to contain the optical converter.
Electrical-to-optical conversion may be placed inside or outside the PSC
package.

### 4.3 Telemetry / Security Chiplet

This chiplet provides:

- fabric telemetry
- congestion monitoring
- security enforcement
- trust-evaluation support

### 4.4 RISC-V Control Cluster

The PSC control plane is responsible for:

- fabric initialization
- policy management
- security and trust management
- routing control
- telemetry aggregation
- fault management

The control-core count scales with the product model and chiplet configuration.

---

## 5. Internal Interconnect

Chiplets are connected through a low-latency, high-bandwidth Internal NoC or
chiplet fabric link. Protocol, lane configuration, bandwidth, and physical
implementation remain for implementation-specific design.

---

## 6. Port and Optical Interface Model

Optical connectivity is the baseline for PSC external, node, and Inter-System
Cross-Connect links. A "port" in this document represents a logical PSC Fabric
interface and its bandwidth unit; it does not select a specific optical
implementation.

Future physical implementation candidates include:

- Pluggable Optics
- Onboard Optics
- External Optical Engine connected through a short-reach electrical interface
- Co-Packaged Optics

Physical lane count, lane speed, modulation, wavelengths, Duplex mode, FEC,
connector, transceiver, reach, and optical power budget are not fixed. The
logical route structure is independent of the selected optical implementation.
Details may be defined by a future `PSC Optical Interface Model` candidate or
implementation-specific specifications.

When a product model such as the Fabric Switch Node uses "800 Gb/s per port,"
the value is a design assumption for one complete logical PSC port and does
not represent a single physical lane.

---

## 7. Product Model Scaling

PSC uses the shared chiplet architecture for multiple product models.

| Product Model | Primary Role |
|---------------|--------------|
| PSC Endpoint | Compute or local-node connection |
| PSC Switch | Rack / fabric switching |
| PSC Fabric Core | Cluster core fabric |

Product models primarily scale by:

- port count
- chiplet count
- control-core count
- configured port roles

A shared 32-port PSC chiplet can be used with different port roles for each
product model. The 32-port configuration is a logical port count and does not
fix a particular physical optical implementation.

### 7.1 PSC Switch Product Overview

PSC Switch is a product model based on the shared PSC chiplet architecture.
A PSC Fabric Switch Node consists of System A and System B. Each system uses a
32-port PSC Switch, for 64 ports across the node.

Per-system port allocation, the Inter-System Cross-Connect, external route
structure, route selection, and failure handling are defined in the
`PSC Fabric Switch Node Architecture Model v0.1`. The Fabric Switch Node uses
the RISC-V Control Cluster. The design remains under active development.

Related document:

- `docs/specification/published/models/psc_fabric_switch_node_architecture_model_v0.1_en.md`

### 7.2 CPU Node PSC Product Role Example

A CPU Node contains one shared 32-port PSC chiplet for each of System A and
System B.

The port roles of each PSC chip are:

- 8 ports: connection to the corresponding PSC Fabric Switch system
- 24 ports: connection to local nodes attached to the CPU Node

No Inter-System Cross-Connect ports like those in a Fabric Switch Node are
provided between PSC-A and PSC-B inside the CPU Node. Local nodes can connect
directly to both PSC-A and PSC-B, allowing the source side to select the
healthy system.

Local nodes are dedicated to that CPU Node. Anticipated examples are:

- GPU Node
- AI Long-Term Memory Node
- Storage Node

The healthy system is used if one PSC or one system link fails. Allocation of
the 24 local ports among node types is not yet fixed. The node types above are
non-normative configuration examples.

### 7.3 Rack-Level Horizontal Scaling

PSC product models can scale horizontally as multiple independent `PSC Compute
Groups` within a rack. One PSC Compute Group consists of one PSC Fabric Switch
Node, one corresponding CPU Node, and Local Nodes dedicated to that CPU Node.
A Fabric Switch Node represents one PSC Compute Group, not the entire rack.

The `PSC Fabric Switch Node Architecture Model v0.1` addresses rack-level
group-count candidates, inter-group communication, failure-domain treatment,
and capacity scaling.

---

## 8. Future Extension

Future candidates include:

- high-density Port Chiplets
- AI-assisted fabric control
- distributed control models
- advanced security functions
- product-specific chiplet-count and control-core scaling
- detailed optical-interface and implementation-specific specifications
