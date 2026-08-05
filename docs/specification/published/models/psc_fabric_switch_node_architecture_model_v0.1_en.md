# PSC Fabric Switch Node Architecture Model v0.1

## Document Information

- Document Name : PSC Fabric Switch Node Architecture Model
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Hardware / Fabric Switch Node
- Document Type : Specification
- Status : Draft
- Author : T. Hirose
- Created : 2026-08
- Last Updated : 2026-08
- Language : English

---

## 1. Purpose

This document defines the node structure, port allocation, route structure,
failure handling, capacity model, and control architecture specific to a PSC
Fabric Switch Node built on the shared PSC chiplet architecture.

---

## 2. Scope

This document covers:

- a dual-system Fabric Switch Node using System A and System B
- a 64-port node composed of two 32-port PSC Switches
- logical port allocation to a CPU Node, external PSC Fabric, and the Inter-System Cross-Connect
- design intent for route selection, failure handling, capacity, and degraded operation
- treatment of optical ports as logical interfaces
- division of responsibility between dedicated hardware and the RISC-V Control Cluster

Optical physical-layer details and higher-level control policy, Recovery Return /
Return Ramp, Resolver, and trust / security policy are not redefined here.

---

## 3. Terminology

| Term | Meaning |
|------|---------|
| Fabric Switch Node | Node composed of the System A and System B PSC Switches |
| System A / System B | Two independently operating switch systems |
| CPU Node Connection | Per-system 8-port group dedicated to one corresponding CPU Node |
| External Route | 8-port logical route group connected to external PSC Fabric |
| Inter-System Cross-Connect | 8-port inter-system route used to access the opposite system's external routes |
| Logical Port | PSC Fabric interface and its corresponding bandwidth unit |
| Route Capacity | Sum of logical port line rates, not guaranteed effective bandwidth |

---

## 4. Node Role

The PSC Fabric Switch Node connects one CPU Node to external PSC Fabric and
provides route choices through System A / System B, multiple external routes,
and the Inter-System Cross-Connect. This node-specific model is separate from
the `PSC Chiplet Architecture Model v0.1`, which defines shared chiplets.

The 64-port PSC Fabric Switch Node defined here represents one `PSC Compute
Group` within a rack, not the entire rack. One Fabric Switch Node connects to
one CPU Node dedicated to the same group through 16 logical ports across A/B.

---

## 5. Default Node Structure

```text
PSC Fabric Switch Node
├ System A PSC Switch: 32 logical ports
└ System B PSC Switch: 32 logical ports
```

The node has 64 logical ports in total. Each system is an independent PSC
Switch and uses a RISC-V Control Cluster. The design remains in progress.

### 5.1 Rack-Level Group Scaling

One PSC Compute Group consists of:

- one PSC Fabric Switch Node
  - System A PSC Switch
  - System B PSC Switch
- one corresponding CPU Node
  - PSC-A
  - PSC-B
- Local Nodes dedicated to that CPU Node
  - GPU Node
  - AI Long-Term Memory Node
  - Storage Node

```text
PSC Rack
├ Compute Group 0
│  ├ PSC Fabric Switch Node 0
│  ├ CPU Node 0
│  └ Dedicated Local Nodes
├ Compute Group 1
│  ├ PSC Fabric Switch Node 1
│  ├ CPU Node 1
│  └ Dedicated Local Nodes
├ Compute Group 2 (optional)
└ Compute Group 3 (optional)
```

A physical rack can contain multiple independent PSC Compute Groups. One, two,
or four groups are current configuration candidates, but v0.1 does not fix or
require a group count per rack. Physical space, power, cooling, weight, optical
cabling, and maintainability determine the deployable group count.

The CPU Node and Local Nodes in each group are dedicated to that group. Sharing
Local Nodes across multiple PSC Compute Groups is not part of the current base
model. Each group is treated as an independently isolatable failure domain
within the rack-level architecture. Shared rack-level resources, including
power, cooling, physical structure, and management infrastructure, may remain
common failure factors. If the CPU Node or Fabric Switch Node in one group
stops, other groups in the rack should in principle continue operating unless
a shared rack-level failure is involved.

Inter-group communication uses each Fabric Switch Node's external PSC Fabric
routes. A dedicated direct connection between PSC Compute Groups in the same
rack is not a current mandatory requirement.

The following simple line-rate examples use the current 800 Gb/s logical-port
assumption.

| Compute Groups per Rack | Aggregate CPU-Node Line Rate | Aggregate External Physical Line Rate |
|-------------------------|------------------------------|---------------------------------------|
| 1 | 12.8 Tb/s | 25.6 Tb/s |
| 2 | 25.6 Tb/s | 51.2 Tb/s |
| 4 | 51.2 Tb/s | 102.4 Tb/s |

