#!/usr/bin/env python3
"""Validate representative Evidence Matrix RULEs against simulation output."""

from __future__ import annotations

import subprocess
import sys
import contextlib
import importlib.util
import io
import re
from dataclasses import dataclass
from pathlib import Path


sys.dont_write_bytecode = True
REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ScenarioCheck:
    name: str
    command: tuple[str, ...]
    expected_rules: tuple[str, ...]
    expected_category: str | None = None
    expected_reason: str | None = None
    expected_observation_mode: str | None = None
    expected_state_transition: str | None = None
    variant: str = "subprocess"
    forbidden_rules: tuple[str, ...] = ()
    forbidden_scope_pattern: str | None = None
    forbidden_patterns: tuple[str, ...] = ()
    required_patterns: tuple[str, ...] = ()
    weight_unchanged_check: bool = False
    previous_step_required_patterns: tuple[str, ...] = ()


SCENARIOS = (
    ScenarioCheck(
        name="switch_score",
        command=(
            "sim/02_controlled/02_rcu_decision_v01/"
            "mini_psc_rcu_decision_v01_switch_score.py",
        ),
        expected_rules=(
            "RULE-01_KEEP_score",
            "RULE-02_SWITCH_score",
        ),
        expected_category="switch",
    ),
    ScenarioCheck(
        name="resolver_switch",
        command=(
            "sim/02_controlled/02_rcu_decision_v01/"
            "mini_psc_rcu_decision_v01.py",
        ),
        expected_rules=(
            "RULE-05_ESCALATE_conflict",
            "RULE-14_RESOLVER_switch",
            "RULE-12_COOLDOWN_active",
        ),
        expected_category="escalation_and_cooldown",
    ),
    ScenarioCheck(
        name="recovery_return_v02",
        command=(
            "sim/02_controlled/06_recovery_return_v02/"
            "mini_psc_rcu_decision_v02_recovery.py",
        ),
        expected_rules=(
            "RULE-15_RECOVERY_CANDIDATE",
            "RULE-16_RECOVERY_VALIDATION_START",
            "RULE-18_RETURN_ELIGIBLE",
            "RULE-19_RETURN_SWITCH",
        ),
        expected_category="switch",
        variant="recovery_return_v02_ab",
    ),
    ScenarioCheck(
        name="light_false_negative",
        command=(
            "sim/02_controlled/07_light_observation_stub/"
            "light_false_negative.py",
        ),
        expected_rules=("RULE-22_RETURN_RAMP_HOLD",),
        expected_category="hold",
    ),
    ScenarioCheck(
        name="light_stale_telemetry",
        command=(
            "sim/02_controlled/07_light_observation_stub/"
            "light_stale_telemetry.py",
        ),
        expected_rules=("RULE-22_RETURN_RAMP_HOLD",),
        expected_category="hold",
    ),
    ScenarioCheck(
        name="light_masked_instability",
        command=(
            "sim/02_controlled/07_light_observation_stub/"
            "light_masked_instability.py",
        ),
        expected_rules=("RULE-22_RETURN_RAMP_HOLD",),
        expected_category="hold",
    ),
    ScenarioCheck(
        name="ramp_hold_insufficient_observation",
        command=(
            "sim/02_controlled/06_recovery_return_v02/"
            "mini_psc_rcu_decision_v03_recovery_ramp_observation.py",
        ),
        expected_rules=("RULE-22_RETURN_RAMP_HOLD",),
        expected_category="hold",
        expected_reason="INSUFFICIENT_OBSERVATION",
        expected_observation_mode="FULL",
        expected_state_transition="RAMPING->RAMPING",
        variant="ramp_hold_insufficient_observation",
        forbidden_rules=(
            "RULE-21_RETURN_RAMP_ADVANCE",
            "RULE-23_RETURN_RAMP_ABORT",
            "RULE-24_RETURN_RAMP_COMPLETE",
        ),
        forbidden_scope_pattern="observation_category=INSUFFICIENT_OBSERVATION",
        forbidden_patterns=(
            "state_transition=RAMPING->ABORTED",
            "state_transition=RAMPING->COMPLETE",
            "state_transition=RAMPING->EMERGENCY",
            "mode=EMERGENCY",
            "EMERGENCY_CUT",
        ),
        required_patterns=(
            "scenario=ramp_hold_insufficient_observation",
            "recovery_state=RAMPING",
            "category=hold",
            "state_transition=RAMPING->RAMPING",
            "observation_mode=FULL",
            "observation_category=INSUFFICIENT_OBSERVATION",
            "observation_samples=0",
            "required_observation_samples=1",
            "observation_window_steps=0",
            "required_observation_window_steps=1",
            "reason=INSUFFICIENT_OBSERVATION",
            "recovered_weight_before=0.30",
            "recovered_weight_after=0.30",
            "ramp_level_before=0.30",
            "ramp_level_after=0.30",
        ),
        previous_step_required_patterns=(
            "RULE-21_RETURN_RAMP_ADVANCE",
            "category=switch",
            "observation_mode=FULL",
            "observation_category=SUFFICIENT_OBSERVATION",
            "recovered_weight_before=0.10",
            "recovered_weight_after=0.30",
            "ramp_level_before=0.10",
            "ramp_level_after=0.30",
            "reason=RECOVERED_PATH_STABLE",
        ),
        weight_unchanged_check=True,
    ),
    ScenarioCheck(
        name="soft_abort_hold_and_reobserve",
        command=(
            "sim/02_controlled/08_recovery_abort_handling/"
            "soft_abort_hold_and_reobserve.py",
        ),
        expected_rules=("RULE-23_RETURN_RAMP_ABORT",),
        expected_category="abort_and_stabilize",
    ),
    ScenarioCheck(
        name="hard_abort_ramp_down",
        command=(
            "sim/02_controlled/08_recovery_abort_handling/"
            "hard_abort_ramp_down.py",
        ),
        expected_rules=("RULE-23_RETURN_RAMP_ABORT",),
        expected_category="hard_abort_ramp_down",
    ),
    ScenarioCheck(
        name="emergency_cut_no_fallback",
        command=(
            "sim/02_controlled/08_recovery_abort_handling/"
            "emergency_cut_no_fallback.py",
        ),
        expected_rules=("RULE-23_RETURN_RAMP_ABORT",),
        expected_category="emergency_cut_no_fallback",
    ),
    ScenarioCheck(
        name="two_path_degraded_abort",
        command=(
            "sim/02_controlled/08_recovery_abort_handling/"
            "two_path_degraded_abort.py",
        ),
        expected_rules=("RULE-23_RETURN_RAMP_ABORT",),
        expected_category="two_path_degraded_arbitration",
    ),
)

