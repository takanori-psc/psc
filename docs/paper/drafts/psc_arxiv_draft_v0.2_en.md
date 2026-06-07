# PSC: A Trust-Aware Stabilization Architecture for High-Bandwidth Computing Fabrics

T. Hirose

Draft v0.2 for arXiv-style submission

## Abstract

Modern computing systems increasingly depend on high-bandwidth communication among CPUs, GPUs, memory devices, storage, accelerators, and network interfaces. As device-level parallelism and data movement continue to increase, CPU-centric communication management and purely performance-driven routing become increasingly exposed to congestion, unstable links, routing oscillation, and cascading failure modes. This paper presents PSC (Photon System Controller), a fabric-centric communication control architecture that separates communication management from the CPU and introduces trust-aware, state-based routing stabilization inside the fabric.

PSC is built around three separable functions: transfer management, routing control, and transfer execution. Its Routing Control Unit (RCU) performs fast local route evaluation, while a higher-level Resolver arbitrates ambiguous, degraded, or policy-conflicting decisions. Unlike routing approaches that continuously chase the highest instantaneous score, PSC distinguishes the best currently scored path from the selected operational path and applies hysteresis, trust validation, recovery guards, and cooldown rules to prevent unnecessary switching.

We describe the PSC architecture, the RCU decision model, the Resolver arbitration model, the telemetry and trust assumptions, and a restricted Fast Mode security boundary for trusted local high-speed communication. Controlled simulations show that PSC suppresses route oscillation compared with an ECMP-like score-following baseline: in one unstable-path scenario, the baseline switches 9 times in 10 steps, whereas PSC switches once and then holds a stable route. Additional simulations validate degraded-mode fallback and staged recovery return. These results are preliminary but demonstrate the central design claim: PSC prioritizes fabric stability, explainability, and controlled recovery over short-term performance maximization.

## 1. Introduction

High-performance computing systems are increasingly dominated by data movement. CPUs, GPUs, memory pools, NVMe devices, accelerators, and network interfaces exchange data at rates that continue to grow faster than traditional host-centric control models were designed to handle. In many conventional systems, the CPU or CPU-managed DMA engines remain responsible for initiating, supervising, or coordinating a significant portion of data movement. This model is increasingly strained by always-on AI workloads, GPU-to-GPU communication, high-speed storage, and low-latency network fabrics.

PSC proposes a different architectural direction: communication management should become a first-class function of the fabric itself. Rather than treating the interconnect as a passive transport medium, PSC treats it as an active control layer that can evaluate state, select routes, enforce policy, contain faults, and recover from degradation without continuous CPU intervention.

The central design philosophy of PSC is not to maximize instantaneous throughput at every step. Instead, PSC aims to maintain stable, explainable, and policy-consistent communication under changing conditions. This is especially important in large or heterogeneous fabrics where reacting too aggressively to short-term score changes can cause route oscillation, instability, and cascading control behavior.

This paper makes four contributions:

1. It proposes PSC, a fabric-centric communication controller architecture separating transfer management, route control, and transfer execution.
2. It defines an RCU decision model that separates candidate filtering, route scoring, switching decisions, degraded fallback, and recovery.
3. It defines the Resolver as an explainable arbitration layer for ambiguity, trust conflict, policy conflict, degraded operation, and recovery return.
4. It presents controlled simulation results showing reduced oscillation, safe degraded fallback, and staged recovery behavior.

## 2. Motivation and Problem Statement

High-bandwidth computing fabrics face several recurring control problems:

- local and fabric-wide congestion;
- unstable or flapping links;
- routing oscillation caused by over-reactive path selection;
- policy and security boundary conflicts;
- trust degradation of nodes, links, or telemetry sources;
- unsafe or premature recovery after faults;
- propagation of local failures into fabric-wide instability.

Traditional routing and load-balancing methods often emphasize reachability, shortest path, cost minimization, or load distribution. These are necessary but insufficient when the fabric is unstable. A path with the best instantaneous score may be a poor operational choice if it has low trust, high variance, or recent failure history. Similarly, a recovered path should not automatically regain traffic until its recovery has been validated.

PSC therefore frames routing as a stability-preserving control problem rather than a pure optimization problem. The fabric must be able to say not only "which path is best now" but also "whether switching now is safe."

## 3. PSC Architecture

PSC is a dedicated communication management unit for computing systems and high-bandwidth fabrics. It can be implemented as an expansion card, chipset-integrated controller, CPU-integrated controller, dedicated processor, or future optical-fabric controller.