This table is a simple sum of logical port line rates. It does not guarantee
effective bandwidth, upstream Fabric capacity, power, cooling, cabling,
weight, or maintainability.

---

## 6. System A / System B Architecture

System A and System B use the same 32-port configuration.

| Port Group | Ports per System | Role |
|------------|------------------|------|
| CPU Node Connection | 8 | Dedicated connection to one corresponding CPU Node |
| Inter-System Cross-Connect | 8 | Inter-system route to the opposite system |
| External PSC Fabric | 16 | Two 8-port external routes |
| Total | 32 | Logical port count per system |

Power, Port Chiplets, optical wiring, upstream switches, and other resources
should be separated into different failure domains where practical.

---

## 7. Port Configuration

### 7.1 System A

- CPU Node Connection: 8 ports connected to PSC-A in the CPU Node
- A-to-B Cross-Connect Route: 8 ports
- A-1 Route: 8 external ports
- A-2 Route: 8 external ports

### 7.2 System B

- CPU Node Connection: 8 ports connected to PSC-B in the CPU Node
- B-to-A Cross-Connect Route: 8 ports
- B-1 Route: 8 external ports
- B-2 Route: 8 external ports

The eight CPU-facing ports in each system are not one-port allocations to
multiple CPU Nodes. All eight System A ports and all eight System B ports
connect to the same single CPU Node.

### 7.3 Logical Port and Optical Interface

The standard configuration assumes optical connectivity for CPU Node,
external Fabric, and Inter-System Cross-Connect links. One port is treated as
a logical PSC port with an aggregate bandwidth of 800 Gb/s. This is a current
design assumption, not a finalized physical product specification, and must
not be interpreted as one physical lane.

Physical lane count, lane speed, modulation, wavelengths, Duplex mode, FEC,
connector, transceiver, reach, and optical power budget are not fixed.
Pluggable Optics, Onboard Optics, External Optical Engines, and Co-Packaged
Optics remain future candidates. Short-reach electrical connectivity for a
future same-board or same-package implementation is not prohibited. Actual
electrical-to-optical conversion may be placed inside or outside the PSC
package, and the logical route structure is independent of the selected
optical implementation.

---

## 8. External Route Structure

The 16 external ports in each system are divided into two independent 8-port
routes.

```text
System A: A-1 (8) + A-2 (8)
System B: B-1 (8) + B-2 (8)
```

Assumed physical line-rate capacity of one external route:

`800 Gb/s × 8 ports = 6.4 Tb/s`

External physical capacity per system:

`6.4 Tb/s × 2 routes = 12.8 Tb/s`

Across the Fabric Switch Node:

`12.8 Tb/s × 2 systems = 25.6 Tb/s`

---

## 9. Inter-System Cross-Connect

Each Cross-Connect direction has eight logical ports and an assumed 6.4 Tb/s
line rate.

- A-to-B provides access from System A to B-1 / B-2
- B-to-A provides access from System B to A-1 / A-2

The Cross-Connect is not merely a set of standby ports. It is an inter-system
route for using the opposite system's external routes. It may be used for
external route or path failures, congestion avoidance, route switching, and
staged recovery.

If the System A Switch completely stops, A-to-B cannot be used. If the System
B Switch completely stops, B-to-A cannot be used. The CPU Node must then
select the healthy opposite system directly.

---

## 10. CPU Node Connectivity

The CPU Node and Fabric Switch Node connect through 16 logical ports across A/B.

- System A 8 ports -> PSC-A in the same CPU Node
- System B 8 ports -> PSC-B in the same CPU Node
- per-system capacity: `800 Gb/s × 8 = 6.4 Tb/s`
- aggregate A/B physical line rate: `6.4 Tb/s × 2 = 12.8 Tb/s`

No Cross-Connect is provided between PSC-A and PSC-B inside the CPU Node.
Local nodes connect directly to both systems, allowing the source side to
select the healthy system. If one entire system stops, operation continues
through the remaining eight ports at an assumed maximum 6.4 Tb/s.

---

## 11. Route Selection

Each system provides three 6.4 Tb/s route candidates for up to eight ports of
traffic entering from the CPU Node.

- System A: A-1, A-2, A-to-B Cross-Connect
- System B: B-1, B-2, B-to-A Cross-Connect

Normal operation uses the two same-system external routes. Under failure or
congestion, choices include the remaining same-system external route, an
opposite-system route through the Cross-Connect, or direct selection of the
opposite system by the CPU Node.

Detailed route policy, staged recovery, Return Ramp, Resolver arbitration,
and trust / security policy belong to higher-level PSC control models. This
hardware model does not duplicate validated control RULEs.

