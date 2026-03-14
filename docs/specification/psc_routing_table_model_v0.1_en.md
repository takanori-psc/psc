# PSC Routing Table Model v0.1

## Document Information

- Document Name: PSC Routing Table Model
- Version: v0.1
- Project: PSC / Photon System Controller
- Layer: PSC Fabric
- Status: Draft
- Author: T. Hirose
- Language: English

---

## 1. Purpose

This document defines the routing table model used by the RCU (Routing Control Unit) in PSC Fabric.

The routing table model describes how routing information is represented, stored, and referenced for PSC routing decisions.

This specification focuses on route entry structure, next-hop representation, route state, policy-related attributes, and multi-path support.

---

## 2. Design Goals

The PSC routing table model is designed with the following goals:

1. Support logical Port-to-Port routing as the primary routing abstraction.
2. Support physical Node-to-Node forwarding as the underlying transport structure.
3. Allow policy-aware, state-aware, and domain-aware route selection.
4. Support multi-path and failover routing.
5. Remain scalable across node-scale, cluster-scale, and fabric-scale deployments.
6. Provide route information in a form usable by RCU, TMU, and TEU.

---

## 3. Basic Model

### 3.1 Primary routing abstraction

PSC routing is logically defined as Port-to-Port routing.

This means that the routing table is primarily used to determine how traffic destined for a destination port should be forwarded through PSC Fabric.

### 3.2 Underlying forwarding context

Although routing is logically Port-based, the physical forwarding path exists across PSC nodes and physical PSC links.

Therefore, PSC routing table entries may contain both:

- logical route information
- physical forwarding context

### 3.3 Two-layer route representation

The PSC routing table model uses a two-layer representation:

- Logical routing layer  
  Destination Port -> Candidate Next Hop Port

- Physical context layer  
  Destination Node / Next Hop Node / Domain context

This allows PSC to preserve Port-based communication abstraction while still supporting physical topology-aware routing.

---

## 4. Routing Table Structure

### 4.1 Route entry concept

A routing table consists of route entries.

Each route entry represents a valid or candidate forwarding path toward a destination communication endpoint.

A route entry may represent:

- a primary path
- an alternate path
- a failover path
- a restricted path
- an adaptive routing candidate

### 4.2 Recommended route entry fields

A PSC route entry may contain the following fields:

Destination fields

- Destination Port ID
- Destination Node ID
- Destination Domain ID

Next Hop fields

- Next Hop Port ID
- Next Hop Node ID

Attribute fields

- Path Class
- Policy Flags
- Trust Level

Route state fields

- Route State
- Priority
- Cost / Score
- Validity
- Update Timestamp

### 4.3 Minimal required fields

At minimum, a practical PSC route entry should include:

- Destination Port ID
- Next Hop Port ID
- Next Hop Node ID
- Route State
- Priority

---

## 5. Route Entry Fields

### 5.1 Destination Port ID

The Destination Port ID identifies the logical PSC communication endpoint for which this route is valid.

Examples:

- GPU service port
- storage endpoint port
- memory access port
- control channel port
- security-managed port

This is the primary destination key for logical PSC routing.

### 5.2 Destination Node ID

The Destination Node ID identifies the PSC node that owns the destination port.

This field provides physical topology context and is useful for:

- domain routing
- fault isolation
- node-level failover
- topology summarization

### 5.3 Destination Domain ID

The Destination Domain ID identifies the routing domain to which the destination belongs.

Examples:

- Port domain
- Node domain
- Cluster domain
- Fabric domain

This field allows route summarization and scalable large-fabric routing.

### 5.4 Next Hop Port ID

The Next Hop Port ID defines the primary forwarding exit or forwarding target for this route entry.

This is the preferred next-hop representation in PSC because PSC routing is fundamentally Port-based.

The Next Hop Port ID is used by TMU and TEU when selecting the actual forwarding interface or forwarding endpoint.

### 5.5 Next Hop Node ID

The Next Hop Node ID identifies the PSC node associated with the selected next hop.

This field provides physical forwarding context and helps with:

- topology management
- node failure handling
- cluster-level routing
- hierarchical route processing

### 5.6 Path Class

Path Class describes the intended routing category of the path.

Example path classes include:

- normal
- low_latency
- high_bandwidth
- secure
- isolated
- failover
- maintenance

Path Class allows route selection to reflect routing intent beyond shortest path.

### 5.7 Policy Flags

Policy Flags contain routing constraints or route control directives.

Examples:

- ISOLATE
- RESTRICT_FORWARD
- INSPECT
- PRIORITY_SECURITY
- LOCAL_ONLY
- FABRIC_ONLY

These flags are derived from Resolver and SPU decisions and must be respected by the RCU.

### 5.8 Trust Level

Trust Level describes the trust requirement or trust status associated with the route.

Trust-aware routing may be required in PSC for secure communication, isolated domains, or controlled forwarding.

### 5.9 Route State

Route State indicates the current usability condition of the route.

Example route states:

- healthy
- degraded
- congested
- restricted
- blocked
- failed
- standby

Route State is one of the most important runtime selection fields.

### 5.10 Priority

Priority defines the relative preference of the route among multiple candidate entries for the same destination.

Higher-priority routes are generally preferred unless current state or policy prevents their use.

### 5.11 Cost / Score

Cost or Score is an optional route metric used by routing logic.

This field may represent:

- path cost
- route preference score
- weighted policy score
- congestion-adjusted score

Future versions may define exact score calculation methods.

### 5.12 Validity

Validity indicates whether the route entry is currently valid for selection.

This may be represented as:

- valid
- temporarily invalid
- expired
- quarantined

### 5.13 Update Timestamp

Update Timestamp records when the route entry was last updated.

This supports bounded staleness handling and loose-consistency routing behavior.

