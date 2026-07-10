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

This document analyzes evidence coverage and gaps for promoting
`RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`,
`RULE-23_RETURN_RAMP_ABORT`, and `RULE-24_RETURN_RAMP_COMPLETE`
from Experimental / Hold to Verified.

This document is a gap analysis and does not change the status of any existing
RULE. The Evidence Matrix, promotion criteria, simulation files, log files, and
validator file are not modified in this step.

---

## 2. Reference Scope

This analysis refers to the following sources.

| Type | Reference |
|------|-----------|
| Promotion criteria | `docs/specification/validation/psc_rule_promotion_criteria_v0.1_en.md` |
| Evidence Matrix | `docs/specification/validation/psc_evidence_matrix_v0.1_en.md` |
| Recovery ramp scenarios | `sim/02_controlled/06_recovery_return_v02/` |
| LIGHT observation scenarios | `sim/02_controlled/07_light_observation_stub/` |
| Abort handling scenarios | `sim/02_controlled/08_recovery_abort_handling/` |
| Validator | `scripts/validate_evidence_rules.py` |

---

## 3. Current Overall Status

In the Evidence Matrix, `RULE-22_RETURN_RAMP_HOLD` is now treated as Verified
for the covered FULL-observation hold evidence with
`reason=INSUFFICIENT_OBSERVATION`. LIGHT Observation coverage remains outside
the current Verified scope. The remaining target RULEs are still Experimental,
and coverage maturity differs by RULE.

| RULE | Current Status | Coverage Summary | Main Gaps |
|------|----------------|------------------|-----------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Experimental / LIGHT remains Hold | FULL observation ramp advance logs exist | Dedicated validator check, LIGHT false-positive / false-negative boundaries, and integration of conditions into the specification are missing |
| `RULE-22_RETURN_RAMP_HOLD` | Verified | FULL `ramp_hold_insufficient_observation` scenario, raw log, verified log, and validator assertions define the current Verified scope; LIGHT hold scenarios remain available outside that scope | Formal specification integration remains separate from evidence status |
| `RULE-23_RETURN_RAMP_ABORT` | Experimental | Abort-class scenarios, raw logs, verified log, and validator checks exist | Abort thresholds, unified post-abort state assertions, and structured results across all abort scenarios are missing |
| `RULE-24_RETURN_RAMP_COMPLETE` | Experimental | Raw / verified logs for ramp complete exist | Dedicated scenario separation, validator check, completion threshold, and post-completion state assertions are missing |

---

## 4. RULE-21_RETURN_RAMP_ADVANCE Gap Analysis

### 4.1 Available Scenario Files

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | Integrated scenario that includes recovery ramp v0.3 FULL / LIGHT observation |

### 4.2 Available Raw Logs

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_scenario_run.txt` | v0.3 ramp advance trace without explicit FULL observation annotation |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | Ramp advance trace including FULL / LIGHT observation mode |

### 4.3 Available Verified Logs / Matrix Mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | Records progressive ramp advance in baseline / ramp_complete scenarios |
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_full_light_observation_validation_log.md` | Records the observation policy difference between FULL and LIGHT |
| Evidence Matrix | Mapped as `recovery_ramp_v03` / `LOG-RAMP-01` with Experimental status |

### 4.4 Validator Coverage

`RULE-21_RETURN_RAMP_ADVANCE` is registered in `CATEGORY_RULES` as a `switch`
category in `scripts/validate_evidence_rules.py`. However, `SCENARIOS` does not
include a dedicated check that expects `RULE-21_RETURN_RAMP_ADVANCE`.

Current validator coverage is indirect. It does not assert the weight before
and after advance, FULL observation mode, or non-advance behavior under
hold / abort conditions.

### 4.5 Missing Evidence

| Missing item | Description |
|--------------|-------------|
| Dedicated validator check | Confirm that `RULE-21_RETURN_RAMP_ADVANCE` appears only when stability conditions are satisfied under FULL observation |
| Negative check | Confirm that recovered weight does not increase under hold / abort conditions |
| Structured result | Return value that can mechanically assert expected category, rule, weight delta, and observation mode |
| Specification integration | Integrate ramp_increment, advance threshold, and FULL observation condition into the specification text |
| LIGHT boundary | Define false-positive / false-negative boundaries for advance under LIGHT observation |

### 4.6 Promotion Blocker

