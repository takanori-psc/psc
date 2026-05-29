# Expected Category Helper Spec v0.1

## Purpose

`expected_category` is a lightweight validator layer above RULE string matching.
It checks whether emitted RULE identifiers match the intended control behavior of
a scenario.

The helper does not validate numeric thresholds, ordering, or telemetry values.

## Categories

| Category | Meaning | Minimal RULE family |
|----------|---------|---------------------|
| `switch` | PSC intentionally changes selected path or ramp target | `RULE-02`, `RULE-14`, `RULE-19`, `RULE-21`, `RULE-24` |
| `hold` | PSC keeps the selected path or current ramp weight | `RULE-01`, `RULE-08`, `RULE-11`, `RULE-20`, `RULE-22` |
| `abort` | PSC stops recovery ramp due to unsafe evidence | `RULE-23` |
| `escalation` | PSC delegates ambiguous decision to Resolver | `RULE-05` |
| `escalation_and_cooldown` | Resolver escalation is followed by cooldown protection | `RULE-05` and `RULE-12` |
| `fallback` | PSC enters or uses degraded fallback behavior | `RULE-07` or `RULE-09` |
| `hold_or_escalate` | Ambiguous LIGHT evidence is handled conservatively | `hold` or `escalation` |

## Initial Validator Contract

A `ScenarioCheck` passes when:

1. The command exits successfully.
2. All `expected_rules` strings appear in output.
3. If `expected_category` is set, emitted RULEs satisfy that category.

The helper should stay string-based until LIGHT scenarios produce stable logs.

## Classification For LIGHT Decisions

| LIGHT condition | Expected category | Safety interpretation |
|-----------------|-------------------|-----------------------|
| Required telemetry missing | `hold` | Never advance on incomplete LIGHT evidence |
| Telemetry stale | `hold` | Freshness failure blocks ramp advance |
| Sparse evidence hides risk | `hold_or_escalate` | Conservative behavior is acceptable |
| Severe instability or hard failure | `abort` | Abort overrides observation mode |
| Trust / stability / confidence conflict | `escalation` or `escalation_and_cooldown` | Resolver review is required before advance |

## Non-Goals

- Threshold comparison
- Step ordering
- Exact ramp weight validation
- Telemetry schema validation
- Evidence Matrix promotion
