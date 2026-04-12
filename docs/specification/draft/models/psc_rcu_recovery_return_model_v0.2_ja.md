# PSC RCU Recovery Return Model v0.2

## 1. ドキュメント情報

- ドキュメント名 : PSC RCU Recovery Return Model
- バージョン : v0.2
- プロジェクト : PSC / Photon System Controller
- レイヤ : PSC Control Plane / RCU
- ドキュメント種別 : Model Specification
- ステータス : Draft
- 作成者 : T. Hirose
- 言語 : Japanese

---

## 2. 目的

本ドキュメントは、PSC RCU における段階的な Recovery Return 挙動を定義する。

PSC RCU Decision Model v0.1 では conservative recovery hold を定義した。
本モデルはその上位拡張として、
回復した経路を制御付きで再参加させる staged re-entry を導入する。

目的は性能回復の即時追従ではない。
安定性を維持しつつ、説明可能な形で recovered path を再評価・再参加させることである。

---

## 3. v0.1との関係

### 3.1 v0.1の挙動

v0.1 では、一度 degraded になった経路が後に回復し、
再び best-performing path になったとしても、
現在の selected path が安定かつ信頼可能であれば即座には戻らない。

### 3.2 v0.2の拡張

v0.2 は v0.1 の保守的設計を維持したまま、
回復経路に対する staged re-entry を追加する。

Recovered path は即復帰対象ではない。
まず validation を通過し、復帰資格を得た後にのみ再選択対象となる。

---

## 4. 設計原則

### 4.1 Stability First

Recovery return は failover 後に得られた安定性を壊してはならない。

### 4.2 Recovered Path ≠ Immediate Switch Target

回復経路は即切替対象ではなく、まず候補として扱う。

### 4.3 Explainable Decision Process

すべての recovery return 判断は、
明示的な状態遷移とルールによって説明可能でなければならない。

### 4.4 役割分離

- Routing Table : 経路状態・候補情報の保持
- Telemetry : confidence / freshness を伴う観測証拠の提供
- RCU : 段階評価と return eligibility 判定
- Resolver : 曖昧性が残った場合の最終裁定

---

## 5. Recovery Return 状態モデル

以下の論理状態を追加する。

- RECOVERY_CANDIDATE
- VALIDATING
- RETURN_ELIGIBLE

これらは RCU の判断過程における制御状態である。

### 5.1 RECOVERY_CANDIDATE

以前 degraded / failed / excluded であった経路が、
最低限の再評価条件を満たした状態。

### 5.2 VALIDATING

回復経路を一定期間観察している状態。

### 5.3 RETURN_ELIGIBLE

validation を通過し、
再選択候補として扱ってよい状態。

重要：

RETURN_ELIGIBLE は即復帰を意味しない。

---

## 6. RECOVERY_CANDIDATE への遷移条件

以下を満たす場合、経路は RECOVERY_CANDIDATE に入ることができる。

- 以前 degraded / failed / limited / excluded であった
- trust が最低閾値以上
- health が有効
- telemetry freshness が許容範囲内
- confidence が最低許容値を下回っていない

---

## 7. Validation 条件

RECOVERY_CANDIDATE に入った経路は VALIDATING 状態で一定 window 観察される。

Validation では以下を確認する。

- trust が継続して閾値以上
- stability が継続して閾値以上
- health が継続して有効
- 急激な再変動が発生していない
- telemetry confidence が維持されている
- policy 上の再参加禁止が存在しない

Validation に失敗した場合、
経路は RECOVERY_CANDIDATE に戻るか、引き続き除外される。

---

## 8. Return Eligibility

validation window を正常に完了した場合のみ、
経路は RETURN_ELIGIBLE となる。

Return eligibility の意味は以下である。

- RCU による再検討対象になる
- 現 selected path と再比較可能になる
- 曖昧な場合は Resolver へ渡せる

Return eligibility は selection を強制しない。

---

## 9. Return Decision Policy

### 9.1 基本原則

現在の selected path が安定かつ信頼可能である限り、
PSC は安易に切り戻さない。

### 9.2 Controlled Return

RETURN_ELIGIBLE の経路は、以下を満たす場合のみ選択可能とする。

- score improvement が十分意味を持つ
- return hysteresis 条件を満たす
- stability risk が許容範囲内
- policy 制約が再参加を許可する

### 9.3 曖昧ケース

回復経路が eligible であっても判断が曖昧な場合、
Resolver へエスカレーションできる。

Resolver は validation 自体を担当しない。
validation 完了後の最終裁定のみを担当する。

---

## 10. Telemetry 要件

Recovery return は Telemetry を証拠として扱う。

特に重要なのは以下である。

- confidence
- freshness
- stability 関連 variance
- trend
- source reliability

古いデータや低 confidence のデータに基づいて、
積極的な return を行ってはならない。

---

## 11. Routing Table との関係

Routing Table は以下を保持しうる。

- current selected path
- best path
- fallback path
- path_state = RECOVERY
- trust / policy requirement

RCU はこれらを参照するが、
recovery return の判断ロジック自体は decision layer に属する。

---

## 12. ルール（概念）

- RULE-15_RECOVERY_CANDIDATE
- RULE-16_RECOVERY_VALIDATION_START
- RULE-17_RECOVERY_VALIDATION_PASS
- RULE-18_RETURN_ELIGIBLE
- RULE-19_RETURN_SWITCH
- RULE-20_RETURN_KEEP
- RULE-21_RETURN_ESCALATE

ルール名は仮であり、実装時に調整可能とする。

---

## 13. スコープ外

本モデルではまだ以下を定義しない。

- weighted traffic redistribution
- probabilistic return
- multi-path partial share re-entry
- 完全な recovery confidence scoring model

これらは v0.2 最小スコープを超える将来拡張とする。

---

## 14. Summary

PSC RCU Recovery Return Model v0.2 は、
v0.1 の conservative recovery hold を拡張し、
回復経路に対する staged re-entry を導入する。

Recovered path は、
まず候補化され、
次に validation され、
その後にのみ controlled eligibility を得て再選択対象となる。

これにより PSC の stability-first 設計を維持しつつ、
将来の recovery-aware / multi-path-capable 制御への道を開く。
