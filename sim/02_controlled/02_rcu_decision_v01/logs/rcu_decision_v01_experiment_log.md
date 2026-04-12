# RCU Decision v0.1 Experiment Log

```bash
python3 mini_psc_rcu_decision_v01.py
```
```text
=== STEP 0 ===
[FILTER]
[INIT] select=B score=0.772 mode=NORMAL

=== STEP 1 ===
[FILTER]
[DECISION] decision=ESCALATE_SWITCH selected=B best=B score_gap=0.028 reason=AMBIGUOUS_TOP_CANDIDATES

=== STEP 2 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.663 best_score=0.694
  improvement=0.031
  selected_stability=0.560
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.531 best_score=0.694
  improvement=0.164
  selected_stability=0.245
  persistence=1
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.451 best_score=0.694
  improvement=0.243
  selected_stability=0.140
  persistence=2
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 5 ===
[FILTER]
[CHECK]
  selected=B best=A
  selected_score=0.362 best_score=0.694
  improvement=0.332
  selected_stability=0.035
  persistence=3
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=B best=A
  selected_score=0.330 best_score=0.694
  improvement=0.364
  selected_stability=0.000
  persistence=4
  mode=NORMAL
[DECISION] decision=SWITCH from=B to=A reason=IMPROVEMENT_AND_PERSISTENT_DEGRADATION

=== STEP 7 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 8 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
  reject=C reasons=TRUST_LOW
[CHECK]
  selected=A best=A
  selected_score=0.694 best_score=0.694
  improvement=0.000
  selected_stability=0.900
  persistence=0
  mode=NORMAL
[DECISION] decision=KEEP reason=HYSTERESIS_HOLD
```

## Summary

- Initial selection favored Path B due to higher performance.
- An ESCALATE_SWITCH decision occurred when the score gap between top candidates was below the configured epsilon threshold.
- Path B gradually degraded over time, but switching did not occur immediately.
- Path C was rejected from STEP 6 onward due to low trust.
- Switching from Path B to Path A occurred only after:
  - the alternative path showed sufficient improvement
  - the selected path stability dropped below threshold
  - degradation persisted beyond the configured limit
- After switching, the system remained stable on Path A.
- This confirms that filtering, escalation, hysteresis, and persistence-based switching are functioning as intended.

---
