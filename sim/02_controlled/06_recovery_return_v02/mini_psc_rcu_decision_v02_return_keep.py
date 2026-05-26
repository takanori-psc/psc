# Dedicated validation scenario for RULE-20_RETURN_KEEP.
#
# The recovered candidate becomes RETURN_ELIGIBLE, but its score improvement
# over the current selected path is below return_margin. PSC must keep the
# current selected path and must not execute RULE-19_RETURN_SWITCH.

RETURN_VALIDATION_STEPS = 2
return_margin = 0.08
return_trust_threshold = 0.8
return_stability_threshold = 0.7
trust_threshold = 0.5

Wc = 0.4
Wp = 0.3

selected_path_name = None
mode = "NORMAL"
recovery_state = "NONE"
recovery_validation_counter = 0
recovery_candidate_name = None


def create_paths(step):
    path_a = {
        "name": "A",
        "utilization": 0.6,
        "buffer": 0.2,
        "retry": 0.1,
        "latency": 0.5,
        "throughput": 0.6,
        "variance": 0.1,
        "trend": 0.1,
        "persistence": 0.1,
        "trust": 0.85,
        "health": 1,
    }

    if step == 0:
        path_b = {
            "name": "B",
            "utilization": 0.45,
            "buffer": 0.10,
            "retry": 0.04,
            "latency": 0.30,
            "throughput": 0.82,
            "variance": 0.05,
            "trend": 0.05,
            "persistence": 0.05,
            "trust": 0.92,
            "health": 1,
        }
    elif step in (1, 2):
        path_b = {
            "name": "B",
            "utilization": 0.45,
            "buffer": 0.10,
            "retry": 0.04,
            "latency": 0.30,
            "throughput": 0.82,
            "variance": 0.40,
            "trend": 0.40,
            "persistence": 0.40,
            "trust": 0.30,
            "health": 0,
        }
    else:
        # B has recovered and is eligible, but only narrowly better than A.
        path_b = {
            "name": "B",
            "utilization": 0.55,
            "buffer": 0.18,
            "retry": 0.08,
            "latency": 0.45,
            "throughput": 0.72,
            "variance": 0.05,
            "trend": 0.05,
            "persistence": 0.05,
            "trust": 0.95,
            "health": 1,
        }

    return [path_a, path_b]


def congestion_score(path):
    return (
        0.3 * path["utilization"]
        + 0.3 * (path["buffer"] ** 2)
        + 0.25 * (path["retry"] ** 2)
        + 0.15 * path["latency"]
    )


def performance_score(path):
    return 0.6 * path["throughput"] + 0.4 * (1 - path["latency"])


def stability_score(path):
    instability = (
        0.4 * path["variance"]
        + 0.3 * path["trend"]
        + 0.3 * path["persistence"]
    )
    return max(0.0, min(1.0, 1 - instability))


def final_score(path):
    return Wc * (1 - congestion_score(path)) + Wp * performance_score(path)


def return_score(path):
    return (
        0.6 * stability_score(path)
        + 0.3 * path["trust"]
        + 0.1 * performance_score(path)
    )


def log_rule(event, rule, **kwargs):
    details = " ".join(f"{key}={value}" for key, value in kwargs.items())
    print(f"[{event}] rule={rule} {details}".rstrip())


def get_path_by_name(paths, name):
    for path in paths:
        if path["name"] == name:
            return path
    return None


def filter_paths(paths):
    valid_paths = []
    rejected_paths = []

    for path in paths:
        reasons = []
        if path["trust"] < trust_threshold:
            reasons.append("TRUST_LOW")
        if path["health"] == 0:
            reasons.append("HEALTH_INVALID")

        if reasons:
            rejected_paths.append((path, reasons))
        else:
            valid_paths.append(path)

    return valid_paths, rejected_paths


def score_paths(paths):
    scored = [{"path": path, "final": final_score(path)} for path in paths]
    scored.sort(key=lambda entry: entry["final"], reverse=True)
    return scored


