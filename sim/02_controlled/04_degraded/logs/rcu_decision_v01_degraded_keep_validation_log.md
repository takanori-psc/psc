# RCU Decision v0.1 DEGRADED Keep Validation Log

Purpose:

- Validate `RULE-08_DEGRADE_keep` with a dedicated DEGRADED-mode scenario.
- Show the difference between `RULE-09_DEGRADE_switch` and `RULE-08_DEGRADE_keep`.
- Confirm that DEGRADED keep is not the same as NORMAL-mode `RULE-01_KEEP_score`.
- Confirm that PSC keeps the current degraded path when it remains health-valid and the alternative path is not recovery eligible.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/02_controlled/04_degraded/mini_psc_rcu_decision_v01_degraded_keep.py
```

Trace:

```text
=== STEP 0 ===
[INIT] step=0 mode=NORMAL selected_path=A selected_score=0.700 selected_trust=0.900 selected_health=1

=== STEP 1 ===
[STATE] rule=RULE-07_DEGRADE_trigger step=1 mode=DEGRADED selected_path=A selected_trust=0.200 selected_health=0 reason=SELECTED_UNSAFE triggered_rule=RULE-07_DEGRADE_trigger
[DECISION] rule=RULE-09_DEGRADE_switch step=1 mode=DEGRADED selected_path=A candidate_path=B selected_score=0.720 candidate_score=0.620 score_gap=-0.100 selected_trust=0.200 candidate_trust=0.450 selected_health=0 candidate_health=1 decision=SWITCH reason=CURRENT_PATH_UNSAFE_HEALTH_INVALID triggered_rule=RULE-09_DEGRADE_switch

=== STEP 2 ===
[DECISION] rule=RULE-08_DEGRADE_keep step=2 mode=DEGRADED selected_path=B candidate_path=A selected_score=0.620 candidate_score=0.660 score_gap=0.040 switch_threshold=0.100 selected_trust=0.450 candidate_trust=0.620 selected_health=1 candidate_health=1 decision=KEEP reason=CURRENT_DEGRADED_PATH_HEALTHY_AND_CANDIDATE_NOT_RECOVERY_ELIGIBLE triggered_rule=RULE-08_DEGRADE_keep
```

Validation Result:

| Step | mode | selected_path | candidate_path | selected_score | candidate_score | score_gap | selected_trust | candidate_trust | selected_health | candidate_health | decision | reason | triggered_rule |
|------|------|---------------|----------------|----------------|-----------------|-----------|----------------|-----------------|-----------------|------------------|----------|--------|----------------|
| 0 | NORMAL | A | - | 0.700 | - | - | 0.900 | - | 1 | - | INIT | INITIAL_SELECTION | - |
| 1 | DEGRADED | A | B | 0.720 | 0.620 | -0.100 | 0.200 | 0.450 | 0 | 1 | SWITCH | CURRENT_PATH_UNSAFE_HEALTH_INVALID | RULE-09_DEGRADE_switch |
| 2 | DEGRADED | B | A | 0.620 | 0.660 | 0.040 | 0.450 | 0.620 | 1 | 1 | KEEP | CURRENT_DEGRADED_PATH_HEALTHY_AND_CANDIDATE_NOT_RECOVERY_ELIGIBLE | RULE-08_DEGRADE_keep |

Audit Conclusion:

- STEP 1 validates the switch case: selected path A becomes unsafe because `health=0` and `trust=0.200`; PSC enters DEGRADED mode and selects fallback B using `RULE-09_DEGRADE_switch`.
- STEP 2 validates the keep case: PSC is already in DEGRADED mode, current degraded path B remains health-valid, and candidate A is only partially recovered.
- Candidate A has a slightly better score (`score_gap=0.040`) and valid health, but `candidate_trust=0.620` is below the recovery trust threshold, so it is not sufficient for recovery or return.
- PSC therefore keeps B using `RULE-08_DEGRADE_keep`.
- No NORMAL-mode `RULE-01_KEEP_score`, recovery, cooldown, or resolver escalation behavior appears in this trace.

---
