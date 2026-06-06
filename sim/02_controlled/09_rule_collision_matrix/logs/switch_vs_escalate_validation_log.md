# Validation Log: switch_vs_escalate

- Scenario name: switch_vs_escalate
- Description: RULE-02_SWITCH_score and RULE-05_ESCALATE_conflict trigger together; escalation must win by priority.
- Registered rules: RULE-02_SWITCH_score, RULE-05_ESCALATE_conflict, RULE-22_RETURN_RAMP_HOLD, RULE-23_RETURN_RAMP_ABORT, RULE-24_RETURN_RAMP_COMPLETE

## Step 0

### Triggered rules

- rule_id=RULE-02_SWITCH_score action=SWITCH_TO_B priority=40 reason=score_gap=0.04 >= switch_margin=0.03
- rule_id=RULE-05_ESCALATE_conflict action=ESCALATE_TO_RESOLVER priority=70 reason=TRUST_CONFLICT with score_gap=0.04 < epsilon=0.05

### Suppressed rules

- rule_id=RULE-02_SWITCH_score action=SWITCH_TO_B priority=40 reason=score_gap=0.04 >= switch_margin=0.03

- Final action: ESCALATE_TO_RESOLVER
- Expected action: ESCALATE_TO_RESOLVER
- Result: PASS

## Overall PASS
