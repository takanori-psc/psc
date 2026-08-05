# PSC Recovery Abort Stabilization Validation Log

## Overview

This validation records Recovery Return Abort Handling scenarios.

The scenario is based on:

```text
docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_en.md
docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_ja.md
```

It validates that `RULE-23_RETURN_RAMP_ABORT` aborts the current Return Ramp
attempt without making immediate traffic cut the default behavior.

## Validation Target

- Rule: `RULE-23_RETURN_RAMP_ABORT`
- Scenarios: `soft_abort_hold_and_reobserve`, `hard_abort_ramp_down`,
  `emergency_cut_no_fallback`, `two_path_degraded_abort`
- Scenario files:
  `sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py`,
  `sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py`,
  `sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py`,
  `sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py`
- Validator: `scripts/validate_evidence_rules.py`
- Validator checks: `ScenarioCheck.name` in
  `soft_abort_hold_and_reobserve`, `hard_abort_ramp_down`,
  `emergency_cut_no_fallback`, `two_path_degraded_abort`

## Verified Scope

This Verified status covers the four FULL-observation abort classes reproduced
by the dedicated abort handling scenarios above: `SOFT_ABORT`, `HARD_ABORT`,
`EMERGENCY_CUT`, and `DEGRADED_ABORT`.

It does not cover:

- The `RULE-23_RETURN_RAMP_ABORT` emissions embedded inside the v0.3 recovery
  ramp engine (`reason=RECOVERED_PATH_UNSTABLE`,
  `reason=RECOVERED_PATH_INVALID` in
  `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py`),
  which remain Experimental evidence.
- `light_delayed_abort_stub.py`, which remains a LIGHT-specific design stub
  outside runnable evidence.

---

## Scenario: soft_abort_hold_and_reobserve

Initial state:

- Recovered Path A = 25%
- Stable Path B = 75%
- Return Ramp is active

Observed condition:

- telemetry conflict
- confidence reduction
- evidence is suspicious
- evidence is not conclusively unsafe

Observed behavior:

- `RULE-23_RETURN_RAMP_ABORT` triggered
- `category=abort_and_stabilize`
- `abort_class=SOFT_ABORT`
- `return_ramp_attempt=aborted`
- `immediate_cut=false`
- Traffic Stabilization Phase entered
- further Return Ramp Advance stopped
- current allocation held temporarily
- observation escalation requested
- Resolver re-evaluation triggered

Raw log:

```text
sim/02_controlled/08_recovery_abort_handling/logs/raw/soft_abort_hold_and_reobserve_run.txt
```

Result:

- RULE-23_RETURN_RAMP_ABORT emitted.
- Traffic Stabilization Phase entered.
- Traffic allocation remained temporarily unchanged.
- Observation escalation occurred.
- Resolver re-evaluation occurred.
- Validation outcome: PASS.

---

## Key Observation

In the SOFT_ABORT class, `RULE-23_RETURN_RAMP_ABORT` means that the current
Return Ramp attempt is aborted. It does not make immediate path cut the default
action.

PSC first stabilizes the traffic allocation, increases observation confidence,
and asks Resolver to re-evaluate the post-abort state.

---

## Scenario: hard_abort_ramp_down

Initial state:

- Recovered Path A = 25%
- Stable Path B = 75%
- Return Ramp is active

Observed condition:

- clear path instability
- link quality collapse
- evidence is conclusively unsafe
- forwarding is still possible
- condition is not EMERGENCY_CUT

Observed behavior:

- `RULE-23_RETURN_RAMP_ABORT` triggered
- `category=hard_abort_ramp_down`
- `abort_class=HARD_ABORT`
- `return_ramp_attempt=aborted`
- `immediate_cut=false`
- Traffic Stabilization Phase entered
- further Return Ramp Advance stopped
- suspect recovered Path A ramped down from 25% to 10%
- stable Path B increased from 75% to 90%
- Resolver re-evaluation triggered
- source-side PSC notification emitted

Raw log:

```text
sim/02_controlled/08_recovery_abort_handling/logs/raw/hard_abort_ramp_down_run.txt
```

Result:

- RULE-23_RETURN_RAMP_ABORT emitted.
- `abort_class=HARD_ABORT` confirmed.
- `immediate_cut=false` confirmed.
- Traffic Stabilization Phase entered.
- Recovered Path A weight was reduced from 25%.
- Stable Path B weight was increased from 75%.
- Resolver re-evaluation occurred.
- Source-side PSC notification occurred.
- Validation outcome: PASS.

---

## HARD_ABORT Observation

