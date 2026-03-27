# PSC Resolver Specification v0.1

Japanese version: [psc_resolver_spec_v0.1_ja.md](psc_resolver_spec_v0.1_ja.md)

## Document Information

- Document Name : Resolver Specification
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSC Fabric
- Document Type : Specification
- Component     : Resolver
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-03
- Last Updated  : 2026-03
- Language      : English

## 0. Philosophical Foundation

This specification is governed by
PSC Resolver Design Philosophy v1.0.

The Resolver is not an optimizer.
It is a structural stabilizer.

All mechanisms described in this document
must respect the following principles:

- No continuous global optimization
- State-based coordination
- Local-first autonomy
- Intervention only when structural stability is at risk
- Resolver is not an execution entity; it defines constraints and decisions.
- Resolver MUST produce decisions that are explainable and reproducible.

---

## 1. Overview

Resolver is the decision-control module of PSC.
It operates in hybrid authority mode:

- Normal: Advisory
- Emergency: Authoritative

Design Principles:
- State-based control (no numeric optimization dependency)
- Local-first stability
- Gossip-assisted adaptation
- Light reservation (Token/Budget model)

Resolver is not the execution engine of routing,
but the accountable decision authority.
Resolver SHALL NOT execute operations.
It SHALL output constraints and decisions to the system.
Resolver is not continuously active; it operates as an intervention-based decision module.
Resolver outputs SHALL be interpreted as constraints, not execution commands.

---

## 2. Authority Model

### 2.1 Advisory Mode (CALM / WARM / HOT)

Resolver outputs:
- Recommend{path_id, queue_id, rate_hint}
- Optional Token{class, scope, ttl}
- ReasonCodes[]

Switching Core performs final execution.

### 2.2 Authoritative Mode (EMERGENCY)

Resolver outputs:
- Enforce{FreezeRoutes, Quarantine, Allow/Deny, Cap}
- Budget stage override
- TokenRules override

The execution layer is required to comply.
Enforce directives MUST take precedence over Recommend outputs.
Resolver mode SHALL be determined by the state machine (Section 3).

Resolver decisions MUST be accountable, auditable, and reproducible with deterministic ordering.
Switching Core execution MUST log Resolver directives when in Authoritative mode.

---

## 3. State Machine

State transitions are strictly stage-based.
Multi-level downward jumps are not permitted.

States:
- CALM
- WARM
- HOT
- EMERGENCY

Resolver outputs SHALL vary depending on state.
CALM is advisory-dominant, while EMERGENCY is enforcement-dominant.
In EMERGENCY, only safety-biased actions are permitted.

### 3.1 Escalation Rules

CALM → WARM:
- Local congestion or degraded link
- Fresh neighbor heat increase

WARM → HOT:
- Sustained saturation
- Link flapping
- Warning-level errors

HOT → EMERGENCY:
Two-phase lock required:
A) Local severe condition
B) Neighbor confirmation (Fresh, sufficient confidence)

### 3.2 De-escalation Rules

EMERGENCY → HOT:
- Sustained recovery of local and neighbor stability

HOT → WARM:
- Queue and link stabilized

WARM → CALM:
- Stable and quiet for sufficient duration

Hysteresis applies.

### 3.3 Deterministic Transition Guarantees

Resolver MUST guarantee:

- Predictable state transitions
- No oscillation under intermittent instability
- Bounded reaction time

Recovery thresholds MUST be stricter than escalation thresholds.
Multi-level downward jumps remain prohibited.

---

### 3.4 State-Enforced Policies

Each state automatically activates enforced control constraints.

#### CALM
- Multipath routing enabled
- Learning and prediction active
- No budget restriction

#### WARM
- Route update rate limited
- Budget upper bound reduced
- Safety margin increased
- Gossip rate slightly increased

#### HOT
- Stable path set enforced
- Non-critical traffic throttled
- Priority classes protected
- Neighbor state broadcast enabled

#### EMERGENCY
- Whitelist-only routing
- External link restriction or isolation
- Signed control-plane updates required
- Optional quarantine mode activation
- FailMode default: CLOSED

---

### 3.5 State Scope Model

