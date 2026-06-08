# PSC Score and Decision Parameter Model v0.1

## 1. Document Information

- Document Name : PSC Score and Decision Parameter Model
- Version : v0.1
- Project : PSC (Photon System Controller)
- Layer : PSCOS / PSC Fabric
- Document Type : Reference / Parameter Model
- Status : Draft
- Author : T. Hirose
- Created : 2026-06-08
- Last Updated : 2026-06-08
- Language : English

---

## 2. Purpose

This document is a reference model that organizes the PSC score model and decision
parameters so that they can be referenced consistently across implementation,
validation, and specification documents.

This model covers the following items.

- score types
- score meanings
- weighting by decision layer
- low-level observation parameters used for score calculation
- input relationships for each composite score

This document does not change existing `RULE-*` IDs, verified evidence, or simulation logs.

---

## 3. Score Types

| Score | Meaning | Primary inputs | Interpretation when high | Nature |
|-------|---------|----------------|---------------------------|--------|
| `congestion_score` | Congestion score | utilization, buffer, retry, latency, packet loss | Disadvantageous because the path is more congested | Negative factor |
| `performance_score` | Performance score | throughput, low latency | Advantageous because the path has better performance | Positive factor |
| `stability_score` | Stability score | variance, degradation trend, persistent instability | Advantageous because the path is more stable | Positive factor |
| `trust_score` | Trust score | path trust, policy compliance, verification state, observed behavior | Advantageous because the path is safer to select | Positive factor |
| `final_score` | Normal path score | low congestion + performance | A path with a high value becomes a normal candidate | Normal Selection |
| `resolver_score` | Resolver decision score | trust + stability + performance | Used by Resolver to select a safe path | Resolver Selection |
| `return_score` | Return decision score | stability + trust + performance | Used to decide whether a path may return after recovery | Recovery Selection |
| `priority` | RULE priority score | relative strength between RULEs | The higher-priority RULE wins the final decision | RULE collision resolution |

---

## 4. Score Interpretation

### 4.1 Congestion Score

```text
congestion_score =
  effect of utilization
+ effect of buffer pressure
+ effect of retry / retransmission
+ effect of latency
+ effect of packet loss
```

`congestion_score` is disadvantageous when high.
When integrating it into the normal `final_score`, it is inverted as follows.

```text
congestion_benefit = 1 - congestion_score
```

### 4.2 Performance Score

```text
performance_score =
  throughput quality
+ low latency
```

`performance_score` is advantageous when high.

### 4.3 Stability Score

```text
stability_score =
  1 - instability

instability =
  magnitude of variance
+ degradation direction from trend
+ continuation of an unstable state by duration / persistence
```

`stability_score` is calculated from observation history with timestamps, not from a
single instantaneous value.
In implementation, it is evaluated by an Observation-side ring buffer or time window.
Specific window seconds or sample counts are not fixed and are treated as configurable
parameters.

### 4.4 Trust Score

`trust_score` may change not only by static authentication or verification state,
but also by dynamic Trust Events.

Examples of Trust Events:

- authentication failure
- policy violation
- signature mismatch
- abnormal communication
- attack indicators

`trust_score` and `trust_block` are separate concepts.

- `trust_score`
  An evaluation factor used for path preference or penalty.
- `trust_block`
  An exclusion condition caused by falling below the trust threshold, explicit
  Trust Block, or a severe violation.

---

## 5. Composite Score Model

### 5.1 Normal Final Score

The normal `final_score` is the score used for Normal Selection.
Its basic composition is low congestion + performance.

```text
final_score =
  Wc * congestion_benefit +
  Wp * performance_score
```

`stability_score` is not a primary component of the normal `final_score`.
However, it remains an important decision factor in hysteresis, Eligibility,
Resolver, and Recovery.

`cost_score` and `power_score` may be added as future extensions, but they are not
included in the core v0.1 / v0.2 decisions.

### 5.2 Resolver Score

When Resolver is active, `resolver_score` takes priority instead of the normal
`final_score`.

```text
resolver_score =
  Wr_trust * trust_score +
  Wr_stability * stability_score +
  Wr_performance * performance_score
```

The weighting order is as follows.

```text
Trust > Stability > Performance
```

Paths below the trust threshold are excluded before `resolver_score` comparison.

### 5.3 Return Score

For Recovery return, `return_score` is used instead of the normal `final_score`.

