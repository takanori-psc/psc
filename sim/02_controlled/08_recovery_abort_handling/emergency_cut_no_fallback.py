#!/usr/bin/env python3
"""Experimental emergency-cut recovery return validation scenario.

RULE-23_RETURN_RAMP_ABORT aborts the current Return Ramp attempt. In the
EMERGENCY_CUT class, PSC immediately excludes the unsafe recovered path. This
scenario uses NO_CAPACITY_MARGIN to distinguish why traffic cannot be safely
transferred to the remaining path.
"""

from __future__ import annotations

from dataclasses import dataclass


SCENARIO_METADATA = {
    "name": "emergency_cut_no_fallback",
    "abort_class": "EMERGENCY_CUT",
    "expected_category": "emergency_cut_no_fallback",
    "expected_rules": ("RULE-23_RETURN_RAMP_ABORT",),
    "reason": "LINK_DOWN_OPTICAL_FAILURE_NO_CAPACITY_MARGIN",
}


@dataclass(frozen=True)
class ValidationResult:
    """Structured result for validation harnesses.

    The emitted log remains fixed text so this scenario can still be used as a
    stable evidence trace. This object only makes the outcome assertable by
    callers and future batch validators.
    """

    rule: str
    passed: bool
    category: str
    reason: str


INITIAL_ALLOCATION = {
    "recovered_path_a": 25,
    "stable_path_b": 75,
}


EMERGENCY_ALLOCATION = {
    "recovered_path_a": 0,
    "stable_path_b": 75,
    "dropped_or_blocked": 25,
}


def evidence_requires_emergency_cut(sample: dict[str, object]) -> bool:
    return (
        sample["path_a_link_down"] is True
        and sample["optical_failure"] is True
        and sample["forwarding_possible"] is False
        and sample["conclusively_unsafe"] is True
        and sample["emergency"] is True
    )


def fallback_transfer_is_blocked(sample: dict[str, object]) -> bool:
    return (
        sample["path_b_exists"] is True
        and sample["path_b_failed"] is False
        and sample["path_b_capacity_margin"] == "insufficient"
        and sample["fallback_block_reason"] == "NO_CAPACITY_MARGIN"
    )


def decide_abort_handling(step: int, sample: dict[str, object]) -> ValidationResult:
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
        "path_a_link_down=true "
        "optical_failure=true "
        "forwarding_possible=false "
        "conclusively_unsafe=true "
        "emergency=true"
    )
    print(
        "[FALLBACK] "
        "path_b_exists=true "
        "path_b_failed=false "
        "path_b_capacity_margin=insufficient "
        "fallback_transfer_allowed=false "
        "fallback_block_reason=NO_CAPACITY_MARGIN"
    )

    if evidence_requires_emergency_cut(sample) and fallback_transfer_is_blocked(sample):
        print(
            "[RECOVERY] rule=RULE-23_RETURN_RAMP_ABORT "
            "category=emergency_cut_no_fallback "
            "abort_class=EMERGENCY_CUT "
            "return_ramp_attempt=aborted "
            "immediate_cut=true "
            "reason=LINK_DOWN_OPTICAL_FAILURE_NO_CAPACITY_MARGIN"
        )
        print(
            "[EMERGENCY] emergency_cut=true "
            "path_a_excluded=true "
            "recovered_path_a_weight=0 "
            "stable_path_b_weight=75 "
            "dropped_or_blocked_weight=25"
        )
        print(
            "[STABILIZATION] phase=Traffic_Stabilization_Phase "
            "entered=false "
            "reason=EMERGENCY_CUT_NO_SAFE_TRANSFER"
        )
        print(
            "[RESOLVER] notification=triggered "
            "decision_scope=emergency_cut_no_fallback"
        )
        print(
            "[SOURCE] notification=sent "
            "action=emergency_throttle_or_stop "
            "required=true "
            "policy_required=true"
        )
        print(
            "[VALIDATION] outcome=PASS "
            "category=emergency_cut_no_fallback "
            "immediate_cut=true "
            "path_excluded=true "
            "fallback_transfer_allowed=false "
            "fallback_block_reason=NO_CAPACITY_MARGIN "
            "source_emergency_control=true"
        )
        return ValidationResult(
            rule="RULE-23_RETURN_RAMP_ABORT",
            passed=True,
            category=SCENARIO_METADATA["expected_category"],
            reason=SCENARIO_METADATA["reason"],
        )

    print(
        "[VALIDATION] outcome=FAIL "
        "reason=EMERGENCY_CUT_CONDITION_NOT_REACHED"
    )
    return ValidationResult(
        rule="NO_ABORT",
        passed=False,
        category="",
        reason="EMERGENCY_CUT_CONDITION_NOT_REACHED",
    )


def run() -> None:
    telemetry_sample = {
        "path_a_link_down": True,
        "optical_failure": True,
        "forwarding_possible": False,
        "conclusively_unsafe": True,
        "emergency": True,
        "path_b_exists": True,
        "path_b_failed": False,
        "path_b_capacity_margin": "insufficient",
        "fallback_transfer_allowed": False,
        "fallback_block_reason": "NO_CAPACITY_MARGIN",
        "allocation_before": INITIAL_ALLOCATION,
        "allocation_after": EMERGENCY_ALLOCATION,
    }

    result = decide_abort_handling(0, telemetry_sample)
    assert result.passed, f"Scenario FAILED: {result.reason}"
    assert result.rule == SCENARIO_METADATA["expected_rules"][0]


if __name__ == "__main__":
    run()
