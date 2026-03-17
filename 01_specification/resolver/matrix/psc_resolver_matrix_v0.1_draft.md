PSC Resolver – State × Class × TokenType Matrix (Draft v0.1)
Design Principles

SYSTEM traffic is always preserved.

REALTIME traffic is preserved under HOT when possible.

BULK traffic is the first to be restricted.

Burst is restricted early to reduce instability.

Recovery is preserved whenever possible.

EMERGENCY follows fail-closed philosophy.

CALM

All classes and token types are allowed.

WARM

SYSTEM

NewFlow: Allow

Reroute: Allow

Burst: Allow

Recovery: Allow

REALTIME

NewFlow: Allow

Reroute: Allow

Burst: Clamp

Recovery: Allow

INTERACTIVE

NewFlow: Allow

Reroute: Clamp

Burst: Clamp

Recovery: Allow

BULK

NewFlow: Clamp

Reroute: Clamp

Burst: Deny

Recovery: Allow

HOT

SYSTEM

NewFlow: Allow

Reroute: Allow

Burst: Allow

Recovery: Allow

REALTIME

NewFlow: Allow

Reroute: Clamp

Burst: Deny

Recovery: Allow

INTERACTIVE

NewFlow: Clamp

Reroute: Deny

Burst: Deny

Recovery: Allow

BULK

NewFlow: Deny

Reroute: Deny

Burst: Deny

Recovery: Clamp

EMERGENCY

SYSTEM

NewFlow: Allow

Reroute: Allow

Burst: Clamp

Recovery: Allow

REALTIME

NewFlow: Clamp

Reroute: Deny

Burst: Deny

Recovery: Allow

INTERACTIVE

NewFlow: Deny

Reroute: Deny

Burst: Deny

Recovery: Clamp

BULK

NewFlow: Deny

Reroute: Deny

Burst: Deny

Recovery: Deny
