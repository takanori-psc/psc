import heapq


STATE_COST = {
    "NORMAL": 1,
    "WARNING": 3,
    "CONGESTED": 10,
}


class Node:
    def __init__(self, name: str, state: str = "NORMAL"):
        self.name = name
        self.state = state
        self.links = {}  # {neighbor_node: link_cost}

    def connect(self, other: "Node", cost: int) -> None:
        self.links[other] = cost
        other.links[self] = cost

    def cost(self) -> int:
        return STATE_COST[self.state]

    def __repr__(self) -> str:
        return f"{self.name}({self.state})"


def calculate_path_cost(path_nodes):
    """
    path_nodes: [nodeA, nodeB, nodeD, nodeF] のようなNode配列
    total cost = link cost + destination node cost
    start node自身のコストは加えない
    """
    total_cost = 0

    for i in range(len(path_nodes) - 1):
        current = path_nodes[i]
        nxt = path_nodes[i + 1]

        link_cost = current.links[nxt]
        node_cost = nxt.cost()

        total_cost += link_cost + node_cost

    return total_cost


def find_best_route(start: Node, goal: Node):
    """
    Dijkstra（ダイクストラ法：最小コスト経路探索）
    total cost = node cost + link cost
    """
    queue = [(0, start.name, start, [start])]
    visited = {}

    while queue:
        total_cost, _, current, path = heapq.heappop(queue)

        if current.name in visited:
            continue

        visited[current.name] = total_cost

        if current == goal:
            return path, total_cost

        for neighbor, link_cost in current.links.items():
            if neighbor.name not in visited:
                new_cost = total_cost + link_cost + neighbor.cost()
                heapq.heappush(
                    queue,
                    (new_cost, neighbor.name, neighbor, path + [neighbor])
                )

    return None, None


def format_path(path_nodes):
    return " -> ".join(node.name for node in path_nodes)


def evaluate_known_routes(route_list):
    """
    route_list: 候補ルートの配列
    """
    results = []

    for route_nodes in route_list:
        cost = calculate_path_cost(route_nodes)
        results.append((route_nodes, cost))

    results.sort(key=lambda x: x[1])
    return results


def print_route_analysis(title, routes, selected_route, selected_cost):
    print(f"=== {title} ===")
    print("Candidate routes:")

    for route_nodes, cost in routes:
        print(f"- {format_path(route_nodes)} | Cost: {cost}")

    print("\nSelected route:")
    print(f"- {format_path(selected_route)} | Cost: {selected_cost}")

    print("\nReason:")

    upper_route_cost = routes[0][1]
    lower_route_cost = routes[1][1]

    nodeD_state = None
    for node in selected_route:
        if node.name == "nodeD":
            nodeD_state = node.state

    # 状態に応じた説明
    if title == "Normal":
        print("- All nodes are in NORMAL state")
        print("- Shorter route has the lowest total cost")

    elif title == "WARNING at nodeD":
        print("- nodeD is WARNING")
        if upper_route_cost <= lower_route_cost:
            print("- Upper route is still cheaper than lower route")
        else:
            print("- Lower route became cheaper due to warning cost")

    elif title == "CONGESTED at nodeD":
        print("- nodeD is CONGESTED")
        print("- Congested route became more expensive than alternative route")

    print()


def main():
    # ノード作成
    nodeA = Node("nodeA")
    nodeB = Node("nodeB")
    nodeC = Node("nodeC")
    nodeD = Node("nodeD")
    nodeE = Node("nodeE")
    nodeF = Node("nodeF")

    # ネットワーク構成
    # 上ルート（短い）
    nodeA.connect(nodeB, 1)
    nodeB.connect(nodeD, 1)
    nodeD.connect(nodeF, 1)

    # 下ルート（遠い）
    nodeA.connect(nodeC, 2)
    nodeC.connect(nodeE, 2)
    nodeE.connect(nodeF, 2)

    upper_route = [nodeA, nodeB, nodeD, nodeF]
    lower_route = [nodeA, nodeC, nodeE, nodeF]

    # Normal
    routes = evaluate_known_routes([upper_route, lower_route])
    selected_route, selected_cost = find_best_route(nodeA, nodeF)
    print_route_analysis("Normal", routes, selected_route, selected_cost)

    # WARNING
    nodeD.state = "WARNING"
    routes = evaluate_known_routes([upper_route, lower_route])
    selected_route, selected_cost = find_best_route(nodeA, nodeF)
    print_route_analysis("WARNING at nodeD", routes, selected_route, selected_cost)

    # CONGESTED
    nodeD.state = "CONGESTED"
    routes = evaluate_known_routes([upper_route, lower_route])
    selected_route, selected_cost = find_best_route(nodeA, nodeF)
    print_route_analysis("CONGESTED at nodeD", routes, selected_route, selected_cost)


if __name__ == "__main__":
    main()
