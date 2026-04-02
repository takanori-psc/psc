# RCU Decision v0.1 Degraded Switch Experiment Log

```bash
python3 mini_psc_rcu_decision_v01.py
```
```text
=== STEP 0 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 1 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 2 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 3 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 4 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 5 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 6 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 7 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 8 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED

=== STEP 9 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=DEGRADED_SWITCH to=B score=0.718 reason=NO_TRUSTED_PATH mode=DEGRADED
```

## Summary

- All trusted paths were rejected due to low trust.
- The RCU did not return NO_ROUTE because fallback paths with valid health were available.
- The system consistently selected Path B as the degraded fallback path.
- This confirms that DEGRADED_SWITCH works as intended when no trusted path exists but healthy fallback paths remain.
- The behavior demonstrates survival-oriented fallback routing under degraded trust conditions.
