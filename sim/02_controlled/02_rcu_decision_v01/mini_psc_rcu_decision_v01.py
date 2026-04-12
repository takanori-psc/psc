# mini_psc_rcu_decision_v01.py

# =========================
# Config
# =========================

Wc = 0.4
Wp = 0.3
Ws = 0.3

switch_margin = 0.10
switch_stability_threshold = 0.40
persistence_limit = 3

recovery_stability_threshold = 0.7
recovery_cooldown_steps = 2

# Resolver behavior
resolver_cooldown_steps = 2

trust_threshold = 0.5
epsilon = 0.05

TEST_DEGRADED = False
TEST_RESOLVER_TRIGGER = True

# =========================
# Dummy Telemetry
# =========================

def create_paths(step):
    if TEST_DEGRADED:
        trust_a = 0.3 if step < 3 else 0.9
        trust_b = 0.2 if step < 3 else 0.8

        return [
            {
                "name": "A",
                "utilization": 0.6,
                "buffer": 0.2,
                "retry": 0.1,
                "latency": 0.6,
                "throughput": 0.5,
                "variance": 0.1,
                "trend": 0.0,
                "persistence": 0.2,
                "trust": trust_a,
                "health": 1,
            },
            {
                "name": "B",
                "utilization": 0.5,
                "buffer": 0.3,
                "retry": 0.2,
                "latency": 0.4,
                "throughput": 0.7,
                "variance": 0.3,
                "trend": 0.2,
                "persistence": 0.3,
                "trust": trust_b,
                "health": 1,
            },
        ]

    if TEST_RESOLVER_TRIGGER:
        if step == 0:
            return [
                {
                    "name": "A",
                    "utilization": 0.50,
                    "buffer": 0.20,
                    "retry": 0.10,
                    "latency": 0.40,
                    "throughput": 0.71,
                    "variance": 0.10,
                    "trend": 0.10,
                    "persistence": 0.20,
                    "trust": 0.60,
                    "health": 1,
                },
                {
                    "name": "B",
                    "utilization": 0.52,
                    "buffer": 0.18,
                    "retry": 0.08,
                    "latency": 0.42,
                    "throughput": 0.68,
                    "variance": 0.12,
                    "trend": 0.10,
                    "persistence": 0.20,
                    "trust": 0.60,
                    "health": 1,
                },
            ]
        elif step == 1:
            return [
                {
                    "name": "A",
                    "utilization": 0.58,
                    "buffer": 0.26,
                    "retry": 0.16,
                    "latency": 0.46,
                    "throughput": 0.63,
                    "variance": 0.05,
                    "trend": 0.05,
                    "persistence": 0.05,
                    "trust": 0.60,
                    "health": 1,
                },
                {
                    "name": "B",
                    "utilization": 0.50,
                    "buffer": 0.20,
                    "retry": 0.10,
                    "latency": 0.40,
                    "throughput": 0.69,
                    "variance": 0.05,
                    "trend": 0.05,
                    "persistence": 0.05,
                    "trust": 0.95,
                    "health": 1,
                },
            ]
        else:
            return [
                {
                    "name": "A",
                    "utilization": 0.58,
                    "buffer": 0.26,
                    "retry": 0.16,
                    "latency": 0.46,
                    "throughput": 0.63,
                    "variance": 0.05,
                    "trend": 0.05,
                    "persistence": 0.05,
                    "trust": 0.60,
                    "health": 1,
                },
                {
                    "name": "B",
                    "utilization": 0.50,
                    "buffer": 0.20,
                    "retry": 0.10,
                    "latency": 0.40,
                    "throughput": 0.69,
                    "variance": 0.40,
                    "trend": 0.40,
                    "persistence": 0.40,
                    "trust": 0.60,
                    "health": 1,
                },
            ]

    # normal mode: stepごとに状態変化させる
    path_a = {
        "name": "A",
        "utilization": 0.6,
        "buffer": 0.2,
        "retry": 0.1,
        "latency": 0.6,
        "throughput": 0.5,
        "variance": 0.1,
        "trend": 0.0,
        "persistence": 0.2,
        "trust": 0.7,
        "health": 1,
    }

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
        "persistence": instability,
        "trust": 1.0,
        "health": 1,
    }

    path_c = {
        "name": "C",
        "utilization": 0.7,
        "buffer": 0.3,
        "retry": 0.15,
        "latency": 0.7,
        "throughput": 0.4,
        "variance": 0.2,
        "trend": 0.0,
        "persistence": 0.2,
        "trust": 1.0 if step < 6 else 0.3,
        "health": 1,
    }

    return [path_a, path_b, path_c]

# =========================
# Score Functions
# =========================

def congestion_score(p):
    u_val = p["utilization"]
    b_val = p["buffer"] ** 2
    r_val = p["retry"] ** 2
    l_val = p["latency"]
    return 0.3 * u_val + 0.3 * b_val + 0.25 * r_val + 0.15 * l_val


def performance_score(p):
    throughput = p["throughput"]
    latency_good = 1 - p["latency"]
    return 0.6 * throughput + 0.4 * latency_good


