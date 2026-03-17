import csv
import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

class State(str, Enum):
    CALM = "CALM"
    WARM = "WARM"
    HOT  = "HOT"
    E1   = "E1"   # EMERGENCY entry (止血)
    E2   = "E2"   # EMERGENCY sustained (封じ込め)
    
@dataclass
class Thresholds:
    E_light: float = 0.20
    E_heavy: float = 0.35
    Q_light: float = 0.70
    Q_heavy: float = 0.90
    L_light: float = 0.85
    L_heavy: float = 0.70

    # critical (EMERGENCY)
    E_critical: float = 0.60
    Q_critical: float = 0.98
    L_critical: float = 0.55

@dataclass
class Timers:
    cooldown_s: float = 2.0
    T_warm_max_s: float = 10.0
    T_hot_down_s: float = 5.0
    T_warm_down_s: float = 15.0

    # EMERGENCY (2-stage)
    T_emerg_cap_s: float = 3.0     # ✅ E1 -> E2
    T_emerg_clear_s: float = 10.0  # E2 -> HOT 解除確認（仮）

def reset_state_timers():
    return 0.0, 0.0  # stable_time, warm_duration

TOKEN_TOTAL = {
    State.CALM: 100,
    State.WARM: 80,
    State.HOT:  60,
    State.E1:   30,
    State.E2:   20,
}

TOKEN_SPLIT = {
    State.CALM: {"CRIT": 20, "LAT": 30, "BULK": 50},
    State.WARM: {"CRIT": 25, "LAT": 35, "BULK": 40},
    State.HOT:  {"CRIT": 35, "LAT": 40, "BULK": 25},
    State.E1:   {"CRIT": 70, "LAT": 25, "BULK": 5},
    State.E2:   {"CRIT": 85, "LAT": 15, "BULK": 0},
}

CAP_RATE = {
    State.CALM: 1.00,
    State.WARM: 1.00,
    State.HOT:  1.00,
    State.E1:   0.25,  # 止血
    State.E2:   0.10,  # 封じ込め
}

def token_emit(state: State) -> dict:
    total = TOKEN_TOTAL[state]
    split = TOKEN_SPLIT[state]
    # 切り捨て→残りをCRITへ寄せる（実装が安定）
    crit = int(total * split["CRIT"] / 100)
    lat  = int(total * split["LAT"]  / 100)
    bulk = int(total * split["BULK"] / 100)
    used = crit + lat + bulk
    crit += (total - used)
    return {"token_total": total, "tok_CRIT": crit, "tok_LAT": lat, "tok_BULK": bulk}
        
@dataclass
class StepInput:
    t: float
    error: float
    queue: float
    link: float

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def reason_from_flags(e: bool, q: bool, l: bool) -> str:
    parts = []
    if e: parts.append("E")
    if q: parts.append("Q")
    if l: parts.append("L")
    return "|".join(parts) if parts else ""