```text
return_score =
  Wret_stability * stability_score +
  Wret_trust * trust_score +
  Wret_performance * performance_score
```

The weighting order is as follows.

```text
Stability > Trust > Performance
```

`return_score` is used to decide whether return is allowed and is separate from the
normal-selection `final_score`.

---

## 6. Decision Weight Meaning

| Decision context | Highest priority | Next priority | Checked last |
|------------------|------------------|---------------|--------------|
| Normal operation | low congestion / performance | threshold / hysteresis | Trust Block / escalation |
| Resolver decision | Trust | Stability | Performance |
| Recovery return | Stability | Trust | Performance |

Key points:

- Normal operation:
  paths that are fast and uncongested become candidates.
- Resolver:
  selects a path that is trustworthy and stable rather than simply fast.
- Recovery:
  first prioritizes that the path is stable.

PSC does not simply select the fastest path. It evaluates congestion, performance,
trust, and stability separately, and changes weighting according to state.

---

## 7. Low-Level Observation Parameters

### 7.1 Score Inputs

| Score | Low-level observation parameter | Type |
|-------|---------------------------------|------|
| `congestion_score` | `utilization` | link utilization |
| `congestion_score` | `buffer_pressure` / `buffer` | buffer pressure |
| `congestion_score` | `retry_rate` / `retry` | retransmission / retry |
| `congestion_score` | `latency` | link latency |
| `congestion_score` | `packet_loss` | packet loss |
| `performance_score` | `throughput` / `throughput_estimate` | effective throughput |
| `performance_score` | `latency` / `end_to_end_latency` | end-to-end latency |
| `stability_score` | `variance` | variation in observed values |
| `stability_score` | `trend` | degradation / improvement direction |
| `stability_score` | `duration` | state duration |
| `stability_score` | `persistence` | persistence of unstable state |
| `stability_score` | `timestamp` | time for history evaluation |
| `stability_score` | ring buffer / time window | history retention unit |
| `trust_score` | `CRC/error_rate` | communication error rate |
| `trust_score` | `link_stability` / link flapping | link stability |
| `trust_score` | `thermal_state` | thermal state |
| `trust_score` | `power_stability` | power stability |
| `trust_score` | `firmware_integrity` | firmware tampering status |
| `trust_score` | `hardware_diagnostics` | hardware self-diagnostics |
| `trust_score` | `secure_boot_validation` | secure boot validation |
| `trust_score` | `signature_validation` / `signature_mismatch` | signature validation |
| `trust_score` | `authentication_result` / authentication failure | authentication state |
| `trust_score` | `policy_validation_result` | policy compliance |
| `trust_score` | `abnormal_communication` | abnormal communication |
| `trust_score` | `attack_indicators` | attack indicators |
| `health_score` / Eligibility | `node_health_state` | node health |
| `health_score` / Eligibility | `failure_state` | failure state |
| `health_score` / Eligibility | `processing_load` | node processing load |
| `health_score` / Eligibility | `route_availability` | route availability |
| `health_score` / Eligibility | `telemetry_freshness` / `freshness` | update time |
| `health_score` / Eligibility | `confidence` | observation confidence |
| `health_score` / Eligibility | `source_reliability` | source reliability |

### 7.2 Composite Score Inputs

| Composite Score | Derived scores used | Source low-level observations |
|-----------------|---------------------|-------------------------------|
| `final_score` | `congestion_score`, `performance_score` | utilization, buffer, retry, latency, packet_loss, throughput |
| `resolver_score` | `trust_score`, `stability_score`, `performance_score` | trust-related hardware / verification information, variance, trend, duration, throughput, latency |
| `return_score` | `stability_score`, `trust_score`, `performance_score` | variance, trend, duration, trust-related hardware / verification information, throughput, latency |

---

## 8. PSC Decision Parameters

Decision Parameters are control parameters such as thresholds, windows, and cooldowns
used by the RULE Engine to finalize decisions after score calculation.

They are not scores themselves.
They are boundary conditions that determine how scores are interpreted and which RULE
is activated.

