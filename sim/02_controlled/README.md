# 01_advanced

Advanced PSC simulation experiments.

## Contents

- `mini_psc_v08d.py`: policy-aware routing simulation
- `mini_psc_v09.py`: Resolver intervention experiment
- `mini_psc_v09a.py`: structured logging refinement
- `mini_psc_v10.py`: trust-aware routing experiment
- `mini_psc_v10a.py`: trust fallback behavior experiment
- `mini_psc_v11.py`: degraded-mode fallback experiment
- `rcu_decision/`: simulations for the RCU Decision Model (v0.1 and later)
- `mini_psc_advanced_experiment_log.md`: experiment notes and results

## Purpose

This directory contains advanced PSC simulation experiments focused on routing behavior under policy, trust, Resolver-guided conditions,
and the RCU decision model.

## Notes

These experiments extend the basic simulation series with more advanced routing logic, including:

- policy-aware routing
- trust-aware routing
- Resolver intervention
- degraded fallback behavior
- RCU decision logic

## Usage

Run a simulation file directly, for example:

```bash
python3 sim/02_controlled/01_advanced/mini_psc_v11.py
```