CATEGORY_RULES = {
    "switch": (
        "RULE-02_SWITCH_score",
        "RULE-14_RESOLVER_switch",
        "RULE-19_RETURN_SWITCH",
        "RULE-21_RETURN_RAMP_ADVANCE",
        "RULE-24_RETURN_RAMP_COMPLETE",
    ),
    "hold": (
        "RULE-01_KEEP_score",
        "RULE-08_DEGRADE_keep",
        "RULE-11_RECOVERY_cooldown",
        "RULE-20_RETURN_KEEP",
        "RULE-22_RETURN_RAMP_HOLD",
    ),
    "abort": (
        "RULE-23_RETURN_RAMP_ABORT",
    ),
    "escalation": (
        "RULE-05_ESCALATE_conflict",
    ),
    "fallback": (
        "RULE-07_DEGRADE_trigger",
        "RULE-09_DEGRADE_switch",
    ),
}

CATEGORY_RULE_COMBINATIONS = {
    "escalation_and_cooldown": (
        "RULE-05_ESCALATE_conflict",
        "RULE-12_COOLDOWN_active",
    ),
}

CATEGORY_ALIASES = {
    "hold_or_escalate": (
        "hold",
        "escalation",
    ),
}


def observed_categories(output: str) -> set[str]:
    categories = {
        category
        for category, rules in CATEGORY_RULES.items()
        if any(rule in output for rule in rules)
    }
    categories.update(re.findall(r"\bcategory=([A-Za-z0-9_]+)", output))

    for category, required_rules in CATEGORY_RULE_COMBINATIONS.items():
        if all(rule in output for rule in required_rules):
            categories.add(category)

    for category, accepted_categories in CATEGORY_ALIASES.items():
        if any(accepted in categories for accepted in accepted_categories):
            categories.add(category)

    return categories