State exists at multiple scopes:

- LinkState
- LocalDomainState
- NodeState

Escalation SHOULD remain localized when possible.
Global escalation is last resort.

NodeState escalates when multi-link degradation is observed OR integrity compromise is detected.

NodeState EMERGENCY SHOULD NOT be triggered solely by a single LinkState unless that link is the last surviving uplink.

---

### 3.6 Default Timing Parameters (Recommended)

T1 = 2s  
T2 = 1s  
R1 = 10s  
R2 = 30s  
R3 = 60s + authorization

Hysteresis is mandatory.

### 3.7 LinkState Update Loop (Reference Pseudocode)

This section is a reference implementation guideline.
It is NON-NORMATIVE unless explicitly stated.
LinkState feeds into LocalDomainState and NodeState aggregation logic.

// runs per link
state LinkState = CALM

loop FastLoop every 50ms:
  m = read_counters(link)
  win.update(m)            // moving window / EMA / ring buffer

loop DecisionLoop every 500ms:
  trg_warm  = win.q_occ_p95 > 0.70 for >= T1  OR win.crc_rate > WARN for >= T1
  trg_hot   = win.q_occ_p95 > 0.90 for >= T2  OR win.drop_rate > DROP_WARN for >= T2 OR win.flap_10s >= 2
  trg_em_a  = win.link_down OR win.crc_rate > FATAL OR win.flap_30s >= 3
  trg_em_b  = neighbor_confirm_fresh(link, min_stage=HOT, min_conf=CONF_MIN)

// escalation (strict stage-based)
if LinkState == HOT and trg_em_a and trg_em_b:
    LinkState = EMERGENCY; emit_state_hint()
else if LinkState == WARM and trg_hot:
    LinkState = HOT; emit_state_hint()
else if LinkState == CALM and trg_warm:
    LinkState = WARM; emit_state_hint()

// de-escalation (hysteresis)
if LinkState == EMERGENCY and stable_for(R3) and authorized():
    LinkState = HOT; emit_state_hint()
else if LinkState == HOT and stable_for(R2):
    LinkState = WARM; emit_state_hint()
else if LinkState == WARM and stable_for(R1):
    LinkState = CALM; emit_state_hint()

function stable_for(duration):
  return (win.q_occ_p95 < 0.60 AND win.drop_rate < DROP_OK AND win.crc_rate < OK AND no_flap) for >= duration

### 3.8 Neighbor Confirmation (Fresh / Confidence) — Two-Phase Lock B

#### 3.8.1 Purpose

neighbor_confirm_fresh() provides the second-phase lock for
HOT → EMERGENCY escalation.

Goals:
- Avoid single-node false-positive escalation
- Resist malicious or noisy neighbor hints
- Keep signaling lightweight (state-only sharing)

---

#### 3.8.2 Inputs and Output

Input:
- link_id
- min_stage (default: HOT)
- min_conf (default: CONF_MIN)


Output:
- Boolean (true if confirmation satisfied)

---

#### 3.8.3 StateHint Message Format

StateHint {
  sender_id
  domain_id
  stage              // CALM/WARM/HOT/EMERGENCY
  scope              // LinkState | LocalDomainState | NodeState
  target             // link_id or domain_id (recommended)
  age                // seconds since observed
  confidence         // LOW | MID | HIGH
  reason_codes[]     // optional
  nonce
  timestamp
  signature          // REQUIRED for HOT/EMERGENCY
}

Rule:
Hints with stage >= HOT MUST include valid signature.

---

#### 3.8.4 Freshness Rules

A hint is Fresh when:

age <= FRESH_MAX(stage, scope)

Recommended defaults:

HOT + LinkState: 2s  
HOT + LocalDomainState: 5s  
EMERGENCY: 5s  

If local link is flapping, freshness window SHOULD be reduced.

CONF_MIN default value: MID

FRESH_MAX and REPLAY_MAX SHOULD be implementation configurable.

---

#### 3.8.5 Confidence Model (Discrete)

Confidence levels:

LOW:
- Weak or short anomaly

MID:
- Sustained anomaly OR multiple weak anomalies

