# PSC Fast Mode LIGHT Observation Boundary v0.1

## 1. Document Information

- Document Name : PSC Fast Mode LIGHT Observation Boundary
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Telemetry / Fast Mode
- Document Type : Design Draft
- Status : Draft
- Language : English

- Related Models:
  - PSC Fast Mode Security Boundary Model v0.1
  - PSC Telemetry Model v0.2
  - PSC RCU Recovery Return Model v0.2
  - PSC Evidence Matrix v0.1

---

## 2. Purpose

This draft defines the safety boundary for LIGHT observation before Fast Mode is integrated into the main PSC control model.

LIGHT observation is not treated as a general replacement for FULL observation.
It is a restricted observation mode that may reduce telemetry cost or latency, but also reduces the evidence available to RCU and Resolver decisions.

The purpose of this document is to prevent the following unsafe sequence:

```text
Fast Mode
-> reduced observation
-> recovery ramp advance
-> false return to an unstable path
```

For this reason, `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` remains on Hold until the safety conditions in this draft are satisfied.

---

## 3. Scope

This draft covers:

- undefined risks of LIGHT observation
- differences between FULL and LIGHT observation
- safety conditions for recovery ramp advancement under LIGHT observation
- promotion conditions for `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)`

This draft does not define:

- the full Fast Mode routing model
- Fast Mode packet format
- Fast Mode authorization flow
- final production thresholds

---

## 4. Design Principle

LIGHT observation must not weaken PSC's stability-first control principle.

If observation is reduced, PSC must compensate by applying stricter gating, slower ramp advancement, shorter telemetry freshness windows, or mandatory Resolver review.

Reduced observation is acceptable only when the system can still explain why a path is safe to advance.

---

## 5. Undefined Risks

| Risk | Description | Impact |
|------|-------------|--------|
| False negative | Instability exists but is not observed | Unsafe ramp advance |
| Telemetry gap | Required metrics are missing or stale | Decision confidence decreases |
| Trust degradation latency | Trust falls after the last accepted sample | Late abort or delayed fallback |
| Stability dip masking | Short instability is hidden by sparse sampling | Recovered path appears stable |
| Source bias | LIGHT mode relies on fewer telemetry sources | Lower evidence diversity |
| Resolver blind spot | Resolver receives reduced context | Arbitration quality decreases |
| Fast Mode isolation effect | Fast Mode traffic may be separated from normal routing telemetry | Observed state may not match routing state |

---

## 6. FULL vs LIGHT Observation

| Item | FULL Observation | LIGHT Observation |
|------|------------------|-------------------|
| Primary goal | Safety and evidence completeness | Lower latency and lower telemetry cost |
| Telemetry density | High | Reduced |
| Required metrics | trust, stability, health, freshness, confidence, path behavior | Minimum safe subset only |
| Stability detection | Direct and repeated | Partial or delayed |
| False negative tolerance | Low | Must be explicitly bounded |
| Recovery ramp advance | Allowed after stable evidence | Hold unless promotion conditions are met |
| Abort behavior | Immediate on instability | Must remain immediate for hard failures |
| Resolver involvement | Optional on clear evidence | Required when confidence is reduced |
| Evidence Matrix status | Formal integration candidate for FULL | Hold for LIGHT |

---

## 7. Minimum LIGHT Observation Inputs

LIGHT observation must provide at least the following inputs before it can participate in recovery ramp decisions:

- path health
- trust score
- stability score or stability proxy
- telemetry freshness
- telemetry confidence
- hard failure indicator
- observation mode identifier

If any of these inputs are unavailable, LIGHT observation must not trigger `RETURN_RAMP_ADVANCE`.

---

## 8. Safety Boundary Rules

### 8.1 No Advance on Missing Evidence

If trust, stability, confidence, or freshness is missing, PSC must keep the current ramp weight.

Expected behavior:

```text
RULE-22_RETURN_RAMP_HOLD
```

### 8.2 Hard Failure Always Aborts

LIGHT observation may reduce normal telemetry, but it must not ignore hard failure indicators.

Expected behavior:

```text
RULE-23_RETURN_RAMP_ABORT
```

### 8.3 Reduced Confidence Requires Stricter Gating

When telemetry confidence is reduced, LIGHT observation must require stricter trust and stability conditions than FULL observation.

### 8.4 Resolver Review on Ambiguity

If LIGHT observation cannot distinguish stable recovery from masked instability, the decision must be escalated or held.

### 8.5 No Promotion by Performance Alone

Higher throughput or lower latency must not be sufficient to advance the ramp under LIGHT observation.

---

## 9. RULE-21 LIGHT Promotion Conditions

`RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` may be promoted from Hold to Formal integration candidate only when all of the following conditions are defined:

| Condition | Requirement |
|-----------|-------------|
| Minimum telemetry set | Required LIGHT inputs are explicitly defined |
| Freshness bound | Maximum accepted telemetry age is defined |
| Confidence floor | Minimum confidence for LIGHT advance is defined |
| False negative bound | Stability miss tolerance is defined |
| Abort override | Hard failure abort is always active |
| Resolver fallback | Ambiguous LIGHT evidence triggers hold or escalation |
| Ramp rate limit | LIGHT advancement is slower or no faster than FULL |
| Validation log | Dedicated LIGHT validation log exists |
| Evidence Matrix update | LIGHT behavior is mapped to scenario, STEP, and log |

Until these conditions are met, LIGHT advancement remains Hold.

---

## 10. Provisional Decision

The current design position is:

```text
RULE-21_RETURN_RAMP_ADVANCE (FULL)
  -> Formal integration candidate

RULE-21_RETURN_RAMP_ADVANCE (LIGHT)
  -> Hold
```

This preserves the safety boundary while allowing Fast Mode exploration to continue.

---

## 11. Next Work

1. Define the minimum LIGHT telemetry input set.
2. Define freshness and confidence thresholds for LIGHT observation.
3. Add a dedicated LIGHT recovery ramp validation scenario.
4. Update Evidence Matrix after validation.
5. Decide whether LIGHT advance remains a variant of RULE-21 or receives a separate RULE number.
