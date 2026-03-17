#!/usr/bin/env python3
import argparse
import csv
import os
from typing import Dict, List, Tuple, Optional

import matplotlib.pyplot as plt


def _find_col(cols: List[str], candidates: List[str]) -> Optional[str]:
    lower = {c.lower(): c for c in cols}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    return None


def _read_csv(path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f)
        cols = r.fieldnames or []
        rows = [row for row in r]
    return cols, rows


def _to_float(x: str) -> Optional[float]:
    try:
        if x is None:
            return None
        x = str(x).strip()
        if x == "":
            return None
        return float(x)
    except Exception:
        return None


def _extract_series(rows: List[Dict[str, str]], col: str) -> List[Optional[float]]:
    return [_to_float(r.get(col, "")) for r in rows]


def _extract_text(rows: List[Dict[str, str]], col: str) -> List[str]:
    return [str(r.get(col, "")).strip() for r in rows]


def _plot_numeric(x, y, xlabel, ylabel, title):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def _plot_state(x, states, xlabel, title):
    # map unique states to integers in order of appearance
    mapping: Dict[str, int] = {}
    y = []
    for s in states:
        if s not in mapping:
            mapping[s] = len(mapping)
        y.append(mapping[s])

    inv = {v: k for k, v in mapping.items()}

    plt.figure()
    plt.step(x, y, where="post")
    plt.xlabel(xlabel)
    plt.yticks(list(inv.keys()), [inv[i] for i in inv.keys()])
    plt.title(title)
    plt.tight_layout()
    plt.show()


def main():
    ap = argparse.ArgumentParser(description="PSC sim log plotter (robust, auto-detect columns)")
    ap.add_argument("csv_path", help="path to csv log, e.g. logs/runs/psc_sim_log_003.csv")
    ap.add_argument("--save-dir", default="", help="if set, save PNGs into this dir (also shows plots)")
    args = ap.parse_args()

    path = args.csv_path
    if not os.path.exists(path):
        raise SystemExit(f"File not found: {path}")

    cols, rows = _read_csv(path)
    if not rows:
        raise SystemExit("CSV has no data rows.")

    # detect time column
    tcol = _find_col(cols, ["t", "time", "sec", "seconds", "step", "tick"])
    if tcol is None:
        # fallback to index
        x = list(range(len(rows)))
        xlabel = "index"
    else:
        x_raw = _extract_series(rows, tcol)
        # replace None with index to keep monotonic
        x = [v if v is not None else i for i, v in enumerate(x_raw)]
        xlabel = tcol

    # columns of interest (if exist)
    state_col = _find_col(cols, ["state"])
    trust_col = _find_col(cols, ["trust"])
    qttl_col  = _find_col(cols, ["q_ttl_s", "q_ttl", "quarantine_ttl", "ttl_q"])
    strike_col = _find_col(cols, ["strike_q", "strike"])
    quiet_col = _find_col(cols, ["quiet_s", "quiet"])

    # Common telemetry candidates (your sim may or may not have them)
    # We'll plot whatever exists among these.
    telemetry_candidates = [
        ("E", ["E", "err", "error", "error_rate"]),
        ("Q", ["Q", "queue", "queue_load", "q_util"]),
        ("L", ["L", "link", "link_util", "loss", "loss_rate"]),
        ("cap_rate", ["cap_rate", "cap", "rate_cap"]),
    ]

    # reason string (optional)
    reason_col = _find_col(cols, ["guard_reason", "reason", "reason_codes", "last_reason"])

    # --- Plot state ---
    if state_col:
        states = _extract_text(rows, state_col)
        _plot_state(x, states, xlabel, f"PSC State ({os.path.basename(path)})")
        if args.save_dir:
            os.makedirs(args.save_dir, exist_ok=True)
            plt.gcf().savefig(os.path.join(args.save_dir, "state.png"), dpi=160)

    # --- Plot telemetry numeric series that exist ---
    for label, cand_cols in telemetry_candidates:
        c = _find_col(cols, cand_cols)
        if not c:
            continue
        y = _extract_series(rows, c)
        # drop None by forward fill (simple) to avoid breaks
        last = None
        yf = []
        for v in y:
            if v is None:
                yf.append(last)
            else:
                last = v
                yf.append(v)
        _plot_numeric(x, yf, xlabel, c, f"{label}: {c} ({os.path.basename(path)})")
        if args.save_dir:
            os.makedirs(args.save_dir, exist_ok=True)
            plt.gcf().savefig(os.path.join(args.save_dir, f"{label.lower()}_{c}.png"), dpi=160)

    # --- Plot guard signals if present ---
    if trust_col:
        trust = _extract_text(rows, trust_col)
        # map NORMAL/SUSPECT etc to 0/1/2...
        _plot_state(x, trust, xlabel, f"Trust ({os.path.basename(path)})")
        if args.save_dir:
            os.makedirs(args.save_dir, exist_ok=True)
            plt.gcf().savefig(os.path.join(args.save_dir, "trust.png"), dpi=160)

    if qttl_col:
        y = _extract_series(rows, qttl_col)
        last = 0.0
        yf = []
        for v in y:
            if v is None:
                yf.append(last)
            else:
                last = v
                yf.append(v)
        _plot_numeric(x, yf, xlabel, qttl_col, f"Quarantine TTL ({os.path.basename(path)})")
        if args.save_dir:
            os.makedirs(args.save_dir, exist_ok=True)
            plt.gcf().savefig(os.path.join(args.save_dir, "q_ttl.png"), dpi=160)

    if strike_col:
        y = _extract_series(rows, strike_col)
        last = 0.0
        yf = []
        for v in y:
            if v is None:
                yf.append(last)
            else:
                last = v
                yf.append(v)
        _plot_numeric(x, yf, xlabel, strike_col, f"Strike Q ({os.path.basename(path)})")
        if args.save_dir:
            os.makedirs(args.save_dir, exist_ok=True)
            plt.gcf().savefig(os.path.join(args.save_dir, "strike_q.png"), dpi=160)

    if quiet_col:
        y = _extract_series(rows, quiet_col)
        last = 0.0
        yf = []
        for v in y:
            if v is None:
                yf.append(last)
            else:
                last = v
                yf.append(v)
        _plot_numeric(x, yf, xlabel, quiet_col, f"Quiet Timer ({os.path.basename(path)})")
        if args.save_dir:
            os.makedirs(args.save_dir, exist_ok=True)
            plt.gcf().savefig(os.path.join(args.save_dir, "quiet.png"), dpi=160)

    # --- Print reason summary (optional) ---
    if reason_col:
        reasons = _extract_text(rows, reason_col)
        counts: Dict[str, int] = {}
        for r in reasons:
            if not r:
                continue
            counts[r] = counts.get(r, 0) + 1
        if counts:
            print("\n[Reason summary]")
            for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
                print(f"{v:6d}  {k}")

    print("done")


if __name__ == "__main__":
    main()
