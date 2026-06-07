# PSC RCU Decision Model v0.3 FULL vs LIGHT Observation Validation Log

## Overview

This validation compares FULL and LIGHT observation modes during progressive recovery ramp behavior.

The objective is to verify whether observation policy differences affect recovery reintegration behavior under identical recovery conditions.

Historical status note:
This log records an experimental v0.3 behavior snapshot. In particular,
`ramp_light_tolerates_moderate_dip` shows LIGHT observation triggering
`RULE-21_RETURN_RAMP_ADVANCE`. That behavior has been superseded as current
expected policy by the Fast Mode LIGHT Boundary and Evidence Matrix position:
LIGHT observation must emit or resolve to `RULE-22_RETURN_RAMP_HOLD` unless it
is promoted to FULL observation or explicit LIGHT promotion gates are defined
and satisfied.

---

## Observation Mode Definitions

### FULL

- Conservative observation policy
- Uses stricter recovery ramp abort thresholds
- Compatible with existing PSC v0.3 behavior

### LIGHT

- Reduced observation sensitivity
- Allows moderate instability during recovery ramp
- Intended for lightweight or lower-cost observation environments

---

## Scenario: ramp_abort_full_stability_dip

Observed behavior:
- observation_mode=FULL
- Recovery ramp started normally
- Recovered path stability dropped to 0.650 at step 9
- RULE-23_RETURN_RAMP_ABORT triggered immediately

Result:
- FULL observation mode aborted reintegration on moderate instability.
- Conservative recovery protection behavior confirmed.

---

## Scenario: ramp_light_tolerates_moderate_dip

Historical experimental scenario:
This scenario is retained as evidence of the earlier v0.3 LIGHT advance
experiment. It is not the current expected LIGHT policy.

Observed behavior:
- observation_mode=LIGHT
- Recovery ramp started normally
- Recovered path stability dropped to 0.650 at step 9
- Ramp continued without abort
- RULE-21_RETURN_RAMP_ADVANCE triggered

Result:
- LIGHT observation mode tolerated moderate instability.
- Reduced observation sensitivity behavior confirmed.

---

## Scenario: ramp_abort_light_hard_failure

Observed behavior:
- observation_mode=LIGHT
- Recovery ramp started normally
- Recovered path stability dropped to 0.550 at step 9
- RULE-23_RETURN_RAMP_ABORT triggered

Result:
- LIGHT observation mode still aborts on severe instability.
- Minimum recovery protection behavior confirmed.

---

## Key Observation

Under identical recovery conditions, different observation policies produced different recovery reintegration behavior.

FULL observation mode prioritized conservative safety behavior, while LIGHT observation mode prioritized recovery continuity under moderate instability conditions.

This validation demonstrates that PSC recovery behavior can be influenced not only by path telemetry, but also by observation policy configuration.