In the HARD_ABORT class, `RULE-23_RETURN_RAMP_ABORT` still aborts the current
Return Ramp attempt rather than defaulting to immediate cut.

Because forwarding remains possible, PSC enters Traffic Stabilization Phase,
ramps down the suspect recovered path, shifts traffic toward the known stable
allocation, triggers Resolver re-evaluation, and notifies source-side PSC that
traffic reduction may be needed under policy control.

---

## Scenario: emergency_cut_no_fallback

Initial state:

- Recovered Path A = 25%
- Stable Path B = 75%
- Return Ramp is active

Observed condition:

- Path A link down
- optical failure
- forwarding on Path A is not possible
- evidence is conclusively unsafe
- emergency condition is confirmed
- Path B exists
- Path B is not failed
- Path B has no capacity margin to absorb Path A traffic

Fallback failure class:

```text
NO_CAPACITY_MARGIN
```

Observed behavior:

- `RULE-23_RETURN_RAMP_ABORT` triggered
- `category=emergency_cut_no_fallback`
- `abort_class=EMERGENCY_CUT`
- `return_ramp_attempt=aborted`
- `immediate_cut=true`
- recovered Path A immediately excluded
- recovered Path A weight set from 25% to 0%
- stable Path B remains at 75%
- Path A traffic is not blindly transferred into Path B
- `fallback_transfer_allowed=false`
- `fallback_block_reason=NO_CAPACITY_MARGIN`
- normal soft/hard Traffic Stabilization Phase not entered
- Resolver emergency notification triggered
- source-side PSC emergency traffic control request emitted

Raw log:

```text
sim/02_controlled/08_recovery_abort_handling/logs/raw/emergency_cut_no_fallback_run.txt
```

Result:

- RULE-23_RETURN_RAMP_ABORT emitted.
- `abort_class=EMERGENCY_CUT` confirmed.
- `immediate_cut=true` confirmed.
- Path A was excluded.
- Path B remained available but could not absorb transferred traffic.
- `fallback_transfer_allowed=false` confirmed.
- `fallback_block_reason=NO_CAPACITY_MARGIN` confirmed.
- Source-side PSC emergency traffic control request occurred.
- Resolver emergency notification occurred.
- Traffic Stabilization Phase was not entered as the normal soft/hard abort phase.
- Validation outcome: PASS.

---

## EMERGENCY_CUT_NO_FALLBACK Observation

In the EMERGENCY_CUT class, PSC immediately excludes the unsafe recovered path.

When the remaining path exists but lacks capacity margin, PSC must not treat
fallback as a generic safe operation. It blocks transfer with
`fallback_block_reason=NO_CAPACITY_MARGIN`, notifies Resolver, and requests
source-side emergency traffic control.

---

## Abort Handling Level Summary

```text
SOFT_ABORT
-> Hold and Re-observe

HARD_ABORT
-> Ramp Down Suspect Path

EMERGENCY_CUT_NO_FALLBACK
-> Immediate Path Exclusion + Source-Side Emergency Traffic Control
```

---

## Scenario: two_path_degraded_abort

Initial state:

- Recovered Path A = 25%
- Stable Path B = 75%
- Return Ramp is active
- only two candidate paths exist
- no third path exists

Observed condition:

- Path A is unstable during Return Ramp
- Path B also shows degradation
- neither path is fully safe
- forwarding is still possible
- condition is not EMERGENCY_CUT

Fallback failure class:

```text
NO_SAFE_ALTERNATE
```

Observed behavior:

- `RULE-23_RETURN_RAMP_ABORT` triggered
- `category=two_path_degraded_arbitration`
- `abort_class=DEGRADED_ABORT`
- `return_ramp_attempt=aborted`
- `immediate_cut=false`
- Traffic Stabilization Phase entered
- further Return Ramp Advance stopped
- all traffic is not blindly moved to Path B
- `fallback_transfer_allowed=false`
- `fallback_block_reason=NO_SAFE_ALTERNATE`
- Resolver arbitration triggered
- `least_bad_selection=true`
- source-side traffic reduction request emitted

Raw log:

```text
sim/02_controlled/08_recovery_abort_handling/logs/raw/two_path_degraded_abort_run.txt
```

Result:

- RULE-23_RETURN_RAMP_ABORT emitted.
- `abort_class=DEGRADED_ABORT` confirmed.
- `immediate_cut=false` confirmed.
- Traffic Stabilization Phase entered.
- `fallback_transfer_allowed=false` confirmed.
- `fallback_block_reason=NO_SAFE_ALTERNATE` confirmed.
- Resolver arbitration occurred.
- `least_bad_selection=true` confirmed.
- Source-side traffic reduction request occurred.
- Validation outcome: PASS.

