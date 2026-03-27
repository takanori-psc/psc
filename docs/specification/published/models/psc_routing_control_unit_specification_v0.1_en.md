# PSC Routing Control Unit Specification v0.1

## Document Information

- Document Name : Routing Control Unit Specification
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSC Fabric
- Document Type : Specification
- Component     : Routing Control Unit (RCU)
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-03
- Last Updated  : 2026-03
- Language      : English

---

## 0. Philosophical Foundation

The Routing Control Unit (RCU) is not a global optimizer.
It is a route decision and transition control module for stable fabric operation.

All mechanisms described in this document
must respect the following principles:

* No continuous global optimization
* State-based route control
* Route switching only when justified by policy or degradation
* Stability takes precedence over unnecessary switching
* Current route cost MUST be re-evaluated against current state
* Route decisions MUST be explainable and reproducible
* RCU is responsible for spatial control (path control), not temporal scheduling
* RCU does not execute data transfer itself; it determines and applies routing decisions to the execution layer

---

## 1. Overview

RCU is the route decision and path transition control module of PSC.

RCU is responsible for:

- route evaluation
- route selection
- path lifecycle control
- failover handling
- degraded-mode routing
- recovery to normal routing

RCU SHALL operate as the spatial control unit of PSC.

Role separation:

- TMU = temporal control (priority / scheduling)
- RCU = spatial control (path / route decision)
- TEU = execution (actual data transfer)

RCU SHALL evaluate route candidates based on:

- path cost
- congestion
- failure state
- trust condition
- policy
- degraded-mode constraints

RCU SHALL support route retention, route switching,
and controlled fallback behavior without causing excessive oscillation.

---

## 2. Scope

RCU covers:

- route candidate evaluation
- selected route maintenance
- switching decision
- degraded fallback route handling
- route recovery handling
- path lifecycle state control

RCU does not cover:

- transfer priority ordering
- burst scheduling
- direct packet / chunk movement
- low-level physical transmission execution

Those functions belong to TMU and TEU.

---

## 3. Functional Responsibilities

### 3.1 Route Evaluation

RCU SHALL evaluate available candidate routes
using current operational state.

Evaluation inputs MAY include:

- topology information
- current path state
- congestion state
- link/node health
- trust level
- policy constraints
- degraded fallback rules

### 3.2 Route Selection

RCU SHALL distinguish between:

- Best route
  = lowest/evaluated best candidate under current condition
- Selected route
  = route actually adopted for operation

RCU MUST allow Best route and Selected route to differ
when switching is suppressed by hysteresis, policy, or recovery rules.

### 3.3 Route Retention

RCU SHALL preserve the current selected route
when route improvement is insufficient to justify switching.

RCU MUST support:

- keep current route
- keep current degraded route
- keep current route within hysteresis margin
- keep current route under policy margin

### 3.4 Route Switching

RCU SHALL switch routes only when switching conditions are satisfied.

Switching decisions MAY include:

- SWITCH
- DEGRADED_SWITCH
- ESCALATE_SWITCH

Route switching MUST consider:

- improvement magnitude
- hysteresis margin
- degraded-mode switch margin
- policy behavior
- resolver override
- trust constraint violation
- route health deterioration

### 3.5 Failover and Degraded Fallback

If a trusted or primary route becomes unavailable or unacceptable,
RCU MAY enter degraded routing behavior under higher-level approval.

RCU SHALL support:

- controlled degraded fallback
- temporary untrusted fallback
- fallback route reselection
- degraded fallback reason logging

Fallback behavior SHALL NOT be treated as undefined routing.
It MUST be treated as controlled exception handling.

### 3.6 Recovery

RCU SHALL support controlled recovery from degraded routing back to normal routing.

Recovery SHALL require explicit conditions such as:

- trusted route return
- stable trusted route availability across consecutive steps
- recovery counter or equivalent guard
- optional throughput / stability / trust-confidence conditions

RCU MUST NOT return from DEGRADED to NORMAL immediately
without satisfying recovery criteria.

---

## 4. Operational States

RCU SHALL maintain lightweight internal operational states.

### 4.1 RCU_NORMAL

- normal route evaluation
- policy-based switching
- hysteresis applies
- trusted route selection preferred when required

### 4.2 RCU_DEGRADED

- fallback route selection allowed
- degraded switch margin applies
- route reselection remains active
- trust failure recovery is prioritized

### 4.3 RCU_RECOVERY

- trusted route return is being verified
- recovery counter or equivalent stability condition applies
- route behavior remains guarded until recovery completes

### 4.4 RCU_LOCKDOWN (Optional)

- used for emergency or strict safety-preserving routing control
- freeze / quarantine / cap constraints dominate routing freedom

---

## 5. Inputs and Outputs

### 5.1 Inputs

RCU inputs MAY include:

- TransferRequest from TMU
  `{src, dst, class, size_hint, qos, deadline?}`

- topology and link state from ICI / control layer

- PathStats from TEU
  `{throughput, loss, stall, retry}`

- telemetry / fault state

- policy information

- trust state

- Resolver recommendations / overrides

### 5.2 Outputs

RCU outputs MAY include:

- PathPlan to TEU
  `{path_id, hops[], encap, rate_cap, failover_list}`

- PathOffer to TMU
  `{path_id, cost, capacity, risk, ttl}`

