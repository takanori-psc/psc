# PSC Recovery Return 拡張モデル v0.2.x（日本語版）

---

## ■ コア原則

```text
RETURN_ELIGIBLE ≠ RETURN_SWITCH
RETURN_SWITCH ≠ FINAL_DECISION
```

---

## ■ 解釈

- `RETURN_ELIGIBLE` は「復帰候補が検証を通過した状態」を意味する
- これは即時の経路切り替えを保証しない
- 復帰候補は baseline（final_score）と競合する可能性がある
- 競合が発生した場合、最終判断は Resolver に委ねられる
- Resolverは「RCUが決定できない場合」だけでなく、
  「RCUの決定が曖昧または競合している場合」にも介入する

---

## ■ Recovery フロー

```text
RCU
→ return_score による候補生成
→ validation（検証）
→ RETURN_ELIGIBLE
→ 曖昧性チェック（score差・trust差・stability差）
→ Resolver による仲裁（必要な場合）
→ 最終決定（switch / keep）
→ 安定化（cooldown / hysteresis）
```

---

## ■ 検証済み挙動

### ● 単一候補ケース（Single-candidate）

- `return_score` が B を選択
- 競合が発生しないため、そのまま復帰

---

### ● 複数候補ケース（Multi-candidate）

- `return_score` が C を選択（安定性優先）
- `final_score` は B を選好（性能優先）
- Resolver が競合を解決し、C を選択

---

## ■ 設計上の意味

- `return_score` は「復帰専用の候補選択ロジック」
- `final_score` は「通常時の経路評価ロジック」
- Resolver は「競合時の仲裁レイヤ」であり、デフォルト選択器ではない

---

## ■ 設計の本質

```text
復帰判定と最終決定は分離されている
```

- 「戻れる」ことと「戻す」ことは別
- PSCは即時最適化ではなく安定性を優先する

---

## ■ 状態

- v0.2 Recovery Return：検証済み
- multi-candidate 拡張：検証済み
- Resolver 連携：検証済み

---

## ■ 参照

- 検証ログ：

  - logs/rcu_decision_v02_multi_candidate_validation_log.md
- 生ログ：

  - logs/raw/multi_candidate_run.txt

---

## ■ 次のステップ

- v0.2.x Recovery 拡張モデルとして正式仕様化
- Resolver の評価ルール詳細化（trust / stability / score差）
