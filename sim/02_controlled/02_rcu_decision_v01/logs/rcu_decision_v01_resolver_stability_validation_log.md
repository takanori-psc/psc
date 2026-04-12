# RCU Decision v0.1 Resolver Stability Validation Log

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
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.788 best_score=0.788
  improvement=0.000
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD
```

## Summary

- Resolver was not triggered in this scenario.
- Path A became the best path under the normal RCU scoring logic.
- Therefore, no stability conflict escalation occurred.
- This log confirms that increased stability can directly affect normal path selection.
- A new test case is needed where best and selected differ while stability_gap remains significant.

---
