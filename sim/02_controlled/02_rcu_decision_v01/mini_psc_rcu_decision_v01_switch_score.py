# Dedicated validation scenario for RULE-02_SWITCH_score.
#
# Scope:
# - NORMAL mode only
# - no degraded / recovery / cooldown / resolver escalation behavior
# - compare RULE-01_KEEP_score and RULE-02_SWITCH_score using score_gap

switch_threshold = 0.10
selected_path_name = None


def create_paths(step):
    scenarios = {
        0: [
            {"name": "A", "score": 0.700},
            {"name": "B", "score": 0.680},
        ],
        1: [
            {"name": "A", "score": 0.700},
            {"name": "B", "score": 0.750},
        ],
        2: [
            {"name": "A", "score": 0.700},
            {"name": "B", "score": 0.840},
        ],
    }
    return scenarios[step]


def score_path(path):
    return path["score"]


def get_path_by_name(paths, name):
    for path in paths:
        if path["name"] == name:
            return path
    return None


def log_rule(event, rule, **kwargs):
    details = " ".join(f"{key}={value}" for key, value in kwargs.items())
    print(f"[{event}] rule={rule} {details}".rstrip())


def decide(step, paths):
    global selected_path_name

    scored = sorted(
        [{"path": path, "score": score_path(path)} for path in paths],
        key=lambda entry: entry["score"],
        reverse=True,
    )
    best = scored[0]["path"]
    best_score = scored[0]["score"]

    if selected_path_name is None:
        selected_path_name = "A"
        selected = get_path_by_name(paths, selected_path_name)
        selected_score = score_path(selected)
        print(
            f"[INIT] step={step} selected_path={selected_path_name} "
            f"selected_score={selected_score:.3f} mode=NORMAL"
        )
        return

    selected = get_path_by_name(paths, selected_path_name)
    selected_score = score_path(selected)
    score_gap = best_score - selected_score

    if best["name"] != selected_path_name and score_gap >= switch_threshold:
        log_rule(
            "DECISION",
            "RULE-02_SWITCH_score",
            step=step,
            selected_path=selected_path_name,
            best_path=best["name"],
            selected_score=f"{selected_score:.3f}",
            best_score=f"{best_score:.3f}",
            score_gap=f"{score_gap:.3f}",
            switch_threshold=f"{switch_threshold:.3f}",
            decision="SWITCH",
            reason="SCORE_GAP_THRESHOLD_MET",
            triggered_rule="RULE-02_SWITCH_score",
        )
        selected_path_name = best["name"]
        return

    log_rule(
        "DECISION",
        "RULE-01_KEEP_score",
        step=step,
        selected_path=selected_path_name,
        best_path=best["name"],
        selected_score=f"{selected_score:.3f}",
        best_score=f"{best_score:.3f}",
        score_gap=f"{score_gap:.3f}",
        switch_threshold=f"{switch_threshold:.3f}",
        decision="KEEP",
        reason="SCORE_GAP_BELOW_THRESHOLD",
        triggered_rule="RULE-01_KEEP_score",
    )


def run():
    for step in range(3):
        print(f"\n=== STEP {step} ===")
        decide(step, create_paths(step))


if __name__ == "__main__":
    run()
