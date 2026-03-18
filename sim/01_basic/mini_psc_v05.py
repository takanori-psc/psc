import heapq
import random

# ------------------------
# Node class
# ------------------------
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.state = "NORMAL"

    def add_neighbor(self, node, cost):
        self.neighbors.append((node, cost))


# ------------------------
# Cost model
# ------------------------
STATE_COST = {
    "NORMAL": 1,
    "WARNING": 3,
    "CONGESTED": 10,
}


# ------------------------
# Dijkstra
# ------------------------
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


# ------------------------
# Random state update
# ------------------------
def randomize_states(nodes):
    for node in nodes:
        r = random.random()
        if r < 0.7:
            node.state = "NORMAL"
        elif r < 0.9:
            node.state = "WARNING"
        else:
            node.state = "CONGESTED"


# ------------------------
# Build topology
# ------------------------
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


# ------------------------
# Simulation loop
# ------------------------
def main():
    nodes, start, end = build_topology()

    print("=== Dynamic Simulation ===\n")

    for step in range(1, 11):
        print(f"--- Step {step} ---")

        # 状態ランダム化
        randomize_states(nodes)

        # 状態表示
        print("Node states:")
        for n in nodes:
            print(f"  {n.name}: {n.state}")

        # ルート計算
        route, cost = find_route(start, end)

        print("\nSelected route:")
        print(f"  {route} | Cost: {cost}\n")


if __name__ == "__main__":
    main()
