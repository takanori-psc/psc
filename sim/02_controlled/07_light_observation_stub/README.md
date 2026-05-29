# PSC LIGHT Observation Scenario Stub

## Purpose

This directory defines the minimum scenario structure for validating LIGHT
observation before `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` can leave Hold.

The files in this directory are design stubs, not verified evidence. They are
intended to connect the LIGHT observation boundary draft to runnable simulation
cases without changing the current recovery ramp implementation prematurely.

## Scope

LIGHT validation starts from the existing progressive recovery ramp behavior in:

```text
sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py
```

The first runnable implementation should reuse that model where possible and add
only the LIGHT-specific stimulus needed for these risks:

- false negative
- telemetry gap
- stale telemetry
- masked instability
- delayed abort
- resolver escalation

## Proposed Structure

```text
sim/02_controlled/07_light_observation_stub/
  README.md
  light_scenario_manifest.md
  expected_category_helper_spec.md
```

Future runnable files should be added only after the scenario manifest is stable:

```text
mini_psc_light_observation_scenarios.py
logs/
  rcu_decision_v04_light_observation_validation_log.md
  raw/light_observation_run.txt
```

## Connection To Existing Scenarios

Existing recovery ramp scenarios remain the baseline:

- `ramp_abort_full_stability_dip` proves FULL conservative abort behavior.
- `ramp_light_tolerates_moderate_dip` demonstrates current LIGHT advance behavior.
- `ramp_abort_light_hard_failure` proves LIGHT can still abort on severe instability.

The LIGHT stub extends those cases with missing-input and ambiguous-evidence
conditions. Until those are runnable or manually traceable, LIGHT advance stays
classified as Hold in the Evidence Matrix.

## Runnable Stubs

`light_telemetry_gap_stub.py` is a minimal LIGHT-only scenario for required
telemetry input loss during an active recovery ramp. Missing required telemetry
must emit `RULE-22_RETURN_RAMP_HOLD` and must not emit
`RULE-21_RETURN_RAMP_ADVANCE`.

`light_stale_telemetry_stub.py` is a separate LIGHT-only scenario for telemetry
that is present but no longer usable. Stale telemetry must also emit
`RULE-22_RETURN_RAMP_HOLD` and must not emit `RULE-21_RETURN_RAMP_ADVANCE`.

Run them with:

```bash
python3 sim/02_controlled/07_light_observation_stub/light_telemetry_gap_stub.py
python3 sim/02_controlled/07_light_observation_stub/light_stale_telemetry_stub.py
```
