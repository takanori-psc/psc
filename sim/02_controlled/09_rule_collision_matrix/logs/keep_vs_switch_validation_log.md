# Validation Log: keep_vs_switch

- Scenario name: keep_vs_switch
- Description: RULE-01_KEEP_score and RULE-02_SWITCH_score trigger together; score switch must win by priority.
- Registered rules: RULE-01_KEEP_score, RULE-02_SWITCH_score, RULE-03_SWITCH_trust, RULE-04_BLOCK_trust, RULE-05_ESCALATE_conflict, RULE-22_RETURN_RAMP_HOLD, RULE-23_RETURN_RAMP_ABORT, RULE-24_RETURN_RAMP_COMPLETE

## Step 0

### Triggered rules

- rule_id=RULE-01_KEEP_score action=KEEP_CURRENT priority=20 reason=keep_score_recommended=true current_path=A
- rule_id=RULE-02_SWITCH_score action=SWITCH_TO_B priority=40 reason=score_gap=0.12 >= switch_margin=0.10

### Suppressed rules

- rule_id=RULE-01_KEEP_score action=KEEP_CURRENT priority=20 reason=keep_score_recommended=true current_path=A

- Final action: SWITCH_TO_B
- Expected action: SWITCH_TO_B
- Result: PASS

## Overall PASS