---

## 6. Route Table Organization

### 6.1 Destination-oriented indexing

The PSC routing table should primarily be indexed by Destination Port ID.

This matches the logical PSC routing model and keeps routing aligned with Port-based communication.

### 6.2 Secondary indexing

Secondary indexing may be provided for:

- Destination Node ID
- Destination Domain ID
- Next Hop Port ID
- Next Hop Node ID
- Path Class
- Route State

This improves lookup efficiency for failover, maintenance, and topology operations.

### 6.3 Grouped route sets

Multiple route entries may exist for the same Destination Port ID.

These entries form a route set.

A route set may include:

- preferred route
- alternate route
- failover route
- restricted route
- adaptive route candidate

---

## 7. Multi-Path Support

### 7.1 Multiple candidate routes

PSC routing tables must support multiple candidate entries for a single destination.

This is required for:

- resilience
- congestion avoidance
- adaptive routing
- topology flexibility
- future high-availability routing

### 7.2 Route set example

A destination route set may look like this:

- Destination Port P100 -> Next Hop Port P210 -> Priority 100 -> healthy
- Destination Port P100 -> Next Hop Port P218 -> Priority 80 -> healthy
- Destination Port P100 -> Next Hop Port P233 -> Priority 60 -> standby

### 7.3 Selection behavior

The routing table itself does not execute route selection.

It only stores route candidates.

Selection logic is performed by the RCU using:

- route state
- policy constraints
- trust requirements
- priority
- score
- topology conditions

---

## 8. Failover Support

### 8.1 Failover-ready entries

The routing table should explicitly support failover-capable entries.

These may be marked by:

- Path Class = failover
- standby Route State
- reduced Priority
- restricted Policy Flags

### 8.2 Failover activation

When the preferred route becomes invalid or unsafe, the RCU may activate an alternate entry from the same route set.

### 8.3 Graceful degradation

Failover routing may select a route that is less optimal but still valid.

Examples:

- longer path
- reduced bandwidth path
- restricted security path
- temporary domain-limited path

---

## 9. Adaptive Routing Support

### 9.1 Runtime route variation

The routing table must support route state changes caused by runtime conditions.

Examples:

- congestion
- thermal pressure
- optical degradation
- retry escalation
- policy change
- node isolation

### 9.2 Stable adaptation

Adaptive routing should use route table updates in a stable manner.

Frequent route thrashing should be avoided.

This may be achieved through:

- hysteresis
- cooldown intervals
- update dampening
- bounded score changes

### 9.3 Relationship to Fabric State

Route entries may be interpreted differently depending on current Fabric State:

- CALM  
  prefer stable primary entries

- WARM  
  allow mild alternate-path preference changes

- HOT  
  prefer congestion relief and load redistribution

- EMERGENCY  
  prioritize safe continuity, isolation, and survivability

---

## 10. Domain-Aware Routing Table Behavior

### 10.1 Domain context

Routing table entries may represent routes inside:

- local node scope
- cluster scope
- fabric scope

### 10.2 Route summarization

For large systems, routing tables should support route summarization at domain boundaries.

This allows an RCU to store abstract reachability information for remote domains rather than full per-port visibility for the entire fabric.

### 10.3 Gateway-oriented entries

At domain boundaries, a route entry may resolve to a gateway-facing next hop instead of the final destination region.

This supports scalable routing across mixed Mesh and Spine-Leaf topologies.

---

## 11. Route Entry Lifecycle

### 11.1 Entry creation

Route entries may be created by:

- topology discovery
- static initialization
- policy provisioning
- route learning
- adaptive updates
- failover preparation

### 11.2 Entry update

Route entries may be updated when:

- topology changes
- policy changes
- link state changes
- congestion changes
- trust conditions change
- Fabric State changes

### 11.3 Entry invalidation

Route entries may be invalidated when:

- a path fails
- a node becomes unavailable
- a policy restriction blocks usage
- a route becomes stale beyond tolerance
- a trust violation is detected

### 11.4 Entry removal

An invalid route entry may be removed immediately or retained for historical / dampening purposes depending on implementation policy.

---

## 12. Interaction with PSC Modules

### 12.1 Resolver

Resolver provides routing intent, policy requirements, and security context that influence route table usage.

### 12.2 SPU

SPU constrains route validity and route selection according to security policy.

### 12.3 RCU

RCU owns route table interpretation, maintenance, and candidate route selection.

### 12.4 TMU

TMU consumes the selected next-hop information and allocates transfer resources accordingly.

### 12.5 TEU

TEU uses the selected forwarding port information to execute actual transfer operations.

---

## 13. Example Route Entry

Example:

- Destination Port ID: PORT_GPU_014
- Destination Node ID: NODE_022
- Destination Domain ID: CLUSTER_A

- Next Hop Port ID: PORT_FABRIC_EGRESS_03
- Next Hop Node ID: NODE_007

- Path Class: low_latency
- Policy Flags: RESTRICT_FORWARD
- Trust Level: trusted_internal

- Route State: healthy
- Priority: 100
- Cost / Score: 18
- Validity: valid
- Update Timestamp: T+002145

---

## 14. Future Extensions

Future versions may define:

- exact route score formula
- explicit route aging model
- route compression format
- route telemetry integration
- optical-path-specific fields
- multi-path load balancing fields
- route provenance tracking
- trust-domain scoring

---

## 15. Summary

PSC Routing Table Model v0.1 defines the route representation used by the RCU in PSC Fabric.

The model is based on:

- Port-to-Port logical routing
- Node-aware physical context
- policy-aware route representation
- multi-path route sets
- failover support
- adaptive routing support
- domain-aware scalability

This document serves as the structural foundation for future PSC routing selection and routing algorithm specifications.

---
