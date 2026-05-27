#!/usr/bin/env python3
"""Validate representative Evidence Matrix RULEs against simulation output."""

from __future__ import annotations

import subprocess
import sys
import contextlib
import importlib.util
import io
from dataclasses import dataclass
from pathlib import Path


sys.dont_write_bytecode = True
REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ScenarioCheck:
    name: str
    command: tuple[str, ...]
    expected_rules: tuple[str, ...]
    variant: str = "subprocess"


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
        variant="recovery_return_v02_ab",
    ),
)


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


def run_check(check: ScenarioCheck) -> tuple[bool, str]:
    cmd = (sys.executable, *check.command)
    if check.variant == "recovery_return_v02_ab":
        returncode, stdout, stderr = run_recovery_return_v02_ab(check)
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

    lines = [f"[{check.name}] command={' '.join(cmd)}"]
    if check.variant != "subprocess":
        lines.append(f"  variant={check.variant}")
    if returncode != 0:
        lines.append(f"  FAIL: process exited with code {returncode}")
    if missing:
        lines.append(f"  FAIL: missing rules: {', '.join(missing)}")
    if returncode == 0 and not missing:
        lines.append(f"  PASS: found {len(check.expected_rules)} expected rules")

    if returncode != 0 or missing:
        tail = "\n".join(output.splitlines()[-25:])
        if tail:
            lines.append("  Output tail:")
            lines.extend(f"    {line}" for line in tail.splitlines())

    return returncode == 0 and not missing, "\n".join(lines)


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
