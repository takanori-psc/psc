# PSC Congestion Control Model v0.1

## Document Information

- Document Name: PSC Congestion Control Model
- Version: v0.1
- Project: PSC / Photon System Controller
- Layer: PSC Fabric
- Status: Draft
- Author: T. Hirose
- Language: English

---

## 1. Purpose

This document defines the congestion control model for PSC Fabric.

The purpose of this model is to detect congestion conditions across multiple scopes, evaluate their severity, and apply non-blocking control while preserving fast-path communication.

This model follows the core PSC principle:

**"Do not break fast path."**

---

## 2. Scope

This document covers the following:

- congestion signal detection
- telemetry-based congestion evaluation
- congestion evaluation at Link-level / Node-level / Fabric-level
- congestion severity classification
- local and distributed control models
- interaction with routing
- AI behavior under congestion
- relationship with Fabric State

This document does not define the following:

- detailed packet formats for telemetry export
- detailed implementation of hardware counters
- transport specifications such as retransmission control
- queue-control microarchitecture

These are to be defined in separate specifications.

---

## 3. Design Principles

PSC congestion control shall follow these principles:

- congestion control must be non-blocking
- fast path must never be globally stalled
- local control is preferred over centralized control
- distributed control is preferred over single-point control
- routing should avoid congestion whenever possible
- policy and trust constraints must always be preserved
- AI is optional and must never delay mandatory control
- AI-related processing may be discarded, throttled, or deferred under congestion

---

## 4. Objectives of Congestion Control

PSC congestion control has the following objectives:

1. early detection
2. suppression of congestion propagation
3. protection of stable traffic from localized overload
4. preservation of critical traffic
5. provision of useful feedback to routing
6. gradual recovery without oscillation
7. maintenance of stability under partial failures and burst loads

---

## 5. Control Scope

Congestion is evaluated at the following scopes, and control is executed locally or cooperatively at each scope.

### 5.1 Link-level

Link-level congestion represents overload or degradation occurring on a specific link.

Control entity: the PSC node that owns the affected link

Control actions:

- reduce route preference
- suppress new assignment
- perform local queue control

Judgment is performed autonomously based on local telemetry.

### 5.2 Node-level

Node-level congestion represents overload occurring inside a PSC node.

Control entity: the affected PSC node

Control actions:

- input restriction
- scheduling adjustment
- internal resource control
- AI suspension

Judgment is performed based on internal node state and local telemetry.

### 5.3 Fabric-level

Fabric-level congestion represents a congestion condition spreading across a wide area or the entire Fabric.

Control entity: distributed PSC group (cooperative operation)

Control actions:

- congestion information sharing
- route redistribution
- Fabric State escalation
- wide-area traffic control

Judgment is performed cooperatively based on distributed telemetry and shared state.

---

## 6. Congestion Signal Model

PSC detects congestion based on telemetry.

### 6.1 Primary Signals

- link utilization
- buffer occupancy
- queue length
- waiting time
- latency increase
- retry rate
- credit starvation
- drop/discard
- processing backlog
- route instability

### 6.2 Secondary Signals

- frequent route reevaluation
- sustained throughput degradation
- ingress/egress asymmetry
- hotspot concentration
- burst skew

### 6.3 Signal Evaluation Properties

Each signal is evaluated using the following:

- instantaneous value
- moving average
- peak value
- persistence duration
- recovery trend

Do not react to instantaneous spikes alone.
Persistence must be emphasized.

---

## 7. Congestion Severity Levels

### 7.1 Levels

- NORMAL
- WATCH
- CONGESTED
- SEVERE
- CRITICAL

### 7.2 Meanings

**NORMAL**
No problem.

**WATCH**
Signs of congestion exist, but control is not yet required.

**CONGESTED**
Congestion is confirmed and control begins.

**SEVERE**
Serious impact on performance and stability.

**CRITICAL**
Service continuity is affected and emergency handling is required.

---

## 8. Congestion Evaluation Model

Congestion evaluation in PSC is based not on a single indicator, but on a **Congestion Score** that integrates multiple telemetry signals.

The Congestion Score is an internal numerical representation for evaluation. In external control, it is converted into a congestion severity level.

### 8.1 Inputs

The evaluation inputs for the Congestion Score shall include at least the following:

- Utilization Score
- Buffer Pressure Score
- Latency Penalty
- Retry Penalty
- Credit Starvation Penalty
- Persistence Modifier
- Recovery Modifier
- Stability Modifier

Each input should be treated as a normalized value greater than or equal to zero.

### 8.2 Evaluation Policy

Congestion evaluation shall follow these policies:

- do not determine congestion based on a single metric alone
- treat sustained degradation as more significant than temporary spikes
- apply gradual reduction when a recovery trend is observed
- prioritize highly reliable telemetry
- apply hysteresis to congestion level transitions
- use evaluation to protect fast path, not to stop fast path

