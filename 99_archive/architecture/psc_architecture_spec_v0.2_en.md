# PSC Architecture Specification

This document is an archived version.
The official specification is:
docs/specification/published/architecture/psc_architecture_spec_v1.0_en.md

Photon System Controller (PSC)

Version: 0.2  
Status: Draft  
Author: T. Hirose  

# 1. Overview

## 1.1 Purpose

Photon System Controller (PSC) is a communication and fabric control architecture designed to decouple data movement management from the central processing unit (CPU).

Modern computing systems increasingly rely on high-bandwidth data transfers between heterogeneous components such as GPUs, storage devices, network interfaces, and accelerators. In conventional architectures, the CPU or CPU-managed DMA engines are responsible for coordinating most data transfers.

As system complexity and bandwidth requirements grow, this centralized model becomes increasingly inefficient and places unnecessary control overhead on the CPU.

PSC introduces a dedicated fabric controller responsible for managing communication between system nodes. By delegating transfer coordination and routing to PSC, the CPU is relieved from a significant portion of communication management tasks.

## 1.2 Concept

PSC treats all system components as nodes connected through a communication fabric.

Examples of nodes include:

- CPU nodes
- GPU nodes
- storage nodes
- network nodes
- accelerator nodes
- PSC nodes (fabric controller nodes)

Data transfers occur directly between nodes through the PSC-managed fabric without requiring CPU intervention for each operation.

PSC operates as both:

- a high-speed switching fabric
- a distributed transfer control system

PSC systems may operate with multiple communication domains,
including the native PSC Fabric domain and compatibility domains
such as Optical PCIe.

The PSC Fabric domain provides the primary communication
environment for node-to-node transfers, while compatibility
domains allow integration with existing device ecosystems.

## 1.3 Design Goals

PSC is designed with the following goals:

- Reduce CPU involvement in high-volume data movement
- Provide scalable communication between heterogeneous system components
- Support multi-path and striped data transfers
- Enable optical interconnect integration
- Allow gradual migration from existing electrical bus architectures
- Provide a foundation for large-scale compute fabrics

## 1.4 Architectural Scope

The PSC architecture defines:

- fabric addressing and node identification
- node discovery and boot procedures
- transfer protocol and flow control
- congestion management and scheduling
- internal PSC module architecture
- scalable fabric topology models

These components together form a complete communication fabric architecture capable of supporting both single-system deployments and large-scale distributed fabrics.

## 1.5 Evolution Path

PSC is designed to evolve through several implementation phases.

Initially, PSC can operate as a bridge-based fabric controller integrated into existing PCIe-based systems. Over time, systems may transition toward hybrid and eventually fully optical node environments.

This phased approach allows PSC technology to be introduced incrementally while maintaining compatibility with current computing platforms.

# 2. Design Philosophy

PSC is designed as a fabric-oriented communication architecture.  
Instead of extending traditional bus-based models, PSC adopts a distributed fabric model where communication is treated as a first-class system function.

The design philosophy of PSC is guided by several core principles.

## 2.1 Everything is a Node

In PSC architecture, all system participants are treated as nodes connected to the fabric.

Examples include:

- CPU nodes
- GPU nodes
- storage nodes
- network nodes
- accelerator nodes
- PSC nodes

PSC does not assign permanent hierarchical roles to specific device classes.  
From the perspective of the fabric, communication occurs between nodes regardless of their internal function.

This node-centric model allows PSC to support heterogeneous systems without requiring specialized connection rules for each device type.

## 2.2 Fabric-First Architecture

Traditional computer systems treat communication infrastructure as a peripheral component attached to the CPU.

PSC reverses this relationship.

Instead of the CPU coordinating communication,
the fabric itself becomes responsible for system-wide data movement.

In PSC systems, the communication fabric is treated as a primary architectural layer responsible for coordinating system-wide data movement.

The PSC fabric performs the following functions:

- routing of transfers between nodes
- congestion management
- transfer admission control
- bandwidth utilization optimization

By offloading these responsibilities from the CPU, PSC allows compute nodes to focus on computation rather than data movement coordination.

## 2.3 Receiver-Driven Flow Control

PSC adopts a receiver-driven communication model.

Before data transfer begins, the receiving node must confirm that sufficient resources are available to accept the incoming transfer.

This approach prevents buffer overflow and reduces the need for large-scale retransmission.

Transfers therefore follow a reservation-based model:

1. Transfer request
2. Receiver readiness confirmation
3. Transfer grant
4. Data transmission
5. Completion acknowledgement

This mechanism improves stability under high traffic conditions.

## 2.4 Chunk-Based Transport Model

PSC internally divides logical transfers into fixed-size chunks.

This design enables:

- efficient scheduling
- multi-path routing
- striped transfers
- localized retransmission

Chunk-based transport allows large transfers to progress incrementally even when parts of the fabric experience temporary congestion.

## 2.5 Distributed Congestion Awareness

PSC does not rely on a centralized congestion control authority.

