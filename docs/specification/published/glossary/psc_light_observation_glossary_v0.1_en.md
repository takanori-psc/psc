# PSC LIGHT Observation Glossary v0.1 (English Version)

## 1. Document Information

- Document Name : PSC LIGHT Observation Glossary
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Telemetry / Fast Mode / Validation
- Document Type : Glossary
- Status : Published Draft
- Author : T. Hirose
- Created : 2026-06-02
- Last Updated : 2026-06-02
- Language : English

- Related Documents:
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC LIGHT Observation Validation Plan v0.1
  - PSC Telemetry Model v0.2
  - PSC RCU Recovery Return Model v0.2
  - PSC Evidence Matrix v0.1

---

## 2. Purpose

This glossary defines LIGHT Observation terminology used by current PSC
validation scenarios, evidence logs, and promotion discussions.

The terms below describe PSC behavior. They are not generic industry definitions.
In PSC, LIGHT Observation is intentionally conservative: reduced observation
does not automatically permit return ramp advancement.

---

## 3. Glossary Terms

### 3.1 LIGHT Observation

- Definition: A reduced observation mode that uses a minimum safe telemetry set instead of full telemetry density.
- PSC Context: LIGHT Observation may reduce telemetry cost or latency during recovery, but it gives the RCU and Resolver less evidence than FULL Observation.
- Why it matters: PSC must compensate for reduced evidence with stricter gating, freshness checks, confidence checks, hold behavior, or Resolver review. LIGHT Observation does not by itself authorize ramp advancement.
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`, `RULE-23_RETURN_RAMP_ABORT`, `RULE-05_ESCALATE_conflict`

### 3.2 FULL Observation

- Definition: The conservative observation mode that uses denser and more complete telemetry during PSC control decisions.
- PSC Context: FULL Observation is the baseline mode for recovery ramp validation and abort behavior. It provides stronger evidence for stability, trust, path health, and hard failure detection.
- Why it matters: FULL Observation is the comparison point for deciding whether LIGHT Observation has enough evidence to advance, hold, abort, or escalate.
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-23_RETURN_RAMP_ABORT`

### 3.3 False Negative

- Definition: A condition where actual path instability exists but LIGHT Observation does not detect it directly.
- PSC Context: The `light_false_negative` validation scenario models a recovery ramp where instability is present while the LIGHT sample appears acceptable.
- Why it matters: Advancing the return ramp after a false negative could return traffic to an unstable path. PSC therefore emits `RULE-22_RETURN_RAMP_HOLD` because the observed evidence is insufficient to prove safe advancement.
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`

### 3.4 Masked Instability

- Definition: A condition where a stability proxy appears healthy while hidden instability still exists.
- PSC Context: The `light_masked_instability` scenario models reduced observation that hides risk behind an acceptable proxy signal.
- Why it matters: PSC treats the proxy as evidence, not truth. When hidden instability cannot be ruled out, the Resolver cannot safely advance the return ramp, so PSC emits `RULE-22_RETURN_RAMP_HOLD`.
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`, `RULE-05_ESCALATE_conflict`

### 3.5 Stale Telemetry

- Definition: Telemetry that exists but is older than the accepted freshness window for the current decision.
- PSC Context: The `light_stale_telemetry` scenario models outdated LIGHT telemetry with insufficient confidence for ramp advancement.
- Why it matters: Old telemetry may no longer describe the current path state. PSC emits `RULE-22_RETURN_RAMP_HOLD` because stale evidence cannot justify increasing recovered-path traffic.
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`

### 3.6 Telemetry Freshness

- Definition: The age and validity window of telemetry used for a PSC decision.
- PSC Context: Freshness is one of the minimum LIGHT Observation inputs. A sample must be current enough to support trust, stability, confidence, and ramp-state decisions.
- Why it matters: Reduced observation increases the risk that an accepted sample is no longer representative. If freshness is missing or stale, PSC must hold rather than advance.
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`

### 3.7 Observation Confidence

