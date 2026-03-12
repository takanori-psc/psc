# PSC Routing Model v0.1

## Document Information

- Document Name: PSC Routing Model
- Version: v0.1
- Project: PSC / Photon System Controller
- Layer: PSC Fabric
- Status: Draft
- Author: T. Hirose
- Language: English

---

## 1. Purpose

This document defines the routing model of PSC Fabric.

The routing model describes how PSC nodes, ports, and clusters establish forwarding paths across the PSC Fabric, and how routing control adapts to topology, faults, load conditions, and future multi-layer fabric expansion.

This specification focuses on the logical routing architecture and the control behavior of the RCU (Routing Control Unit).

---

## 2. Design Goals

The PSC routing model is designed with the following goals:

1. Support scalable communication across node-scale, cluster-scale, and fabric-scale systems.
2. Allow topology-aware routing for mesh and future hierarchical fabrics.
3. Support local autonomy without requiring strict global synchronization.
4. Enable failover and adaptive routing under degraded or congested conditions.
5. Preserve deterministic behavior where required by policy or transfer class.
6. Integrate routing decisions with PSC state-based control architecture.

---

## 3. Routing Principles

PSC routing is based on the following principles:

### 3.1 State-based routing

Routing decisions are based on abstract fabric and node states rather than on precise global optimization.

Examples of routing-relevant state include:

- CALM
- WARM
- HOT
- EMERGENCY

### 3.2 Local-first decision model

Routing should prefer local routing knowledge and local topology awareness whenever possible.

Global coordination may exist, but PSC routing must remain operational even when only partial topology knowledge is available.

### 3.3 Policy-aware path selection

Routing is not based only on shortest-path logic.
Path selection may also consider:

- security policy
- trust level
- transfer class
- isolation domain
- congestion state
- fault state
- redundancy requirements

### 3.4 Multi-path capable architecture

PSC routing should support multiple valid paths between source and destination when topology permits.

Multi-path support is used for:

- resilience
- failover
- congestion avoidance
- load distribution
- future high-availability operation

---

## 4. Routing Architecture

PSC routing is structured as a layered decision and execution model.

### 4.1 Routing-related modules

The following modules are relevant to routing operation:

- Resolver  
  Determines routing intent and policy constraints.

- Scheduler  
  Coordinates routing priority and transfer scheduling order.

- SPU (Security Policy Unit)  
  Applies security restrictions and routing permissions.

- RCU (Routing Control Unit)  
  Selects logical routes and maintains routing knowledge.

- TMU (Transfer Management Unit)  
  Converts selected route decisions into transfer scheduling and resource allocation.

- TEU (Transfer Execution Unit)  
  Executes actual packet / chunk forwarding.

### 4.2 Routing responsibility of the RCU

The RCU is responsible for:

- maintaining route information
- selecting candidate paths
- evaluating route validity
- handling route changes due to faults or congestion
- providing route output to TMU

The RCU does not directly execute data transfer.
It only determines routing behavior and route selection.

---

## 5. Routing Domains

PSC Fabric routing is divided into hierarchical routing domains.

### 5.1 Port domain

The port domain is the smallest routing scope.

It defines communication between logical communication endpoints inside a node or across directly connected interfaces.

### 5.2 Node domain

The node domain defines routing behavior inside a single PSC node.

This includes:

- local switching
- internal forwarding
- local policy enforcement
- local device-to-device transfer selection

### 5.3 Cluster domain

The cluster domain defines routing across a group of PSC nodes that operate within a shared local topology.

Examples include:

- workstation cluster
- rack-scale group
- local accelerator island
- storage cluster

### 5.4 Fabric domain

The fabric domain defines system-wide routing across the entire PSC Fabric.

This domain supports:

- multi-cluster routing
- large-scale path selection
- hierarchical routing extension
- future spine-leaf and optical fabric expansion

---

## 6. RCU Routing Model

### 6.1 Route input elements

The RCU may use the following inputs:

- source address
- destination address
- source domain
- destination domain
- transfer class
- policy flags
- trust level
- node state
- fabric state
- fault information
- congestion indicators
- topology information

### 6.2 Route output

The RCU produces route selection results such as:

- selected next hop
- selected path class
- alternate path candidates
- failover path candidates
- routing restriction flags
- isolation routing constraints

### 6.3 Route decision mode

The RCU may operate in several decision modes:

- normal routing
- restricted routing
- isolated routing
- failover routing
- adaptive routing

### 6.4 Loose consistency model

The RCU is not required to maintain perfectly synchronized global routing knowledge.

Instead, PSC routing uses a loose-consistency approach:

- local route correctness is prioritized
- stale global information is tolerated within bounded limits
- route selection must remain safe under partial information
- failover behavior must remain valid without full fabric convergence

---

## 7. Mesh Routing

### 7.1 Default topology assumption

The default PSC Fabric topology is partial mesh.

This means:

- not all nodes are directly connected
- multiple possible routes may exist
- local topology may differ between deployments

### 7.2 Mesh routing behavior

In mesh routing, the RCU selects routes based on:

- direct path availability
- hop count
- current node / link state
- congestion indicators
- policy restrictions
- redundancy needs

### 7.3 Mesh routing characteristics

Mesh routing should support:

- direct forwarding when available
- alternate-path selection
- local rerouting
- path diversity
- graceful degradation under partial failure

### 7.4 Preferred behavior in mesh routing

When multiple valid routes exist, route preference may consider:

1. policy compliance
2. trust / security constraints
3. path health
4. congestion state
5. hop efficiency

Shortest path alone is not always the preferred route.

---

## 8. Spine-Leaf Routing

### 8.1 Future topology support

PSC Fabric must support future hierarchical topologies such as spine-leaf fabric.

This is especially important for large-scale and optical PSC deployments.

### 8.2 Spine-leaf routing model

In spine-leaf routing:

- leaf nodes connect to local aggregation points
- spine paths provide higher-level interconnection
- routing may distinguish local and uplink decisions

### 8.3 Routing behavior in hierarchical fabrics

The routing model should support:

- leaf-local routing
- leaf-to-leaf routing through spine paths
- domain boundary routing
- aggregated path selection
- scalable route abstraction

### 8.4 Route abstraction

In large fabrics, the RCU should not require full per-node visibility for all remote domains.

Instead, remote areas may be represented as abstract reachable domains or summarized route regions.

---

## 9. Failover Routing

### 9.1 Purpose

Failover routing ensures that communication remains possible when links, nodes, or routing regions become unavailable or degraded.

### 9.2 Trigger conditions

Failover routing may be triggered by:

- link failure
- node failure
- policy isolation event
- congestion escalation
- security incident
- topology partition
- optical signal degradation

### 9.3 Failover behavior

When failover routing is triggered, the RCU should:

1. invalidate unsafe or unusable routes
2. search for alternate valid paths
3. preserve policy and security constraints
4. notify TMU of route changes
5. avoid unstable oscillation if possible

### 9.4 Graceful degradation

If a preferred route is unavailable, PSC should degrade gracefully rather than fail immediately.

Examples include:

- longer but valid route selection
- lower-bandwidth routing
- restricted-mode routing
- temporary isolation path

---

## 10. Adaptive Routing

### 10.1 Purpose

Adaptive routing allows PSC Fabric to respond to changing load, congestion, faults, and topology conditions.

### 10.2 Adaptation inputs

Adaptive routing may use:

- node thermal state
- transfer queue pressure
- congestion level
- retry rate
- link quality
- fault telemetry
- optical monitoring data
- fabric state transitions

### 10.3 Adaptation policy

Adaptive routing must remain policy-bounded.

This means adaptation is allowed only inside safe routing boundaries defined by:

- security policy
- trust requirements
- isolation domain
- transfer class
- system state constraints

### 10.4 Stability requirement

Adaptive routing must avoid excessive oscillation.

The routing system should use bounded adaptation behavior such as:

- hysteresis
- cooldown intervals
- route preference persistence
- state-based threshold switching

### 10.5 Relationship to Fabric State Model

Adaptive routing behavior may change depending on fabric state:

- CALM  
  Prefer stable and efficient normal routing

- WARM  
  Begin mild congestion-aware adaptation

- HOT  
  Prefer load relief and controlled rerouting

- EMERGENCY  
  Prioritize survivability, isolation, and safe route continuity

---

## 11. Routing Constraints

PSC routing must always respect the following constraints:

- security restrictions
- domain isolation rules
- transfer-class requirements
- routing safety rules
- failover validity
- hardware capability limits

A route that is shorter but violates policy must not be selected.

---

## 12. Future Extensions

Future versions may define:

- explicit route metrics
- route scoring model
- multi-path load balancing
- optical path-aware routing
- trust-domain routing
- cluster gateway behavior
- fabric-wide route summarization
- routing telemetry feedback loop

---

## 13. Summary

PSC Routing Model v0.1 defines a scalable, policy-aware, state-based routing architecture for PSC Fabric.

The model supports:

- local-first route control
- mesh routing
- future spine-leaf routing
- failover routing
- adaptive routing
- loose-consistency distributed operation

This routing model is intended to serve as the foundation for future PSC routing specifications and implementation phases.

---
