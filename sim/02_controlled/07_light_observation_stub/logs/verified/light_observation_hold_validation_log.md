# PSC LIGHT Observation Hold Validation Log

## Overview

This validation records runnable LIGHT observation scenarios that must keep the
return ramp in Hold.

The scenarios are separate from the earlier design stubs and do not modify
existing validated recovery ramp simulations.

---

## Scenario: light_false_negative

Observed behavior:
- observation_mode=LIGHT
- Actual path instability exists
- LIGHT observation fails to detect the instability directly
- RULE-22_RETURN_RAMP_HOLD triggered
- category=hold
- reason=OBSERVATION_FALSE_NEGATIVE

Result:
- LIGHT false negatives do not advance the return ramp.
- Hold behavior confirmed.

---

## Scenario: light_stale_telemetry

Observed behavior:
- observation_mode=LIGHT
- Telemetry is present but outdated
- Confidence is insufficient for ramp advance
- RULE-22_RETURN_RAMP_HOLD triggered
- category=hold
- reason=STALE_TELEMETRY

Result:
- Stale LIGHT telemetry does not advance the return ramp.
- Hold behavior confirmed.

---

## Scenario: light_masked_instability

Observed behavior:
- observation_mode=LIGHT
- Stability proxy appears healthy
- Hidden instability exists
- Resolver cannot safely advance the return ramp
- RULE-22_RETURN_RAMP_HOLD triggered
- category=hold
- reason=MASKED_INSTABILITY

Result:
- Masked LIGHT instability does not advance the return ramp.
- Hold behavior confirmed.

---

## Key Observation

LIGHT observation can produce insufficient, outdated, or misleading evidence.
Under those conditions PSC must emit `RULE-22_RETURN_RAMP_HOLD` and keep the
scenario in the `hold` category.
