# mini_psc_rcu_decision_v01_minimal.py

import math

# =========================
# Config
# =========================

Wc = 0.4
Wp = 0.3
Ws = 0.3

switch_margin = 0.10
switch_stability_threshold = 0.40
persistence_limit = 3

# =========================
# Dummy Telemetry
# =========================

def create_paths(step):
    """
    stepごとに状態変化させる
    """

    # Path A: 安定だけど遅い
    path_a = {
        "name": "A",
        "utilization": 0.6,
        "buffer": 0.2,
        "retry": 0.1,
        "latency": 0.6,
        "throughput": 0.5,
        "variance": 0.1,
        "trend": 0.0,
        "persistence": 0.2
    }

    # Path B: 速いけど不安定（徐々に悪化）
    instability = min(1.0, 0.2 + step * 0.15)

    path_b = {
        "name": "B",
        "utilization": 0.5,
        "buffer": instability,
        "retry": instability,
        "latency": 0.3,
        "throughput": 0.8,
        "variance": instability,
        "trend": 1.0 if instability > 0.5 else 0.3,
        "persistence": instability
    }

    return [path_a, path_b]

# =========================
# Score Functions
# =========================

def congestion_score(p):
    U = p["utilization"]
    B = p["buffer"] ** 2
    R = p["retry"] ** 2
    L = p["latency"]

    return 0.3*U + 0.3*B + 0.25*R + 0.15*L


def performance_score(p):
    T = p["throughput"]
    L_good = 1 - p["latency"]

    return 0.6*T + 0.4*L_good


def stability_score(p):
    V = p["variance"]
    T = p["trend"]
    P = p["persistence"]

    instability = 0.4*V + 0.3*T + 0.3*P
    return 1 - instability


def final_score(p):
    cong = 1 - congestion_score(p)
    perf = performance_score(p)
    stab = stability_score(p)

    return Wc*cong + Wp*perf + Ws*stab


# =========================
# RCU Logic
# =========================

selected_path_name = None
degradation_counter = 0


def decide(paths):
    global selected_path_name, degradation_counter

    scored = []
    for p in paths:
        s = final_score(p)
        scored.append((p, s))

    # Best path
    best = max(scored, key=lambda x: x[1])[0]

    if selected_path_name is None:
        selected_path_name = best["name"]
        print(f"[INIT] select {best['name']}")
        return

    selected = next(p for p in paths if p["name"] == selected_path_name)

    selected_score = final_score(selected)
    best_score = final_score(best)

    improvement = best_score - selected_score
    stab = stability_score(selected)

    # persistence tracking
    if stab < switch_stability_threshold:
        degradation_counter += 1
    else:
        degradation_counter = 0

    print(
        f"[CHECK] selected={selected['name']} best={best['name']} "
        f"improve={improvement:.3f} stab={stab:.3f} persist={degradation_counter}"
    )

    if (
        improvement > switch_margin
        and stab < switch_stability_threshold
        and degradation_counter > persistence_limit
    ):
        print(f"[SWITCH] {selected['name']} -> {best['name']}")
        selected_path_name = best["name"]
        degradation_counter = 0
    else:
        print("[KEEP]")


# =========================
# Simulation Loop
# =========================

def run():
    for step in range(10):
        print(f"\n=== STEP {step} ===")
        paths = create_paths(step)
        decide(paths)


if __name__ == "__main__":
    run()
