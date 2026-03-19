import heapq
import math

# ============================================
# PSC Routing Simulation v11
# Trust Failure Handling + Resolver-managed Degraded Fallback
# ============================================

# --------------------------------------------
# Configuration
# --------------------------------------------
SOURCE = "nodeA"
DESTINATION = "nodeF"

POLICY = "latency"           # "stability" or "latency"
TRUST_MODE = "require_trusted" # v11 normal mode
HYSTERESIS_MARGIN = 3 if POLICY == "stability" else 0
RESOLVER_IMPROVEMENT_THRESHOLD = 2

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
# v11 intentionally uses same trust pattern as v10b:
# trusted path does not exist under strict require_trusted
# --------------------------------------------
TRUST_TABLE = {
    "nodeA": "TRUSTED",
    "nodeB": "TRUSTED",
    "nodeC": "UNTRUSTED",
    "nodeD": "UNTRUSTED",
    "nodeE": "UNTRUSTED",
    "nodeF": "TRUSTED",
}

# --------------------------------------------
# Step scenarios
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
        "nodeD": "BUSY",
        "nodeE": "NORMAL",
        "nodeF": "NORMAL",
    },
]


# ============================================
# Utility functions
# ============================================

def is_trusted(node: str) -> bool:
    return TRUST_TABLE.get(node) == "TRUSTED"


def route_is_trusted(route: list[str] | None) -> bool:
    if not route:
        return False
    return all(is_trusted(node) for node in route)


