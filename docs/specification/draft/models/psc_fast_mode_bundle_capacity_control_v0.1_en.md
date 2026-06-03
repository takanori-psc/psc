# PSC Fast Mode Bundle Capacity Control v0.1

## 1. Document Information

- Document Name : PSC Fast Mode Bundle Capacity Control
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Fast Mode / Capacity Control
- Document Type : Design Draft
- Status : Draft
- Language : English

- Related Models:
  - PSC Fast Mode Security Boundary Model v0.1
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC RCU Recovery Return Model v0.2
  - PSC Recovery Return Abort Handling v0.1
  - PSC Telemetry Model v0.2

---

## 2. Purpose

This draft defines capacity stabilization and source throttling behavior for
PSC Fast Mode when one or more physical lanes degrade inside a Fast Mode bundle.

Fast Mode is an isolated 1-hop trusted local capacity-control mode between a
CPU node PSC and a local device node PSC, GPU node PSC, or NVMe node PSC. It is
not a general routing mode or a complex arbitration mode.

Example:

```text
CPU PSC
<-> local device node PSC / GPU node PSC / NVMe node PSC
```

Multiple physical lanes may exist inside a single Fast Mode bundle. If lane
capacity changes, PSC must stabilize the bundle rather than immediately trying
to restore full utilization.

---

## 3. Scope

This draft covers:

- boundary isolation control
- lane degradation detection
- effective bundle capacity calculation
- source throttling requests
- capacity stabilization margin
- capacity recovery ramp
- bundle failure conditions
- no-capacity-margin conditions
- observation and evidence requirements

This draft does not define:

- general PSC routing fallback
- complex multi-path Resolver arbitration
- device-internal bottleneck diagnosis
- Fast Mode packet format
- production threshold values
- simulation behavior
- validator behavior
- Evidence Matrix entries

---

## 4. Key Concepts

| Term | Meaning |
|------|---------|
| Fast Mode Bundle | A direct trusted Fast Mode connection between PSC endpoints that may contain multiple physical lanes |
| Lane Health | Per-lane operational condition such as healthy, degraded, unavailable, or failed |
| Bundle Health | Aggregate health of the Fast Mode Bundle derived from lane health, capacity, confidence, and policy |
| Effective Capacity | The usable capacity after excluding unavailable lanes and applying degradation and safety margin |
| Safety Margin | Reserved capacity headroom used to prevent overload and oscillation after lane degradation |
| Source Throttle | A policy-controlled request to the source-side PSC to reduce or shape offered traffic |
| Capacity Recovery Ramp | Gradual restoration of allowed utilization after capacity evidence becomes stable |
| NO_CAPACITY_MARGIN | A condition where remaining capacity cannot safely absorb the traffic demand |
| Boundary Gate | The minimum Fast Mode boundary logic that enforces local trusted 1-hop containment and explicit exit / fallback handoff |
| Capacity Manager | The minimum Fast Mode capacity logic that tracks lane health, bundle health, effective capacity, safety margin, throttling, and recovery ramp |
| LANE_LOSS | A physical or structural lane failure class that requires lane exclusion and firmware-visible warning |

---

## 5. Design Principles

### 5.1 Isolated 1-Hop Trusted Local Mode

Fast Mode is limited to a trusted local domain and a 1-hop local connection.

The primary intended relationship is:

```text
CPU node PSC
<-> local device node PSC / GPU node PSC / NVMe node PSC
```

Fast Mode must remain isolated between the CPU node and local node area. It must
not automatically escape into the routing fabric.

Normal PSC routing or fabric control may resume only after explicit Fast Mode
exit or fallback handoff.

### 5.2 Fast Mode Is Not Alternate Routing

Fast Mode bundle degradation must not assume that another route exists.

When a CPU PSC and GPU PSC communicate through a direct trusted bundle, the
bundle may have multiple lanes, but those lanes are not independent routing
paths in the normal PSC fabric.

Fast Mode must not perform general routing and should not include complex
multi-path Resolver arbitration. Resolver involvement in this model is limited
to authorization, policy, boundary decisions, suspension, or fallback handoff.

### 5.3 Stabilize Capacity Before Restoring Utilization

When lane capacity decreases, PSC must first stabilize traffic against the new
effective capacity.

Immediate full-capacity restoration can overload remaining lanes and create
oscillation.

