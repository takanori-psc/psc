# PSC Fast Mode Flow Buffer Model v0.1

## 1. Document Information

- Document Name : PSC Fast Mode Flow Buffer Model
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Fast Mode / Flow Buffer
- Document Type : Design Draft
- Status : Draft
- Language : English

- Related Models:
  - PSC Fast Mode Bundle Capacity Control v0.1
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC Recovery Return Abort Handling v0.1
  - PSC Telemetry Model v0.2

---

## 2. Purpose

This draft defines the conceptual role of the Flow Buffer in Fast Mode, the
responsibility separation between PSC and the Flow Buffer implementation, and
the operational model used to keep Fast Mode stable.

The primary purpose of the Flow Buffer is stable Fast Mode operation. In Fast
Mode, short-term transfer variance on optical links, small arrival skew across
lanes, and GPU-side DMA or processing timing variance may occur. The Flow Buffer
absorbs these short-term variations and acts as an adjustment area that helps
maintain continuous Basket Stream transfer.

The Flow Buffer should be separated from the PSC core. PSC acts as the control
plane and performs state monitoring, trend tracking, policy judgment, and
Pause / Abort decisions. In contrast, FIFO management, memory management, DMA
control, and GPU-facing transfer are data movement responsibilities and should
not be tightly coupled to the main PSC control logic.

This separation allows PSC to make stability decisions based on state
information without depending on the internal Flow Buffer implementation.

---

## 3. Scope

This draft covers:

- the basic role of the Flow Buffer in Fast Mode
- why the Flow Buffer is separated from the PSC core
- responsibility separation between PSC and Flow Buffer Manager
- Flow Buffer hardware independence
- Flow Buffer monitoring model
- exception handling related to Flow Buffer state
- Flow Buffer state logging policy

This draft does not define:

- concrete Flow Buffer capacity values
- production thresholds
- implementation methods for each memory type
- DMA engine details
- GPU-side queueing algorithms
- simulation implementation
- Evidence Matrix entries

---

## 4. Fast Mode Basic Principle

Fast Mode uses the following basic transition:

```text
START
↓
STREAM
↓
COMPLETE
```

Fast Mode operates over a pre-established trusted channel. During normal
operation, PSC does not need to continuously intervene while the Basket Stream
is being transferred.

The basic Fast Mode behavior is:

- use a pre-established channel
- continuously transfer the Basket Stream after START
- avoid requiring PSC per-basket intervention during normal operation
- terminate the transfer unit with COMPLETE

PSC should focus on state monitoring and exception decisions rather than
continuously intervening in the normal Fast Mode transfer path.

---

## 5. Flow Buffer Concept

The Flow Buffer is a buffering component that absorbs short-term flow variance
in the Fast Mode transfer path.

The Flow Buffer is intended to:

- absorb instantaneous transfer variance
- absorb GPU-side processing delay
- stabilize Fast Mode

The Flow Buffer functions as an adjustment reservoir or smoothing buffer. When
there is a short-term difference between the arriving Basket Stream rate from
the source side and the rate that the GPU side or device side can actually
consume, the Flow Buffer temporarily absorbs the difference.

In normal state, the Flow Buffer should remain close to empty. If the Flow
Buffer continuously maintains high occupancy, that may indicate more than
transient variance. It may be a sign of capacity mismatch, GPU-side processing
delay, DMA congestion, or link / trust degradation.

The Flow Buffer is not a storage area for permanently increasing throughput. In
stable Fast Mode operation, the Flow Buffer is treated as a safety component
that absorbs short-term jitter.

---

## 6. Responsibility Separation

PSC and Flow Buffer Manager must have clearly separated responsibilities.

### 6.1 PSC Responsibilities

PSC monitors Flow Buffer state from the control plane and makes the required
decisions.

PSC responsibilities are:

- occupancy monitoring
- trend monitoring
- alert judgment
- Pause / Abort judgment

PSC does not manage internal Flow Buffer processing. PSC does not directly
control FIFO pointers, memory allocation, DMA descriptors, or GPU-facing
transfer ordering.

### 6.2 Flow Buffer Manager Responsibilities

Flow Buffer Manager manages the actual data handling of the Flow Buffer.