def stability_score(p):
    variance = p["variance"]
    trend = p["trend"]
    persistence = p["persistence"]
    instability = 0.4 * variance + 0.3 * trend + 0.3 * persistence
    score = 1 - instability
    return max(0.0, min(1.0, score))


def final_score(p):
    congestion_benefit = 1 - congestion_score(p)
    performance = performance_score(p)

    # stabilityを一時的に外す
    # temporary validation mode:
    # exclude stability from final_score so that stability conflict
    # can be escalated to Resolver instead of being absorbed by RCU.
    return Wc * congestion_benefit + Wp * performance


def resolver_score(p):
    trust = p["trust"]
    stability = stability_score(p)
    performance = performance_score(p)
    return 0.5 * trust + 0.3 * stability + 0.2 * performance


def resolve(paths):
    best = max(paths, key=lambda p: resolver_score(p))
    return best


# =========================
# Helpers
# =========================

def select_path_ecmp(paths):
    # final_scoreベースで単純選択
    scored = score_paths(paths)
    return scored[0]["path"]

def log_rule(event, rule, **kwargs):
    details = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"[{event}] rule={rule} {details}".rstrip())


def get_path_by_name(paths, name):
    for path in paths:
        if path["name"] == name:
            return path
    return None


def filter_paths(paths):
    valid = []
    rejected = []

    for path in paths:
        reasons = []

        if path["trust"] < trust_threshold:
            reasons.append("TRUST_LOW")

        if path["health"] == 0:
            reasons.append("HEALTH_INVALID")

        if reasons:
            rejected.append((path, reasons))
        else:
            valid.append(path)

    return valid, rejected


def score_paths(paths):
    scored = []

    for path in paths:
        cong = congestion_score(path)
        perf = performance_score(path)
        stab = stability_score(path)
        total = final_score(path)

        scored.append(
            {
                "path": path,
                "congestion": cong,
                "performance": perf,
                "stability": stab,
                "final": total,
            }
        )

    scored.sort(key=lambda x: x["final"], reverse=True)
    return scored


# =========================
# RCU State
# =========================

selected_path_name = None
degradation_counter = 0
mode = "NORMAL"
recovery_cooldown_counter = 0

resolver_cooldown = 0


# =========================
# Decision Logic
# =========================

