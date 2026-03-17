PSC Address Format v0.1 adopts a fixed 64-bit hierarchical address structure.

The address is composed of:

Fabric ID   : 16 bits
Cluster ID  : 16 bits
Node ID     : 24 bits
Port ID     : 8 bits

This format is designed for efficient hardware implementation,
clear hierarchical routing, and scalability across PSC Fabric
deployments ranging from small local systems to large distributed
regional infrastructures.

The 64-bit PSC address is defined as a native fabric address used
for routing and transfer execution inside the PSC Fabric.

Higher-level logical names, service identifiers, and global-scale
object references are handled by upper resolution layers such as
the Resolver, and are not required to be embedded directly into
the native transfer address.
