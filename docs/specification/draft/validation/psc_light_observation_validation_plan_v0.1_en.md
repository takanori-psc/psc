# PSC LIGHT Observation Validation Plan v0.1

## 1. Document Information

- Document Name : PSC LIGHT Observation Validation Plan
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Telemetry / Fast Mode / Validation
- Document Type : Validation Draft
- Status : Draft
- Language : English

- Related Models:
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC Evidence Matrix v0.1
  - PSC RCU Recovery Return Model v0.2
  - PSC Resolver Specification v0.1

---

## 2. Purpose

This draft defines the minimum validation plan required before `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` can be reconsidered for promotion from Hold.

The purpose is not to implement LIGHT validation yet.
The purpose is to identify what must be observed, simulated, and checked so that LIGHT observation can be judged as safe enough for staged recovery ramp advancement.

Current position:

```text
RULE-21_RETURN_RAMP_ADVANCE (LIGHT)
  -> Hold
```

The Hold state can only be removed after LIGHT-specific failure modes are represented as validation scenarios and mapped to expected control behavior.

---

## 3. Validation Principle

LIGHT observation may reduce telemetry density, but it must not reduce the ability to explain why a recovery ramp advanced, held, aborted, or escalated.

Validation therefore checks control intent, not only RULE presence.

The first validation layer should answer:

```text
Did PSC choose the expected behavior category for the scenario?
```

It does not need to perform numeric threshold comparison in v0.1.

---

## 4. Scenario Set

| Scenario | Risk represented | Minimum stimulus | Expected behavior category | Candidate RULE evidence |
|----------|------------------|------------------|----------------------------|-------------------------|
| light_false_negative | Instability exists but LIGHT observation does not detect it directly | Hidden stability dip during recovery ramp | hold_or_escalate | `RULE-22_RETURN_RAMP_HOLD` or `RULE-05_ESCALATE_conflict` |
| light_telemetry_gap | Required LIGHT input is unavailable | Missing trust, stability proxy, freshness, or confidence | hold | `RULE-22_RETURN_RAMP_HOLD` |
| light_stale_telemetry | Telemetry exists but freshness exceeds the accepted window | Old sample used during ramp decision | hold | `RULE-22_RETURN_RAMP_HOLD` |
| light_masked_instability | Sparse sampling hides a short instability dip | Stability dip occurs between accepted samples | hold_or_escalate | `RULE-22_RETURN_RAMP_HOLD` or `RULE-05_ESCALATE_conflict` |
| light_delayed_abort | LIGHT observes instability later than FULL | Hard failure or severe instability appears after LIGHT delay | abort | `RULE-23_RETURN_RAMP_ABORT` |
| light_resolver_escalation | LIGHT evidence is insufficient to distinguish recovery from risk | Conflicting trust / stability / confidence signals | escalation_and_cooldown | `RULE-05_ESCALATE_conflict`, `RULE-12_COOLDOWN_active` |

---

## 5. Expected Behavior Categories

The validator should prepare for behavior categories in addition to RULE matching.

| Category | Meaning | Acceptable evidence |
|----------|---------|---------------------|
| switch | PSC intentionally changes the selected path or ramp target | Switch RULE appears and the scenario expects switching |
| hold | PSC maintains the current selected path or ramp weight | KEEP or HOLD RULE appears |
| abort | PSC stops recovery ramp advancement due to unsafe evidence | `RULE-23_RETURN_RAMP_ABORT` appears |
| escalation | PSC delegates ambiguous control to Resolver | `RULE-05_ESCALATE_conflict` appears |
| escalation_and_cooldown | PSC escalates and then suppresses repeated arbitration | escalation RULE and cooldown RULE both appear |
| fallback | PSC enters or uses a degraded fallback path | DEGRADED trigger / switch RULE appears |

This lets validation move from:

```text
Was a RULE emitted?
```

to:

```text
Was the emitted RULE consistent with the intended control behavior?
```

---

## 6. Hold Removal Gates

`RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` should remain on Hold until all gates below are satisfied.

| Gate | Requirement |
|------|-------------|
| Scenario coverage | All LIGHT-specific scenarios in Section 4 exist as runnable or manually traceable validation cases |
| Expected category mapping | Each scenario has a declared expected behavior category |
| Missing telemetry handling | Missing required LIGHT input cannot produce ramp advance |
| Stale telemetry handling | Stale telemetry cannot produce ramp advance |
| Masked instability handling | Ambiguous sparse evidence produces hold or Resolver escalation |
| Delayed abort handling | Severe instability still produces abort even under LIGHT observation |
| Resolver escalation handling | Ambiguous LIGHT evidence can escalate and then enter cooldown |
| Evidence Matrix integration | Scenario, RULE, STEP, and log references are added after execution evidence exists |

---

## 7. Validator Structure Extension Draft

The current `scripts/validate_evidence_rules.py` validates whether expected RULE identifiers appear in scenario output.

The next structure should keep that behavior and add optional behavior intent metadata.

Proposed shape:

```python
ScenarioCheck(
    name="resolver_switch",
    command=(...),
    expected_rules=(...),
    expected_category="escalation_and_cooldown",
)
```

Initial categories should remain string-based and non-numeric.
The validator should pass when:

1. the command exits successfully,
2. all required RULE identifiers appear, and
3. the scenario's expected behavior category is satisfied by the observed RULE family.

This should be treated as a structure extension only.
Threshold comparison, step ordering, and telemetry value checks should remain out of scope for the first extension.

---

## 8. Initial Category Mapping for Existing Scenarios

| Existing scenario | Current expected RULE basis | Proposed expected category |
|-------------------|-----------------------------|----------------------------|
| switch_score | `RULE-01_KEEP_score`, `RULE-02_SWITCH_score` | switch |
| resolver_switch | `RULE-05_ESCALATE_conflict`, `RULE-14_RESOLVER_switch`, `RULE-12_COOLDOWN_active` | escalation_and_cooldown |
| recovery_return_v02 | `RULE-15`, `RULE-16`, `RULE-18`, `RULE-19` | switch |
| degraded | `RULE-07`, `RULE-09` | fallback |
| recovery_hold | `RULE-10`, `RULE-11`, keep behavior | hold |

This mapping is provisional and should be refined when LIGHT-specific scenarios are added.

---

## 9. Non-Goals

This plan does not define:

- final LIGHT thresholds
- production telemetry schemas
- Fast Mode packet format
- numeric pass / fail comparison
- Resolver internal arbitration logic
- promotion of LIGHT advance to Verified status

---

## 10. Next Work

1. Add LIGHT scenario stubs or scripted cases for the six scenarios in Section 4.
2. Extend `ScenarioCheck` with an optional `expected_category` field.
3. Add a small category inference helper based on emitted RULE identifiers.
4. Generate dedicated LIGHT validation logs.
5. Update the Evidence Matrix only after logs exist.
