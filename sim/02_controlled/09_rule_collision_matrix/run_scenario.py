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

BASE_DIR = Path(__file__).resolve().parent
SCENARIO_DIR = BASE_DIR / "scenarios"
SCENARIO_ALIASES: dict[str, str] = {
    "abort": "return_vs_abort",
    "return": "return_vs_abort",
    "return_abort": "return_vs_abort",
    "escalate": "switch_vs_escalate",
    "switch_escalate": "switch_vs_escalate",
    "keep": "keep_vs_switch",
    "keep_switch": "keep_vs_switch",
    "trust_block": "trust_block_vs_switch",
    "block": "trust_block_vs_switch",
}


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


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    evaluate: RuleFunc


# ============================================================
# Rule Priority Table
# ============================================================
#
# This table is the single source of priority values for rules integrated into
# the collision matrix. A value of None does not mean the PSC rule is undefined;
# it means this simulator has no collision predicate/priority for that rule yet.
# External-active entries name the Evidence Matrix owner so bare RULE numbers do
# not obscure the current operational namespace.
RULE_PRIORITY_TABLE: dict[str, int | None] = {
    "RULE-01_KEEP_score": 20,
    "RULE-02_SWITCH_score": 40,
    "RULE-03_SWITCH_trust": 65,
    "RULE-04_BLOCK_trust": 80,
    "RULE-05_ESCALATE_conflict": 70,
    "RULE-06": None,  # reserved_future.
    "RULE-07_DEGRADE_trigger": None,  # external_active_not_integrated.
    "RULE-08_DEGRADE_keep": None,  # external_active_not_integrated.
    "RULE-09_DEGRADE_switch": None,  # external_active_not_integrated.
    "RULE-10_RECOVERY_trigger": None,  # external_active_not_integrated.
    "RULE-11_RECOVERY_cooldown": None,  # external_active_not_integrated.
    "RULE-12_COOLDOWN_active": None,  # external_active_not_integrated.
    "RULE-13_RESOLVER_keep": None,  # external_active_not_integrated.
    "RULE-14_RESOLVER_switch": None,  # external_active_not_integrated.
    "RULE-15_RECOVERY_CANDIDATE": None,  # external_active_not_integrated.
    "RULE-16_RECOVERY_VALIDATION_START": None,  # external_active_not_integrated.
    "RULE-17_RECOVERY_VALIDATION_PASS": None,  # legacy_reserved.
    "RULE-18_RETURN_ELIGIBLE": None,  # external_active_not_integrated.
    "RULE-19_RETURN_SWITCH": None,  # external_active_not_integrated.
    "RULE-20_RETURN_KEEP": None,  # external_active_not_integrated.
    "RULE-21_RETURN_RAMP_ADVANCE": None,  # external_active_not_integrated.
    "RULE-22_RETURN_RAMP_HOLD": 50,
    "RULE-23_RETURN_RAMP_ABORT": 90,
    "RULE-24_RETURN_RAMP_COMPLETE": 60,
}


def rule_priority(rule_id: str) -> int:
    priority = RULE_PRIORITY_TABLE.get(rule_id)
    if priority is None:
        raise ValueError(f"rule priority is not registered for active rule: {rule_id}")
    return priority


def _state(step: dict[str, Any]) -> dict[str, Any]:
    return step.get("state", {})


def _telemetry(step: dict[str, Any]) -> dict[str, Any]:
    return step.get("telemetry", {})


def _path_trust(telemetry: dict[str, Any], path_name: Any) -> float | None:
    path_trust = telemetry.get("path_trust", {})
    if not isinstance(path_trust, dict) or path_name not in path_trust:
        return None
    return float(path_trust[path_name])


def rule_01_keep_score(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)
    current_path = state.get("current_path")

    if current_path and telemetry.get("keep_score_recommended") is True:
        return RuleResult(
            "RULE-01_KEEP_score",
            "KEEP_CURRENT",
            rule_priority("RULE-01_KEEP_score"),
            f"keep_score_recommended=true current_path={current_path}",
            -1,
        )
    return None


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
            rule_priority("RULE-02_SWITCH_score"),
            f"score_gap={score_gap:.2f} >= switch_margin={switch_margin:.2f}",
            -1,
        )
    return None


def rule_03_switch_trust(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)
    current_path = state.get("current_path")
    best_path = telemetry.get("best_path")
    trust_switch_threshold = float(state.get("trust_switch_threshold", 0.80))

    if not current_path or not best_path or best_path == current_path:
        return None

    current_trust = _path_trust(telemetry, current_path)
    best_trust = _path_trust(telemetry, best_path)
    if current_trust is None or best_trust is None:
        return None

    if best_trust >= trust_switch_threshold and best_trust > current_trust:
        return RuleResult(
            "RULE-03_SWITCH_trust",
            f"SWITCH_TO_{best_path}",
            rule_priority("RULE-03_SWITCH_trust"),
            f"trust[{best_path}]={best_trust:.2f} >= "
            f"trust_switch_threshold={trust_switch_threshold:.2f} "
            f"and trust[{best_path}] > trust[{current_path}]={current_trust:.2f}",
            -1,
        )
    return None


