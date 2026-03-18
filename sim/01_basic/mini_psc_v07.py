import heapq

# ------------------------
# Node定義
# ------------------------
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.state = "NORMAL"

    def add_neighbor(self, neighbor, cost):
        self.neighbors.append((neighbor, cost))


# ------------------------
# 状態コスト
# ------------------------
STATE_COST = {
    "NORMAL": 1,
    "WARNING": 5,
    "CONGESTED": 20  # ←強すぎないように調整
}


# ------------------------
# グラフ構築
# ------------------------
def build_graph():
    nodeA = Node("nodeA")
    nodeB = Node("nodeB")
    nodeC = Node("nodeC")
    nodeD = Node("nodeD")
    nodeE = Node("nodeE")
    nodeF = Node("nodeF")

    # 上ルート（少し重くする）
    nodeA.add_neighbor(nodeB, 2)
    nodeB.add_neighbor(nodeD, 2)
    nodeD.add_neighbor(nodeF, 2)

    # 下ルート（少し軽くする）
    nodeA.add_neighbor(nodeC, 2)
    nodeC.add_neighbor(nodeE, 1)
    nodeE.add_neighbor(nodeF, 2)

    return nodeA, nodeF, [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF]


# ------------------------
# ダイクストラ
# ------------------------
def find_route(start, end):
    queue = []
    counter = 0
    heapq.heappush(queue, (0, counter, start, [start.name]))

    visited = {}

    while queue:
        cost, _, current, path = heapq.heappop(queue)

        if current.name in visited:
            continue
        visited[current.name] = cost

        if current == end:
            return path, cost

        for neighbor, link_cost in current.neighbors:
            node_cost = STATE_COST[neighbor.state]
            new_cost = cost + link_cost + node_cost

            counter += 1
            heapq.heappush(queue, (new_cost, counter, neighbor, path + [neighbor.name]))

    return None, float("inf")


# ------------------------
# 状態制御（ここがキモ）
# ------------------------
def update_states(step, nodes):
    for n in nodes:
        n.state = "NORMAL"

    # ★ nodeDを周期的に詰まらせる
    if step % 3 == 0:
        for n in nodes:
            if n.name == "nodeD":
                n.state = "CONGESTED"

    # ★ nodeC側に軽い負荷を時々入れる
    if step % 5 == 0:
        for n in nodes:
            if n.name == "nodeC":
                n.state = "WARNING"


# ------------------------
# メイン
# ------------------------
def main():
    start, end, nodes = build_graph()

    print("=== Controlled Switching Simulation ===\n")

    prev_route = None
    route_changes = 0
    history = []

    for step in range(1, 11):
        update_states(step, nodes)

        print(f"--- Step {step} ---")
        print("Node states:")
        for n in nodes:
            print(f"  {n.name}: {n.state}")

        route, cost = find_route(start, end)
        history.append(route)

        print("\nSelected route:")
        print(f"  {route} | Cost: {cost}")

        if prev_route and route != prev_route:
            route_changes += 1
            print("  → Route CHANGED")

        print()
        prev_route = route

    # ------------------------
    # 分析
    # ------------------------
    print("=== Analysis ===")
    print(f"Total route changes: {route_changes}")

    print("\nRoute history:")
    for i, r in enumerate(history, 1):
        print(f"  Step {i}: {r}")


if __name__ == "__main__":
    main()
