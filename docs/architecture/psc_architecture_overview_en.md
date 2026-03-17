# PSC Architecture Overview

## Document Information

* Document Name: PSC Architecture Overview
* Version      : v0.1
* Project      : PSC / Photon System Controller
* Layer        : Architecture
* Status       : Draft
* Author       : T. Hirose
* Language     : English (EN)

---

## 1. Overview

This document provides an overview of the **overall architecture** of PSC (Photon System Controller).

PSC is a **fabric-centric communication architecture** that separates data movement processing from the CPU and delegates it to a dedicated fabric control processor.

PSC consists of the following components:

* PSC Node
* PSC Fabric
* Resolver
* Transfer Pipeline

---

## 2. PSC Node

A PSC Node is a communication control node connected to the PSC Fabric.

Each PSC Node includes the following core modules:

* Session Manager
* Flow Queue Manager
* Transfer Scheduler (DRR)
* Routing Engine
* Backpressure Controller
* DMA Engine
* Resolver

The PSC Node is responsible for managing data transfers between system components such as CPUs, GPUs, memory, and storage.

---

## 3. PSC Fabric

PSC Fabric is a communication network that interconnects PSC Nodes.

It provides the following characteristics:

* Optical link-based interconnect
* Cut-through forwarding
* Multi-path routing
* Adaptive congestion avoidance

The PSC Fabric enables high-speed data transfer between nodes.

---

## 4. Transfer Pipeline

Data transfer in PSC is processed through the following pipeline:

1. Transfer Session Creation
2. Chunk Segmentation
3. Flow Queue Scheduling
4. Fabric Routing
5. Receiver Reordering
6. DMA Write

PSC uses chunk-based data transfer to achieve efficient flow control and robust error recovery.

---

## 5. Resolver

The Resolver is a lightweight control module located within each PSC Node.

It observes the state of the fabric and performs arbitration such as:

* Routing decision adjustment
* Congestion mitigation
* Flow prioritization adjustment
* Exceptional condition arbitration

Rather than acting as a centralized controller, the Resolver functions as a **distributed arbitration mechanism** within the fabric.

---

## 6. Control Model

PSC Fabric operates based on a three-layer control model:

### Fast Path Control

* DRR Scheduler
* Normal Routing

### Local Protection

* Backpressure
* Flow Control

### Distributed Arbitration

* Resolver-based decision making

This structure enables PSC Fabric to achieve both high throughput and system stability.

---

## 7. Summary

PSC Architecture is designed based on the following principles:

* Fabric-centric design
* Distributed control model
* Chunk-based data transport
* Receiver-driven transfer

Unlike traditional CPU-centric architectures, PSC achieves high scalability by delegating data movement control to the fabric layer.