- Definition: The decision confidence PSC assigns to observed telemetry after considering completeness, freshness, and observation mode.
- PSC Context: LIGHT Observation can have lower confidence because it relies on fewer signals, lower density, or proxy measurements.
- Why it matters: Confidence determines whether evidence can support advance, must hold, or should be escalated. Insufficient confidence keeps the return ramp in Hold.
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`, `RULE-05_ESCALATE_conflict`

### 3.8 Hold

- Definition: A PSC behavior category where the current selected path or current return ramp weight is maintained.
- PSC Context: LIGHT validation uses `expected_category=hold` when evidence is insufficient for `RETURN_RAMP_ADVANCE`.
- Why it matters: Hold is the conservative result that prevents uncertain observation from increasing exposure to a recovered path.
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`, `RULE-20_RETURN_KEEP`, `RULE-11_RECOVERY_cooldown`

### 3.9 Return Ramp

- Definition: The progressive reintegration process that gradually increases traffic weight on a recovered path.
- PSC Context: Return Ramp runs after recovery validation and before full traffic return. It remains observable and abortable during reintegration.
- Why it matters: The ramp limits recovery risk by changing traffic allocation in stages rather than switching immediately.
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`, `RULE-23_RETURN_RAMP_ABORT`, `RULE-24_RETURN_RAMP_COMPLETE`

### 3.10 Return Ramp Advance

- Definition: A PSC decision to increase recovered-path traffic weight during the Return Ramp.
- PSC Context: Under FULL Observation, advance can occur after stable evidence. Under LIGHT Observation, advance remains blocked until promotion conditions are satisfied.
- Why it matters: Advance increases exposure to the recovered path. PSC must not advance from LIGHT evidence alone when false negative, stale telemetry, or masked instability risks remain unresolved.
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`

### 3.11 RULE-22_RETURN_RAMP_HOLD

- Definition: The PSC rule emitted when the Return Ramp must keep its current weight because advancement conditions are not satisfied.
- PSC Context: Current LIGHT validation scenarios use this rule for false negative, stale telemetry, masked instability, telemetry gap, and other insufficient-evidence cases.
- Why it matters: The rule records that PSC intentionally chose conservative hold behavior rather than treating LIGHT Observation as permission to advance.
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-23_RETURN_RAMP_ABORT`, `RULE-05_ESCALATE_conflict`

### 3.12 Observation Promotion

- Definition: The process of moving a LIGHT Observation behavior from Hold status toward formal advance eligibility.
- PSC Context: Promotion applies to `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` only after minimum telemetry, freshness bounds, confidence floors, false negative bounds, masked-instability handling, and evidence logs are defined.
- Why it matters: Promotion prevents performance or lower telemetry cost from becoming the only reason to advance the ramp.
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`

### 3.13 Observation Escalation

- Definition: A PSC behavior where reduced or conflicting observation evidence is sent to Resolver review instead of being resolved by the local LIGHT decision path.
- PSC Context: LIGHT Observation may escalate when trust, stability proxy, freshness, or confidence cannot distinguish recovery from risk.
- Why it matters: Escalation preserves PSC safety when hold alone is not enough to explain or arbitrate ambiguous evidence.
- Related Rules: `RULE-05_ESCALATE_conflict`, `RULE-12_COOLDOWN_active`, `RULE-22_RETURN_RAMP_HOLD`

---

## 4. Validation Alignment

The current LIGHT Observation validation scenarios use these terms as follows.

| Scenario | Term focus | Expected category | Expected rule | Reason |
|----------|------------|-------------------|---------------|--------|
| light_false_negative | False Negative | hold | `RULE-22_RETURN_RAMP_HOLD` | `OBSERVATION_FALSE_NEGATIVE` |
| light_stale_telemetry | Stale Telemetry | hold | `RULE-22_RETURN_RAMP_HOLD` | `STALE_TELEMETRY` |
| light_masked_instability | Masked Instability | hold | `RULE-22_RETURN_RAMP_HOLD` | `MASKED_INSTABILITY` |

These scenarios confirm that LIGHT Observation is conservative until the
promotion criteria for ramp advancement are explicitly satisfied.
