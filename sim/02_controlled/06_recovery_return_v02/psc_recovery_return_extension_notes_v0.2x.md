# PSC Recovery Return Extension Notes (v0.2.x Draft)

## Core Principle

```text
RETURN_ELIGIBLE ≠ RETURN_SWITCH
RETURN_SWITCH ≠ FINAL_DECISION
```

## Interpretation

- `RETURN_ELIGIBLE` means a recovery candidate has passed validation.
- It does not guarantee immediate switching.
- A return candidate may still conflict with the path preferred by baseline scoring.
- In such cases, final arbitration is delegated to Resolver.

## Recovery Flow

```text
RCU
→ candidate generation by return_score
→ validation
→ RETURN_ELIGIBLE
→ ambiguity check
→ Resolver arbitration (if needed)
→ final switch / keep
→ cooldown / stabilization
```

## Validated Behavior

### Single-candidate case

- `return_score` selects B
- direct return occurs without conflict

### Multi-candidate case

- `return_score` selects C
- `final_score` prefers B
- Resolver resolves the conflict and selects C

## Design Meaning

- `return_score` is a recovery-oriented selector
- `final_score` is a baseline path evaluator
- Resolver is a conflict arbiter, not a default selector

## Status

- v0.2 recovery return: validated
- multi-candidate extension: validated
- Resolver interaction: validated

## Next Step

- formalize as v0.2.x recovery extension model
