import heapq
import math

# ============================================
# PSC Routing Simulation v12
# Degraded Mode Policy Refinement
# - trust failure detection
# - resolver-managed degraded fallback
# - degraded-mode-specific switching policy
# - fallback penalty
# - recovery from DEGRADED to NORMAL
# ============================================

# --------------------------------------------
# Configuration
# --------------------------------------------
SOURCE = "nodeA"
DESTINATION = "nodeF"

POLICY = "latency"          # "stability" or "latency"
TRUST_MODE = "require_trusted"
HYSTERESIS_MARGIN = 3 if POLICY == "stability" else 0
RESOLVER_IMPROVEMENT_THRESHOLD = 2

# v12 additions
DEGRADED_SWITCH_MARGIN = 2 if POLICY == "stability" else 0
DEGRADED_FALLBACK_PENALTY = 2
RECOVERY_REQUIRED_STEPS = 2   # consecutive steps with trusted route available

# --------------------------------------------
# Topology
# --------------------------------------------
GRAPH = {
    "nodeA": {"nodeB": 2, "nodeC": 1},
    "nodeB": {"nodeA": 2, "nodeD": 2, "nodeE": 4},
    "nodeC": {"nodeA": 1, "nodeD": 1, "nodeE": 3},
    "nodeD": {"nodeB": 2, "nodeC": 1, "nodeF": 2},
    "nodeE": {"nodeB": 4, "nodeC": 3, "nodeF": 1},
    "nodeF": {"nodeD": 2, "nodeE": 1},
}

# --------------------------------------------
# State cost model
# --------------------------------------------
STATE_COST = {
    "NORMAL": 0,
    "BUSY": 2,
    "CONGESTED": 5,
}

# --------------------------------------------
# Trust table
# v12:
# nodeD becomes trusted again so that
# trusted route recovery can be observed
# --------------------------------------------
TRUST_TABLE = {
    "nodeA": "TRUSTED",
    "nodeB": "TRUSTED",
    "nodeC": "UNTRUSTED",
    "nodeD": "TRUSTED",
    "nodeE": "UNTRUSTED",
    "nodeF": "TRUSTED",
}