def decide(paths):
    global selected_path_name, degradation_counter, mode, recovery_cooldown_counter, resolver_cooldown

    valid_paths, rejected_paths = filter_paths(paths)

    # =========================
    # Recovery Check
    # =========================
    if mode == "DEGRADED" and len(valid_paths) > 0:
        recovery_candidates = [
            path for path in valid_paths
            if stability_score(path) > recovery_stability_threshold
        ]

        if len(recovery_candidates) > 0:
            print("[RECOVERY] stable trusted path detected")

            best = max(recovery_candidates, key=lambda path: final_score(path))

            log_rule(
                "STATE",
                "RULE-10_RECOVERY_trigger",
                to=best["name"],
                reason="STABLE_TRUSTED_PATH",
                mode="NORMAL",
            )

            selected_path_name = best["name"]
            degradation_counter = 0
            mode = "NORMAL"
            recovery_cooldown_counter = recovery_cooldown_steps
            return

    print("[FILTER]")
    for path, reasons in rejected_paths:
        print(f"  reject={path['name']} reasons={','.join(reasons)}")

    # =========================
    # Degraded / Fallback
    # =========================
    if len(valid_paths) == 0:
        fallback_paths = [path for path in paths if path["health"] != 0]

        if len(fallback_paths) == 0:
            log_rule(
                "STATE",
                "RULE-07_DEGRADE_trigger",
                reason="NO_HEALTHY_PATH",
                mode="DEGRADED",
            )
            selected_path_name = None
            degradation_counter = 0
            mode = "DEGRADED"
            return

        scored_fallback = score_paths(fallback_paths)
        fallback_entry = scored_fallback[0]
        fallback = fallback_entry["path"]

        if selected_path_name == fallback["name"]:
            log_rule(
                "DECISION",
                "RULE-08_DEGRADE_keep",
                selected=fallback["name"],
                score=f"{fallback_entry['final']:.3f}",
                reason="NO_TRUSTED_PATH",
                mode="DEGRADED",
            )
        else:
            log_rule(
                "DECISION",
                "RULE-09_DEGRADE_switch",
                to=fallback["name"],
                score=f"{fallback_entry['final']:.3f}",
                reason="NO_TRUSTED_PATH",
                mode="DEGRADED",
            )
            selected_path_name = fallback["name"]

        degradation_counter = 0
        mode = "DEGRADED"
        return

    # =========================
    # Normal Scoring
    # =========================
    scored = score_paths(valid_paths)
    best_entry = scored[0]
    best = best_entry["path"]

    if selected_path_name is None:
        selected_path_name = best["name"]
        mode = "NORMAL"
        print(f"[INIT] select={best['name']} score={best_entry['final']:.3f} mode={mode}")
        return

    selected = get_path_by_name(valid_paths, selected_path_name)

    if selected is None:
        mode = "DEGRADED"
        log_rule(
            "STATE",
            "RULE-07_DEGRADE_trigger",
            reason="SELECTED_REJECTED",
            mode=mode,
        )
        selected_path_name = best["name"]
        degradation_counter = 0
        log_rule(
            "DECISION",
            "RULE-09_DEGRADE_switch",
            from_="INVALID",
            to=best["name"],
            score_best=f"{best_entry['final']:.3f}",
            reason="SELECTED_REJECTED",
            mode=mode,
        )
        return

    # =========================
    # Recovery Cooldown Check
    # =========================
    if recovery_cooldown_counter > 0:
        log_rule(
            "STATE",
            "RULE-11_RECOVERY_cooldown",
            remaining=recovery_cooldown_counter,
            reason="RECOVERY_COOLDOWN",
        )
        recovery_cooldown_counter -= 1
        return

    selected_score = final_score(selected)
    best_score = best_entry["final"]
    improvement = best_score - selected_score
    stability = stability_score(selected)

    if stability < switch_stability_threshold:
        degradation_counter += 1
    else:
        degradation_counter = 0

    # =========================
    # Resolver Escalation
    # =========================
    if len(scored) >= 2:
        if resolver_cooldown > 0:
            log_rule(
                "STATE",
                "RULE-12_COOLDOWN_active",
                remaining=resolver_cooldown,
                reason="RESOLVER_COOLDOWN",
            )
            resolver_cooldown -= 1
        else:
            second_entry = scored[1]
            score_gap = best_entry["final"] - second_entry["final"]

            trust_gap = abs(best["trust"] - selected["trust"])
            stability_gap = abs(stability_score(best) - stability_score(selected))

            if (
                score_gap < epsilon
                and best["name"] != selected["name"]
                and (trust_gap > 0.1 or stability_gap > 0.2)
            ):
                reason_parts = []

                if trust_gap > 0.1:
                    reason_parts.append("TRUST_CONFLICT")
                if stability_gap > 0.2:
                    reason_parts.append("STABILITY_CONFLICT")

                reason = "+".join(reason_parts)

                log_rule(
                    "ESCALATE",
                    "RULE-05_ESCALATE_conflict",
                    reason=reason,
                    score_gap=f"{score_gap:.3f}",
                    trust_gap=f"{trust_gap:.3f}",
                    stability_gap=f"{stability_gap:.3f}",
                    best=best["name"],
                    selected=selected["name"],
                )

                resolved = resolve([entry["path"] for entry in scored])
                resolved_name = resolved.get("name")

                if resolved_name is None:
                    print("[DECISION] decision=KEEP reason=RESOLVER_NO_RESULT")
                    degradation_counter = 0
                    mode = "NORMAL"
                    return

                if resolved_name == selected_path_name:
                    log_rule(
                        "DECISION",
                        "RULE-13_RESOLVER_keep",
                        selected=selected_path_name,
                        reason="RESOLVER_SAME_SELECTION",
                    )
                else:
                    log_rule(
                        "DECISION",
                        "RULE-14_RESOLVER_switch",
                        from_=selected_path_name,
                        to=resolved_name,
                        reason="RESOLVER_DECISION",
                    )
                    selected_path_name = resolved_name

                resolver_cooldown = resolver_cooldown_steps
                degradation_counter = 0
                mode = "NORMAL"
                return

    print("[CHECK]")
    print(f"  selected={selected['name']} best={best['name']}")
    print(f"  selected_score={selected_score:.3f} best_score={best_score:.3f}")
    print(f"  improvement={improvement:.3f}")
    print(f"  selected_stability={stability:.3f}")
    print(f"  persistence={degradation_counter}")
    print(f"  mode={mode}")

    if (
        best["name"] != selected["name"]
        and improvement > switch_margin
        and stability < switch_stability_threshold
        and degradation_counter > persistence_limit
    ):
        log_rule(
            "DECISION",
            "RULE-02_SWITCH_score",
            from_=selected["name"],
            to=best["name"],
            improvement=f"{improvement:.3f}",
            reason="IMPROVEMENT_AND_PERSISTENT_DEGRADATION",
        )
        selected_path_name = best["name"]
        degradation_counter = 0
        mode = "NORMAL"
    else:
        log_rule(
            "DECISION",
            "RULE-01_KEEP_score",
            selected=selected["name"],
            best=best["name"],
            improvement=f"{improvement:.3f}",
            reason="HYSTERESIS_HOLD",
        )


# =========================
# Simulation Loop
# =========================

def run():
    for step in range(10):
        print(f"\n=== STEP {step} ===")

        paths = create_paths(step)

        # PSC（既存）
        decide(paths)

        # ECMP（ここに入れる）
        valid_paths, _ = filter_paths(paths)
        ecmp_selected = select_path_ecmp(valid_paths if valid_paths else paths)
        print(f"[ECMP] selected={ecmp_selected['name']}")

if __name__ == "__main__":
    run()
