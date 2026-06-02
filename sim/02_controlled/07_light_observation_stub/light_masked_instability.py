#!/usr/bin/env python3
"""Runnable LIGHT masked-instability validation scenario.

A healthy-looking LIGHT proxy cannot safely advance when hidden instability exists.
"""

from __future__ import annotations


SCENARIO_METADATA = {
    "name": "light_masked_instability",
    "observation_mode": "LIGHT",
    "expected_category": "hold",
    "expected_rules": ("RULE-22_RETURN_RAMP_HOLD",),
    "reason": "MASKED_INSTABILITY",
}


REQUIRED_LIGHT_TELEMETRY = (
    "trust",
    "stability_proxy",
    "freshness",
    "confidence",
    "hidden_instability",
)


def missing_required_fields(sample: dict[str, object]) -> list[str]:
    return [
        field
        for field in REQUIRED_LIGHT_TELEMETRY
        if field not in sample or sample[field] is None
    ]


def instability_masked_by_proxy(sample: dict[str, object]) -> bool:
    return (
        sample["freshness"] == "current"
        and sample["stability_proxy"] == "healthy"
        and sample["hidden_instability"] == "exists"
    )


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
            f"scenario=light_masked_instability missing={','.join(missing)} "
            "reason=REQUIRED_TELEMETRY_MISSING"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    if instability_masked_by_proxy(sample):
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "category=hold "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            "stability_proxy=healthy "
            "hidden_instability=exists "
            "resolver_can_advance=false "
            "scenario=light_masked_instability "
            "reason=MASKED_INSTABILITY"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    print(
        "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
        "category=hold "
        "observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_masked_instability "
        "reason=NO_MASKED_INSTABILITY_CASE"
    )
    return "RULE-22_RETURN_RAMP_HOLD"


def run() -> None:
    telemetry_sample = {
        "trust": 0.95,
        "stability_proxy": "healthy",
        "freshness": "current",
        "confidence": "accepted",
        "hidden_instability": "exists",
    }

    decide_light_ramp_step(0, telemetry_sample)


if __name__ == "__main__":
    run()
