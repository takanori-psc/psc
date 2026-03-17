# PSC Concept

Japanese version: [psc_concept_ja.md](psc_concept_ja.md)

## Document Information

This document represents the finalized concept of PSC.
Early drafts are archived under 99_archive/concept/.

- Name: PSC Concept
- Version: v0.1
- Project: PSC / Photon System Controller
- Document Type: Concept
- Status: Draft
- Author: T. Hirose
- Language: English

---

## 1. Introduction

PSC (Photon System Controller) is a research project aimed at redesigning the communication structure of computer systems.

In traditional computer architectures, the CPU has served as the central component of the entire system, handling much of the following functions:

- computation
- control
- data movement

However, in modern computing environments, improving computational performance alone is no longer sufficient.  
Instead, **efficient data movement** has become a critical challenge.

PSC addresses this issue by proposing a **communication-centric computer architecture**.

---

## 2. Data Movement Crisis

In recent computer systems, computational performance continues to increase, while the **cost of data movement** is becoming a major factor limiting overall system performance.

Compared with processor performance improvements, the costs associated with:

- memory bandwidth
- device communication
- inter-node communication

are becoming increasingly significant.

This issue is often referred to as the **Data Movement Crisis**.

PSC attempts to address this challenge by redesigning the communication structure of computer systems.

PSC aims to improve data movement efficiency through approaches such as:

- communication-centric architecture design
- fabric-based data movement management
- distributed communication control

---

## 3. Communication-Centric Computing

The fundamental concept of PSC is **Communication-Centric Computing**.

This approach prioritizes communication as a central design principle of computer systems.

Traditional computer systems are typically structured as:

```
CPU
↓
Bus
↓
Device
```

PSC expands this model into a structure centered around:

```
Fabric
↓
Node
```


In this model, the communication network (Fabric) becomes the foundation of the entire system.

---

## 4. Fabric-First Architecture

PSC adopts a **Fabric-First Architecture**.

This design philosophy places the communication network at the center of the computer architecture.

In PSC, the fabric is not merely a communication path.  
Instead, it becomes a critical system component responsible for:

- data movement
- load distribution
- routing control
- congestion management

---

## 5. Everything is a Node

In PSC, all system components are treated as **nodes**.

Examples include:

- CPU
- GPU
- Memory
- Storage
- Accelerators
- Network Interfaces

All of these components are connected to the fabric as nodes.

This model improves both flexibility and scalability of system architecture.

---

## 6. Receiver-Driven Data Movement

PSC controls data transfer using a **Receiver-Driven** model.

In this communication model, the receiver initiates and controls the data transfer.

This approach enables:

- effective backpressure control
- congestion avoidance
- stable communication throughput

---

## 7. Distributed Control

PSC is designed as a **distributed control communication architecture**.

Communication control is not handled by a single centralized controller.  
Instead, multiple control modules operate cooperatively in a distributed manner.

This approach improves:

- scalability
- availability
- fault tolerance

---

## 8. Towards Large-Scale Fabric Computing

PSC is designed with future applications in mind, including:

- large-scale distributed computing
- next-generation data center architectures
- optical communication fabrics

The ultimate goal of PSC is to establish a **communication-centric computing infrastructure**.
