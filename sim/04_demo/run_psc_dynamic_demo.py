# PSC Dynamic Demo Script
# run_psc_dynamic_demo.py

import time

print("=== PSC Dynamic Routing Demo ===\n")

print("Scenario:")
print("Network conditions change over time\n")

# ルート定義
routes = [
    {
        "name": "Route A",
        "path": ["nodeA", "nodeB", "nodeE", "nodeF"],
        "base_cost": 8,
        "trust_penalty": 2,
    },
    {
        "name": "Route B",
        "path": ["nodeA", "nodeC", "nodeD", "nodeF"],
        "base_cost": 7,
        "trust_penalty": 1,  # 初期は信頼性高い
    },
]

current_route = None

def evaluate_routes(step):
    global current_route

    print(f"\n=== Step {step} ===\n")

    # Stepごとの変化
    if step == 2:
        print("Event: nodeC trust degraded!\n")
        routes[1]["trust_penalty"] = 5  # Bが危険になる

    best_route = None
    best_score = 999

    print("Evaluating routes...\n")

    for r in routes:
        score = r["base_cost"] + r["trust_penalty"]

        print(f"{r['name']}:")
        print(f"  Path: {' -> '.join(r['path'])}")
        print(f"  Base cost: {r['base_cost']}")
        print(f"  Trust penalty: +{r['trust_penalty']}")
        print(f"  Final score: {score}\n")

        if score < best_score:
            best_score = score
            best_route = r

    # ルート変化判定
    if current_route is None:
        print("Initial route selection")
    elif current_route != best_route:
        print("Route change detected!")
    else:
        print("Route remains stable")

    current_route = best_route

    print(f"\nSelected route: {' -> '.join(best_route['path'])}")
    print(f"Score: {best_score}")

# 実行
for step in range(1, 4):
    evaluate_routes(step)
    time.sleep(1)

print("\n=== Summary ===\n")

print("PSC adapts routing decisions based on changing network conditions.")
print("It avoids unreliable paths and switches to more stable routes when needed.")

print("\n=== Key Insight ===")
print("Routing is not static — PSC continuously adapts to network state.")
