PSC Terminology

PSC Glossary v0.2 (English Version)

Core System
PSC

Photon System Controller

A communication processor that controls optical fabric communication.
PSC replaces the traditional CPU-centric bus architecture with a fabric-driven architecture.

PSC Fabric

A communication fabric managed and controlled by PSC.

Characteristics:

Node connectivity

Distributed communication

Fabric routing capability

Chunk-based transport

Receiver-driven transfer

PSC Fabric is intended to become the foundation of the GAIOS network in the future.

Fabric-driven Architecture

A computer architecture model in which communication is organized through a fabric network instead of a CPU-controlled bus system.

Optical Interconnect Types

PSC classifies optical communication into two domains.

Optical PCIe Domain

A domain where the PCI Express protocol is transported over optical links.

Protocol : PCIe  
Medium   : Optical

Purpose:

Maintain compatibility with existing PCIe devices

Connect GPUs and NVMe storage

Preserve OS and driver compatibility

Security:

Trusted Local Domain

This domain is not directly reachable from external networks.

PSC Fabric Domain

A native communication fabric controlled by PSC.

Protocol : PSC Fabric Protocol  
Medium   : Optical

Characteristics:

Node-to-node communication

Fabric routing

Chunk transport

Policy-based control

Typical usage:

Blade-to-blade communication

In-rack communication

Cluster communication

GAIOS network connectivity

Optical Interconnect Comparison
	Optical PCIe	PSC Fabric
Architecture	CPU bus	Fabric network
Protocol	PCIe	PSC Fabric Protocol
Control	CPU Root Complex	PSC
Security Scope	Trusted Local	Compute Network
Exposure	Internal	Potentially external
PSC Port Model

All PSC fabric ports share a common physical interface.

The role and behavior of each port are determined by logical configuration.

Port Mode

Defines the communication mode used by a port.

Examples:

PSC_NATIVE
PCIe_TUNNEL
PCIe_BRIDGE
MANAGEMENT
Security Class

Defines the trust level of a port.

Examples:

LOCAL_TRUSTED
RACK_TRUSTED
CLUSTER_TRUSTED
EXTERNAL_PUBLIC
Policy Profile

Defines communication rules applied to a port.

Control parameters include:

Allowed connection domains

Direction control

Bandwidth limitations

Routing restrictions

Visibility control

Security Domains

PSC Fabric separates communication scopes into security domains.

Trusted Device Domain

A trusted domain inside a node.

Examples:

CPU

Memory

GPU

NVMe

Devices in this domain cannot be directly accessed from external networks.

Fabric Domain

A compute fabric used for communication between PSC nodes.

Examples:

Blade-to-blade communication

In-rack communication

Cluster communication

Open Network Domain

A domain used for GAIOS network connectivity.

External nodes may connect through this domain.

PSC Internal Modules
Resolver

Evaluates transfer requests and determines control policies.

Scheduler

Handles transfer scheduling.

RCU

Routing Control Unit

Computes routing paths in the PSC fabric.

TMU

Transfer Management Unit

Manages data transfers.

Responsibilities:

Chunk segmentation

Flow control

TEU

Transfer Execution Unit

Executes actual data transmission.

OMU

Optical Monitoring Unit

Monitors optical link conditions.

Telemetry / Fault Monitor

Responsible for system monitoring and fault detection.

SPU

Security Policy Unit

Manages PSC security policies.

Responsibilities:

Port attribute management

Domain control

Access validation

Isolation enforcement

Transfer Model
Receiver-driven Transfer

Data transfer is controlled by the receiver side.

Chunk Transport

Data is transferred in chunk units.

Credit Flow Control

A buffer-based flow control mechanism.

Fabric State Model

CALM
Low load state

WARM
Increasing load state

HOT
High load state

EMERGENCY
Abnormal or critical state

Fabric Topology

Mesh

Hierarchical Fabric

Spine-Leaf Fabric

Implementation Phases

Phase1
PCIe Bridge PSC

Phase2
Hybrid Fabric

Phase3
Native PSC Fabric

Phase4
Optical Fabric
