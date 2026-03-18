from collections import deque

# =========================================
# mini_psc_v10.py
# Policy-aware Routing + Resolver Escalation
# + Trust-aware Route Selection
# =========================================

POLICY = "stability"   # "stability" or "latency"
TRUST_MODE = "prefer_trusted"   # "off", "prefer_trusted", "require_trusted"

# Resolver settings
RESOLVER_IMPROVEMENT_THRESHOLD = 2
RESOLVER_ESCALATE_ON_CONGESTED = True
RESOLVER_ESCALATE_ON_FAILED = True

# -----------------------------------------
# Topology
# -----------------------------------------
graph = {
    "nodeA": ["nodeB", "nodeC"],
    "nodeB": ["nodeA", "nodeD"],
    "nodeC": ["nodeA", "nodeD", "nodeE"],
    "nodeD": ["nodeB", "nodeC", "nodeF"],
    "nodeE": ["nodeC", "nodeF"],
    "nodeF": ["nodeD", "nodeE"],
}

# -----------------------------------------
# Link costs
# -----------------------------------------
link_costs = {
    ("nodeA", "nodeB"): 2,
    ("nodeB", "nodeA"): 2,
    ("nodeA", "nodeC"): 1,
    ("nodeC", "nodeA"): 1,
    ("nodeB", "nodeD"): 2,
    ("nodeD", "nodeB"): 2,
    ("nodeC", "nodeD"): 2,
    ("nodeD", "nodeC"): 2,
    ("nodeC", "nodeE"): 3,
    ("nodeE", "nodeC"): 3,
    ("nodeD", "nodeF"): 2,
    ("nodeF", "nodeD"): 2,
    ("nodeE", "nodeF"): 1,
    ("nodeF", "nodeE"): 1,
}

# -----------------------------------------
# State cost table
# -----------------------------------------
state_cost_map = {
    "NORMAL": 0,
    "BUSY": 2,
    "CONGESTED": 5,
    "FAILED": 999,
}

# -----------------------------------------
# Trust table
# True  = trusted
# False = untrusted
# Source / Destination は通常 trusted 扱い
# -----------------------------------------
trust_table = {
    "nodeA": True,
    "nodeB": True,
    "nodeC": False,
    "nodeD": True,
    "nodeE": False,
    "nodeF": True,
}

