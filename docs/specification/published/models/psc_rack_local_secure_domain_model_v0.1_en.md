# PSC Rack-local Secure Domain Model v0.1

## Document Information

- Document Name : PSC Rack-local Secure Domain Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSCOS (Control Layer)
- Document Type : Specification
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-04
- Last Updated  : 2026-04
- Language      : English

---

## Overview

This document defines the Rack-local Secure Domain in PSC.

The model provides a restricted high-speed communication domain within a single rack, balancing performance and isolation.

Communication that exits the rack-local domain or traverses boundary nodes is not eligible for this model and must return to standard PSC policy evaluation.

This model also improves latency stability by restricting communication
to deterministic single-hop paths, minimizing latency variance (jitter).

---

## Scope

This model applies to the following nodes:

- CPU nodes within the same rack
- Nodes directly attached to those CPU nodes:
  - Memory nodes
  - GPU nodes
  - Storage nodes

---

## Out of Scope

The following communications are not eligible:

- Communication with nodes outside the rack
- Communication traversing Switch Nodes
- Communication passing through Boundary Nodes (IO nodes)
- Multi-hop communication involving one or more intermediate nodes
  beyond direct CPU-adjacent connections

---

## Definition

The Rack-local Secure Domain is a restricted communication domain composed of CPU-adjacent nodes within the same rack.

Within this domain, policy evaluation can be partially simplified due to the limited communication scope.

Multi-hop communication refers to any communication path that
traverses one or more intermediate nodes beyond direct CPU-adjacent connections.

Such paths are not eligible for this domain.

---

## Eligibility Conditions for Fast Mode

Rack-local Secure Fast Mode is applied only when all of the following conditions are satisfied:

- source.rack_id == destination.rack_id
- The communication path contains no Switch Nodes
- The communication path contains no Boundary Nodes
- hop_count == 1 (direct CPU-adjacent path)
- Traceability is preserved

If any condition is violated, the communication must fall back to standard PSC policy control.

---

## Control Rules

### Intra-domain Communication

- Reduced policy evaluation
- RCU-driven decision making
- High-speed communication prioritized

---

### Boundary Crossing

- Full policy evaluation enforced
- Resolver intervention allowed

---

### Violation Handling

- Immediate removal of Fast Mode
- Fallback to standard PSC control

---

## State Integration

### CALM

- Rack-local Secure Fast Mode is allowed
- Stable high-speed communication is maintained

---

### WARM

- Fast Mode maintained
- Monitoring is strengthened for selected flows

---

### HOT

- Fast Mode is restricted
- Resolver intervention is applied

---

### EMERGENCY

- Rack-level isolation is enforced
- External communication is blocked
- Only minimal internal communication is allowed (degraded operation)

---

## Design Principles

1. High-speed optimization must remain within restricted scope
2. Boundary crossing must always trigger stricter control
3. Traceability must be preserved
4. Isolation and degradation take priority during anomalies
5. Uncontrolled propagation must be prevented
6. Ensure latency stability through single-hop communication

---