Instead, each PSC monitors its local environment and adjusts behavior according to fabric conditions.

PSC uses a multi-level state model:

- CALM
- WARM
- HOT
- EMERGENCY

These states guide scheduling behavior and transfer admission policies.

Local stabilization is prioritized to prevent congestion from propagating across the fabric.

## 2.6 Local-First Stability

PSC prioritizes local stability over global optimization.

When congestion or failure occurs, PSC attempts to stabilize traffic locally before attempting wider fabric adjustments.

This strategy reduces the risk of global instability and allows the system to remain operational even during partial failures.

## 2.7 Incremental Deployment

PSC is designed to be deployable in stages.

The architecture supports gradual transition from existing electrical bus-based systems toward fully optical fabric-based systems.

This approach allows PSC technology to be introduced without requiring immediate replacement of existing hardware ecosystems.

# 3. Terminology and Naming Conventions

This section defines the core terminology used throughout the PSC architecture specification.

Consistent terminology is required to ensure that architectural components, protocols, and system behaviors are interpreted unambiguously.


## 3.1 Node

A Node is any computational, storage, or communication entity connected to the PSC fabric.

Examples include:

- CPU nodes
- GPU nodes
- storage nodes
- network nodes
- accelerator nodes
- PSC nodes

From the perspective of the fabric, all participants are treated as nodes capable of sending or receiving transfers.


## 3.2 PSC Node

A PSC node is a fabric controller node responsible for managing communication within the PSC fabric.

PSC nodes perform the following functions:

- routing of transfers between nodes
- congestion monitoring
- transfer scheduling
- flow control enforcement
- fabric topology participation

PSC nodes therefore serve as both communication switches and transfer control agents.


## 3.3 Fabric

Fabric refers to the communication network formed by PSC nodes and their connected links.

The PSC fabric provides:

- node-to-node communication
- routing of transfers
- multi-path data movement
- congestion-aware scheduling

The fabric is designed to operate independently of any specific compute node.


## 3.4 Port

A Port is a physical or logical interface through which a PSC node connects to another node or PSC.

Ports are used to establish links within the fabric.

Each PSC node exposes multiple ports which may be connected to:

- compute nodes
- storage nodes
- network nodes
- other PSC nodes


## 3.5 Link

A Link is the physical or logical communication channel between two ports.

Links may be implemented using:

- electrical interconnects
- optical interconnects

Links are assumed to operate as full-duplex communication channels.


## 3.6 Transfer

A Transfer represents a logical data movement operation between two nodes.

Transfers may involve large amounts of data and are therefore internally segmented for efficient transport across the fabric.


## 3.7 Chunk

A Chunk is the smallest transport unit used internally by the PSC fabric.

Large transfers are divided into multiple chunks to allow:

- scheduling flexibility
- multi-path routing
- striped transmission
- localized retransmission


## 3.8 Route

A Route defines the path taken by a transfer across the PSC fabric.

Routes may involve multiple PSC nodes and links.

Multiple routes may exist between the same pair of nodes.


## 3.9 Credit

Credit represents permission to transmit data toward a receiving node.

PSC uses credit-based flow control to prevent receiver buffer overflow and maintain stable fabric operation.


## 3.10 Fabric Domain

A Fabric Domain is a group of PSC nodes operating within the same addressing and routing environment.

Within a domain, PSC nodes share compatible routing and identification mechanisms.


## 3.11 Node Address

A Node Address uniquely identifies a node within the PSC fabric.

Node addressing may include identifiers for:

- fabric domain
- PSC node
- local node


## 3.12 Naming Conventions

The following naming conventions are used in this specification.

### Node Types

Node types are written in lowercase with descriptive prefixes.

Examples:

- cpu node
- gpu node
- storage node
- network node
- accelerator node
- psc node


### PSC Modules

Internal PSC modules use capitalized identifiers.

Examples:

- TMU (Transfer Management Unit)
- RCU (Routing Control Unit)
- Scheduler
- Resolver


### Protocol Messages

Protocol message identifiers are written in uppercase.

Examples:

- TRANSFER_REQUEST
- TRANSFER_GRANT
- DATA_CHUNK
- TRANSFER_COMPLETE

# 4. Port Architecture

The PSC port architecture defines how nodes and PSC controllers connect to the fabric.

PSC uses a unified port model in which all external connections are treated as fabric ports.  
Ports do not have permanent device-specific roles. Instead, any port may connect to any type of node or PSC controller.

This approach allows PSC systems to support flexible topologies and heterogeneous device environments.


## 4.1 Unified Port Model

PSC adopts a unified port model.

All ports are treated as fabric ports capable of connecting to:

- compute nodes
- storage nodes
- network nodes
- accelerator nodes
- other PSC nodes

Ports are therefore not permanently classified by device type.

This design simplifies the hardware interface model and enables flexible system configuration.


## 4.2 Node Perspective

From the perspective of the PSC fabric, all devices are treated as nodes.

Connections between nodes occur through PSC ports.

Example connections include:

- PSC → CPU node
- PSC → GPU node
- PSC → storage node
- PSC → network node
- PSC → PSC node

This model ensures that the PSC fabric does not impose rigid hierarchy between device classes.


## 4.3 Port Count

The baseline PSC architecture defines a total of **32 ports** per PSC node.

These ports may be used for:

- local node connections
- PSC fabric expansion
- external network connections

The 32-port structure provides sufficient flexibility for both local system integration and larger PSC fabric topologies.


## 4.4 Active and Reserved Ports

Although the architecture defines 32 ports, not all ports must be active in early implementations.

The recommended baseline configuration is:

- 16 active ports
- 16 reserved ports

Reserved ports are intended for:

- future hardware expansion
- fabric growth
- higher bandwidth configurations

This approach allows PSC systems to evolve without redesigning the base architecture.


## 4.5 Fabric Expansion

Ports may be used to connect PSC nodes to form a larger PSC fabric.

When PSC nodes connect to one another, the fabric topology may form:

- partial mesh networks
- hierarchical topologies
- extended PSC clusters

Multiple PSC-to-PSC links may also be used to increase bandwidth between fabric segments.


## 4.6 Port Symmetry

PSC ports are symmetric from the architectural perspective.

This means:

- any port may connect to any node type
- no port is permanently assigned to a specific device class
- system configuration determines port usage

Port symmetry simplifies both hardware design and system integration.


## 4.7 Future Optical Integration

PSC ports are designed to support both electrical and optical link implementations.

Early implementations may use electrical interconnects for compatibility with existing systems.

Future PSC systems may transition toward optical link technologies to achieve significantly higher bandwidth and longer communication distances.


## 4.8 Fabric Communication Domains

PSC systems may operate with multiple communication domains.

Two primary communication domains are defined.

### Optical PCIe Domain

A compatibility domain in which PCIe protocol traffic may be transported
over optical links.

This domain allows PSC systems to maintain compatibility with existing
PCIe-based devices such as GPUs and NVMe storage.

### PSC Fabric Domain

The native PSC communication environment used for node-to-node transfers
within the PSC fabric.

This domain supports PSC routing, transfer control, and fabric-level
scheduling mechanisms.

## 4.9 Port Policy Model

PSC ports support logical policy configuration.

Although ports share a unified physical interface, their behavior may
be controlled through policy attributes.

### Port Mode

Port Mode defines the communication mode used by the port.

Examples:

- PSC_NATIVE
- PCIe_TUNNEL
- MANAGEMENT

### Security Class

Security Class defines the trust level assigned to the port.

Examples:

- LOCAL_TRUSTED
- FABRIC_TRUSTED
- EXTERNAL

### Policy Profile

Policy Profile defines communication rules applied to the port.

Possible policies include:

- routing restrictions
- bandwidth limitations
- transfer admission rules
- visibility control


# 5. Node Model and Addressing

The PSC architecture defines a hierarchical node identification and addressing model that allows PSC fabrics to scale from single-system deployments to large multi-PSC environments.

Nodes are identified using a layered addressing structure that separates global PSC identity from local fabric addressing.


## 5.1 Node Model

All devices connected to the PSC fabric are treated as nodes.

Examples include:

- cpu nodes
- gpu nodes
- storage nodes
- network nodes
- accelerator nodes
- psc nodes

From the perspective of the fabric, nodes may act as either transfer sources or transfer destinations.

PSC nodes additionally act as fabric controllers responsible for routing and transfer coordination.


## 5.2 PSC Unique Identifier (PSC UID)

Each PSC controller possesses a globally unique identifier called the **PSC UID**.

The PSC UID is defined as a **128-bit identifier**.

The PSC UID serves the following purposes:

- global identification of PSC controllers
- prevention of identifier collisions
- long-term system identification across fabrics

PSC UID values are intended to be permanently assigned to each PSC controller instance.


## 5.3 PSC Fabric Identifier (PSC ID)

Within a PSC fabric domain, controllers are also assigned a shorter identifier known as the **PSC ID**.

The PSC ID is defined as a **16-bit identifier**.

The PSC ID is used for:

- routing within a fabric domain
- efficient packet header representation
- local PSC addressing

PSC IDs are not required to be globally unique and are only required to be unique within a single fabric domain.


## 5.4 Fabric Domain

A Fabric Domain represents a group of PSC nodes participating in the same routing and addressing environment.

Within a fabric domain:

- PSC IDs must be unique
- routing information is shared among PSC controllers
- node discovery operates within the domain

Multiple fabric domains may exist and may be interconnected through gateway PSC nodes or bridge mechanisms.


## 5.5 Local Node Identifier (Node ID)

Each PSC controller assigns identifiers to nodes connected to its local ports.

This identifier is referred to as the **Node ID**.

The Node ID is unique within the scope of a single PSC controller.

The Node ID is used to identify:

- compute nodes
- storage nodes
- network nodes
- accelerator nodes

connected to that PSC.


## 5.6 Hierarchical Address Structure

PSC uses a hierarchical addressing structure composed of three components:

