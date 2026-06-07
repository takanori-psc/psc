# PSC Rule Dependency Diagram

This diagram uses the active rule names from the Evidence Matrix and current
simulation logs. Published RCU model processing stages are `STEP-*`, not
operational `RULE-*` identifiers.

```mermaid
flowchart LR
    subgraph Observation
        OBS["Observation inputs<br/>trust, health, score, stability, freshness, confidence"]
        LIGHT["LIGHT Boundary<br/>Hold unless FULL promotion or explicit gates"]
    end

    subgraph KEEP_BLOCK
        R01["RULE-01_KEEP_score"]
        R04["RULE-04_BLOCK_trust<br/>Verified"]
        R11["RULE-11_RECOVERY_cooldown"]
        R12["RULE-12_COOLDOWN_active"]
        R13["RULE-13_RESOLVER_keep"]
        R20["RULE-20_RETURN_KEEP"]
        R22["RULE-22_RETURN_RAMP_HOLD"]
    end

    subgraph SWITCH_RAMP
        R02["RULE-02_SWITCH_score"]
        R03["RULE-03_SWITCH_trust<br/>active, not Verified final action"]
        R09["RULE-09_DEGRADE_switch"]
        R14["RULE-14_RESOLVER_switch"]
        R19["RULE-19_RETURN_SWITCH<br/>Verified v0.2 direct return"]
        R21["RULE-21_RETURN_RAMP_ADVANCE<br/>Experimental operational RULE-21 owner"]
        R24["RULE-24_RETURN_RAMP_COMPLETE"]
        R25["RULE-25_RETURN_RAMP_START<br/>Experimental v0.3 ramp entry"]
    end

    subgraph ESCALATE
        R05["RULE-05_ESCALATE_conflict"]
        R21E["RULE-21_RETURN_ESCALATE<br/>Legacy Concept"]
    end

    subgraph DEGRADE
        R07["RULE-07_DEGRADE_trigger"]
        R08["RULE-08_DEGRADE_keep"]
    end

    subgraph RECOVERY
        R10["RULE-10_RECOVERY_trigger"]
        R15["RULE-15_RECOVERY_CANDIDATE"]
        R16["RULE-16_RECOVERY_VALIDATION_START"]
        R17["RULE-17_RECOVERY_VALIDATION_PASS<br/>Legacy Concept"]
        R18["RULE-18_RETURN_ELIGIBLE"]
    end

    subgraph ABORT
        R23["RULE-23_RETURN_RAMP_ABORT"]
    end

    subgraph CollisionMatrix
        CM["Partial arbitration model<br/>active priority: RULE-01..05, RULE-22..24"]
    end

    OBS --> R01
    OBS --> R02
    OBS --> R03
    OBS --> R04
    OBS --> R05
    OBS --> R07

    LIGHT --> R22
    LIGHT --> R23
    LIGHT --> R05
    LIGHT -. "historical LIGHT advance logs<br/>not current policy" .-> R21

    R07 --> R08
    R07 --> R09
    R08 --> R10
    R09 --> R10
    R10 --> R11
    R10 --> R15
    R15 --> R16
    R16 --> R18
    R16 -. "legacy marker" .-> R17

    R18 --> R20
    R18 --> R19
    R18 --> R25
    R19 --> R11
    R25 --> R22
    R25 --> R21
    R22 --> R21
    R21 --> R22
    R21 --> R23
    R21 --> R24
    R24 --> R11

    R05 --> R13
    R05 --> R14
    R13 --> R12
    R14 --> R12
    R12 --> R01

    R23 --> R05
    R23 --> R07
    R21E -. "legacy only" .-> R05

    CM --> R01
    CM --> R02
    CM --> R03
    CM --> R04
    CM --> R05
    CM --> R22
    CM --> R23
    CM --> R24
```

## Dependency Notes

| Rule | Dependency / ownership note |
|------|-----------------------------|
| RULE-01 | Default local keep after escalation, cooldown, recovery, and switch gates do not force action. |
| RULE-02 | Depends on local score improvement reaching switch threshold. |
| RULE-03 | Active in collision matrix as a trust-switch candidate, but not promoted to Verified without a dedicated final-action scenario. |
| RULE-04 | Verified safety block. It takes priority over `RULE-02_SWITCH_score` and `RULE-03_SWITCH_trust` in `trust_block_vs_switch`. |
| RULE-05 | Depends on ambiguity/conflict and invokes Resolver. |
| RULE-06 | Future reserved slot; no current active Evidence Matrix owner. |
| RULE-07 | Depends on selected/current path invalidation or no valid path. |
| RULE-08 | Depends on degraded mode with maintainable fallback. |
| RULE-09 | Depends on degraded mode requiring fallback selection change. |
| RULE-10 | Depends on DEGRADED mode plus stable trusted recovery path. |
| RULE-11 | Depends on recovery or return completion setting recovery cooldown. |
| RULE-12 | Depends on Resolver execution setting resolver cooldown. |
| RULE-13 | Depends on Resolver returning current selection. |
| RULE-14 | Depends on Resolver returning a different selection. |
| RULE-15 | Depends on a recovered path meeting trust and stability candidate thresholds. |
| RULE-16 | Depends on candidate continuation through validation window. |
| RULE-17 | Legacy Concept; current code emits `RULE-18` directly after `RULE-16`. |
| RULE-18 | Depends on validation window completion. |
| RULE-19 | Verified v0.2 direct return switch. It is not the Return Ramp start owner. |
| RULE-20 | Depends on return eligibility with insufficient return margin. |
| RULE-21 | Operational `RULE-21` owner is `RULE-21_RETURN_RAMP_ADVANCE`; LIGHT variant remains Hold unless promoted. |
| RULE-21_RETURN_ESCALATE | Legacy Concept retained only for v0.2 history. |
| RULE-22 | Current authoritative LIGHT behavior resolves to Hold unless FULL promotion or explicit gates exist. |
| RULE-23 | Depends on unstable/invalid recovered path, hard failure, or abort class. |
| RULE-24 | Depends on progressive ramp reaching target weight. |
| RULE-25 | Experimental v0.3 ramp entry; replaces the v0.2 direct return execution point but is not semantically identical to `RULE-19`. |