def simulate(inputs: List[StepInput],
             thr: Thresholds = Thresholds(),
             tm: Timers = Timers(),
             dt: float = 1.0) -> List[dict]:

    state: State = State.CALM
    cooldown_remaining = 0.0
    warm_duration = 0.0
    stable_time = 0.0

    # E1/E2
    e1_time = 0.0
    emerg_clear_ok = 0.0

    # ✅ E1入口用：critical連続時間
    critical_hold = 0.0

    rows: List[dict] = []

    for s in inputs:
        # sanitize
        e = clamp01(s.error)
        q = clamp01(s.queue)
        lnk = clamp01(s.link)

        # triggers
        eL = e > thr.E_light
        qL = q > thr.Q_light
        lL = lnk < thr.L_light
        trigger_light = eL or qL or lL

        eH = e > thr.E_heavy
        qH = q > thr.Q_heavy
        lH = lnk < thr.L_heavy
        trigger_heavy = eH or qH or lH

        eC = e > thr.E_critical
        qC = q > thr.Q_critical
        lC = lnk < thr.L_critical
        trigger_critical = eC or qC or lC

        reason_light = reason_from_flags(eL, qL, lL)
        reason_heavy = reason_from_flags(eH, qH, lH)
        reason_critical = reason_from_flags(eC, qC, lC)

        # update cooldown
        if cooldown_remaining > 0.0:
            cooldown_remaining = max(0.0, cooldown_remaining - dt)

        # warm duration
        if state == State.WARM:
            warm_duration += dt
        else:
            warm_duration = 0.0

        # stable_time
        if state in (State.E1, State.E2):
            # EMERGENCY中の安定は "criticalが消えている"
            if not trigger_critical:
                stable_time += dt
            else:
                stable_time = 0.0
        elif state == State.HOT:
            # HOTの安定は「lightが消えた（十分落ち着いた）」で判定
            if not trigger_light:
                stable_time += dt
            else:
                stable_time = 0.0
        elif state == State.WARM:
            if not trigger_light:
                stable_time += dt
            else:
                stable_time = 0.0
        else:
            stable_time = 0.0

        transition = ""

        # --- critical hold (2s) ---
        if trigger_critical:
            critical_hold += dt
        else:
            critical_hold = 0.0

        # --- EMERGENCY entry: criticalが2秒連続ならE1（E1/E2中は除外） ---
        if (critical_hold >= 2.0) and (state not in (State.E1, State.E2)):
            state = State.E1
            cooldown_remaining = 0.0
            stable_time, warm_duration = reset_state_timers()
            e1_time = 0.0
            emerg_clear_ok = 0.0
            transition = "ANY->E1(hold2s)"

        # --- State machine ---
        if state == State.CALM:
            if trigger_light and cooldown_remaining == 0.0:
                state = State.WARM
                cooldown_remaining = tm.cooldown_s
                stable_time, warm_duration = reset_state_timers()
                transition = "CALM->WARM"

        elif state == State.WARM:
            if trigger_heavy:
                state = State.HOT
                cooldown_remaining = tm.cooldown_s
                stable_time, warm_duration = reset_state_timers()
                transition = "WARM->HOT"

            elif (not trigger_light) and (stable_time >= tm.T_warm_down_s):
                state = State.CALM
                cooldown_remaining = tm.cooldown_s
                stable_time, warm_duration = reset_state_timers()
                transition = "WARM->CALM"

        elif state == State.HOT:
            # HOT -> WARM（lightが消えて一定時間安定）
            if (not trigger_light) and (stable_time >= tm.T_hot_down_s):
                state = State.WARM
                cooldown_remaining = tm.cooldown_s
                stable_time, warm_duration = reset_state_timers()
                transition = "HOT->WARM"

        elif state == State.E1:
                    # E1 -> E2（tm.T_emerg_cap_s 秒）
                    if e1_time >= tm.T_emerg_cap_s:
                        state = State.E2
                        stable_time, warm_duration = reset_state_timers()
                        emerg_clear_ok = 0.0
                        transition = "E1->E2"
                    else:
                        e1_time += dt

        elif state == State.E2:
            # E2 -> HOT（解除条件が連続で成立）
            clear_ok = (e < 0.85 * thr.E_critical) and (q < 0.98 * thr.Q_critical) and (lnk > 1.05 * thr.L_critical)

            if clear_ok:
                emerg_clear_ok += dt
                if emerg_clear_ok >= tm.T_emerg_clear_s:
                    state = State.HOT
                    cooldown_remaining = tm.cooldown_s
                    stable_time, warm_duration = reset_state_timers()
                    e1_time = 0.0
                    emerg_clear_ok = 0.0
                    transition = "E2->HOT"
            else:
                emerg_clear_ok = 0.0

        tok = token_emit(state)

        rows.append({
            "t": s.t,
            "state": state.value,
            "error": e,
            "queue": q,
            "link": lnk,

            "trigger_light": int(trigger_light),
            "trigger_heavy": int(trigger_heavy),
            "reason_light": reason_light,
            "reason_heavy": reason_heavy,

            "trigger_critical": int(trigger_critical),
            "reason_critical": reason_critical,

            "cap_rate": CAP_RATE[state],
            **tok,

            "cooldown_remaining": round(cooldown_remaining, 3),
            "warm_duration": round(warm_duration, 3),
            "stable_time": round(stable_time, 3),

            "critical_hold": round(critical_hold, 3),
            "e1_time": round(e1_time, 3),
            "emerg_clear_ok": round(emerg_clear_ok, 3),

            "transition": transition,
        })

    return rows
        
def build_scenario(dt: float = 1.0) -> List[StepInput]:
    """
    Phase1: calm (0-19s)
    Phase2: warm trigger by queue (20-39s)
    Phase3: hot trigger by queue (40-59s)
    Phase4: recover (60-119s)
    """
    inputs: List[StepInput] = []
    t = 0.0

    def push(seconds: int, error: float, queue: float, link: float):
        nonlocal t
        steps = int(seconds / dt)
        for _ in range(steps):
            inputs.append(StepInput(t=t, error=error, queue=queue, link=link))
            t += dt

    push(20, error=0.05, queue=0.20, link=0.95)  # Phase1
    push(20, error=0.10, queue=0.75, link=0.92)  # Phase2 -> WARM

    # Phase3 分割（EMERGENCYテスト用）
    push(10, error=0.12, queue=0.95, link=0.90)  # HOT
    push(5,  error=0.12, queue=0.99, link=0.90)  # critical 5秒 （確実）
    push(6,  error=0.12, queue=0.95, link=0.90)  # HOT継続
    # heavyは消えるが light は残る（= Q=0.75）
    push(10, error=0.10, queue=0.75, link=0.90)  # MID: lightだけ残る
    push(60, error=0.05, queue=0.20, link=0.95)  # Phase4 -> down

    return inputs

def main():
    dt = 1.0
    inputs = build_scenario(dt=dt)
    rows = simulate(inputs, dt=dt)

    # --- 出力先：logs/ に集約 ---
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    base_name = "psc_sim_log"
    pattern = re.compile(rf"{base_name}_(\d+)\.csv")

    existing = []
    for fname in os.listdir(log_dir):
        m = pattern.match(fname)
        if m:
            existing.append(int(m.group(1)))

    next_index = max(existing) + 1 if existing else 1
    out_csv = os.path.join(log_dir, f"{base_name}_{next_index:03d}.csv")
    # ----------------------------

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote: {out_csv}")

if __name__ == "__main__":
    main()
