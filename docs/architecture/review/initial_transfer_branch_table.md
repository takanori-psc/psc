# PSC Branch List From Initial Transfer State

This document is not a new specification. It is a review / navigation aid
derived from the current Evidence Matrix and review diagrams. It helps inspect
reachable branches from `NORMAL_TRANSFER` / the initial forwarding state as
current state -> condition -> selected RULE -> next state.

This document is intended to answer: "PSC is currently here. What can happen
next?" Use it to navigate from the current PSC position through initial
transfer, DEGRADED, RECOVERY, RETURN, RETURN_RAMP, LIGHT_POLICY, and LEGACY
paths.

## How To Read

- Start from the current state.
- Match the condition.
- Follow the selected RULE to the next state.
- Do not treat Legacy Concept rows as active runtime paths.

## Recommended Review Order

1. Overall Map
2. Quick Reference
3. Detailed Branches
4. Legacy / Historical Notes

## Overall Map

```text
NORMAL_TRANSFER
|
|- RULE-01_KEEP_score
|- RULE-02_SWITCH_score
|- RULE-03_SWITCH_trust
|- RULE-04_BLOCK_trust
|- RULE-05_ESCALATE_conflict ----------------> RESOLVER_REVIEW
`- RULE-07_DEGRADE_trigger
        |
        v
     DEGRADED
        |
        |- RULE-08_DEGRADE_keep
        |- RULE-09_DEGRADE_switch
        `- RULE-10_RECOVERY_trigger
                |
                v
          RECOVERY
                |
        RULE-15_RECOVERY_CANDIDATE
                |
        RULE-16_RECOVERY_VALIDATION_START
                |
        RULE-18_RETURN_ELIGIBLE
                |
        +-------+---------------------------+
        |                                   |
      v0.2                                v0.3
        |                                   |
 RULE-19_RETURN_SWITCH             RULE-25_RETURN_RAMP_START
        |                                   |
        v                                   v
 NORMAL_TRANSFER                    RETURN_RAMP
                                            |
                      +---------------------+---------------------+
                      |                     |                     |
        RULE-22_RETURN_RAMP_HOLD  RULE-21_RETURN_RAMP_ADVANCE  RULE-23_RETURN_RAMP_ABORT
                      |                     |                     |
                      +----------> RETURN_RAMP <------------------+
                                            |
                              RULE-24_RETURN_RAMP_COMPLETE
                                            |
                                            v
                                     NORMAL_TRANSFER

LIGHT_POLICY:
  LIGHT observation normally resolves to RULE-22_RETURN_RAMP_HOLD until
  FULL promotion or explicit LIGHT promotion gates are satisfied.
```

## PSC Control Flow Quick Reference

| Area | Main branch | Selected RULE | Next state / result | Status |
|------|-------------|---------------|---------------------|--------|
| Initial transfer / NORMAL | Keep current path | RULE-01_KEEP_score | NORMAL_TRANSFER | Verified |
| Initial transfer / NORMAL | Local score switch | RULE-02_SWITCH_score | NORMAL_TRANSFER | Verified |
| Initial transfer / NORMAL | Trust-based switch candidate | RULE-03_SWITCH_trust | NORMAL_TRANSFER | Active. Verified final-action coverage is not ready |
| Initial transfer / NORMAL | Block unsafe / trust-blocked switch | RULE-04_BLOCK_trust | BLOCK_SWITCH | Verified safety block |
| Initial transfer / NORMAL | Delegate ambiguity / conflict to Resolver | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Verified |
| Initial transfer / NORMAL | No usable trusted path | RULE-07_DEGRADE_trigger | DEGRADED | Verified |
| DEGRADED | Keep / switch fallback | RULE-08_DEGRADE_keep / RULE-09_DEGRADE_switch | DEGRADED | Verified |
| DEGRADED | Stable trusted recovery path detected | RULE-10_RECOVERY_trigger | RECOVERY_CANDIDATE | Verified |
| Recovery validation | Register candidate and start validation | RULE-15_RECOVERY_CANDIDATE / RULE-16_RECOVERY_VALIDATION_START | VALIDATING | Verified |
| Recovery validation | Become return eligible after validation pass | RULE-18_RETURN_ELIGIBLE | RETURN_ELIGIBLE | Verified. `RULE-17` is not emitted |
| Return execution | v0.2 direct return | RULE-19_RETURN_SWITCH | NORMAL_TRANSFER / RECOVERY_COOLDOWN | Verified v0.2 |
| Return execution | Return margin is insufficient | RULE-20_RETURN_KEEP | NORMAL_TRANSFER | Verified |
| Return execution | Start v0.3 progressive ramp | RULE-25_RETURN_RAMP_START | RETURN_RAMP | Experimental. Not synonymous with `RULE-19` |
| Return ramp | Hold / advance / abort / complete | RULE-22 / RULE-21 / RULE-23 / RULE-24 | RETURN_RAMP / ABORT_STABILIZATION / NORMAL_TRANSFER | Experimental. `RULE-21` owner is `RULE-21_RETURN_RAMP_ADVANCE` |
| LIGHT policy | Hold until FULL promotion or explicit gates | RULE-22_RETURN_RAMP_HOLD | RETURN_RAMP | Current authoritative policy |
| LIGHT policy | Hard failure / unsafe recovered path | RULE-23_RETURN_RAMP_ABORT | ABORT_STABILIZATION | Safety-first |
| LIGHT policy | Ambiguous evidence | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Verified escalation |
| Legacy / reserved | Validation pass marker / return escalation / future slot | RULE-17 / RULE-21_RETURN_ESCALATE / RULE-06 | No active runtime path | Legacy Concept / future reserved |