Flow Buffer Manager responsibilities are:

- FIFO management
- memory management
- DMA control
- GPU-facing transfer

Flow Buffer Manager provides PSC with the state information required for
monitoring. However, control decisions such as Fast Mode Pause, Rate Down, or
Abort belong to PSC.

---

## 7. Hardware Independence

The Flow Buffer is defined as a conceptual component that does not depend on a
specific memory technology.

The Flow Buffer may be implemented with:

- DDR5
- DDR6
- HBM
- MRAM
- future Optical Memory

PSC must not make decisions based on assumptions about the internal Flow Buffer
memory technology. PSC monitors state information provided by Flow Buffer
Manager.

Therefore, PSC control logic should use hardware-independent information such
as:

- current occupancy
- occupancy trend
- fill / drain behavior
- health state
- alert state

Memory technology specific latency, retention, wear, bandwidth, and thermal
behavior are absorbed by Flow Buffer Manager or a lower implementation layer.

---

## 8. Monitoring Model

PSC monitors the operational state of the Flow Buffer, not its internal
processing.

Examples of Flow Buffer monitoring metrics are:

| Metric | Meaning |
|--------|---------|
| Current Occupancy | Current Flow Buffer usage |
| Peak Occupancy | Maximum usage within the observation window |
| Fill Rate | Rate entering the Flow Buffer from the source side |
| Drain Rate | Rate leaving the Flow Buffer toward the GPU / device side |
| Health State | Health reported by Flow Buffer Manager |

PSC uses these states to determine whether the Flow Buffer is absorbing
temporary variance or approaching a sustained capacity mismatch.

The following trends are especially relevant to PSC:

- Current Occupancy continuously increases
- Peak Occupancy repeatedly reaches a high level
- Fill Rate remains above Drain Rate for an extended period
- Health State indicates degraded or unstable

This draft does not define concrete thresholds.

---

## 9. Exception Handling

When Flow Buffer or surrounding state becomes unsafe, PSC determines whether
Fast Mode can continue.

Example exception conditions are:

- Buffer Critical
- Hardware Failure
- Link Failure
- Trust Degradation

PSC may perform the following actions as needed:

```text
PAUSE
RATE DOWN
ABORT
```

### 9.1 PAUSE

PAUSE is used to temporarily stop Fast Mode transfer and provide time for Flow
Buffer drain, state observation, or Resolver / policy review.

### 9.2 RATE DOWN

RATE DOWN is used to reduce source-side offered traffic and suppress Flow
Buffer occupancy growth.

RATE DOWN is useful when the Flow Buffer has not yet reached critical failure
but trend and health state indicate an operational stability risk.

### 9.3 ABORT

ABORT is used when continuing Fast Mode is unsafe.

Examples:

- Flow Buffer reaches critical state
- hardware failure prevents Flow Buffer reliability from being maintained
- link failure breaks Basket Stream continuity
- trust degradation prevents the Fast Mode boundary from being maintained

Post-abort recovery or fallback details are delegated to the Recovery Return
and Abort Handling models.

---

## 10. Logging

Flow Buffer state is subject to logging.

Examples of Flow Buffer state are:

```text
NORMAL
ELEVATED
HIGH
CRITICAL
```

Logs should preferably include at least:

- timestamp
- Flow Buffer state
- current occupancy
- peak occupancy
- fill rate
- drain rate
- health state
- PSC action

Flow Buffer logs are used for facility improvement and capacity design. In
particular, Peak Occupancy, Fill Rate, Drain Rate, RATE DOWN frequency, and
PAUSE / ABORT conditions become future capacity planning and simulation input.

---

## 11. Future Work

This draft does not define fixed values for Flow Buffer State Thresholds.

Flow Buffer thresholds, state transitions, capacity margin, RATE DOWN
conditions, PAUSE conditions, and ABORT conditions will be determined through
future simulation.

Future work:

1. Define Flow Buffer occupancy simulation.
2. Create a simulation model for Basket Stream rate and GPU drain behavior.
3. Validate state transition conditions for NORMAL / ELEVATED / HIGH / CRITICAL.
4. Organize Flow Buffer logs as capacity planning input.
5. Define monitoring abstraction for each hardware implementation.

This document defines only the conceptual model.
