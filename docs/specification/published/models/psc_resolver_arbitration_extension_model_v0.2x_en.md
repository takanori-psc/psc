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

## Resolver Score Priority

This extension follows the layered decision structure defined in the
PSC RCU Decision Model v0.1.

When Resolver is active, the Resolver must prioritize `resolver_score` rather
than the normal `final_score`.

```text
resolver_score =
  Wr_trust * trust_score +
  Wr_stability * stability_score +
  Wr_performance * performance_score

where Wr_trust > Wr_stability > Wr_performance
```

Paths below the trust threshold, paths blocked by `trust_block`, and paths with
hard policy or verification failures must be excluded before `resolver_score`
comparison.

Resolver active conditions include:

- trust conflict
- stability degradation
- ambiguous score result
- Resolver-related rule activation such as `RULE-05`, `RULE-06`, or `RULE-14`

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
