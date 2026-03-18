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
    "CONGESTED": 20
}

# ヒステリシス閾値
# 新ルートが current_route よりこれ以上安くないと切り替えない
HYSTERESIS_MARGIN = 2


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

    # 上ルート
    nodeA.add_neighbor(nodeB, 2)
    nodeB.add_neighbor(nodeD, 2)
    nodeD.add_neighbor(nodeF, 2)

    # 下ルート
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
# 指定ルートのコスト計算
# ------------------------
def calculate_route_cost(route, nodes_dict):
    total_cost = 0
    for i in range(len(route) - 1):
        current = nodes_dict[route[i]]
        next_name = route[i + 1]

        for neighbor, link_cost in current.neighbors:
            if neighbor.name == next_name:
                total_cost += link_cost + STATE_COST[neighbor.state]
                break

    return total_cost


# ------------------------
# 状態制御
# ------------------------
def update_states(step, nodes):
    for n in nodes:
        n.state = "NORMAL"

    if step % 3 == 0:
        for n in nodes:
            if n.name == "nodeD":
                n.state = "CONGESTED"

    if step % 5 == 0:
        for n in nodes:
            if n.name == "nodeC":
                n.state = "WARNING"


# ------------------------
# メイン
# ------------------------
def main():
    start, end, nodes = build_graph()
    nodes_dict = {n.name: n for n in nodes}

    current_route = None
    current_cost = None

    route_changes = 0
    history = []

    print("=== Controlled Switching Simulation + Hysteresis ===\n")

    for step in range(1, 11):
        update_states(step, nodes)

        print(f"--- Step {step} ---")
        print("Node states:")
        for n in nodes:
            print(f"  {n.name}: {n.state}")

        best_route, best_cost = find_route(start, end)

        selected_route = best_route
        selected_cost = best_cost
        reason = "Best route selected"

        # ヒステリシス適用
        if current_route is not None:
            current_route_cost = calculate_route_cost(current_route, nodes_dict)

            # 新ルートが十分良くないなら現状維持
            if best_route != current_route and best_cost >= current_route_cost - HYSTERESIS_MARGIN:
                selected_route = current_route
                selected_cost = current_route_cost
                reason = "Kept previous route due to hysteresis"
            else:
                if best_route != current_route:
                    route_changes += 1
                    reason = "Route changed (better route exceeded hysteresis margin)"

        print("\nBest computed route:")
        print(f"  {best_route} | Cost: {best_cost}")

        print("\nSelected route:")
        print(f"  {selected_route} | Cost: {selected_cost}")
        print(f"Reason: {reason}\n")

        current_route = selected_route
        current_cost = selected_cost
        history.append(selected_route)

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
