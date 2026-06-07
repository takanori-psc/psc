# PSC RCU Decision Model v0.1

## Internal Processing Steps

Operational `RULE-*` IDs are defined by the current Evidence Matrix / validation namespace.
The `STEP-*` IDs in this published model describe internal RCU processing stages only and
must not be treated as operational rule identifiers.

This document clarifies the PSC score model and resolver priority logic without changing
existing `RULE-*` ownership, verified evidence, or simulation logs.

---

## 0. Layered Decision Structure

PSC path decisions are organized into four layers. The layers are evaluated in order,
and later layers must not re-admit a path that failed a hard exclusion in an earlier layer.

| Layer | Name | Primary criteria | Purpose |
|-------|------|------------------|---------|
| Layer 1 | Eligibility | trust threshold, policy compliance, verification state, `trust_block` | Exclude paths that must not participate in selection |
| Layer 2 | Normal Selection | `final_score` from congestion benefit and performance | Select normal candidates during non-ambiguous operation |
| Layer 3 | Resolver Selection | `resolver_score` from trust, stability, and performance | Select or keep a path when Resolver is active |
| Layer 4 | Recovery Selection | `return_score` from stability, trust, and performance | Decide controlled return after recovery validation |

### 0.1 Eligibility

Eligibility is evaluated before scoring.

- Paths below the trust threshold are excluded.
- Paths with policy violations, failed verification state, invalid health, or `trust_block`
  are excluded from normal selection.
- Regulatory violation risk is treated as a policy violation for trust and policy evaluation.
- `trust_score` and `trust_block` are separate concepts:
  - `trust_score` is a preference or penalty factor.
  - `trust_block` is a hard exclusion condition below threshold or after severe violation.

### 0.2 Normal Selection Score

`final_score` is the normal candidate selection score.

```text
final_score =
  Wc * (1 - congestion_score) +
  Wp * performance_score
```

`stability_score` is not a primary component of the normal `final_score` in this clarified
v0.1/v0.2 decision model. Stability remains important for hysteresis, eligibility,
Resolver activation, Resolver arbitration, and Recovery return.

`cost_score` and `power_score` are optional future extensions. They are not part of the
core v0.1/v0.2 `final_score` decision.

### 0.3 Stability Score

`stability_score` is derived from observation history, not a single instantaneous sample.

```text
instability = f(variance, trend, duration)
stability_score = 1 - instability
```

Observation records used for stability evaluation must carry timestamps. Implementations are
expected to evaluate stability through an Observation-side ring buffer or time window. The
window length is a configurable parameter and is not fixed by this model.

### 0.4 Resolver Score

When Resolver is active, Resolver selection prioritizes `resolver_score`, not `final_score`.

Resolver active conditions include, but are not limited to:

- trust conflict
- stability degradation
- ambiguous score result
- Resolver-related rule activation such as `RULE-05`, `RULE-06`, or `RULE-14`

```text
resolver_score =
  Wr_trust * trust_score +
  Wr_stability * stability_score +
  Wr_performance * performance_score

where Wr_trust > Wr_stability > Wr_performance
```

Paths below the trust threshold are excluded before `resolver_score` comparison.

### 0.5 Return Score

Recovery return uses `return_score`, which is separate from normal `final_score`.

```text
return_score =
  Wret_stability * stability_score +
  Wret_trust * trust_score +
  Wret_performance * performance_score

where Wret_stability > Wret_trust > Wret_performance
```

`return_score` is a recovery return decision score. It must not be treated as the normal
candidate selection score.

---

## 1. Path Validity Steps

### STEP-01_TRUST_HEALTH_FILTER: Trust / Health Filtering

Paths that do not satisfy the minimum trust or health requirements must not be considered for normal selection.

- Condition:

  - `trust < trust_threshold`
  - `trust_block == true`
  - `policy_violation == true`
  - `verification_state == failed`
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
