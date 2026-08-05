# PSC RULE Promotion Gap Analysis v0.1

## Document Information

| Item | Description |
|------|-------------|
| Document ID | `PSC-RULE-PROMOTION-GAP-ANALYSIS-v0.1-en` |
| Title | PSC RULE-21 through RULE-24 Evidence Gap Analysis |
| Version | v0.1 |
| Language | English |
| Status | Draft |
| Scope | `RULE-21_RETURN_RAMP_ADVANCE` through `RULE-24_RETURN_RAMP_COMPLETE` |
| Related Criteria | `docs/specification/validation/psc_rule_promotion_criteria_v0.1_en.md` |
| Related Evidence Matrix | `docs/specification/validation/psc_evidence_matrix_v0.1_en.md` |

---

## 1. Purpose

This document tracks the original evidence gaps, the gaps resolved at Verified
promotion, and the work that remains for `RULE-21_RETURN_RAMP_ADVANCE`,
`RULE-22_RETURN_RAMP_HOLD`, `RULE-23_RETURN_RAMP_ABORT`, and
`RULE-24_RETURN_RAMP_COMPLETE`.

This document is not the authoritative source for RULE status. The Evidence
Matrix is authoritative for status and Verified scope; this document is a
gap-closure record that explains that state. Modification of the Promotion
Criteria, Evidence Matrix, simulations, validator, and logs is outside the
scope of this document.

---

## 2. Reference Scope

| Type | Reference |
|------|-----------|
| Promotion criteria | `docs/specification/validation/psc_rule_promotion_criteria_v0.1_en.md` |
| Authoritative Evidence Matrix | `docs/specification/validation/psc_evidence_matrix_v0.1_en.md` |
| Recovery ramp scenarios | `sim/02_controlled/06_recovery_return_v02/` |
| LIGHT observation scenarios | `sim/02_controlled/07_light_observation_stub/` |
| Abort handling scenarios | `sim/02_controlled/08_recovery_abort_handling/` |
| Validator | `scripts/validate_evidence_rules.py` |

---

## 3. Current Overall Status

In the Evidence Matrix, RULE-21 through RULE-24 have been promoted to Verified
with the limited scopes below. LIGHT-observation-based advance remains Hold.
LIGHT observation coverage and other out-of-scope evidence remain Hold or
Experimental. The ramp engine's internal `RECOVERED_PATH_UNSTABLE` /
`RECOVERED_PATH_INVALID` abort trace remains Experimental and is not included
in the Verified scope.

| RULE | Current Status | Verified Scope | Outside Scope |
|------|----------------|----------------|---------------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Verified (FULL only) | Positive / negative evidence for FULL advance | LIGHT advance remains Hold |
| `RULE-22_RETURN_RAMP_HOLD` | Verified (limited scope) | FULL / `INSUFFICIENT_OBSERVATION` hold | LIGHT hold coverage is outside the Verified scope |
| `RULE-23_RETURN_RAMP_ABORT` | Verified (limited scope) | Four FULL abort classes | LIGHT delayed abort and internal ramp-engine abort traces are Experimental / outside scope |
| `RULE-24_RETURN_RAMP_COMPLETE` | Verified (FULL only) | FULL completion and post-completion state | LIGHT completion is outside scope |

---

## 4. RULE-21_RETURN_RAMP_ADVANCE Gap Analysis

### 4.1 Available Evidence

| Type | Evidence |
|------|----------|
| Scenario | `mini_psc_rcu_decision_v03_recovery_ramp_observation.py`: `ramp_complete` (positive), `ramp_abort_full_stability_dip` (negative) |
| Raw log | `ramp_complete_run.txt` (`RAW-RAMP-FULL-ADV-01`), `ramp_abort_full_stability_dip_run.txt` (`RAW-RAMP-ABORT-FULLDIP-01`) |
| Verified log | `rcu_decision_v03_ramp_full_advance_validation_log.md` (`LOG-RAMP-FULL-ADV-01`) |
| Validator | `ScenarioCheck.name=ramp_complete` and `ScenarioCheck.name=ramp_abort_full_stability_dip` |
| Matrix mapping | Maps the FULL advance sequence and non-advance under instability to a Verified row |

### 4.2 Resolved Gaps

