# PSC Transfer Flow v0.1

## Document Information

- Document Name: PSC Transfer Flow
- Version: v0.1
- Project: PSC / Photon System Controller
- Layer: PSC Fabric
- Document Type: Specification
- Status: Draft
- Author: T. Hirose
- Created: 2026-03
- Last Updated: 2026-03
- Language: English

---

## 1. Purpose

PSC Transfer Flow defines the operational behavior of data movement inside the PSC Fabric.

It describes how a transfer is initiated, authorized, scheduled, transmitted, acknowledged, retried, and completed under PSC's receiver-driven and chunk-based communication model.

This specification focuses on transfer lifecycle behavior rather than packet field format.

---

## 2. Design Principles

PSC Transfer Flow is based on the following principles:

- receiver-driven authorization
- chunk-based transport
- credit-based flow control
- policy-aware scheduling
- adaptive routing under congestion
- localized retry and recovery

PSC does not treat a transfer as a single monolithic action.
Instead, each transfer is managed as a controlled sequence of states and chunk-level operations.

---

## 3. Transfer Model Overview

A PSC transfer proceeds through the following high-level stages:

1. Transfer Request
2. Transfer Evaluation
3. Transfer Grant
4. Transfer Scheduling
5. Chunk Transmission
6. Acknowledgement and Credit Update
7. Completion
8. Retry or Abort if needed

This model ensures that data is not transmitted unless the receiving side has accepted the transfer conditions.

---

## 4. Core Entities

The following entities participate in PSC Transfer Flow:

### Source Node
The node that owns or provides the data to be transferred.

### Destination Node
The node that will receive the data.

### Source PSC
The PSC responsible for coordinating transfer behavior at the sender side.

### Destination PSC
The PSC responsible for validating and accepting transfer behavior at the receiver side.

### Resolver
Evaluates fabric condition and policy constraints.

### Scheduler
Selects transfer execution timing and priority.

### SPU
Validates security and domain crossing rules.

### RCU
Selects paths and routing behavior.

### TMU
Creates and tracks transfer context.

### TEU
Executes chunk transmission and reception.

---

## 5. Transfer States

PSC Transfer Flow uses the following initial state model.

### IDLE
No active transfer context exists.

### REQUESTED
A transfer request has been issued but not yet accepted.

### EVALUATING
The destination side is validating resources, policy, and readiness.

### GRANTED
The transfer is authorized and resources have been reserved.

### SCHEDULED
The transfer is waiting for execution according to scheduler policy.

### ACTIVE
Chunks are being transmitted.

### PAUSED
Transfer is temporarily halted due to policy, congestion, or resource constraints.

### RETRY
A failed chunk or transfer segment is being retried.

### COMPLETING
Final chunks have been delivered and completion processing is in progress.

### COMPLETED
Transfer finished successfully.

### ABORTED
Transfer was terminated before completion.

### FAULTED
Transfer encountered an unrecoverable error or security violation.

---

## 6. Transfer State Machine

A typical PSC transfer follows this state progression:

IDLE
→ REQUESTED
→ EVALUATING
→ GRANTED
→ SCHEDULED
→ ACTIVE
→ COMPLETING
→ COMPLETED

Possible deviations include:

- ACTIVE → PAUSED
- PAUSED → ACTIVE
- ACTIVE → RETRY
- RETRY → ACTIVE
- REQUESTED → ABORTED
- EVALUATING → ABORTED
- ACTIVE → ABORTED
- ACTIVE → FAULTED

---

## 7. Transfer Request Phase

A transfer begins when the destination side requests or authorizes the movement of data according to PSC's receiver-driven model.

The request phase includes:

- source node identification
- destination node identification
- requested transfer size
- transfer type
- priority class
- security and domain validation context
- requested policy hints

A transfer request does not guarantee execution.
It only creates a candidate transfer context.

---

## 8. Transfer Evaluation Phase

