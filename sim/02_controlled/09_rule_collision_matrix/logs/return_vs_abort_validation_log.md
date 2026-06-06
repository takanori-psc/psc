# Validation Log: return_vs_abort

- Scenario name: return_vs_abort
- Description: Return Ramp hold collides with an abort condition; abort must win by priority.
- Registered rules: RULE-01_KEEP_score, RULE-02_SWITCH_score, RULE-03_SWITCH_trust, RULE-04_BLOCK_trust, RULE-05_ESCALATE_conflict, RULE-22_RETURN_RAMP_HOLD, RULE-23_RETURN_RAMP_ABORT, RULE-24_RETURN_RAMP_COMPLETE

## Step 0

### Triggered rules

- rule_id=RULE-02_SWITCH_score action=SWITCH_TO_B priority=40 reason=score_gap=0.12 >= switch_margin=0.10
- rule_id=RULE-22_RETURN_RAMP_HOLD action=RETURN_RAMP_HOLD priority=50 reason=return ramp remains active while completion is not confirmed
- rule_id=RULE-23_RETURN_RAMP_ABORT action=RETURN_RAMP_ABORT priority=90 reason=abort_signal=true; telemetry_conflict=true confidence=reduced; recovered_path_stability=0.55 < ramp_abort_stability=0.60

### Suppressed rules

- rule_id=RULE-22_RETURN_RAMP_HOLD action=RETURN_RAMP_HOLD priority=50 reason=return ramp remains active while completion is not confirmed
- rule_id=RULE-02_SWITCH_score action=SWITCH_TO_B priority=40 reason=score_gap=0.12 >= switch_margin=0.10

- Final action: RETURN_RAMP_ABORT
- Expected action: RETURN_RAMP_ABORT
- Result: PASS

## Overall PASS
