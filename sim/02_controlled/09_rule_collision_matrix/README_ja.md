# PSC ルール衝突マトリクス

## 目的

このディレクトリは、同じステップで複数の PSC ルールが発火した場合に、
どのルールが最終アクションとして採用されるかを確認するための最小
シミュレータです。

ランナーは各ステップですべての登録済みルールを評価し、発火したルールを
記録したうえで、優先度によって最終アクションを決定します。これにより、
大きな分岐の内部に隠れがちな優先度の挙動を確認できます。

## 流れ

1. JSON シナリオを読み込む。
2. 各ステップですべての登録済みルールを評価する。
3. 発火したルールは次の情報を返す。
   - `rule_id`
   - `action`
   - `priority`
   - `reason`
4. 最も高い優先度のルールを採用する。
5. 発火ルール、抑制ルール、最終アクション、期待アクション、`PASS` /
   `FAIL` を出力する。

優先度が同じ場合は、登録順で決定します。そのため出力は常に決定的です。

## 登録済みルール

- `RULE-02_SWITCH_score`
- `RULE-05_ESCALATE_conflict`
- `RULE-22_RETURN_RAMP_HOLD`
- `RULE-23_RETURN_RAMP_ABORT`
- `RULE-24_RETURN_RAMP_COMPLETE`

## シナリオ形式

YAML 依存を避けるため、シナリオは JSON を第一形式とします。

```json
{
  "name": "return_vs_abort",
  "description": "Return Ramp hold collides with an abort condition.",
  "steps": [
    {
      "step_id": 0,
      "state": {},
      "telemetry": {},
      "expected_action": "RETURN_RAMP_ABORT"
    }
  ]
}
```

## 実行

```bash
python3 sim/02_controlled/09_rule_collision_matrix/run_scenario.py \
  sim/02_controlled/09_rule_collision_matrix/scenarios/return_vs_abort.json
```

構文チェック:

```bash
python3 -m py_compile sim/02_controlled/09_rule_collision_matrix/run_scenario.py
```