- Fabric Domain Identifier
- PSC Identifier
- Local Node Identifier

Conceptually:

Fabric Domain → PSC → Node


## 5.7 Node Address Representation

A full node address may therefore be expressed as:

(Fabric Domain ID, PSC ID, Node ID)

Example:

(Fabric 1, PSC 4, Node 3)

This hierarchical address allows the PSC architecture to scale across multiple controllers while keeping routing operations efficient.


## 5.8 Address Resolution

Address resolution within the PSC fabric allows nodes to locate the destination PSC responsible for a given Node ID.

PSC controllers maintain routing knowledge of other PSC nodes within the same fabric domain.

Once the destination PSC is identified, the transfer is routed through the PSC fabric to reach the appropriate controller and its associated local node.

# 6. Boot and Node Discovery

PSC fabrics must support automatic initialization and discovery of both local nodes and neighboring PSC controllers.

This section defines the procedures used to establish fabric connectivity during system startup.


## 6.1 PSC Boot Sequence

When a PSC controller powers on, it performs the following initialization steps:

1. Hardware initialization
2. Port status detection
3. PSC UID verification
4. Fabric domain initialization
5. Neighbor discovery

During this phase, the PSC prepares its routing and fabric management subsystems.


## 6.2 Local Node Discovery

After hardware initialization, the PSC scans its ports to detect connected local nodes.

Detected devices may include:

- cpu nodes
- gpu nodes
- storage nodes
- network nodes
- accelerator nodes

Each detected node is assigned a **Node ID** within the scope of that PSC controller.

Node discovery may use link-level identification mechanisms depending on the physical interface implementation.


## 6.3 PSC Neighbor Discovery

PSC controllers also detect other PSC controllers connected to their ports.

When a PSC-to-PSC link is established, the controllers exchange the following information:

- PSC UID
- PSC ID
- fabric domain identifier
- link capabilities

This process allows PSC controllers to identify neighboring fabric participants.


## 6.4 Fabric Formation

After neighbor discovery completes, PSC controllers begin constructing a fabric topology map.

This topology map includes:

- reachable PSC nodes
- available links
- link capabilities
- path distances

The fabric topology map is used by the routing subsystem to determine viable transfer routes.


## 6.5 Node Registration

Once nodes and PSC controllers have been discovered, the PSC registers local nodes within the fabric domain.

Node registration associates the following information:

- Node ID
- owning PSC ID
- link port
- node capabilities

This information allows the fabric to correctly route transfers toward the destination node.


## 6.6 Routing Initialization

After node discovery and registration complete, the PSC routing subsystem initializes routing tables.

Routing initialization determines:

- reachable PSC nodes
- preferred routes
- alternative routes
- fabric distance metrics

This routing information enables the PSC fabric to begin forwarding transfers between nodes.


## 6.7 Dynamic Fabric Updates

PSC fabrics may experience topology changes due to:

- node attachment
- node removal
- PSC addition
- link failure

When such changes occur, PSC controllers update their topology maps and routing tables accordingly.

This ensures that the PSC fabric remains operational and adapts to evolving system configurations.

# 7. Transfer Protocol

PSC fabrics use a reservation-based transfer protocol designed to ensure reliable and congestion-aware communication between nodes.

Transfers are coordinated through PSC controllers before data transmission begins. This prevents buffer overflow and ensures that receiving nodes are prepared to accept incoming data.


## 7.1 Transfer Model

Data movement within the PSC fabric follows a controlled transfer sequence.

A typical transfer proceeds through the following stages:

1. TRANSFER_REQUEST
2. Transfer evaluation
3. TRANSFER_GRANT
4. DATA_CHUNK transmission
5. TRANSFER_COMPLETE

This staged process ensures that transfers only begin when both sender and receiver are ready.


## 7.2 TRANSFER_REQUEST

A TRANSFER_REQUEST message is issued by the source node (or its associated PSC) to initiate a data transfer.

The request includes information such as:

- source node address
- destination node address
- requested transfer size
- transfer priority
- optional capability flags

The request is forwarded through the PSC fabric until it reaches the destination PSC responsible for the target node.


## 7.3 Transfer Evaluation

Upon receiving a TRANSFER_REQUEST, the destination PSC evaluates whether the receiving node can accept the transfer.

The evaluation considers:

- available receive buffers
- current fabric congestion
- node readiness
- scheduling policies

If the destination node cannot accept the transfer immediately, the request may be queued or rejected.


## 7.4 TRANSFER_GRANT

If the destination node confirms readiness, the destination PSC sends a TRANSFER_GRANT message back to the source.

The grant message authorizes the sender to begin transmitting data.

The grant may include:

- maximum chunk size
- permitted transmission rate
- route information
- credit allocation

This mechanism implements receiver-driven flow control.


## 7.5 DATA_CHUNK Transmission

After receiving TRANSFER_GRANT, the sender begins transmitting data in chunk units.

Each DATA_CHUNK represents a fixed-size data segment defined by the PSC transport model.

