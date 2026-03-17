Figure 1. PSC System Architecture


                 +----------------------+
                 |       CPU Node       |
                 +----------+-----------+
                            |
                            | Local / Trusted
                            v
                 +----------------------+
                 |         PSC          |
                 |  (Fabric Controller) |
                 +----+-----------+-----+
                      |           |
        --------------+           +-------------------------------
        |                                                  |
        |                                                  |
        v                                                  v

+------------------+                             +----------------------+
| Optical PCIe     |                             |  PSC Fabric Domain   |
| Domain           |                             |  (Compute Fabric)    |
|------------------|                             +----+-----+-----+-----+
| GPU Node         |                                  |     |     | 
| NVMe Storage     |                                  |     |     |
| Trusted Device   |                                  |     |     |
+------------------+                                  |     |     |
                                                      |     |     |
                                                      v     v     v

                                                +---------+ +---------+ +-------------------+
                                                | PSC     | | PSC     | | GAIOS Network     |
                                                | Fabric  | | Fabric  | | Node              |
                                                | Node    | | Node    | | (Open Network)    |
                                                +----+----+ +----+----+ +-------------------+
                                                     |              |
                                                     |              |
                                                     v              v
                                              (Fabric Expansion / Cluster Extension)



Figure 2. PSC Internal Architecture


                +--------------------------------------------------+
                |                       PSC                        |
                |              (Fabric Controller)                 |
                |                                                  |
                |   +---------------------------+                  |
                |   |        Resolver           |                  |
                |   +-------------+-------------+                  |
                |                 |                                |
                |         +-------v-------+                        |
                |         |   Scheduler   |                        |
                |         +-------+-------+                        |
                |                 |                                |
                |   +-------------v-------------+                  |
                |   |   SPU: Security Policy    |                  |
                |   |          Unit             |                  |
                |   +-------------+-------------+                  |
                |                 |                                |
                |   +-------------v-------------+                  |
                |   |   Routing Control Unit    |                  |
                |   |          (RCU)            |                  |
                |   +-------------+-------------+                  |
                |                 |                                |
                |   +-------------v-------------+                  |
                |   |  Transfer Management Unit |                  |
                |   |          (TMU)            |                  |
                |   +-------------+-------------+                  |
                |                 |                                |
                |   +-------------v-------------+                  |
                |   |  Transfer Execution Unit  |                  |
                |   |          (TEU)            |                  |
                |   +-------------+-------------+                  |
                |                 |                                |
                |         +-------v-------+                        |
                |         | Optical Mon.  |                        |
                |         | Unit (OMU)    |                        |
                |         +-------+-------+                        |
                |                 |                                |
                |   +-------------v-------------+                  |
                |   | Telemetry / Fault Monitor |                  |
                |   +---------------------------+                  |
                +-----------------+--------------------------------+
                                  |
                                  v
          PSC Fabric Ports (Common Optical Fabric Interface)
