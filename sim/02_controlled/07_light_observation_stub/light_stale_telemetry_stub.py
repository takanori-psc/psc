#!/usr/bin/env python3
"""Minimal LIGHT stale-telemetry scenario stub.

This stub proves that present telemetry is not automatically usable telemetry.
"""

from __future__ import annotations


REQUIRED_LIGHT_TELEMETRY = (
    "trust",
    "stability_proxy",
    "freshness",
    "confidence",
)


def missing_required_fields(sample: dict[str, object]) -> list[str]:
    return [
        field
        for field in REQUIRED_LIGHT_TELEMETRY
        if field not in sample or sample[field] is None
    ]


def decide_light_ramp_step(step: int, sample: dict[str, object]) -> str:
    missing = missing_required_fields(sample)

    if missing:
        print(f"STEP {step}")
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            f"scenario=light_stale_telemetry missing={','.join(missing)} "
            "reason=REQUIRED_TELEMETRY_MISSING"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    if sample["freshness"] == "stale":
        print(f"STEP {step}")
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            "scenario=light_stale_telemetry reason=STALE_TELEMETRY"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    print(f"STEP {step}")
    print(
        "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
        "observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_stale_telemetry reason=NO_STALE_TELEMETRY_CASE"
    )
    return "RULE-22_RETURN_RAMP_HOLD"


def run() -> None:
    telemetry_sample = {
        "trust": 0.95,
        "stability_proxy": 0.97,
        "freshness": "stale",
        "confidence": "accepted",
    }

    decide_light_ramp_step(0, telemetry_sample)


if __name__ == "__main__":
    run()
