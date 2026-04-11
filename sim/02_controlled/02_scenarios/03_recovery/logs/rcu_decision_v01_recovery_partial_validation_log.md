# RCU Decision v0.1 Recovery Partial Validation Log

## Purpose

Validate intermediate recovery behavior after degraded-mode transition.
This log confirms recovery cooldown and hysteresis hold, but does not yet demonstrate path switching back to B.

```
python3 mini_psc_rcu_decision_v01_recovery.py
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
  selected_stability=0.950
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
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 3 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[STATE] rule=RULE-07_DEGRADE_trigger reason=SELECTED_REJECTED mode=DEGRADED
[DECISION] rule=RULE-09_DEGRADE_switch from_=INVALID to=A score_best=0.460 reason=SELECTED_REJECTED mode=DEGRADED
[ECMP] selected=B

=== STEP 4 ===
[RECOVERY] stable trusted path detected
[STATE] rule=RULE-10_RECOVERY_trigger to=A reason=STABLE_TRUSTED_PATH mode=NORMAL
[ECMP] selected=B

=== STEP 5 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=2 reason=RECOVERY_COOLDOWN
[ECMP] selected=B

=== STEP 6 ===
[FILTER]
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=1 reason=RECOVERY_COOLDOWN
[ECMP] selected=B

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.460 best_score=0.526
  improvement=0.066
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.066 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.460 best_score=0.526
  improvement=0.066
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.066 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=A best=B
  selected_score=0.460 best_score=0.526
  improvement=0.066
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.066 reason=HYSTERESIS_HOLD
[ECMP] selected=B
```