The main PSC components are:

- Transfer Management Unit (TMU): manages transfer requests, priority, scheduling, and transfer context.
- Routing Control Unit (RCU): evaluates route candidates and controls path selection, switching, degraded fallback, and recovery.
- Transfer Execution Unit (TEU): executes data movement over selected paths.
- Interconnect Interface (ICI): connects PSC to electrical and optical interconnects.
- Optical Monitoring Unit (OMU): monitors optical link health, power, temperature, error rates, retraining, and lifecycle degradation.
- Control Interface: receives initial configuration and management commands from the CPU or management layer.
- Resolver: arbitrates high-level decisions when RCU output is ambiguous, conflicting, degraded, or recovery-related.

The role separation is intentional:

```text
TMU      = time control and scheduling
RCU      = spatial control and route selection
Resolver = high-level arbitration
TEU      = transfer execution
```

PSC does not require the CPU to continuously manage normal data movement. The CPU configures and supervises the PSC, while PSC performs autonomous fabric-level communication control.

## 4. Transfer and Addressing Model

PSC uses a receiver-driven, chunk-based transfer model. A transfer proceeds through states such as REQUESTED, EVALUATING, GRANTED, SCHEDULED, ACTIVE, RETRY, COMPLETING, COMPLETED, ABORTED, or FAULTED. The destination side participates in authorization and flow control before data transmission proceeds.

PSC native addresses are modeled as 64-bit hierarchical fabric addresses:

```text
Fabric ID : Cluster ID : Node ID : Port ID
16 bits   : 16 bits    : 24 bits : 8 bits
```

This address structure supports routing at fabric, cluster, node, and port scope. The packet structure includes routing information, security tags, transfer control fields, chunk descriptors, and payload data.

## 5. RCU Decision Model

The RCU performs normal routing decisions. Its core pipeline is:

```text
Candidate Filtering
-> Score Evaluation
-> Switching Decision
-> Degraded / Recovery Handling
```

### 5.1 Candidate Filtering

Before scoring, unusable paths are rejected. Rejection conditions include:

- trust violation;
- node failure;
- policy violation;
- hard stale telemetry;
- route unavailable.

If no trusted path remains, the RCU either enters a degraded decision path or escalates to the Resolver.

### 5.2 Route Scoring

PSC evaluates multiple route dimensions:

- congestion score;
- performance score;
- stability score;
- trust;
- health;
- policy compatibility;
- telemetry confidence.

The clarified baseline RCU decision model uses `FinalScore` for normal
candidate selection. Its core components are congestion benefit and
performance:

```text
CongestionBenefit(path) = 1 - CongestionScore(path)

FinalScore(path) =
  Wc * CongestionBenefit(path) +
  Wp * PerformanceScore(path)
```

`Wc` and `Wp` are implementation parameters. They are not fixed constants
of the architecture.

`StabilityScore` is not a primary component of the normal `FinalScore`.
Instead, PSC treats stability as a control signal for hysteresis,
eligibility, Resolver arbitration, and Recovery return decisions. The key
architectural principle is that performance is not the only determinant, even
when normal candidate ranking is based on congestion benefit and performance.

### 5.3 Best Path vs. Selected Path

PSC explicitly separates:

- Best Path: the currently highest-scored candidate;
- Selected Path: the path actually used by the fabric.

These may differ. PSC allows the selected path to remain active when the best path only marginally improves the score, when switching would cause instability, or when recovery has not been validated.

### 5.4 Switching Rule

The RCU does not switch immediately when a better-scored path appears. A simplified switching rule is:

```text
If Improvement > switch_margin
AND StabilityScore(SelectedPath) < switch_stability_threshold
AND persistence_degradation(SelectedPath) > persistence_limit
then SWITCH
else KEEP
```

This expresses the stability-first behavior: short-term score improvement is insufficient by itself.

## 6. Resolver Arbitration Model

The Resolver is the high-level decision layer of PSC. It does not replace the RCU. It is invoked when the RCU decision is insufficient, ambiguous, or unsafe.

The core principle is:

```text
RCU tentative decision != Resolver final decision
```

The Resolver is activated under conditions such as:

- no valid trusted route;
- policy conflict;
- degraded-only candidate set;
- repeated switching without convergence;
- unstable telemetry confidence;
- small score gap with large trust or stability gap;
- recovery candidate ambiguity.

The Resolver input includes:

```text
TransferRequest {
  src, dst, class, qos, deadline
}

CandidatePaths {
  path_id, hops, link_ids, node_ids,
  base_cost, estimated_cost, current_rank
}

TelemetrySummary {
  congestion_score, health_state,
  availability_state, trust_score_ref,
  scope_level, confidence
}

RoutingPolicyContext {
  mode, hysteresis_margin, trust_mode,
  degraded_mode_allowed, recovery_preference
}

RCUContext {
  selected_path_id, best_path_id,
  tentative_decision, escalation_reason
}
```

The Resolver output is:

```text
ResolverDecision {
  final_decision_type
  selected_path_id
  rationale {
    type
    details
  }
  override_policy {
    degraded_mode
    trust_exception
    recovery_hold
  }
}
```

Decision types include:

```text
KEEP
SWITCH
DEGRADED_SWITCH
NO_ROUTE
HOLD
RETURN
```

A typical arbitration trigger is:

```text
ESCALATE if:
score_gap < epsilon
AND (
  trust_gap > trust_conflict_threshold
  OR
  stability_gap > stability_conflict_threshold
)
```

This condition captures the central Resolver function: when ordinary scores are too close to justify a purely numeric decision, trust and stability become decisive.

## 7. Telemetry and Trust

PSC treats telemetry as evidence, not as absolute truth. Telemetry data is associated with:

- value;
- confidence;
- freshness;
- source reliability.

PSC may decay stale telemetry instead of immediately discarding it:

```text
weight = confidence * exp(-lambda * Age)
```

Trust is also broader than security authentication. PSC trust includes:

- stability;
- behavioral predictability;
- observability;
- policy consistency;
- recovery reliability;
- operational integrity.

This allows PSC to reject or penalize paths that are technically reachable but operationally unsafe.

## 8. Operation Modes and State Transitions

PSC uses operation modes to constrain routing behavior:

- NORMAL: trusted paths only; hysteresis enabled; degraded fallback prohibited.
- TRUST_FAILURE: trusted route unavailable; Resolver escalation occurs.
- DEGRADED: Resolver-authorized fallback; limited or untrusted routes may be used under policy.
- RECOVERY: trusted route has reappeared but must be validated before normal return.

At the broader fabric level, PSC also uses a state model:

```text
CALM -> WARM -> HOT -> EMERGENCY
```

Recovery is staged rather than immediate:

```text
EMERGENCY -> HOT -> WARM -> CALM
```

This state machine limits oscillation and prevents aggressive recovery.

## 9. Fast Mode Security Boundary

PSC includes a restricted Fast Mode for trusted local high-speed communication. Fast Mode is not a general routing optimization feature. It is a secure local high-speed region with strict boundaries.

Fast Mode is allowed only when conditions such as the following hold:

- one-hop PSC connectivity;
- same secure domain;
- trusted local devices;
- Resolver authorization;
- traceability;
- no forwarding into the general routing fabric.

Allowed examples include CPU-GPU direct communication, CPU-NVMe local communication, trusted local GPU fabric, trusted accelerator fabric, and local memory fabric.

Forbidden cases include:

- multi-hop Fast Mode;
- cross-rack Fast Mode;
- Internet-routed Fast Mode;
- unauthenticated device participation;
- Resolver bypass;
- autonomous GPU mesh expansion;
- unmanaged inter-domain bridging.

Fast Mode illustrates the PSC philosophy: even high-speed paths must remain bounded by trust, domain control, and recovery mechanisms.

## 10. Evaluation

PSC has been evaluated through controlled Python simulations in the repository. These simulations are not hardware benchmarks. They validate decision behavior: oscillation suppression, degraded fallback, recovery hold, recovery return, and Resolver arbitration.

### 10.1 Oscillation Scenario

Scenario:

- Path B has higher performance but fluctuates periodically.
- Path A is slightly slower but more stable.
- The baseline selects the highest current score in an ECMP-like manner.
- PSC applies Resolver arbitration, hysteresis, and cooldown.

Observed result:

| Method | Switches in 10 steps |
|--------|----------------------|
| ECMP-like baseline | 9 |
| PSC | 1 |

The baseline reacts to short-term fluctuations and repeatedly changes paths. PSC switches once from the unstable path to the stable path, then suppresses further oscillation.

### 10.2 Degraded Rule Validation

Scenario:

- The selected path becomes untrusted.
- RCU rejects the path due to low trust.
- PSC enters DEGRADED behavior and switches to a safe fallback.
- Recovery cooldown prevents immediate instability after recovery.

Observed behavior:

