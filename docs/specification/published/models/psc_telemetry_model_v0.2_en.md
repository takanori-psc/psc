# PSC Telemetry Model v0.2 (English Version)

## 1. Document Information

- Document Name   : PSC Telemetry Model
- Version         : v0.2
- Project         : PSC (Photon System Controller)
- Layer           : PSCOS / PSC Fabric
- Document Type   : Specification / Model
- Status          : Draft (Design Finalization Candidate)
- Author          : T. Hirose
- Created         : 2026-04-02
- Last Updated    : 2026-04-02
- Language        : English

---

## 2. Objective

This model defines the structure of telemetry data used by the RCU (Routing Control Unit) and Resolver for decision-making.

The design policy of this model is as follows.

- Telemetry is not truth but an observed result
- Observed data includes uncertainty
- The RCU makes decisions with uncertainty taken into account

---

## 3. Design Principles

### 3.1 Telemetry = Evidence

Telemetry is not truth.
The RCU treats telemetry as evidence and applies weighting according to confidence.

### 3.2 Clarification of Granularity

All metrics have the following two axes.

- Temporal Resolution
- Spatial Scope

### 3.3 Adaptive Sampling

Observation frequency is not fixed.
It changes dynamically according to system state.

---

## 4. Telemetry Granularity

### 4.1 Temporal Resolution

Each metric has a Base Interval, and the observation frequency changes according to system state.

#### Link Metrics

- Base Interval: 10ms
- Under high load: 1 to 5ms
- In stable state: 50ms

#### Node Metrics

- Base Interval: 100ms
- In degraded state: 50ms

#### Path Metrics

- Base Interval: 200ms
- In unstable state: 50 to 100ms

### 4.2 Adaptive Sampling Rules

Observation frequency is increased under the following conditions.

- Packet loss increase
- Sudden latency change
- Retry increase
- Heartbeat loss
- Confidence decrease

If the stable state continues for a certain period, the interval returns to the base cycle.

### 4.3 Spatial Scope

| Type         | Unit            |
| :----------- | :-------------- |
| Link Metrics | Per-Link        |
| Node Metrics | Per-Node        |
| Path Metrics | Per-Path        |
| Aggregated   | Aggregated Unit |

---

## 5. Data Quality Attributes

All telemetry data has the following attributes.

- value (observed value)
- confidence
- freshness (update time)
- source_reliability

### 5.1 confidence

Confidence is composed of the following elements.

```text
confidence =
  measurement_quality ×
  sampling_density ×
  consistency ×
  source_factor
```

#### Element Definitions

- measurement_quality
  Measurement accuracy and abnormality status

- sampling_density
  Sample density

- consistency
  Time-series consistency

- source_factor
  Reliability of the information source

### 5.2 source_reliability

| Type     | Reference Range |
| :------- | :-------------- |
| hardware | 0.9 to 1.0      |
| software | 0.6 to 0.85     |
| derived  | 0.3 to 0.7      |

### 5.3 freshness

Freshness is the update time.
The RCU evaluates it by the difference from the current time (Age).

---

## 6. Telemetry Definitions

### 6.1 Link Metrics

- utilization
- latency
- retry_rate
- packet_loss
- buffer_pressure

### 6.2 Node Metrics

- node_health_state
- processing_load
- failure_state

### 6.3 Path Metrics

- end_to_end_latency
- stability
- throughput_estimate

---

## 7. Derived Scores

### 7.1 Congestion Score

Represents the load condition of a link.

### 7.2 Health Score

Represents the state of a node.

### 7.3 Stability Score

Represents variability.

---

## 8. Decay / Aging

### 8.1 Basic Policy

Old data is not discarded immediately.
Its weight is reduced according to elapsed time.

### 8.2 Decay Model

```text
weight = confidence × exp(-λ × Age)
```

### 8.3 Minimum Retention

A minimum weight is retained for a short period.

### 8.4 Expiration Conditions

The data is invalidated only under the following conditions.

- No update for a long period
- Information source abnormality
- Policy violation

---

## 9. RCU Input Interface

### 9.1 Input Structure

```text
metric_name
scope_id
raw_value
normalized_value
confidence
timestamp
source
trend
variance
sample_count
```

### 9.2 Usage Rules

- raw_value is used for recording
- normalized_value is used for evaluation
- trend is used for direction judgment
- variance is used for stability evaluation

---

## 10. Conclusion

This model provides the following.

- Decision-making with uncertainty taken into account
- Fast response to state changes
- Noise-tolerant control

---

## 11. Next Steps

- Design of the RCU evaluation function
- Specification of degraded control
- Resolver trigger conditions
