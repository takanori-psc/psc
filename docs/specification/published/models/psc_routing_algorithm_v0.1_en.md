# PSC Routing Algorithm Specification v0.1

## Document Information

- Document Name: PSC Routing Algorithm
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Fabric
- Document Type : Specification
- Status : Draft
- Author : T. Hirose
- Created : 2026-03
- Last Updated : 2026-03
- Language : English

---

## 1. Purpose

This document defines the routing algorithm used by the
RCU (Routing Control Unit) within the PSC Fabric.

The routing algorithm defined in this specification is not a simple shortest-path selection mechanism.
Instead, it determines routes while considering Fabric state, congestion level, policy constraints,
reliability, and failure conditions, prioritizing system stability.

This specification mainly covers the following.

- Routing decision logic
- Route scoring
- Congestion-aware routing
- Policy-aware routing
- Trust-aware routing
- Failover decision
- Adaptive routing
- Fabric state interaction

---

## 2. Scope

This specification defines the route selection logic used for node-to-node transfers within the PSC Fabric.

This specification includes the following.

- Evaluation methods for candidate routes
- Principles for route score calculation
- Routing control based on Fabric state
- Route switching based on congestion, failure, and reliability
- Policy-constrained route selection

This specification does not include the following.

- Physical storage format of routing tables
- Address format details
- Packet structure details
- Full transfer flow definition
- Cryptographic key management

These are defined in separate specifications.

---

## 3. Design Philosophy

The PSC Routing Algorithm is designed as a state-based routing system
prioritizing stability, continuity, and controllability,
rather than a purely numerical optimization algorithm focused only on throughput.

The fundamental principles are as follows.

### 3.1 Stability First

Routing prioritizes overall Fabric stability
over instantaneous shortest-path performance.

### 3.2 State-aware Routing

Routing decisions consider not only link conditions
but also the global Fabric state.

CALM / WARM / HOT / EMERGENCY

### 3.3 Policy-constrained Routing

Even if a route is technically available,
it must not be selected if it violates
security, isolation, priority, or bandwidth reservation policies.

### 3.4 Trust-weighted Routing

The trust level of links and nodes
directly influences route selection.

### 3.5 Graceful Degradation

When failures or congestion occur,
the system maintains operational continuity whenever possible,
rather than stopping completely.

### 3.6 Hysteresis-based Switching

Route switching should not oscillate frequently.
Hysteresis mechanisms are used to stabilize route transitions.

### 3.7 Single-active-route Principle

PSC Routing Algorithm v0.1 adopts a **single active route model**.

For each transfer, the RCU selects one primary route
and performs data transfer through that route.

To avoid control complexity and routing oscillation caused by changing Fabric conditions,
multipath routing is not used in this version.

However, backup route candidates may be maintained
in preparation for failover.

These backup routes are not used for simultaneous traffic distribution.
Instead, they are reserved for rapid failover
when the active route becomes unavailable or degraded.

Multipath routing may be introduced
as a future extension of the PSC Fabric architecture.

---

## 4. Routing Objectives

The objectives of the PSC Routing Algorithm are as follows.

- Select a valid route from source to destination
- Reduce congestion concentration within the Fabric
- Avoid failed links and nodes
- Ensure routing compliance with security policies
- Prefer highly reliable routes
- Adjust routing behavior according to Fabric state
- Prevent route switching oscillations

---

## 5. Routing Decision Model

PSC performs routing decisions
using the following multi-stage model.

### 5.1 Decision Stages

- Candidate Route Discovery
- Route Eligibility Check
- Route Scoring
- Route Ranking
- Route Selection
- Route Lock / Hold
- Re-evaluation Trigger

### 5.2 Candidate Route Discovery

The RCU extracts candidate routes
from routing tables and Fabric state information.

The following factors are considered.

- Reachability
- Hop count
- Intermediate node type
- Available links
- Fabric state
- Policy constraints
- Failure information

### 5.3 Route Eligibility Check

Candidate routes must satisfy the following conditions.

- Link state is operational
- Intermediate nodes allow routing
- No Security Policy violations
- Logical reachability to the destination
- Not restricted by EMERGENCY conditions

### 5.4 Route Scoring

Each eligible candidate route
is assigned a score based on multiple evaluation factors.

### 5.5 Route Ranking

Candidate routes are sorted by score.

### 5.6 Route Selection

The highest-ranked route is selected as the primary route,
but the final decision considers

- hysteresis conditions
- route hold time
- differences from the currently active route

### 5.7 Route Lock / Hold

Once a route is selected,
it is held for a certain duration
to avoid switching due to minor score fluctuations.

### 5.8 Re-evaluation Trigger

Route evaluation may be triggered by

- link failure
- node failure
- congestion threshold exceeded
- Fabric state change
- Security Policy update
- Trust score degradation
- periodic timer expiration

---

## 6. Route Scoring Model

Each candidate route receives
a composite score based on multiple evaluation factors.

