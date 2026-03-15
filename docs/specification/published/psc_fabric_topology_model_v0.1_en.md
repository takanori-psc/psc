# PSC Fabric Topology Model v0.1

## Document Information

- Document Name   : PSC Fabric Topology Model
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

This document defines the topology model of PSC Fabric.

The topology model describes how PSC nodes, switches, and links
can be organized across multiple scales,
from local rack-level systems to global-scale distributed environments.

The purpose of this document is to define:

- topology levels
- structural roles of each level
- connectivity principles
- scalability direction
- fault isolation boundaries

---

## 2. Scope

This document covers the following topology levels:

- Rack topology
- Cluster topology
- Floor topology
- Global topology

This document focuses on structural topology design.

It does not define:

- detailed routing algorithms
- packet format
- security protocol details
- physical connector implementation

These are defined in separate documents.

---

## 3. Design Principles

PSC Fabric topology is designed according to the following principles:

- hierarchical scalability
- local autonomy
- bounded fault domains
- incremental expansion
- policy-aware interconnection
- support for heterogeneous node populations

---

## 4. Topology Levels

### 4.1 Rack Topology

Rack topology is the smallest practical deployment unit of PSC Fabric.

A rack typically contains:

- compute nodes
- memory nodes
- storage nodes
- accelerator nodes (GPU, AI accelerators, FPGA, etc.)
- local PSC switching elements

Rack topology emphasizes:

- short-distance high-bandwidth links
- low-latency communication
- local traffic concentration
- fast fault containment

### 4.2 Cluster Topology

Cluster topology connects multiple racks into a larger coordination domain.

Cluster topology emphasizes:

- inter-rack communication
- shared resource access
- scalable routing coordination
- cluster-local policy enforcement

### 4.3 Floor Topology

Floor topology connects multiple clusters inside a larger physical site.

Floor topology emphasizes:

- larger fault-domain separation
- regional traffic aggregation
- scalable path diversity
- administrative segmentation

### 4.4 Global Topology

Global topology connects geographically distributed PSC domains.

Global topology emphasizes:

- long-distance federation
- inter-site policy control
- trust-aware connectivity
- bandwidth and latency diversity

---

## 5. Structural Model

PSC Fabric topology is not defined as a single fixed physical shape.

Instead, PSC supports multiple topology patterns depending on scale and deployment goals.

Examples include:

- star-like aggregation
- spine-leaf structures
- mesh-assisted structures
- hierarchical federation

The exact topology may vary by deployment level,
but all forms should preserve:

- clear control boundaries
- scalable expansion paths
- fault isolation structure
- routing consistency

---

## 6. Fault Domain Model

Each topology level should define its own fault containment boundary.

Examples:

- rack failure should not directly collapse cluster control
- cluster failure should not directly collapse floor-wide operation
- floor failure should not directly collapse global federation

Topology design should therefore support:

- isolation
- rerouting
- degradation handling
- partial survival operation

---

## 7. Policy and Security Considerations

Topology boundaries are also policy boundaries.

Different topology levels may apply different rules for:

- routing permission
- trust relationships
- resource visibility
- security filtering
- inter-domain transfer control

This allows PSC Fabric to scale
without requiring uniform trust across all nodes.

---

## 8. Future Extensions

Future versions of this document may define:

- recommended topology templates
- topology discovery model
- topology identifiers
- dynamic topology adaptation
- topology-aware routing hints

---

## 9. Summary

PSC Fabric topology is defined as a multi-level scalable structure
that spans:

- rack
- cluster
- floor
- global

This layered approach allows PSC to support
local efficiency, fault isolation, policy separation,
and long-range distributed expansion.