In the Quick Reference, `RULE-22 / RULE-21 / RULE-23 / RULE-24` refer to
`RULE-22_RETURN_RAMP_HOLD`, `RULE-21_RETURN_RAMP_ADVANCE`,
`RULE-23_RETURN_RAMP_ABORT`, and `RULE-24_RETURN_RAMP_COMPLETE`.
Historical v0.3 LIGHT advance logs are not current LIGHT policy.

---

## NORMAL

## Initial Transfer / NORMAL Branches

| Current state | Condition | Selected RULE | Next state | Notes / status |
|---------------|-----------|---------------|------------|----------------|
| NORMAL_TRANSFER / initial forwarding state | Keep current path because score improvement does not pass hysteresis / switch threshold | RULE-01_KEEP_score | NORMAL_TRANSFER | Verified keep rule |
| NORMAL_TRANSFER / initial forwarding state | Local score is clearly better and no trust block or escalation applies | RULE-02_SWITCH_score | NORMAL_TRANSFER | Verified local switch rule |
| NORMAL_TRANSFER / initial forwarding state | Trust prefers a switch candidate | RULE-03_SWITCH_trust | NORMAL_TRANSFER | Active in collision matrix, but Verified promotion is pending a final-action scenario |
| NORMAL_TRANSFER / initial forwarding state | Score / trust switch candidate points to an unsafe or trust-blocked path | RULE-04_BLOCK_trust | NORMAL_TRANSFER / BLOCK_SWITCH | Verified safety block. Takes priority over `RULE-02_SWITCH_score` and `RULE-03_SWITCH_trust`, producing `BLOCK_SWITCH` |
| NORMAL_TRANSFER / initial forwarding state | Trust / stability / score conflict or ambiguity should not be resolved by local action | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Verified escalation rule |
| NORMAL_TRANSFER / initial forwarding state | Selected / current path is invalid, or there is no usable trusted path | RULE-07_DEGRADE_trigger | DEGRADED | Verified degrade entry rule |

---

## DEGRADED

## DEGRADED Branches

| Current state | Condition | Selected RULE | Next state | Notes / status |
|---------------|-----------|---------------|------------|----------------|
| DEGRADED | Maintainable fallback can be kept | RULE-08_DEGRADE_keep | DEGRADED | Verified degraded keep rule |
| DEGRADED | Degraded fallback switch is required | RULE-09_DEGRADE_switch | DEGRADED | Verified degraded switch rule |
| DEGRADED | Stable trusted recovery path exists | RULE-10_RECOVERY_trigger | RECOVERY_CANDIDATE / NORMAL recovery path | Verified recovery trigger |

---

## RECOVERY

## Recovery Validation Branches

| Current state | Condition | Selected RULE | Next state | Notes / status |
|---------------|-----------|---------------|------------|----------------|
| DEGRADED / recovery path | Recovered path satisfies trust / stability candidate thresholds | RULE-15_RECOVERY_CANDIDATE | RECOVERY_CANDIDATE | Verified recovery candidate rule |
| RECOVERY_CANDIDATE | Start or continue candidate validation window | RULE-16_RECOVERY_VALIDATION_START | VALIDATING | Verified validation start rule |
| VALIDATING | Validation window completes and return eligibility is met | RULE-18_RETURN_ELIGIBLE | RETURN_ELIGIBLE | Verified. Current code moves directly from `RULE-16` to `RULE-18` with `reason="VALIDATION_PASSED"` |
| VALIDATING | Legacy concept that modeled validation pass as a distinct stage | RULE-17_RECOVERY_VALIDATION_PASS | VALIDATION_PASS_LEGACY | Legacy Concept only. Not an active runtime path |

