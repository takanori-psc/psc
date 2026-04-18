# PSC Resolver Arbitration Extension Model v0.2.x (EN)

---

## Core Principle

```text
RCU tentative decision ≠ Resolver final decision
```

---

## Interpretation

- The Resolver is invoked not only when the RCU cannot determine a decision,
  but also when the RCU decision is ambiguous or conflicting
- In particular, when the score gap is small while trust or stability differences are significant,
  normal scoring alone is insufficient for final decision making
- In such cases, the Resolver functions as a conflict-arbitration layer

---

## ESCALATE Condition

```text
ESCALATE if:

score_gap < epsilon
AND
(trust_gap > trust_conflict_threshold
 OR
 stability_gap > stability_conflict_threshold)
```

---

## Metric Definitions

```text
score_gap     = |best.final_score - selected.final_score|
trust_gap     = |best.trust - selected.trust|
stability_gap = |stability_score(best) - stability_score(selected)|
```

---

## Design Meaning

- `score_gap` represents how small the difference is under baseline evaluation
- `trust_gap` represents the difference in trust
- `stability_gap` represents the difference in stability
- When the score gap is sufficiently small, trust / stability differences affect the final decision

---

## Resolver Role

- Re-evaluate the RCU tentative decision
- Arbitrate using trust / stability / recovery conditions
- Return the final keep / switch decision

---

## Arbitration Flow

```text
RCU
→ compute best candidate
→ compute score_gap / trust_gap / stability_gap
→ ESCALATE decision
→ Resolver arbitration
→ final decision
```

---

## Status

- Consistent with the v0.2.x Recovery Return model
- Consistent with multi-candidate validation results
- Extends Resolver from “exception handling” to “conflict arbitration”

---

## Next Step

- Integrate into the existing Resolver Model v0.1
- Fix threshold values (epsilon / trust_conflict_threshold / stability_conflict_threshold)