HIGH:
- Severe anomaly (link down, fatal CRC)
  OR multi-symptom sustained anomaly

Sender rule:
- EMERGENCY stage MUST use HIGH confidence.
- HOT stage SHOULD use MID or HIGH.

Receiver rule:
- Ignore hints with confidence < min_conf.

---

#### 3.8.6 Quorum Policy

Confirmation requires K distinct neighbors.

Default values:
- K = 1 (small prototype)
- K = 2 (recommended)
- K = 3 (hostile domain)

Constraints:
- Distinct sender_id required.
- At most one confirmation per domain_id.

---

#### 3.8.7 Scope Matching Rules

A confirmation is valid if:

1) Neighbor reports LinkState(stage >= min_stage) for same link
OR
2) Neighbor reports LocalDomainState(stage >= min_stage) with
   reason_codes containing INTEGRITY or WIDE_FAILURE
OR
3) Neighbor reports NodeState(stage >= min_stage) AND
   local node observes multi-link degradation

---

#### 3.8.8 Replay and Spoof Protection

Receiver MUST reject hint if:
- signature invalid (when required)
- timestamp older than REPLAY_MAX (recommended: 30s)
- nonce previously seen
- sender not in trust set (secured domains)

In unsecured domains:
- K MUST be >= 2
- domain_id filtering REQUIRED if available

---

#### 3.8.9 Normative Definition

neighbor_confirm_fresh(link, min_stage, min_conf) returns true if:

- At least K valid StateHints satisfy:
  - stage >= min_stage
  - confidence >= min_conf
  - freshness condition met
  - signature valid (when required)
  - distinct sender constraint met

Otherwise returns false.

### 3.9 Reference Pseudocode (NON-NORMATIVE)

function neighbor_confirm_fresh(link, min_stage=HOT, min_conf=CONF_MIN):

  valid = []

  for hint in inbox.hints_for(target=link.id):

    if hint.stage < min_stage:
        continue

    if hint.confidence < min_conf:
        continue

    if not is_fresh(hint):
        continue

    if hint.stage >= HOT and not verify_signature(hint):
        continue

    if is_replay(hint):
        continue

    valid.append(hint)

  valid = distinct_by_sender(valid)

  if domain_id_known:
      valid = cap_one_per_domain(valid)

  return count(valid) >= K

### 3.10 Reason Code Standardization

Reason codes SHOULD be standardized for interoperability and simulation.

Recommended base set:

FLAP              // link instability
CRC_WARN          // warning-level errors
CRC_FATAL         // fatal-level errors
SATURATION        // queue saturation
DROP_EXCESS       // sustained drop rate
INTEGRITY         // signature or security anomaly
WIDE_FAILURE      // multi-link degradation
LOCAL_ONLY        // confined local anomaly

Rules:
- reason_codes are informational and MUST NOT override stage logic.
- Multiple reason_codes MAY be included.
- EMERGENCY stage MUST include at least one reason_code.

### 3.11 Simulation Scoring Model (NON-NORMATIVE)

This section defines a simulation-only evaluation model.
It does NOT modify Resolver's normative stage-based control logic.

Resolver operational decisions remain stage-based.
The scoring model is used exclusively for:

- Threshold tuning
- Stability analysis
- Flapping tolerance evaluation
- Change pressure assessment

---

#### 3.11.1 Purpose

The scoring model quantifies instability pressure
without altering stage transition rules.

It allows controlled experimentation with:

- Link flapping intensity
- Reroute frequency
- Token issuance pressure
- Emergency escalation timing

This model MUST NOT be interpreted as a numeric optimizer.

---

#### 3.11.2 Window Definition

Simulation window:

WINDOW = 10 seconds (recommended)

Metrics are evaluated per window.

---

#### 3.11.3 Input Counters (Per Window)

F = link state transitions (UP↔DOWN count)

R = reroute executions

T = token issued count

---

#### 3.11.4 Scoring Formula (Aggressive Profile v1)

Scoring formula (Aggressive Profile v1):

S = F + 2R + 1.5T

Where:

- F captures physical instability
- R captures routing instability
- T captures control-plane pressure

