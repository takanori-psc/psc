# PSC RCU Decision Model v0.1

## Absolute Rules

---

## 1. Path Validity Rules

### RULE-01: Trust / Health Filtering

Paths that do not satisfy the minimum trust or health requirements must not be considered for normal selection.

- Condition:

  - `trust < trust_threshold`
  - `health == 0`
- Action:

  - Exclude from valid path set

---

### RULE-02: No Valid Path → Degraded Mode

If no valid paths exist, the system must enter DEGRADED mode.

- If fallback paths (`health != 0`) exist:

  - Select best fallback path
- Otherwise:

  - Return `NO_ROUTE`
- Mode:

  - `DEGRADED`

---

### RULE-03: Selected Path Invalid → Immediate Replacement

If the currently selected path becomes invalid, it must not be retained.

- Action:

  - Switch to best valid path
- Mode:

  - `DEGRADED`

---

## 2. Normal Selection Rules

### RULE-04: Initial Selection

When no path is selected:

- Action:

  - Select path with highest `final_score`
- Mode:

  - `NORMAL`

---

### RULE-05: No Switch on Small Improvement

A path must not be switched if the improvement is below threshold.

- Condition:

  - `improvement <= switch_margin`
- Action:

  - KEEP

---

### RULE-06: Persistent Degradation Required for Switch

Switching must only occur when degradation is sustained.

- Conditions:

  - `best != selected`
  - `improvement > switch_margin`
  - `stability(selected) < switch_stability_threshold`
  - `degradation_counter > persistence_limit`
- Action:

  - SWITCH

---

### RULE-07: Degradation Counter Behavior

Degradation must be tracked over time.

- If:

  - `stability < threshold` → increment counter
  - otherwise → reset counter

---

## 3. Resolver Rules

### RULE-08: Resolver Activation Conditions

Resolver must only be invoked under ambiguity conditions.

- Conditions:

  - `score_gap < epsilon`
  - `best != selected`
  - `(trust_gap > threshold OR stability_gap > threshold)`
  - `resolver_cooldown == 0`

---

### RULE-09: Same Selection → No Switch

If Resolver returns the currently selected path:

- Action:

  - `RESOLVED_KEEP`
- No switching is allowed

---

### RULE-10: Resolver-Driven Switch

Switching is only allowed when Resolver selects a different path.

- Action:

  - `RESOLVED_SWITCH`

---

### RULE-11: Resolver Cooldown

After Resolver execution:

- Action:

  - Set cooldown (`resolver_cooldown > 0`)
- During cooldown:

  - Resolver must not be re-invoked

---

## 4. Degraded / Recovery Rules

### RULE-12: Recovery Condition

Recovery from DEGRADED mode requires stable and trusted paths.

- Condition:

  - `stability > recovery_stability_threshold`
- Action:

  - Select best candidate
  - Transition to NORMAL

---

### RULE-13: Recovery Cooldown

After recovery:

- Action:

  - Enforce cooldown period
- During cooldown:

  - No switching allowed

---

### RULE-14: Fallback Behavior

In DEGRADED mode:

- Trust filtering may be relaxed
- Health must still be valid

---

## 5. Scoring Rules

### RULE-15: Separation of RCU and Resolver Logic

RCU and Resolver must not use identical evaluation logic.

- RCU:

  - `congestion + performance`
- Resolver:

  - `trust + stability + performance`

---

### RULE-16: Stability Escalation Model (v0.1)

Stability must not be absorbed into RCU scoring.

- Stability conflicts must be escalated to Resolver
- This is a deliberate design choice in v0.1

---

## Notes

- These rules define **non-negotiable behavior constraints**
- Parameter values (e.g., thresholds, margins) are defined separately
- The system must always behave consistently with these rules

---
