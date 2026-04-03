# RCU Decision v0.1 Resolver Stability Conflict Cooldown Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.510 mode=NORMAL

=== STEP 1 ===
[FILTER]
[ESCALATE] reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350
[DECISION] decision=RESOLVED_KEEP reason=RESOLVER_SAME_SELECTION

=== STEP 2 ===
[FILTER]
[RESOLVER_COOLDOWN] remaining=2
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
[RESOLVER_COOLDOWN] remaining=1
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
[ESCALATE] reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350
[DECISION] decision=RESOLVED_KEEP reason=RESOLVER_SAME_SELECTION

=== STEP 5 ===
[FILTER]
[RESOLVER_COOLDOWN] remaining=2
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
[RESOLVER_COOLDOWN] remaining=1
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
[ESCALATE] reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350
[DECISION] decision=RESOLVED_KEEP reason=RESOLVER_SAME_SELECTION

=== STEP 8 ===
[FILTER]
[RESOLVER_COOLDOWN] remaining=2
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
[RESOLVER_COOLDOWN] remaining=1
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

- STABILITY_CONFLICT escalation was successfully triggered and handled by the Resolver.
- Resolver correctly maintained the selected path based on stability considerations.
- Resolver cooldown mechanism effectively suppressed redundant escalations.
- The system demonstrates stable and periodic escalation behavior with proper cooldown control.
- This confirms that the separation between RCU and Resolver responsibilities is functioning as designed.

---
