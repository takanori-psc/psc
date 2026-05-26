# RCU Decision v0.2 RETURN_KEEP Validation Log

Purpose:

- Validate `RULE-20_RETURN_KEEP` with a dedicated scenario.
- Confirm that a trusted, stable, and `RETURN_ELIGIBLE` recovery candidate does not cause a return switch when its score improvement is below `return_margin`.
- Distinguish this behavior from `RULE-19_RETURN_SWITCH`, which requires `improvement >= return_margin`.

Command:

```bash
python3 sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v02_return_keep.py
```

Trace:

```text
=== STEP 0 ===
[FILTER]
[INIT] selected_path=B selected_score=0.558 mode=NORMAL

=== STEP 1 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[STATE] rule=RULE-07_DEGRADE_trigger step=1 reason=SELECTED_REJECTED mode=DEGRADED
[DECISION] rule=RULE-09_DEGRADE_switch step=1 from_=INVALID to=A score=0.460 reason=SELECTED_REJECTED mode=DEGRADED

=== STEP 2 ===
[FILTER]
  reject=B reasons=TRUST_LOW,HEALTH_INVALID
[CHECK] step=2 selected_path=A best_path=A mode=DEGRADED

=== STEP 3 ===
[FILTER]
[RECOVERY] rule=RULE-15_RECOVERY_CANDIDATE step=3 candidate_path=B candidate_trust=0.950 candidate_stability=0.950 return_score=0.920 reason=STABLE_TRUSTED_PATH

=== STEP 4 ===
[FILTER]
[RECOVERY] rule=RULE-16_RECOVERY_VALIDATION_START step=4 candidate_path=B validation_step=2 required=2
[RECOVERY] rule=RULE-18_RETURN_ELIGIBLE step=4 candidate_path=B reason=VALIDATION_PASSED
[DECISION] rule=RULE-20_RETURN_KEEP step=4 selected_path=A candidate_path=B selected_score=0.460 candidate_score=0.498 improvement=0.038 return_margin=0.080 decision=KEEP reason=RETURN_MARGIN_NOT_MET triggered_rule=RULE-20_RETURN_KEEP
```

Validation Result:

| Item | Value |
|------|-------|
| selected_path | A |
| candidate_path | B |
| candidate_trust | 0.950 |
| candidate_stability | 0.950 |
| selected_score | 0.460 |
| candidate_score | 0.498 |
| improvement | 0.038 |
| return_margin | 0.080 |
| decision | KEEP |
| reason | RETURN_MARGIN_NOT_MET |
| triggered_rule | RULE-20_RETURN_KEEP |

Audit Conclusion:

- Candidate B is trusted, stable, and explicitly marked `RETURN_ELIGIBLE`.
- Candidate B has a higher score than selected path A, but the improvement is below `return_margin`.
- PSC keeps selected path A.
- `RULE-19_RETURN_SWITCH` is not triggered because the required switch condition `improvement >= return_margin` is not satisfied.
- This log provides step-based evidence for `RULE-20_RETURN_KEEP`.

---
