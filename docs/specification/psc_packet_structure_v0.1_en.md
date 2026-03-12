PSC Fabric Packet Structure v0.1
1. Purpose

PSC Fabric Packet is the fundamental transport unit used within the PSC Fabric.

It carries:

routing information

security context

transfer control

chunked data payload

PSC packets are optimized for receiver-driven chunk transport across an adaptive optical fabric.

2. Design Principles

PSC Packet design follows these rules.

Fabric-native

Packets are designed for PSC Fabric routing, not traditional bus or IP networking.

Receiver-driven transfer

Transfers are initiated and controlled by the receiving node, not the sender.

Chunk transport

Large transfers are divided into chunks.

Benefits:

congestion control

flow control

partial retry

multi-path scheduling

Policy-aware communication

Packet headers contain security and domain information, enabling:

SPU enforcement

domain control

secure routing

3. Packet Structure Overview
PSC Packet

┌─────────────────────┐
│ PSC Header          │
├─────────────────────┤
│ Routing Information │
├─────────────────────┤
│ Security Tag        │
├─────────────────────┤
│ Transfer Control    │
├─────────────────────┤
│ Chunk Descriptor    │
├─────────────────────┤
│ Payload Data        │
└─────────────────────┘
4. PSC Header

The PSC Header defines the fundamental packet identity.

Fields
Version
Packet Type
Packet Length
Transfer ID
Sequence Number
Flags
Description

Version

PSC protocol version.

Allows future protocol evolution.

Packet Type

Defines packet behavior.

Initial types:

REQUEST
DATA
ACK
FLOW_CONTROL
CONTROL
FAULT
TELEMETRY

Packet Length

Total packet size.

Transfer ID

Unique identifier of the transfer session.

Used by:

TMU

TEU

Flow control

Sequence Number

Chunk ordering index within the transfer.

Flags

Various control flags.

Examples:

RETRY
PRIORITY
SECURE_PATH
MULTIPATH
PARTIAL_CHUNK
5. Routing Information

Routing fields allow the PSC Fabric to determine packet path.

Fields
Source Node ID
Destination Node ID
Source Port ID
Destination Port ID
Fabric Domain
Path Hint
Hop Count
Source Node ID

Origin PSC node.

Destination Node ID

Target PSC node.

Source Port ID

Logical port identifier.

Defined by PSC Port Model v0.1.

Destination Port ID

Target logical port.

Fabric Domain

Defines routing scope.

Examples:

LOCAL
CLUSTER
GLOBAL
EXTERNAL
Path Hint

Optional hint for RCU routing.

Examples:

LOW_LATENCY
HIGH_BANDWIDTH
RESILIENT
Hop Count

Prevents infinite routing loops.

6. Security Tag

Security Tag is evaluated by the SPU (Security Policy Unit).

Fields
Security Class
Trust Level
Domain Authorization
Policy Flags
Integrity Tag
Security Class

Matches the Port Security Class.

SYSTEM
TRUSTED
USER
EXTERNAL
QUARANTINED
Trust Level

Additional trust evaluation.

Domain Authorization

Allowed domain scope.

Policy Flags

Security behavior indicators.

Examples:

INSPECT
ISOLATE
PRIORITY_SECURITY
RESTRICT_FORWARD
Integrity Tag

Packet integrity verification field.

7. Transfer Control

Transfer Control fields support PSC's receiver-driven transport model.

Fields
Transfer Type
Transfer State
Flow Credit
Priority Class
Retry Counter
Transfer Type
STREAM
BLOCK
MEMORY
CONTROL
TELEMETRY
Transfer State

State of transfer progression.

Examples:

INIT
ACTIVE
PAUSED
RETRY
COMPLETE
Flow Credit

Remaining credit units allowed by receiver.

Used for flow control.

Priority Class

Scheduler priority.

Example classes:

REALTIME
HIGH
NORMAL
BACKGROUND
Retry Counter

Number of retransmission attempts.

8. Chunk Descriptor

PSC transfers use chunk-based data transport.

Chunk descriptor defines the fragment.

Fields
Chunk ID
Chunk Offset
Chunk Size
Total Transfer Size
Chunk Flags
Chunk ID

Unique chunk index.

Chunk Offset

Byte offset within transfer.

Chunk Size

Size of this chunk.

Total Transfer Size

Full transfer size.

Chunk Flags

Examples:

FIRST_CHUNK
LAST_CHUNK
PARTIAL
RECOVERY
9. Payload Data

Actual transferred data.

Payload may contain:

Memory data
File blocks
Model parameters
Inference tensors
Storage objects
Control messages

PSC does not enforce payload semantics.

Payload interpretation belongs to higher layers (PSCOS / applications).

10. Packet Lifecycle

Typical PSC packet lifecycle:

Receiver Node

Transfer Request
      ↓
Resolver
      ↓
Scheduler
      ↓
SPU Validation
      ↓
RCU Route Selection
      ↓
TMU Transfer Context
      ↓
TEU Packet Generation
      ↓
PSC Fabric Routing
      ↓
Destination PSC
11. Error Handling

Errors may occur at several layers.

Examples
Security violation
Route failure
Link degradation
Flow control violation
Integrity mismatch

Possible actions:

Retry
Reroute
Quarantine
Drop
Fault escalation
12. Packet Types Summary
REQUEST        Receiver initiates transfer
DATA           Chunk data packet
ACK            Chunk acknowledgement
FLOW_CONTROL   Credit updates
CONTROL        PSC control message
FAULT          Error notification
TELEMETRY      Monitoring data
