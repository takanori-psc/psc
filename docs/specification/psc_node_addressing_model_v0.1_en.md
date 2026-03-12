PSC Node Addressing Model v0.1
Author: T.Hirose
Status: Draft

1. Purpose

PSC Node Addressing Model defines how nodes, ports, and routing domains
are identified inside the PSC Fabric.

The goal of this model is to provide a scalable, hierarchical, and
implementation-friendly addressing structure that supports both
early small-scale PSC systems and future large-scale distributed
fabric architectures.

This addressing model enables efficient routing, node identification,
and transfer management across PSC Fabric environments.

---

2. Design Goals

The addressing model is designed with the following goals:

• Scalability
Support small local PSC systems and future large-scale distributed fabrics.

• Hierarchical structure
Allow logical grouping of nodes using clusters and fabrics.

• Routing efficiency
Enable efficient routing decisions inside the Routing Control Unit (RCU).

• Implementation simplicity
Allow efficient hardware and firmware implementation.

• Future extensibility
Provide space for future expansion such as hierarchical fabrics
and global distributed PSC networks.

---

3. Addressing Scope

PSC addressing is used for identifying:

• PSC Fabric instances
• Clusters within a fabric
• Nodes connected to the fabric
• Ports inside a node

These identifiers allow routing decisions and transfer operations
to be executed by PSC internal modules.

Primary users of this addressing model include:

Resolver
RCU (Routing Control Unit)
TMU (Transfer Management Unit)
Scheduler

---

4. Fabric Address Structure

PSC uses a hierarchical address structure.

Basic Address Format

Fabric ID : Cluster ID : Node ID : Port ID

Each field represents a different level of the PSC fabric topology.

Example

1 : 2 : 15 : 3

Fabric 1
Cluster 2
Node 15
Port 3

This structure allows scalable addressing and efficient routing
in multi-cluster PSC fabrics.

---

5. Address Field Definitions

5.1 Fabric ID

Fabric ID identifies a PSC Fabric domain.

Multiple fabrics may exist in large-scale deployments.
Fabric ID separates independent PSC fabric domains.

Example

Fabric 0
Fabric 1
Fabric 2

---

5.2 Cluster ID

Cluster ID identifies a group of nodes inside a fabric.

Clusters allow logical grouping and can represent:

• Physical racks
• Local network groups
• Data center segments
• Edge clusters

Cluster-based grouping improves routing efficiency
and scalability.

---

5.3 Node ID

Node ID identifies a PSC node inside a cluster.

Each node represents a device connected to the PSC Fabric.

Typical node types include:

CPU nodes
GPU nodes
Memory nodes
Storage nodes
Network nodes
Accelerator nodes

Node IDs must be unique inside a cluster.

---

5.4 Port ID

Port ID identifies a communication endpoint inside a node.

Ports represent PSC communication interfaces.

Examples include:

PSC optical ports
Internal device interfaces
Logical communication endpoints

Port ID enables routing to specific interfaces
inside a PSC node.

---

6. Routing Scope

Routing decisions are primarily performed by the
Routing Control Unit (RCU).

The routing scope is determined by the hierarchical address.

Routing levels include:

Port-level routing
Node-level routing
Cluster-level routing
Fabric-level routing

Hierarchical routing allows efficient scaling
of large PSC fabrics.

---

7. Address Resolution

Address resolution is responsible for mapping
logical node identifiers to routing paths.

Resolution responsibilities are shared across:

Resolver
RCU
TMU

Typical resolution steps include:

1. Node request generated
2. Resolver validates request
3. Address interpreted by routing logic
4. RCU determines next hop
5. Transfer scheduled by TMU
6. Transfer executed by TEU

This model enables distributed routing
without centralized bottlenecks.

---

8. Addressing Example

Example Fabric

Fabric 1

Cluster 0
    CPU Node 0
    GPU Node 1

Cluster 1
    Memory Node 0
    Storage Node 1

Example Address

1 : 1 : 0 : 2

Fabric 1
Cluster 1
Node 0
Port 2

This identifies a specific port on a memory node
inside cluster 1 of fabric 1.

---

9. Future Extensions

Future PSC versions may extend the addressing model with:

• Hierarchical routing domains
• Spine-Leaf topology identifiers
• Global PSC network addressing
• Logical service addressing
• Function-level addressing

The current addressing structure is designed to
support these extensions.

---

10. Summary

PSC Node Addressing Model provides a hierarchical
addressing structure for identifying nodes, clusters,
and ports inside PSC Fabric environments.

The model enables scalable routing, efficient transfer
management, and future expansion toward large-scale
distributed PSC systems.