```text
TRUST_LOW -> SELECTED_REJECTED
-> RULE-07_DEGRADE_trigger
-> RULE-09_DEGRADE_switch
-> RULE-11_RECOVERY_cooldown
```

This validates that degraded operation is a controlled exception, not undefined routing behavior.

### 10.3 Recovery Return

PSC v0.1 uses conservative recovery hold: after fallback, it does not immediately return to a recovered path merely because that path becomes high scoring again.

PSC v0.2 introduces staged return:

```text
RECOVERY_CANDIDATE
-> VALIDATION
-> RETURN_ELIGIBLE
-> RETURN_SWITCH
-> COOLDOWN
```

In the recovery return simulation, the recovered path returns only after validation and sufficient improvement.

### 10.4 Multi-Candidate Recovery

In multi-candidate recovery, PSC separates recovery-oriented selection from baseline score selection:

```text
return_score != final_score
```

The simulation shows:

- return_score selects a more stable candidate C;
- final_score prefers higher-performance candidate B;
- Resolver arbitrates the conflict and selects C.

This validates the design separation:

```text
RCU return_score      = recovery candidate generator
RCU final_score       = baseline evaluator
Resolver arbitration  = final conflict resolution
```

## 11. Discussion

PSC is intentionally conservative. It may preserve a stable path even when another path has a temporarily better score. This is not a defect but a design choice: PSC values operational continuity, explainability, and bounded recovery over immediate score maximization.

The simulations suggest that this approach can suppress oscillation and make degraded and recovery behavior auditable. The logs are rule-based, which means each decision can be traced to conditions such as TRUST_LOW, SELECTED_REJECTED, ESCALATE_CONFLICT, RECOVERY_CANDIDATE, RETURN_ELIGIBLE, or COOLDOWN_ACTIVE.

PSC is especially relevant for:

- GPU-rich systems;
- AI/HPC clusters;
- rack-local accelerator fabrics;
- disaggregated memory and storage systems;
- future optical interconnects;
- fabrics requiring explicit security and trust boundaries.

## 12. Limitations

This work is currently architectural and simulation-based. It does not yet provide:

- hardware implementation results;
- optical link measurements;
- large-scale topology benchmarks;
- formal stability proofs;
- comparison against production data-center control planes;
- complete security proofs for Fast Mode;
- standardized coefficient selection for all scoring functions.

The current simulations validate control behavior, not absolute performance.

## 13. Future Work

Future work includes:

- large-scale simulations with realistic topologies;
- formal analysis of hysteresis and cooldown stability;
- integration with optical link telemetry;
- hardware-oriented RCU and Resolver prototypes;
- Fast Mode security validation;
- policy language formalization;
- workload-driven evaluation for AI/HPC and disaggregated systems.

## 14. Conclusion

PSC is a fabric-centric communication control architecture for high-bandwidth computing systems. Its main contribution is not a new shortest-path algorithm, but a control structure that separates fast local routing decisions from higher-level arbitration. The RCU handles normal route evaluation, while the Resolver handles ambiguity, trust conflict, degraded operation, and recovery.

The key architectural insight is that the best-scored path and the safest operational path are not always the same. By combining telemetry confidence, trust, hysteresis, Resolver arbitration, degraded fallback, and staged recovery, PSC provides a path toward communication fabrics that are not merely fast, but stable, explainable, and controllable.

## Appendix A. Reproducibility Notes

The simulations referenced in this draft correspond to the repository paths:

- `sim/02_controlled/03_oscillation/mini_psc_rcu_decision_v01_oscillation.py`
- `sim/02_controlled/04_degraded/mini_psc_rcu_decision_v01_degraded.py`
- `sim/02_controlled/05_recovery_hold/mini_psc_rcu_decision_v01_recovery.py`
- `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v02_recovery.py`

Representative logs:

- `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md`
- `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md`
- `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_vs_v01_recovery_hold_log.md`
- `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_multi_candidate_validation_log.md`

## Appendix B. Internal Specification Sources

This draft is derived from the PSC specification documents in the repository, including:

- PSC Architecture Specification v1.0
- PSC RCU Decision Model v0.1
- PSC Routing Control Unit Specification v0.1
- PSC Resolver Model v0.2
- PSC Resolver Arbitration Extension Model v0.2.x
- PSC Telemetry Model v0.2
- PSC Trust Model v0.1
- PSC State Transition Model v0.1
- PSC Fast Mode Security Boundary Model v0.1
- PSC Transfer Flow v0.1
- PSC Address Format v0.1
- PSC Fabric Packet Structure v0.1