---

## RETURN

## Return Execution Branches

| Current state | Condition | Selected RULE | Next state | Notes / status |
|---------------|-----------|---------------|------------|----------------|
| RETURN_ELIGIBLE | Execute v0.2 direct return | RULE-19_RETURN_SWITCH | NORMAL_TRANSFER / RECOVERY_COOLDOWN | Verified v0.2 direct return rule |
| RETURN_ELIGIBLE | Return margin is insufficient, so current path is kept | RULE-20_RETURN_KEEP | NORMAL_TRANSFER | Verified return keep rule |
| RETURN_ELIGIBLE | Enter v0.3 progressive ramp | RULE-25_RETURN_RAMP_START | RETURN_RAMP | Experimental v0.3 ramp entry. Not semantically identical to `RULE-19_RETURN_SWITCH` |

---

## RETURN_RAMP

## Return Ramp Branches

| Current state | Condition | Selected RULE | Next state | Notes / status |
|---------------|-----------|---------------|------------|----------------|
| RETURN_RAMP | More observation is required, or advance conditions are not met | RULE-22_RETURN_RAMP_HOLD | RETURN_RAMP | Experimental hold rule. Also the current authoritative LIGHT policy behavior |
| RETURN_RAMP | FULL observation or promoted evidence is stable and advance conditions are met | RULE-21_RETURN_RAMP_ADVANCE | RETURN_RAMP | Operational `RULE-21` owner. FULL or promoted evidence only |
| RETURN_RAMP | Recovered path is unstable / invalid, hard failure occurs, or abort class applies | RULE-23_RETURN_RAMP_ABORT | ABORT_STABILIZATION | Experimental abort rule |
| RETURN_RAMP | Progressive ramp reaches target weight | RULE-24_RETURN_RAMP_COMPLETE | NORMAL_TRANSFER / RECOVERY_COOLDOWN | Experimental ramp complete rule |

---

## LIGHT_POLICY

## LIGHT Policy Branches

| Current state | Condition | Selected RULE | Next state | Notes / status |
|---------------|-----------|---------------|------------|----------------|
| LIGHT_BOUNDARY | LIGHT observation is missing / stale / low confidence, or no explicit promotion gate exists | RULE-22_RETURN_RAMP_HOLD | RETURN_RAMP | Current authoritative LIGHT policy |
| LIGHT_BOUNDARY | Hard failure or unsafe recovered path is detected | RULE-23_RETURN_RAMP_ABORT | ABORT_STABILIZATION | Safety-first abort |
| LIGHT_BOUNDARY | Evidence is ambiguous and insufficient for local decision | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Delegates to Resolver review |
| LIGHT_BOUNDARY | Promoted to FULL, or explicit LIGHT promotion gates are defined and satisfied | versioned normal ramp path | FULL observation / RETURN_RAMP | Joins FULL observation / normal ramp path |
| LIGHT_BOUNDARY | Historical v0.3 log shows LIGHT advance | RULE-21_RETURN_RAMP_ADVANCE | Not current policy | `ramp_light_tolerates_moderate_dip` and similar logs are historical experimental behavior, not current LIGHT policy |

---

## LEGACY

## Legacy / Historical Notes

| Current state | Condition | Selected RULE | Next state | Notes / status |
|---------------|-----------|---------------|------------|----------------|
| VALIDATING | Legacy wording records validation pass as a distinct stage | RULE-17_RECOVERY_VALIDATION_PASS | VALIDATION_PASS_LEGACY | Legacy Concept. Current code transitions directly from `RULE-16` to `RULE-18` |
| RETURN / escalation history | v0.2 recovery return escalation label | RULE-21_RETURN_ESCALATE | RESOLVER_REVIEW / legacy only | Legacy Concept. Not the operational `RULE-21` owner |
| reserved namespace | Future-use reserved number | RULE-06 | none | Future reserved. No current active Evidence Matrix owner |

## Notes

- The collision matrix is partial arbitration only, not complete PSC-wide rule arbitration.
- `RULE-03_SWITCH_trust` requires a dedicated final-action validation scenario before Verified promotion.
- `RULE-25_RETURN_RAMP_START` remains Experimental until formal v0.3 integration.
