import heapq


STATE_COST = {
    "NORMAL": 1,
    "WARNING": 5,
    "CONGESTED": 100,
}


class Node:
    def __init__(self, name: str, state: str = "NORMAL"):
        self.name = name
        self.state = state
        self.links = []

    def connect(self, other: "Node") -> None:
        if other not in self.links:
            self.links.append(other)
        if self not in other.links:
            other.links.append(self)

    def cost(self):
        return STATE_COST[self.state]

    def __repr__(self):
        return f"{self.name}({self.state})"


def find_route(start: Node, goal: Node):
    """
    Dijkstra（ダイクストラ：最小コスト経路）
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

        for neighbor in current.links:
            if neighbor.name not in visited:
                new_cost = total_cost + neighbor.cost()
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
    nodeA.connect(nodeB)
    nodeA.connect(nodeC)
    nodeB.connect(nodeD)
    nodeC.connect(nodeE)
    nodeD.connect(nodeF)
    nodeE.connect(nodeF)

    print("=== Normal ===")
    route, cost = find_route(nodeA, nodeF)
    print("Route:", route)
    print("Cost:", cost)

    # 軽い混雑
    nodeD.state = "WARNING"

    print("\n=== WARNING at nodeD ===")
    route, cost = find_route(nodeA, nodeF)
    print("Route:", route)
    print("Cost:", cost)

    # 重い混雑
    nodeD.state = "CONGESTED"

    print("\n=== CONGESTED at nodeD ===")
    route, cost = find_route(nodeA, nodeF)
    print("Route:", route)
    print("Cost:", cost)


if __name__ == "__main__":
    main()