`RULE-21_RETURN_RAMP_ADVANCE` is close to a promotion candidate if limited to
FULL observation, but it still lacks a dedicated validator and specification
integration.

`RULE-21_RETURN_RAMP_ADVANCE` based on LIGHT observation remains Hold.
LIGHT-based advance must not be treated as Verified evidence until
false-positive / false-negative behavior under LIGHT observation is sufficiently
bounded and either LIGHT-to-FULL escalation conditions or LIGHT advance promotion
gates are defined.

---

## 5. RULE-22_RETURN_RAMP_HOLD Gap Analysis

### 5.1 Available Scenario Files

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/07_light_observation_stub/light_false_negative.py` | Hold under LIGHT observation false negative |
| `sim/02_controlled/07_light_observation_stub/light_stale_telemetry.py` | Hold under stale telemetry |
| `sim/02_controlled/07_light_observation_stub/light_masked_instability.py` | Hold under masked instability |
| `sim/02_controlled/07_light_observation_stub/light_telemetry_gap_stub.py` | Design stub for LIGHT-specific required telemetry gap |
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | Runnable FULL observation `ramp_hold_insufficient_observation` trace during recovery ramp |

### 5.2 Available Raw Logs

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/07_light_observation_stub/logs/raw/light_false_negative_run.txt` | `reason=OBSERVATION_FALSE_NEGATIVE` |
| `sim/02_controlled/07_light_observation_stub/logs/raw/light_stale_telemetry_run.txt` | `reason=STALE_TELEMETRY` |
| `sim/02_controlled/07_light_observation_stub/logs/raw/light_masked_instability_run.txt` | `reason=MASKED_INSTABILITY` |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | Hold trace during FULL / LIGHT ramp |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_hold_insufficient_observation_run.txt` | `reason=INSUFFICIENT_OBSERVATION`, `category=hold`, `observation_mode=FULL`, and unchanged `0.30 -> 0.30` ramp level |

### 5.3 Available Verified Logs / Matrix Mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/07_light_observation_stub/logs/verified/light_observation_hold_validation_log.md` | Records LIGHT false-negative / stale / masked-instability hold |
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_ramp_hold_insufficient_observation_validation_log.md` | Records FULL `INSUFFICIENT_OBSERVATION` hold after a prior ramp advance |
| Evidence Matrix | `ramp_hold_insufficient_observation` is mapped to Verified evidence; LIGHT scenarios are documented as evidence available outside the current Verified scope |

### 5.4 Validator Coverage

`scripts/validate_evidence_rules.py` directly checks the following three
runnable LIGHT scenarios.

| Validator scenario | Expected RULE | Expected category |
|--------------------|---------------|-------------------|
| `light_false_negative` | `RULE-22_RETURN_RAMP_HOLD` | `hold` |
| `light_stale_telemetry` | `RULE-22_RETURN_RAMP_HOLD` | `hold` |
| `light_masked_instability` | `RULE-22_RETURN_RAMP_HOLD` | `hold` |

The validator detects the RULE and category for the LIGHT scenarios, but those
LIGHT checks are outside the current Verified scope. For
`ramp_hold_insufficient_observation`, the validator also asserts reason,
observation mode, state transition, unchanged ramp level, previous-step
advance, and forbidden same-step advance / abort / complete / emergency
outcomes.

### 5.5 Missing Evidence

| Missing item | Description |
|--------------|-------------|
| LIGHT telemetry gap runnable coverage | `light_telemetry_gap_stub.py` remains a LIGHT-specific design stub and is not promoted by the FULL observation ramp-hold evidence |
| Specification integration | Formal text still needs to integrate hold / advance / abort transitions across v0.3 ramp behavior |

### 5.6 Promotion Blocker

`RULE-22_RETURN_RAMP_HOLD` now has the evidence set required for Verified
status in the Evidence Matrix for the covered FULL-observation hold scope:
runnable scenario, raw log, verified log, and validator assertions for
`INSUFFICIENT_OBSERVATION`.

This does not include LIGHT Observation scenarios in the current Verified scope,
does not promote LIGHT-based ramp advance, and does not complete the broader
v0.3 ramp specification integration.

---

## 6. RULE-23_RETURN_RAMP_ABORT Gap Analysis

### 6.1 Available Scenario Files

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py` | `SOFT_ABORT` |
| `sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py` | `HARD_ABORT` |
| `sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py` | `EMERGENCY_CUT` |
| `sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py` | `DEGRADED_ABORT` / `NO_SAFE_ALTERNATE` |
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | Abort trace during recovery ramp |
| `sim/02_controlled/07_light_observation_stub/light_delayed_abort_stub.py` | Design stub for LIGHT delayed abort |