def rule_04_block_trust(step: dict[str, Any]) -> RuleResult | None:
    state = _state(step)
    telemetry = _telemetry(step)
    current_path = state.get("current_path")
    best_path = telemetry.get("best_path")
    trust_block_threshold = float(state.get("trust_block_threshold", 0.50))
    blocked_paths = telemetry.get("trust_blocked_paths", [])

    if not current_path or not best_path or best_path == current_path:
        return None

    best_trust = _path_trust(telemetry, best_path)
    explicit_block = isinstance(blocked_paths, list) and best_path in blocked_paths
    threshold_block = best_trust is not None and best_trust <= trust_block_threshold

    if explicit_block or threshold_block:
        reasons = []
        if explicit_block:
            reasons.append(f"{best_path} in trust_blocked_paths")
        if threshold_block:
            reasons.append(
                f"trust[{best_path}]={best_trust:.2f} <= "
                f"trust_block_threshold={trust_block_threshold:.2f}"
            )
        return RuleResult(
            "RULE-04_BLOCK_trust",
            "BLOCK_SWITCH",
            rule_priority("RULE-04_BLOCK_trust"),
            "; ".join(reasons),
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
            rule_priority("RULE-05_ESCALATE_conflict"),
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
            rule_priority("RULE-22_RETURN_RAMP_HOLD"),
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
            rule_priority("RULE-23_RETURN_RAMP_ABORT"),
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
            rule_priority("RULE-24_RETURN_RAMP_COMPLETE"),
            "ramp_complete=true and no abort condition is active",
            -1,
        )
    return None


# ============================================================
# RULE_REGISTRY
# ============================================================
#
# Only implemented rules are active here. Placeholder priority entries above
# reserve RULE-01 through RULE-24 without evaluating inactive rules.
RULE_REGISTRY: tuple[RuleDefinition, ...] = (
    RuleDefinition("RULE-01_KEEP_score", rule_01_keep_score),
    RuleDefinition("RULE-02_SWITCH_score", rule_02_switch_score),
    RuleDefinition("RULE-03_SWITCH_trust", rule_03_switch_trust),
    RuleDefinition("RULE-04_BLOCK_trust", rule_04_block_trust),
    RuleDefinition("RULE-05_ESCALATE_conflict", rule_05_escalate_conflict),
    RuleDefinition("RULE-22_RETURN_RAMP_HOLD", rule_22_return_ramp_hold),
    RuleDefinition("RULE-23_RETURN_RAMP_ABORT", rule_23_return_ramp_abort),
    RuleDefinition("RULE-24_RETURN_RAMP_COMPLETE", rule_24_return_ramp_complete),
)


def evaluate_rules(step: dict[str, Any]) -> list[RuleResult]:
    triggered: list[RuleResult] = []
    for index, rule in enumerate(RULE_REGISTRY):
        result = rule.evaluate(step)
        if result is not None:
            if result.rule_id != rule.rule_id:
                raise ValueError(f"rule registry mismatch: {rule.rule_id} returned {result.rule_id}")
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


def list_scenario_files() -> list[Path]:
    return sorted(SCENARIO_DIR.glob("*.json"))


def scenario_name_from_path(path: Path) -> str:
    try:
        return str(load_scenario(path).get("name", path.stem))
    except (OSError, json.JSONDecodeError, ValueError):
        return path.stem


def scenario_aliases_for(name: str) -> list[str]:
    aliases = [alias for alias, target in SCENARIO_ALIASES.items() if target == name]
    return sorted(aliases)


def print_scenario_list() -> None:
    print("SCENARIOS")
    for index, path in enumerate(list_scenario_files(), start=1):
        name = scenario_name_from_path(path)
        aliases = scenario_aliases_for(name)
        alias_text = f" aliases={', '.join(aliases)}" if aliases else ""
        print(f"{index}. {name} path={path}{alias_text}")


def resolve_scenario_path(selector: str) -> Path:
    candidate = Path(selector)
    if candidate.exists():
        return candidate

    scenario_files = list_scenario_files()
    if selector.isdigit():
        scenario_index = int(selector)
        if 1 <= scenario_index <= len(scenario_files):
            return scenario_files[scenario_index - 1]
        raise ValueError(f"scenario number out of range: {selector}")

    normalized = selector[:-5] if selector.endswith(".json") else selector
    normalized = SCENARIO_ALIASES.get(normalized, normalized)

    for path in scenario_files:
        scenario_name = scenario_name_from_path(path)
        if normalized in (path.stem, scenario_name):
            return path

    raise ValueError(f"unknown scenario: {selector}")


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


def markdown_text(value: Any) -> str:
    return " ".join(str(value).split())


def registered_rule_text() -> str:
    return ", ".join(rule.rule_id for rule in RULE_REGISTRY)


def write_validation_log(
    scenario: dict[str, Any],
    step_results: list[StepResult],
    overall_outcome: str,
) -> Path:
    scenario_name = str(scenario.get("name", "unnamed"))
    description = markdown_text(scenario.get("description", ""))
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{safe_filename(scenario_name)}_validation_log.md"

    lines = [
        f"# Validation Log: {scenario_name}",
        "",
        f"- Scenario name: {scenario_name}",
        f"- Description: {description}",
        f"- Registered rules: {registered_rule_text()}",
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
    print(f"REGISTERED_RULES {registered_rule_text()}")
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
        print(f"usage: {argv[0]} <scenario.json|scenario-name|alias|number|--list>", file=sys.stderr)
        return 2

    if argv[1] == "--list":
        print_scenario_list()
        return 0

    try:
        scenario_path = resolve_scenario_path(argv[1])
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    scenario = load_scenario(scenario_path)
    return 0 if run_scenario(scenario) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
