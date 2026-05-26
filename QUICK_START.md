# PSC Quick Start

This guide is the shortest path to run PSC simulations
and inspect the generated validation logs.

PSC behavior is validated through RULE-to-scenario-to-log traceability.
The goal is not only to run a demo, but to confirm how control decisions are produced.

---

## Prerequisite

All examples assume a Python 3 environment.

---

## 1. Run the RCU Decision v0.1 Simulation

```bash
python3 sim/02_controlled/02_rcu_decision_v01/mini_psc_rcu_decision_v01.py
```

This simulation validates the core RCU Decision Model v0.1:

- trust-aware path selection
- stability-preserving KEEP behavior
- Resolver escalation
- degraded operation
- controlled recovery
- cooldown-based oscillation resistance

---

## 2. Inspect Generated Logs

Generated logs are written under:

`sim/02_controlled/02_rcu_decision_v01/logs/`

| Scenario | Log |
| --- | --- |
| Resolver Stability Conflict + Cooldown | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_stability_conflict_cooldown_rule_log.md` |
| Degraded -> Recovery -> Stabilization | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md` |
| Resolver Switch Decision | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md` |

---

## 3. Compare Behavior with RULE References

Open the Evidence Matrix:

- English: docs/specification/validation/psc_evidence_matrix_v0.1_en.md
- Japanese: docs/specification/validation/psc_evidence_matrix_v0.1_ja.md

Check how each scenario maps to explicit RULE decisions:

| Behavior | RULE examples |
| --- | --- |
| Ambiguous path conflict | `RULE-05_ESCALATE_conflict` |
| Cooldown suppression | `RULE-12_COOLDOWN_active` |
| Degraded fallback | `RULE-09_DEGRADE_switch`, `RULE-08_DEGRADE_keep` |
| Recovery transition | `RULE-10_RECOVERY_trigger`, `RULE-11_RECOVERY_cooldown` |
| Resolver switch | `RULE-14_RESOLVER_switch` |

---

## 4. Run Quick Demos

| Demo | Command | Purpose |
| --- | --- | --- |
| Static Demo | `python3 sim/04_demo/run_psc_demo.py` | Basic trust-aware routing and stable path preference |
| Dynamic Demo | `python3 sim/04_demo/run_psc_dynamic_demo.py` | Adaptive behavior under changing path conditions |

---

## 5. Read the Core Model

After running the simulation, read the model specification:

- English: docs/specification/published/models/psc_rcu_decision_model_v0.1_en.md
- Japanese: docs/specification/published/models/psc_rcu_decision_model_v0.1_ja.md

The important point is PSC's control behavior:
it prioritizes resilient, stable decisions over unstable peak throughput.