### 6.2 Available Raw Logs

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/soft_abort_hold_and_reobserve_run.txt` | `SOFT_ABORT` / `abort_and_stabilize` |
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/hard_abort_ramp_down_run.txt` | `HARD_ABORT` / `hard_abort_ramp_down` |
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/emergency_cut_no_fallback_run.txt` | `EMERGENCY_CUT` / `NO_CAPACITY_MARGIN` |
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/two_path_degraded_abort_run.txt` | `DEGRADED_ABORT` / `NO_SAFE_ALTERNATE` |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_scenario_run.txt` | Recovery ramp abort trace |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | FULL / LIGHT observation abort trace |

### 6.3 Available Verified Logs / Matrix Mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/08_recovery_abort_handling/logs/verified/recovery_abort_stabilization_validation_log.md` | Records soft / hard / emergency / two-path degraded abort |
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | Records ramp abort behavior |
| Evidence Matrix | Abort handling scenarios are mapped to `LOG-ABORT-01` and `RAW-ABORT-*` |

### 6.4 Validator Coverage

`scripts/validate_evidence_rules.py` directly checks the following abort
handling scenarios.

| Validator scenario | Expected RULE | Expected category |
|--------------------|---------------|-------------------|
| `soft_abort_hold_and_reobserve` | `RULE-23_RETURN_RAMP_ABORT` | `abort_and_stabilize` |
| `hard_abort_ramp_down` | `RULE-23_RETURN_RAMP_ABORT` | `hard_abort_ramp_down` |
| `emergency_cut_no_fallback` | `RULE-23_RETURN_RAMP_ABORT` | `emergency_cut_no_fallback` |
| `two_path_degraded_abort` | `RULE-23_RETURN_RAMP_ABORT` | `two_path_degraded_arbitration` |

The current validator can detect the RULE and category. However, individual
assertions for abort class, fallback block reason, source notification, and
stabilization action still depend on string containment in scenario output.

### 6.5 Missing Evidence

| Missing item | Description |
|--------------|-------------|
| Structured result unification | `two_path_degraded_abort.py` has a structured result, but the other abort scenarios still return plain strings |
| Abort class assertion | The validator should explicitly assert `SOFT_ABORT`, `HARD_ABORT`, `EMERGENCY_CUT`, and `DEGRADED_ABORT` |
| Post-abort state assertion | Mechanically validate allocation hold, ramp down, path exclusion, least-bad arbitration, and similar outcomes |
| Threshold integration | Integrate abort thresholds and observation-mode-specific thresholds into the specification text |
| LIGHT delayed abort | Formal runnable / raw / verified coverage for `light_delayed_abort_stub.py` is not complete |

### 6.6 Promotion Blocker

`RULE-23_RETURN_RAMP_ABORT` has the broadest scenario and raw-log coverage.
However, the validator does not yet sufficiently structure post-abort outcome
checks for each abort class. Before promotion to Verified, abort scenarios need
unified structured results, and fallback block reason plus stabilization action
must be explicit assertions.

---

## 7. RULE-24_RETURN_RAMP_COMPLETE Gap Analysis

### 7.1 Available Scenario Files

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | Integrated scenario containing recovery ramp complete |

