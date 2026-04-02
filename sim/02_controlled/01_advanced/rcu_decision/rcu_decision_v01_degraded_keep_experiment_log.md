# RCU Decision v01 Degraded Keep Experiment Log

```
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 1 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 2 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 3 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 4 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 5 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 6 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 7 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 8 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 9 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_KEEP selected=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED
```

## Summary

- All trusted paths were rejected due to low trust.
- A fallback path (Path B) was selected in DEGRADED mode.
- The initial decision triggered DEGRADED_SWITCH.
- Subsequent decisions correctly transitioned to DEGRADED_KEEP.
- The system maintained a stable fallback path without unnecessary switching.
- This confirms that degraded-mode hysteresis and state retention are functioning correctly.
- The behavior demonstrates stable survival-oriented control under degraded conditions.

---