- The FULL-observation advance sequence `0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90` is confirmed.
- The validator asserts `category=switch`, FULL observation, `RECOVERED_PATH_STABLE`, and arrival at completion.
- Negative evidence confirms that RULE-21 and RULE-24 do not fire and weight remains `0.10` when instability occurs immediately before a due advance step.

### 4.3 Remaining Gaps

- Formal specification integration of `ramp_increment`, the advance threshold, and the FULL-observation condition.
- Additional validation of LIGHT-observation false-positive / false-negative boundaries and promotion gates.

### 4.4 Gap Closure

The `ramp_complete` and `ramp_abort_full_stability_dip` scenarios, their two
raw logs, `LOG-RAMP-FULL-ADV-01`, validator assertions for transitions, mode,
reason, completion, and forbidden abort, and the RULE-21 Verified mapping in
the Evidence Matrix close the evidence gap for the FULL-observation scope.
LIGHT advance remains Hold.

---

## 5. RULE-22_RETURN_RAMP_HOLD Gap Analysis

### 5.1 Available Evidence

| Type | Evidence |
|------|----------|
| Scenario | `mini_psc_rcu_decision_v03_recovery_ramp_observation.py`: `ramp_hold_insufficient_observation` |
| Raw log | `ramp_hold_insufficient_observation_run.txt` (`RAW-RAMP-HOLD-INSUFF-01`) |
| Verified log | `rcu_decision_v03_ramp_hold_insufficient_observation_validation_log.md` (`LOG-RAMP-HOLD-INSUFF-01`) |
| Validator | `ScenarioCheck.name=ramp_hold_insufficient_observation` |
| Matrix mapping | Maps the FULL / `INSUFFICIENT_OBSERVATION` hold to a Verified row |

The LIGHT `light_false_negative`, `light_stale_telemetry`, and
`light_masked_instability` scenarios and `LOG-LIGHT-HOLD-01` / `RAW-LIGHT-*`
are also available, but are outside the current Verified scope.
`light_telemetry_gap_stub.py` remains a design stub.

### 5.2 Resolved Gaps

- A runnable FULL-observation hold trace with `reason=INSUFFICIENT_OBSERVATION` is available.
- After the STEP 9 advance, STEP 10 maintains `0.30 -> 0.30` and `RAMPING->RAMPING`.
- The validator asserts that no same-step advance, abort, complete, or emergency outcome occurs.

### 5.3 Remaining Gaps

- Formal specification integration of the ramp hold / advance / abort transitions.
- Additional validation of LIGHT-observation boundaries, including the telemetry gap.

### 5.4 Gap Closure

`ramp_hold_insufficient_observation`, `RAW-RAMP-HOLD-INSUFF-01`,
`LOG-RAMP-HOLD-INSUFF-01`, validator assertions for reason, category, mode,
state transition, unchanged weight, and forbidden outcomes, and the RULE-22
Verified mapping in the Evidence Matrix close the gap for the FULL /
`INSUFFICIENT_OBSERVATION` scope.

---

## 6. RULE-23_RETURN_RAMP_ABORT Gap Analysis

### 6.1 Available Evidence

| Abort Class | Scenario | Raw Log | Verified Log |
|-------------|----------|---------|--------------|
| `SOFT_ABORT` | `soft_abort_hold_and_reobserve` | `RAW-ABORT-SOFT-01` | `LOG-ABORT-01` |
| `HARD_ABORT` | `hard_abort_ramp_down` | `RAW-ABORT-HARD-01` | `LOG-ABORT-01` |
| `EMERGENCY_CUT` | `emergency_cut_no_fallback` | `RAW-ABORT-EMERG-01` | `LOG-ABORT-01` |
| `DEGRADED_ABORT` | `two_path_degraded_abort` | `RAW-ABORT-2PATH-01` | `LOG-ABORT-01` |

Each scenario is checked by the same-named `ScenarioCheck` in
`scripts/validate_evidence_rules.py` and mapped to the RULE-23 Verified row in
the Evidence Matrix.

### 6.2 Resolved Gaps

- Runnable scenarios, raw logs, and a verified log cover all four FULL abort classes.
- The validator asserts abort class, reason, post-abort state, and cross-class exclusion.
- Class-specific outcomes such as fallback blocking, Resolver re-evaluation, and source notification are confirmed.

### 6.3 Remaining Gaps

