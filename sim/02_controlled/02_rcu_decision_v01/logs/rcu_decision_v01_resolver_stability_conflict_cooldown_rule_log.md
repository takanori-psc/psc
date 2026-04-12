# RCU Decision v0.1 Resolver Stability Conflict Cooldown Rule_Log

```Bash
python3 mini_psc_rcu_decision_v01.py
```
```
=== STEP 0 ===
[FILTER]
[INIT] select=A score=0.510 mode=NORMAL

=== STEP 1 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350 best=B selected=A
[DECISION] decision=RESOLVED_KEEP reason=RESOLVER_SAME_SELECTION

=== STEP 2 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 3 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 4 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350 best=B selected=A
[DECISION] decision=RESOLVED_KEEP reason=RESOLVER_SAME_SELECTION

=== STEP 5 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 6 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 7 ===
[FILTER]
[ESCALATE] rule=RULE-05_ESCALATE_conflict reason=STABILITY_CONFLICT score_gap=0.036 trust_gap=0.000 stability_gap=0.350 best=B selected=A
[DECISION] decision=RESOLVED_KEEP reason=RESOLVER_SAME_SELECTION

=== STEP 8 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=2 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

=== STEP 9 ===
[FILTER]
[STATE] rule=RULE-12_COOLDOWN_active remaining=1 reason=RESOLVER_COOLDOWN
[CHECK]
  selected=A best=B
  selected_score=0.470 best_score=0.506
  improvement=0.036
  selected_stability=0.950
  persistence=0
  mode=NORMAL
[DECISION] rule=RULE-01_KEEP_score selected=A best=B improvement=0.036 reason=HYSTERESIS_HOLD

```

## Summary

- RULE-05_ESCALATE_conflict was triggered under near-equal scoring conditions with a stability conflict between competing paths.
- Resolver returned a KEEP-equivalent decision (no path change), preserving the current selection without triggering a switch.
- RULE-12_COOLDOWN_active successfully suppressed repeated escalation in subsequent steps.
- During cooldown, RULE-01_KEEP_score maintained stable path selection through hysteresis control.
- This log demonstrates that ambiguity detection (RCU), decision resolution (Resolver), and stabilization (Cooldown + Hysteresis) operate consistently under the PSC RCU Decision Model v0.1.

---