The weight of T reflects change pressure sensitivity.

---

#### 3.11.5 State Mapping (Simulation Only)

CALM        : S ≤ 2
WARM        : 3 ≤ S ≤ 5
HOT         : 6 ≤ S ≤ 9
EM_CANDIDATE: S ≥ 10

---

#### 3.11.6 Emergency Confirmation (Simulation)

EMERGENCY is entered when:

- S ≥ 10 for two consecutive windows

This simulation rule does NOT override
the normative two-phase lock mechanism defined in Section 3.1.

Normative escalation rules remain authoritative.

---

#### 3.11.7 Observed Behavioral Properties (Prototype Results)

Prototype simulation produced the following separation:

- Light flap (F ≤ 2, T minimal):
  Stable in CALM.

- Moderate flap (F ≈ 4, low T):
  Temporary HOT, self-recovery.

- Heavy flap (F ≥ 8):
  HOT → EMERGENCY after 2 windows.

- Control-plane thrash (low F, high T):
  EMERGENCY triggered when sustained.

- Mild control fluctuation:
  Remains HOT without EM escalation.

This demonstrates clear stage separation
without excessive sensitivity.

---

#### 3.11.8 Design Interpretation

The scoring model reveals:

- Token pressure is a meaningful early-warning signal.
- Physical instability and control instability must both be observable.
- Aggressive Token weighting improves early containment
  in data-center-class environments.

T weight MAY be tuned per deployment profile.

---

#### 3.11.9 Constraints

- This model MUST NOT replace stage-based logic.
- It MUST NOT introduce numeric optimization dependency.
- It MUST remain optional and simulation-bound.

### 3.12 Event Propagation Model

Resolver communication follows an event-driven propagation model.

Under normal operating conditions, PSC nodes SHOULD NOT generate
periodic control traffic for global synchronization.

State information is propagated only when instability events occur.

---

#### 3.12.1 Primary Propagation Scope

When a node detects a local instability event
(congestion, queue overflow, link degradation, etc.),
the event SHOULD first be propagated only to
directly connected neighboring PSC nodes.

This one-hop propagation enables rapid local coordination
while keeping the control plane quiet during stable operation.

---

#### 3.12.2 Extended Propagation

Propagation beyond one hop is permitted only when:

- the system state reaches HOT or EMERGENCY
- local containment fails
- multi-domain instability is detected

In such cases, events MAY propagate to the next hop
to coordinate broader stabilization responses.

---

#### 3.12.3 Distance-Based Influence

Event influence MUST decay with propagation distance.

Neighbor nodes treat received events as actionable signals,
while nodes further away SHOULD treat them as advisory hints.

This mechanism prevents unnecessary global reactions
to localized disturbances.

---

#### 3.12.4 Global Escalation

Network-wide propagation SHOULD be avoided
during normal operation.

Global stabilization actions SHOULD only occur when:

- EMERGENCY states propagate across multiple domains, or
- designated coordinating nodes determine wider intervention
  is required.

This design preserves PSC's "quiet network" philosophy
while still allowing rapid response to large-scale failures.

---

## 4. Reservation Model (Light)

Budget/Token governs admission and change pressure, not continuous rate control.
rate_hint is advisory and MAY be clamped by the execution layer under constrained Budget.

Hard rate limiting, if required, SHALL be expressed via Enforcement (e.g., Cap/Throttle), not via Budget.

This reservation model is not designed for bandwidth guarantees,
but for overload propagation containment.
Token and Budget SHALL be interpreted as constraints by the execution layer.

### 4.1 Budget (Stage-Based)

Budget[class] ∈ {STOP, LOW, MID, HIGH}

Default by state:

CALM:
- All HIGH

WARM:
- BULK = MID

HOT:
- BULK = LOW
- INTERACTIVE = MID

EMERGENCY:
- SYSTEM = HIGH
- REALTIME = MID
- INTERACTIVE = LOW
- BULK = STOP

### 4.2 Token Usage

Token required for:
- NewFlow
- Reroute
- Burst
- Recovery

Token is permission, not guarantee.

TTL is enforced.

---

## 5. Candidate Generation

