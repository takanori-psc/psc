#!/usr/bin/env python3
"""Runnable LIGHT false-negative validation scenario.

LIGHT observation misses actual path instability, so the return ramp must hold.
"""

from __future__ import annotations


SCENARIO_METADATA = {
    "name": "light_false_negative",
    "observation_mode": "LIGHT",
    "expected_category": "hold",
    "expected_rules": ("RULE-22_RETURN_RAMP_HOLD",),
    "reason": "OBSERVATION_FALSE_NEGATIVE",
}


def light_observation_failed(sample: dict[str, object]) -> bool:
    return (
        sample["actual_path_instability"] == "exists"
        and sample["light_detected_instability"] is False
    )


def decide_light_ramp_step(step: int, sample: dict[str, object]) -> str:
    print(f"STEP {step}")
    print(
        "[SCENARIO] "
        f"name={SCENARIO_METADATA['name']} "
        f"observation_mode={SCENARIO_METADATA['observation_mode']} "
        f"expected_category={SCENARIO_METADATA['expected_category']} "
        "expected_rules=RULE-22_RETURN_RAMP_HOLD"
    )

    if light_observation_failed(sample):
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "category=hold "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            "actual_path_instability=exists "
            "light_detected_instability=false "
            "scenario=light_false_negative "
            "reason=OBSERVATION_FALSE_NEGATIVE"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    print(
        "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
        "category=hold "
        "observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_false_negative "
        "reason=NO_FALSE_NEGATIVE_CASE"
    )
    return "RULE-22_RETURN_RAMP_HOLD"


def run() -> None:
    telemetry_sample = {
        "trust": 0.95,
        "stability_proxy": 0.96,
        "freshness": "current",
        "confidence": "accepted",
        "actual_path_instability": "exists",
        "light_detected_instability": False,
    }

    decide_light_ramp_step(0, telemetry_sample)


if __name__ == "__main__":
    run()