def category_satisfied(expected_category: str | None, output: str) -> bool:
    if expected_category is None:
        return True
    return expected_category in observed_categories(output)


def run_recovery_return_v02_ab(check: ScenarioCheck) -> tuple[int, str, str]:
    """Run the v0.2 recovery-return behavior without the later multi-candidate C path."""
    module_path = REPO_ROOT / check.command[0]
    spec = importlib.util.spec_from_file_location("psc_recovery_return_v02_check", module_path)
    if spec is None or spec.loader is None:
        return 1, "", f"failed to load module: {module_path}"

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    original_create_paths = module.create_paths

    def create_paths_without_c(step: int):
        return [path for path in original_create_paths(step) if path.get("name") != "C"]

    module.create_paths = create_paths_without_c

    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        module.run()

    return 0, stdout.getvalue(), stderr.getvalue()


def run_recovery_ramp_scenario(check: ScenarioCheck) -> tuple[int, str, str]:
    """Run one v0.3 recovery-ramp scenario so forbidden-rule checks stay scoped."""
    module_path = REPO_ROOT / check.command[0]
    spec = importlib.util.spec_from_file_location("psc_recovery_ramp_check", module_path)
    if spec is None or spec.loader is None:
        return 1, "", f"failed to load module: {module_path}"

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        module.run_scenario(check.variant, 11, "FULL")

    return 0, stdout.getvalue(), stderr.getvalue()


def step_block_containing(output: str, pattern: str) -> str:
    marker = output.find(pattern)
    if marker == -1:
        return ""

    start = output.rfind("\n=== STEP ", 0, marker)
    if start == -1:
        start = 0
    else:
        start += 1

    end = output.find("\n=== STEP ", marker)
    if end == -1:
        end = len(output)

    return output[start:end]


def previous_step_block(output: str, pattern: str) -> str:
    marker = output.find(pattern)
    if marker == -1:
        return ""

    current_start = output.rfind("\n=== STEP ", 0, marker)
    if current_start == -1:
        return ""

    previous_start = output.rfind("\n=== STEP ", 0, current_start)
    if previous_start == -1:
        return ""
    previous_start += 1

    return output[previous_start:current_start]


def weights_unchanged(output: str) -> bool:
    matches = re.findall(
        r"\brecovered_weight_before=([0-9.]+)\b.*\brecovered_weight_after=([0-9.]+)\b",
        output,
    )
    return bool(matches) and all(before == after for before, after in matches)


