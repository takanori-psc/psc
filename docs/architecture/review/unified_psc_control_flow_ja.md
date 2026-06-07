# 統合 PSC 制御フロー レビュー

本レビュー図は、現在の Evidence Matrix、制御シミュレーション、
LIGHT boundary draft、abort handling draft、および collision matrix の
scope note に基づく。公開仕様およびシミュレーションコードは変更しない。

## 参照元

- 運用 RULE traceability: `docs/specification/validation/psc_evidence_matrix_v0.1_ja.md`
- Published RCU Decision Model: `docs/specification/published/models/psc_rcu_decision_model_v0.1_ja.md`
- Recovery return / ramp behavior: `sim/02_controlled/06_recovery_return_v02/`
- LIGHT observation boundary: `docs/specification/draft/models/psc_fast_mode_light_observation_boundary_v0.1_ja.md`
- Abort handling: `docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_ja.md`
- Rule collision priority subset: `sim/02_controlled/09_rule_collision_matrix/`

## Namespace Note

Published RCU Decision Model は、内部処理段階を `STEP-*` で表す。
運用上の `RULE-*` identifier は Evidence Matrix / validation namespace と
simulation logs が所有する。

Legacy Concept:

- `RULE-17_RECOVERY_VALIDATION_PASS` は Legacy Concept。現在の code は
  `RULE-16_RECOVERY_VALIDATION_START` から `RULE-18_RETURN_ELIGIBLE` へ
  `reason="VALIDATION_PASSED"` で直接進む。
- `RULE-21_RETURN_ESCALATE` は Legacy Concept。運用上の `RULE-21` 所有者は
  `RULE-21_RETURN_RAMP_ADVANCE` である。

## RULE 所有関係

| Rule | 現在の意味 | Category | Review status |
|------|------------|----------|---------------|
| RULE-01_KEEP_score | hysteresis / 小幅改善時に selected path を維持 | KEEP | Verified |
| RULE-02_SWITCH_score | 明確な score 優位で切替 | SWITCH | Verified |
| RULE-03_SWITCH_trust | collision matrix 内の trust-driven switch candidate | SWITCH | Active; final-action 専用検証まで Verified ではない |
| RULE-04_BLOCK_trust | trust により unsafe switch を block | KEEP / BLOCK | Verified |
| RULE-05_ESCALATE_conflict | trust/stability/score の曖昧性を Resolver へ escalation | ESCALATE | Verified |
| RULE-06 | active Evidence Matrix owner なし | Reserved | Future reserved |
| RULE-07_DEGRADE_trigger | selected/current path invalid で DEGRADED へ | DEGRADE | Verified |
| RULE-08_DEGRADE_keep | degraded fallback path を維持 | DEGRADE / KEEP | Verified |
| RULE-09_DEGRADE_switch | degraded fallback path へ切替 | DEGRADE / SWITCH | Verified |
| RULE-10_RECOVERY_trigger | stable trusted path で DEGRADED から NORMAL へ | RECOVERY | Verified |
| RULE-11_RECOVERY_cooldown | recovery 直後の再切替を抑制 | RECOVERY / KEEP | Verified |
| RULE-12_COOLDOWN_active | Resolver cooldown 中の再 escalation 抑制 | ESCALATE / KEEP guard | Verified |
| RULE-13_RESOLVER_keep | Resolver が current path を維持 | KEEP / RESOLVER | Verified |
| RULE-14_RESOLVER_switch | Resolver が別 path へ切替 | SWITCH / RESOLVER | Verified |
| RULE-15_RECOVERY_CANDIDATE | recovered path を candidate 登録 | RECOVERY | Verified |
| RULE-16_RECOVERY_VALIDATION_START | recovery candidate validation を開始/継続 | RECOVERY | Verified |
| RULE-17_RECOVERY_VALIDATION_PASS | validation pass marker | RECOVERY | Legacy Concept |
| RULE-18_RETURN_ELIGIBLE | candidate を return eligible にする | RECOVERY | Verified |
| RULE-19_RETURN_SWITCH | Verified v0.2 direct return switch | RECOVERY / SWITCH | Verified |
| RULE-20_RETURN_KEEP | return margin 未達で current path 維持 | RECOVERY / KEEP | Verified |
| RULE-21_RETURN_RAMP_ADVANCE | FULL / promoted 条件下で recovery ramp advance | RECOVERY / SWITCH | Experimental; operational RULE-21 owner |
| RULE-21_RETURN_ESCALATE | v0.2 return escalation label | ESCALATE | Legacy Concept |
| RULE-22_RETURN_RAMP_HOLD | current ramp weight 維持 | RECOVERY / KEEP | Experimental |
| RULE-23_RETURN_RAMP_ABORT | active return ramp attempt を abort | ABORT | Experimental |
| RULE-24_RETURN_RAMP_COMPLETE | progressive reintegration 完了 | RECOVERY / SWITCH | Experimental |
| RULE-25_RETURN_RAMP_START | v0.3 progressive ramp entry | RECOVERY / RAMP START | Experimental; RULE-01..24 Verified namespace 外 |

## Collision Matrix Scope

Collision matrix は partial arbitration model であり、PSC 全体の完全な
rule arbitration engine ではない。現在の active collision coverage は以下に集中する。

