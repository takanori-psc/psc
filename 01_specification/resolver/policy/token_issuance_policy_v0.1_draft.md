PSC Resolver – Token Issuance Policy (Draft v0.1)


1. Purpose

Token represents permission, not bandwidth guarantee.
Token issuance governs change pressure (NewFlow, Reroute, Burst, Recovery).

2. Issuer Model

Token MAY be issued by:

Resolver (primary authority)

Execution Layer (local safety fallback only)

Authorization Module (Recovery-related authorization)

Resolver is the default issuer.

3. Token Structure

Token {
type,
class,
scope,
ttl,
issuer_state,
nonce,
timestamp,
signature
}

Signature Rules:

If issuer_state >= HOT → Token MUST be signed.

If issuer_state < HOT → Signature MAY be omitted.

4. Scope Hierarchy

Scope levels:

Link ⊂ LocalDomain ⊂ Node

Token scope MUST encompass the intended operation.

5. Token Type Policies
5.1 NewFlow

Purpose: Control admission pressure.

Rules:

MUST NOT issue if Budget[class] == STOP.

In EMERGENCY:

Only SYSTEM MAY be issued.

BULK SHOULD be clamped from WARM onward.

5.2 Reroute

Purpose: Prevent routing oscillation.

Rules:

In WARM: SHOULD require Token.

In HOT or higher: MUST require Token.

Safety-enforced reroute does not require Token.

5.3 Burst

Purpose: Limit instability from sudden load spikes.

Rules:

In WARM: INTERACTIVE and REALTIME MAY be clamped.

In HOT: Only SYSTEM SHOULD be allowed.

In EMERGENCY: Only SYSTEM MAY be issued.

TTL SHOULD be short.

5.4 Recovery

Purpose: Preserve system self-healing.

Rules:

Recovery SHOULD generally be allowed.

In NodeState == EMERGENCY:

SYSTEM: Allow

REALTIME: Allow

INTERACTIVE: Clamp

BULK: Clamp (not Deny)

Recovery for BULK MUST NOT be denied in EMERGENCY unless explicitly overridden by Enforcement.

6. Rate Limiting

Token issuance rate MUST be state-aware:

WARM: Moderate rate limitation.

HOT: Strong rate limitation.

EMERGENCY: Only essential Tokens issued.

Exact numeric thresholds are implementation-defined.

7. Execution Layer Fallback

Execution Layer MAY issue ultra-short-lived Token only for:

Immediate safety-preserving local fallback.

Scope MUST be Link.

MUST be logged and reported to Resolver.
