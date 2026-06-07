# PSC RCU Decision Model v0.1

## Internal Processing Steps

Operational `RULE-*` IDs are defined by the current Evidence Matrix / validation namespace.
The `STEP-*` IDs in this published model describe internal RCU processing stages only and
must not be treated as operational rule identifiers.

---

## 1. Path Validity Steps

### STEP-01_TRUST_HEALTH_FILTER: Trust / Health Filtering

Paths that do not satisfy the minimum trust or health requirements must not be considered for normal selection.

- Condition:

  - `trust < trust_threshold`
  - `health == 0`
- Action:

  - Exclude from valid path set

---

### STEP-02_NO_VALID_PATH_DEGRADED_MODE: No Valid Path → Degraded Mode

If no valid paths exist, the system must enter DEGRADED mode.

- If fallback paths (`health != 0`) exist:

  - Select best fallback path
- Otherwise:

  - Return `NO_ROUTE`
- Mode:

  - `DEGRADED`

---

### STEP-03_SELECTED_PATH_INVALID_REPLACEMENT: Selected Path Invalid → Immediate Replacement

If the currently selected path becomes invalid, it must not be retained.

- Action:

  - Switch to best valid path
- Mode:

  - `DEGRADED`

---

## 2. Normal Selection Steps

### STEP-04_INITIAL_SELECTION: Initial Selection

When no path is selected:

- Action:

  - Select path with highest `final_score`
- Mode:

  - `NORMAL`

---

### STEP-05_SMALL_IMPROVEMENT_KEEP: No Switch on Small Improvement

A path must not be switched if the improvement is below threshold.

- Condition:

  - `improvement <= switch_margin`
- Action:

  - KEEP

---

### STEP-06_PERSISTENT_DEGRADATION_SWITCH: Persistent Degradation Required for Switch

Switching must only occur when degradation is sustained.

- Conditions:

  - `best != selected`
  - `improvement > switch_margin`
  - `stability(selected) < switch_stability_threshold`
  - `degradation_counter > persistence_limit`
- Action:

  - SWITCH

---

### STEP-07_DEGRADATION_COUNTER: Degradation Counter Behavior

Degradation must be tracked over time.

- If:
  - `stability < switch_stability_threshold` → increment counter
  - otherwise → reset counter

---

## 3. Resolver Steps

### STEP-08_RESOLVER_ACTIVATION: Resolver Activation Conditions

Resolver must only be invoked under ambiguity conditions.

- Conditions:

  - `score_gap < epsilon`
  - `best != selected`
  - `(trust_gap > 0.1 OR stability_gap > 0.2)`
  - `resolver_cooldown == 0`

---

### STEP-09_RESOLVER_SAME_SELECTION_KEEP: Same Selection → No Switch

If Resolver returns the currently selected path:

- Action:

  - `RESOLVED_KEEP`
- No switching is allowed

---

### STEP-10_RESOLVER_DRIVEN_SWITCH: Resolver-Driven Switch

Switching is only allowed when Resolver selects a different path.

- Action:

  - `RESOLVED_SWITCH`

---

### STEP-11_RESOLVER_COOLDOWN: Resolver Cooldown

After Resolver execution:

- Action:
  - Set resolver cooldown to a fixed number of steps
    (`resolver_cooldown = resolver_cooldown_steps`)

- Default:
  - `resolver_cooldown_steps = 2`

- Behavior:
  - While cooldown is active:
    - Resolver must not be re-invoked

---

## 4. Degraded / Recovery Steps

### STEP-12_RECOVERY_CONDITION: Recovery Condition

Recovery from DEGRADED mode requires stable and trusted paths.

- Condition:

  - `stability > recovery_stability_threshold`
- Action:

  - Select best candidate
  - Transition to NORMAL

---

### STEP-13_RECOVERY_COOLDOWN: Recovery Cooldown

After recovery:

- Action:
  - Set recovery cooldown to a fixed number of steps
    (`recovery_cooldown_counter = recovery_cooldown_steps`)

- Default:
  - `recovery_cooldown_steps = 2`

- Behavior:
  - While cooldown is active:
    - No switching is allowed

---

### STEP-14_FALLBACK_BEHAVIOR: Fallback Behavior

In DEGRADED mode:

- Trust filtering is explicitly relaxed as an exception rule
- Paths with valid health (`health != 0`) must be considered

- Action:
  - Select the best path from fallback candidates using `final_score`

- Constraint:
  - Health validation must always be enforced

---

## 5. Scoring Steps

### STEP-15_RCU_RESOLVER_LOGIC_SEPARATION: Separation of RCU and Resolver Logic

RCU and Resolver must not use identical evaluation logic.

- RCU:

  - `congestion + performance`
- Resolver:

  - `trust + stability + performance`

---

### STEP-16_STABILITY_ESCALATION_MODEL: Stability Escalation Model (v0.1)

Stability must not be absorbed into RCU scoring.

- Stability conflicts must be escalated to Resolver
- This is a deliberate design choice in v0.1

---

## Notes

- These steps define the published model's internal processing stages
- Parameter values (e.g., thresholds, margins) are defined separately
- The system must always behave consistently with these steps
- Operational `RULE-*` IDs, including `RULE-01_KEEP_score`, are defined by the
  Evidence Matrix / validation namespace and are authoritative for validation.

---
