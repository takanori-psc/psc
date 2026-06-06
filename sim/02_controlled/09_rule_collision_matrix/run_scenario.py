#!/usr/bin/env python3
"""Minimal PSC rule collision simulator.

Scenario files are JSON so the runner stays dependency-free.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


RuleFunc = Callable[[dict[str, Any]], "RuleResult | None"]


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    action: str
    priority: int
    reason: str
    registry_index: int


@dataclass(frozen=True)
class StepResult:
    step_id: Any
    triggered: list[RuleResult]
    suppressed: list[RuleResult]
    final_action: str
    expected_action: str
    outcome: str


def _state(step: dict[str, Any]) -> dict[str, Any]:
    return step.get("state", {})


def _telemetry(step: dict[str, Any]) -> dict[str, Any]:
    return step.get("telemetry", {})


def rule_02_switch_score(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)
    current_path = state.get("current_path")
    best_path = telemetry.get("best_path")
    score_gap = float(telemetry.get("score_gap", 0.0))
    switch_margin = float(state.get("switch_margin", 0.10))

    if current_path and best_path and best_path != current_path and score_gap >= switch_margin:
        return RuleResult(
            "RULE-02_SWITCH_score",
            f"SWITCH_TO_{best_path}",
            40,
            f"score_gap={score_gap:.2f} >= switch_margin={switch_margin:.2f}",
            -1,
        )
    return None


def rule_05_escalate_conflict(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)
    conflict = telemetry.get("conflict")
    score_gap = float(telemetry.get("score_gap", 0.0))
    epsilon = float(state.get("epsilon", 0.05))

    if conflict in ("TRUST_CONFLICT", "STABILITY_CONFLICT") and score_gap < epsilon:
        return RuleResult(
            "RULE-05_ESCALATE_conflict",
            "ESCALATE_TO_RESOLVER",
            70,
            f"{conflict} with score_gap={score_gap:.2f} < epsilon={epsilon:.2f}",
            -1,
        )
    return None


def rule_22_return_ramp_hold(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)

    if (
        state.get("return_ramp") == "active"
        and telemetry.get("ramp_complete") is not True
    ):
        return RuleResult(
            "RULE-22_RETURN_RAMP_HOLD",
            "RETURN_RAMP_HOLD",
            50,
            "return ramp remains active while completion is not confirmed",
            -1,
        )
    return None


def rule_23_return_ramp_abort(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)

    if state.get("return_ramp") != "active":
        return None

    abort_reasons = []
    if telemetry.get("abort_signal") is True:
        abort_reasons.append("abort_signal=true")
    if telemetry.get("emergency") is True:
        abort_reasons.append("emergency=true")
    if telemetry.get("telemetry_conflict") is True and telemetry.get("confidence") == "reduced":
        abort_reasons.append("telemetry_conflict=true confidence=reduced")
    if telemetry.get("recovered_path_stability", 1.0) < state.get("ramp_abort_stability", 0.60):
        abort_reasons.append(
            "recovered_path_stability="
            f"{float(telemetry.get('recovered_path_stability')):.2f} "
            f"< ramp_abort_stability={float(state.get('ramp_abort_stability', 0.60)):.2f}"
        )

    if abort_reasons:
        return RuleResult(
            "RULE-23_RETURN_RAMP_ABORT",
            "RETURN_RAMP_ABORT",
            90,
            "; ".join(abort_reasons),
            -1,
        )
    return None


def rule_24_return_ramp_complete(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)

    if (
        state.get("return_ramp") == "active"
        and telemetry.get("ramp_complete") is True
        and telemetry.get("abort_signal") is not True
        and telemetry.get("emergency") is not True
    ):
        return RuleResult(
            "RULE-24_RETURN_RAMP_COMPLETE",
            "RETURN_RAMP_COMPLETE",
            60,
            "ramp_complete=true and no abort condition is active",
            -1,
        )
    return None


RULES: tuple[tuple[str, RuleFunc], ...] = (
    ("RULE-02_SWITCH_score", rule_02_switch_score),
    ("RULE-05_ESCALATE_conflict", rule_05_escalate_conflict),
    ("RULE-22_RETURN_RAMP_HOLD", rule_22_return_ramp_hold),
    ("RULE-23_RETURN_RAMP_ABORT", rule_23_return_ramp_abort),
    ("RULE-24_RETURN_RAMP_COMPLETE", rule_24_return_ramp_complete),
)


def evaluate_rules(step: dict[str, Any]) -> list[RuleResult]:
    triggered: list[RuleResult] = []
    for index, (rule_id, rule_func) in enumerate(RULES):
        result = rule_func(step)
        if result is not None:
            if result.rule_id != rule_id:
                raise ValueError(f"rule registry mismatch: {rule_id} returned {result.rule_id}")
            triggered.append(
                RuleResult(
                    result.rule_id,
                    result.action,
                    result.priority,
                    result.reason,
                    index,
                )
            )
    return triggered


def resolve_collision(triggered: list[RuleResult]) -> tuple[RuleResult | None, list[RuleResult]]:
    if not triggered:
        return None, []

    ordered = sorted(triggered, key=lambda item: (-item.priority, item.registry_index))
    return ordered[0], ordered[1:]


def load_scenario(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        scenario = json.load(handle)

    if not isinstance(scenario.get("steps"), list):
        raise ValueError("scenario must contain a steps array")
    return scenario


def print_rule_list(label: str, rules: list[RuleResult]) -> None:
    if not rules:
        print(f"{label}: none")
        return

    print(f"{label}:")
    for rule in rules:
        print(
            "  "
            f"- rule_id={rule.rule_id} "
            f"action={rule.action} "
            f"priority={rule.priority} "
            f"reason={rule.reason}"
        )


def append_markdown_rule_list(lines: list[str], label: str, rules: list[RuleResult]) -> None:
    lines.append(f"### {label}")
    if not rules:
        lines.append("")
        lines.append("none")
        lines.append("")
        return

    lines.append("")
    for rule in rules:
        lines.append(
            f"- rule_id={rule.rule_id} "
            f"action={rule.action} "
            f"priority={rule.priority} "
            f"reason={rule.reason}"
        )
    lines.append("")


def safe_filename(value: str) -> str:
    safe_chars = []
    for char in value:
        if char.isalnum() or char in ("-", "_"):
            safe_chars.append(char)
        else:
            safe_chars.append("_")
    return "".join(safe_chars).strip("_") or "unnamed"


def write_validation_log(
    scenario: dict[str, Any],
    step_results: list[StepResult],
    overall_outcome: str,
) -> Path:
    scenario_name = str(scenario.get("name", "unnamed"))
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{safe_filename(scenario_name)}_validation_log.md"

    lines = [
        f"# Validation Log: {scenario_name}",
        "",
        f"- Scenario name: {scenario_name}",
        f"- Description: {scenario.get('description', '')}",
        f"- Registered rules: {', '.join(rule_id for rule_id, _ in RULES)}",
        "",
    ]

    for result in step_results:
        lines.append(f"## Step {result.step_id}")
        lines.append("")
        append_markdown_rule_list(lines, "Triggered rules", result.triggered)
        append_markdown_rule_list(lines, "Suppressed rules", result.suppressed)
        lines.append(f"- Final action: {result.final_action}")
        lines.append(f"- Expected action: {result.expected_action}")
        lines.append(f"- Result: {result.outcome}")
        lines.append("")

    lines.append(f"## Overall {overall_outcome}")
    lines.append("")

    log_path.write_text("\n".join(lines), encoding="utf-8")
    return log_path


def run_scenario(scenario: dict[str, Any]) -> bool:
    print(f"SCENARIO {scenario.get('name', 'unnamed')}")
    print(f"DESCRIPTION {scenario.get('description', '')}")
    print(f"REGISTERED_RULES {', '.join(rule_id for rule_id, _ in RULES)}")
    print()

    all_passed = True
    step_results: list[StepResult] = []
    for index, step in enumerate(scenario["steps"]):
        step_id = step.get("step_id", index)
        triggered = evaluate_rules(step)
        winner, suppressed = resolve_collision(triggered)
        final_action = winner.action if winner else "NO_ACTION"
        expected_action = step.get("expected_action", "NO_ACTION")
        outcome = "PASS" if final_action == expected_action else "FAIL"
        all_passed = all_passed and outcome == "PASS"
        step_results.append(
            StepResult(
                step_id,
                triggered,
                suppressed,
                final_action,
                expected_action,
                outcome,
            )
        )

        print(f"STEP {step_id}")
        print_rule_list("triggered_rules", triggered)
        print_rule_list("suppressed_rules", suppressed)
        print(f"final_action: {final_action}")
        print(f"expected_action: {expected_action}")
        print(f"result: {outcome}")
        print()

    overall_outcome = "PASS" if all_passed else "FAIL"
    write_validation_log(scenario, step_results, overall_outcome)
    print(f"OVERALL {overall_outcome}")
    return all_passed


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <scenario.json>", file=sys.stderr)
        return 2

    scenario = load_scenario(Path(argv[1]))
    return 0 if run_scenario(scenario) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