- control/configuration outputs to ICI or switching layer

- switch decision state
  `{KEEP, SWITCH, DEGRADED_SWITCH, ESCALATE_SWITCH}`

- recovery / degraded-mode state signals

---

## 6. Decision Model

### 6.1 Current Route Re-evaluation

RCU MUST re-evaluate the current selected route
against the current system state.

Current route cost MUST NOT remain stale across steps.

RCU SHALL support per-step or event-driven re-evaluation.

### 6.2 Best Route vs Selected Route

RCU MUST compute the Best route under current conditions.

RCU MUST then compare:

- current selected route
- current selected route re-evaluated cost
- best route
- best route cost
- policy-specific switching rule
- margin / hysteresis condition

Selected route MAY remain unchanged
even when Best route differs.

### 6.3 Policy-sensitive Switching

RCU SHALL support policy-sensitive switching behavior.

Examples:

- stability policy:
  - preserve current route for small improvements
- latency policy:
  - switch immediately or more aggressively when a better route appears

Policy behavior MUST affect actual switching decisions,
not only candidate ranking.

### 6.4 Hysteresis-based Switching

RCU MUST implement hysteresis to suppress route oscillation.

Example rule:

- keep current route when improvement is within hysteresis margin
- switch route when improvement exceeds hysteresis margin

Dedicated degraded-mode switching margin MAY be used.

### 6.5 Degraded-mode Decision

When operating in degraded mode, RCU SHALL:

- evaluate fallback candidates
- compare degraded routes
- apply fallback penalty or trust-aware weighting
- preserve controlled route continuity
- allow policy-sensitive switching within degraded mode

### 6.6 Resolver-assisted Override

Resolver MAY authorize degraded fallback or escalation.

In such cases, RCU SHALL apply Resolver-approved routing exceptions safely.

Resolver involvement MAY include:

- allow untrusted fallback
- force degraded mode transition
- force escalation switch

RCU SHALL remain the route execution-decision layer,
while Resolver remains the higher-level decision authority.

---

## 7. Path Lifecycle Model

RCU SHALL manage path lifecycle states.

Recommended lifecycle:

- SETUP
- ACTIVE
- DEGRADED
- FAILOVER
- RECOVERY
- TEARDOWN

### 7.1 SETUP

- route selected
- path configured but not yet fully active

### 7.2 ACTIVE

- route currently in use
- current route cost continuously re-evaluated

### 7.3 DEGRADED

- selected route remains usable but degraded
- fallback or guarded switching may occur

### 7.4 FAILOVER

- route transition to alternative path in progress

### 7.5 RECOVERY

- trusted or preferred path is returning
- guarded transition toward normal mode

### 7.6 TEARDOWN

- path removed
- TMU notified if capacity becomes unavailable

---

## 8. Failover and Recovery Rules

### 8.1 Failover Trigger Conditions

Failover MAY be triggered by:

- current route includes FAILED node
- current route includes CONGESTED node
- trusted route unavailable
- trust constraint violation
- degraded route becomes unacceptable
- policy-based escalation

### 8.2 Recovery Trigger Conditions

Recovery MAY be triggered by:

- trusted route becomes available again
- trusted route remains stable for required consecutive steps
- recovery counter threshold satisfied
- optional throughput / stability / confidence thresholds satisfied

### 8.3 Controlled Recovery

Recovery MUST be gradual.

RCU MUST avoid abrupt oscillation between DEGRADED and NORMAL.

---

## 9. Safety and Stability Rules

RCU MUST preserve operational safety.

It MUST support:

- route-switch suppression under small improvement
- anti-oscillation behavior
- degraded fallback as controlled exception
- deterministic reaction to route loss
- stable recovery behavior

RCU SHOULD fall back to conservative route control
if upstream decision context becomes unavailable.

---

## 10. Decision Guarantees

RCU MUST operate under deterministic routing decision principles.

- identical effective inputs SHOULD produce identical route decisions
- current route re-evaluation MUST be included in the decision basis
- route decision order MUST be fixed
- no decision cycle may end in undefined route state

### 10.1 Deterministic Fallback

If primary candidate selection fails:

- RCU MUST either

  - select an allowed degraded fallback route, or
  - return a controlled no-route outcome to upper layers

Uncontrolled undefined routing is prohibited.

### 10.2 Deterministic Switching Order

RCU MUST process route decisions in a stable order, such as:

1. current route re-evaluation
2. best route computation
3. policy filtering
4. hysteresis / margin comparison
5. degraded / fallback logic
6. Resolver override handling
7. final route decision

---

## 11. Auditability

RCU decisions MUST be explainable and traceable.

Each decision record SHOULD include:

- current selected route
- current selected route cost
- best route
- best route cost
- improvement value
- applied margin
- policy phase
- degraded / recovery mode state
- final decision
- final reason

RCU SHOULD log:

- KEEP decisions
- SWITCH decisions
- DEGRADED_SWITCH decisions
- ESCALATE_SWITCH decisions
- fallback reasons
- recovery reasons

---

## 12. Future Work

- adaptive trust / risk weighting refinement
- degraded recovery enhancement using throughput / trust confidence
- multi-route candidate comparison expansion
- topology-dependent failover parameterization
- multipath extension beyond single selected route
- integration with broader PSC Fabric Control Architecture

---

End of v0.1
