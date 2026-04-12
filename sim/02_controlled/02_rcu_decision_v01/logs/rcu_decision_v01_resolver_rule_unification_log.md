# RCU Decision v0.1 Resolver Rule Unification Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.510 mode=NORMAL

=== STEP 1 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350 best=B selected=A
[DECISION] rule=RULE-13_RESOLVER_keep selected=A reason=RESOLVER_SAME_SELECTION

=== STEP 2 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350 best=B selected=A
[DECISION] rule=RULE-13_RESOLVER_keep selected=A reason=RESOLVER_SAME_SELECTION

=== STEP 5 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350 best=B selected=A
[DECISION] rule=RULE-13_RESOLVER_keep selected=A reason=RESOLVER_SAME_SELECTION

=== STEP 8 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD
```

## Summary

- RULE-05_ESCALATE_conflict correctly detects ambiguity between competing paths.
- Resolver decisions are now fully expressed using RULE-based logging (`RULE-13_RESOLVER_keep`), replacing previous non-RULE decision outputs.
- RULE-12_COOLDOWN_active prevents repeated escalation, stabilizing Resolver invocation.
- RULE-01_KEEP_score maintains stable operation through hysteresis after Resolver intervention.
- This log confirms that Resolver decision results are fully integrated into the RULE framework, completing the unified decision model.

---
