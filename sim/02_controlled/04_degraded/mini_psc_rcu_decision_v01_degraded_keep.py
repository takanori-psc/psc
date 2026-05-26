# Dedicated validation scenario for RULE-08_DEGRADE_keep.
#
# Scope:
# - show RULE-09_DEGRADE_switch when the selected path becomes unsafe
# - show RULE-08_DEGRADE_keep while DEGRADED mode continues
# - avoid NORMAL-mode RULE-01_KEEP_score, recovery, cooldown, and resolver logic

trust_threshold = 0.50
recovery_trust_threshold = 0.80
switch_threshold = 0.10

selected_path_name = None
mode = "NORMAL"


def create_paths(step):
    scenarios = {
        0: [
            {"name": "A", "score": 0.700, "trust": 0.900, "health": 1},
            {"name": "B", "score": 0.640, "trust": 0.850, "health": 1},
        ],
        1: [
            {"name": "A", "score": 0.720, "trust": 0.200, "health": 0},
            {"name": "B", "score": 0.620, "trust": 0.450, "health": 1},
        ],
        2: [
            # A is slightly better by score and health has recovered, but trust is
            # still below recovery threshold. It must not pull PSC out of B.
            {"name": "A", "score": 0.660, "trust": 0.620, "health": 1},
            {"name": "B", "score": 0.620, "trust": 0.450, "health": 1},
        ],
    }
    return scenarios[step]


def get_path_by_name(paths, name):
    for path in paths:
        if path["name"] == name:
            return path
    return None


def score_path(path):
    return path["score"]


def log_rule(event, rule, **kwargs):
    details = " ".join(f"{key}={value}" for key, value in kwargs.items())
    print(f"[{event}] rule={rule} {details}".rstrip())


def best_fallback(paths):
    healthy_paths = [path for path in paths if path["health"] != 0]
    if not healthy_paths:
        return None
    return max(healthy_paths, key=score_path)


def best_recovery_candidate(paths, current_name):
    candidates = [
        path for path in paths
        if path["name"] != current_name
        and path["health"] != 0
        and path["trust"] >= recovery_trust_threshold
    ]
    if not candidates:
        return None
    return max(candidates, key=score_path)


def decide(step, paths):
    global selected_path_name, mode

    if step == 0:
        selected_path_name = "A"
        selected = get_path_by_name(paths, selected_path_name)
        print(
            f"[INIT] step={step} mode=NORMAL selected_path=A "
            f"selected_score={score_path(selected):.3f} "
            f"selected_trust={selected['trust']:.3f} selected_health={selected['health']}"
        )
        return

    selected = get_path_by_name(paths, selected_path_name)

    if mode == "NORMAL" and (
        selected is None
        or selected["health"] == 0
        or selected["trust"] < trust_threshold
    ):
        fallback = best_fallback(paths)
        log_rule(
            "STATE",
            "RULE-07_DEGRADE_trigger",
            step=step,
            mode="DEGRADED",
            selected_path=selected_path_name,
            selected_trust=f"{selected['trust']:.3f}",
            selected_health=selected["health"],
            reason="SELECTED_UNSAFE",
            triggered_rule="RULE-07_DEGRADE_trigger",
        )
        log_rule(
            "DECISION",
            "RULE-09_DEGRADE_switch",
            step=step,
            mode="DEGRADED",
            selected_path=selected_path_name,
            candidate_path=fallback["name"],
            selected_score=f"{score_path(selected):.3f}",
            candidate_score=f"{score_path(fallback):.3f}",
            score_gap=f"{score_path(fallback) - score_path(selected):.3f}",
            selected_trust=f"{selected['trust']:.3f}",
            candidate_trust=f"{fallback['trust']:.3f}",
            selected_health=selected["health"],
            candidate_health=fallback["health"],
            decision="SWITCH",
            reason="CURRENT_PATH_UNSAFE_HEALTH_INVALID",
            triggered_rule="RULE-09_DEGRADE_switch",
        )
        selected_path_name = fallback["name"]
        mode = "DEGRADED"
        return

    if mode == "DEGRADED":
        current = get_path_by_name(paths, selected_path_name)
        candidate = max(
            [path for path in paths if path["name"] != selected_path_name],
            key=score_path,
        )
        recovery_candidate = best_recovery_candidate(paths, selected_path_name)
        score_gap = score_path(candidate) - score_path(current)

        if current["health"] != 0 and recovery_candidate is None:
            log_rule(
                "DECISION",
                "RULE-08_DEGRADE_keep",
                step=step,
                mode="DEGRADED",
                selected_path=current["name"],
                candidate_path=candidate["name"],
                selected_score=f"{score_path(current):.3f}",
                candidate_score=f"{score_path(candidate):.3f}",
                score_gap=f"{score_gap:.3f}",
                switch_threshold=f"{switch_threshold:.3f}",
                selected_trust=f"{current['trust']:.3f}",
                candidate_trust=f"{candidate['trust']:.3f}",
                selected_health=current["health"],
                candidate_health=candidate["health"],
                decision="KEEP",
                reason="CURRENT_DEGRADED_PATH_HEALTHY_AND_CANDIDATE_NOT_RECOVERY_ELIGIBLE",
                triggered_rule="RULE-08_DEGRADE_keep",
            )
            return

        fallback = best_fallback(paths)
        log_rule(
            "DECISION",
            "RULE-09_DEGRADE_switch",
            step=step,
            mode="DEGRADED",
            selected_path=current["name"],
            candidate_path=fallback["name"],
            selected_score=f"{score_path(current):.3f}",
            candidate_score=f"{score_path(fallback):.3f}",
            score_gap=f"{score_path(fallback) - score_path(current):.3f}",
            selected_trust=f"{current['trust']:.3f}",
            candidate_trust=f"{fallback['trust']:.3f}",
            selected_health=current["health"],
            candidate_health=fallback["health"],
            decision="SWITCH",
            reason="CURRENT_DEGRADED_PATH_UNMAINTAINABLE",
            triggered_rule="RULE-09_DEGRADE_switch",
        )
        selected_path_name = fallback["name"]


def run():
    for step in range(3):
        print(f"\n=== STEP {step} ===")
        decide(step, create_paths(step))


if __name__ == "__main__":
    run()
