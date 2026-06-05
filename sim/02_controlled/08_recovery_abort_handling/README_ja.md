# PSC Recovery Return Abort Handling シナリオ

## 目的

このディレクトリには、以下の draft に対する実験的な検証シナリオが含まれます。

```text
docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_en.md
docs/specification/draft/models/psc_recovery_return_abort_handling_v0.1_ja.md
```

これらのシナリオは、`RULE-23_RETURN_RAMP_ABORT` が現在の Return Ramp 試行を中断し、
その後 Traffic Stabilization Phase と Resolver の再評価へ進むことを検証します。
条件が emergency cut ケースでない限り、即時の traffic cut はデフォルト動作ではありません。

## スコープ

これらのシナリオは軽量な検証アセットです。既存の recovery return simulation は変更しません。
また、experimental validation scenario として validator に接続され、PSC Evidence Matrix でも追跡されています。

## 構成

```text
sim/02_controlled/08_recovery_abort_handling/
  README.md
  soft_abort_hold_and_reobserve.py
  hard_abort_ramp_down.py
  emergency_cut_no_fallback.py
  two_path_degraded_abort.py
  logs/
    raw/
      soft_abort_hold_and_reobserve_run.txt
      hard_abort_ramp_down_run.txt
      emergency_cut_no_fallback_run.txt
      two_path_degraded_abort_run.txt
    verified/
      recovery_abort_stabilization_validation_log.md
```

## シナリオ: soft_abort_hold_and_reobserve

初期 allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active

観測された条件:

- telemetry conflict
- confidence reduction
- evidence は疑わしいが、決定的に unsafe ではない

期待される挙動:

- `RULE-23_RETURN_RAMP_ABORT` を発行する
- Traffic Stabilization Phase に入る
- 以降の ramp advancement を停止する
- 現在の allocation を一時的に維持する
- observation escalation を要求する
- Resolver の再評価をトリガーする

期待カテゴリ:

```text
abort_and_stabilize
```

実行:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py
```

raw log の再生成:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/soft_abort_hold_and_reobserve_run.txt
```

## シナリオ: hard_abort_ramp_down

初期 allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active

観測された条件:

- 明確な path instability
- link quality collapse
- evidence は決定的に unsafe
- forwarding はまだ可能

期待される挙動:

- `RULE-23_RETURN_RAMP_ABORT` を発行する
- Traffic Stabilization Phase に入る
- 以降の Return Ramp Advance を停止する
- 疑わしい recovered Path A を ramp down する
- traffic を既知の stable Path B へ寄せる
- Resolver の再評価をトリガーする
- traffic reduction が必要になる可能性を source-side PSC に通知する

期待カテゴリ:

```text
hard_abort_ramp_down
```

実行:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py
```

raw log の再生成:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/hard_abort_ramp_down_run.txt
```

## シナリオ: emergency_cut_no_fallback

初期 allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active

観測された条件:

- Path A link down / optical failure
- Path A での forwarding は不可能
- evidence は決定的に unsafe
- emergency condition が確認済み
- Path B は存在し、failed ではない
- Path B には Path A traffic を吸収する capacity margin がない

Fallback failure class:

```text
NO_CAPACITY_MARGIN
```

期待される挙動:

- `RULE-23_RETURN_RAMP_ABORT` を発行する
- `EMERGENCY_CUT` を実行する
- recovered Path A を即時に除外する
- recovered Path A の weight を 0 に設定する
- Path A traffic を Path B へ盲目的に転送しない
- `fallback_transfer_allowed=false` を設定する
- `fallback_block_reason=NO_CAPACITY_MARGIN` を発行する
- emergency throttling または stop のため source-side PSC に通知する
- Resolver emergency notification をトリガーする
- 通常の soft/hard Traffic Stabilization Phase をスキップする

期待カテゴリ:

```text
emergency_cut_no_fallback
```

実行:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py
```

raw log の再生成:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/emergency_cut_no_fallback_run.txt
```

## シナリオ: two_path_degraded_abort

初期 allocation:

- Recovered Path A: 25%
- Stable Path B: 75%
- Return Ramp: active
- Candidate paths: 2
- Third path: none

観測された条件:

- Return Ramp 中に Path A が unstable
- Path B も degradation を示している
- third path は存在しない
- どちらの path も完全には safe ではない
- forwarding はまだ可能
- 条件は EMERGENCY_CUT ではない

Fallback failure class:

```text
NO_SAFE_ALTERNATE
```

期待される挙動:

- `RULE-23_RETURN_RAMP_ABORT` を発行する
- Traffic Stabilization Phase に入る
- 以降の Return Ramp Advance を停止する
- 全 traffic を Path B へ盲目的に移さない
- `fallback_transfer_allowed=false` を設定する
- `fallback_block_reason=NO_SAFE_ALTERNATE` を発行する
- Resolver arbitration をトリガーする
- least-bad allocation を選択する
- policy が許可する場合、限定的な forwarding を維持する
- source-side traffic reduction を要求する

期待カテゴリ:

```text
two_path_degraded_arbitration
```

実行:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py
```

raw log の再生成:

```bash
python3 sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py > sim/02_controlled/08_recovery_abort_handling/logs/raw/two_path_degraded_abort_run.txt
```

## Abort Handling Levels

```text
SOFT_ABORT
-> Hold and Re-observe

HARD_ABORT
-> Ramp Down Suspect Path

EMERGENCY_CUT_NO_FALLBACK
-> Immediate Path Exclusion + Source-Side Emergency Traffic Control

TWO_PATH_DEGRADED_ABORT
-> Resolver Arbitration + Least-Bad Allocation
```
