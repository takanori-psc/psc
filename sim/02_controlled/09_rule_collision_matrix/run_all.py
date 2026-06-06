#!/usr/bin/env python3
"""Run every PSC rule collision scenario."""

from __future__ import annotations

from run_scenario import list_scenario_files, load_scenario, run_scenario


def main() -> int:
    all_passed = True
    scenario_files = list_scenario_files()

    for index, scenario_path in enumerate(scenario_files):
        if index:
            print()
        print(f"RUNNING {scenario_path}")
        scenario = load_scenario(scenario_path)
        all_passed = run_scenario(scenario) and all_passed

    print()
    print(f"ALL_SCENARIOS {'PASS' if all_passed else 'FAIL'}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