### 7.2 Available Raw Logs

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_scenario_run.txt` | `RULE-24_RETURN_RAMP_COMPLETE`, `recovered_weight=1.00`, `evacuation_weight=0.00` |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | Complete trace under FULL observation mode |

### 7.3 Available Verified Logs / Matrix Mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | Records ramp_complete scenario and `RULE-24_RETURN_RAMP_COMPLETE` |
| Evidence Matrix | Mapped as `recovery_ramp_v03` / `LOG-RAMP-03` with Experimental status |

### 7.4 Validator Coverage

`RULE-24_RETURN_RAMP_COMPLETE` is registered in `CATEGORY_RULES` as a `switch`
category in `scripts/validate_evidence_rules.py`. However, `SCENARIOS` does not
include a dedicated check that expects `RULE-24_RETURN_RAMP_COMPLETE`.

Current validator coverage does not assert completion threshold, final
allocation, post-completion state, or absence of additional advance after
completion.

### 7.5 Missing Evidence

| Missing item | Description |
|--------------|-------------|
| Dedicated scenario | Reproducible scenario that makes ramp complete the clear primary target |
| Dedicated validator check | Assertion for `RULE-24_RETURN_RAMP_COMPLETE` and final allocation |
| Completion threshold | Define the completion decision threshold in the specification text |
| Post-completion state | Raw / validator evidence that the state after completion is stable |
| No additional advance | Assertion that no unnecessary additional advance appears after complete |

### 7.6 Promotion Blocker

`RULE-24_RETURN_RAMP_COMPLETE` appears in raw / verified logs, but it lacks the
validator check and completion-condition specification required by the promotion
criteria. It is too early to promote it to Verified.

---

## 8. Validator Coverage Summary

| RULE | Current validator coverage | Gap |
|------|----------------------------|-----|
| `RULE-21_RETURN_RAMP_ADVANCE` | Present in category mapping, but no dedicated scenario check | FULL advance condition, weight delta, and negative checks are missing |
| `RULE-22_RETURN_RAMP_HOLD` | Directly checks the FULL `ramp_hold_insufficient_observation` scenario for the current Verified scope; also keeps LIGHT hold checks outside that scope | LIGHT reason-specific assertions and unchanged-weight checks remain future coverage work |
| `RULE-23_RETURN_RAMP_ABORT` | Directly checks four abort handling scenarios | Structured assertions for abort class / fallback reason / post-abort action are missing |
| `RULE-24_RETURN_RAMP_COMPLETE` | Present in category mapping, but no dedicated scenario check | Completion threshold, final allocation, and post-completion state checks are missing |

The current `scripts/validate_evidence_rules.py` is useful as a smoke /
traceability validator that confirms representative Evidence Matrix RULEs
appear in output. For Verified promotion, state assertions dedicated to
RULE-21 through RULE-24 need to be added.

---

## 9. Recommended Promotion Order

The recommended promotion order is as follows.

1. `RULE-22_RETURN_RAMP_HOLD`
2. `RULE-23_RETURN_RAMP_ABORT`
3. `RULE-21_RETURN_RAMP_ADVANCE (FULL only)`
4. `RULE-24_RETURN_RAMP_COMPLETE`

Rationale:

- `RULE-22` establishes the LIGHT hold safety boundary and is the basis for suppressing LIGHT advance.
- `RULE-23` is a safe-side RULE that prevents return to unsafe paths and should be stabilized before advance / complete.
- `RULE-21` should be reviewed only after limiting it to FULL observation. LIGHT-based advance remains Hold.
- `RULE-24` should be reviewed as the completion condition after the advance / hold / abort boundaries are stable.

---

## 10. Main Blockers

| RULE | Promotion blocker |
|------|-------------------|
| `RULE-21_RETURN_RAMP_ADVANCE` | LIGHT false-positive / false-negative boundaries are undefined, and FULL advance lacks a dedicated validator |
| `RULE-22_RETURN_RAMP_HOLD` | Evidence blocker cleared for covered FULL / `INSUFFICIENT_OBSERVATION` hold behavior; LIGHT Observation coverage and broader v0.3 specification integration remain separate |
| `RULE-23_RETURN_RAMP_ABORT` | Post-abort action assertions by abort class are missing, and structured result coverage is not unified |
| `RULE-24_RETURN_RAMP_COMPLETE` | Validator coverage for completion threshold, final allocation, and post-completion state is missing |

---

## 11. Conclusion

At this point, `RULE-22_RETURN_RAMP_HOLD` has the scenario, raw log, verified
log, Evidence Matrix mapping, and validator assertions needed for Verified
status in the Evidence Matrix for FULL / `INSUFFICIENT_OBSERVATION` hold
evidence. LIGHT Observation scenarios remain outside the current Verified
scope. `RULE-23_RETURN_RAMP_ABORT` remains the closest remaining Experimental
promotion candidate.

`RULE-21_RETURN_RAMP_ADVANCE` may become a promotion candidate if limited to
FULL observation, but LIGHT observation based advance remains Hold.
LIGHT-based advance must not be treated as Verified evidence until
false-positive / false-negative behavior is sufficiently bounded.

`RULE-24_RETURN_RAMP_COMPLETE` has completion traces, but dedicated validator
coverage and completion-condition specification are still missing. It should be
reviewed for promotion after RULE-21 / RULE-22 / RULE-23 boundaries are
organized.
