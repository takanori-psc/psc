# PSC Control Flow Review Findings

This review uses the current repository state as authoritative. It covers the
published/draft specifications, Evidence Matrix, validation logs, controlled
simulation code, and the current rule consistency cleanup. Published
specifications and simulation code were not modified by this review artifact.

## Updated Findings

- Published RCU Decision Model processing stages now use `STEP-*` labels rather
  than local operational `RULE-*` labels. Operational `RULE-*` ownership is
  defined by the Evidence Matrix / validation namespace.
- `RULE-04_BLOCK_trust` is now covered as an Active / Verified safety block
  rule. It has precedence over `RULE-02_SWITCH_score` and
  `RULE-03_SWITCH_trust`, and resolves to `BLOCK_SWITCH`.
- `RULE-17_RECOVERY_VALIDATION_PASS` is a Legacy Concept. Current operational
  behavior transitions from `RULE-16_RECOVERY_VALIDATION_START` directly to
  `RULE-18_RETURN_ELIGIBLE` with `reason="VALIDATION_PASSED"`.
- `RULE-21_RETURN_ESCALATE` is a Legacy Concept. Operational `RULE-21`
  ownership is unified under `RULE-21_RETURN_RAMP_ADVANCE`.
- `RULE-19_RETURN_SWITCH` remains the Verified v0.2 direct return rule.
  `RULE-25_RETURN_RAMP_START` is the experimental v0.3 ramp-entry candidate and
  is not semantically identical to `RULE-19`.
- LIGHT observation policy is authoritative as Hold: LIGHT must emit or resolve
  to `RULE-22_RETURN_RAMP_HOLD` unless promoted to FULL or explicit LIGHT
  promotion gates are defined and satisfied.
- Historical v0.3 LIGHT advance logs, including
  `ramp_light_tolerates_moderate_dip`, should be treated as historical
  experimental behavior rather than current LIGHT policy.

## Remaining Limitations

- The collision matrix is a partial arbitration model, not a complete PSC-wide
  rule arbitration engine. It currently covers core keep/switch/trust/block/
  escalation rules and recovery ramp hold/abort/complete rules.
- `RULE-06..21` are not fully integrated into collision arbitration. Several are
  active PSC degraded/resolver/recovery rules, but their collision predicates and
  priorities remain future work.
- `RULE-03_SWITCH_trust` is active in the collision matrix namespace but is not
  yet promoted as Verified Evidence Matrix coverage because there is no dedicated
  scenario where it is the sole final switch action.
- `RULE-25_RETURN_RAMP_START` remains outside the `RULE-01..24` verified
  namespace until formal v0.3 integration. It should not be promoted to
  Verified or merged into `RULE-19` without a dedicated integration decision.
- Abort handling emits `RULE-23_RETURN_RAMP_ABORT`, but post-abort outcomes are
  still represented mostly as scenario categories rather than first-class
  operational rules.
- Scoring, filtering, resolver, degraded, recovery, and LIGHT helper logic is
  duplicated across controlled simulation scripts.

## Operational Importance

- The highest-impact namespace risks are now controlled by explicit ownership:
  `STEP-*` for published model stages, Evidence Matrix `RULE-*` for operational
  rules, Legacy Concept labels for obsolete rule meanings, and Experimental
  labels for v0.3 candidates.
- The remaining risk is behavioral drift: executable historical scenarios can
  still demonstrate LIGHT advance and experimental ramp start behavior even
  where current documentation treats those behaviors as Hold or candidate-only.
- Collision-matrix conclusions should be read as local arbitration conclusions,
  not as complete PSC-wide precedence guarantees.

## Recommendations

- Keep the Evidence Matrix / validation namespace as the authoritative
  operational rule registry.
- Add a dedicated `RULE-03_SWITCH_trust` final-action validation scenario before
  promoting it to Verified coverage.
- Treat `RULE-25_RETURN_RAMP_START` as experimental until v0.3 integration adds
  formal traceability, validation coverage, and an explicit relationship to
  `RULE-19_RETURN_SWITCH`.
- If current LIGHT policy must be enforced at runtime, update the executable
  v0.3 LIGHT/ramp scenarios so LIGHT cannot advance without FULL promotion or
  explicit LIGHT promotion gates.
- Expand the collision matrix only by adding real predicates and traceable
  priorities for degraded/resolver/recovery rules; do not use bare placeholders
  as operational definitions.
- Consider extracting duplicated simulation helpers into a shared support module
  after the rule namespace stabilizes.
