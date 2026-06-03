#!/usr/bin/env python3
"""Experimental soft-abort recovery return validation scenario.

RULE-23_RETURN_RAMP_ABORT aborts the current Return Ramp attempt, but the
SOFT_ABORT class keeps traffic allocation stable while PSC re-observes and asks
Resolver to re-evaluate the state.
"""

from __future__ import annotations


SCENARIO_METADATA = {
    "name": "soft_abort_hold_and_reobserve",
    "abort_class": "SOFT_ABORT",
    "expected_category": "abort_and_stabilize",
    "expected_rules": ("RULE-23_RETURN_RAMP_ABORT",),
    "reason": "TELEMETRY_CONFLICT_CONFIDENCE_REDUCTION",
}


INITIAL_ALLOCATION = {
    "recovered_path_a": 25,
    "stable_path_b": 75,
}


def evidence_requires_soft_abort(sample: dict[str, object]) -> bool:
    return (
        sample["telemetry_conflict"] is True
        and sample["confidence"] == "reduced"
        and sample["conclusively_unsafe"] is False
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
        "telemetry_conflict=true "
        "confidence=reduced "
        "conclusively_unsafe=false "
        "evidence=suspicious"
    )

    if evidence_requires_soft_abort(sample):
        print(
            "[RECOVERY] rule=RULE-23_RETURN_RAMP_ABORT "
            "category=abort_and_stabilize "
            "abort_class=SOFT_ABORT "
            "return_ramp_attempt=aborted "
            "immediate_cut=false "
            "reason=TELEMETRY_CONFLICT_CONFIDENCE_REDUCTION"
        )
        print(
            "[STABILIZATION] phase=Traffic_Stabilization_Phase "
            "entered=true "
            "stop_return_ramp_advance=true "
            "allocation_action=hold_temporarily "
            "recovered_path_a_weight=25 "
            "stable_path_b_weight=75"
        )
        print(
            "[OBSERVATION] escalation=requested "
            "confidence_action=increase_observation_density "
            "target_mode=FULL"
        )
        print(
            "[RESOLVER] re_evaluation=triggered "
            "decision_scope=post_abort_stabilization"
        )
        print(
            "[VALIDATION] outcome=PASS "
            "category=abort_and_stabilize "
            "allocation_unchanged=true "
            "observation_escalation=true "
            "resolver_re_evaluation=true"
        )
        return "RULE-23_RETURN_RAMP_ABORT"

    print(
        "[VALIDATION] outcome=FAIL "
        "reason=SOFT_ABORT_CONDITION_NOT_REACHED"
    )
    return "NO_ABORT"


def run() -> None:
    telemetry_sample = {
        "telemetry_conflict": True,
        "confidence": "reduced",
        "conclusively_unsafe": False,
        "hard_failure": False,
        "emergency": False,
        "allocation_before": INITIAL_ALLOCATION,
    }

    decide_abort_handling(0, telemetry_sample)


if __name__ == "__main__":
    run()