### 5.4 Source-Side Control Is First-Class

If destination-side or bundle-side capacity decreases, the source-side PSC may
need to reduce the offered traffic rate.

Source throttling must be policy controlled and explainable.

If Fast Mode cannot maintain safe margin, it should throttle source traffic or
suspend Fast Mode.

### 5.5 Observation Must Support the Decision

Capacity changes must be backed by evidence. If LIGHT observation is
insufficient, PSC should increase observation density or promote to FULL
observation before increasing utilization.

---

## 6. Minimum Fast Mode Logic

Fast Mode v0.1 should keep only the minimum required logic.

```text
Fast Mode Logic =
Boundary Gate
+ Capacity Manager
```

### 6.1 Boundary Gate

Boundary Gate handles:

- 1-hop enforcement
- trusted local domain validation
- CPU node <-> local device node containment
- routing fabric isolation
- explicit exit / fallback handoff

Boundary Gate does not perform route search or general PSC path selection.

### 6.2 Capacity Manager

Capacity Manager handles:

- lane health
- bundle health
- effective capacity
- baseline and dynamic safety margin
- source throttle
- capacity recovery ramp

Capacity Manager does not arbitrate among unrelated fabric paths. It controls
local Fast Mode bundle capacity and source-side pressure.

---

## 7. Capacity Planning and Double Margin

Fast Mode capacity should be planned with two distinct margins.

### 7.1 Hardware-Level Headroom

Node designers should estimate maximum theoretical node bandwidth.

Required optical channel count should be selected with hardware-level headroom
so target devices can run at maximum expected load with margin.

### 7.2 PSC Control-Level Safety Margin

PSC then applies an additional control-level safety margin.

PSC reserves operational margin, monitors margin consumption, and uses that
margin to absorb jitter, retry, transient delay variance, and recovery ramp
uncertainty.

Fast Mode should not depend on raw 100% physical capacity in normal operation.
Specific margin values remain implementation and simulation dependent.
Simulation should later tune margin rules and recovery behavior.

If unexplained noise, jitter, retry, delay variance, or instability repeatedly
consumes a large portion of the PSC safety margin, Fast Mode should classify the
bundle as unstable and may suspend or downgrade Fast Mode.

---

## 8. Scope Control for Node-Internal Causes

Fast Mode v0.1 focuses on PSC-visible lane and bundle capacity plus boundary
isolation.

Device-internal causes are outside the primary Fast Mode logic, including:

- GPU thermal throttle
- VRAM pressure
- DMA congestion
- node-internal bottlenecks
- application-local scheduling limits

These may be represented later as external node-side capacity reports. Fast
Mode v0.1 should not attempt to diagnose or arbitrate those causes internally.

---

## 9. Lane Degradation Detection

PSC should detect lane degradation using evidence such as:

- lane down or unavailable signal
- optical error or link quality degradation
- increased retry, loss, or corruption indicators
- reduced lane throughput
- increased latency or variance
- stale or conflicting telemetry
- reduced observation confidence
- lane-loss or repeated lane-loss after reinitialization

Lane health classes:

| Lane Health | Description |
|-------------|-------------|
| HEALTHY | Lane can carry expected traffic within policy and safety margin |
| DEGRADED | Lane remains usable but at reduced confidence or capacity |
| LIMITED | Lane is usable only under throttled or restricted conditions |
| UNAVAILABLE | Lane cannot carry traffic temporarily |
| FAILED | Lane must be excluded until recovery validation succeeds |

### 9.1 Lane-Loss Handling

`LANE_LOSS` should be treated as a physical or structural failure class, not as
normal quality degradation.

A lane that enters `LANE_LOSS` should be marked `FAILED` and excluded from Fast
Mode capacity. Automatic runtime recovery of `LANE_LOSS` should not be assumed.

Recovery should require one of the following:

- system power cycle
- explicit maintenance action
- hardware reinitialization

If the same lane-loss condition reappears after reinitialization or power
cycle, PSC should keep Fast Mode disabled for that lane or bundle and emit a RED
firmware-level warning.

Operators or maintenance systems should inspect:

- optical cable
- connector
- optical module
- rack / node joint
- PSC endpoint
- related physical layer

---

## 10. Effective Bundle Capacity

Effective Capacity is the currently usable bundle capacity after accounting for
lane health and safety margin.

Conceptual calculation:

