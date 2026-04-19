# RCU Decision v0.2 Multi-Candidate Validation Log

## Scenario

- Recovery phase includes multiple candidates (B, C)
- Path B: high performance, moderate instability
- Path C: lower performance, high stability
- Both paths satisfy recovery eligibility conditions

---

## Key Observation

### 1. Candidate Selection

- `return_score` selects **C**
- C shows higher stability despite lower performance

---

### 2. Score Divergence

- `final_score` prefers **B**
- `return_score` prefers **C**

→ Confirms:

```
return_score ≠ final_score
```

---

### 3. Conflict Condition

- Score gap between selected and best is small (~0.05)
- Trust/stability difference triggers escalation

---

### 4. Resolver Behavior

- Resolver is activated due to conflict
- Final decision switches from **A → C**

```
RCU (candidate) → Resolver (arbitration) → final decision
```

---

## Additional Observation

Two recovery behaviors were observed:

1. **Single-candidate case (B only)**

   - `return_score` selects B
   - Direct return occurs without conflict

2. **Multi-candidate case (B vs C)**

   - `return_score` selects C
   - `final_score` prefers B
   - Resolver resolves conflict and selects C

---

## Result

- Recovery candidate ≠ final decision confirmed
- Multi-candidate evaluation works correctly
- Resolver arbitration layer is validated
- Stability-first behavior is maintained after switching

---

## Conclusion

### Core Design Validation

- `return_score` acts as **candidate generator**
- `final_score` acts as **baseline evaluation**
- `Resolver` acts as **conflict arbiter**

---

### Architectural Insight

```
RCU → Candidate Selection (return_score)
Resolver → Conflict Resolution
RCU → Stabilization (hysteresis / cooldown)
```

---

## Notes

- Return eligibility does not guarantee switching
- Decision is deferred under ambiguity
- System prioritizes stability over immediate performance gain

---

## Status

- Multi-candidate recovery: ✔ validated
- Score separation: ✔ validated
- Resolver integration: ✔ validated
- Ready for v0.2.x specification expansion
