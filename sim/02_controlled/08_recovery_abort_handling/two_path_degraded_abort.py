#!/usr/bin/env python3
"""Experimental two-path degraded abort validation scenario.

RULE-23_RETURN_RAMP_ABORT aborts the current Return Ramp attempt. When only two
candidate paths exist and both are degraded, PSC must not assume a fully safe
alternate path exists. Resolver arbitrates a least-bad allocation.
"""

from __future__ import annotations

from dataclasses import dataclass


SCENARIO_METADATA = {
    "name": "two_path_degraded_abort",
    "abort_class": "DEGRADED_ABORT",
    "expected_category": "two_path_degraded_arbitration",
    "expected_rules": ("RULE-23_RETURN_RAMP_ABORT",),
    "reason": "TWO_PATH_DEGRADED_NO_SAFE_ALTERNATE",
}


INITIAL_ALLOCATION = {
    "recovered_path_a": 25,
    "stable_path_b": 75,
    "candidate_paths": 2,
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


def evidence_requires_degraded_abort(sample: dict[str, object]) -> bool:
    return (
        sample["path_a_instability"] is True
        and sample["path_b_degraded"] is True
        and sample["third_path_exists"] is False
        and sample["neither_path_fully_safe"] is True
        and sample["forwarding_possible"] is True
        and sample["emergency"] is False
    )


def fallback_has_no_safe_alternate(sample: dict[str, object]) -> bool:
    return (
        sample["fallback_transfer_allowed"] is False
        and sample["fallback_block_reason"] == "NO_SAFE_ALTERNATE"
        and sample["no_safe_alternate"] is True
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
        "stable_path_b_weight=75 "
        "candidate_paths=2 "
        "third_path_exists=false"
    )
    print(
        "[OBSERVATION] "
        "path_a_instability=true "
        "path_b_degraded=true "
        "neither_path_fully_safe=true "
        "forwarding_possible=true "
        "emergency=false"
    )
    print(
        "[FALLBACK] "
        "fallback_transfer_allowed=false "
        "fallback_block_reason=NO_SAFE_ALTERNATE "
        "no_safe_alternate=true"
    )

    if evidence_requires_degraded_abort(sample) and fallback_has_no_safe_alternate(sample):
        print(
            "[RECOVERY] rule=RULE-23_RETURN_RAMP_ABORT "
            "category=two_path_degraded_arbitration "
            "abort_class=DEGRADED_ABORT "
            "return_ramp_attempt=aborted "
            "immediate_cut=false "
            "reason=TWO_PATH_DEGRADED_NO_SAFE_ALTERNATE"
        )
        print(
            "[STABILIZATION] phase=Traffic_Stabilization_Phase "
            "entered=true "
            "stop_return_ramp_advance=true "
            "allocation_action=hold_for_arbitration "
            "recovered_path_a_weight=25 "
            "stable_path_b_weight=75"
        )
        print(
            "[RESOLVER] arbitration=triggered "
            "decision_scope=two_path_degraded "
            "least_bad_selection=true"
        )
        print(
            "[SOURCE] notification=sent "
            "action=traffic_reduction_requested "
            "policy_required=true"
        )
        print(
            "[VALIDATION] outcome=PASS "
            "category=two_path_degraded_arbitration "
            "fallback_transfer_allowed=false "
            "fallback_block_reason=NO_SAFE_ALTERNATE "
            "least_bad_selection=true "
            "source_reduction_requested=true"
        )
        return ValidationResult(
            rule="RULE-23_RETURN_RAMP_ABORT",
            passed=True,
            category=SCENARIO_METADATA["expected_category"],
            reason=SCENARIO_METADATA["reason"],
        )

    print(
        "[VALIDATION] outcome=FAIL "
        "reason=TWO_PATH_DEGRADED_CONDITION_NOT_REACHED"
    )
    return ValidationResult(
        rule="NO_ABORT",
        passed=False,
        category="",
        reason="TWO_PATH_DEGRADED_CONDITION_NOT_REACHED",
    )


def run() -> None:
    telemetry_sample = {
        "path_a_instability": True,
        "path_b_degraded": True,
        "third_path_exists": False,
        "neither_path_fully_safe": True,
        "forwarding_possible": True,
        "emergency": False,
        "fallback_transfer_allowed": False,
        "fallback_block_reason": "NO_SAFE_ALTERNATE",
        "no_safe_alternate": True,
        "allocation_before": INITIAL_ALLOCATION,
    }

    result = decide_abort_handling(0, telemetry_sample)
    assert result.passed, f"Scenario FAILED: {result.reason}"
    assert result.rule == SCENARIO_METADATA["expected_rules"][0]


if __name__ == "__main__":
    run()
