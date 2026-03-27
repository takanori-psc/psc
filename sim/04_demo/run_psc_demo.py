# PSC Demo Script
# run_psc_demo.py

print("=== PSC Routing Demo ===\n")

print("Scenario:")
print("Sending data from nodeA to nodeF\n")

# 固定データ（分かりやすさ優先）
routes = [
    {
        "name": "Route A",
        "path": ["nodeA", "nodeB", "nodeE", "nodeF"],
        "cost": 8,
        "trust_penalty": 2,
    },
    {
        "name": "Route B",
        "path": ["nodeA", "nodeC", "nodeD", "nodeF"],
        "cost": 7,
        "trust_penalty": 5,
    },
]

print("Evaluating routes...\n")

best_route = None
best_score = 999

for r in routes:
    score = r["cost"] + r["trust_penalty"]
    
    print(f"{r['name']}:")
    print(f"  Path: {' -> '.join(r['path'])}")
    print(f"  Base cost: {r['cost']}")
    print(f"  Trust penalty: +{r['trust_penalty']}")
    print(f"  Final score: {score}\n")

    if score < best_score:
        best_score = score
        best_route = r

print("=== Decision ===\n")

print(f"Selected route: {' -> '.join(best_route['path'])}")
print(f"Final score: {best_score}\n")

print("Reason:")
print("- PSC selects routes based on cost + trust")
print("- Even if a route is shorter, low trust increases risk")
print("\nConclusion:")
print("PSC prefers slightly longer but more trusted routes.")

print("\n=== Key Insight ===")
print("Route B is shorter, but has significantly lower trust.")
print("PSC avoids risky paths even if they are faster.")