---

## TWO_PATH_DEGRADED_ABORT Observation

When only two candidate paths exist and both are degraded, PSC must not assume a
fully safe alternate path exists.

The correct behavior is to abort the active Return Ramp attempt, hold traffic for
arbitration, block blind fallback with `NO_SAFE_ALTERNATE`, and ask Resolver to
select the least-bad allocation while source-side PSC reduces traffic under
policy control.

---

## Extended Abort Handling Level Summary

```text
SOFT_ABORT
-> Hold and Re-observe

HARD_ABORT
-> Ramp Down Suspect Path

EMERGENCY_CUT_NO_FALLBACK
-> Immediate Path Exclusion + Source-Side Emergency Traffic Control

TWO_PATH_DEGRADED_ABORT
-> Resolver Arbitration + Least-Bad Allocation
```

---

## Validator Assertions

`scripts/validate_evidence_rules.py` checks the following for each abort
class, in addition to the `RULE-23_RETURN_RAMP_ABORT` rule name and expected
category:

| Abort class | `abort_class` assertion | `reason` assertion | Post-abort state assertions | Cross-class exclusion |
|-------------|--------------------------|---------------------|------------------------------|------------------------|
| `SOFT_ABORT` | `abort_class=SOFT_ABORT` | `reason=TELEMETRY_CONFLICT_CONFIDENCE_REDUCTION` | `immediate_cut=false`, `entered=true`, `allocation_action=hold_temporarily`, `escalation=requested`, `target_mode=FULL`, `re_evaluation=triggered`, `allocation_unchanged=true` | `abort_class=HARD_ABORT`/`EMERGENCY_CUT`/`DEGRADED_ABORT` and `immediate_cut=true` must not appear |
| `HARD_ABORT` | `abort_class=HARD_ABORT` | `reason=CLEAR_INSTABILITY_LINK_QUALITY_COLLAPSE` | `immediate_cut=false`, `allocation_action=ramp_down_suspect_path`, `recovered_path_a_weight=10`, `stable_path_b_weight=90`, `re_evaluation=triggered`, `[SOURCE] notification=sent`, `recovered_path_reduced=true` | `abort_class=SOFT_ABORT`/`EMERGENCY_CUT`/`DEGRADED_ABORT` and `immediate_cut=true` must not appear |
| `EMERGENCY_CUT` | `abort_class=EMERGENCY_CUT` | `reason=LINK_DOWN_OPTICAL_FAILURE_NO_CAPACITY_MARGIN` | `immediate_cut=true`, `fallback_block_reason=NO_CAPACITY_MARGIN`, `emergency_cut=true`, `path_a_excluded=true`, `recovered_path_a_weight=0`, `dropped_or_blocked_weight=25`, `entered=false`, `[SOURCE] notification=sent` | `abort_class=SOFT_ABORT`/`HARD_ABORT`/`DEGRADED_ABORT` and `immediate_cut=false` must not appear |
| `DEGRADED_ABORT` | `abort_class=DEGRADED_ABORT` | `reason=TWO_PATH_DEGRADED_NO_SAFE_ALTERNATE` | `immediate_cut=false`, `fallback_block_reason=NO_SAFE_ALTERNATE`, `no_safe_alternate=true`, `allocation_action=hold_for_arbitration`, `least_bad_selection=true`, `[SOURCE] notification=sent` | `abort_class=SOFT_ABORT`/`HARD_ABORT`/`EMERGENCY_CUT` and `immediate_cut=true` must not appear |

All four scenarios also assert `outcome=PASS` in the scenario's own
`[VALIDATION]` line, and all four now return a structured
`ValidationResult(rule, passed, category, reason)` object from
`decide_abort_handling`, matching the pattern already used by
`two_path_degraded_abort.py`. `run()` asserts `result.passed` and
`result.rule == SCENARIO_METADATA["expected_rules"][0]` for every scenario.

---

## Final Judgment

Verified.

For the FULL-observation `SOFT_ABORT`, `HARD_ABORT`, `EMERGENCY_CUT`, and
`DEGRADED_ABORT` classes, the runnable scenarios, raw logs, this verified log,
and the validator assertions confirm that `RULE-23_RETURN_RAMP_ABORT` aborts
the active Return Ramp attempt without defaulting to immediate traffic cut,
and that each abort class produces its own distinct, non-confused post-abort
outcome. See "Verified Scope" above for what remains outside this status.