During evaluation, the destination PSC determines whether the transfer may proceed.

Evaluation includes:

- receive buffer availability
- flow credit capacity
- security policy validation
- domain crossing authorization
- destination node readiness
- current congestion state
- route feasibility

The evaluation outcome may be:

- grant
- defer
- reject
- quarantine

---

## 9. Transfer Grant Phase

If evaluation succeeds, the destination side issues a transfer grant.

The grant defines the initial operating conditions for the transfer.

Grant information may include:

- transfer identifier
- permitted chunk size
- initial credit allocation
- allowed route scope
- security enforcement level
- policy profile
- retry limits

After grant issuance, the transfer becomes eligible for scheduling.

---

## 10. Scheduling Phase

The Scheduler determines when granted transfers may begin execution.

Scheduling decisions may depend on:

- priority class
- policy profile
- congestion state
- route availability
- credit availability
- transfer type
- local queue depth

PSC scheduling is not purely throughput-maximizing.
It is stability-aware and policy-aware.

Examples:

- memory-oriented traffic may be latency-prioritized
- bulk storage traffic may be throughput-shaped
- secure or quarantined traffic may be delayed or isolated

---

## 11. Active Transfer Phase

Once scheduled, the transfer enters ACTIVE state.

In ACTIVE state:

- chunks are emitted by TEU
- routing is selected by RCU
- credit limits are enforced by TMU / TEU
- security rules remain enforced by SPU
- Scheduler may continue shaping execution

A transfer remains ACTIVE while at least one chunk is in transmission, in-flight, or awaiting acknowledgement.

---

## 12. Chunk Transmission Model

PSC transfers are executed in chunk units.

Each chunk is treated as a controlled transport element with:

- chunk identity
- offset within transfer
- transfer association
- route selection
- credit cost
- acknowledgement status

Benefits of chunk-based execution include:

- fine-grained scheduling
- multipath distribution
- selective retry
- localized congestion adaptation

---

## 13. Credit Flow Control

PSC uses receiver-controlled credit flow.

The receiver advertises available transmission permission in credit units.

### Credit Rules

1. No chunk may be transmitted without sufficient credit.
2. Credit is consumed when a chunk is sent.
3. Credit is returned or refreshed when the receiver accepts progress.
4. Credit policy may be tightened under congestion.
5. Credit may be frozen during PAUSED or security-restricted states.

This prevents receiver overflow and stabilizes transfer pacing.

---

## 14. Acknowledgement Model

PSC uses acknowledgement to confirm chunk progress and support retry decisions.

Acknowledgement may operate at chunk granularity.

Possible acknowledgement outcomes include:

- accepted
- delayed
- rejected
- integrity failure
- policy violation

Acknowledgement also supports:

- credit refresh
- progress tracking
- completion detection
- retry trigger

---

## 15. Pause and Resume Behavior

A transfer may enter PAUSED state when continued execution is temporarily unsafe or undesirable.

Possible pause causes:

- congestion escalation
- credit exhaustion
- route instability
- destination-side pressure
- policy restriction
- security inspection

A paused transfer may later resume if:

- credits recover
- congestion reduces
- route becomes valid
- policy allows continuation

Pause does not imply failure.

---

## 16. Retry Model

PSC supports localized retry rather than whole-transfer restart whenever possible.

Retry may occur when:

- chunk loss is detected
- integrity verification fails
- link failure interrupts transmission
- temporary route failure occurs

### Retry Rules

1. Retry should be limited to failed chunks when possible.
2. Retry route may differ from original route.
3. Retry budget must be tracked per transfer.
4. Persistent failure may escalate to ABORTED or FAULTED.
5. Security-related failures may skip retry and go directly to fault handling.

This model improves efficiency and resilience.

---

## 17. Abort and Fault Handling

### ABORTED
The transfer is intentionally terminated before completion.

Possible reasons:

- sender cancellation
- receiver rejection
- timeout
- administrative policy
- unrecoverable congestion