### 6.1 Score Components

- Base Reachability Score
- Hop Count Penalty
- Congestion Penalty
- Reliability Bonus / Penalty
- Trust Bonus / Penalty
- Policy Fitness Modifier
- Fabric State Modifier
- Failover Penalty
- Stability Bonus

### 6.2 Basic Concept

The scoring model follows these principles.

- Reachability is the highest priority
- Fewer hops are preferable
- Congested links reduce the score
- Reliable links increase the score
- Low-trust nodes or links decrease the score
- Policy-compliant routes are preferred
- Recently failed routes are treated cautiously
- Stable existing routes are preserved when acceptable

### 6.3 Abstract Formula

RouteScore =
  Reachability
  - HopPenalty
  - CongestionPenalty
  ± ReliabilityAdjustment
  ± TrustAdjustment
  + PolicyAdjustment
  + FabricStateAdjustment
  - FailoverPenalty
  + StabilityBonus

In this version,
precise coefficients are not defined
and may depend on implementation.

---

## 7. Congestion-aware Routing

### 7.1 Purpose

When congestion concentrates on specific links or nodes,
PSC distributes traffic to maintain overall Fabric stability.

### 7.2 Congestion Inputs

Congestion evaluation may use

- link utilization
- buffer occupancy
- queue length
- retransmission trends
- credit shortage frequency
- latency increase trends
- congestion alerts from Telemetry / Fault Monitor

### 7.3 Congestion Response

The RCU may

- penalize routes containing congested links
- re-evaluate alternative routes
- allow detours for low-priority traffic
- protect high-priority traffic
- strengthen safety control under HOT / EMERGENCY states

### 7.4 Localized vs Fabric-wide Congestion

Localized congestion  
Specific links or segments are penalized.

Fabric-wide congestion  
The system enters global load suppression behavior.

---

## 8. Policy-aware Routing

Routes that violate security or operational policies
must not be selected.

Policy-violating routes are excluded
rather than merely penalized.

Exception policies may exist for EMERGENCY mode.

---

## 9. Trust-aware Routing

PSC evaluates link and node trust levels continuously
rather than treating them as simple Up/Down states.

Low-trust routes may be penalized or excluded.

---

## 10. Failover Decision

When the active route fails or degrades significantly,
PSC performs failover.

Failover types include

Soft Failover  
Hard Failover  
Emergency Failover

---

## 11. Adaptive Routing

PSC supports adaptive routing based on Fabric conditions.

However, adaptation is gradual and stability-oriented,
not aggressive real-time optimization.

---

## 12. Fabric State Interaction

Routing behavior depends on Fabric state.

- CALM  
- WARM  
- HOT  
- EMERGENCY

Each state adjusts routing priorities
toward stability and survivability.

---

## 13. Route Stability Control

To avoid route oscillation,
PSC introduces

- Minimum Route Hold Time
- Score Improvement Threshold
- Switch Cooldown Timer
- Recovery Observation Window
- Hysteresis Margin

---

## 14. Interaction with Other Modules

- Resolver  
- Scheduler  
- SPU  
- TMU  
- TEU  
- OMU  
- Telemetry / Fault Monitor

Each module contributes information
used by the routing decision process.

---

## 15. High-level Pseudocode

```text
function select_route(source, destination, transfer_context):

    candidates = discover_routes(source, destination)

    eligible_routes = []
    for route in candidates:
        if not is_reachable(route):
            continue
        if not policy_allows(route, transfer_context):
            continue
        if not fabric_state_allows(route):
            continue
        eligible_routes.append(route)

    if eligible_routes is empty:
        return NO_ROUTE

    for route in eligible_routes:
        route.score = evaluate_route_score(route, transfer_context)

    ranked_routes = sort_by_score_descending(eligible_routes)

    best_route = ranked_routes[0]

    if should_keep_current_route(best_route) == true:
        return current_route
    else:
        return best_route
```


---

## 16. Non-goals

The following are not defined in v0.1.

- exact scoring coefficients
- machine learning optimization
- distributed routing control protocols
- large-scale distributed route computation
- multipath transfer specification
- full QoS class definitions

These may be introduced in future versions.

---

## 17. Future Extensions

Possible future extensions include

- Multi-path routing
- Predictive congestion avoidance
- Learning-assisted scoring
- Hierarchical routing domains
- Topology-aware large-scale route aggregation
- Trust decay / recovery model
- Fabric-wide reroute coordination

---

## 18. Summary

PSC Routing Algorithm treats routing
as a control problem integrating

- stability
- congestion management
- reliability
- policy compliance
- failure avoidance

rather than a simple shortest-path problem.

Version v0.1 defines the fundamental structure of
routing decision logic,
route scoring,
congestion-aware routing,
policy-aware routing,
trust-aware routing,
failover handling,
adaptive routing,
and Fabric state interaction.

Future versions will extend this model
with coefficient models,
route retention rules,
and multipath control.