```text
raw_lane_capacity = sum(healthy_lane_capacity + degraded_lane_usable_capacity)
effective_capacity = raw_lane_capacity - safety_margin
```

PSC should not expose raw lane capacity directly to traffic admission. It should
admit traffic based on effective capacity.

Effective Capacity inputs:

- number of healthy lanes
- number of degraded lanes
- per-lane usable capacity
- lane confidence
- telemetry freshness
- bundle policy
- safety margin
- traffic class

---

## 11. Safety Margin

Safety Margin is reserved bundle capacity that prevents the remaining lanes from
being driven to saturation after degradation.

Safety Margin should increase when:

- one or more lanes degrade
- observation confidence decreases
- telemetry is stale or conflicting
- lane recovery is recent
- traffic is bursty
- Resolver classifies the bundle as unstable

Safety Margin may decrease only after stable evidence persists through a
capacity recovery validation window.

---

## 12. Source Throttle

When offered traffic exceeds effective capacity, PSC should request source-side
throttling.

Source Throttle may request:

- reduced offered rate
- temporary burst shaping
- deferral of low-priority traffic
- preservation of high-priority traffic
- delayed retry for capacity-sensitive transfers

All source throttling must be policy controlled.

Source Throttle is expected when:

- one or more lanes become degraded or unavailable
- remaining lanes have insufficient capacity margin
- bundle health becomes LIMITED
- recovery ramp is active but not yet complete
- observation confidence is insufficient for full utilization

---

## 13. Capacity Recovery Ramp

When capacity is restored, PSC should not immediately return to full
utilization.

Capacity Recovery Ramp gradually increases allowed utilization only after:

- failed or degraded lanes report recovery
- telemetry freshness is acceptable
- confidence is sufficient
- lane stability persists over a validation window
- bundle health is no longer degraded
- Resolver or policy permits recovery

The ramp should:

- start from the current effective capacity
- increase allowed utilization gradually
- preserve safety margin
- stop or hold if telemetry becomes suspicious
- abort if hard failure or unsafe evidence appears

This behavior follows the same stability-first principle as Recovery Return and
Recovery Abort Handling.

---

## 14. No-Capacity-Margin Conditions

`NO_CAPACITY_MARGIN` occurs when remaining bundle capacity cannot safely absorb
the offered traffic after lane degradation.

This may occur even if at least one lane remains healthy.

Expected behavior:

- do not assume the bundle can continue at prior capacity
- hold current state if forwarding remains safe
- request source reduction
- increase observation density or promote LIGHT to FULL observation
- trigger Resolver re-evaluation if ambiguity remains
- avoid immediate full recovery until capacity evidence stabilizes

`NO_CAPACITY_MARGIN` is not the same as bundle failure. It means remaining
capacity is insufficient for safe admission at the current offered load.

---

## 15. Bundle Failure Conditions

A Fast Mode Bundle should be considered unavailable when:

- all lanes are failed or unavailable
- lane loss prevents safe Fast Mode operation
- forwarding safety cannot be maintained
- optical failure affects the bundle as a whole
- severe corruption is detected
- source throttling cannot reduce traffic enough to keep forwarding safe
- policy prohibits continued Fast Mode use

Expected behavior:

```text
Fast Mode unavailable
-> exit or suspend Fast Mode
-> fall back to normal PSC behavior if available
-> notify Resolver and source-side PSC
```

Fallback to normal PSC behavior is conditional. It is used only if a valid
normal PSC path exists and policy allows it.

Fast Mode must not automatically escape into the routing fabric. Normal PSC
routing or fabric control may resume only after explicit Fast Mode exit or
fallback handoff.

---

## 16. Fast Mode Host and Firmware Notification

PSC performs Fast Mode protection actions autonomously.

Host, OS, UEFI, BIOS, and firmware notifications are for visibility, user
warning, event logging, and maintenance guidance. OS participation must not be
required for PSC to perform critical Fast Mode protection.

### 16.1 Severity Levels

