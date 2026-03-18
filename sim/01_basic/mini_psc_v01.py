from collections import deque


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

    def __repr__(self) -> str:
        return f"{self.name}({self.state})"


def find_route(start: Node, goal: Node):
    """
    BFS（幅優先探索：近い順に経路を探す方法）
    CONGESTED（混雑）ノードは通らない
    """
    queue = deque([(start, [start.name])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current.name in visited:
            continue
        visited.add(current.name)

        if current == goal:
            return path

        for neighbor in current.links:
            if neighbor.name not in visited and neighbor.state != "CONGESTED":
                queue.append((neighbor, path + [neighbor.name]))

    return None


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

    print("=== Normal route ===")
    route = find_route(nodeA, nodeF)
    print("Route:", route)

    # 混雑発生
    nodeD.state = "CONGESTED"

    print("\n=== After congestion at nodeD ===")
    route = find_route(nodeA, nodeF)
    print("Route:", route)


if __name__ == "__main__":
    main()