def run_check(check: ScenarioCheck) -> tuple[bool, str]:
    cmd = (sys.executable, *check.command)
    if check.variant == "recovery_return_v02_ab":
        returncode, stdout, stderr = run_recovery_return_v02_ab(check)
    elif check.variant == "ramp_hold_insufficient_observation":
        returncode, stdout, stderr = run_recovery_ramp_scenario(check)
    else:
        result = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        returncode = result.returncode
        stdout = result.stdout
        stderr = result.stderr

    output = stdout + stderr
    missing = [rule for rule in check.expected_rules if rule not in output]
    forbidden_output = output
    if check.forbidden_scope_pattern is not None:
        forbidden_output = step_block_containing(output, check.forbidden_scope_pattern)
    forbidden_present = [
        rule for rule in check.forbidden_rules if rule in forbidden_output
    ]
    forbidden_patterns_present = [
        pattern for pattern in check.forbidden_patterns if pattern in forbidden_output
    ]
    missing_patterns = [
        pattern for pattern in check.required_patterns if pattern not in output
    ]
    previous_output = output
    if check.forbidden_scope_pattern is not None:
        previous_output = previous_step_block(output, check.forbidden_scope_pattern)
    missing_previous_patterns = [
        pattern
        for pattern in check.previous_step_required_patterns
        if pattern not in previous_output
    ]
    expected_reason_ok = (
        check.expected_reason is None
        or f"reason={check.expected_reason}" in forbidden_output
    )
    observation_mode_ok = (
        check.expected_observation_mode is None
        or f"observation_mode={check.expected_observation_mode}" in forbidden_output
    )
    state_transition_ok = (
        check.expected_state_transition is None
        or f"state_transition={check.expected_state_transition}" in forbidden_output
    )
    weight_scope = forbidden_output if check.forbidden_scope_pattern else output
    weight_ok = not check.weight_unchanged_check or weights_unchanged(weight_scope)
    category_ok = category_satisfied(check.expected_category, output)
    categories = observed_categories(output)

    lines = [f"[{check.name}] command={' '.join(cmd)}"]
    if check.variant != "subprocess":
        lines.append(f"  variant={check.variant}")
    if check.expected_category is not None:
        observed = ", ".join(sorted(categories)) if categories else "none"
        lines.append(
            f"  category expected={check.expected_category} observed={observed}"
        )
    if returncode != 0:
        lines.append(f"  FAIL: process exited with code {returncode}")
    if missing:
        lines.append(f"  FAIL: missing rules: {', '.join(missing)}")
    if forbidden_present:
        lines.append(f"  FAIL: forbidden rules present: {', '.join(forbidden_present)}")
    if forbidden_patterns_present:
        lines.append(
            f"  FAIL: forbidden patterns present: {', '.join(forbidden_patterns_present)}"
        )
    if missing_patterns:
        lines.append(f"  FAIL: missing patterns: {', '.join(missing_patterns)}")
    if missing_previous_patterns:
        lines.append(
            "  FAIL: previous step missing patterns: "
            + ", ".join(missing_previous_patterns)
        )
    if not weight_ok:
        lines.append("  FAIL: recovered weight changed or was not logged")
    if not expected_reason_ok:
        lines.append(f"  FAIL: expected reason not found: {check.expected_reason}")
    if not observation_mode_ok:
        lines.append(
            f"  FAIL: expected observation mode not found: {check.expected_observation_mode}"
        )
    if not state_transition_ok:
        lines.append(
            f"  FAIL: expected state transition not found: {check.expected_state_transition}"
        )
    if not category_ok:
        lines.append(f"  FAIL: expected category not satisfied: {check.expected_category}")
    if (
        returncode == 0
        and not missing
        and not forbidden_present
        and not forbidden_patterns_present
        and not missing_patterns
        and not missing_previous_patterns
        and weight_ok
        and expected_reason_ok
        and observation_mode_ok
        and state_transition_ok
        and category_ok
    ):
        lines.append(f"  PASS: found {len(check.expected_rules)} expected rules")

    if (
        returncode != 0
        or missing
        or forbidden_present
        or forbidden_patterns_present
        or missing_patterns
        or missing_previous_patterns
        or not weight_ok
        or not expected_reason_ok
        or not observation_mode_ok
        or not state_transition_ok
        or not category_ok
    ):
        tail = "\n".join(output.splitlines()[-25:])
        if tail:
            lines.append("  Output tail:")
            lines.extend(f"    {line}" for line in tail.splitlines())

    return (
        returncode == 0
        and not missing
        and not forbidden_present
        and not forbidden_patterns_present
        and not missing_patterns
        and not missing_previous_patterns
        and weight_ok
        and expected_reason_ok
        and observation_mode_ok
        and state_transition_ok
        and category_ok
    ), "\n".join(lines)


def main() -> int:
    failed = False

    for check in SCENARIOS:
        ok, report = run_check(check)
        print(report)
        if not ok:
            failed = True

    if failed:
        print("\nEvidence RULE validation failed.")
        return 1

    print("\nEvidence RULE validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
