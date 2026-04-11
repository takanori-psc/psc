# RCU Decision v0.1 Resolver Switch Rule Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.510 mode=NORMAL

=== STEP 1 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=TRUST_CONFLICT score_gap=0.036 trust_gap=0.350 stability_gap=0.000 best=B selected=A
[DECISION] rule=RULE-14_RESOLVER_switch from_=A to=B reason=RESOLVER_DECISION

=== STEP 2 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.506 best_score=0.506
  improvement=0.000
  selected_stability=0.600
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD
```

## Summary

- RULE-05_ESCALATE_conflict was triggered by a trust conflict under near-equal scoring conditions between competing paths.
- Resolver decisions are now fully expressed using RULE-based logging, and RULE-14_RESOLVER_switch correctly switched the selection from A to B.
- RULE-12_COOLDOWN_active prevented repeated escalation immediately after Resolver intervention.
- RULE-01_KEEP_score maintained stable operation after the Resolver-driven switch.
- This log confirms that Resolver switch decisions are fully integrated into the RULE framework, completing both KEEP and SWITCH validation within the unified decision model.

---
