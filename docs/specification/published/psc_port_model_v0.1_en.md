# PSC Port Model v0.1

## Document Information

- Document Name: PSC Port Model
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Fabric
- Document Type : Specification
- Status : Draft
- Author : T. Hirose
- Created : 2026-03
- Last Updated : 2026-03
- Language : English

---

## 1. Purpose

PSC Port is not defined as a fixed device-specific interface.

Instead, each port is defined as a **role-based communication endpoint**.

Port behavior is determined by the following factors.

- Policy
- Trust Class
- Domain
- Transfer Requirements

This allows PSC to treat ports not as static bus attachments  
but as **adaptive fabric endpoints**.

---

## 2. Design Principles

### 2.1 Conventional Port Model

Ports are statically assigned to device categories.

Examples:

- GPU Port
- Storage Port
- Network Port

### 2.2 PSC Port Model

A PSC port represents a **logical communication role**.

A port primarily represents not:

- what device is attached

but rather:

- role
- security level
- communication policy
- domain
- transfer characteristics

---

## 3. Port Definition

A PSC Port is a communication endpoint connected to the PSC Fabric.

Possible connections:

- Local devices
- Other PSC nodes
- Fabric links

Each port has the following attributes:

- Port ID
- Port Role
- Port Mode
- Security Class
- Policy Profile
- Domain Scope
- Link State
- Capability Flags

---

## 4. Port Structure
```
PSC Port
├ Port ID
├ Port Role
├ Port Mode
├ Security Class
├ Policy Profile
├ Domain Scope
├ Link State
└ Capability Flags
```

---

## 5. Port ID

Port ID is the identifier used to distinguish a communication endpoint within a PSC node.

Requirements:

- Unique within a PSC node
- Used by Resolver / Scheduler / RCU / TMU
- Mapped to routing tables
- Logical roles may change without modifying physical wiring

Examples:

- Port 0x01
- Port 0x02
- Port 0x03

---

## 6. Port Role

The current logical role of the port.

Examples:

- Compute
- Memory
- Storage
- Network
- Fabric
- Management

---

## 7. Port Mode

Operational mode of the port.

- Endpoint Mode
- Fabric Link Mode
- Relay Mode
- Isolated Mode
- Maintenance Mode

---

## 8. Security Class

Trust level applied to the port.

- System
- Trusted
- User
- External
- Quarantined

---

## 9. Policy Profile

Defines communication behavior.

- Latency Optimized
- Throughput Optimized
- Secure
- Balanced
- Resilient

---

## 10. Domain Scope

Defines where the port may communicate.

- Local Node
- Local Fabric
- Cluster
- Global Fabric
- External Boundary

---

## 11. Link State

Link state:

- DOWN
- INIT
- READY
- DEGRADED
- RESTRICTED
- FAULT

---

## 12. Capability Flags

Capabilities supported by the port.

Examples:

- Chunk Transfer Supported
- Credit Flow Control Supported
- Secure Tag Enforcement Supported
- Multi-path Eligible
- Fabric Relay Allowed

---

## 13. Dynamic Role Binding

PSC ports are not permanently bound to a single role.

Conditions:

- security constraint
- topology policy
- Resolver approval
- Scheduler / RCU updates
- active transfer drain

---

## 14. Port Control Ownership

Roles of PSC modules.

- Resolver
- Scheduler
- SPU
- RCU
- TMU
- TEU
- OMU
- Telemetry / Fault Monitor

---

## 15. Behavior by Fabric State

- CALM
- WARM
- HOT
- EMERGENCY

---

## 16. Initial Port Policy Rules

Rule 1  
All ports must have exactly one Security Class.

Rule 2  
All ports must have exactly one Policy Profile.

Rule 3  
Port Role may change only under PSC control.

Rule 4  
External / Quarantined ports cannot directly obtain System privileges.

Rule 5  
Fabric-role ports require routing validation.

Rule 6  
Domain expansion must be explicitly authorized.

Rule 7  
DEGRADED / FAULT states may trigger policy downgrade.

---

## 17. Example Port Table

Port ID   Role        Mode            Security   Policy        Domain  
0x01      Compute     Endpoint        Trusted    Latency       Local Node  
0x02      Memory      Endpoint        System     Latency       Local Node  
0x03      Storage     Endpoint        User       Throughput    Cluster  
0x04      Fabric      Fabric Link     Trusted    Balanced      Cluster  
0x05      Network     Relay           External   Secure        External Boundary  
0x06      Management  Maintenance     System     Resilient     Local Node  

---

## 18. Design Significance

The PSC Port Model provides the following advantages.

1. **Device abstraction**  
Ports are no longer permanently tied to specific devices.

2. **Policy-native communication**  
Security and communication policy become part of port definition.

3. **Fabric adaptability**  
Ports can be repurposed depending on topology, workload, and fault conditions.
