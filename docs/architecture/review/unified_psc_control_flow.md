# Unified PSC Control Flow Review

This review diagram reflects the current repository behavior from the Evidence
Matrix, controlled simulations, LIGHT boundary drafts, abort handling drafts,
and the collision matrix scope note. It does not modify published
specifications or simulation code.

## Source Basis

- Operational rule traceability: `docs/specification/validation/psc_evidence_matrix_v0.1_en.md`
- Published RCU Decision Model: `docs/specification/published/models/psc_rcu_decision_model_v0.1_en.md`
- Recovery return and ramp behavior: `sim/02_controlled/06_recovery_return_v02/`
- LIGHT observation boundary: `docs/specification/draft/models/psc_fast_mode_light_observation_boundary_v0.1_en.md`
- Abort handling: `docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_en.md`
- Rule collision priority subset: `sim/02_controlled/09_rule_collision_matrix/`

## Namespace Note

The published RCU Decision Model now uses `STEP-*` identifiers for internal
processing stages. Operational `RULE-*` identifiers are owned by the Evidence
Matrix / validation namespace and simulation logs.

Legacy conceptual labels:

- `RULE-17_RECOVERY_VALIDATION_PASS` is a Legacy Concept. Current code moves
  from `RULE-16_RECOVERY_VALIDATION_START` directly to
  `RULE-18_RETURN_ELIGIBLE` with `reason="VALIDATION_PASSED"`.
- `RULE-21_RETURN_ESCALATE` is a Legacy Concept. Operational `RULE-21`
  ownership belongs to `RULE-21_RETURN_RAMP_ADVANCE`.

## Rule Ownership Map

| Rule | Current meaning | Category | Review status |
|------|-----------------|----------|---------------|
| RULE-01_KEEP_score | Keep selected path under hysteresis / small improvement | KEEP | Verified |
| RULE-02_SWITCH_score | Switch on clear score advantage | SWITCH | Verified |
| RULE-03_SWITCH_trust | Trust-driven switch candidate in collision matrix | SWITCH | Active in collision matrix; not Verified until final-action scenario exists |
| RULE-04_BLOCK_trust | Block unsafe switch by trust | KEEP / BLOCK | Verified |
| RULE-05_ESCALATE_conflict | Escalate trust/stability/score ambiguity to Resolver | ESCALATE | Verified |
| RULE-06 | No active Evidence Matrix owner | Reserved | Future reserved |
| RULE-07_DEGRADE_trigger | Enter DEGRADED when selected/current path is invalid | DEGRADE | Verified |
| RULE-08_DEGRADE_keep | Keep degraded fallback path | DEGRADE / KEEP | Verified |
| RULE-09_DEGRADE_switch | Switch to degraded fallback path | DEGRADE / SWITCH | Verified |
| RULE-10_RECOVERY_trigger | Return from DEGRADED to NORMAL when stable trusted path exists | RECOVERY | Verified |
| RULE-11_RECOVERY_cooldown | Suppress immediate post-recovery switching | RECOVERY / KEEP | Verified |
| RULE-12_COOLDOWN_active | Resolver cooldown suppresses repeated escalation | ESCALATE / KEEP guard | Verified |
| RULE-13_RESOLVER_keep | Resolver keeps current path | KEEP / RESOLVER | Verified |
| RULE-14_RESOLVER_switch | Resolver switches to different path | SWITCH / RESOLVER | Verified |
| RULE-15_RECOVERY_CANDIDATE | Register recovered path as candidate | RECOVERY | Verified |
| RULE-16_RECOVERY_VALIDATION_START | Start / continue recovery candidate validation | RECOVERY | Verified |
| RULE-17_RECOVERY_VALIDATION_PASS | Legacy validation-pass marker | RECOVERY | Legacy Concept |
| RULE-18_RETURN_ELIGIBLE | Candidate becomes eligible for return | RECOVERY | Verified |
| RULE-19_RETURN_SWITCH | Verified v0.2 direct return switch | RECOVERY / SWITCH | Verified |
| RULE-20_RETURN_KEEP | Keep current path when return margin is not met | RECOVERY / KEEP | Verified |
| RULE-21_RETURN_RAMP_ADVANCE | Advance recovery ramp under FULL / promoted conditions | RECOVERY / SWITCH | Experimental; operational RULE-21 owner |
| RULE-21_RETURN_ESCALATE | v0.2 return escalation label | ESCALATE | Legacy Concept |
| RULE-22_RETURN_RAMP_HOLD | Hold current ramp weight | RECOVERY / KEEP | Experimental |
| RULE-23_RETURN_RAMP_ABORT | Abort active return ramp attempt | ABORT | Experimental |
| RULE-24_RETURN_RAMP_COMPLETE | Complete progressive reintegration | RECOVERY / SWITCH | Experimental |
| RULE-25_RETURN_RAMP_START | v0.3 progressive ramp entry | RECOVERY / RAMP START | Experimental; outside RULE-01..24 Verified namespace |

## Collision Matrix Scope

The collision matrix is a partial arbitration model, not a complete PSC-wide
rule arbitration engine. Current active collision coverage focuses on:

- core keep/switch/trust/block/escalation rules: `RULE-01` through `RULE-05`
- recovery ramp hold/abort/complete rules: `RULE-22` through `RULE-24`

Many recovery, resolver, and degraded-mode rules from `RULE-07` through
`RULE-21` are active in PSC evidence and logs, but their collision predicates
and priorities are not integrated into the collision matrix yet.

## Unified Flowchart

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
