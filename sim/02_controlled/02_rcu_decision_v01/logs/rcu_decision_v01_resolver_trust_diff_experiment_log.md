# RCU Decision v0.1 Resolver Trust Diff Experiment Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=B score=0.772 mode=NORMAL

=== STEP 1 ===
[FILTER]
[ESCALATE] invoking resolver
[DECISION] decision=RESOLVED_SWITCH to=B reason=RESOLVER_DECISION

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.663 best_score=0.694
  improvement=0.031
  selected_stability=0.560
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.531 best_score=0.694
  improvement=0.164
  selected_stability=0.245
  persistence=1
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.451 best_score=0.694
  improvement=0.243
  selected_stability=0.140
  persistence=2
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.362 best_score=0.694
  improvement=0.332
  selected_stability=0.035
  persistence=3
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=B best=A
  selected_score=0.330 best_score=0.694
  improvement=0.364
  selected_stability=0.000
  persistence=4
  mode=NORMAL
[DECISION] decision=SWITCH from=B to=A reason=IMPROVEMENT_AND_PERSISTENT_DEGRADATION

=== STEP 7 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD
```

## Summary

- A trust difference was introduced between Path A and Path B.
- At STEP 1, ESCALATE triggered Resolver-based decision making.
- The Resolver selected Path B due to higher trust, despite lower stability.
- The system initially followed the trust-prioritized decision.
- As Path B degraded over time, the RCU maintained the path due to hysteresis.
- Eventually, persistent degradation triggered a SWITCH to Path A.
- This confirms that trust-aware Resolver influences initial decision, while RCU enforces stability over time.
- The system demonstrates proper separation of decision policy (Resolver) and control logic (RCU).
---
