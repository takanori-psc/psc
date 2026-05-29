#!/usr/bin/env python3
"""Minimal LIGHT masked-instability scenario stub.

This stub represents instability risk hidden between sparse LIGHT observations.
"""

from __future__ import annotations


REQUIRED_LIGHT_TELEMETRY = (
    "trust",
    "stability_proxy",
    "freshness",
    "confidence",
    "observed_window",
    "unobserved_window",
)


def missing_required_fields(sample: dict[str, object]) -> list[str]:
    return [
        field
        for field in REQUIRED_LIGHT_TELEMETRY
        if field not in sample or sample[field] is None
    ]


def instability_masked_by_light_gap(sample: dict[str, object]) -> bool:
    return (
        sample["freshness"] == "current"
        and sample["observed_window"] == "stable"
        and sample["unobserved_window"] == "instability_risk"
    )


def decide_light_ramp_step(step: int, sample: dict[str, object]) -> str:
    missing = missing_required_fields(sample)

    if missing:
        print(f"STEP {step}")
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            f"scenario=light_masked_instability missing={','.join(missing)} "
            "reason=REQUIRED_TELEMETRY_MISSING"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    if instability_masked_by_light_gap(sample):
        print(f"STEP {step}")
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            "scenario=light_masked_instability "
            "reason=MASKED_INSTABILITY_RISK"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    print(f"STEP {step}")
    print(
        "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
        "observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_masked_instability reason=NO_MASKED_INSTABILITY_CASE"
    )
    return "RULE-22_RETURN_RAMP_HOLD"


def run() -> None:
    telemetry_sample = {
        "trust": 0.95,
        "stability_proxy": 0.97,
        "freshness": "current",
        "confidence": "accepted",
        "observed_window": "stable",
        "unobserved_window": "instability_risk",
    }

    decide_light_ramp_step(0, telemetry_sample)


if __name__ == "__main__":
    run()
