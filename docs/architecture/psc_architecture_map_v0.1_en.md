## PSC Architecture Map

Version: v0.1

This document provides a high-level structural map of the PSC architecture.

```
GAIOS
Planet-scale Distributed AI OS
────────────────────────

PSCOS
PSC Control Software Layer
────────────────────────

PSC Fabric
Photon System Controller Network

 ├ Addressing
 │   ├ PSC Address Format(0.1)
 │   └ PSC Node Addressing Model(0.1)
 │
 ├ Communication
 │   ├ PSC Packet Structure(0.1)
 │   ├ PSC Port Model(0.1)
 │   └ PSC Transfer Flow(0.1)
 │
 ├ Routing
 │   ├ PSC Routing Model(0.1)
 │   ├ PSC Routing Table Model(0.1)
 │   ├ PSC Routing Algorithm(0.1)
 │   └ PSC Routing Decision Pipeline
 │
 ├ Fabric Control
 │   ├ PSC Fabric State Model(0.1)
 │   ├ PSC Node Type Model(0.1)
 │   └ PSC Control Plane Model(0.1)
 │
 ├ Fabric Telemetry
 │   └ PSC Telemetry Model(0.1)
 │
 ├ Traffic Control
 │   └ PSC Congestion Control Model(0.1)
 │
 ├ Policy / Governance
 │   └ PSC Policy Model(0.1)
 │
 └ Security
     └ PSC Security Model(0.1)

────────────────────────
PSC Hardware
Photon System Controller

 ├ PSC Chip
 ├ PSC Ports (16 ports)
 ├ Optical Fabric Links
 ├ PSC Nodes
 ├ PSC Blades
 └ PSC Joint Units
```