Candidate set C is defined as: Fixed ∪ Gossip (Fresh/Valid)

### 5.1 Fixed Paths
Predefined:
- PathA (low latency)
- PathB (load avoidance)
- PathC (trust priority)

### 5.2 Gossip Paths

GossipHint includes:
- prefer_path
- avoid_link
- stage
- age
- confidence

Freshness filtering:
- REALTIME: short expiration
- BULK: longer tolerance

### 5.3 Emergency Mode

Only Fixed paths are used.
Gossip influence is minimized.

---

## 6. Scoring Model (Lexicographic)

This model avoids numeric optimization and prioritizes safety through lexicographic ordering.
This model SHALL NOT replace Resolver decision logic.

1. SafetyRank
2. StabilityRank
3. LoadRank
4. PreferenceRank

Sticky routing is preferred.

Sticky routing SHALL preserve existing flow-to-path bindings
unless safety or enforcement constraints require change.

Sticky preference MUST NOT override SafetyRank ordering.

---

## 7. Enforcement Set (Emergency Only)

Enforcement is applied with minimal necessary scope.
All enforcement actions are derived from Resolver Authoritative decisions.

- FreezeRoutes(scope, duration)
- Quarantine(target, mode)
- Allow/Deny class control
- Cap(class, stage)

FailMode default: CLOSED

---

## 8. Anti-Chatter Mechanisms

- Hysteresis on state transition
- Sticky flow preservation
- Reroute cooldown
- Gossip aging weight reduction

---

## 9. Future Work

- Simulation parameter tuning
- Token TTL optimization
- Budget mapping calibration
- Security boundary formalization

---

## 10. Decision Guarantees

Resolver MUST operate under strict deterministic decision principles.
 - Resolver MUST be deterministic.
 - The same input conditions MUST always produce the same output.
 - The decision order MUST be fixed and reproducible.
 - Resolver MUST NOT produce undefined or ambiguous outcomes.

### 10.1 Fallback Requirement

If the candidate set becomes empty at any stage of decision:
 - Resolver MUST perform a deterministic fallback action.

Fallback behavior SHALL be defined as:
 - Advisory mode:
    - Hold (no new changes applied)
 - Authoritative mode:
    - Closed or enforced safe-state operation

Resolver MUST ensure that no decision cycle results in an undefined state.

### 10.2 Deterministic Decision Order

Resolver MUST apply a strictly defined decision order during each decision cycle.
 - All filtering, constraint application, and selection steps MUST be executed in a predefined sequence.
 - The order MUST be consistent across all implementations.
 - Reordering of decision stages MUST NOT change the final outcome.

---

## 11. Auditability

All Resolver decisions MUST be fully auditable and reproducible.

### 11.1 Logging Requirements

Resolver MUST record decision logs for every decision cycle.
In Authoritative mode, logging is mandatory and MUST NOT be skipped.

Each log entry MUST include:
 - Input state:
    - Fabric state
    - Telemetry data (abstracted form)
    - Policy constraints
    - Trust-related inputs (if applicable)
 - Candidate set before filtering
 - Filtering and constraint application steps
 - Final decision output
 - ReasonCodes associated with the decision

### 11.2 Reproducibility

Resolver decisions MUST be reproducible from logs.
 - Given the same recorded inputs, the decision process MUST yield the same result.
 - Logs MUST contain sufficient information to replay the decision process.
 - Replay MUST follow the same deterministic decision order defined in Section 10.

### 11.3 Accountability

Resolver decisions MUST be accountable.
 - Each decision MUST be traceable to its input conditions and applied constraints.
 - The system MUST be able to explain why a specific decision was made.
 - In Authoritative mode, enforced actions MUST be traceable to Resolver directives.

---

End of v0.1

## Release Notes (v0.1 FINAL)
- Stage-based Resolver core defined (CALM/WARM/HOT/EMERGENCY)
- Two-phase lock for HOT→EMERGENCY specified
- LinkState reference loop added (NON-NORMATIVE)
- Simulation Scoring Model added (NON-NORMATIVE, Aggressive Profile v1)
- Event propagation model added (event-driven, distance-decayed)