- core keep/switch/trust/block/escalation rules: `RULE-01` through `RULE-05`
- recovery ramp hold/abort/complete rules: `RULE-22` through `RULE-24`

`RULE-07` through `RULE-21` の多くは PSC evidence / logs 上では active だが、
collision predicates と priorities は collision matrix に未統合である。

## 統合 Flowchart

```mermaid
flowchart TD
    O["Observation inputs<br/>telemetry, trust, health, score, stability, freshness, confidence, observation_mode"] --> FB{"Fast Mode / LIGHT boundary?"}
    FB -->|FULL or normal observation| FULL["FULL observation evidence"]
    FB -->|LIGHT observation| LB{"LIGHT observation policy"}

    LB -->|Missing, stale, low confidence,<br/>false negative, masked instability,<br/>or no explicit promotion gate| R22L["RULE-22_RETURN_RAMP_HOLD<br/>current LIGHT policy"]
    LB -->|Hard failure or unsafe recovered path| R23L["RULE-23_RETURN_RAMP_ABORT"]
    LB -->|Ambiguous evidence| R05L["RULE-05_ESCALATE_conflict"]
    LB -->|Promoted to FULL or explicit gates satisfied| FULL

    FULL --> TF["RCU filtering and scoring<br/>published model internal stages are STEP-*"]
    TF -->|Trust/health invalid or no valid path| D0{"Fallback handling"}
    D0 -->|No usable path| R07N["RULE-07_DEGRADE_trigger"]
    D0 -->|Fallback maintainable| R08["RULE-08_DEGRADE_keep"]
    D0 -->|Fallback switch required| R09["RULE-09_DEGRADE_switch"]

    TF -->|Valid candidates| RCU["Local RCU decision<br/>score, hysteresis, persistence"]
    RCU --> CD{"Cooldown active?"}
    CD -->|Recovery cooldown| R11["RULE-11_RECOVERY_cooldown"]
    CD -->|Resolver cooldown| R12["RULE-12_COOLDOWN_active"]
    CD -->|No cooldown| ESC{"Resolver escalation condition?"}

    ESC -->|Trust/stability/score conflict| R05["RULE-05_ESCALATE_conflict"]
    R05 --> RES["Resolver evaluation"]
    RES -->|Keep current path| R13["RULE-13_RESOLVER_keep"]
    RES -->|Switch path| R14["RULE-14_RESOLVER_switch"]
    R13 --> R12
    R14 --> R12

    ESC -->|No escalation| SW{"Local action gate"}
    SW -->|Small improvement| R01["RULE-01_KEEP_score"]
    SW -->|Score switch| R02["RULE-02_SWITCH_score"]
    SW -->|Trust switch candidate| R03["RULE-03_SWITCH_trust<br/>active; not Verified final action"]
    SW -->|Trust block| R04["RULE-04_BLOCK_trust<br/>Verified safety block"]

    R07N --> DEG["DEGRADED"]
    R08 --> DEG
    R09 --> DEG
    DEG --> REC{"Stable trusted recovered path?"}
    REC -->|No| TF
    REC -->|Yes| R10["RULE-10_RECOVERY_trigger"]
    R10 --> R15["RULE-15_RECOVERY_CANDIDATE"]
    R15 --> R16["RULE-16_RECOVERY_VALIDATION_START"]
    R16 --> R18["RULE-18_RETURN_ELIGIBLE<br/>reason=VALIDATION_PASSED"]
    R16 -. "Legacy marker, not emitted" .-> R17["RULE-17_RECOVERY_VALIDATION_PASS<br/>Legacy Concept"]

    R18 --> RET{"Return execution model"}
    RET -->|v0.2 direct return| R19["RULE-19_RETURN_SWITCH<br/>Verified v0.2"]
    RET -->|Return margin not met| R20["RULE-20_RETURN_KEEP"]
    RET -->|v0.3 progressive ramp| R25["RULE-25_RETURN_RAMP_START<br/>Experimental v0.3"]

    R19 --> R11
    R20 --> R01
    R25 --> RAMP{"RETURN_RAMP"}
    RAMP -->|Hold / observe more| R22["RULE-22_RETURN_RAMP_HOLD"]
    RAMP -->|FULL or promoted evidence stable| R21["RULE-21_RETURN_RAMP_ADVANCE"]
    RAMP -->|Unstable / invalid / hard failure| R23["RULE-23_RETURN_RAMP_ABORT"]
    RAMP -->|Target reached| R24["RULE-24_RETURN_RAMP_COMPLETE"]
    R21 --> RAMP
    R22 --> RAMP
    R24 --> R11

    R23 --> ABH{"Abort handling"}
    R23L --> ABH
    ABH -->|SOFT_ABORT / HARD_ABORT| RES
    ABH -->|Emergency cut or no safe allocation| DEG
    ABH -->|Restart allowed only after re-evaluation| R25

    R21E["RULE-21_RETURN_ESCALATE<br/>Legacy Concept"] -. "not operational RULE-21 owner" .-> R05
    LIGHTHIST["Historical v0.3 LIGHT advance logs<br/>not current LIGHT policy"] -.-> R22L
```