Chunk-based transport allows:

- flexible scheduling
- multi-path routing
- congestion-aware forwarding
- partial retransmission when required


## 7.6 TRANSFER_COMPLETE

After all chunks have been successfully transmitted, the sender issues a TRANSFER_COMPLETE message.

This message indicates that the logical transfer operation has finished.

The receiving PSC confirms completion and releases any resources reserved for the transfer.


## 7.7 TRANSFER_ABORT

Transfers may be aborted under exceptional conditions such as:

- node failure
- link failure
- congestion escalation
- timeout conditions

In such cases, a TRANSFER_ABORT message is issued to terminate the transfer and release reserved resources.


## 7.8 Multi-Path Transfers

PSC fabrics support routing transfers across multiple paths.

Large transfers may be distributed across multiple routes to improve bandwidth utilization and reduce congestion.

Chunk-based transport enables flexible multi-path distribution without requiring application-level coordination.


## 7.9 Transfer Reliability

PSC fabrics ensure transfer reliability through a combination of mechanisms:

- credit-based flow control
- receiver-driven transfer authorization
- chunk-level retransmission capability
- route adaptation under congestion conditions

These mechanisms allow PSC fabrics to maintain stable operation even under heavy system load.

# 8. Chunk and Flow Control

PSC fabrics implement a chunk-based transport model combined with credit-based flow control to ensure stable and efficient data movement across the fabric.

These mechanisms allow PSC systems to maintain high throughput while preventing receiver buffer overflow and limiting congestion propagation.


## 8.1 Chunk Structure

All data transfers in PSC are divided into fixed-size transport units called **Chunks**.

A Chunk represents the smallest unit of transmission across the PSC fabric.

Chunk-based transport enables:

- incremental transfer progress
- flexible scheduling
- multi-path distribution
- localized retransmission

The chunk size is implementation dependent but should remain constant within a fabric environment.


## 8.2 Chunk Size

The PSC specification does not mandate a single fixed chunk size.

However, recommended ranges include:

- 4 KB
- 8 KB
- 16 KB
- 64 KB

Implementations may select a chunk size based on:

- fabric latency
- link bandwidth
- buffering capabilities

The chunk size should be large enough to minimize protocol overhead while remaining small enough to allow efficient scheduling.


## 8.3 Credit-Based Flow Control

PSC uses credit-based flow control to regulate the transmission of data chunks.

Each receiving node advertises available buffer capacity in the form of **credits**.

Each credit represents permission to transmit a defined amount of data.

Senders must possess sufficient credits before transmitting data chunks.


## 8.4 Credit Allocation

Credits are allocated by the receiving PSC or receiving node.

Credit allocation may depend on:

- available receive buffer space
- node processing capacity
- congestion state
- scheduling policies

Credits may be dynamically adjusted as system conditions change.


## 8.5 Credit Consumption

Each transmitted chunk consumes a corresponding amount of credit.

When a chunk is successfully processed by the receiving node, the receiver may return credits to the sender.

This mechanism allows continuous streaming transfers while maintaining buffer safety.


## 8.6 Flow Control Window

PSC implementations may optionally use a flow control window to allow multiple chunks to be in flight simultaneously.

The flow control window determines how many chunks may be transmitted before additional credit updates are required.

A larger window allows higher throughput but requires larger buffering capacity.


## 8.7 Congestion Interaction

Credit-based flow control interacts with PSC congestion management mechanisms.

When congestion states escalate (for example from CALM to WARM or HOT), the system may:

- reduce credit issuance
- limit transfer admission
- prioritize critical transfers

These adjustments help prevent congestion from spreading across the fabric.


## 8.8 Retransmission

If a chunk transmission fails due to link errors or path failure, PSC may retransmit only the affected chunks.

Chunk-level retransmission improves efficiency compared to retransmitting entire transfers.


## 8.9 Adaptive Flow Control

PSC implementations may dynamically adjust flow control behavior based on system conditions.

Possible adjustments include:

- credit rate limiting
- dynamic chunk pacing
- congestion-aware scheduling

Adaptive control allows PSC fabrics to maintain stability across a wide range of workloads.

# 9. Scheduler and Resolver Interaction

PSC fabrics rely on coordinated interaction between scheduling mechanisms and fabric state evaluation in order to maintain stable operation under varying traffic conditions.

Two key components participate in this process:

- Scheduler
- Resolver

The Scheduler is responsible for selecting transfers to execute, while the Resolver evaluates global or semi-global fabric conditions and may adjust scheduling behavior when instability is detected.


## 9.1 Scheduler Role

The Scheduler is responsible for selecting which transfers may proceed through the PSC fabric.

Scheduler responsibilities include:

- selecting transfers from request queues
- allocating available link bandwidth
- balancing traffic across multiple routes
- prioritizing urgent or latency-sensitive transfers

The Scheduler operates continuously and makes decisions based primarily on local information available at the PSC node.


## 9.2 Resolver Role

The Resolver acts as a supervisory control component responsible for evaluating broader fabric conditions.