def decide(step, paths):
    global selected_path_name, mode
    global recovery_state, recovery_validation_counter, recovery_candidate_name

    valid_paths, rejected_paths = filter_paths(paths)

    print("[FILTER]")
    for path, reasons in rejected_paths:
        print(f"  reject={path['name']} reasons={','.join(reasons)}")

    if selected_path_name is None and valid_paths:
        best_entry = score_paths(valid_paths)[0]
        selected_path_name = best_entry["path"]["name"]
        mode = "NORMAL"
        print(
            f"[INIT] selected_path={selected_path_name} "
            f"selected_score={best_entry['final']:.3f} mode={mode}"
        )
        return

    selected = get_path_by_name(valid_paths, selected_path_name)

    if selected is None:
        fallback = score_paths(valid_paths)[0]["path"]
        log_rule(
            "STATE",
            "RULE-07_DEGRADE_trigger",
            step=step,
            reason="SELECTED_REJECTED",
            mode="DEGRADED",
        )
        log_rule(
            "DECISION",
            "RULE-09_DEGRADE_switch",
            step=step,
            from_="INVALID",
            to=fallback["name"],
            score=f"{final_score(fallback):.3f}",
            reason="SELECTED_REJECTED",
            mode="DEGRADED",
        )
        selected_path_name = fallback["name"]
        mode = "DEGRADED"
        return

    if mode == "DEGRADED":
        recovery_candidates = [
            path for path in valid_paths
            if path["name"] != selected_path_name
            and path["trust"] >= return_trust_threshold
            and stability_score(path) >= return_stability_threshold
        ]

        if recovery_candidates:
            candidate = max(recovery_candidates, key=return_score)

            if recovery_state == "NONE":
                recovery_candidate_name = candidate["name"]
                recovery_state = "CANDIDATE"
                recovery_validation_counter = 1
                log_rule(
                    "RECOVERY",
                    "RULE-15_RECOVERY_CANDIDATE",
                    step=step,
                    candidate_path=recovery_candidate_name,
                    candidate_trust=f"{candidate['trust']:.3f}",
                    candidate_stability=f"{stability_score(candidate):.3f}",
                    return_score=f"{return_score(candidate):.3f}",
                    reason="STABLE_TRUSTED_PATH",
                )
                return

            recovery_state = "VALIDATING"
            recovery_validation_counter += 1
            log_rule(
                "RECOVERY",
                "RULE-16_RECOVERY_VALIDATION_START",
                step=step,
                candidate_path=recovery_candidate_name,
                validation_step=recovery_validation_counter,
                required=RETURN_VALIDATION_STEPS,
            )

            if recovery_validation_counter >= RETURN_VALIDATION_STEPS:
                recovery_state = "ELIGIBLE"
                log_rule(
                    "RECOVERY",
                    "RULE-18_RETURN_ELIGIBLE",
                    step=step,
                    candidate_path=recovery_candidate_name,
                    reason="VALIDATION_PASSED",
                )

    scored = score_paths(valid_paths)
    best = scored[0]["path"]
    selected = get_path_by_name(valid_paths, selected_path_name)
    selected_score = final_score(selected)
    candidate = get_path_by_name(valid_paths, recovery_candidate_name)
    candidate_score = final_score(candidate) if candidate else None

    if recovery_state == "ELIGIBLE" and candidate is not None and best["name"] == candidate["name"]:
        improvement = candidate_score - selected_score
        if improvement >= return_margin:
            log_rule(
                "DECISION",
                "RULE-19_RETURN_SWITCH",
                step=step,
                selected_path=selected["name"],
                candidate_path=candidate["name"],
                selected_score=f"{selected_score:.3f}",
                candidate_score=f"{candidate_score:.3f}",
                improvement=f"{improvement:.3f}",
                return_margin=f"{return_margin:.3f}",
                decision="SWITCH",
                reason="RETURN_MARGIN_MET",
                triggered_rule="RULE-19_RETURN_SWITCH",
            )
            selected_path_name = candidate["name"]
            mode = "NORMAL"
            return

        log_rule(
            "DECISION",
            "RULE-20_RETURN_KEEP",
            step=step,
            selected_path=selected["name"],
            candidate_path=candidate["name"],
            selected_score=f"{selected_score:.3f}",
            candidate_score=f"{candidate_score:.3f}",
            improvement=f"{improvement:.3f}",
            return_margin=f"{return_margin:.3f}",
            decision="KEEP",
            reason="RETURN_MARGIN_NOT_MET",
            triggered_rule="RULE-20_RETURN_KEEP",
        )
        return

    print(
        f"[CHECK] step={step} selected_path={selected['name']} "
        f"best_path={best['name']} mode={mode}"
    )


def run():
    for step in range(5):
        print(f"\n=== STEP {step} ===")
        decide(step, create_paths(step))


if __name__ == "__main__":
    run()
