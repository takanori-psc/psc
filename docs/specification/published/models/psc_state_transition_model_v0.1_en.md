# PSC State Transition Model v0.1

## Document Information

- Document Name : PSC State Transition Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSCOS (Control Layer)
- Document Type : Specification
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-04
- Last Updated  : 2026-04
- Language      : English

---

## Overview

This document defines the state transition model of PSC (Photon System Controller).
The model is designed to ensure system stability, handle abnormal conditions, and enable safe recovery.

State transitions are executed based on fixed rules, prioritizing stability and preventing ambiguous decisions and unnecessary switching.

---

## State Definitions

### CALM

The system operates in a stable normal condition.
Optimal routing and control are maintained, and external fluctuations have minimal impact.

- Stability: High
- Variability: Low
- Resolver Involvement: None

---

### WARM

Minor fluctuations or increased load are detected.
The system maintains stability while monitoring and evaluating conditions.

- Stability: Medium to High
- Variability: Medium
- Resolver Involvement: Minimal or none

---

### HOT

Conflicts, ambiguity, or trust degradation occur.
Cases that cannot be resolved by standard RCU decision-making increase.

- Stability: Low to Medium
- Variability: High
- Resolver Involvement: Conditional (triggered by conflict or ambiguity)

---

### EMERGENCY

A critical failure or abnormal condition prevents normal control.
The system operates in a constrained mode with minimal functionality preserved, and control decisions are restricted.

- Stability: Very Low
- Variability: Undefined
- Resolver Involvement: Limited or bypassed

---

## Transition Rules

### CALM → WARM

Transition occurs when minor load increase or fluctuation is detected.

---

### WARM → HOT

Transition occurs when conflict, ambiguity, or trust degradation exceeds defined thresholds.

---

### HOT → EMERGENCY

Transition occurs when a critical failure or uncontrollable condition is detected.

---

### EMERGENCY → HOT

Transition occurs when minimum control conditions are restored.

---

### HOT → WARM

Transition occurs when conflicts and ambiguity are resolved and stability improves.

---

### WARM → CALM

Transition occurs when the system stabilizes sufficiently and fluctuations are resolved.

---

## Recovery Procedure

Recovery is performed in a gradual and state-aware manner to prevent oscillation.

1. Minimum control conditions are satisfied
2. Transition from EMERGENCY to HOT
3. Evaluation is performed in HOT state
4. Transition from HOT to WARM
5. Transition from WARM to CALM

---

## Resolver Involvement

Resolver is not tied to a specific state but is dynamically involved based on system conditions.

- CALM / WARM: No or minimal involvement
- HOT: Conditional activation (driven by conflict or ambiguity)
- EMERGENCY: Involvement is limited or bypassed

---

## Design Principles

1. State transitions are based on explicit conditions
2. Unnecessary switching is suppressed
3. The system prioritizes safe behavior under abnormal conditions
4. Recovery is performed gradually
5. All decisions are traceable

---
