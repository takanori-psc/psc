# PSC Node Type Model v0.1

## Document Information

- Document Name   : PSC Node Type Model
- Version         : v0.1
- Project         : PSC / Photon System Controller
- Layer           : PSC Fabric
- Document Type   : Specification
- Status          : Draft
- Author          : T. Hirose
- Created         : 2026-03
- Last Updated    : 2026-03
- Language        : English

---

# 1. Purpose

This document defines the **Node Type Model** used within PSC Fabric.

PSC adopts a **fabric-centric distributed computer architecture**, where system components are connected to the PSC Fabric as independent nodes.

The Node Type Model defines:

- classification of node roles
- responsibilities of each node type
- relationships between nodes and PSC planes (Data / Control / Management)
- extensibility of node types

The goal of this model is to clearly establish **functional separation, control structure, and scalability** within PSC Fabric.

---

# 2. Scope

This document covers:

- logical classification of nodes within PSC Fabric
- fundamental responsibilities of node types
- relationships between node types and fabric functions

This document does **not** define:

- internal node implementation details
- hardware architecture of nodes
- detailed communication protocols between nodes

These topics are defined in separate specifications.

---

# 3. Design Principles

The PSC Node Type Model follows these design principles.

## 3.1 Role Separation

To ensure stability and scalability, PSC separates node roles into clearly defined functional categories.

## 3.2 Fabric-Centric Architecture

PSC Fabric acts as the central communication layer.  
All nodes communicate through the fabric rather than through direct system buses.

## 3.3 Distributed Autonomy

PSC Fabric follows a distributed architecture.  
Nodes operate autonomously while cooperating through the fabric.

## 3.4 Extensibility

The Node Type Model is designed to support future expansion and additional node types.

---

# 4. Node Type Overview

PSC Fabric defines the following fundamental node types.

| Node Type       | Role                               |
|-----------------|------------------------------------|
| Compute Node    | Application and compute processing |
| Memory Node     | Memory resource provider           |
| Storage Node    | Persistent storage provider        |
| Fabric Node     | Fabric packet forwarding           |
| Gateway Node    | External network connectivity      |
| Control Node    | Fabric control functions           |
| Management Node | Operational management             |

PSC architecture separates:

- **resource nodes**
- **transport nodes**
- **control nodes**
- **management nodes**

This separation enables scalable and stable operation of PSC Fabric.

---

# 5. Node Type Definitions

## 5.1 Compute Node

Compute Nodes execute applications and perform computational tasks.

Primary responsibilities:

- application execution
- data processing
- generation of PSC fabric requests
- receiving processed data

Compute Nodes access memory, storage, and accelerators through PSC Fabric.

---

## 5.2 Memory Node

Memory Nodes provide memory resources within PSC Fabric.

Primary responsibilities:

- memory allocation
- high-bandwidth data access
- low-latency memory services

Memory Nodes may operate as part of a distributed memory pool.

---

## 5.3 Storage Node

Storage Nodes provide persistent storage services.

Primary responsibilities:

- long-term data storage
- large-capacity data access
- participation in distributed storage systems

Storage Nodes may form distributed storage architectures across the fabric.

---

## 5.4 Fabric Node

Fabric Nodes maintain connectivity within PSC Fabric.

Primary responsibilities:

- packet forwarding
- route relay
- maintaining fabric connectivity
- ensuring efficient data transport

Fabric Nodes function as the network infrastructure of PSC Fabric.

---

## 5.5 Gateway Node

Gateway Nodes connect PSC Fabric to external systems or networks.

Primary responsibilities:

- external network connectivity
- protocol translation
- boundary management between PSC Fabric and other systems

Gateway Nodes serve as the boundary nodes of PSC Fabric.

---

## 5.6 Control Node

Control Nodes provide control-plane functionality for PSC Fabric.

Primary responsibilities:

- fabric state monitoring
- routing policy management
- distribution of control information
- assisting fabric state convergence

Control Nodes act as core elements of the PSC Control Plane.

---

## 5.7 Management Node

Management Nodes provide operational management capabilities.

Primary responsibilities:

- monitoring
- configuration management
- log collection
- operational control

Management Nodes form the core of the PSC Management Plane.

---

# 6. Node Type and Plane Relationship

PSC defines three primary planes.

| Plane            | Primary Node Types                            |
|------------------|-----------------------------------------------|
| Data Plane       | Compute / Memory / Storage / Fabric / Gateway |
| Control Plane    | Control Node                                  |
| Management Plane | Management Node                               |

This structure separates:

- data transport
- control logic
- operational management

Such separation improves stability and scalability.

---

# 7. Dedicated vs Combined Deployment

PSC recommends **logical separation** between Control Nodes and Management Nodes.

Reasons include:

- fault isolation
- improved security
- operational stability

In some implementations these roles may coexist on the same physical system, but the PSC architecture treats them as logically distinct roles.

---

# 8. Node Type Extensibility

The PSC Node Type Model supports future extensions.

Possible examples include:

- Accelerator Node
- Service Node
- Hybrid Node

New node types can be introduced while following PSC architectural principles.

---

# 9. Summary

The PSC Node Type Model defines the functional roles of nodes within PSC Fabric.

PSC architecture separates nodes into:

- resource providers
- transport infrastructure
- control systems
- management systems

This role separation enables PSC Fabric to achieve:

- distributed control
- high scalability
- stable operation
