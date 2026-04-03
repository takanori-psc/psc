RCU Decision v0.1 Resolver Trust Escalation Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.771 mode=NORMAL

=== STEP 1 ===
[FILTER]
[ESCALATE] reason=TRUST_CONFLICT score_gap=0.005 trust_gap=0.350
[DECISION] decision=RESOLVED_SWITCH to=B reason=RESOLVER_DECISION

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.769 best_score=0.769
  improvement=0.000
  selected_stability=0.870
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD
```

## Summary

- Resolver was triggered only once under a trust conflict condition.
- The selected path switched from A to B by resolver decision.
- After the resolved switch, the system remained stable and kept B.
- Unnecessary repeated escalation was not observed.
- Trust-based escalation worked as intended in this scenario.

---
