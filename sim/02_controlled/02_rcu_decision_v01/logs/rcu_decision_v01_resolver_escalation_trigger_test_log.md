# RCU Decision v0.1 Resolver Escalation Trigger Test_log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.771 mode=NORMAL

=== STEP 1 ===
[FILTER]
[ESCALATE] invoking resolver
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

- Resolver escalation was successfully triggered under the intended condition
- Resolver selected path B and the decision was correctly reflected as RESOLVED_SWITCH
- After the Resolver-based switch, the system remained stable with selected == best
- No unnecessary repeated escalation or switching was observed after convergence

- This test confirms that the Resolver escalation path and post-switch stabilization work as intended

→ Next step: refine escalation conditions by incorporating additional factors such as trust gap and stability gap

---
