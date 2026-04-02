# RCU Decision v0.1 Recovery Experiment Log

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
[RECOVERY] stable trusted path detected
[DECISION] decision=RECOVER to=B reason=STABLE_TRUSTED_PATH mode=NORMAL

=== STEP 4 ===
[FILTER]
[ESCALATE] invoking resolver
[DECISION] decision=RESOLVED_SWITCH to=A reason=RESOLVER_DECISION

=== STEP 5 ===
[FILTER]
[ESCALATE] invoking resolver
[DECISION] decision=RESOLVED_SWITCH to=A reason=RESOLVER_DECISION

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

- Initially, all paths were rejected due to low trust, triggering DEGRADED mode.
- The system selected a fallback path and maintained it using DEGRADED_KEEP.
- At STEP 3, trust values recovered, enabling valid paths.
- The system successfully transitioned from DEGRADED to NORMAL mode using RECOVER.
- Immediately after recovery, ESCALATE was triggered due to competing candidates.
- The Resolver selected Path A based on stability.
- This confirms that recovery logic is functioning correctly.
- However, the absence of a post-recovery stabilization period leads to immediate re-evaluation.
- Introducing a recovery cooldown period is recommended to improve control stability.
---
