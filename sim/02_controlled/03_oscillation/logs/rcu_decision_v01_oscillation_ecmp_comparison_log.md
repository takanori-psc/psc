RCU Decision v0.1 Oscillation Scenario (ECMP vs PSC) Log

## Scenario

Path B has higher performance but fluctuates periodically,
while Path A is more stable but slightly slower.

## Command

```bash
python3 mini_psc_rcu_decision_v01_oscillation.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=B score=0.530 mode=NORMAL
[ECMP] selected=B

=== STEP 1 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=TRUST_CONFLICT+STABILITY_CONFLICT score_gap=0.031 trust_gap=0.100 stability_gap=0.535 best=A selected=B
[DECISION] rule=RULE-14_RESOLVER_switch from_=B to=A reason=RESOLVER_DECISION
[ECMP] selected=A

=== STEP 2 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.484 best_score=0.530
  improvement=0.046
  selected_stability=0.935
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.046 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 3 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=A
  selected_score=0.484 best_score=0.484
  improvement=0.000
  selected_stability=0.935
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=A

=== STEP 4 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=TRUST_CONFLICT score_gap=0.046 trust_gap=0.100 stability_gap=0.035 best=B selected=A
[DECISION] rule=RULE-13_RESOLVER_keep selected=A reason=RESOLVER_SAME_SELECTION
[ECMP] selected=B

=== STEP 5 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=A
  selected_score=0.484 best_score=0.484
  improvement=0.000
  selected_stability=0.935
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=A

=== STEP 6 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.484 best_score=0.530
  improvement=0.046
  selected_stability=0.935
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.046 reason=HYSTERESIS_HOLD
[ECMP] selected=B

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=A best=A
  selected_score=0.484 best_score=0.484
  improvement=0.000
  selected_stability=0.935
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=A

=== STEP 8 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=TRUST_CONFLICT score_gap=0.046 trust_gap=0.100 stability_gap=0.035 best=B selected=A
[DECISION] rule=RULE-13_RESOLVER_keep selected=A reason=RESOLVER_SAME_SELECTION
[ECMP] selected=B

=== STEP 9 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=A
  selected_score=0.484 best_score=0.484
  improvement=0.000
  selected_stability=0.935
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=A improvement=0.000 reason=HYSTERESIS_HOLD
[ECMP] selected=A
```

## Summary

PSC:
  switch_count = 1

ECMP:
  switch_count = 9

## Observation

ECMP reacts to short-term fluctuations and switches frequently (9 switches in 10 steps).

PSC suppresses oscillation using resolver, hysteresis, and cooldown, resulting in stable path selection (1 switch).
