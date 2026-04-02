# RCU Decision v0.1 Degraded Experiment Log

```bash
python3 mini_psc_rcu_decision_v01.py
```
```text
=== STEP 0 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 1 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 2 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 3 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 4 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 5 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 6 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 7 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 8 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

=== STEP 9 ===
[FILTER]
  reject=A reasons=TRUST_LOW
  reject=B reasons=TRUST_LOW
[DECISION] decision=NO_ROUTE reason=NO_VALID_PATH mode=DEGRADED

```

## Summary

- All paths were rejected due to low trust, resulting in zero valid candidates.
- The RCU correctly entered DEGRADED mode and consistently returned NO_ROUTE.
- No switching, escalation, or evaluation was performed after filtering.
- This confirms that the system safely handles scenarios with no valid paths.
- The behavior demonstrates fail-safe operation under invalid telemetry conditions.

---