# -----------------------------------------
# Simulation scenario
# -----------------------------------------
simulation_steps = [
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

SOURCE = "nodeA"
DESTINATION = "nodeF"


def get_margin(policy: str) -> int:
    if policy == "stability":
        return 3
    if policy == "latency":
        return 0
    raise ValueError(f"Unknown policy: {policy}")


def find_all_paths(graph_data, start, goal):
    queue = deque([[start]])
    results = []

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            results.append(path)
            continue

        for neighbor in graph_data[node]:
            if neighbor not in path:
                queue.append(path + [neighbor])

    return results


def calculate_route_cost(path, node_states):
    total_cost = 0

    for i in range(len(path) - 1):
        edge = (path[i], path[i + 1])
        total_cost += link_costs.get(edge, 999)

    for node in path[1:-1]:
        total_cost += state_cost_map[node_states[node]]

    return total_cost


def is_trusted_path(path):
    for node in path[1:-1]:
        if not trust_table.get(node, False):
            return False
    return True


def split_paths_by_trust(paths):
    trusted_paths = []
    untrusted_paths = []

    for path in paths:
        if is_trusted_path(path):
            trusted_paths.append(path)
        else:
            untrusted_paths.append(path)

    return trusted_paths, untrusted_paths


def choose_best_route(paths, node_states):
    best_route = None
    best_cost = float("inf")

    for path in paths:
        cost = calculate_route_cost(path, node_states)
        if cost < best_cost:
            best_cost = cost
            best_route = path

    return best_route, best_cost


def choose_best_route_with_trust(all_paths, node_states, trust_mode):
    trusted_paths, untrusted_paths = split_paths_by_trust(all_paths)

    if trust_mode == "off":
        route, cost = choose_best_route(all_paths, node_states)
        return route, cost, "trust mode off -> best route from all paths"

    if trust_mode == "require_trusted":
        if trusted_paths:
            route, cost = choose_best_route(trusted_paths, node_states)
            return route, cost, "require_trusted -> selected best trusted route"
        return None, float("inf"), "require_trusted -> no trusted route available"

    if trust_mode == "prefer_trusted":
        if trusted_paths:
            route, cost = choose_best_route(trusted_paths, node_states)
            return route, cost, "prefer_trusted -> selected best trusted route"
        route, cost = choose_best_route(untrusted_paths, node_states)
        return route, cost, "prefer_trusted -> no trusted route available, fallback to untrusted route"

    raise ValueError(f"Unknown trust_mode: {trust_mode}")


def route_contains_state(path, node_states, target_states):
    if path is None:
        return False
    for node in path[1:-1]:
        if node_states[node] in target_states:
            return True
    return False


def resolver_should_intervene(current_route, current_cost_now, best_route, best_cost, node_states, policy):
    if current_route is None:
        return False, "initial selection -> no escalation"

    if best_route is None:
        return False, "no candidate route available -> no escalation"

    if current_route == best_route:
        return False, "current route already best -> no escalation"

    improvement = current_cost_now - best_cost

    if RESOLVER_ESCALATE_ON_FAILED and route_contains_state(current_route, node_states, {"FAILED"}):
        return True, "current route includes FAILED node -> escalate"

    if RESOLVER_ESCALATE_ON_CONGESTED and route_contains_state(current_route, node_states, {"CONGESTED"}):
        return True, "current route includes CONGESTED node -> escalate"

    if policy == "stability":
        if improvement >= RESOLVER_IMPROVEMENT_THRESHOLD:
            return True, (
                f"improvement={improvement} >= threshold={RESOLVER_IMPROVEMENT_THRESHOLD} -> escalate"
            )
        return False, (
            f"improvement={improvement} < threshold={RESOLVER_IMPROVEMENT_THRESHOLD} -> no escalation"
        )

    return False, "latency policy does not require resolver escalation here"


def resolver_decide(current_route, current_cost_now, best_route, best_cost, node_states, policy):
    escalate, resolver_reason = resolver_should_intervene(
        current_route=current_route,
        current_cost_now=current_cost_now,
        best_route=best_route,
        best_cost=best_cost,
        node_states=node_states,
        policy=policy,
    )

    if not escalate:
        return current_route, current_cost_now, resolver_reason, "KEEP"

    return best_route, best_cost, resolver_reason, "ESCALATE_SWITCH"


def select_route_with_policy_and_resolver(current_route, best_route, best_cost, node_states, policy):
    margin = get_margin(policy)

    if best_route is None:
        return {
            "selected_route": current_route,
            "selected_cost": calculate_route_cost(current_route, node_states) if current_route else None,
            "decision": "NO_ROUTE",
            "current_cost_now": calculate_route_cost(current_route, node_states) if current_route else None,
            "policy_reason": "no candidate route available",
            "resolver_reason": "not used",
            "final_reason": "No route available under current trust mode",
        }

    if current_route is None:
        return {
            "selected_route": best_route,
            "selected_cost": best_cost,
            "decision": "SELECT",
            "current_cost_now": None,
            "policy_reason": "initial selection",
            "resolver_reason": "not needed",
            "final_reason": "Initial route selected",
        }

    current_cost_now = calculate_route_cost(current_route, node_states)

    if best_route == current_route:
        return {
            "selected_route": current_route,
            "selected_cost": current_cost_now,
            "decision": "KEEP",
            "current_cost_now": current_cost_now,
            "policy_reason": "current route is already the best route",
            "resolver_reason": "not needed",
            "final_reason": "Keep current route",
        }

    improvement = current_cost_now - best_cost

    if best_cost < current_cost_now - margin:
        if policy == "stability":
            policy_reason = (
                f"improvement={improvement}, margin={margin} -> better route exists beyond hysteresis"
            )
            selected_route, selected_cost, resolver_reason, decision = resolver_decide(
                current_route, current_cost_now, best_route, best_cost, node_states, policy
            )
            final_reason = (
                "Resolver switched to better route"
                if decision == "ESCALATE_SWITCH"
                else "Keep current route"
            )
            return {
                "selected_route": selected_route,
                "selected_cost": selected_cost,
                "decision": decision,
                "current_cost_now": current_cost_now,
                "policy_reason": policy_reason,
                "resolver_reason": resolver_reason,
                "final_reason": final_reason,
            }

        policy_reason = (
            f"improvement={improvement}, margin={margin} -> switch under latency policy"
        )
        return {
            "selected_route": best_route,
            "selected_cost": best_cost,
            "decision": "SWITCH",
            "current_cost_now": current_cost_now,
            "policy_reason": policy_reason,
            "resolver_reason": "not used",
            "final_reason": "Switch route under latency policy",
        }

    if best_cost == current_cost_now:
        return {
            "selected_route": current_route,
            "selected_cost": current_cost_now,
            "decision": "KEEP",
            "current_cost_now": current_cost_now,
            "policy_reason": "equal-cost alternative found -> keep current route",
            "resolver_reason": "not needed",
            "final_reason": "Keep current route",
        }

    policy_reason = (
        f"improvement={improvement}, margin={margin} -> within hysteresis, keep current route"
    )

    selected_route, selected_cost, resolver_reason, decision = resolver_decide(
        current_route, current_cost_now, best_route, best_cost, node_states, policy
    )

    final_reason = (
        "Resolver switched to better route"
        if decision == "ESCALATE_SWITCH"
        else "Keep current route"
    )

    return {
        "selected_route": selected_route,
        "selected_cost": selected_cost,
        "decision": decision,
        "current_cost_now": current_cost_now,
        "policy_reason": policy_reason,
        "resolver_reason": resolver_reason,
        "final_reason": final_reason,
    }


def print_node_states(node_states):
    print("Node states:")
    for node in sorted(node_states.keys()):
        print(f"  {node}: {node_states[node]}")


def print_trust_table():
    print("Trust table:")
    for node in sorted(trust_table.keys()):
        status = "TRUSTED" if trust_table[node] else "UNTRUSTED"
        print(f"  {node}: {status}")


def main():
    all_paths = find_all_paths(graph, SOURCE, DESTINATION)
    current_route = None
    margin = get_margin(POLICY)

    print("=== Policy-aware Routing Simulation v10 ===")
    print(f"Source: {SOURCE}")
    print(f"Destination: {DESTINATION}")
    print(f"Policy: {POLICY}")
    print(f"Trust mode: {TRUST_MODE}")
    print(f"Hysteresis Margin: {margin}")
    print(f"Resolver improvement threshold: {RESOLVER_IMPROVEMENT_THRESHOLD}")
    print()

    print_trust_table()
    print()

    for step_index, node_states in enumerate(simulation_steps, start=1):
        print(f"--- Step {step_index} ---")
        print_node_states(node_states)
        print()

        best_route, best_cost, trust_reason = choose_best_route_with_trust(
            all_paths, node_states, TRUST_MODE
        )

        print("Best computed route:")
        print(f"  {best_route} | Cost: {best_cost}")
        print(f"Trust phase: {trust_reason}")
        if best_route is not None:
            print(f"Trusted path: {is_trusted_path(best_route)}")
        print()

        result = select_route_with_policy_and_resolver(
            current_route=current_route,
            best_route=best_route,
            best_cost=best_cost,
            node_states=node_states,
            policy=POLICY,
        )

        if current_route is not None:
            print("Current route re-evaluated:")
            print(f"  {current_route} | Cost: {result['current_cost_now']}")
            print(f"Trusted path: {is_trusted_path(current_route)}")
            print()

        print("Selected route:")
        print(f"  {result['selected_route']} | Cost: {result['selected_cost']}")
        print(f"Decision: {result['decision']}")
        print(f"Policy phase: {result['policy_reason']}")
        print(f"Resolver phase: {result['resolver_reason']}")
        print(f"Final reason: {result['final_reason']}")

        if current_route is not None and best_route is not None and best_route != current_route:
            print(
                f"Policy check: current_cost={result['current_cost_now']}, "
                f"best_cost={best_cost}, margin={margin}, "
                f"improvement={result['current_cost_now'] - best_cost}, policy={POLICY}"
            )

        print()
        current_route = result["selected_route"]


if __name__ == "__main__":
    main()
