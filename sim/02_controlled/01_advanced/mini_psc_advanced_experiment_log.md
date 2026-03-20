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

---

## v12 - Degraded Mode Policy Refinement

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection + Trust Failure Recovery + Degraded Mode Policy Refinement

- Feature:
  - Kept `TRUST_MODE = require_trusted`
  - Detects trust failure when no trusted route is available
  - Allows degraded fallback through Resolver override
  - Introduced a dedicated switching margin for degraded mode
  - Introduced a penalty for untrusted fallback routes
  - Added a recovery condition to return from `DEGRADED` to `NORMAL` when a trusted route is available for multiple consecutive steps
  - Added a structure in which degraded mode has its own decision boundary, separate from normal stability / latency behavior

- Result:
  - Success:
    - Implemented a dedicated route switching policy for degraded mode
    - Implemented a basic structure that applies a penalty to untrusted fallback routes
    - Implemented recovery control from `DEGRADED` back to `NORMAL` when a trusted route becomes stably available again
    - Represented trust failure / degraded fallback / degraded switching / normal recovery as a single continuous control flow

  - Observations:
    - At Step 1 / Step 2, the trusted route `A-B-D-F` was selected, and the system operated as normal `NORMAL` mode routing
    - At Step 3, the trusted route was lost, trust failure was detected, the Resolver enabled override, and the system transitioned from `NORMAL` to `DEGRADED`
    - At Step 3, even with fallback penalty applied, the improvement was large enough that degraded mode policy triggered a `DEGRADED_SWITCH` to `A-C-E-F`
    - At Step 4, the fallback candidate changed, but improvement was 0, so the decision remained KEEP, showing that the degraded-mode-specific switching boundary was functioning
    - At Step 5, the trusted route became available again, but because the recovery counter was only 1/2, the system did not immediately return to normal mode and instead remained in degraded mode while switching to a better route
    - At Step 6, trusted route availability reached 2 consecutive steps, and recovery from `DEGRADED` to `NORMAL` was triggered
    - In v11, once the system entered degraded mode, fallback reselection tended to dominate behavior, but in v12, degraded mode gained its own switching policy and recovery condition

  - Issues:
    - The fallback penalty is still a fixed value and has not yet been made adaptive based on trust severity or node risk
    - The recovery condition is based on a simple consecutive-step rule and is still rough as a stability criterion
    - The priority design for cases where a trusted route returns during degraded mode can still be refined further
    - It is still unverified how degraded switch margin and recovery conditions behave under `latency` policy

  - Next:
    - Extend fallback penalty into trust weight / risk weight
    - Improve degraded recovery conditions using throughput / stability / trust confidence
    - Run v12 under `latency` policy and compare degraded-mode behavior differences
    - Define degraded mode not merely as an exception state, but as a controlled operational mode

- Execution Log:

### v12 - Policy: stability / Trust mode: require_trusted (Execution Log)

```text
=== Policy-aware Routing Simulation v12 ===
Source: nodeA
Destination: nodeF
Policy: stability
Initial trust mode: require_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2
Degraded switch margin: 2
Degraded fallback penalty: 2
Recovery required steps: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: TRUSTED
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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial trusted route selected

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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=8, best_cost=8, margin=3, improvement=0, policy=stability, operation_mode=NORMAL

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: CONGESTED
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
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 16

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
Decision: DEGRADED_SWITCH
Policy phase: improvement=9, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=16, best_cost=7, margin=3, improvement=9, policy=stability, operation_mode=DEGRADED

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: CONGESTED
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
  Route: ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 9
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9
Decision: KEEP
Policy phase: no improvement
Resolver phase: degraded mode policy applied
Final reason: Keep current degraded route
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=9, margin=3, improvement=0, policy=stability, operation_mode=DEGRADED

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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 1/2
  Recovery decision: STAY_DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: improvement=3, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=6, margin=3, improvement=3, policy=stability, operation_mode=DEGRADED

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 2/2
  Recovery decision: RESTORE_NORMAL
  Operation mode: DEGRADED -> NORMAL

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability, operation_mode=NORMAL
```
- Insight:
    - In v12, degraded mode began to be treated not merely as a fallback state, but as a control mode
      with its own switching margin and recovery condition
    - Even under trust failure, reachability could be preserved, and once a trusted route became stably
      available again, the system could return to normal mode
    - The introduction of fallback penalty suggests a direction in which untrusted routes are not
      completely forbidden, but treated as disadvantaged candidates
    - PSC Routing is evolving beyond route selection / trust control / resolver intervention toward
      multi-layer control that also includes operational mode transition

---

## v12c - Degraded Mode Policy Boundary Comparison

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection + Trust Failure Recovery + Degraded Mode Boundary Comparison

- Feature:
  - Kept `TRUST_MODE = require_trusted`
  - Detects trust failure when no trusted route is available
  - Allows degraded fallback through Resolver override
  - Introduced a boundary-case scenario to compare policy behavior inside degraded mode
  - Intentionally created an `improvement = 1` comparison at Step 4
  - Verified whether stability policy and latency policy produce different decisions under degraded mode
  - Continued validating degraded-mode route switching and normal recovery flow

