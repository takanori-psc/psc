# Validation Log: trust_block_vs_switch

- Scenario name: trust_block_vs_switch
- Description: RULE-04_BLOCK_trust collides with score and trust switch candidates; trust block must win by priority.
- Registered rules: RULE-01_KEEP_score, RULE-02_SWITCH_score, RULE-03_SWITCH_trust, RULE-04_BLOCK_trust, RULE-05_ESCALATE_conflict, RULE-22_RETURN_RAMP_HOLD, RULE-23_RETURN_RAMP_ABORT, RULE-24_RETURN_RAMP_COMPLETE

## Step 0

### Triggered rules

- rule_id=RULE-02_SWITCH_score action=SWITCH_TO_B priority=40 reason=score_gap=0.14 >= switch_margin=0.10
- rule_id=RULE-03_SWITCH_trust action=SWITCH_TO_B priority=65 reason=trust[B]=0.92 >= trust_switch_threshold=0.80 and trust[B] > trust[A]=0.60
- rule_id=RULE-04_BLOCK_trust action=BLOCK_SWITCH priority=80 reason=B in trust_blocked_paths

### Suppressed rules

- rule_id=RULE-03_SWITCH_trust action=SWITCH_TO_B priority=65 reason=trust[B]=0.92 >= trust_switch_threshold=0.80 and trust[B] > trust[A]=0.60
- rule_id=RULE-02_SWITCH_score action=SWITCH_TO_B priority=40 reason=score_gap=0.14 >= switch_margin=0.10

- Final action: BLOCK_SWITCH
- Expected action: BLOCK_SWITCH
- Result: PASS

## Overall PASS
