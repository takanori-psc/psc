# PSC Chiplet Architecture Model v0.1

## Document Information

- Document Name   : PSC Chiplet Architecture Model
- Version         : v0.1
- Project         : PSC / Photon System Controller
- Layer           : PSC Hardware
- Document Type   : Specification
- Status          : Draft
- Author          : T. Hirose
- Created         : 2026-03
- Last Updated    : 2026-03
- Language        : English

---

## 1. Purpose

This document defines the chiplet architecture model for PSC devices.

PSC is designed as a scalable fabric device
and adopts a chiplet-based architecture
instead of a monolithic chip design.

Chiplet architecture enables:

- scalable port configurations
- multiple product variants
- flexible control-plane scaling
- improved manufacturing efficiency

---

## 2. Design Philosophy

PSC hardware follows these principles.

### 2.1 Modular Architecture

Functional units are separated into chiplets.

### 2.2 Scalable Fabric

Port count and processing capacity scale through additional chiplets.

### 2.3 Unified Device Architecture

PSC Endpoint, PSC Switch, and PSC Fabric Core share the same base architecture.

---

## 3. PSC Chiplet Structure

A PSC device package consists of multiple chiplets.

Example structure:
```
PSC Package
├ Switching Core Chiplet
├ Port Chiplet(s)
├ Telemetry / Security Chiplet
└ RISC-V Control Cluster
```
Each chiplet provides specialized functionality.

---

## 4. Chiplet Types

PSC is composed of several chiplet types.

### 4.1 Switching Core Chiplet

Responsible for fabric switching operations.

Main functions:

- fabric switching
- packet forwarding
- internal routing
- crossbar / NoC management

This chiplet forms the core of the data plane.

### 4.2 Port Chiplet

Provides fabric port interfaces.

Main functions:

- optical link control
- port buffer management
- port status monitoring
- configurable port roles
 
Ports can change roles via configuration.

Examples:

- fabric port
- endpoint port
- trusted port
- restricted port

### 4.3 Telemetry / Security Chiplet

Provides fabric monitoring and security features.

Main functions:

- fabric telemetry
- congestion monitoring
- security enforcement
- support for trust evaluation

Provides state information used by the routing pipeline.
 
### 4.4 RISC-V Control Cluster

Responsible for the PSC control plane.

Main functions:
 
- fabric initialization
- policy management
- security control
- trust management
- routing control
- telemetry aggregation
- fault management
 
The number of cores scales with the chiplet architecture.

---

## 5. Internal Interconnect

Chiplets are connected via a high-speed internal interconnect.

Examples include:

- internal NoC
- chiplet fabric links

The internal interconnect must provide low latency and high bandwidth.

---

## 6. Port Configuration Model

PSC ports are role-configurable rather than fixed-function.

Example roles:
```
Fabric Port
Endpoint Port
Storage Port
Trusted Port
External Domain Port
```

---

## 7. Product Model Scaling

PSC supports multiple product models using the same chiplet architecture.

Examples:

| Model           | Purpose                 |
| --------------- | ----------------------- |
| PSC Endpoint    | compute node connection |
| PSC Switch      | rack switch             |
| PSC Fabric Core | cluster core fabric     |

Models differ in:

- port count
- chiplet count
- control core count

---

## 8. Future Extension

Possible future extensions include:

- high-density port chiplets
- AI-assisted fabric control
- distributed control models
- advanced security features
 
