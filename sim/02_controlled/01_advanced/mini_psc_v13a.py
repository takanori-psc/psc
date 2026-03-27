import heapq
import math

# ============================================
# PSC Routing Simulation v13a
# Adaptive Trust Weight for Degraded Fallback
# ============================================

# --------------------------------------------
# Configuration
# --------------------------------------------
SOURCE = "nodeA"
DESTINATION = "nodeF"

POLICY = "stability"   # "stability" or "latency"
TRUST_MODE = "require_trusted"

HYSTERESIS_MARGIN = 3 if POLICY == "stability" else 0
RESOLVER_IMPROVEMENT_THRESHOLD = 2
DEGRADED_SWITCH_MARGIN = 2 if POLICY == "stability" else 0
RECOVERY_REQUIRED_STEPS = 2

# --------------------------------------------
# Topology
# --------------------------------------------
GRAPH = {
    "nodeA": {"nodeB": 2, "nodeC": 1},
    "nodeB": {"nodeA": 2, "nodeD": 2, "nodeE": 3},
    "nodeC": {"nodeA": 1, "nodeD": 2, "nodeE": 2},
    "nodeD": {"nodeB": 2, "nodeC": 2, "nodeF": 2},
    "nodeE": {"nodeB": 3, "nodeC": 2, "nodeF": 2},
    "nodeF": {"nodeD": 2, "nodeE": 2},
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
# Trust levels and weights
# --------------------------------------------
TRUST_TABLE = {
    "nodeA": "TRUSTED",
    "nodeB": "TRUSTED",
    "nodeC": "UNTRUSTED",
    "nodeD": "TRUSTED",
    "nodeE": "LIMITED",
    "nodeF": "TRUSTED",
}

TRUST_WEIGHT = {
    "TRUSTED": 0,
    "LIMITED": 1,
    "UNTRUSTED": 3,
}

# --------------------------------------------
# Step scenarios
# Design intent:
# - Step 1/2: trusted path available
# - Step 3: trusted-only fails -> degraded fallback
# - degraded fallback should prefer lower trust-weight route
# - Step 4: current degraded route is reevaluated
# - Step 5/6: trusted route returns and recovery occurs
# --------------------------------------------
STEP_NODE_STATES = [
    {
        "nodeA": "NORMAL",
        "nodeB": "NORMAL",
        "nodeC": "NORMAL",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    {
        "nodeA": "NORMAL",
        "nodeB": "BUSY",
        "nodeC": "NORMAL",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    {
        "nodeA": "NORMAL",
        "nodeB": "CONGESTED",
        "nodeC": "NORMAL",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    {
        "nodeA": "NORMAL",
        "nodeB": "CONGESTED",
        "nodeC": "BUSY",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    {
        "nodeA": "NORMAL",
        "nodeB": "NORMAL",
        "nodeC": "BUSY",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
    {
        "nodeA": "NORMAL",
        "nodeB": "NORMAL",
        "nodeC": "NORMAL",
        "nodeD": "NORMAL",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
]

FORCE_TRUST_FAILURE_STEPS = {3, 4}


# ============================================
# Utility functions
# ============================================

def is_trusted(node: str) -> bool:
    return TRUST_TABLE.get(node) == "TRUSTED"


def get_trust_weight(node: str) -> int:
    level = TRUST_TABLE.get(node, "UNTRUSTED")
    return TRUST_WEIGHT[level]


def route_is_fully_trusted(route):
    if not route:
        return False
    return all(is_trusted(node) for node in route)


def calc_route_cost(route, node_states, apply_trust_weight=False):
    if not route or len(route) < 2:
        return math.inf

    total = 0

    # link cost
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        total += GRAPH[a][b]

    # state cost for transit nodes
    for node in route[1:-1]:
        total += STATE_COST[node_states[node]]

    # trust weight for degraded fallback
    if apply_trust_weight:
        for node in route[1:-1]:
            total += get_trust_weight(node)

    return total


def enumerate_routes(node_states, allow_untrusted, apply_trust_weight=False):
    pq = []
    heapq.heappush(pq, (0, [SOURCE]))
    results = []

    while pq:
        _, path = heapq.heappop(pq)
        current = path[-1]

        if current == DESTINATION:
            true_cost = calc_route_cost(
                route=path,
                node_states=node_states,
                apply_trust_weight=apply_trust_weight,
            )
            results.append((true_cost, path))
            continue

        for neighbor in GRAPH[current]:
            if neighbor in path:
                continue

            if not allow_untrusted and not is_trusted(neighbor):
                continue

            new_path = path + [neighbor]
            tentative_cost = calc_route_cost(
                route=new_path,
                node_states=node_states,
                apply_trust_weight=apply_trust_weight,
            )
            heapq.heappush(pq, (tentative_cost, new_path))

    unique = {}
    for cost, route in results:
        key = tuple(route)
        if key not in unique or cost < unique[key]:
            unique[key] = cost

    return sorted((cost, list(route)) for route, cost in unique.items())


def find_best_route(node_states, allow_untrusted, apply_trust_weight=False, force_no_route=False):
    if force_no_route:
        return None, math.inf

    routes = enumerate_routes(
        node_states=node_states,
        allow_untrusted=allow_untrusted,
        apply_trust_weight=apply_trust_weight,
    )

    if not routes:
        return None, math.inf

    return routes[0][1], routes[0][0]


def reevaluate_current_route(current_route, node_states, apply_trust_weight=False):
    if current_route is None:
        return math.inf

    return calc_route_cost(
        route=current_route,
        node_states=node_states,
        apply_trust_weight=apply_trust_weight,
    )


def resolver_should_escalate(improvement, threshold):
    return improvement >= threshold


def resolver_allow_degraded_fallback(policy):
    if policy in ("stability", "latency"):
        return True, "preserve connectivity"
    return False, "policy does not allow degraded fallback"


def degraded_should_switch(policy, improvement, margin):
    if improvement <= 0:
        return False, "no improvement"

    if policy == "latency":
        return True, f"improvement={improvement}, degraded_margin={margin} -> switch in degraded latency mode"

    if policy == "stability":
        if improvement > margin:
            return True, f"improvement={improvement}, degraded_margin={margin} -> beyond degraded margin"
        return False, f"improvement={improvement}, degraded_margin={margin} -> within degraded margin"

    return False, "unknown degraded policy"


def calc_route_trust_summary(route):
    if not route:
        return "none"

    levels = [TRUST_TABLE[node] for node in route]
    total_weight = sum(get_trust_weight(node) for node in route[1:-1])

    return f"levels={levels}, transit_trust_weight={total_weight}"


# ============================================
# Main simulation
# ============================================

print("=== Policy-aware Routing Simulation v13a ===")
print(f"Source: {SOURCE}")
print(f"Destination: {DESTINATION}")
print(f"Policy: {POLICY}")
print(f"Initial trust mode: {TRUST_MODE}")
print(f"Hysteresis Margin: {HYSTERESIS_MARGIN}")
print(f"Resolver improvement threshold: {RESOLVER_IMPROVEMENT_THRESHOLD}")
print(f"Degraded switch margin: {DEGRADED_SWITCH_MARGIN}")
print(f"Recovery required steps: {RECOVERY_REQUIRED_STEPS}")
print("Adaptive trust weight: ENABLED")
print()

print("Trust table:")
for node in TRUST_TABLE:
    print(f"  {node}: {TRUST_TABLE[node]} (weight={get_trust_weight(node)})")
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
        apply_trust_weight=False,
        force_no_route=force_no_trusted,
    )

    print("Primary route search:")
    print("  Mode: TRUSTED_ONLY")
    if primary_route is None:
        print("  Result: NO ROUTE")
    else:
        print("  Result: ROUTE FOUND")
        print(f"  Route: {primary_route} | Cost: {primary_cost}")
        print(f"  Trust summary: {calc_route_trust_summary(primary_route)}")
    print()

    best_route = None
    best_cost = math.inf

    if primary_route is not None:
        trusted_recovery_counter += 1
    else:
        trusted_recovery_counter = 0

    if operation_mode == "DEGRADED" and primary_route is not None:
        print("Recovery check:")
        print("  Trusted route available: YES")
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

    if best_route is None and operation_mode == "NORMAL" and primary_route is not None:
        best_route = primary_route
        best_cost = primary_cost

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
        print(f"  Reason: {override_reason}")
        print()

        if override_enabled:
            previous_mode = operation_mode
            operation_mode = "DEGRADED"

            print("Operation mode:")
            print(f"  {previous_mode} -> {operation_mode}")
            print()

            fallback_route, fallback_cost = find_best_route(
                node_states=node_states,
                allow_untrusted=True,
                apply_trust_weight=True,
                force_no_route=False,
            )

            print("Fallback route search:")
            print("  Mode: ALLOW_UNTRUSTED_FALLBACK + ADAPTIVE_TRUST_WEIGHT")
            if fallback_route is None:
                print("  Result: NO ROUTE")
            else:
                print("  Result: ROUTE FOUND")
                print(f"  Route: {fallback_route} | Cost: {fallback_cost}")
                print(f"  Trust summary: {calc_route_trust_summary(fallback_route)}")
            print()

            best_route = fallback_route
            best_cost = fallback_cost

    elif best_route is None and operation_mode == "DEGRADED":
        fallback_route, fallback_cost = find_best_route(
            node_states=node_states,
            allow_untrusted=True,
            apply_trust_weight=True,
            force_no_route=False,
        )

        print("Fallback route search:")
        print("  Mode: ALLOW_UNTRUSTED_FALLBACK + ADAPTIVE_TRUST_WEIGHT")
        if fallback_route is None:
            print("  Result: NO ROUTE")
        else:
            print("  Result: ROUTE FOUND")
            print(f"  Route: {fallback_route} | Cost: {fallback_cost}")
            print(f"  Trust summary: {calc_route_trust_summary(fallback_route)}")
        print()

        best_route = fallback_route
        best_cost = fallback_cost

    if best_route is None:
        print("Selected route:")
        print("  None | Cost: None")
        print("Decision: NO_ROUTE")
        print()
        continue

    if current_route is None:
        current_route = best_route
        print("Selected route:")
        print(f"  {current_route} | Cost: {best_cost}")
        print("Decision: SELECT")
        if operation_mode == "DEGRADED":
            print("Policy phase: initial selection after degraded fallback")
            print("Resolver phase: adaptive trust-weight fallback enabled")
            print("Final reason: degraded fallback route selected")
        else:
            print("Policy phase: initial selection")
            print("Resolver phase: not needed")
            print("Final reason: Initial trusted route selected")
        print()
        continue

    current_cost = reevaluate_current_route(
        current_route=current_route,
        node_states=node_states,
        apply_trust_weight=(operation_mode == "DEGRADED"),
    )

    print("Current route re-evaluated:")
    print(f"  {current_route} | Cost: {current_cost}")
    print(f"  Trust summary: {calc_route_trust_summary(current_route)}")
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
                resolver_phase = "adaptive trust-weight degraded mode applied"
                final_reason = "Switched route under degraded mode policy"
            else:
                decision = "KEEP"
                policy_phase = degraded_reason_text
                resolver_phase = "adaptive trust-weight degraded mode applied"
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
        apply_trust_weight=(operation_mode == "DEGRADED"),
    )

    print("Selected route:")
    print(f"  {current_route} | Cost: {selected_cost}")
    print(f"  Trust summary: {calc_route_trust_summary(current_route)}")
    print(f"Decision: {decision}")
    print(f"Policy phase: {policy_phase}")
    print(f"Resolver phase: {resolver_phase}")
    print(f"Final reason: {final_reason}")

    if operation_mode == "DEGRADED":
        print("Degraded mode: ACTIVE")
        print("Adaptive trust weight: ENABLED")

    print(
        f"Policy check: current_cost={current_cost}, best_cost={best_cost}, "
        f"margin={HYSTERESIS_MARGIN}, improvement={improvement}, policy={POLICY}, "
        f"operation_mode={operation_mode}"
    )
    print()
