# PSC Rule Dependency Diagram

この図は Evidence Matrix と現在の simulation logs の active rule 名を使用する。
Published RCU model の内部処理段階は `STEP-*` であり、運用上の `RULE-*`
identifier ではない。

```mermaid
flowchart LR
    subgraph Observation
        OBS["Observation inputs<br/>trust, health, score, stability, freshness, confidence"]
        LIGHT["LIGHT Boundary<br/>FULL promotion または explicit gates まで Hold"]
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
        R03["RULE-03_SWITCH_trust<br/>active, final-action 未 Verified"]
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
    LIGHT -. "historical LIGHT advance logs<br/>current policy ではない" .-> R21

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
| RULE-01 | escalation、cooldown、recovery、switch gate が action を強制しない場合の default keep。 |
| RULE-02 | local score improvement が switch threshold に達することに依存する。 |
| RULE-03 | collision matrix では trust-switch candidate として active だが、final-action 専用 scenario までは Verified ではない。 |
| RULE-04 | Verified safety block。`trust_block_vs_switch` で `RULE-02_SWITCH_score` と `RULE-03_SWITCH_trust` より優先される。 |
| RULE-05 | ambiguity/conflict に依存し Resolver を呼び出す。 |
| RULE-06 | future reserved slot。現在の active Evidence Matrix owner はない。 |
| RULE-07 | selected/current path invalidation または no valid path に依存する。 |
| RULE-08 | maintainable fallback がある degraded mode に依存する。 |
| RULE-09 | fallback selection change が必要な degraded mode に依存する。 |
| RULE-10 | DEGRADED mode と stable trusted recovery path に依存する。 |
| RULE-11 | recovery または return completion が recovery cooldown を設定することに依存する。 |
| RULE-12 | Resolver execution が resolver cooldown を設定することに依存する。 |
| RULE-13 | Resolver が current selection を返すことに依存する。 |
| RULE-14 | Resolver が different selection を返すことに依存する。 |
| RULE-15 | recovered path が trust / stability candidate thresholds を満たすことに依存する。 |
| RULE-16 | candidate が validation window を継続することに依存する。 |
| RULE-17 | Legacy Concept。現在の code は `RULE-16` の直後に `RULE-18` を emit する。 |
| RULE-18 | validation window completion に依存する。 |
| RULE-19 | Verified v0.2 direct return switch。Return Ramp start の owner ではない。 |
| RULE-20 | return eligible だが return margin が不足する場合に依存する。 |
| RULE-21 | operational `RULE-21` owner は `RULE-21_RETURN_RAMP_ADVANCE`。LIGHT variant は promotion まで Hold。 |
| RULE-21_RETURN_ESCALATE | v0.2 history のためだけに残る Legacy Concept。 |
| RULE-22 | 現在の authoritative LIGHT behavior。FULL promotion または explicit gates まで Hold。 |
| RULE-23 | unstable/invalid recovered path、hard failure、abort class に依存する。 |
| RULE-24 | progressive ramp が target weight に到達することに依存する。 |
| RULE-25 | Experimental v0.3 ramp entry。v0.2 direct return execution point を置換するが `RULE-19` と同義ではない。 |
