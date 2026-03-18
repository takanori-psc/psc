from collections import deque

# =========================================
# mini_psc_v08b.py
# Controlled Switching Simulation + Hysteresis
# =========================================

HYSTERESIS_MARGIN = 3

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
# (undirected graph: store both directions)
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
# Dynamic node states for each step
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


def find_all_paths(graph, start, goal):
    """BFS-style enumeration of simple paths."""
    queue = deque([[start]])
    results = []

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            results.append(path)
            continue

        for neighbor in graph[node]:
            if neighbor not in path:
                queue.append(path + [neighbor])

    return results


def calculate_route_cost(path, node_states):
    """Route cost = link costs + intermediate node state costs."""
    total_cost = 0

    # link costs
    for i in range(len(path) - 1):
        edge = (path[i], path[i + 1])
        total_cost += link_costs.get(edge, 999)

    # node state costs
    # source/destination are excluded here for simplicity
    for node in path[1:-1]:
        state = node_states[node]
        total_cost += state_cost_map[state]

    return total_cost


def choose_best_route(all_paths, node_states):
    """Pick lowest-cost available route."""
    best_route = None
    best_cost = float("inf")

    for path in all_paths:
        cost = calculate_route_cost(path, node_states)
        if cost < best_cost:
            best_cost = cost
            best_route = path

    return best_route, best_cost


def select_route_with_hysteresis(current_route, current_cost, best_route, best_cost):
    """
    Keep current route unless the new route is significantly better.
    """
    if current_route is None:
        return best_route, best_cost, "Initial route selected"

    if best_route == current_route:
        return current_route, current_cost, "Keep current route (same as best route)"

    if best_cost < current_cost - HYSTERESIS_MARGIN:
        return best_route, best_cost, "Switch route (significant improvement)"

    return current_route, current_cost, "Keep current route (within hysteresis margin)"


def print_node_states(node_states):
    print("Node states:")
    for node in sorted(node_states.keys()):
        print(f"  {node}: {node_states[node]}")


def main():
    all_paths = find_all_paths(graph, SOURCE, DESTINATION)

    current_route = None
    current_cost = None

    print("=== Controlled Switching Simulation + Hysteresis v08b ===")
    print(f"Source: {SOURCE}")
    print(f"Destination: {DESTINATION}")
    print(f"Hysteresis Margin: {HYSTERESIS_MARGIN}")
    print()

    for step_index, node_states in enumerate(simulation_steps, start=1):
        print(f"--- Step {step_index} ---")
        print_node_states(node_states)
        print()

        best_route, best_cost = choose_best_route(all_paths, node_states)

        print("Best computed route:")
        print(f"  {best_route} | Cost: {best_cost}")
        print()

        selected_route, selected_cost, reason = select_route_with_hysteresis(
            current_route=current_route,
            current_cost=current_cost,
            best_route=best_route,
            best_cost=best_cost,
        )

        print("Selected route:")
        print(f"  {selected_route} | Cost: {selected_cost}")
        print(f"Reason: {reason}")

        if current_route is not None and best_route != current_route and selected_route == current_route:
            print(
                f"Hysteresis check: current_cost={current_cost}, "
                f"best_cost={best_cost}, margin={HYSTERESIS_MARGIN}"
            )

        print()

        current_route = selected_route
        current_cost = selected_cost


if __name__ == "__main__":
    main()
