# RCU Decision v0.1 Recovery Cooldown Experiment Log
```
Python3 mini_psc_rcu_decision_v01.py
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
[RECOVERY] stable trusted path detected
[DECISION] decision=RECOVER to=B reason=STABLE_TRUSTED_PATH mode=NORMAL

=== STEP 4 ===
[FILTER]
[COOLDOWN] holding after recovery (2)
[DECISION] decision=KEEP reason=RECOVERY_COOLDOWN

=== STEP 5 ===
[FILTER]
[COOLDOWN] holding after recovery (1)
[DECISION] decision=KEEP reason=RECOVERY_COOLDOWN

=== STEP 6 ===
[FILTER]
[ESCALATE] invoking resolver
[DECISION] decision=RESOLVED_SWITCH to=A reason=RESOLVER_DECISION

=== STEP 7 ===
[FILTER]
[ESCALATE] invoking resolver
[DECISION] decision=RESOLVED_SWITCH to=A reason=RESOLVER_DECISION

=== STEP 8 ===
[FILTER]
[ESCALATE] invoking resolver
[DECISION] decision=RESOLVED_SWITCH to=A reason=RESOLVER_DECISION

=== STEP 9 ===
[FILTER]
[ESCALATE] invoking resolver
[DECISION] decision=RESOLVED_SWITCH to=A reason=RESOLVER_DECISION
```

## Summary

---