### 8.3 Congestion Score

PSC internally represents congestion conditions as a Congestion Score.

In v0.1, the Congestion Score is based on the following additive model.

```
Congestion Score =
Utilization Score
+ Buffer Pressure Score
+ Latency Penalty
+ Retry Penalty
+ Credit Starvation Penalty
+ Persistence Modifier
- Recovery Modifier
- Stability Modifier
```

#### 8.3.1 Score Normalization Requirements

Each input that composes the Congestion Score must be normalized into a mutually comparable scale.

In v0.1, the following principles apply:

- each score should preferably be normalized to a common range such as 0.0 to 1.0
- penalty terms shall be treated in the positive direction
- modifier terms such as Recovery and Stability shall be treated in the subtractive direction
- Persistence Modifier shall be treated as a time-dependent amplification term
- no single element should dominate the entire score

The implementation may adopt either of the following approaches:

- normalized score (for example 0.0 to 1.0)
- scaled integer score (for example 0 to 100)

However, the scale must be consistent within the same scope.

This model is the v0.1 baseline form, prioritized for ease of implementation. Future versions may extend it to weighted models or policy-dependent correction models.

### 8.4 Meaning of Each Input Element

#### 8.4.1 Utilization Score

Represents the utilization of a link or node.
The score increases as high utilization continues.

#### 8.4.2 Buffer Pressure Score

Represents buffer occupancy and queue pressure.
Sustained pressure is emphasized over instantaneous occupancy.

#### 8.4.3 Latency Penalty

Represents the amount of latency increase from the normal baseline.
Sustained increase is treated more heavily than short-term spikes.

#### 8.4.4 Retry Penalty

Represents increases in retransmission, retry, or transfer failure.
It is used as a sign of link degradation or localized congestion.

#### 8.4.5 Credit Starvation Penalty

Represents sustained lack of credits or persistent transmission wait states.
It is treated as an important signal of blockage at the receiver or relay side.

#### 8.4.6 Persistence Modifier

Added when a degraded condition continues for a certain period.
This distinguishes instantaneous spikes from structural congestion.

#### 8.4.7 Recovery Modifier

Subtracted when an improvement trend in congestion indicators continues.
It is used for gradual decline rather than abrupt recovery.

#### 8.4.8 Stability Modifier

Subtracted when routes, states, and transfer behavior are stable.
It prevents overreaction to short-term fluctuations.

### 8.5 Normalization Policy

To make comparison possible across heterogeneous nodes and links, each input value should be normalized whenever possible.

The detailed normalization method will be defined in a future version, but v0.1 adopts the following principles:

- utilization is normalized by maximum capacity ratio
- buffer pressure is normalized by maximum allowable occupancy ratio
- latency is evaluated as the difference from the normal baseline
- retry rate and credit starvation are treated as frequency per unit time
- Persistence / Recovery / Stability are managed independently as modifier terms

### 8.6 Level Conversion

The Congestion Score is converted into the following severity levels for control use:

- NORMAL
- WATCH
- CONGESTED
- SEVERE
- CRITICAL

In v0.1, either fixed thresholds or implementation-defined thresholds may be used, but the following must be satisfied:

- severity must increase monotonically toward higher levels
- upward and downward thresholds must be separated
- transition to a higher level should preferably require sustained confirmation
- recovery should lower the level gradually

### 8.7 Hysteresis

Hysteresis shall be applied to changes in congestion level.

#### 8.7.1 Basic Principles

- upward thresholds are higher than downward thresholds
- downward transitions shall have a minimum hold time
- when oscillation is detected, downward transitions shall be delayed
- recovery is treated more slowly than degradation

#### 8.7.2 Purpose

The purposes of hysteresis are as follows:

- suppression of level oscillation
- prevention of route flapping
- suppression of false recovery caused by temporary improvement
- preference for stable control reaction

### 8.8 Scope-specific Evaluation

The Congestion Score may be calculated independently for each of the following scopes: Link-level / Node-level / Fabric-level.

#### 8.8.1 Link-level Score

Primarily uses link utilization, link latency, retry rate, and credit starvation.

#### 8.8.2 Node-level Score

Primarily uses internal node queues, buffer pressure, processing delay, and ingress/egress imbalance.

#### 8.8.3 Fabric-level Score

Primarily uses congestion distribution across multiple nodes and links, hotspot concentration, wide-area latency increase, and regional load propagation.

Fabric-level Score does not complete within a single node and is evaluated cooperatively based on distributed telemetry and shared state.

### 8.9 Reflection to Routing

The Congestion Score and its severity level are reflected into Routing in the following ways:

#### 8.9.1 Penalty

At WATCH level or above, a congestion penalty may be applied to the target link or node.

#### 8.9.2 Route Suppression

At CONGESTED or SEVERE level, route preference for new low-priority traffic may be reduced.

#### 8.9.3 Invalidation

