PSC Address Format v0.1
Author: T.Hirose
Status: Draft

1. Purpose

PSC Address Format defines the native address structure used
inside the PSC Fabric for routing and transfer execution.

The address format is designed to provide a clear hierarchical
structure that supports efficient routing, scalable deployment,
and simple hardware implementation.

The PSC address represents the physical and logical location
of a communication endpoint within the PSC Fabric.

---

2. Design Goals

The PSC Address Format is designed with the following goals.

Scalability

The address structure must support PSC deployments ranging
from small local systems to large distributed infrastructures.

Hierarchical Routing

The address format must reflect the hierarchical topology
of PSC Fabric including fabrics, clusters, nodes, and ports.

Hardware Efficiency

The format must allow efficient hardware implementation
inside PSC modules such as RCU, TMU, and TEU.

Deterministic Routing

Routing decisions should be derived directly from address
fields without complex translation overhead.

Future Expandability

The format should allow future PSC extensions such as
global addressing and logical service identification.

---

3. Address Format Overview

PSC uses a fixed-length 64-bit address.

The address is composed of four hierarchical fields.

Fabric ID
Cluster ID
Node ID
Port ID

Address Layout

Fabric ID : Cluster ID : Node ID : Port ID

Each field represents a level of the PSC Fabric topology.

---

4. Bit Allocation

The PSC native address is allocated as follows.

Fabric ID   : 16 bits
Cluster ID  : 16 bits
Node ID     : 24 bits
Port ID     : 8 bits

Total       : 64 bits

This allocation balances scalability and hardware efficiency.

---

5. Field Definitions

5.1 Fabric ID

Fabric ID identifies a PSC Fabric domain.

A fabric represents a routing domain where PSC nodes
are interconnected by PSC Fabric links.

Multiple fabrics may exist in large deployments.

Maximum fabrics

65536

---

5.2 Cluster ID

Cluster ID identifies a logical grouping of nodes
within a fabric.

Clusters can represent physical or logical groupings such as

Rack groups
Local compute clusters
Data center segments
Edge clusters

Cluster-based organization improves routing scalability
and management.

Maximum clusters per fabric

65536

---

5.3 Node ID

Node ID identifies a PSC node inside a cluster.

A node represents a device or processing element
connected to the PSC Fabric.

Examples include

CPU nodes
GPU nodes
Memory nodes
Storage nodes
Network nodes
Accelerator nodes

Node IDs must be unique inside a cluster.

Maximum nodes per cluster

16777216

---

5.4 Port ID

Port ID identifies a communication endpoint inside a node.

Ports represent PSC communication interfaces or
internal functional endpoints.

Examples include

Optical PSC ports
Internal device interfaces
Logical communication endpoints

Maximum ports per node

256

---

6. Routing Use

PSC routing decisions are primarily handled by
the Routing Control Unit (RCU).

The hierarchical address format allows routing
decisions to be performed using address field analysis.

Routing levels include

Fabric-level routing
Cluster-level routing
Node-level routing
Port-level routing

This structure enables efficient routing
in large PSC fabrics.

---

7. Resolution Layer Relationship

The 64-bit PSC address represents the native
transfer address used inside the PSC Fabric.

Higher-level identifiers such as

Logical service names
Global identifiers
Virtual node references
Application-level object identifiers

are resolved by upper layers such as the Resolver.

Example resolution model

Logical Name
      ↓
Resolver
      ↓
PSC Native Address (64-bit)

This separation keeps the PSC Fabric routing
system simple and efficient.

---

8. Address Examples

Example Address

1 : 2 : 100 : 3

Fabric 1
Cluster 2
Node 100
Port 3

Example Usage

GPU node requesting data from a memory node

Source Address

1 : 2 : 50 : 1

Destination Address

1 : 2 : 100 : 3

---

9. Future Extensions

Future PSC versions may extend the addressing model
with additional concepts such as

Hierarchical routing domains
Spine-leaf topology identifiers
Global PSC addressing
Logical service addressing
Function-level addressing

The current 64-bit structure is designed
to remain compatible with such extensions.

---

10. Summary

PSC Address Format v0.1 defines a 64-bit hierarchical
address used inside the PSC Fabric.

The structure consists of Fabric ID, Cluster ID,
Node ID, and Port ID fields.

This design enables scalable routing, efficient
hardware implementation, and clear hierarchical
organization of PSC systems.

The native PSC address focuses on fabric-level
communication while higher-level identification
is handled by upper resolution layers.