- Formal specification integration of the abort threshold and observation-mode-specific thresholds.
- Additional runnable / raw / verified validation for LIGHT delayed abort.
- Additional validation of the ramp engine's internal `RECOVERED_PATH_UNSTABLE` / `RECOVERED_PATH_INVALID` abort traces. These remain Experimental.

### 6.4 Gap Closure

The four abort-handling scenarios, four `RAW-ABORT-*` logs, `LOG-ABORT-01`,
validator assertions for abort class, reason, post-abort state, and cross-class
exclusion, and the RULE-23 Verified mapping in the Evidence Matrix close the
gap for the four-FULL-abort-class scope. This closure does not include the
internal ramp-engine abort traces.

---

## 7. RULE-24_RETURN_RAMP_COMPLETE Gap Analysis

### 7.1 Available Evidence

| Type | Evidence |
|------|----------|
| Scenario | `mini_psc_rcu_decision_v03_recovery_ramp_observation.py`: `ramp_complete` (`scenario_steps=22`) |
| Raw log | `ramp_complete_run.txt` (`RAW-RAMP-FULL-ADV-01`) |
| Verified log | `rcu_decision_v03_ramp_complete_validation_log.md` (`LOG-RAMP-COMPLETE-01`) |
| Validator | `ScenarioCheck.name=ramp_complete` |
| Matrix mapping | Maps FULL completion and post-completion state to a Verified row |

### 7.2 Resolved Gaps

- STEP 17 confirms `recovered_weight=1.00`, `evacuation_weight=0.00`, and `RAMP_TARGET_REACHED`.
- Recovery cooldown at STEP 18-19 and `mode=NORMAL` at STEP 20-21 are confirmed.
- The validator asserts that RULE-24 and RULE-25 each occur once and that no abort, additional advance, or duplicate completion occurs.

### 7.3 Remaining Gaps

- Formal specification integration of the completion threshold (`ramp_max_weight=1.00`).
- Additional validation of completion boundaries under LIGHT observation.

### 7.4 Gap Closure

`ramp_complete`, `RAW-RAMP-FULL-ADV-01`, `LOG-RAMP-COMPLETE-01`, validator
assertions for completion, post-completion state, single occurrence, and
forbidden abort, and the RULE-24 Verified mapping in the Evidence Matrix close
the gap for the FULL-completion scope.

---

## 8. Gap Closure Summary

| RULE | Closed Scope | Closure Chain |
|------|--------------|---------------|
| RULE-21 | FULL advance positive / negative | 2 scenarios -> 2 raw logs -> `LOG-RAMP-FULL-ADV-01` -> dedicated assertions -> Matrix mapping |
| RULE-22 | FULL / `INSUFFICIENT_OBSERVATION` hold | scenario -> `RAW-RAMP-HOLD-INSUFF-01` -> `LOG-RAMP-HOLD-INSUFF-01` -> dedicated assertions -> Matrix mapping |
| RULE-23 | Four FULL abort classes | 4 scenarios -> 4 `RAW-ABORT-*` logs -> `LOG-ABORT-01` -> class-specific assertions -> Matrix mapping |
| RULE-24 | FULL completion / post-completion | scenario -> `RAW-RAMP-FULL-ADV-01` -> `LOG-RAMP-COMPLETE-01` -> dedicated assertions -> Matrix mapping |

---

## 9. Remaining Work

1. Formally integrate RULE-21 through RULE-24 and ramp state transitions into the specification.
2. Specify `ramp_increment` and the advance threshold.
3. Specify the abort threshold and observation-mode-specific thresholds.
4. Specify the completion threshold.
5. Add validation for LIGHT-observation hold / advance / completion boundaries, false positives / false negatives, telemetry gaps, and promotion gates.
6. Add runnable evidence, raw logs, verified logs, and validator assertions for the ramp engine's internal `RECOVERED_PATH_UNSTABLE` / `RECOVERED_PATH_INVALID` abort traces.

These items do not invalidate the current limited-scope Verified statuses.
They are work required for formal specification integration or promotion of
additional scope.

---

## 10. Conclusion

With the Evidence Matrix as the authoritative source, RULE-21 through RULE-24
have been promoted to Verified in their respective limited scopes, and the
evidence gaps required for those promotions are closed. LIGHT observation
coverage, out-of-scope evidence, and internal ramp-engine abort traces remain
Hold or Experimental. The remaining gaps are limited to formal specification
integration and validation of additional scope.
