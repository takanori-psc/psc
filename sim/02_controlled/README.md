# PSC Controlled Simulation

PSC prioritizes stability over immediate performance recovery.

This directory contains controlled PSC simulation experiments,
representing the evolution of routing control logic and decision models.

---

## Structure Overview

### 01_advanced_series
Early advanced simulations (v08d–v13b) exploring:

- policy-aware routing
- trust-aware routing
- Resolver intervention
- degraded mode behavior

These experiments represent the transition from basic routing
to structured control-plane logic.

---

### 02_rcu_decision_v01
Implementation of the PSC RCU Decision Model v0.1.

Includes:

- core decision logic
- resolver escalation behavior
- stability / trust-based decision rules

---

### 03_oscillation
Validation of oscillation behavior.

- Comparison with ECMP
- Demonstrates PSC stability via hysteresis and resolver control

---

### 04_degraded
Validation of degraded path handling.

- Trust / health-based rejection
- Safe fallback behavior
- Rule validation logs

---

### 05_recovery_hold
Validation of conservative recovery behavior (v0.1).

- PSC does not immediately return to recovered paths
- Stability-first design is preserved

---

### 06_recovery_return_v02
Next-generation recovery model (v0.2).

- Staged re-entry of recovered paths
- Validation before return
- Controlled recovery switching

---

## Evolution Flow

```
basic routing (01_basic)
→ advanced control experiments (01_advanced_series)
→ RCU Decision Model v0.1
→ scenario validation (oscillation / degraded / recovery)
→ recovery return extension (v0.2)
```

---

## Usage

Run a simulation file directly, for example:

```bash
python3 sim/02_controlled/03_oscillation/mini_psc_rcu_decision_v01_oscillation.py
```

---

## Notes

- Each directory represents a specific stage in PSC evolution.
- Logs are stored alongside simulations for traceability.
- English logs are primary; Japanese logs provide design context.