The Resolver may:

- monitor congestion states
- detect abnormal traffic patterns
- recommend routing adjustments
- limit or throttle transfers when instability occurs

Unlike the Scheduler, the Resolver does not directly execute transfers but instead influences scheduling behavior through policy adjustments.


## 9.3 Fabric State Model

PSC fabrics maintain a multi-level operational state model representing current congestion conditions.

The defined states are:

- CALM
- WARM
- HOT
- EMERGENCY

These states guide scheduling policies and transfer admission behavior.


## 9.4 CALM State

CALM represents normal operating conditions.

Characteristics:

- low congestion
- stable routing
- normal credit availability

Scheduler behavior in CALM state:

- maximize throughput
- allow multi-path transfers
- maintain high link utilization


## 9.5 WARM State

WARM indicates early signs of congestion or resource pressure.

Characteristics:

- localized congestion
- reduced credit availability
- increased queue depth

Scheduler adjustments in WARM state:

- moderate transfer admission
- prefer shorter routes
- reduce aggressive striping


## 9.6 HOT State

HOT represents significant congestion within part of the fabric.

Characteristics:

- persistent queue buildup
- reduced routing flexibility
- elevated packet latency

Scheduler adjustments in HOT state:

- restrict new transfer admission
- prioritize critical transfers
- reduce multi-path traffic dispersion


## 9.7 EMERGENCY State

EMERGENCY represents severe congestion or partial fabric instability.

Characteristics:

- buffer exhaustion risk
- routing collapse risk
- sustained traffic overload

Scheduler behavior in EMERGENCY state:

- temporarily halt non-critical transfers
- prioritize recovery traffic
- stabilize local links


## 9.8 Resolver Influence

The Resolver may adjust Scheduler behavior by:

- modifying transfer admission thresholds
- adjusting credit policies
- recommending route restrictions
- triggering congestion mitigation policies

These adjustments help stabilize the fabric before congestion spreads further.


## 9.9 Local-First Stabilization

PSC prioritizes stabilizing congestion locally before applying broader fabric-wide changes.

When instability is detected, PSC controllers attempt to:

- reduce traffic entering the affected region
- reroute transfers where possible
- temporarily slow transfer admission

This approach minimizes the risk of cascading congestion across the entire fabric.


## 9.10 Adaptive Scheduling

PSC scheduling behavior may dynamically adapt based on:

- congestion state
- credit availability
- link utilization
- transfer priority

Adaptive scheduling allows PSC fabrics to maintain high performance during normal operation while preserving stability during heavy load.

# 10. PSC Internal Architecture

This section describes the internal functional architecture of a PSC controller.

PSC controllers consist of several specialized modules responsible for routing, transfer management, execution, monitoring, and fabric control.

These modules cooperate to maintain stable and efficient operation of the PSC fabric.


## 10.1 Architectural Overview

A PSC controller is composed of several functional subsystems.

Major internal components include:

- Routing Control Unit (RCU)
- Transfer Management Unit (TMU)
- Transfer Execution Unit (TEU)
- Optical Monitoring Unit (OMU)
- Scheduler
- Resolver
- Security Policy Unit (SPU)

Each module performs a specialized role within the PSC controller.


## 10.2 Routing Control Unit (RCU)

The Routing Control Unit is responsible for determining transfer routes across the PSC fabric.

RCU responsibilities include:

- maintaining routing tables
- selecting paths between PSC nodes
- supporting multi-path routing
- updating routes when topology changes occur

RCU operates based on topology information gathered during fabric discovery and updated dynamically as the system evolves.


## 10.3 Transfer Management Unit (TMU)

The Transfer Management Unit manages transfer requests and resource allocation.

TMU responsibilities include:

- handling incoming TRANSFER_REQUEST messages
- performing transfer admission control
- allocating transfer resources
- coordinating with Scheduler and Resolver

TMU acts as the coordination layer between routing decisions and transfer execution.


## 10.4 Transfer Execution Unit (TEU)

The Transfer Execution Unit is responsible for the actual movement of data chunks across the fabric.

TEU responsibilities include:

- transmitting DATA_CHUNK units
- receiving incoming chunks
- performing chunk-level retransmission
- managing link-level buffering

TEU interacts closely with the port interfaces and link hardware.


## 10.5 Optical Monitoring Unit (OMU)

The Optical Monitoring Unit monitors the health and performance of physical links.

OMU responsibilities include:

- monitoring link signal quality
- detecting link degradation
- reporting link failure events
- providing telemetry for congestion analysis

Although named for optical monitoring, OMU may also monitor electrical links in early PSC implementations.


## 10.6 Scheduler

The Scheduler selects which transfers may proceed through the PSC fabric.

Scheduler responsibilities include:

- selecting transfers from request queues
- allocating bandwidth across links
- balancing load across available routes
- applying priority policies

The Scheduler operates continuously and adapts behavior based on congestion state.


## 10.7 Resolver

The Resolver evaluates broader fabric conditions and may influence scheduling behavior.

