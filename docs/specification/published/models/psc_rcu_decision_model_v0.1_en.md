# PSC RCU Decision Model v0.1 (English Version)

## 1. Document Information

- Document Name   : PSC RCU Decision Model
- Version         : v0.1
- Project         : PSC (Photon System Controller)
- Layer           : PSCOS / PSC Fabric
- Document Type   : Specification / Model
- Status          : Draft
- Author          : T. Hirose
- Created         : 2026-04-02
- Last Updated    : 2026-04-02
- Language        : English

---

## 2. Objective

This model defines the path selection and switching decision logic of the RCU (Routing Control Unit).

The RCU evaluates path candidates based on telemetry and determines whether to keep the current Selected Path or switch to a new Best Path.

---

## 3. Basic Structure

The RCU decision process consists of the following three stages.

1. Candidate Filtering
2. Score Evaluation
3. Switching Decision

---

## 4. Candidate Filtering

The RCU removes unusable paths before score calculation.

### 4.1 Rejection Conditions

A path is rejected if any of the following conditions is met.

- trust violation
- node failure
- policy violation
- hard stale telemetry
- route unavailable

### 4.2 Rules

```text
If trust_violation(path) = true, reject path.
If node_failure(path) = true, reject path.
If policy_violation(path) = true, reject path.
If telemetry_state(path) = hard_invalid, reject path.
```

If no candidate remains, the RCU outputs `NO_ROUTE` or `ESCALATE_SWITCH`.

---

## 5. Score Evaluation

All metrics MUST be normalized to [0, 1] before evaluation
and MUST maintain consistent scaling across all paths.
The RCU evaluates the following three scores for valid path candidates.

- CongestionScore(path)
- PerformanceScore(path)
- StabilityScore(path)

### 5.1 Congestion Benefit

Since a lower CongestionScore is better, it is inverted during integration.

```text
CongestionBenefit(path) = 1 - CongestionScore(path)
```

### 5.2 Final Score

```text
FinalScore(path) =
  Wc * CongestionBenefit(path) +
  Wp * PerformanceScore(path) +
  Ws * StabilityScore(path)
```

### 5.3 Initial Weights

```text
Wc = 0.4
Wp = 0.3
Ws = 0.3
```

---

## 6. Best Path and Selected Path

The RCU distinguishes the following two paths.

- Best Path
  The path with the highest FinalScore at the current time

- Selected Path
  The path currently in use

The Best Path and the Selected Path do not need to be the same.

---

## 7. Switching Decision

The RCU does not switch immediately even if a Best Path exists.
It makes the decision based on improvement, stability, and persistence.

### 7.1 Improvement

```text
Improvement =
  FinalScore(BestPath) - FinalScore(SelectedPath)
```

### 7.2 Switch Condition

```text
If Improvement > switch_margin
  AND StabilityScore(SelectedPath) < switch_stability_threshold
  AND persistence_degradation(SelectedPath) > persistence_limit
then SWITCH
else KEEP
```

### 7.3 Return Condition

```text
If Improvement > return_margin
  AND StabilityScore(BestPath) > return_stability_threshold
  AND persistence_recovery(BestPath) > recovery_limit
then RETURN or SWITCH_BACK
```

### 7.4 Initial Example Values

```text
switch_margin = 0.10
return_margin = 0.15

switch_stability_threshold = 0.40
return_stability_threshold = 0.60

persistence_limit = 3 cycles
recovery_limit = 5 cycles
```

Return conditions must be stricter than switch conditions.

---

## 8. Decision Outputs

The RCU has the following outputs.

- KEEP
- SWITCH
- DEGRADED_SWITCH
- ESCALATE_SWITCH
- NO_ROUTE

---

## 9. Resolver Escalation

If the RCU cannot make a safe decision by itself, it delegates the decision to the Resolver.

### 9.1 Escalation Conditions

- no trusted route
- multiple candidates with similar score
- degraded-only candidates
- policy conflict
- unstable telemetry confidence
- repeated switch attempts without convergence

### 9.2 Rules

```text
If no trusted route exists, escalate.
If score difference between top candidates < epsilon, escalate.
If only degraded paths remain, escalate.
If repeated switching does not converge, escalate.
```

---

## 10. Conclusion

This model enables the RCU to provide the following.

- candidate rejection based on constraints
- path evaluation based on multiple scores
- stable switching decisions using hysteresis

---

## 11. Next Steps

- integration into the full RCU Model
- implementation in simulation
- refinement of Resolver interaction conditions
