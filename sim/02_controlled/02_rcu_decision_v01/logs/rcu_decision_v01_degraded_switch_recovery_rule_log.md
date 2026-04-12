# RCU Decision v0.1 Degraded Switch Recovery Rule Log

```Bash
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] rule=RULE-09_DEGRADE_switch to=B score=0.499 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 1 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] rule=RULE-08_DEGRADE_keep selected=B score=0.499 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 2 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] rule=RULE-08_DEGRADE_keep selected=B score=0.499 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 3 ===
[RECOVERY] stable trusted path detected
[STATE] rule=RULE-10_RECOVERY_trigger to=B reason=STABLE_TRUSTED_PATH mode=NORMAL

=== STEP 4 ===
[FILTER]
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=2 reason=RECOVERY_COOLDOWN

=== STEP 5 ===
[FILTER]
[STATE] rule=RULE-11_RECOVERY_cooldown remaining=1 reason=RECOVERY_COOLDOWN

=== STEP 6 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.499 best_score=0.499
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.499 best_score=0.499
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.499 best_score=0.499
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.499 best_score=0.499
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=B best=B improvement=0.000 reason=HYSTERESIS_HOLD
```

## Summary

- RULE-09_DEGRADE_switch was triggered when no trusted paths were available, selecting a fallback path under degraded conditions.
- RULE-08_DEGRADE_keep maintained the selected fallback path during continued degraded state without unnecessary switching.
- RULE-10_RECOVERY_trigger was activated once stability and trust conditions were restored, transitioning the system back to NORMAL mode.
- RULE-11_RECOVERY_cooldown prevented immediate re-evaluation after recovery, stabilizing the transition.
- After recovery, RULE-01_KEEP_score maintained stable operation through hysteresis, confirming no unnecessary switching.
- This log demonstrates that PSC safely degrades under trust failure and recovers predictably without oscillation, validating the degraded-to-recovery control flow.

---
