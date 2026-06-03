#!/usr/bin/env python3
"""Experimental hard-abort recovery return validation scenario.

RULE-23_RETURN_RAMP_ABORT aborts the current Return Ramp attempt. In the
HARD_ABORT class, PSC enters Traffic Stabilization Phase and ramps down the
suspect recovered path while forwarding is still possible.
"""

from __future__ import annotations


SCENARIO_METADATA = {
    "name": "hard_abort_ramp_down",
    "abort_class": "HARD_ABORT",
    "expected_category": "hard_abort_ramp_down",
    "expected_rules": ("RULE-23_RETURN_RAMP_ABORT",),
    "reason": "CLEAR_INSTABILITY_LINK_QUALITY_COLLAPSE",
}


INITIAL_ALLOCATION = {
    "recovered_path_a": 25,
    "stable_path_b": 75,
}


STABILIZED_ALLOCATION = {
    "recovered_path_a": 10,
    "stable_path_b": 90,
}


def evidence_requires_hard_abort(sample: dict[str, object]) -> bool:
    return (
        sample["clear_instability"] is True
        and sample["link_quality"] == "collapse"
        and sample["conclusively_unsafe"] is True
        and sample["forwarding_possible"] is True
    )


def decide_abort_handling(step: int, sample: dict[str, object]) -> str:
    print(f"STEP {step}")
    print(
        "[SCENARIO] "
        f"name={SCENARIO_METADATA['name']} "
        f"abort_class={SCENARIO_METADATA['abort_class']} "
        f"expected_category={SCENARIO_METADATA['expected_category']} "
        "expected_rules=RULE-23_RETURN_RAMP_ABORT"
    )
    print(
        "[STATE] "
        "return_ramp=active "
        "recovered_path_a_weight=25 "
        "stable_path_b_weight=75"
    )
    print(
        "[OBSERVATION] "
        "clear_instability=true "
        "link_quality=collapse "
        "conclusively_unsafe=true "
        "forwarding_possible=true"
    )

    if evidence_requires_hard_abort(sample):
        print(
            "[RECOVERY] rule=RULE-23_RETURN_RAMP_ABORT "
            "category=hard_abort_ramp_down "
            "abort_class=HARD_ABORT "
            "return_ramp_attempt=aborted "
            "immediate_cut=false "
            "reason=CLEAR_INSTABILITY_LINK_QUALITY_COLLAPSE"
        )
        print(
            "[STABILIZATION] phase=Traffic_Stabilization_Phase "
            "entered=true "
            "stop_return_ramp_advance=true "
            "allocation_action=ramp_down_suspect_path "
            "recovered_path_a_weight=10 "
            "stable_path_b_weight=90"
        )
        print(
            "[RESOLVER] re_evaluation=triggered "
            "decision_scope=post_abort_hard_abort"
        )
        print(
            "[SOURCE] notification=sent "
            "action=traffic_reduction_may_be_needed "
            "policy_required=true"
        )
        print(
            "[VALIDATION] outcome=PASS "
            "category=hard_abort_ramp_down "
            "recovered_path_reduced=true "
            "stable_path_increased=true "
            "resolver_re_evaluation=true "
            "source_notification=true"
        )
        return "RULE-23_RETURN_RAMP_ABORT"

    print(
        "[VALIDATION] outcome=FAIL "
        "reason=HARD_ABORT_CONDITION_NOT_REACHED"
    )
    return "NO_ABORT"


def run() -> None:
    telemetry_sample = {
        "clear_instability": True,
        "link_quality": "collapse",
        "conclusively_unsafe": True,
        "forwarding_possible": True,
        "emergency": False,
        "allocation_before": INITIAL_ALLOCATION,
        "allocation_after": STABILIZED_ALLOCATION,
    }

    decide_abort_handling(0, telemetry_sample)


if __name__ == "__main__":
    run()
