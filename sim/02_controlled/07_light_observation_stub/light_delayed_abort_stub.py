#!/usr/bin/env python3
"""Minimal LIGHT delayed-abort scenario stub.

This stub represents hard failure detected only after LIGHT misses instability.
"""

from __future__ import annotations


REQUIRED_LIGHT_TELEMETRY = (
    "trust",
    "stability_proxy",
    "freshness",
    "confidence",
    "hard_failure",
    "prior_instability_observed",
)


def missing_required_fields(sample: dict[str, object]) -> list[str]:
    return [
        field
        for field in REQUIRED_LIGHT_TELEMETRY
        if field not in sample or sample[field] is None
    ]


def delayed_hard_failure_detected(sample: dict[str, object]) -> bool:
    return (
        sample["freshness"] == "current"
        and sample["prior_instability_observed"] is False
        and sample["hard_failure"] is True
    )


def observe_light_step(step: int, sample: dict[str, object]) -> str:
    missing = missing_required_fields(sample)

    if missing:
        print(f"STEP {step}")
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            f"scenario=light_delayed_abort missing={','.join(missing)} "
            "reason=REQUIRED_TELEMETRY_MISSING"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    if delayed_hard_failure_detected(sample):
        print(f"STEP {step}")
        print(
            "[RECOVERY] rule=RULE-23_RETURN_RAMP_ABORT "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            "scenario=light_delayed_abort "
            "reason=DELAYED_HARD_FAILURE_DETECTED"
        )
        return "RULE-23_RETURN_RAMP_ABORT"

    print(f"STEP {step}")
    print(
        "[OBSERVATION] observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_delayed_abort "
        "reason=INSTABILITY_NOT_DETECTED_BY_LIGHT"
    )
    return "NO_RULE_EMITTED"


def run() -> None:
    telemetry_samples = (
        {
            "trust": 0.95,
            "stability_proxy": 0.97,
            "freshness": "current",
            "confidence": "accepted",
            "hard_failure": False,
            "prior_instability_observed": False,
        },
        {
            "trust": 0.95,
            "stability_proxy": 0.97,
            "freshness": "current",
            "confidence": "accepted",
            "hard_failure": True,
            "prior_instability_observed": False,
        },
    )

    for step, sample in enumerate(telemetry_samples):
        observe_light_step(step, sample)


if __name__ == "__main__":
    run()
