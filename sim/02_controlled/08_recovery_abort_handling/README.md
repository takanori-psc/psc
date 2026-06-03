# PSC Recovery Return Abort Handling Scenarios

## Purpose

This directory contains experimental validation scenarios for the draft:

```text
docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_en.md
docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_ja.md
```

These scenarios validate that `RULE-23_RETURN_RAMP_ABORT` aborts the current
Return Ramp attempt, followed by Traffic Stabilization Phase and Resolver
re-evaluation. Immediate traffic cut is not the default behavior unless the
condition is an emergency cut case.

## Scope

These scenarios are lightweight validation assets. They do not modify existing
recovery return simulations and are not yet connected to the validator or
Evidence Matrix.

## Structure

```text
sim/02_controlled/08_recovery_abort_handling/
  README.md
  soft_abort_hold_and_reobserve.py
  hard_abort_ramp_down.py
  emergency_cut_no_fallback.py
  two_path_degraded_abort.py
  logs/
    raw/
      soft_abort_hold_and_reobserve_run.txt
      hard_abort_ramp_down_run.txt
      emergency_cut_no_fallback_run.txt
      two_path_degraded_abort_run.txt
    verified/
      recovery_abort_stabilization_validation_log.md
```

## Scenario: soft_abort_hold_and_reobserve

Initial allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active

Observed condition:

- telemetry conflict
- confidence reduction
- evidence is suspicious but not conclusively unsafe

Expected behavior:

- emit `RULE-23_RETURN_RAMP_ABORT`
- enter Traffic Stabilization Phase
- stop further ramp advancement
- keep current allocation temporarily
- request observation escalation
- trigger Resolver re-evaluation

Expected category:

```text
abort_and_stabilize
```

Run:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py
```

Regenerate raw log:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/soft_abort_hold_and_reobserve_run.txt
```

## Scenario: hard_abort_ramp_down

Initial allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active

Observed condition:

- clear path instability
- link quality collapse
- evidence is conclusively unsafe
- forwarding is still possible

Expected behavior:

- emit `RULE-23_RETURN_RAMP_ABORT`
- enter Traffic Stabilization Phase
- stop further Return Ramp Advance
- ramp down suspect recovered Path A
- move traffic toward known stable Path B
- trigger Resolver re-evaluation
- notify source-side PSC that traffic reduction may be needed

Expected category:

```text
hard_abort_ramp_down
```

Run:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py
```

Regenerate raw log:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/hard_abort_ramp_down_run.txt
```

## Scenario: emergency_cut_no_fallback

Initial allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active

Observed condition:

- Path A link down / optical failure
- forwarding on Path A is not possible
- evidence is conclusively unsafe
- emergency condition is confirmed
- Path B exists and is not failed
- Path B has no capacity margin to absorb Path A traffic

Fallback failure class:

```text
NO_CAPACITY_MARGIN
```

Expected behavior:

- emit `RULE-23_RETURN_RAMP_ABORT`
- perform `EMERGENCY_CUT`
- immediately exclude recovered Path A
- set recovered Path A weight to 0
- do not blindly transfer Path A traffic into Path B
- set `fallback_transfer_allowed=false`
- emit `fallback_block_reason=NO_CAPACITY_MARGIN`
- notify source-side PSC for emergency throttling or stop
- trigger Resolver emergency notification
- skip the normal soft/hard Traffic Stabilization Phase

Expected category:

```text
emergency_cut_no_fallback
```

Run:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py
```

Regenerate raw log:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/emergency_cut_no_fallback_run.txt
```

## Scenario: two_path_degraded_abort

Initial allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active
- Candidate paths: 2
- Third path: none

Observed condition:

- Path A is unstable during Return Ramp
- Path B also shows degradation
- no third path exists
- neither path is fully safe
- forwarding is still possible
- condition is not EMERGENCY_CUT

Fallback failure class:

```text
NO_SAFE_ALTERNATE
```

Expected behavior:

- emit `RULE-23_RETURN_RAMP_ABORT`
- enter Traffic Stabilization Phase
- stop further Return Ramp Advance
- do not blindly move all traffic to Path B
- set `fallback_transfer_allowed=false`
- emit `fallback_block_reason=NO_SAFE_ALTERNATE`
- trigger Resolver arbitration
- select least-bad allocation
- preserve limited forwarding if policy allows
- request source-side traffic reduction

Expected category:

```text
two_path_degraded_arbitration
```

Run:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py
```

Regenerate raw log:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/two_path_degraded_abort_run.txt
```

## Abort Handling Levels

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