- Result:
  - Success:
    - Clearly demonstrated policy-boundary differences inside degraded mode
    - Successfully created an `improvement = 1` condition at Step 4
    - Under stability policy, the system kept the current route for a small improvement
    - Under latency policy, the system performed `DEGRADED_SWITCH` under the same condition
    - Confirmed that policy characteristics affect actual route switching behavior even during degraded mode

  - Observations:
    - At Step 3, after trust failure detection, Resolver override triggered `NORMAL -> DEGRADED`, and fallback route `A-C-E-F` was selected
    - In v12c / stability Step 4, `current_cost = 9`, `best_cost = 8`, and `improvement = 1`, and because `degraded_margin = 2`, the decision was KEEP
    - In v12c / latency Step 4, the same `current_cost = 9`, `best_cost = 8`, and `improvement = 1` condition appeared, but because `degraded_margin = 0`, `DEGRADED_SWITCH` was triggered
    - This confirms that, even under degraded mode, stability preserves the current route for small improvements, while latency switches immediately to the better route
    - At Step 5 / Step 6, trusted-route return and `DEGRADED -> NORMAL` recovery also continued to work correctly
    - The degraded mode introduced in v12 was shown in v12c to be not merely a fallback state, but a policy-sensitive control mode

  - Issues:
    - Fallback penalty is still fixed and has not yet been extended into dynamic weighting based on trust severity or route risk
    - Recovery condition is still based on consecutive-step count and could be improved using throughput or trust confidence
    - This comparison is based on a single boundary case and should be revalidated under multiple load patterns and more complex topologies
    - The effect of trust weight / risk weight in degraded-mode route comparison remains a future verification target

  - Next:
    - Extend fallback penalty into adaptive trust weight / risk weight
    - Improve degraded recovery conditions using throughput / stability / trust confidence
    - Validate degraded policy boundaries under more complex topologies and multi-route candidate conditions
    - In v13, introduce trust / risk weighting and move fallback evaluation beyond a fixed penalty model

- Execution Log:

### v12c - Policy: stability / Trust mode: require_trusted (Execution Log)

```text
=== Policy-aware Routing Simulation v12c ===
Source: nodeA
Destination: nodeF
Policy: stability
Initial trust mode: require_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2
Degraded switch margin: 2
Degraded fallback penalty: 2
Recovery required steps: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: TRUSTED
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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial trusted route selected

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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=8, best_cost=8, margin=3, improvement=0, policy=stability, operation_mode=NORMAL

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: CONGESTED
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
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 16

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
Decision: DEGRADED_SWITCH
Policy phase: improvement=9, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=16, best_cost=7, margin=3, improvement=9, policy=stability, operation_mode=DEGRADED

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: CONGESTED
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
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9
Decision: KEEP
Policy phase: improvement=1, degraded_margin=2 -> within degraded margin
Resolver phase: degraded mode policy applied
Final reason: Keep current degraded route
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=8, margin=3, improvement=1, policy=stability, operation_mode=DEGRADED

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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 1/2
  Recovery decision: STAY_DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: improvement=3, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=6, margin=3, improvement=3, policy=stability, operation_mode=DEGRADED

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 2/2
  Recovery decision: RESTORE_NORMAL
  Operation mode: DEGRADED -> NORMAL

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability, operation_mode=NORMAL
```

### v12c - Policy: latency / Trust mode: require_trusted (Execution Log)

```text
=== Policy-aware Routing Simulation v12c ===
Source: nodeA
Destination: nodeF
Policy: latency
Initial trust mode: require_trusted
Hysteresis Margin: 0
Resolver improvement threshold: 2
Degraded switch margin: 0
Degraded fallback penalty: 2
Recovery required steps: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: TRUSTED
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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial trusted route selected

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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=8, best_cost=8, margin=0, improvement=0, policy=latency, operation_mode=NORMAL

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: CONGESTED
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
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 16

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
Decision: DEGRADED_SWITCH
Policy phase: improvement=9, degraded_margin=0 -> switch in degraded latency mode
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 0
Fallback penalty: 2
Policy check: current_cost=16, best_cost=7, margin=0, improvement=9, policy=latency, operation_mode=DEGRADED

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: CONGESTED
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
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8
Decision: DEGRADED_SWITCH
Policy phase: improvement=1, degraded_margin=0 -> switch in degraded latency mode
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 0
Fallback penalty: 2
Policy check: current_cost=9, best_cost=8, margin=0, improvement=1, policy=latency, operation_mode=DEGRADED

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
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 1/2
  Recovery decision: STAY_DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: improvement=2, degraded_margin=0 -> switch in degraded latency mode
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 0
Fallback penalty: 2
Policy check: current_cost=8, best_cost=6, margin=0, improvement=2, policy=latency, operation_mode=DEGRADED

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 2/2
  Recovery decision: RESTORE_NORMAL
  Operation mode: DEGRADED -> NORMAL

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=6, best_cost=6, margin=0, improvement=0, policy=latency, operation_mode=NORMAL
```
- Insight:
    - v12c explicitly demonstrated a policy-boundary difference inside degraded mode
    - Under the same improvement = 1 condition, stability selected KEEP while latency selected DEGRADED_SWITCH
    - This confirms that degraded mode functions not merely as an exception state, but as a policy-sensitive operational control mode
    - PSC Routing has advanced beyond trust-failure recovery to a stage where differences in degraded operational policy can also be expressed

---
