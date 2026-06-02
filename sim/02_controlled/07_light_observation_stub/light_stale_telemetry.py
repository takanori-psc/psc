#!/usr/bin/env python3
"""Runnable LIGHT stale-telemetry validation scenario.

Present but outdated LIGHT telemetry is insufficient for return ramp advance.
"""

from __future__ import annotations


SCENARIO_METADATA = {
    "name": "light_stale_telemetry",
    "observation_mode": "LIGHT",
    "expected_category": "hold",
    "expected_rules": ("RULE-22_RETURN_RAMP_HOLD",),
    "reason": "STALE_TELEMETRY",
}


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

    print(f"STEP {step}")
    print(
        "[SCENARIO] "
        f"name={SCENARIO_METADATA['name']} "
        f"observation_mode={SCENARIO_METADATA['observation_mode']} "
        f"expected_category={SCENARIO_METADATA['expected_category']} "
        "expected_rules=RULE-22_RETURN_RAMP_HOLD"
    )

    if missing:
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "category=hold "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            f"scenario=light_stale_telemetry missing={','.join(missing)} "
            "reason=REQUIRED_TELEMETRY_MISSING"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    if sample["freshness"] == "stale":
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "category=hold "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            "telemetry_age=outdated "
            "confidence=insufficient "
            "scenario=light_stale_telemetry "
            "reason=STALE_TELEMETRY"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    print(
        "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
        "category=hold "
        "observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_stale_telemetry "
        "reason=NO_STALE_TELEMETRY_CASE"
    )
    return "RULE-22_RETURN_RAMP_HOLD"


def run() -> None:
    telemetry_sample = {
        "trust": 0.95,
        "stability_proxy": 0.97,
        "freshness": "stale",
        "confidence": "insufficient",
    }

    decide_light_ramp_step(0, telemetry_sample)


if __name__ == "__main__":
    run()
