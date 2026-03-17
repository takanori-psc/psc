# PSC Overview

Japanese version: [psc_overview_ja.md](psc_overview_ja.md)

## Document Information

- Name: PSC Overview
- Version: v0.1
- Project: PSC / Photon System Controller
- Document Type: Overview
- Status: Draft
- Author: T. Hirose
- Language: English

---

## 1. Overview

PSC (Photon System Controller) is a **fabric-centric communication architecture** designed to separate data movement management from the CPU in computer systems.

In traditional computer architectures, the CPU is responsible for controlling most data movement operations.

PSC redesigns this structure by delegating functions such as:

- data transfer control  
- route selection  
- congestion control  
- communication policy management  

to a **dedicated communication controller (PSC)**, enabling a scalable communication infrastructure.

PSC is not merely an interconnect.  
It aims to establish a **fabric-centric distributed computer architecture**.

In the future, PSC is envisioned as a potential foundation for large-scale distributed computing systems and next-generation data center architectures.

---

## 2. Problem

Traditional computer architectures have several structural limitations.

### CPU-Centric Communication

In many systems, control of data movement is concentrated in the CPU.

This results in:

- increased CPU overhead  
- scalability bottlenecks  
- reduced communication efficiency

### DMA Dependency

Data movement is typically handled by DMA mechanisms, which introduce several limitations:

- coarse transfer granularity  
- limited flexibility in routing control  
- difficulty handling complex communication patterns

### Data Movement Bottleneck

In modern computing systems, **data movement** is increasingly becoming a primary bottleneck, often more significant than raw computation performance.

### Scalability Limitation

CPU-centric bus architectures introduce constraints when scaling systems:

- limited connection counts  
- shared bandwidth contention  
- topology constraints

---

## 3. PSC Core Idea

PSC adopts the following design principles to address these challenges.

### Fabric-First Architecture

The communication network is designed as the **central structure of the system architecture**.

### Everything is a Node

All system components are treated as **nodes**.

Examples include:

- CPU
- GPU
- Memory
- Storage
- Accelerators
- Network Interfaces

### Receiver-Driven Transfer

Data transfer is controlled by the **receiver side**.

This enables:

- effective backpressure control  
- congestion avoidance  
- stable throughput

### Chunk-Based Transport

Data is divided into **chunks**, allowing flexible routing and transfer control.

### Policy-Aware Routing

Routing decisions consider factors such as:

- policy constraints  
- system load  
- trust levels

### Distributed Congestion Control

PSC Fabric employs **distributed congestion control mechanisms** to maintain efficient network operation.

---

## 4. PSC Architecture

A PSC-based system consists of several key components.

### Nodes

Nodes represent system components such as:

- CPU Nodes
- GPU Nodes
- Memory Nodes
- Storage Nodes
- Accelerator Nodes

### PSC Controllers

PSC Controllers manage communication between nodes.

Their responsibilities include:

- transfer control
- routing
- congestion management

### PSC Fabric

PSC Fabric is the communication network connecting nodes.

Key characteristics include:

- high bandwidth
- low latency
- multi-path communication

### Transfer Pipeline

PSC uses a pipeline-based data transfer mechanism:

- Request
- Scheduling
- Routing
- Transfer
- Completion

---

## 5. PSC Control Model

PSC consists of multiple control modules.

Major modules include:

- Resolver
- Scheduler
- SPU
- RCU
- TMU
- TEU
- OMU

These modules cooperate to perform:

- transfer control
- routing decisions
- state monitoring

---

## 6. PSC Fabric Model

PSC Fabric operates based on the following communication models:

- Fabric Domain
- Node Addressing
- Transfer Protocol
- Chunk Transport
- Multi-Path Routing

These mechanisms provide:

- high scalability
- high availability
- efficient communication

---

## 7. PSC Evolution Path

PSC is designed to evolve through several deployment phases.

### Phase 1

PCIe Bridge PSC

PSC is introduced as an extension to existing systems.

### Phase 2

Hybrid Fabric

Hybrid systems combining PCIe and PSC Fabric.

### Phase 3

Native PSC Fabric

Systems built primarily around PSC Fabric.

### Phase 4

Optical Fabric

Large-scale fabric systems based on optical communication.

---

## 8. Future Topics

Future research directions include:

- Resolver extensions
- Fabric state optimization
- automatic port role assignment
- topology adaptation

Key concepts:

- State-Driven Fabric Control
- Adaptive Fabric Topology
- Resolver-Driven Fabric Optimization

---

PSC is a research project exploring a **communication-centric computer architecture**, aiming to become a foundation for future large-scale distributed computing systems.