# --------------------------------------------
# Step scenarios
# v12 intentionally creates:
# - early trust failure (nodeD unavailable as trusted path)
# - degraded fallback
# - later trusted recovery
# --------------------------------------------
STEP_NODE_STATES = [
    # Step 1: trusted route exists
    {
        "nodeA": "NORMAL",
        "nodeB": "NORMAL",
        "nodeC": "NORMAL",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    # Step 2: trusted route becomes worse but still available
    {
        "nodeA": "NORMAL",
        "nodeB": "BUSY",
        "nodeC": "NORMAL",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    # Step 3: simulate trust failure by temporarily forcing trusted path loss
    {
        "nodeA": "NORMAL",
        "nodeB": "CONGESTED",
        "nodeC": "NORMAL",
        "nodeD": "CONGESTED",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    # Step 4: degraded continues, fallback candidate changes
    {
        "nodeA": "NORMAL",
        "nodeB": "NORMAL",
        "nodeC": "BUSY",
        "nodeD": "CONGESTED",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    # Step 5: trusted route starts recovering
    {
        "nodeA": "NORMAL",
        "nodeB": "NORMAL",
        "nodeC": "BUSY",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    # Step 6: trusted route stable again
    {
        "nodeA": "NORMAL",
        "nodeB": "NORMAL",
        "nodeC": "NORMAL",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
]

# --------------------------------------------
# v12 trusted-availability override
# To demonstrate trust failure / recovery clearly,
# trusted-only search is forced unavailable on steps 3-4.
# --------------------------------------------
FORCE_TRUST_FAILURE_STEPS = {3, 4}


# ============================================
# Utility functions
# ============================================

def is_trusted(node: str) -> bool:
    return TRUST_TABLE.get(node) == "TRUSTED"


def route_is_trusted(route: list[str] | None) -> bool:
    if not route:
        return False
    return all(is_trusted(node) for node in route)


def calc_route_cost(route: list[str], node_states: dict[str, str], penalty: int = 0) -> int:
    """
    Route cost = sum of link costs + sum of intermediate node state costs + optional penalty
    Source/Destination state cost is ignored for simplicity.
    """
    if not route or len(route) < 2:
        return math.inf

    total = 0

    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        total += GRAPH[a][b]

    for node in route[1:-1]:
        total += STATE_COST[node_states[node]]

    total += penalty
    return total


def enumerate_routes(node_states: dict[str, str], allow_untrusted: bool, fallback_penalty: int = 0) -> list[tuple[int, list[str]]]:
    pq = []
    heapq.heappush(pq, (0, [SOURCE]))
    results = []

    while pq:
        _, path = heapq.heappop(pq)
        current = path[-1]

        if current == DESTINATION:
            penalty = 0 if route_is_trusted(path) else fallback_penalty
            true_cost = calc_route_cost(path, node_states, penalty=penalty)
            results.append((true_cost, path))
            continue

        for neighbor in GRAPH[current]:
            if neighbor in path:
                continue

            if not allow_untrusted and not is_trusted(neighbor):
                continue

            new_path = path + [neighbor]
            penalty = 0 if route_is_trusted(new_path) else fallback_penalty
            tentative_cost = calc_route_cost(new_path, node_states, penalty=penalty)
            heapq.heappush(pq, (tentative_cost, new_path))

    unique = {}
    for cost, route in results:
        key = tuple(route)
        if key not in unique or cost < unique[key]:
            unique[key] = cost

    return sorted((cost, list(route)) for route, cost in unique.items())


def find_best_route(
    node_states: dict[str, str],
    allow_untrusted: bool,
    fallback_penalty: int = 0,
    force_no_route: bool = False
) -> tuple[list[str] | None, int]:
    if force_no_route:
        return None, math.inf

    routes = enumerate_routes(
        node_states=node_states,
        allow_untrusted=allow_untrusted,
        fallback_penalty=fallback_penalty,
    )
    if not routes:
        return None, math.inf
    return routes[0][1], routes[0][0]


def reevaluate_current_route(
    current_route: list[str] | None,
    node_states: dict[str, str],
    fallback_penalty: int = 0
) -> int:
    if current_route is None:
        return math.inf
    penalty = 0 if route_is_trusted(current_route) else fallback_penalty
    return calc_route_cost(current_route, node_states, penalty=penalty)


def resolver_should_escalate(improvement: int, threshold: int) -> bool:
    return improvement >= threshold


def resolver_allow_degraded_fallback(policy: str) -> tuple[bool, str]:
    if policy in ("stability", "latency"):
        return True, "preserve connectivity"
    return False, "policy does not allow degraded fallback"


def degraded_should_switch(policy: str, improvement: int, margin: int) -> tuple[bool, str]:
    if improvement <= 0:
        return False, "no improvement"

    if policy == "latency":
        return True, f"improvement={improvement}, degraded_margin={margin} -> switch in degraded latency mode"

    if policy == "stability":
        if improvement > margin:
            return True, f"improvement={improvement}, degraded_margin={margin} -> beyond degraded margin"
        return False, f"improvement={improvement}, degraded_margin={margin} -> within degraded margin"

    return False, "unknown degraded policy"


# ============================================
# Main simulation
# ============================================

print("=== Policy-aware Routing Simulation v12 ===")
print(f"Source: {SOURCE}")
print(f"Destination: {DESTINATION}")
print(f"Policy: {POLICY}")
print(f"Initial trust mode: {TRUST_MODE}")
print(f"Hysteresis Margin: {HYSTERESIS_MARGIN}")
print(f"Resolver improvement threshold: {RESOLVER_IMPROVEMENT_THRESHOLD}")
print(f"Degraded switch margin: {DEGRADED_SWITCH_MARGIN}")
print(f"Degraded fallback penalty: {DEGRADED_FALLBACK_PENALTY}")
print(f"Recovery required steps: {RECOVERY_REQUIRED_STEPS}")
print()

print("Trust table:")
for node in TRUST_TABLE:
    print(f"  {node}: {TRUST_TABLE[node]}")
print()

current_route = None
operation_mode = "NORMAL"
trusted_recovery_counter = 0

for step_index, node_states in enumerate(STEP_NODE_STATES, start=1):
    print(f"--- Step {step_index} ---")
    print("Node states:")
    for node in node_states:
        print(f"  {node}: {node_states[node]}")
    print()

    force_no_trusted = step_index in FORCE_TRUST_FAILURE_STEPS

    primary_route, primary_cost = find_best_route(
        node_states=node_states,
        allow_untrusted=False,
        fallback_penalty=0,
        force_no_route=force_no_trusted,
    )

    print("Primary route search:")
    print("  Mode: TRUSTED_ONLY")
    if primary_route is None:
        print("  Result: NO ROUTE")
    else:
        print("  Result: ROUTE FOUND")
        print(f"  Route: {primary_route} | Cost: {primary_cost}")
    print()

    degraded_used = False
    degraded_reason = None
    best_route = None
    best_cost = math.inf

    # ----------------------------------------
    # Recovery check when trusted route exists
    # ----------------------------------------
    if primary_route is not None:
        trusted_recovery_counter += 1
    else:
        trusted_recovery_counter = 0

    if operation_mode == "DEGRADED" and primary_route is not None:
        print("Recovery check:")
        print(f"  Trusted route available: YES")
        print(f"  Recovery counter: {trusted_recovery_counter}/{RECOVERY_REQUIRED_STEPS}")

        if trusted_recovery_counter >= RECOVERY_REQUIRED_STEPS:
            previous_mode = operation_mode
            operation_mode = "NORMAL"
            print("  Recovery decision: RESTORE_NORMAL")
            print(f"  Operation mode: {previous_mode} -> {operation_mode}")
            best_route = primary_route
            best_cost = primary_cost
        else:
            print("  Recovery decision: STAY_DEGRADED")
        print()

    # ----------------------------------------
    # Normal mode with trusted route
    # ----------------------------------------
    if best_route is None and operation_mode == "NORMAL" and primary_route is not None:
        best_route = primary_route
        best_cost = primary_cost

    # ----------------------------------------
    # Trust failure -> degraded fallback
    # ----------------------------------------
    if best_route is None and primary_route is None:
        print("Trust phase:")
        print("  require_trusted -> no trusted route available")
        print()

        print("Trust failure:")
        print("  Detected: YES")
        print(f"  Reason: no trusted path from {SOURCE} to {DESTINATION}")
        print()

        override_enabled, override_reason = resolver_allow_degraded_fallback(POLICY)

        print("Resolver decision:")
        print(f"  Override: {'YES' if override_enabled else 'NO'}")
        if override_enabled:
            print("  Action: enable untrusted fallback")
        else:
            print("  Action: no fallback")
        print(f"  Reason: {override_reason}")
        print()

        if override_enabled:
            previous_mode = operation_mode
            operation_mode = "DEGRADED"
            degraded_used = True
            degraded_reason = override_reason

            print("Operation mode:")
            print(f"  {previous_mode} -> {operation_mode}")
            print()

            fallback_route, fallback_cost = find_best_route(
                node_states=node_states,
                allow_untrusted=True,
                fallback_penalty=DEGRADED_FALLBACK_PENALTY,
                force_no_route=False,
            )

            print("Fallback route search:")
            print("  Mode: ALLOW_UNTRUSTED_FALLBACK")
            if fallback_route is None:
                print("  Result: NO ROUTE")
            else:
                print("  Result: ROUTE FOUND")
                print(f"  Route: {fallback_route} | Cost: {fallback_cost}")
                print(f"  Penalty applied to untrusted route: {DEGRADED_FALLBACK_PENALTY}")
            print()

            best_route = fallback_route
            best_cost = fallback_cost
        else:
            best_route = None
            best_cost = math.inf

    # ----------------------------------------
    # If degraded but not recovering yet, compare fallback routes
    # ----------------------------------------
    elif best_route is None and operation_mode == "DEGRADED":
        fallback_route, fallback_cost = find_best_route(
            node_states=node_states,
            allow_untrusted=True,
            fallback_penalty=DEGRADED_FALLBACK_PENALTY,
            force_no_route=False,
        )

        print("Fallback route search:")
        print("  Mode: ALLOW_UNTRUSTED_FALLBACK")
        if fallback_route is None:
            print("  Result: NO ROUTE")
        else:
            print("  Result: ROUTE FOUND")
            print(f"  Route: {fallback_route} | Cost: {fallback_cost}")
            print(f"  Penalty applied to untrusted route: {DEGRADED_FALLBACK_PENALTY}")
        print()

        best_route = fallback_route
        best_cost = fallback_cost

    # ----------------------------------------
    # Final decision
    # ----------------------------------------
    if best_route is None:
        print("Selected route:")
        print("  None | Cost: None")
        print("Decision: NO_ROUTE")
        print("Policy phase: no candidate route available")
        print("Resolver phase: fallback denied or unavailable")
        print("Final reason: No route available")
        print()
        continue

    if current_route is None:
        current_route = best_route
        print("Selected route:")
        print(f"  {current_route} | Cost: {best_cost}")
        print("Decision: SELECT")
        if operation_mode == "DEGRADED":
            print("Policy phase: initial selection after degraded fallback")
            print("Resolver phase: override enabled")
            print("Final reason: degraded fallback route selected")
            if degraded_reason:
                print(f"Fallback reason: {degraded_reason}")
        else:
            print("Policy phase: initial selection")
            print("Resolver phase: not needed")
            print("Final reason: Initial trusted route selected")
        print()
        continue

    current_cost = reevaluate_current_route(
        current_route=current_route,
        node_states=node_states,
        fallback_penalty=DEGRADED_FALLBACK_PENALTY if operation_mode == "DEGRADED" else 0,
    )

    print("Current route re-evaluated:")
    print(f"  {current_route} | Cost: {current_cost}")
    print()

    improvement = current_cost - best_cost

    if best_route == current_route:
        decision = "KEEP"
        policy_phase = "current route is already the best route"
        resolver_phase = "not needed"
        final_reason = "Keep current route"

    else:
        if operation_mode == "DEGRADED":
            should_switch, degraded_reason_text = degraded_should_switch(
                policy=POLICY,
                improvement=improvement,
                margin=DEGRADED_SWITCH_MARGIN,
            )

            if should_switch:
                current_route = best_route
                decision = "DEGRADED_SWITCH"
                policy_phase = degraded_reason_text
                resolver_phase = "degraded mode policy applied"
                final_reason = "Switched route under degraded mode policy"
            else:
                decision = "KEEP"
                policy_phase = degraded_reason_text
                resolver_phase = "degraded mode policy applied"
                final_reason = "Keep current degraded route"

        elif POLICY == "latency":
            current_route = best_route
            decision = "SWITCH"
            policy_phase = f"improvement={improvement}, margin={HYSTERESIS_MARGIN} -> switch under latency policy"
            resolver_phase = "not used"
            final_reason = "Switch route under latency policy"

        elif POLICY == "stability":
            if improvement > HYSTERESIS_MARGIN:
                current_route = best_route
                decision = "SWITCH"
                policy_phase = f"improvement={improvement}, margin={HYSTERESIS_MARGIN} -> beyond hysteresis, switch"
                resolver_phase = "not needed"
                final_reason = "Switch route under stability policy"
            else:
                if resolver_should_escalate(improvement, RESOLVER_IMPROVEMENT_THRESHOLD):
                    current_route = best_route
                    decision = "ESCALATE_SWITCH"
                    policy_phase = f"improvement={improvement}, margin={HYSTERESIS_MARGIN} -> within hysteresis, keep current route"
                    resolver_phase = f"improvement={improvement} >= threshold={RESOLVER_IMPROVEMENT_THRESHOLD} -> escalate"
                    final_reason = "Resolver switched to better route"
                else:
                    decision = "KEEP"
                    policy_phase = f"improvement={improvement}, margin={HYSTERESIS_MARGIN} -> within hysteresis, keep current route"
                    resolver_phase = f"improvement={improvement} < threshold={RESOLVER_IMPROVEMENT_THRESHOLD} -> no escalation"
                    final_reason = "Keep current route"
        else:
            decision = "KEEP"
            policy_phase = "unknown policy -> keep current route"
            resolver_phase = "not used"
            final_reason = "Keep current route"

    selected_cost = reevaluate_current_route(
        current_route=current_route,
        node_states=node_states,
        fallback_penalty=DEGRADED_FALLBACK_PENALTY if operation_mode == "DEGRADED" else 0,
    )

    print("Selected route:")
    print(f"  {current_route} | Cost: {selected_cost}")
    print(f"Decision: {decision}")
    print(f"Policy phase: {policy_phase}")
    print(f"Resolver phase: {resolver_phase}")
    print(f"Final reason: {final_reason}")

    if operation_mode == "DEGRADED":
        print("Degraded mode: ACTIVE")
        print(f"Degraded switch margin: {DEGRADED_SWITCH_MARGIN}")
        print(f"Fallback penalty: {DEGRADED_FALLBACK_PENALTY}")

    print(
        f"Policy check: current_cost={current_cost}, best_cost={best_cost}, "
        f"margin={HYSTERESIS_MARGIN}, improvement={improvement}, policy={POLICY}, "
        f"operation_mode={operation_mode}"
    )
    print()
