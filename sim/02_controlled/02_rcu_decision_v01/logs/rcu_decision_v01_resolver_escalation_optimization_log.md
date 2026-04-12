# RCU Decision v0.1 Resolver Escalation Optimization Log

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
[COOLDOWN] holding after recovery (2)
[DECISION] decision=KEEP reason=RECOVERY_COOLDOWN

=== STEP 5 ===
[FILTER]
[COOLDOWN] holding after recovery (1)
[DECISION] decision=KEEP reason=RECOVERY_COOLDOWN

=== STEP 6 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.718 best_score=0.718
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.718 best_score=0.718
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.718 best_score=0.718
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[CHECK]
  selected=B best=B
  selected_score=0.718 best_score=0.718
  improvement=0.000
  selected_stability=0.730
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD
```

## Summary

- No unnecessary Resolver escalation observed (ESCALATE count = 0)
- KEEP (HYSTERESIS_HOLD) correctly maintained when best == selected
- Stable state transitions confirmed: Degraded → Recover → Cooldown → Normal
- No regression observed in existing control logic

- No test case triggered the Resolver escalation condition (score_gap < epsilon and best != selected)
- Resolver behavior (RESOLVED_KEEP / RESOLVED_SWITCH) remains unverified

→ Next step: validate behavior under conditions that reliably trigger Resolver escalation
---
