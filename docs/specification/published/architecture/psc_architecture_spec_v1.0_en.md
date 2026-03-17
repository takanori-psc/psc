# PSC Architecture Specification v1.0

## Document Information

- Document Name : PSC Architecture Specification
- Version       : v1.0
- Project       : PSC / Photon System Controller
- Layer         : PSC Hardware / System Architecture
- Document Type : architecture
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-03
- Last Updated  : 2026-03
- Language      : English

---

## 1. Purpose

To decouple communication management from the CPU in personal computers,
enabling a transition toward future optical interconnects and network-based computing architectures.

---

## 2. Background

Modern personal computers are based on a CPU-centric control architecture.
All data transfers are managed by the CPU or DMA under CPU control.

However, in recent years, communication demands have increased significantly due to:

- Large-scale parallel processing by GPUs
- Widespread adoption of high-speed NVMe storage
- Continuous AI workloads
- High-speed network communication

Managing all communication through the CPU is approaching its limits in terms of efficiency and power consumption.

A new mechanism is required to offload communication management from the CPU.

---

## 3. Overview of the Solution

PSC (Photon System Controller) is a dedicated control unit responsible for managing communication within and outside the computer system.

PSC provides the following functions:

- Inter-module communication management
- Data transfer path establishment
- CPU-independent data transfer control
- Support for both electrical and optical interconnects

This allows the CPU to focus purely on computation, improving overall system efficiency and stability.

---

## 4. PSC Architecture

PSC is an independent communication control unit responsible for managing data transfers between system components such as CPU, GPU, memory, storage, and network interfaces.

### 4.1 Transfer Management Unit (TMU)

Manages transfer requests between modules and determines transfer paths based on system state and control policies.

### 4.2 Routing Control Unit (RCU)

Establishes physical and logical communication paths for both electrical and optical interconnects.

### 4.3 Transfer Execution Unit (TEU)

Executes actual data transfers based on established paths, enabling high-speed operation without CPU intervention.

### 4.4 Interconnect Interface (ICI)

Provides connectivity to:

- Electrical interconnects (e.g., PCIe)
- Optical interconnects (future support)

### 4.5 Control Interface

Receives initialization and control commands from the CPU.
Normal communication is handled autonomously by PSC.

### 4.6 Optical Monitoring Unit (OMU)

Monitors optical link health and maintains link quality.

Monitored parameters include:

- Transmit optical power (Tx)
- Receive optical power (Rx)
- Temperature
- Error statistics (BER/FEC)
- Link retraining and correction

### 4.7 Optical Link Lifecycle Management

Manages long-term degradation and lifetime of optical links.

Monitored metrics:

- Long-term Tx/Rx trends
- Laser bias current
- Temperature history
- Error statistics
- Total operating time

PSC may perform:

- Warning notifications
- Replacement recommendations
- Performance limitation or shutdown
- Failover to alternative paths

---

## 5. Relationship between CPU and PSC

In traditional architectures, the CPU manages both computation and communication.

With PSC:

CPU responsibilities:

- Execute computations
- Run applications
- Configure and control PSC

PSC responsibilities:

- Manage communication
- Execute transfers autonomously
- Stabilize routing

PSC acts as an evolution of DMA, further reducing CPU communication overhead.

---

## 6. System Architecture with PSC

Traditional model:

CPU → Controls all components

PSC model:

CPU → Compute unit
PSC → Communication controller

Components communicate via PSC instead of direct CPU control.

Benefits:

- Reduced CPU load
- Improved parallelism
- Stable routing control
- Optical interconnect readiness

---

## 7. Evolution toward Network Computing

PSC-enabled systems can operate as nodes in a distributed computing environment.

PSC manages:

- Local communication
- Inter-system communication
- External network communication

Multiple PSC systems can form a unified distributed computing platform.

---

## 8. Implementation Model

### 8.1 Expansion Card Model

- Add-on PCIe card
- Easy adoption and testing

### 8.2 Chipset Integration Model

- Lower latency
- Better system integration
- Improved power efficiency

### 8.3 CPU Integrated Model

- Maximum efficiency
- Minimal latency
- Full integration

### 8.4 Dedicated Processor Model

- Maximum flexibility
- Suitable for large-scale systems
- Optimized for distributed environments

---

## 9. System Structure Diagram

```
        CPU
         |
         | Control
         |
        PSC
   +-----+-----+-----+
   |     |     |     |
  GPU   RAM   NVMe  Network
```

---

## 10. Internal Architecture

PSC consists of multiple internal functional units that cooperate to perform communication management.

The internal architecture follows a layered execution pipeline
from control input to physical data transfer.

Figure 2 illustrates the conceptual internal structure of PSC.

### 10.1 Core Internal Units and Roles

The following units work together to form the communication control functionality of PSC.

Transfer Management Unit (TMU):
Receives transfer requests and manages transfer operations.
Responsible for scheduling and prioritization of data transfers.

Routing Control Unit (RCU):
Determines and configures communication paths.
Controls routing across both electrical and optical interconnects.

Transfer Execution Unit (TEU):
Executes actual data transfers.
Provides high-efficiency and low-latency data movement.

Interconnect Interface (ICI):
Provides physical connectivity to external interconnects.
Supports PCIe and future optical interconnect technologies.

Control Interface (CI):
Handles control communication with the CPU.
Responsible for initialization, monitoring, and control command handling.

---

### Figure 2: PSC Internal Architecture (Conceptual)

```
              Control Interface (CI)
                     │
                     │
                     ▼
                ┌─────────┐
                │   TMU   │
                └────┬────┘
                     │
                ┌────▼────┐
                │   RCU   │
                └────┬────┘
                     │
                ┌────▼────┐
                │   TEU   │
                └────┬────┘
                     │
                ┌────▼────┐
                │   ICI   │
                └─────────┘
```

---

## 11. Operational Flow

1. Request received via ICI(initiated by CPU or device)
2. TMU schedules transfer
3. RCU determines route
4. TEU executes transfer
5. OMU monitors and corrects
6. Completion notification

---

## 12. Fault Detection and Failover

PSC detects failures and performs:

- Link retraining
- Output correction
- Path switching
- Notification

---

## 13. Design Goals

- Full separation of communication from CPU
- High efficiency and low latency
- Optical interconnect support
- High reliability
- Support for distributed computing

---

## 14. State Model

- Initialization
- Idle
- Transfer
- Monitoring
- Recovery
- Fault

---

## 15. Future Extensions

PSC is designed to support future:

- Optical CPUs
- Optical memory
- Fully optical interconnect systems

---

End of v1.0
