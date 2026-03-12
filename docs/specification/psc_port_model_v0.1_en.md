PSC Port Model v0.1

1. Purpose

PSC Port is not defined as a fixed device-specific interface.
Instead, each port is defined as a role-based communication endpoint whose behavior is determined by policy, trust class, domain, and transfer requirements.

This allows PSC to treat ports as adaptive fabric endpoints rather than static bus attachments.

2. Design Principle
Conventional Port Model

A port is statically assigned to a device category.

Examples:

GPU Port

Storage Port

Network Port

PSC Port Model

A port is a logical communication role assigned dynamically by PSC.

A port does not primarily represent “what device is attached,” but rather:

what role the endpoint plays

what security level it has

what policy governs traffic

what domain it belongs to

what transfer behavior is allowed

3. Port Definition

A PSC Port is a communication endpoint managed by PSC that connects a local device, a remote PSC node, or a fabric path into the PSC Fabric.

Each port has:

Port ID

Port Role

Port Mode

Security Class

Policy Profile

Domain Scope

Link State

Capability Flags

4. Port Structure
PSC Port
├─ Port ID
├─ Port Role
├─ Port Mode
├─ Security Class
├─ Policy Profile
├─ Domain Scope
├─ Link State
└─ Capability Flags
5. Port ID

Port ID is the unique local identifier for a PSC-managed communication endpoint.

Requirements

Unique within a PSC node

Used by Resolver / Scheduler / RCU / TMU

Mapped to routing and policy tables

Can be rebound to different logical roles without changing physical wiring

Example
Port 0x01
Port 0x02
Port 0x03
6. Port Role

Port Role represents the current logical role assigned to the port.

This role may change depending on system configuration or PSC control policy.

Initial Role Categories
Compute

Used for CPU / GPU / accelerator task traffic

Memory

Used for memory-oriented transactions and low-latency data access

Storage

Used for block/object/file movement and persistence traffic

Network

Used for external network ingress/egress or gateway behavior

Fabric

Used for PSC-to-PSC internal fabric links

Management

Used for control, telemetry, diagnostics, maintenance

7. Port Mode

Port Mode defines the operational behavior of the port.

Modes
Endpoint Mode

Port is attached to a local endpoint device

Fabric Link Mode

Port connects to another PSC node or switching path

Relay Mode

Port can relay traffic between domains or paths under policy control

Isolated Mode

Port is logically attached but restricted from normal traffic

Maintenance Mode

Port is reserved for diagnostics / update / recovery

8. Security Class

Security Class defines the trust and enforcement level applied to traffic entering or leaving the port.

Classes
System

Core PSC internal traffic only
Highest trust
Used for Resolver / control / fault / recovery paths

Trusted

Trusted internal devices or validated PSC nodes

User

Normal application-facing traffic

External

Untrusted or boundary-facing traffic

Quarantined

Restricted traffic class for suspicious / degraded / recovery use

9. Policy Profile

Policy Profile defines the behavioral target of the port.

This affects scheduling, routing preference, buffer policy, and admission behavior.

Profiles
Latency Optimized

Prioritize minimal delay
Used for memory-like or urgent control traffic

Throughput Optimized

Prioritize sustained transfer efficiency
Used for storage / bulk transfer / streaming

Secure

Prioritize inspection, validation, and restricted routing

Balanced

Default mixed policy

Resilient

Prioritize stability and fallback behavior under degraded fabric state

10. Domain Scope

Domain Scope defines where the port is allowed to communicate.

Scopes
Local Node

Traffic remains inside local PSC node scope

Local Fabric

Traffic may traverse nearby PSC fabric segment

Cluster

Traffic may communicate across a trusted cluster

Global Fabric

Traffic may traverse larger PSC-wide fabric

External Boundary

Traffic may cross into non-PSC or external network environment

11. Link State

Link State represents current operational condition.

States
DOWN

No active link

INIT

Training / negotiation / bring-up in progress

READY

Link established and available

DEGRADED

Link active but performance/reliability reduced

RESTRICTED

Link active with policy-limited operation

FAULT

Link failure or unsafe behavior detected

12. Capability Flags

Capability Flags describe what the port can support.

Examples

Chunk Transfer Supported

Credit Flow Control Supported

Secure Tag Enforcement Supported

Multi-path Eligible

Fabric Relay Allowed

Low-latency Path Eligible

External Boundary Crossing Allowed

Telemetry Priority Enabled

13. Dynamic Role Binding

A key PSC feature is that port meaning is not fixed permanently.

Rule

A physical port may be rebound logically if:

security constraints allow it

topology policy allows it

Resolver approves the change

Scheduler / RCU tables are updated consistently

active transfers are safely drained or migrated

Example

A port connected to an accelerator shelf may operate as:

Compute role during inference workload

Fabric role when used as relay expansion

Isolated mode during validation failure

Maintenance mode during firmware or optical inspection

This is one of the major differences from conventional bus-centric systems.

14. Port Control Ownership

PSC modules interact with the port as follows:

Resolver

Determines high-level role eligibility and policy authority

Scheduler

Applies traffic priority and service profile

SPU

Enforces trust class, domain crossing, and policy restrictions

RCU

Maps port to routing behavior and path selection

TMU

Assigns transfer context and flow-control behavior

TEU

Executes actual transfer issuance through the selected port

OMU

Monitors optical/link condition and health signals

Telemetry / Fault Monitor

Tracks degradation, anomalies, and failure escalation

15. Port Behavior by Fabric State

Port behavior should also depend on global/local fabric condition.

CALM

Normal full-policy operation

WARM

Mild load adaptation, path optimization, soft shaping

HOT

Aggressive prioritization, admission control, rerouting

EMERGENCY

Restricted traffic set, protection-first behavior, quarantine escalation

16. Initial Port Policy Rules
Rule 1

All ports must have exactly one active Security Class.

Rule 2

All ports must have exactly one active Policy Profile.

Rule 3

Port Role may change, but only through PSC-controlled rebinding.

Rule 4

External or Quarantined ports cannot directly gain System privileges.

Rule 5

Fabric-role ports require routing validation and telemetry monitoring.

Rule 6

Domain expansion must be explicitly authorized by policy.

Rule 7

A DEGRADED or FAULT link may trigger automatic policy downgrade.

17. Example Port Table
Port ID   Role        Mode            Security   Policy        Domain
0x01      Compute     Endpoint        Trusted    Latency       Local Node
0x02      Memory      Endpoint        System     Latency       Local Node
0x03      Storage     Endpoint        User       Throughput    Cluster
0x04      Fabric      Fabric Link     Trusted    Balanced      Cluster
0x05      Network     Relay           External   Secure        External Boundary
0x06      Management  Maintenance     System     Resilient     Local Node
18. Design Significance

This model gives PSC three major advantages:

1. Device abstraction

Ports are no longer hardwired to device meaning.

2. Policy-native communication

Security and routing policy become part of port identity.

3. Fabric adaptability

Ports can be repurposed according to topology, workload, and fault conditions.