Resolver responsibilities include:

- monitoring congestion states
- detecting abnormal traffic patterns
- recommending policy adjustments
- assisting in congestion mitigation

Resolver operates as a supervisory system that helps maintain long-term fabric stability.


## 10.8 Security Policy Unit (SPU)

The Security Policy Unit (SPU) is responsible for enforcing security
policies within the PSC controller.

The SPU performs policy validation before routing and scheduling
decisions are executed.

Responsibilities include:

- port security classification
- domain isolation enforcement
- transfer authorization checks
- security policy evaluation


## 10.9 Module Interaction

PSC internal modules cooperate through a layered control structure.

Typical interaction flow includes:

1. Resolver evaluates fabric conditions
2. Scheduler selects transfer candidates
3. SPU validates security policies
4. RCU determines possible routes
5. TMU manages transfer resources
6. TEU performs data transmission
7. OMU monitors link health

This layered structure allows PSC controllers to manage both local transfers and global fabric conditions effectively.


## 10.10 Scalability

PSC internal modules are designed to scale with increasing fabric size and traffic volume.

Possible scalability mechanisms include:

- parallel routing engines
- distributed scheduling pipelines
- multi-queue transfer management
- hardware-assisted congestion monitoring

These capabilities allow PSC controllers to support both small-scale systems and large distributed fabrics.

PSC Transfer Pipeline

Node Request
     │
     ▼
+------------+
|  Resolver  |
+------------+
     │
     ▼
+-------------+
|  Scheduler  |
+-------------+
     │
     ▼
+----------------------+
| Security Policy Unit |
|        (SPU)         |
+----------------------+
     │
     ▼
+----------------------+
| Routing Control Unit |
|        (RCU)         |
+----------------------+
     │
     ▼
+----------------------+
| Transfer Management  |
|        Unit (TMU)    |
+----------------------+
     │
     ▼
+----------------------+
| Transfer Execution   |
|        Unit (TEU)    |
+----------------------+
     │
     ▼
+----------------------+
| PSC Fabric Switching |
|        Core          |
+----------------------+
     │
     ▼
        PSC Fabric
        

# 11. Fabric Topology

PSC fabrics are designed to support flexible network topologies that can scale from small single-system deployments to large multi-controller environments.

Topology design influences routing efficiency, fault tolerance, and system scalability.


## 11.1 Topology Flexibility

PSC fabrics do not enforce a single mandatory topology.

Instead, PSC supports multiple topology structures depending on system scale and deployment requirements.

Possible PSC fabric structures include:

- single-controller systems
- multi-PSC local fabrics
- partial mesh networks
- hierarchical fabrics
- extended PSC clusters


## 11.2 Single PSC Systems

In the simplest deployment model, a single PSC controller connects directly to system nodes.

Example configuration:

- PSC → CPU node
- PSC → GPU node
- PSC → storage node
- PSC → network node

This configuration is suitable for single-machine systems or workstation-class environments.


## 11.3 Multi-PSC Fabric

Multiple PSC controllers may connect together to form a PSC fabric.

PSC-to-PSC links allow controllers to cooperate in routing and transfer management.

Benefits of multi-PSC fabrics include:

- expanded port capacity
- distributed routing
- increased bandwidth
- improved fault tolerance


## 11.4 Partial Mesh Topology

PSC fabrics commonly use a **partial mesh topology**.

In a partial mesh, each PSC connects to several other PSC nodes, but not necessarily all of them.

This approach provides:

- good routing flexibility
- moderate hardware complexity
- scalable expansion capability

Partial mesh networks balance performance and implementation cost.


## 11.5 Hierarchical Fabrics

Large PSC deployments may use hierarchical topology structures.

Example structure:

- local PSC clusters
- aggregation PSC nodes
- higher-level PSC fabric layers

Hierarchical designs improve scalability when large numbers of PSC nodes are deployed.


## 11.6 Multi-Link Connections

PSC nodes may establish multiple links between the same pair of controllers.

Multi-link connections allow:

- increased aggregate bandwidth
- redundancy in case of link failure
- improved load balancing

Routing systems may distribute traffic across these links dynamically.


## 11.7 Fault Tolerance

PSC fabrics are designed to tolerate link and node failures.

If a link fails:

- routing tables are updated
- alternate routes are selected
- transfers may be rerouted

This allows PSC fabrics to continue operating even when parts of the network become unavailable.


## 11.8 Fabric Expansion

PSC fabrics can grow incrementally by attaching additional PSC controllers.

When a new PSC node joins the fabric:

1. link discovery occurs
2. topology maps are updated
3. routing tables are recalculated

This incremental expansion model allows PSC fabrics to scale without requiring full system redesign.


## 11.9 Optical Fabric Potential

PSC fabrics are designed with future optical interconnect integration in mind.

Optical links enable:

- significantly higher bandwidth
- longer communication distances
- improved energy efficiency

As optical devices become more common, PSC fabrics may transition toward fully optical node environments.

