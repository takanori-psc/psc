# RCU Decision v0.1 Resolver Stability Conflict Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.771 mode=NORMAL

=== STEP 1 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.728 best_score=0.728
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD
```
## Summary

- Resolver was not triggered in this scenario.
- Path A remained both selected and best under normal RCU scoring.
- The intended stability conflict did not occur.
- This result suggests that stability has a strong effect on final_score in the current weighting.
- A dedicated step-specific conflict case is needed to validate STABILITY_CONFLICT escalation.
---
