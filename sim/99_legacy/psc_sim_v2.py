import csv
import os
from dataclasses import dataclass
from enum import Enum


# =============================
#  State Definition
# =============================

class State(str, Enum):
    CALM = "CALM"
    WARM = "WARM"
    HOT = "HOT"
    EMERGENCY = "EMERGENCY"


# =============================
#  Thresholds
# =============================

@dataclass
class Thresholds:
    E_light: float = 0.20
    E_heavy: float = 0.35
    Q_light: float = 0.70
    Q_heavy: float = 0.90
    L_light: float = 0.85
    L_heavy: float = 0.70

    # critical
    E_critical: float = 0.60
    Q_critical: float = 0.98
    L_critical: float = 0.55


# =============================
#  Timers
# =============================

@dataclass
class Timers:
    T_hot_down_s: float = 5.0
    T_warm_down_s: float = 15.0
    cooldown_s: float = 3.0


# =============================
#  State Update Logic
# =============================

def update_state(state, E, Q, L, time_in_state, th, tm):

    # ---- EMERGENCY 最優先 ----
    if (
        E > th.E_critical or
        Q > th.Q_critical or
        L < th.L_critical
    ):
        return State.EMERGENCY

    # ---- 状態別処理 ----

    if state == State.EMERGENCY:
        if (
            E < th.E_heavy and
            Q < th.Q_heavy and
            L > th.L_heavy and
            time_in_state > tm.cooldown_s
        ):
            return State.HOT
        return State.EMERGENCY

    if state == State.HOT:
        if (
            E < th.E_light and
            Q < th.Q_light and
            L > th.L_light and
            time_in_state > tm.T_hot_down_s
        ):
            return State.WARM
        return State.HOT

    if state == State.WARM:
        if (
            E > th.E_heavy or
            Q > th.Q_heavy or
            L < th.L_heavy
        ):
            return State.HOT

        if (
            E < th.E_light and
            Q < th.Q_light and
            L > th.L_light and
            time_in_state > tm.T_warm_down_s
        ):
            return State.CALM

        return State.WARM

    # CALM
    if (
        E > th.E_light or
        Q > th.Q_light or
        L < th.L_light
    ):
        return State.WARM

    return State.CALM


# =============================
#  Simple Simulation
# =============================

def run_simulation():

    th = Thresholds()
    tm = Timers()

    state = State.CALM
    time_in_state = 0.0
    dt = 1.0

    log_filename = "psc_sim_log_v2.csv"

    with open(log_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "E", "Q", "L", "state"])

        for t in range(120):

            # ---- ダミー負荷パターン ----
            if 20 < t < 40:
                E = 0.4
                Q = 0.8
                L = 0.75
            elif 60 < t < 70:
                E = 0.65
                Q = 0.99
                L = 0.5
            else:
                E = 0.1
                Q = 0.5
                L = 0.95

            next_state = update_state(
                state, E, Q, L, time_in_state, th, tm
            )

            if next_state == state:
                time_in_state += dt
            else:
                print(f"[{t}s] {state.value} -> {next_state.value}")
                state = next_state
                time_in_state = 0.0

            writer.writerow([t, E, Q, L, state.value])

    print("Simulation complete.")
    print(f"Log saved to {log_filename}")


if __name__ == "__main__":
    run_simulation()
