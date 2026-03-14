# PSC Documentation Map

Project: PSC / Photon System Controller  
Document Type: Documentation Map  
Status: Draft  

---

# 1. Overview

This document describes the structure of PSC documentation.

PSC documentation is organized into multiple layers to clearly separate
conceptual ideas, architectural design, and formal specifications.

The documentation structure follows a layered approach:

```
PSC Concept
↓
PSC Architecture
↓
PSC Specification
```

---

# 2. PSC Documentation Structure

## 2.1 Concept Layer

Concept documents describe the high-level ideas and philosophy of PSC.

Location:

```
docs/concept
```

Main documents:

- PSC Concept
- PSC Architecture Map
- PSC Documentation Map

These documents explain:

- PSC design philosophy
- Fabric-centric computing concept
- High-level system structure

---

## 2.2 Specification Layer

Specification documents define the detailed design of PSC components.

Location:

```
docs/specification
```

Main specification groups:

### Addressing

- PSC Address Format
- PSC Node Addressing Model

### Packet

- PSC Packet Structure

### Port Model

- PSC Port Model

### Routing

- PSC Routing Model
- PSC Routing Algorithm
- PSC Routing Table Model

### Transfer

- PSC Transfer Flow

These specifications define the core behavior of PSC Fabric.

---

# 3. Specification Relationship

PSC specifications are organized as follows:

```
PSC Fabric

├ Addressing
│ ├ PSC Address Format
│ └ PSC Node Addressing Model
│
├ Packet
│ └ PSC Packet Structure
│
├ Port
│ └ PSC Port Model
│
├ Routing
│ ├ PSC Routing Model
│ ├ PSC Routing Algorithm
│ └ PSC Routing Table Model
│
└ Transfer
  └ PSC Transfer Flow
```

---

# 4. Future Documents

The following documents may be added in the future:

Architecture:

- PSC Fabric Architecture
- PSC Node Architecture
- PSC Routing Pipeline Architecture

Protocol:

- PSC Transport Model
- PSC Security Model
- PSC Congestion Control Model

System:

- PSC Native System Architecture
- PSC Hybrid System Architecture

---

# 5. Purpose of This Map

The documentation map helps:

- Understand the structure of PSC documentation
- Navigate PSC specifications
- Maintain consistency across documents
- Support future expansion of PSC architecture

---

# 6. Project

PSC  
Photon System Controller

Fabric-centric distributed computer architecture