### FAULTED
The transfer encountered a severe or invalid condition.

Possible reasons:

- security violation
- repeated integrity failure
- unrecoverable route collapse
- illegal state transition
- internal PSC malfunction

ABORTED and FAULTED are distinct.
Abort is controlled termination.
Fault is error termination.

---

## 18. Completion Phase

A transfer enters COMPLETING when all required chunks have been delivered and accepted.

Completion processing includes:

- final acknowledgement validation
- transfer accounting update
- resource release
- credit reconciliation
- telemetry update

After successful completion, the transfer enters COMPLETED state.

---

## 19. Multipath Transfer Behavior

PSC may distribute chunks across multiple paths when policy and topology allow it.

Multipath use may improve:

- throughput
- link utilization
- fault tolerance

Multipath requires:

- chunk identity preservation
- acknowledgement tracking
- reordering tolerance
- route-aware retry behavior

Multipath should be reduced or restricted under HOT or EMERGENCY conditions unless needed for recovery.

---

## 20. Congestion Interaction

Transfer behavior must adapt to PSC fabric state.

### CALM
- normal scheduling
- normal credit issuance
- multipath allowed
- throughput optimization allowed

### WARM
- moderate shaping
- reduced aggressive striping
- preference for stable routes
- selective admission control

### HOT
- stricter admission control
- reduced transfer concurrency
- priority enforcement
- possible pause of low-priority transfers

### EMERGENCY
- only essential traffic prioritized
- non-critical transfers paused or rejected
- aggressive stabilization
- quarantine and protection behavior enabled

---

## 21. Transfer Control Ownership

PSC modules participate in transfer control as follows.

### Resolver
Evaluates transfer eligibility against fabric condition.

### Scheduler
Determines when the transfer may run.

### SPU
Validates security and domain rules.

### RCU
Chooses routes and adapts path selection.

### TMU
Maintains transfer state, credits, and retry context.

### TEU
Executes chunk send and receive behavior.

### OMU
Reports link degradation relevant to transfer adaptation.

### Telemetry / Fault Monitor
Collects progress, anomalies, and escalation events.

---

## 22. Initial Transfer Policy Rules

### Rule 1
Every transfer must have exactly one Transfer ID.

### Rule 2
No transfer may enter ACTIVE state without grant.

### Rule 3
No chunk may be transmitted without available credit.

### Rule 4
A paused transfer retains context unless explicitly aborted.

### Rule 5
Retry must preserve transfer identity even if path changes.

### Rule 6
Security policy may override performance policy.

### Rule 7
A transfer in FAULTED state must not re-enter ACTIVE directly.

### Rule 8
Completion requires both delivery progress and acceptance confirmation.

---

## 23. Example Transfer Flow

Example:

1. Destination requests a block transfer.
2. Destination PSC evaluates buffer and policy readiness.
3. Grant is issued with chunk size and initial credit.
4. Scheduler places the transfer in execution order.
5. TEU transmits chunks.
6. Receiver acknowledges accepted chunks and returns credits.
7. One chunk fails integrity verification.
8. That chunk is retried on an alternate route.
9. Remaining chunks complete successfully.
10. Transfer enters COMPLETING and then COMPLETED.

---

## 24. Design Significance

PSC Transfer Flow provides the following advantages:

1. Receiver-safe transfer execution  
   Data is only transmitted when the receiver is prepared.

2. Chunk-level adaptability  
   Transfers can be paced, retried, and rerouted efficiently.

3. Congestion-aware behavior  
   Transfer execution adapts to actual fabric condition.

4. Policy-native communication  
   Security and domain rules remain active throughout transfer lifecycle.

---

## 25. Open Design Notes

The following items remain open for future refinement:

- exact grant message structure
- detailed acknowledgement encoding
- retry budget policy
- timeout model
- reordering behavior in multipath mode
- interaction between Trust Level and transfer admission
