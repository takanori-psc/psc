# PSC State Transition Diagram

この state model は local RCU mode、Resolver cooldown、v0.2 recovery return、
v0.3 recovery ramp、LIGHT boundary behavior、post-abort handling を統合する。

```mermaid
stateDiagram-v2
    [*] --> NORMAL

    NORMAL --> NORMAL: RULE-01_KEEP_score / keep
    NORMAL --> NORMAL: RULE-02_SWITCH_score / local switch
    NORMAL --> NORMAL: RULE-04_BLOCK_trust / block unsafe switch
    NORMAL --> RESOLVER_REVIEW: RULE-05_ESCALATE_conflict
    NORMAL --> DEGRADED: RULE-07_DEGRADE_trigger

    RESOLVER_REVIEW --> NORMAL: RULE-13_RESOLVER_keep
    RESOLVER_REVIEW --> NORMAL: RULE-14_RESOLVER_switch
    NORMAL --> RESOLVER_COOLDOWN: Resolver executed
    RESOLVER_COOLDOWN --> NORMAL: RULE-12_COOLDOWN_active expires

    DEGRADED --> DEGRADED: RULE-08_DEGRADE_keep
    DEGRADED --> DEGRADED: RULE-09_DEGRADE_switch
    DEGRADED --> NORMAL: RULE-10_RECOVERY_trigger
    NORMAL --> RECOVERY_COOLDOWN: RULE-11_RECOVERY_cooldown set
    RECOVERY_COOLDOWN --> NORMAL: cooldown expires

    DEGRADED --> RECOVERY_CANDIDATE: RULE-15_RECOVERY_CANDIDATE
    RECOVERY_CANDIDATE --> VALIDATING: RULE-16_RECOVERY_VALIDATION_START
    VALIDATING --> RETURN_ELIGIBLE: RULE-18_RETURN_ELIGIBLE / reason=VALIDATION_PASSED
    VALIDATING --> RECOVERY_CANDIDATE: validation fails or candidate changes
    VALIDATING --> VALIDATION_PASS_LEGACY: RULE-17_RECOVERY_VALIDATION_PASS / Legacy Concept
    VALIDATION_PASS_LEGACY --> RETURN_ELIGIBLE: legacy conceptual path only

    RETURN_ELIGIBLE --> NORMAL: RULE-20_RETURN_KEEP
    RETURN_ELIGIBLE --> NORMAL: RULE-19_RETURN_SWITCH / Verified v0.2 direct return
    RETURN_ELIGIBLE --> RETURN_RAMP: RULE-25_RETURN_RAMP_START / Experimental v0.3 ramp entry

    RETURN_RAMP --> RETURN_RAMP: RULE-22_RETURN_RAMP_HOLD
    RETURN_RAMP --> RETURN_RAMP: RULE-21_RETURN_RAMP_ADVANCE / FULL or promoted evidence
    RETURN_RAMP --> NORMAL: RULE-24_RETURN_RAMP_COMPLETE
    RETURN_RAMP --> ABORT_STABILIZATION: RULE-23_RETURN_RAMP_ABORT

    ABORT_STABILIZATION --> RESOLVER_REVIEW: SOFT_ABORT or HARD_ABORT re-evaluation
    ABORT_STABILIZATION --> DEGRADED: EMERGENCY_CUT or no safe allocation
    ABORT_STABILIZATION --> RETURN_RAMP: restart through versioned ramp-start rule

    NORMAL --> LIGHT_BOUNDARY: LIGHT observation
    DEGRADED --> LIGHT_BOUNDARY: LIGHT observation
    RETURN_RAMP --> LIGHT_BOUNDARY: LIGHT ramp observation
    LIGHT_BOUNDARY --> RETURN_RAMP: RULE-22_RETURN_RAMP_HOLD / current policy
    LIGHT_BOUNDARY --> ABORT_STABILIZATION: RULE-23_RETURN_RAMP_ABORT
    LIGHT_BOUNDARY --> RESOLVER_REVIEW: RULE-05_ESCALATE_conflict
    LIGHT_BOUNDARY --> RETURN_RAMP: promotion to FULL or explicit LIGHT gates
```

## State Notes

| State | Current repository owner | Notes |
|-------|--------------------------|-------|
| NORMAL | RCU decision simulations | default local scoring/keep/switch mode。 |
| DEGRADED | RCU decision simulations | trusted valid path がない、または selected path が reject された場合に入る。 |
| RESOLVER_REVIEW | Resolver arbitration simulations | ambiguity 時に呼ばれ、keep または switch を返す。 |
| RESOLVER_COOLDOWN | RCU simulations | Resolver escalation の連続発火を抑制する。 |
| RECOVERY_COOLDOWN | RCU simulations | recovery 直後の switch を抑制する。 |
| RECOVERY_CANDIDATE | Recovery return v0.2 | recovered path は即時再利用されず candidate になる。 |
| VALIDATING | Recovery return v0.2 | validation window で candidate を観測する。 |
| VALIDATION_PASS_LEGACY | Published recovery return v0.2 history | Legacy Concept。現在の code は `RULE-16` 直後に `RULE-18` を emit する。 |
| RETURN_ELIGIBLE | Recovery return v0.2 | candidate は競合可能になるが、selection は強制しない。 |
| RETURN_RAMP | v0.3 recovery ramp | Experimental。`RULE-25` で開始し、`RULE-21` through `RULE-24` を使う。 |
| LIGHT_BOUNDARY | Fast Mode LIGHT draft + stubs | 現在方針は、FULL promotion または explicit gates まで `RULE-22` Hold。 |
| ABORT_STABILIZATION | Abort handling draft + scenarios | post-abort stabilization 後に Resolver re-evaluation または emergency transition。 |
