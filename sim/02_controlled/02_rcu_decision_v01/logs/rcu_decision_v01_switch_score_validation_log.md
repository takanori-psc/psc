# RCU Decision v0.1 SWITCH Score Validation Log

Purpose:

- Validate `RULE-02_SWITCH_score` with a dedicated NORMAL-mode scenario.
- Confirm that PSC keeps the selected path when `score_gap < switch_threshold`.
- Confirm that PSC switches to the best path when `score_gap >= switch_threshold`.
- Keep degraded, recovery, cooldown, and resolver escalation behavior out of scope for this scenario.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/02_controlled/02_rcu_decision_v01/mini_psc_rcu_decision_v01_switch_score.py
```

Trace:

```text
=== STEP 0 ===
[INIT] step=0 selected_path=A selected_score=0.700 mode=NORMAL

=== STEP 1 ===
[DECISION] rule=RULE-01_KEEP_score step=1 selected_path=A best_path=B selected_score=0.700 best_score=0.750 score_gap=0.050 switch_threshold=0.100 decision=KEEP reason=SCORE_GAP_BELOW_THRESHOLD triggered_rule=RULE-01_KEEP_score

=== STEP 2 ===
[DECISION] rule=RULE-02_SWITCH_score step=2 selected_path=A best_path=B selected_score=0.700 best_score=0.840 score_gap=0.140 switch_threshold=0.100 decision=SWITCH reason=SCORE_GAP_THRESHOLD_MET triggered_rule=RULE-02_SWITCH_score
```

Validation Result:

| Step | selected_path | best_path | selected_score | best_score | score_gap | switch_threshold | decision | reason | triggered_rule |
|------|---------------|-----------|----------------|------------|-----------|------------------|----------|--------|----------------|
| 0 | A | A | 0.700 | 0.700 | 0.000 | 0.100 | INIT | INITIAL_SELECTION | - |
| 1 | A | B | 0.700 | 0.750 | 0.050 | 0.100 | KEEP | SCORE_GAP_BELOW_THRESHOLD | RULE-01_KEEP_score |
| 2 | A | B | 0.700 | 0.840 | 0.140 | 0.100 | SWITCH | SCORE_GAP_THRESHOLD_MET | RULE-02_SWITCH_score |

Audit Conclusion:

- STEP 1 validates the negative threshold case: B is better, but `score_gap=0.050` is below `switch_threshold=0.100`, so PSC keeps A using `RULE-01_KEEP_score`.
- STEP 2 validates the positive threshold case: B is clearly better, and `score_gap=0.140` is above `switch_threshold=0.100`, so PSC switches A -> B using `RULE-02_SWITCH_score`.
- No degraded, recovery, cooldown, or resolver escalation behavior appears in this trace.

---