| Severity | Meaning | Expected Notification | Expected Fast Mode Action |
|----------|---------|-----------------------|---------------------------|
| GREEN | Normal Fast Mode operation | No warning required | Continue normal Fast Mode |
| YELLOW | Fast Mode remains operational, but quality has degraded | OS-level notification and system event log after boot | Continue without shutdown, possibly throttle or reduce capacity |
| RED | Fast Mode cannot be safely maintained, or initialization detects a critical Fast Mode condition | UEFI / BIOS / firmware-level warning | Disable or suspend Fast Mode; use normal PSC behavior if available |
| BLACK | PSC or required base fabric cannot initialize safely | Firmware / service-level failure indication | Boot may be blocked or service intervention may be required |

### 16.2 YELLOW Conditions

YELLOW conditions indicate degraded but still operational Fast Mode behavior.
The system should continue without shutdown.

Examples:

- `LANE_DEGRADATION`
- `MARGIN_CONSUMPTION_HIGH`
- `NOISE_DEGRADATION`
- `SOURCE_THROTTLE_ACTIVE`
- `FAST_MODE_DEGRADED`
- `BUNDLE_UNSTABLE` while still operational

Example user-facing warning:

```text
Fast Mode link quality is degraded. PSC is reducing transfer rate to maintain stability.
```

### 16.3 RED Conditions

RED conditions indicate that Fast Mode cannot be safely maintained.

These may be detected before OS boot or during Fast Mode initialization. RED
conditions should be visible at UEFI / BIOS / firmware level because the OS may
not be reached or Fast Mode may be disabled before OS boot.

Expected behavior:

- disable or suspend Fast Mode
- continue using normal PSC behavior if available
- keep failed lanes excluded
- record firmware-visible diagnostic information
- guide hardware inspection or maintenance

Examples:

- `LANE_LOSS`
- `OPTICAL_MODULE_FAILURE`
- `CONNECTOR_FAULT`
- `PSC_PHY_FAILURE`
- `FAST_MODE_INITIALIZATION_FAILURE`
- repeated lane-loss after system power cycle or reinitialization

Example user-facing warning:

```text
PSC Fast Mode critical warning: lane loss detected. Fast Mode has been disabled. Check optical cable, connector, optical module, rack/node joint, or PSC endpoint.
```

### 16.4 BLACK Conditions

BLACK conditions are outside normal Fast Mode degradation.

They indicate that PSC or the required base fabric cannot initialize safely.
Normal boot may be blocked or require service intervention.

### 16.5 OS vs Firmware Responsibility

PSC must perform protection autonomously.

OS notification is for:

- user visibility
- event logging
- maintenance guidance
- operational status display

YELLOW conditions may be reported to the OS after boot.

RED conditions should be reported at UEFI / BIOS / firmware level because Fast
Mode may be disabled before OS boot or the OS may not be reached.

BLACK conditions may prevent normal boot if base PSC initialization is unsafe.

---

## 17. Expected Behavior Examples

| Case | Condition | Expected Behavior |
|------|-----------|-------------------|
| A | 8 lanes healthy | Effective capacity remains 100% |
| B | 1 lane degraded | Effective capacity is reduced and source throttle is requested if offered load exceeds safe capacity |
| C | Capacity restored | Capacity Recovery Ramp gradually returns utilization toward full capacity |
| D | Remaining lanes have insufficient margin | Emit or classify `NO_CAPACITY_MARGIN`, hold current state when safe, and request source reduction |
| E | Bundle failure | Fast Mode becomes unavailable and PSC falls back to normal behavior if available |
| F | Lane loss | Mark the lane FAILED, exclude it from Fast Mode capacity, and emit RED firmware-level warning |

---

## 18. Observation and Evidence Requirements

PSC must retain enough evidence to explain capacity decisions.

Minimum evidence:

- bundle identifier
- lane identifiers
- lane health state
- bundle health state
- effective capacity
- safety margin
- offered traffic estimate
- source throttle request state
- observation mode
- telemetry freshness
- telemetry confidence
- Resolver decision or policy reason
- notification severity
- host / firmware notification state
- lane-loss recurrence state

If LIGHT observation cannot provide sufficient evidence for capacity increase,
PSC must hold capacity recovery or promote to FULL observation.

---

## 19. Draft Validation Direction

This document is a draft specification only.

Future validation work may add:

- lane degradation source throttle scenario
- no-capacity-margin scenario
- capacity recovery ramp scenario
- bundle failure fallback scenario
- host / firmware notification severity scenario
- lane-loss recurrence scenario
- LIGHT-to-FULL observation promotion scenario

No simulation, validator, Evidence Matrix, or published specification update is
defined by this document.
