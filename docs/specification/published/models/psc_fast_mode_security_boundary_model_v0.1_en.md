# PSC Fast Mode Security Boundary Model v0.1 (English Version)

---

# Document Information

- Document Name : PSC Fast Mode Security Boundary Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSC Fabric / Security Layer
- Document Type : Specification
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-05
- Last Updated  : 2026-05
- Language      : English

---

# 1. Overview

Fast Mode is a restricted ultra-low-latency communication mode within the PSC Fabric.

This mode is not defined as a general routing optimization mechanism.
Instead, it is defined as a restricted high-speed execution mode
available only within limited secure domains.

Fast Mode is intended for the following purposes:

- High-speed communication between CPU nodes and internally connected devices
- Restricted high-speed data transfer between GPU nodes
- Rack-local AI/HPC processing optimization
- Ultra-low-latency communication paths
- Efficient utilization of PSC Fabric internal bandwidth

However, Fast Mode may simplify or omit several safety controls
normally present in PSC Routing.

Therefore, Fast Mode requires strict security boundary management.

For this reason, Fast Mode shall only be available
within trusted local domains.

---

# 2. Fast Mode Definition

Fast Mode is an ultra-low-latency and high-bandwidth transfer mode
permitted only under restricted conditions within the PSC Fabric.

Fast Mode shall only be permitted when all of the following conditions are satisfied:

- Within PSC 1-hop connectivity
- Trusted Local Domain internal devices
- Within the same Secure Domain
- Communication between trusted nodes
- Communication authorized by the Resolver

Unlike normal Routing Mode,
Fast Mode is not intended for general Fabric Routing.

Therefore,
Fast Mode packets shall be prohibited from being forwarded
into the standard PSC Routing Fabric.

Fast Mode shall not be used
as an extension mechanism for general Routing Fabric.

---

# 3. Security Boundary Principles

Fast Mode prioritizes performance,
but strictly limits its usable scope.

The following principles define
the Fast Mode Security Boundary model.

## 3.1 Restricted Local Domain

Fast Mode shall be limited
to Rack-local or Node-local ranges.

Transfers to external networks
or unknown nodes shall be prohibited.

---

## 3.2 One-hop Limitation

Fast Mode prohibits communication paths
that traverse multiple PSC devices.

Only the following paths are permitted:

- CPU PSC → GPU PSC
- CPU PSC → Trusted Internal Device PSC
- GPU PSC → Trusted Local GPU Fabric Node
- CPU PSC → Local Memory Node PSC
- CPU PSC → Local Storage Node PSC

Communication paths traversing
more than one PSC hop shall be prohibited.

---

## 3.3 Managed GPU Local Fabric

GPU-to-GPU Fast Mode communication
shall only be permitted
within Resolver-authorized Local GPU Fabric Domains.

A Local GPU Fabric Domain
must be managed by
a CPU PSC or Management PSC.

GPU nodes shall not autonomously extend,
bridge, or federate Fast Mode Domains.

GPU-to-GPU Fast Mode communication
shall be restricted
to the same Trusted Local Domain
under CPU supervision.

---

## 3.4 Resolver Authority

Fast Mode participation
requires Resolver authentication
and policy-based authorization.

Unauthenticated nodes
shall be prohibited
from participating in Fast Mode.

---

## 3.5 Isolation Principle

Fast Mode Domains
shall be separated
from standard Routing Domains.

Fast Mode internal communication
shall not directly enter
the standard PSC Routing Fabric.

Fast Mode communication
must be logically isolatable
from standard Routing Telemetry
and Routing control paths.

---

## 3.6 Physical Port and Domain Limitation

Because Fast Mode assumes 1-hop connectivity,
the number of simultaneously connected Fast Mode endpoints
is limited by the PSC physical port count,
optical channel count,
or assignable lane capacity.

However,
Fast Mode limitations
shall not be defined solely
by simple physical port counts.

Fast Mode shall only be permitted
within Resolver-authorized Trusted Local Domains
under manageable operational conditions.

The scale of Fast Mode connectivity
shall be limited by:

- Local port/channel capacity
- Domain management capability
- Security Policy constraints

---

# 4. Allowed Topologies

The following configurations are permitted:

- CPU ↔ GPU direct connection configurations
- CPU ↔ NVMe high-speed connections
- Trusted Local GPU Fabric
- Trusted AI Processing Fabric
- Internal Accelerator Fabric
- Shared Memory Pool Fabric
- Trusted Local Memory Fabric

---

# 5. Forbidden Topologies

The following configurations are prohibited:

- PSC multi-hop Fast Mode
- Cross-rack Fast Mode
- Internet-routed Fast Mode
- Unknown node participation
- Unauthenticated device access
- External relay routing
- Dynamic unverified topology expansion
- Resolver bypass routing
- Autonomous GPU mesh expansion
- Unmanaged inter-domain Fast Mode bridging

---

# 6. Domain Identification

Fast Mode Domains
shall be managed separately
from standard Routing Domains.

Each Domain shall maintain:

- Domain ID
- Trust Level
- Resolver Policy ID
- Allowed Node Group
- Security Classification

The Resolver shall verify
Domain integrity
before communication begins.

---

# 7. Resolver Involvement

The Resolver plays a critical role
in Fast Mode control.

The Resolver manages:

- Fast Mode authorization
- Domain verification
- Trust validation
- Anomaly detection
- Fast Mode termination decisions
- Fallback control

Upon detection of dangerous conditions,
the Resolver shall be capable
of immediately disabling Fast Mode.

---

# 8. Fallback and Recovery

When Fast Mode abnormalities occur,
PSC shall safely return
to standard Routing Mode.

The following procedures shall be performed during recovery:

- Fast Mode termination
- Routing reevaluation
- Trust revalidation
- Resolver reauthentication
- Cooldown application
- Recovery Procedure execution

Immediate re-entry
from abnormal conditions
shall be prohibited.

---

# 9. Design Principles

The design principles of Fast Mode are as follows:

- Prioritize safety over raw performance
- Permit only trusted local communication
- Maintain Resolver control authority
- Clearly define Domain boundaries
- Prevent Fabric contamination propagation
- Enable isolation during AI runaway conditions
- Guarantee safe fallback to standard Routing

Fast Mode is not a mechanism
for accelerating the entire PSC Fabric.

Fast Mode is a restricted high-speed communication mechanism
permitted only within limited secure regions.

Fast Mode is a mechanism
for defining
"Trusted High-speed Local Regions"
within the PSC Fabric.
