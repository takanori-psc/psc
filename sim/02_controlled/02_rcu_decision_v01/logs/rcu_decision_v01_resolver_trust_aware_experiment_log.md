# RCU Decision v0.1 Resolver Trust Aware Experiment Log

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
- The trust-aware Resolver was executed successfully.
- The overall behavior remained unchanged because the competing paths had no meaningful trust difference in this test.
- As a result, the Resolver continued to favor Path A based on higher stability.
- This confirms that the trust-aware extension did not break existing Resolver behavior.
- A dedicated differential-trust test is required to verify trust-sensitive path selection.
---
