# RCU Decision v0.1 Degraded Rule Validation Log

## Purpose

Validate degraded-mode behavior when a previously selected path becomes untrusted or invalid.

```
python3 mini_psc_rcu_decision_v01_degraded.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=B score=0.526 mode=NORMAL
[ECMP] selected=B

=== STEP 1 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.526 best_score=0.526
  improvement=0.000
  selected_stability=0.800
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.526 best_score=0.526
  improvement=0.000
  selected_stability=0.800
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 3 ===
[FILTER]
  reject=B reasons=TRUST_LOW
[STATE] rule=RULE-07_DEGRADE_trigger reason=SELECTED_REJECTED mode=DEGRADED
[DECISION] rule=RULE-09_DEGRADE_switch from_=INVALID to=A score_best=0.460 reason=SELECTED_REJECTED mode=DEGRADED
[ECMP] selected=A

=== STEP 4 ===
[RECOVERY] stable trusted path detected
[STATE] rule=RULE-10_RECOVERY_trigger to=A reason=STABLE_TRUSTED_PATH mode=NORMAL
[ECMP] selected=A

=== STEP 5 ===
[FILTER]
  reject=B reasons=TRUST_LOW
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=2 reason=RECOVERY_COOLDOWN
[ECMP] selected=A

=== STEP 6 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=1 reason=RECOVERY_COOLDOWN
[ECMP] selected=A

=== STEP 7 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[CHECK]
  selected=A best=A
  selected_score=0.460 best_score=0.460
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=A

=== STEP 8 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[CHECK]
  selected=A best=A
  selected_score=0.460 best_score=0.460
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=A

=== STEP 9 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[CHECK]
  selected=A best=A
  selected_score=0.460 best_score=0.460
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=A
```
