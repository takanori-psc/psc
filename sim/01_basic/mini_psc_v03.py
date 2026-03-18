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


def find_route(start: Node, goal: Node):
    """
    Dijkstra（ダイクストラ法：最小コスト経路探索）
    今回は
    total cost = link cost + node state cost
    """
    queue = [(0, start.name, start, [start.name])]
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
                    (new_cost, neighbor.name, neighbor, path + [neighbor.name])
                )

    return None, None


def main():
    # ノード作成
    nodeA = Node("nodeA")
    nodeB = Node("nodeB")
    nodeC = Node("nodeC")
    nodeD = Node("nodeD")
    nodeE = Node("nodeE")
    nodeF = Node("nodeF")

    # ネットワーク構成
    # 近いルート: A-B-D-F
    nodeA.connect(nodeB, 1)
    nodeB.connect(nodeD, 1)
    nodeD.connect(nodeF, 1)

    # 遠いルート: A-C-E-F
    nodeA.connect(nodeC, 2)
    nodeC.connect(nodeE, 2)
    nodeE.connect(nodeF, 2)

    print("=== Normal ===")
    route, cost = find_route(nodeA, nodeF)
    print("Route:", route)
    print("Cost:", cost)

    nodeD.state = "WARNING"
    print("\n=== WARNING at nodeD ===")
    route, cost = find_route(nodeA, nodeF)
    print("Route:", route)
    print("Cost:", cost)

    nodeD.state = "CONGESTED"
    print("\n=== CONGESTED at nodeD ===")
    route, cost = find_route(nodeA, nodeF)
    print("Route:", route)
    print("Cost:", cost)


if __name__ == "__main__":
    main()
