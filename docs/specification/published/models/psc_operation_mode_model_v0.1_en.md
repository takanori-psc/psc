# PSC Operation Mode Model v0.1 (Draft)

---

## Document Information

- Document Name: PSC Operation Mode Model
- Version: v0.1
- Project: PSC (Photon System Controller)
- Layer: PSC Fabric / Control Model
- Status: Draft
- Author: T. Hirose
- Language: English

---

## 1. Purpose

This specification defines the operational states (Operation Modes) of the PSC Fabric and specifies the allowed routing behavior, fallback mechanisms, and recovery operations in each state.

This model functions as a higher-level control layer above the Routing Model, Trust Model, and Resolver Model, ensuring overall system stability, reliability, and continuity.

---

## 2. Scope

This specification covers:

- Definition of operation modes in PSC Fabric
- Allowed actions and restrictions for each mode
- State transition conditions
- Recovery and stability validation behavior

This specification does NOT cover:

- Routing algorithms (Routing Model)
- Trust evaluation logic (Trust Model)
- Route cost calculation
- Internal Resolver algorithms

---

## 3. Operation Modes

PSC defines the following operation modes:

### 3.1 NORMAL

Normal operating state.

- Assumes the availability of trusted routes
- Standard policies (latency / stability) are applied
- Hysteresis is enabled
- Degraded fallback is prohibited

---

### 3.2 TRUST_FAILURE

State where no trusted route is available.

- The assumption of normal operation is broken
- No trusted route exists as a routing result
- Escalation to Resolver is triggered

Note:
This state is primarily a transient state and typically transitions immediately to DEGRADED or another operational state.

---

### 3.3 DEGRADED

Degraded operation state.

- Fallback is allowed based on Resolver decision
- allow_untrusted_fallback is enabled
- Route selection may consider trust weight
- Connectivity is prioritized over strict trust constraints

---

### 3.4 RECOVERY

Recovery validation state.

- Entered after trusted routes become available again
- Immediate transition to NORMAL is not allowed
- Stability must be verified over a period of time

---

## 4. Mode Definitions

### 4.1 NORMAL

Allowed actions:

- Use trusted routes only
- Apply policy (latency / stability)
- Apply hysteresis
- Perform standard route switching

Restrictions:

- Use of untrusted routes is prohibited
- Degraded fallback is not allowed

---

### 4.2 TRUST_FAILURE

State where no trusted route is available.

This state is a transient state triggered when the loss of trusted routes is detected.
It typically transitions quickly to DEGRADED or another state.
It functions as a trigger for fault detection and Resolver decision-making.

Allowed actions:

- Attempt to discover trusted routes
- Notify Resolver

Restrictions:

- Normal communication cannot be maintained
- Fallback is not yet permitted

---

### 4.3 DEGRADED

Allowed actions:

- Use untrusted / limited routes (conditionally)
- Perform route selection considering trust weight
- Apply degraded-specific switching criteria

Restrictions:

- Reduction in security level is allowed
- Standard policy criteria may not be strictly applied
- In DEGRADED mode, trust constraints may be partially relaxed to prioritize connectivity,
  but the allowed scope is restricted by policy and Resolver decisions

---

### 4.4 RECOVERY

Allowed actions:

- Monitor trusted routes
- Perform stability validation (counter-based / time-based)

Restrictions:

- Immediate transition to NORMAL is prohibited
- If instability is detected, transition back to DEGRADED

---

## 5. State Transition Conditions

### 5.1 NORMAL → TRUST_FAILURE

Condition:

- No trusted route is available

---

### 5.2 TRUST_FAILURE → DEGRADED

Condition:

- Resolver allows fallback

---

### 5.3 DEGRADED → RECOVERY

Condition:

- Trusted route becomes available again
- Recovery trigger conditions are met

---

### 5.4 RECOVERY → NORMAL

Condition:

- Trusted route remains stable for a defined period
- Example: consecutive successful steps (RECOVERY_REQUIRED_STEPS)

---

### 5.5 RECOVERY → DEGRADED

Condition:

- Trusted route becomes unavailable or unstable again

---

## 6. Inputs and Outputs

### 6.1 Inputs

- Routing results (best route / cost)
- Trusted route loss events
- Trusted route recovery events
- Trust level information
- Policy evaluation results
- Hysteresis evaluation results
- Resolver override decisions
- Node states (NORMAL / BUSY / CONGESTED)

---

### 6.2 Outputs

- Current operation mode
- Enforcement of trusted-only constraint
- Fallback enable / disable
- Route switching allow / hold
- Recovery start / continue / abort

---

## 7. Recovery and Stability Policy

- Recovery must be performed gradually, not instantly
- Stability evaluation may use:
  - Consecutive success count
  - Time-based validation
  - Error rate
- If instability is detected, the system transitions back to DEGRADED

---

## 8. Design Principles

- Separation of routing and control
- Balance between safety and continuity
- Explicit state transition definitions
- Resilience against transient fluctuations (hysteresis / recovery)

---

## 9. Open Design Items

- Whether TRUST_FAILURE should remain a state or be treated as an event
- Recovery criteria (time-based vs count-based)
- Detailed policy behavior in DEGRADED mode
- Integration with Fabric State Model (CALM / WARM / HOT / EMERGENCY)

