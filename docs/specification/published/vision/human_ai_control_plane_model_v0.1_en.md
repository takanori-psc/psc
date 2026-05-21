# Human-AI Control Plane Model v0.1

## Document Information

- Document Name : Human-AI Control Plane Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : Operational Control Layer
- Document Type : Conceptual Architecture Model
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-05
- Last Updated  : 2026-05
- Language      : English

---

## 1. Overview

This model defines the control structure, responsibility separation, and trust boundaries for next-generation AI operational environments in which:

- Humans
- Local AI
- Cloud AI
- Execution Environments

coexist and interact simultaneously.

In conventional AI usage models, humans are often treated merely as users.

However, in actual multi-AI operational environments, humans function not merely as users, but as operational control entities responsible for:

- AI selection
- Output comparison
- Execution approval
- Trust evaluation
- Boundary management
- Escalation decisions

In this model, this human-side control entity is defined as the **Human Resolver**.

Furthermore, the overall control structure centered around the Human Resolver — including:

- Local AI
- Cloud AI
- Execution Environments

—is defined as the **Human-AI Control Plane**.

---

## 2. Operational Structure

### 2.1 Basic Structure

```text
+--------------------------------------------------+
|              Human Resolver Plane                |
|--------------------------------------------------|
| AI selection                                     |
| Output comparison                                |
| Trust evaluation                                 |
| Execution approval                               |
| Arbitration                                      |
| Boundary control                                 |
+--------------------------------------------------+

        ↓                ↓                ↓

+----------------+  +----------------+  +----------------+
| Local AI Plane |  | Cloud AI Plane |  | Execution Plane|
|----------------|  |----------------|  |----------------|
| Local LLM      |  | ChatGPT        |  | Terminal       |
| Qwen           |  | Codex Cloud    |  | Git            |
| Continue       |  | Remote Agents  |  | File System    |
+----------------+  +----------------+  +----------------+
```

In this structure, the Human Resolver functions as the central operational control entity, integrating and supervising multiple AI systems and execution environments.

---

## 3. Human Resolver Concept

The Human Resolver is the final control authority within a multi-AI operational environment.

The Human Resolver is responsible for:

- AI output comparison
- Execution approval decisions
- Trust boundary evaluation
- Semantic conflict resolution
- Execution authorization
- Agent switching decisions
- Emergency stop decisions

The Human Resolver is not merely an operator.

Instead, it functions as the Arbitration Layer of the overall AI operational system.

---

## 4. Operational Boundary Concept

In multi-AI operational environments, multiple boundaries coexist simultaneously:

- Local AI Boundary
- Cloud AI Boundary
- Execution Boundary
- Trust Boundary
- Human Approval Boundary

These boundaries are not simple Local / Cloud separations.

In practice, they become interconnected through mechanisms such as:

- External communication
- Plugins
- IDE integration
- Telemetry
- Remote execution
- File access
- Git operations

Therefore:

```text
Local LLM = trusted
```

cannot be assumed automatically.

This model defines Trust Boundaries based on **Operational Trust**, including:

- execution capability,
- external connectivity,
- operational authority,
- and execution privileges.

---

## 5. Multi-Agent Operational Environment

Modern AI operational environments are increasingly evolving toward structures in which multiple AI systems operate in parallel while specializing in different roles.

Example:

| Plane          | Role                       |
| -------------- | -------------------------- |
| Local AI       | Semantic analysis          |
| Cloud AI       | Arbitration / reasoning    |
| Execution AI   | Implementation / execution |
| Human Resolver | Final decision making      |

In this structure, each AI system is responsible for different areas of expertise.

As a result, reliable operation requires:

- comparison,
- validation,
- and arbitration

between multiple AI systems rather than complete control by a single AI.

---

## 6. Execution Separation

AI operational environments require explicit separation between:

- Human execution
- AI-assisted execution

Example:

| Environment    | Purpose                 |
| -------------- | ----------------------- |
| Human Terminal | Manual execution        |
| AI Terminal    | Agent execution         |
| Editor         | Source modification     |
| External AI    | Reasoning / arbitration |

This visual and structural separation is important for:

- preventing operational mistakes,
- identifying execution ownership,
- trust management,
- and execution tracing.

---

## 7. Multi-Surface Confusion

In environments involving multiple AI systems and multiple operational surfaces, the following elements coexist simultaneously:

- Chat UI
- IDE
- Terminal
- Agent console
- Git operations
- Browser environments

Under these conditions, ambiguity may emerge regarding:

- who executed an action,
- which AI proposed an operation,
- what has already been executed,
- and which entities should be trusted.

This model defines this operational ambiguity as:

```text
Multi-Surface Confusion
```

---

## 8. Design Principles

This model is based on the following principles:

- Human-centered control
- Trust separation
- Multi-agent arbitration
- Explicit execution approval
- Operational boundary visibility
- Human-readable execution tracing
- Layered trust validation

In Human-AI operational environments, fully autonomous control that excludes humans is not considered the primary design objective.

Instead, layered operational control structures incorporating the Human Resolver are regarded as essential.