At CRITICAL level, or at implementation-defined SEVERE conditions, the route candidate may be temporarily invalidated.

However, policy or trust constraints must never be violated solely because of congestion.

### 8.10 Positioning in v0.1

This model is the **baseline evaluation model** of PSC congestion control.

The purposes of v0.1 are:

- to define a minimally implementable structure
- to provide an internal evaluation value connectable to Routing
- to provide a foundation for integration with Fabric State
- to remain extensible toward weighted models and AI-assisted evaluation in future versions

---

## 9. Control Reaction Model

### 9.1 Link-level

- reduce route preference
- stop new low-priority traffic
- apply penalty
- defer low-priority transfer
- preserve critical communication

### 9.2 Node-level

- lower preference for routes through the node
- restrict low-priority input
- stop background tasks
- stop AI
- isolate internal paths

### 9.3 Fabric-level

- propagate congestion notification
- avoid overloaded regions
- use alternative routes
- elevate Fabric State
- move to safe operation

---

## 10. Interaction with Routing

Congestion Score and congestion severity level directly affect route selection and control actions in Routing.

This chapter defines Routing responses according to congestion conditions.

### 10.1 Basic Principles

- congestion is treated as one evaluation factor in Routing
- Policy and Trust always take priority
- security constraints must not be violated solely because of congestion
- controls that block fast path are prohibited
- congestion control is an adjustment of route selection, not a full stop

### 10.2 Congestion Levels and Routing Actions

Routing applies the following actions according to congestion severity level.

#### NORMAL

- no congestion-related effect
- perform normal routing evaluation

#### WATCH

- small penalty may be applied
- perform mild avoidance in new route selection

#### CONGESTED

- apply a clear penalty
- suppress assignment of new low-priority traffic
- prefer alternative routes if available

#### SEVERE

- apply a strong penalty
- as a rule, avoid assigning new traffic
- execute route switching (failover) when necessary

#### CRITICAL

- the affected link or node may be temporarily invalidated
- it may be excluded from the Routing table
- however, if no alternative path exists, limited use may be permitted

### 10.3 Penalty Model

Congestion impact in Routing is reflected mainly as a penalty.

- Link-level → added to link cost
- Node-level → added to transit-node cost
- Fabric-level → applied as a correction to the entire route score

The penalty shall be added to the route evaluation score in Routing.

The penalty magnitude should preferably increase in proportion to the Congestion Score.

### 10.4 Route Suppression

Depending on congestion conditions, Routing may perform the following:

- suppress new allocation of low-priority traffic
- stop generating new routes toward a specific link
- lower the selection probability of congested routes

### 10.5 Route Invalidation

A route is temporarily invalidated under the following conditions:

- CRITICAL level reached
- sustained SEVERE state (implementation-defined)

An invalidated route is excluded from selection until recovery conditions are satisfied.

### 10.6 Failover

Routing performs route switching under the following conditions:

- congestion persists and performance degradation becomes significant
- CRITICAL or sustained SEVERE state continues
- latency or throughput exceeds an allowable threshold

Failover shall use hysteresis to prevent excessive switching.

### 10.7 Constraints

- route selection that violates Policy constraints is prohibited
- routes that do not satisfy Trust requirements are not selectable
- congestion avoidance shall be performed only within the allowable range

---

## 11. Integration with Fabric State

### CALM

- normal operation
- AI allowed

### WARM

- strengthen early warning detection
- begin AI restriction

### HOT

- apply strong penalty
- stop non-critical processing
- greatly reduce AI

### EMERGENCY

- safety first
- fully exclude AI
- prioritize stabilization

---

## 12. AI Interaction Model

### 12.1 Roles

- pattern analysis
- prediction
- anomaly detection
- route suggestion

### 12.2 Constraints

- must not block fast path
- must not delay control
- must not violate policy
- must not violate trust

### 12.3 Under Congestion

AI may be:

- deferred
- restricted
- sampled
- partially executed
- discarded

---

## 13. Recovery Model

### 13.1 Conditions

- utilization decreases
- queues decrease
- latency returns to normal
- retries decrease
- stability is maintained

### 13.2 Principles

- recovery must be slow
- immediate return is prohibited
- flapping must be prevented
- return must be staged

---

## 14. Distinction Between Fault and Congestion

Congestion:

- overload
- queue accumulation
- reachability remains

Fault:

- link down
- unreachable
- integrity violation

Severe congestion may exhibit behavior similar to faults.

---

## 15. Open Design Items

1. scoring formula
2. normalization across heterogeneous nodes
3. telemetry period
4. hysteresis duration
5. invalidation threshold
6. notification scope
7. handling of AI confidence
8. burst vs. structural congestion

---

## 16. Summary

PSC congestion control is composed of:

- non-blocking control
- telemetry-driven evaluation
- distributed control

While preserving fast path, it realizes:

- local reaction
- routing integration
- Fabric State integration
- optional AI usage