---

## 12. Failure Handling

- Failure of one 8-port external route does not immediately require capacity
  degradation when the other same-system route is healthy and has sufficient capacity.
- If both external routes in one system are unavailable, bandwidth can be
  maintained through the Cross-Connect when both opposite-system routes are
  healthy and have sufficient available capacity.
- In these cases route redundancy decreases, but available bandwidth does not
  necessarily decrease.
- Capacity-degraded operation begins when remaining effective capacity falls
  below required bandwidth.
- If the entire System A or System B Switch stops, the CPU Node selects the
  remaining system and maximum connection line rate falls from 12.8 to 6.4 Tb/s.
- A common node-wide failure or simultaneous A/B failure cannot be sustained
  by this node alone.

Cross-Connect and A-1 / A-2 / B-1 / B-2 should avoid excessive sharing of
power, Port Chiplets, optical wiring, and upstream switches so that redundancy
is not merely apparent.

---

## 13. Capacity and Degraded Operation

| Connection / Route | Calculation | Assumed Line Rate |
|--------------------|-------------|-------------------|
| CPU Node connection per system | 800 Gb/s × 8 | 6.4 Tb/s |
| CPU Node connection across A/B | 6.4 Tb/s × 2 | 12.8 Tb/s |
| One external route | 800 Gb/s × 8 | 6.4 Tb/s |
| External capacity per system | 6.4 Tb/s × 2 | 12.8 Tb/s |
| Node-wide external physical capacity | 12.8 Tb/s × 2 | 25.6 Tb/s |
| One directional Cross-Connect route | 800 Gb/s × 8 | 6.4 Tb/s |

These values are simple sums of logical port line rates, not guaranteed
effective bandwidth. Effective bandwidth accounting for protocol overhead,
control traffic, Telemetry, retransmission, and buffer contention will be
determined by future simulation and implementation evaluation.

The following are conceptual operational labels for explanation only:

- NORMAL
- ROUTE_REDUNDANCY_DEGRADED
- CRITICAL_SINGLE_PATH
- CAPACITY_DEGRADED
- ISOLATED

Because `NORMAL` and `ISOLATED` are already used in existing PSC models, this
document does not define this set as a new official state model. Formal state
names, transitions, and thresholds require separate alignment with existing
state models.

---

## 14. Control Architecture

### 14.1 Dedicated Hardware

- link-heartbeat monitoring
- timeout detection
- transfer-gate control
- emergency cut
- fault-event latch
- minimum fault-information retention

### 14.2 RISC-V Control Cluster

- fault-cause classification
- route-state management
- route selection
- A/B inter-system coordination
- notification to other nodes
- Telemetry aggregation
- input provision for Hold / Switch / Return decisions
- log management

### 14.3 Higher-Level PSC Control Models

- detailed route-selection policy
- staged recovery and Return Ramp
- Resolver arbitration
- trust and security policy

Processing is not concentrated entirely in firmware. Dedicated hardware
handles immediate safety actions, while the RISC-V cluster and higher-level
control models handle policy and coordination.

---

## 15. Telemetry and Logging

The Port Chiplet and control plane distinguish and report at least:

- optical lane-level degradation
- logical port-level degradation
- route-group-level degradation
- complete route loss

Link state, capacity indication, failure domain, route availability, and
Cross-Connect use are aggregated as Telemetry for route selection and fault
analysis. Lane Remapping, FEC, optical-module recovery, and physical-layer
retransmission are outside this model.

---

## 16. Design Status and Future Work

This model is Draft. Open or future work includes:

- product specification of the 800 Gb/s logical-port assumption
- simulation of effective bandwidth, oversubscription, and buffer contention
- physical optical lanes, modulation, wavelengths, Duplex mode, FEC, connector, reach, and power budget
- selection among Pluggable / Onboard / External Engine / Co-Packaged Optics
- physical implementation of failure-domain separation
- formal mapping of conceptual operational labels to existing state models
- implementation-specific route-selection, capacity-degradation, and recovery thresholds
- the future document candidate `PSC Optical Interface Model`

Formal references:

- `docs/specification/published/models/psc_chiplet_architecture_model_v0.1_en.md`
- `docs/specification/published/models/psc_resolver_arbitration_extension_model_v0.2x_en.md`
- `docs/specification/published/models/psc_trust_model_v0.1_en.md`
- `docs/specification/published/models/psc_state_transition_model_v0.1_en.md`
- `docs/specification/published/models/psc_fast_mode_security_boundary_model_v0.1_en.md`
- `docs/specification/published/models/psc_rcu_recovery_return_model_v0.2_en.md`
- `docs/specification/published/models/psc_recovery_return_extension_model_v0.2x_en.md`
