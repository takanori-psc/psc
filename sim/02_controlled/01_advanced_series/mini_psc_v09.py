from collections import deque

# =========================================
# mini_psc_v09.py
# Policy-aware Routing + Resolver Escalation
# =========================================

POLICY = "stability"   # "stability" or "latency"

# Resolver settings
RESOLVER_IMPROVEMENT_THRESHOLD = 2   # cost improvement needed for escalation
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


def choose_best_route(all_paths, node_states):
    best_route = None
    best_cost = float("inf")

    for path in all_paths:
        cost = calculate_route_cost(path, node_states)
        if cost < best_cost:
            best_cost = cost
            best_route = path

    return best_route, best_cost


def route_contains_state(path, node_states, target_states):
    for node in path[1:-1]:
        if node_states[node] in target_states:
            return True
    return False


def resolver_should_intervene(current_route, current_cost_now, best_route, best_cost, node_states, policy):
    if current_route is None:
        return False, "No escalation (initial selection)"

    if current_route == best_route:
        return False, "No escalation (same route as best)"

    improvement = current_cost_now - best_cost

    if RESOLVER_ESCALATE_ON_FAILED and route_contains_state(current_route, node_states, {"FAILED"}):
        return True, "Escalate: current route includes FAILED node"

    if RESOLVER_ESCALATE_ON_CONGESTED and route_contains_state(current_route, node_states, {"CONGESTED"}):
        return True, "Escalate: current route includes CONGESTED node"

    if policy == "stability" and improvement >= RESOLVER_IMPROVEMENT_THRESHOLD:
        return True, f"Escalate: improvement {improvement} >= threshold {RESOLVER_IMPROVEMENT_THRESHOLD}"

    return False, "No escalation"


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

    if current_route is None:
        return best_route, best_cost, "Initial route selected", None, "SELECT"

    current_cost_now = calculate_route_cost(current_route, node_states)

    if best_route == current_route:
        return (
            current_route,
            current_cost_now,
            "Keep current route (same as best route)",
            current_cost_now,
            "KEEP",
        )

    if best_cost < current_cost_now - margin:
        if policy == "stability":
            return resolver_decide(
                current_route, current_cost_now, best_route, best_cost, node_states, policy
            )[:2] + (
                resolver_decide(
                    current_route, current_cost_now, best_route, best_cost, node_states, policy
                )[2],
                current_cost_now,
                resolver_decide(
                    current_route, current_cost_now, best_route, best_cost, node_states, policy
                )[3],
            )
        else:
            reason = "Switch route (better route found under latency policy)"
            return best_route, best_cost, reason, current_cost_now, "SWITCH"

    if best_cost == current_cost_now:
        return (
            current_route,
            current_cost_now,
            "Keep current route (equal cost alternative)",
            current_cost_now,
            "KEEP",
        )

    selected_route, selected_cost, resolver_reason, resolver_decision = resolver_decide(
        current_route, current_cost_now, best_route, best_cost, node_states, policy
    )
    return selected_route, selected_cost, resolver_reason, current_cost_now, resolver_decision


def print_node_states(node_states):
    print("Node states:")
    for node in sorted(node_states.keys()):
        print(f"  {node}: {node_states[node]}")


def main():
    all_paths = find_all_paths(graph, SOURCE, DESTINATION)
    current_route = None
    margin = get_margin(POLICY)

    print("=== Policy-aware Routing Simulation v09 ===")
    print(f"Source: {SOURCE}")
    print(f"Destination: {DESTINATION}")
    print(f"Policy: {POLICY}")
    print(f"Hysteresis Margin: {margin}")
    print(f"Resolver improvement threshold: {RESOLVER_IMPROVEMENT_THRESHOLD}")
    print()

    for step_index, node_states in enumerate(simulation_steps, start=1):
        print(f"--- Step {step_index} ---")
        print_node_states(node_states)
        print()

        best_route, best_cost = choose_best_route(all_paths, node_states)

        print("Best computed route:")
        print(f"  {best_route} | Cost: {best_cost}")
        print()

        selected_route, selected_cost, reason, current_cost_now, decision = (
            select_route_with_policy_and_resolver(
                current_route=current_route,
                best_route=best_route,
                best_cost=best_cost,
                node_states=node_states,
                policy=POLICY,
            )
        )

        if current_route is not None:
            print("Current route re-evaluated:")
            print(f"  {current_route} | Cost: {current_cost_now}")
            print()

        print("Selected route:")
        print(f"  {selected_route} | Cost: {selected_cost}")
        print(f"Decision: {decision}")
        print(f"Reason: {reason}")

        if current_route is not None and best_route != current_route:
            print(
                f"Policy check: current_cost={current_cost_now}, "
                f"best_cost={best_cost}, margin={margin}, policy={POLICY}"
            )

        print()
        current_route = selected_route


if __name__ == "__main__":
    main()
