# mini_psc_v13b.py

from collections import deque

TRUST_WEIGHTS = {
    "TRUSTED": 0,
    "LIMITED": 2,
    "UNTRUSTED": 5,
}

graph = {
    "nodeA": {"nodeB": 3, "nodeC": 2},
    "nodeB": {"nodeA": 3, "nodeE": 3},
    "nodeC": {"nodeA": 2, "nodeD": 3},
    "nodeD": {"nodeC": 3, "nodeF": 2},
    "nodeE": {"nodeB": 3, "nodeF": 2},
    "nodeF": {"nodeD": 2, "nodeE": 2},
}

trust_table = {
    "nodeA": "TRUSTED",
    "nodeB": "LIMITED",
    "nodeC": "UNTRUSTED",
    "nodeD": "TRUSTED",
    "nodeE": "TRUSTED",
    "nodeF": "TRUSTED",
}

node_states = {
    "nodeA": "NORMAL",
    "nodeB": "NORMAL",
    "nodeC": "NORMAL",
    "nodeD": "NORMAL",
    "nodeE": "NORMAL",
    "nodeF": "NORMAL",
}

SOURCE = "nodeA"
DESTINATION = "nodeF"


def find_all_routes(graph, source, destination, max_depth=6):
    routes = []
    queue = deque()
    queue.append((source, [source]))

    while queue:
        current, path = queue.popleft()

        if len(path) > max_depth:
            continue

        if current == destination:
            routes.append(path)
            continue

        for neighbor in graph[current]:
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))

    return routes


def compute_route_cost(route, graph):
    total = 0
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        total += graph[a][b]
    return total


def get_trust_weight(level):
    return TRUST_WEIGHTS.get(level, 99)


def compute_route_trust_penalty(route, trust_table):
    transit_nodes = route[1:-1]
    total_penalty = 0
    breakdown = []

    for node in transit_nodes:
        level = trust_table.get(node, "UNTRUSTED")
        weight = get_trust_weight(level)
        total_penalty += weight
        breakdown.append((node, level, weight))

    return total_penalty, breakdown


def evaluate_route(route, graph, trust_table):
    base_cost = compute_route_cost(route, graph)
    trust_penalty, trust_breakdown = compute_route_trust_penalty(route, trust_table)
    weighted_cost = base_cost + trust_penalty

    return {
        "path": route,
        "base_cost": base_cost,
        "trust_penalty": trust_penalty,
        "weighted_cost": weighted_cost,
        "trust_breakdown": trust_breakdown,
    }


def print_route_evaluation(result):
    print(f"Route candidate: {result['path']}")
    print(f"  base_cost: {result['base_cost']}")
    print(f"  trust_penalty: {result['trust_penalty']}")
    print(f"  weighted_cost: {result['weighted_cost']}")
    print("  trust_breakdown:")
    for node, level, weight in result["trust_breakdown"]:
        print(f"    {node}: {level} (+{weight})")
    print()


def main():
    print("=== Adaptive Trust Weight Route Selection Simulation v13b ===")
    print()
    print(f"Source: {SOURCE}")
    print(f"Destination: {DESTINATION}")
    print()

    print("Trust table:")
    for node in sorted(trust_table.keys()):
        print(f"  {node}: {trust_table[node]}")
    print()

    all_routes = find_all_routes(graph, SOURCE, DESTINATION)
    evaluated_routes = []

    for route in all_routes:
        result = evaluate_route(route, graph, trust_table)
        evaluated_routes.append(result)

    # weighted cost で並べ替え
    evaluated_routes.sort(key=lambda x: (x["weighted_cost"], x["base_cost"]))

    print("Evaluated routes:")
    print()
    for result in evaluated_routes:
        print_route_evaluation(result)

    selected = evaluated_routes[0]

    print("Selected route:")
    print(f"  {selected['path']}")
    print(f"  weighted_cost: {selected['weighted_cost']}")
    print()

    # 補助説明
    print("Selection reason:")
    print("  route with the lowest weighted cost was selected")
    print("  adaptive trust weight changed fallback preference when plain cost was close")


if __name__ == "__main__":
    main()
