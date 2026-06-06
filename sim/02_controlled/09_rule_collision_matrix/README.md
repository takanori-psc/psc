# PSC Rule Collision Matrix

## Purpose

This directory contains a minimal simulator for checking how PSC rules collide
when more than one rule is triggered in the same step.

The runner evaluates every registered rule for each scenario step, records all
triggered rules, and resolves the final action by priority. This makes priority
behavior visible instead of hiding it inside one large decision branch.

## Flow

1. Load a JSON scenario.
2. Evaluate all registered rules for each step.
3. Each triggered rule returns:
   - `rule_id`
   - `action`
   - `priority`
   - `reason`
4. Resolve collisions by highest priority.
5. Print triggered rules, suppressed rules, final action, expected action, and
   `PASS` or `FAIL`.

Ties are resolved by rule registry order so output is deterministic.

## Registered Rules

- `RULE-02_SWITCH_score`
- `RULE-05_ESCALATE_conflict`
- `RULE-22_RETURN_RAMP_HOLD`
- `RULE-23_RETURN_RAMP_ABORT`
- `RULE-24_RETURN_RAMP_COMPLETE`

## Scenario Format

Scenarios are JSON-first to avoid YAML dependencies.

```json
{
  "name": "return_vs_abort",
  "description": "Return Ramp hold collides with an abort condition.",
  "steps": [
    {
      "step_id": 0,
      "state": {},
      "telemetry": {},
      "expected_action": "RETURN_RAMP_ABORT"
    }
  ]
}
```

## Run

```bash
python3 sim/02_controlled/09_rule_collision_matrix/run_scenario.py \
  sim/02_controlled/09_rule_collision_matrix/scenarios/return_vs_abort.json
```

Compile check:

```bash
python3 -m py_compile sim/02_controlled/09_rule_collision_matrix/run_scenario.py
```
