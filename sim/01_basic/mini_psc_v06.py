import heapq
import random
from collections import defaultdict

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.state = "NORMAL"

    def add_neighbor(self, node, cost):
        self.neighbors.append((node, cost))


STATE_COST = {
    "NORMAL": 1,
    "WARNING": 3,
    "CONGESTED": 10,
}


def find_route(start, end):
    queue = [(0, start.name, start, [start.name])]
    visited = {}

    while queue:
        cost, _, node, path = heapq.heappop(queue)

        if node.name in visited:
            continue

        visited[node.name] = cost

        if node == end:
            return path, cost

        for neighbor, link_cost in node.neighbors:
            state_cost = STATE_COST[neighbor.state]
            new_cost = cost + link_cost + state_cost

            heapq.heappush(
                queue,
                (new_cost, neighbor.name, neighbor, path + [neighbor.name])
            )

    return None, float("inf")


def randomize_states(nodes):
    for node in nodes:
        r = random.random()
        if r < 0.7:
            node.state = "NORMAL"
        elif r < 0.9:
            node.state = "WARNING"
        else:
            node.state = "CONGESTED"


def build_topology():
    nodeA = Node("nodeA")
    nodeB = Node("nodeB")
    nodeC = Node("nodeC")
    nodeD = Node("nodeD")
    nodeE = Node("nodeE")
    nodeF = Node("nodeF")

    nodeA.add_neighbor(nodeB, 1)
    nodeA.add_neighbor(nodeC, 2)

    nodeB.add_neighbor(nodeD, 2)
    nodeC.add_neighbor(nodeE, 2)

    nodeD.add_neighbor(nodeF, 2)
    nodeE.add_neighbor(nodeF, 3)

    return [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF], nodeA, nodeF


def main():
    nodes, start, end = build_topology()

    prev_route = None
    route_changes = 0

    node_usage = defaultdict(int)
    route_history = []

    print("=== Dynamic Simulation + Analysis ===\n")

    for step in range(1, 11):
        print(f"--- Step {step} ---")

        randomize_states(nodes)

        print("Node states:")
        for n in nodes:
            print(f"  {n.name}: {n.state}")

        route, cost = find_route(start, end)

        print("\nSelected route:")
        print(f"  {route} | Cost: {cost}")

        # --- 分析 ---
        route_history.append(route)

        # ルート変化チェック
        if prev_route and route != prev_route:
            route_changes += 1
            print("  → Route changed")

        prev_route = route

        # ノード使用カウント
        for n in route:
            node_usage[n] += 1

        print()

    # --- 結果出力 ---
    print("=== Analysis Result ===\n")

    print(f"Total route changes: {route_changes}\n")

    print("Node usage count:")
    for node, count in sorted(node_usage.items()):
        print(f"  {node}: {count}")

    print("\nRoute history:")
    for i, r in enumerate(route_history, 1):
        print(f"  Step {i}: {r}")


if __name__ == "__main__":
    main()
