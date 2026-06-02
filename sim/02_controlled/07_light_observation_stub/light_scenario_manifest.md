# LIGHT Scenario Manifest v0.1

## Status

- Type: scenario design and runnable validation manifest
- Evidence status: partial runnable validation
- Target gate: keep `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` on Hold

## Scenario Set

| Scenario | Stimulus | Expected category | Acceptable RULE evidence | Existing connection |
|----------|----------|-------------------|--------------------------|---------------------|
| light_false_negative | Recovery ramp runs while actual instability is not detected by LIGHT sampling | hold | `RULE-22_RETURN_RAMP_HOLD` | Extends `ramp_light_tolerates_moderate_dip` |
| light_telemetry_gap | Required LIGHT input is missing: trust, stability proxy, freshness, or confidence | hold | `RULE-22_RETURN_RAMP_HOLD` | New LIGHT-only input validation |
| light_stale_telemetry | Telemetry sample exists but exceeds the freshness window | hold | `RULE-22_RETURN_RAMP_HOLD` | New LIGHT-only freshness validation |
| light_masked_instability | Stability proxy appears healthy while hidden instability exists | hold | `RULE-22_RETURN_RAMP_HOLD` | Extends `ramp_light_tolerates_moderate_dip` |
| light_delayed_abort | LIGHT observes severe instability later than FULL but still sees hard failure | abort | `RULE-23_RETURN_RAMP_ABORT` | Extends `ramp_abort_light_hard_failure` |
| light_resolver_escalation | LIGHT evidence cannot distinguish recovery from risk | escalation_and_cooldown | `RULE-05_ESCALATE_conflict` and `RULE-12_COOLDOWN_active` | Extends resolver conflict behavior |

## Minimal Scenario Fields

Each future runnable LIGHT scenario should declare:

| Field | Purpose |
|-------|---------|
| `name` | Stable scenario identifier used by validator and logs |
| `observation_mode` | Must be `LIGHT` for this set |
| `stimulus` | Short description of telemetry perturbation |
| `expected_category` | Behavior intent expected from PSC |
| `expected_rules` | Required RULE identifiers for the current validation depth |
| `source_scenario` | Existing scenario or model being extended |
| `promotion_blocker` | Reason this scenario still blocks LIGHT advance promotion |

## Runnable Validation Records

```text
name=light_false_negative
observation_mode=LIGHT
stimulus=actual path instability exists but LIGHT observation fails to detect it
expected_category=hold
expected_rules=RULE-22_RETURN_RAMP_HOLD
source_scenario=ramp_light_tolerates_moderate_dip
promotion_blocker=false-negative LIGHT observation must not produce LIGHT advance
```

```text
name=light_stale_telemetry
observation_mode=LIGHT
stimulus=telemetry data is outdated and confidence is insufficient
expected_category=hold
expected_rules=RULE-22_RETURN_RAMP_HOLD
source_scenario=recovery_ramp_v03
promotion_blocker=stale telemetry must not produce LIGHT advance
```

```text
name=light_masked_instability
observation_mode=LIGHT
stimulus=stability proxy appears healthy while hidden instability exists
expected_category=hold
expected_rules=RULE-22_RETURN_RAMP_HOLD
source_scenario=ramp_light_tolerates_moderate_dip
promotion_blocker=masked instability must not produce LIGHT advance
```

## Initial Stub Records

```text
name=light_telemetry_gap
observation_mode=LIGHT
stimulus=missing trust or stability proxy during active recovery ramp
expected_category=hold
expected_rules=RULE-22_RETURN_RAMP_HOLD
source_scenario=recovery_ramp_v03
promotion_blocker=missing telemetry must not produce LIGHT advance
```

```text
name=light_delayed_abort
observation_mode=LIGHT
stimulus=severe instability or hard failure appears after sparse LIGHT samples
expected_category=abort
expected_rules=RULE-23_RETURN_RAMP_ABORT
source_scenario=ramp_abort_light_hard_failure
promotion_blocker=hard failure override must stay active in LIGHT
```

```text
name=light_resolver_escalation
observation_mode=LIGHT
stimulus=trust and stability proxy disagree during ramp decision
expected_category=escalation_and_cooldown
expected_rules=RULE-05_ESCALATE_conflict,RULE-12_COOLDOWN_active
source_scenario=resolver_switch
promotion_blocker=ambiguous LIGHT evidence must be reviewable by Resolver
```
