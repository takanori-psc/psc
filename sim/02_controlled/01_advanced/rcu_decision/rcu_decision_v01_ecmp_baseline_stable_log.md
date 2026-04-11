# RCU Decision v0.1 Ecmp Baseline Stable Log

## Scenario

Stable environment where the best path does not change significantly.

## Expected Behavior

- ECMP: Selects the current best path (no oscillation expected)
- PSC: Maintains the selected path with hysteresis and stability control

## Observation

- Both ECMP and PSC converge to the same path (B)
- No oscillation is observed in either method
- PSC does not introduce unnecessary switching

## Interpretation

This result confirms that PSC behaves consistently with ECMP in stable conditions,
without introducing additional instability.

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.510 mode=NORMAL
[ECMP] selected=A

=== STEP 1 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=TRUST_CONFLICT score_gap=0.036 trust_gap=0.350 stability_gap=0.000 best=B selected=A
[DECISION] rule=RULE-14_RESOLVER_switch from_=A to=B reason=RESOLVER_DECISION
[ECMP] selected=B

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
[ECMP] selected=B

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
[ECMP] selected=B

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
[ECMP] selected=B

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
[ECMP] selected=B

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
[ECMP] selected=B

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
[ECMP] selected=B

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
[ECMP] selected=B

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
[ECMP] selected=B
```
---
