## v11 - Trust Failure Handling + Resolver-managed Degraded Fallback

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection + Trust Failure Recovery

- Feature:
  - Kept `TRUST_MODE = require_trusted` as the normal operating mode
  - Explicitly detects trust failure when no trusted path exists
  - Allows Resolver intervention only when needed
  - Transitions operation mode from `NORMAL` to `DEGRADED`
  - Temporarily enables untrusted fallback
  - Logs trust failure / resolver override / degraded mode / fallback reason

- Result:
  - Success:
    - Introduced a structure that explicitly detects trust failure under strict trust constraints
    - Implemented the basic behavior of Resolver-managed degraded fallback when no trusted path exists
    - Confirmed a design direction that extends `require_trusted` from hard stop behavior into controlled exception handling
    - Added an operational recovery layer on top of trust / policy / resolver

  - Observations:
    - In all steps, the primary route search returned `NO ROUTE` under the `TRUSTED_ONLY` condition
    - After trust failure was detected, the Resolver enabled override and allowed untrusted fallback
    - At Step 1, operation mode transitioned from `NORMAL` to `DEGRADED`
    - Even while degraded mode remained active, route re-selection continued,
      and fallback route switching occurred at Step 5 / Step 6
    - The `NO_ROUTE` behavior seen in v10b could be transformed into controlled degraded recovery in v11

  - Issues:
    - During degraded mode, route switching currently prioritizes fallback route reselection,
      so the application boundary of stability / latency policy is still rough
    - Exit conditions for degraded mode are not yet implemented
    - Fallback permission conditions are currently simple rules and are not yet policy-specific
    - Penalty or trust weight for fallback routes has not yet been introduced

- Next:
    - Organize how policy / resolver should be reapplied during degraded mode
    - Add recovery conditions from degraded mode back to normal mode
    - Introduce penalty / trust weight for fallback routes
    - Clarify how the difference between stability / latency appears during degraded mode

### v11 - Policy: stability / Trust mode: require_trusted (Execution Log)

```text
Policy: stability
Trust mode: require_trusted

=== Policy-aware Routing Simulation v11 ===
Source: nodeA
Destination: nodeF
Policy: stability
Initial trust mode: require_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: UNTRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: SELECT
Policy phase: initial selection after degraded fallback
Resolver phase: override enabled
Final reason: degraded fallback route selected
Fallback reason: preserve connectivity

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=3, improvement=0, policy=stability

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=3, improvement=0, policy=stability

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: BUSY
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=8, best_cost=5, margin=3, improvement=3, policy=stability
```

- Insight:
    - strict trust constraints can drive the system into NO_ROUTE
    - in v11, Resolver-managed degraded fallback allows trust failure to be handled as controlled exception processing instead of a hard stop
    - PSC Routing extends beyond route selection into operational recovery under trust constraint violation
    - the introduction of degraded mode suggests that reachability preservation and control continuity may be achieved together

---

### v11 - Policy: latency / Trust mode: require_trusted (Execution Log)

```text
Policy: latency
Trust mode: require_trusted

=== Policy-aware Routing Simulation v11 ===
Source: nodeA
Destination: nodeF
Policy: latency
Initial trust mode: require_trusted
Hysteresis Margin: 0
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: UNTRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: SELECT
Policy phase: initial selection after degraded fallback
Resolver phase: override enabled
Final reason: degraded fallback route selected
Fallback reason: preserve connectivity

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=0, improvement=0, policy=latency

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=0, improvement=0, policy=latency

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=0, improvement=0, policy=latency

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=0, improvement=0, policy=latency

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: BUSY
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=8, best_cost=5, margin=0, improvement=3, policy=latency
```
- Insight:
    - strict trust constraints can drive the system into NO_ROUTE
    - in v11, Resolver-managed degraded fallback allows trust failure to be handled as controlled exception processing instead of a hard stop
    - under degraded mode, fallback route reselection currently dominates route switching behavior in both stability and latency policies
    - this suggests that degraded mode needs its own explicit policy boundary instead of relying only on normal-mode policy semantics