# 12. Implementation Phases

PSC architecture is designed to support gradual adoption rather than requiring an immediate transition to a completely new system model.

This phased approach allows PSC technology to integrate with existing computing platforms while enabling long-term migration toward fully fabric-based systems.


## 12.1 Phase 1 — Bridge-Based PSC

The initial deployment phase introduces PSC as a fabric controller connected to existing systems.

In this phase:

- PSC may appear as a PCIe-attached controller
- traditional devices remain electrically connected
- PSC manages transfers between selected devices

This configuration allows PSC to offload some data movement tasks while maintaining compatibility with existing hardware ecosystems.


## 12.2 Phase 2 — Hybrid Fabric Systems

In the hybrid phase, PSC begins to operate as a central communication fabric within the system.

Characteristics include:

- multiple PSC controllers forming a local fabric
- mixed electrical and optical links
- partial migration of devices to PSC-managed communication

Some devices may still rely on traditional bus-based interfaces, while others communicate directly through PSC.


## 12.3 Phase 3 — Native PSC Fabric Systems

In native PSC systems, the communication fabric becomes the primary interconnect architecture.

In this phase:

- most devices connect directly to PSC controllers
- transfers occur primarily through the PSC fabric
- traditional bus architectures are minimized

The system operates as a fabric-oriented compute environment rather than a bus-oriented architecture.


## 12.4 Phase 4 — Optical Fabric Systems

Future PSC systems may transition toward fully optical interconnect environments.

In this phase:

- optical links dominate fabric connectivity
- long-distance node communication becomes practical
- large-scale PSC fabrics may span multiple systems or facilities

Optical fabrics enable extremely high bandwidth and energy-efficient communication.


## 12.5 Incremental Deployment Benefits

The phased deployment model provides several advantages:

- compatibility with existing platforms
- reduced initial adoption cost
- gradual ecosystem transition
- flexibility for hardware vendors

This approach allows PSC to evolve alongside existing computing architectures rather than replacing them abruptly.

# 13. Future Work

While this specification defines the core architecture of the PSC fabric, several areas remain open for further research and development.

Future work may expand PSC capabilities, refine protocol behavior, and explore new deployment environments.


## 13.1 Advanced Congestion Control

Although PSC currently uses credit-based flow control and a multi-level congestion state model, more advanced congestion management techniques may be explored.

Possible directions include:

- predictive congestion avoidance
- adaptive credit scaling
- machine-learning assisted traffic prediction
- global congestion telemetry


## 13.2 Enhanced Scheduling Policies

PSC scheduling mechanisms may be extended to support more sophisticated traffic management.

Potential improvements include:

- application-aware scheduling
- latency-sensitive traffic prioritization
- workload classification
- dynamic resource reservation


## 13.3 Large-Scale Fabric Coordination

As PSC fabrics grow in size, additional coordination mechanisms may be required.

Future research may address:

- inter-domain routing
- large-scale topology optimization
- distributed routing convergence mechanisms
- cross-fabric communication protocols


## 13.4 Optical Device Integration

Future PSC implementations may support direct integration with optical-native devices.

Possible developments include:

- optical GPU interfaces
- optical storage controllers
- optical network interfaces
- integrated photonic switching modules


## 13.5 Hardware Acceleration

PSC controllers may incorporate specialized hardware accelerators to improve performance.

Examples include:

- hardware routing engines
- dedicated scheduling pipelines
- congestion detection hardware
- transfer offload engines


## 13.6 Security and Isolation

Future PSC fabrics may incorporate additional security mechanisms.

Possible areas of development include:

- node authentication
- encrypted fabric communication
- isolation between fabric domains
- hardware-level access control


## 13.7 Fabric Operating Systems

PSC fabrics may eventually support fabric-level operating environments.

These systems could provide:

- global resource visibility
- fabric-wide scheduling
- distributed memory access coordination
- large-scale compute orchestration


## 13.8 Research Opportunities

PSC architecture opens several research opportunities in areas such as:

- fabric-oriented computing models
- distributed transfer control
- high-performance optical interconnects
- large-scale heterogeneous compute fabrics

Continued exploration of these areas may lead to new system architectures built upon PSC principles.

# 14. Open Design Items

The following items were identified during early PSC protocol design
and will be refined in later specification revisions.

## 14.1 Domain Naming Alignment

The Domain Scope defined in the PSC Port Model and the Fabric Domain
field in the PSC Packet structure should be aligned in a future revision.

## 14.2 Trust Level Definition

The origin and lifecycle of the Trust Level field in the Security Tag
needs clarification. It may be derived from port security class,
session validation, or dynamic policy evaluation.

## 14.3 Sequence Number vs Chunk ID Semantics

The functional distinction between Sequence Number and Chunk ID
should be explicitly defined to support multipath transfer and
reordering behavior.

## 14.4 Integrity Tag Coverage

The integrity scope of the Integrity Tag should be defined,
including whether it protects only the header or the entire packet
including payload.

---

End of PSC Architecture Specification v0.2
