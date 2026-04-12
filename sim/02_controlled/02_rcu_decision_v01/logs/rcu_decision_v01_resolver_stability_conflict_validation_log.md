# RCU Decision v0.1 Resolver Stability Conflict Validation Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.510 mode=NORMAL

=== STEP 1 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

```
## Summary

- A conflict scenario between selected path A and best path B was successfully created.
- However, Resolver was not triggered because score_gap (0.036) exceeded epsilon (0.03).
- This indicates that the escalation threshold is slightly too strict for this scenario.
- Adjusting epsilon or reducing score_gap is required to trigger STABILITY_CONFLICT.
---
