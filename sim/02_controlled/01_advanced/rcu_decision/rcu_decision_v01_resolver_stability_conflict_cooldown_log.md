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

- STABILITY_CONFLICT escalation was triggered under near-equal scoring conditions between competing paths.
- Resolver correctly returned `RESOLVED_KEEP`, maintaining the current path based on stability-oriented evaluation.
- Resolver cooldown successfully suppressed redundant escalations for subsequent steps.
- During cooldown, the system maintained stability using `HYSTERESIS_HOLD`.
- This log confirms that the separation between RCU ambiguity detection and Resolver decision logic is functioning as designed in PSC RCU Decision Model v0.1.

---
