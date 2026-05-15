# PSC RCU Decision Model v0.3 Progressive Recovery Ramp Validation Log

## Scenario: baseline

Observed behavior:
- Recovery candidate detected at step 6
- Validation completed at step 7
- Ramp started with recovered_weight=0.10
- Ramp advanced to recovered_weight=0.30

Result:
- Progressive recovery ramp behavior confirmed.

---

## Scenario: ramp_abort

Observed behavior:
- Ramp started successfully
- Recovered path stability dropped to 0.550 at step 9
- RULE-23_RETURN_RAMP_ABORT triggered
- Traffic fallback behavior confirmed

Result:
- Ramp abort protection behavior validated.

---

## Scenario: ramp_complete

Observed behavior:
- Ramp advanced progressively from recovered_weight=0.10 to 1.00
- Ramp hold behavior observed between increment steps
- RULE-24_RETURN_RAMP_COMPLETE triggered at step 17
- evacuation_weight reached 0.00

Result:
- Full progressive reintegration behavior validated.
- Controlled recovery completion confirmed.

---

## Key Observation

Unlike immediate recovery return behavior,
PSC v0.3 progressively reintegrates recovered paths through staged traffic allocation and continuous observation.

The recovery process remains abortable during reintegration, allowing fallback protection if recovered path stability degrades during ramp progression.