| Parameter | Meaning | Primary purpose | Related layer / RULE |
|-----------|---------|-----------------|----------------------|
| `switch_threshold` / `switch_margin` | switch threshold | Allows switch only when `score_gap` or improvement is sufficiently large | Normal Selection / `RULE-01`, `RULE-02` |
| `trust_threshold` | trust lower bound | Excludes paths below the threshold in Eligibility | Eligibility / `RULE-04`, `RULE-07`, `RULE-09` |
| `trust_switch_threshold` | trust switch threshold | Treats a candidate with sufficiently high trust as a trust-driven switch candidate | Resolver / Trust Switch / `RULE-03` |
| `trust_block_threshold` | Trust Block threshold | Treats trust below the threshold as a block cause. It is separated from explicit `trust_block` as a cause, but the outcome is the same `BLOCK_SWITCH` | Eligibility / `RULE-04` |
| `return_threshold` / `return_margin` | return threshold | Allows return only when improvement of the Recovery candidate is sufficiently large | Recovery Selection / `RULE-19`, `RULE-20` |
| `return_trust_threshold` | return trust lower bound | Trust condition for a Recovery return candidate to become an eligible return candidate | Recovery Selection / `RULE-15`, `RULE-18` |
| `return_stability_threshold` | return stability lower bound | Stability condition for a Recovery return candidate to become an eligible return candidate | Recovery Selection / `RULE-15`, `RULE-18` |
| `resolver_trigger_threshold` / `epsilon` | Resolver trigger threshold | Passes the decision to Resolver when `score_gap` is small and there is a trust / stability conflict | Resolver Selection / `RULE-05` |
| `trust_conflict_threshold` | trust conflict threshold | Treats a large trust difference as a conflict when local decision is difficult | Resolver Selection / `RULE-05`, `RULE-14` |
| `stability_conflict_threshold` | stability conflict threshold | Treats a large stability difference as a conflict when local decision is difficult | Resolver Selection / `RULE-05`, `RULE-14` |
| `stability_window` | stability evaluation window | Observation history range used to evaluate `variance` / `trend` / `duration` | Observation / Stability |
| `persistence_limit` | persistence decision threshold | Allows switch / escalation only for sustained degradation, not transient fluctuation | Hysteresis / `RULE-01`, `RULE-02` |
| `cooldown_steps` | number of cooldown steps | Suppresses repeated switch / repeated escalation | Cooldown / `RULE-11`, `RULE-12` |
| `resolver_cooldown_steps` | number of Resolver cooldown steps | Suppresses re-escalation after Resolver execution | Resolver Cooldown / `RULE-12` |
| `recovery_cooldown_steps` | number of Recovery cooldown steps | Suppresses re-switching immediately after recovery | Recovery Cooldown / `RULE-11` |

### 8.1 Decision Flow

The relationship between PSC score / parameter / rule is organized in the following order.

```text
Observation Parameters
  utilization, latency, retry, trust events, timestamp, confidence, ...

↓

Derived Scores
  congestion_score, performance_score, stability_score, trust_score

↓

Composite Scores
  final_score, resolver_score, return_score

↓

Decision Parameters
  switch_threshold, trust_threshold, return_threshold,
  resolver_trigger_threshold, stability_window, cooldown_steps

↓

RULE Engine
  RULE-01_KEEP_score, RULE-02_SWITCH_score, RULE-04_BLOCK_trust,
  RULE-05_ESCALATE_conflict, RULE-11_RECOVERY_cooldown,
  RULE-12_COOLDOWN_active, ...
```

### 8.2 Parameter Notes

- `switch_threshold` and `switch_margin` are treated as similar switch boundaries
  depending on context.
- `return_threshold` and `return_margin` are treated as boundaries for Recovery return.
- `resolver_trigger_threshold` may appear as `epsilon` in implementation or documents.
- `stability_window` is a configurable parameter, not a fixed number of seconds.
- `cooldown_steps` is a generic name and may be split into `resolver_cooldown_steps`
  and `recovery_cooldown_steps` in implementation.
- explicit `trust_block` and falling below `trust_block_threshold` are separate causes,
  but their outcome can be treated as `BLOCK_SWITCH` by the same `RULE-04_BLOCK_trust`.

---

## 9. Notes

- `policy_validation_result` is not a low-level physical observation.
  However, it is treated as a control observation parameter included in `trust_score`
  and Eligibility.
- `priority` is not a path score. It is a priority used to resolve collisions between
  RULEs.
- The score names in this document are treated as reference names aligned with the
  PSC RCU Decision Model, Telemetry Model, Trust Model, and Recovery Return Model.
