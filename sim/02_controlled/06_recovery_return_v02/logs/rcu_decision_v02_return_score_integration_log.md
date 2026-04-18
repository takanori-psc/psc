# RCU Decision v0.2 Return Score Integration Log

## Purpose
Validate separation of recovery evaluation from final_score

## Scenario

- Path A: stable, moderate performance, trust=0.8
- Path B: degraded (step < 6), then recovers (trust=0.95, high performance)
- Single recovery candidate scenario (B only)

## Key Observation

[RECOVERY] rule=RULE-15_RECOVERY_CANDIDATE candidate=B step=1 return_score=0.956 reason=STABLE_TRUSTED_PATH

## Result

- return_score successfully applied to candidate selection
- no behavioral regression observed
- recovery flow unchanged under single-candidate condition

## Note

Single-candidate scenario does not demonstrate evaluation divergence.
Multi-candidate validation required.