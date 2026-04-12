# RCU Decision v0.2 Recovery Return Validation Log

```
python3 mini_psc_rcu_decision_v02_recovery.py
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
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[CHECK]
  selected=A best=A
  selected_score=0.460 best_score=0.460
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=DEGRADED
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 5 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[CHECK]
  selected=A best=A
  selected_score=0.460 best_score=0.460
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=DEGRADED
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 6 ===
[RECOVERY] rule=RULE-15_RECOVERY_CANDIDATE candidate=B step=1 reason=STABLE_TRUSTED_PATH
[ECMP] selected=B

=== STEP 7 ===
[RECOVERY] rule=RULE-16_RECOVERY_VALIDATION_START candidate=B step=2 required=2
[RECOVERY] rule=RULE-18_RETURN_ELIGIBLE candidate=B reason=VALIDATION_PASSED
[FILTER]
[DECISION] rule=RULE-19_RETURN_SWITCH from_=A to=B improvement=0.152 reason=RECOVERY_RETURN_ELIGIBLE
[ECMP] selected=B

=== STEP 8 ===
[FILTER]
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=2 reason=RECOVERY_COOLDOWN
[ECMP] selected=B

=== STEP 9 ===
[FILTER]
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=1 reason=RECOVERY_COOLDOWN
[ECMP] selected=B
```