def calc_route_cost(route: list[str], node_states: dict[str, str]) -> int:
    """
    Route cost = sum of link costs + sum of intermediate node state costs
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

    return total


def dijkstra_all_routes(node_states: dict[str, str], allow_untrusted: bool) -> list[tuple[int, list[str]]]:
    """
    Enumerate shortest routes with trust filtering.
    This is a simple path search using priority queue.
    """
    pq = []
    heapq.heappush(pq, (0, [SOURCE]))
    results = []

    while pq:
        cost_so_far, path = heapq.heappop(pq)
        current = path[-1]

        if current == DESTINATION:
            true_cost = calc_route_cost(path, node_states)
            results.append((true_cost, path))
            continue

        for neighbor in GRAPH[current]:
            if neighbor in path:
                continue

            if not allow_untrusted and not is_trusted(neighbor):
                # strict mode: reject any untrusted node
                # source/destination are already fixed, so this is enough
                continue

            new_path = path + [neighbor]
            tentative_cost = calc_route_cost(new_path, node_states)
            heapq.heappush(pq, (tentative_cost, new_path))

    # Deduplicate by route tuple
    unique = {}
    for cost, route in results:
        key = tuple(route)
        if key not in unique or cost < unique[key]:
            unique[key] = cost

    sorted_routes = sorted((cost, list(route)) for route, cost in unique.items())
    return sorted_routes


def find_best_route(node_states: dict[str, str], allow_untrusted: bool) -> tuple[list[str] | None, int]:
    routes = dijkstra_all_routes(node_states, allow_untrusted=allow_untrusted)
    if not routes:
        return None, math.inf
    return routes[0][1], routes[0][0]


def reevaluate_current_route(current_route: list[str] | None, node_states: dict[str, str]) -> int:
    if current_route is None:
        return math.inf
    return calc_route_cost(current_route, node_states)


def resolver_should_escalate(improvement: int, threshold: int) -> bool:
    return improvement >= threshold


def resolver_allow_degraded_fallback(policy: str) -> tuple[bool, str]:
    """
    Minimal v11 rule:
    If trust failure occurs, allow degraded fallback to preserve connectivity.
    """
    if policy in ("stability", "latency"):
        return True, "preserve connectivity"
    return False, "policy does not allow degraded fallback"


# ============================================
# Main simulation
# ============================================

print("=== Policy-aware Routing Simulation v11 ===")
print(f"Source: {SOURCE}")
print(f"Destination: {DESTINATION}")
print(f"Policy: {POLICY}")
print(f"Initial trust mode: {TRUST_MODE}")
print(f"Hysteresis Margin: {HYSTERESIS_MARGIN}")
print(f"Resolver improvement threshold: {RESOLVER_IMPROVEMENT_THRESHOLD}")
print()

print("Trust table:")
for node in TRUST_TABLE:
    print(f"  {node}: {TRUST_TABLE[node]}")
print()

current_route = None
operation_mode = "NORMAL"

for step_index, node_states in enumerate(STEP_NODE_STATES, start=1):
    print(f"--- Step {step_index} ---")
    print("Node states:")
    for node in node_states:
        print(f"  {node}: {node_states[node]}")
    print()

    # ----------------------------------------
    # Primary search: strict trusted-only
    # ----------------------------------------
    primary_route, primary_cost = find_best_route(node_states, allow_untrusted=False)

    if primary_route is not None:
        print("Primary route search:")
        print("  Mode: TRUSTED_ONLY")
        print("  Result: ROUTE FOUND")
        print(f"  Route: {primary_route} | Cost: {primary_cost}")
        print()

        best_route = primary_route
        best_cost = primary_cost
        trust_failure_detected = False
        degraded_used = False
        degraded_reason = None

    else:
        print("Primary route search:")
        print("  Mode: TRUSTED_ONLY")
        print("  Result: NO ROUTE")
        print()

        trust_failure_detected = True
        trust_failure_reason = f"no trusted path from {SOURCE} to {DESTINATION}"

        print("Trust phase:")
        print("  require_trusted -> no trusted route available")
        print()

        print("Trust failure:")
        print("  Detected: YES")
        print(f"  Reason: {trust_failure_reason}")
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

            fallback_route, fallback_cost = find_best_route(node_states, allow_untrusted=True)

            print("Fallback route search:")
            print("  Mode: ALLOW_UNTRUSTED_FALLBACK")
            if fallback_route is None:
                print("  Result: NO ROUTE")
            else:
                print("  Result: ROUTE FOUND")
                print(f"  Route: {fallback_route} | Cost: {fallback_cost}")
            print()

            best_route = fallback_route
            best_cost = fallback_cost

        else:
            degraded_used = False
            degraded_reason = None
            best_route = None
            best_cost = math.inf

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
        if degraded_used:
            print("Policy phase: initial selection after degraded fallback")
            print("Resolver phase: override enabled")
            print("Final reason: degraded fallback route selected")
            print(f"Fallback reason: {degraded_reason}")
        else:
            print("Policy phase: initial selection")
            print("Resolver phase: not needed")
            print("Final reason: Initial route selected")
        print()
        continue

    current_cost = reevaluate_current_route(current_route, node_states)

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
        if degraded_used:
            current_route = best_route
            decision = "DEGRADED_SWITCH"
            policy_phase = "trust failure forced degraded fallback path selection"
            resolver_phase = "override enabled"
            final_reason = "Switched to degraded fallback route"

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
                policy_phase = (
                    f"improvement={improvement}, margin={HYSTERESIS_MARGIN} -> beyond hysteresis, switch"
                )
                resolver_phase = "not needed"
                final_reason = "Switch route under stability policy"

            else:
                if resolver_should_escalate(improvement, RESOLVER_IMPROVEMENT_THRESHOLD):
                    current_route = best_route
                    decision = "ESCALATE_SWITCH"
                    policy_phase = (
                        f"improvement={improvement}, margin={HYSTERESIS_MARGIN} -> within hysteresis, keep current route"
                    )
                    resolver_phase = (
                        f"improvement={improvement} >= threshold={RESOLVER_IMPROVEMENT_THRESHOLD} -> escalate"
                    )
                    final_reason = "Resolver switched to better route"
                else:
                    decision = "KEEP"
                    policy_phase = (
                        f"improvement={improvement}, margin={HYSTERESIS_MARGIN} -> within hysteresis, keep current route"
                    )
                    resolver_phase = (
                        f"improvement={improvement} < threshold={RESOLVER_IMPROVEMENT_THRESHOLD} -> no escalation"
                    )
                    final_reason = "Keep current route"

        else:
            decision = "KEEP"
            policy_phase = "unknown policy -> keep current route"
            resolver_phase = "not used"
            final_reason = "Keep current route"

    selected_cost = reevaluate_current_route(current_route, node_states)

    print("Selected route:")
    print(f"  {current_route} | Cost: {selected_cost}")
    print(f"Decision: {decision}")
    print(f"Policy phase: {policy_phase}")
    print(f"Resolver phase: {resolver_phase}")
    print(f"Final reason: {final_reason}")

    if degraded_used:
        print("Degraded mode: ACTIVE")
        print(f"Fallback reason: {degraded_reason}")

    print(
        f"Policy check: current_cost={current_cost}, best_cost={best_cost}, "
        f"margin={HYSTERESIS_MARGIN}, improvement={improvement}, policy={POLICY}"
    )
    print()
