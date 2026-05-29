#!/usr/bin/env python3
"""Minimal LIGHT resolver-escalation scenario stub.

This stub represents conflicting LIGHT evidence that cannot decide recovery vs risk.
"""

from __future__ import annotations


REQUIRED_LIGHT_TELEMETRY = (
    "trust_evidence",
    "stability_evidence",
    "confidence_evidence",
    "freshness",
)


def missing_required_fields(sample: dict[str, object]) -> list[str]:
    return [
        field
        for field in REQUIRED_LIGHT_TELEMETRY
        if field not in sample or sample[field] is None
    ]


def evidence_conflicts(sample: dict[str, object]) -> bool:
    return (
        sample["freshness"] == "current"
        and sample["trust_evidence"] == "recovery"
        and sample["stability_evidence"] == "risk"
        and sample["confidence_evidence"] == "ambiguous"
    )


def observe_light_step(step: int, sample: dict[str, object]) -> str:
    missing = missing_required_fields(sample)

    if missing:
        print(f"STEP {step}")
        print(
            "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            f"scenario=light_resolver_escalation missing={','.join(missing)} "
            "reason=REQUIRED_TELEMETRY_MISSING"
        )
        return "RULE-22_RETURN_RAMP_HOLD"

    if evidence_conflicts(sample):
        print(f"STEP {step}")
        print(
            "[ESCALATE] rule=RULE-05_ESCALATE_conflict "
            "observation_mode=LIGHT "
            "ramp_state=RAMPING "
            "scenario=light_resolver_escalation "
            "reason=LIGHT_EVIDENCE_CONFLICT"
        )
        return "RULE-05_ESCALATE_conflict"

    print(f"STEP {step}")
    print(
        "[RECOVERY] rule=RULE-22_RETURN_RAMP_HOLD "
        "observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_resolver_escalation reason=NO_CONFLICT_CASE"
    )
    return "RULE-22_RETURN_RAMP_HOLD"


def emit_cooldown(step: int) -> str:
    print(f"STEP {step}")
    print(
        "[STATE] rule=RULE-12_COOLDOWN_active "
        "observation_mode=LIGHT "
        "ramp_state=RAMPING "
        "scenario=light_resolver_escalation "
        "reason=RESOLVER_ESCALATION_COOLDOWN"
    )
    return "RULE-12_COOLDOWN_active"


def run() -> None:
    telemetry_sample = {
        "trust_evidence": "recovery",
        "stability_evidence": "risk",
        "confidence_evidence": "ambiguous",
        "freshness": "current",
    }

    observe_light_step(0, telemetry_sample)
    emit_cooldown(1)


if __name__ == "__main__":
    run()
