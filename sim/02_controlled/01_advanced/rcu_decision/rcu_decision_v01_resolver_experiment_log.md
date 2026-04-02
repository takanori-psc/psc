# RCU Decision v0.1 Resolver Experiment Log
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
[DECISION] decision=RESOLVED_SWITCH to=A reason=RESOLVER_DECISION

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 6 ===
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

- Initial selection favored Path B due to higher performance.
- At STEP 1, competing paths had similar scores, triggering ESCALATE.
- The Resolver was invoked to resolve ambiguity.
- The Resolver selected Path A based on higher stability.
- The system switched to Path A using RESOLVED_SWITCH.
- Subsequent steps maintained Path A consistently using KEEP.
- This confirms that Resolver-based decision-making works correctly.
- The system successfully integrates rule-based control and higher-level decision logic.

---
