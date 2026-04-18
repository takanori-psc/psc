# PSC Recovery Return Extension Model v0.2.x (EN)

---

## Core Principle

```text
RETURN_ELIGIBLE ≠ RETURN_SWITCH
RETURN_SWITCH ≠ FINAL_DECISION
```

---

## Interpretation

- `RETURN_ELIGIBLE` means that a recovery candidate has passed validation
- It does not guarantee an immediate path switch
- A recovery candidate may conflict with the baseline evaluation (`final_score`)
- When such conflicts occur, the final decision is delegated to the Resolver
- The Resolver is invoked not only when RCU cannot decide, but also when:

  - the RCU decision is ambiguous
  - or multiple evaluation criteria are in conflict

---

## Recovery Flow

```text
RCU
→ candidate generation by return_score
→ validation
→ RETURN_ELIGIBLE
→ ambiguity check (score gap / trust gap / stability gap)
→ Resolver arbitration (if needed)
→ final decision (switch / keep)
→ stabilization (cooldown / hysteresis)
```

---

## Validated Behavior

### Single-candidate Case

- `return_score` selects B
- No conflict occurs
- Direct return is executed

---

### Multi-candidate Case

- `return_score` selects C (stability-oriented)
- `final_score` prefers B (performance-oriented)
- Resolver resolves the conflict and selects C

---

## Design Meaning

- `return_score` is a **recovery-oriented selector**
- `final_score` is a **baseline path evaluator**
- Resolver is a **conflict arbitration layer**, not a default selector

---

## Core Design Insight

```text
Recovery eligibility and final decision are separated
```

- “Can return” and “should return” are different decisions
- PSC prioritizes stability over immediate optimization

---

## Status

- v0.2 Recovery Return: validated
- Multi-candidate extension: validated
- Resolver interaction: validated

---

## References

- Validation log:

  - logs/rcu_decision_v02_multi_candidate_validation_log.md
- Raw log:

  - logs/raw/multi_candidate_run.txt

---

## Next Step

- Formalize as v0.2.x recovery extension model
- Define Resolver evaluation rules (trust / stability / score gap)
