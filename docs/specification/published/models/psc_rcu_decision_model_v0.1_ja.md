# PSC RCU Decision Model v0.1（日本語版）

## 1. ドキュメント情報

- ドキュメント名   : PSC RCU Decision Model
- バージョン       : v0.1
- プロジェクト     : PSC (Photon System Controller)
- レイヤ           : PSCOS / PSC Fabric
- ドキュメント種別 : Specification / Model
- ステータス       : Draft
- 作成者           : T. Hirose
- 作成日           : 2026-04-02
- 最終更新         : 2026-04-02
- 言語             : 日本語

---

## 2. 目的

本モデルは、RCU（Routing Control Unit）の経路選択および切替判断ロジックを定義する。

RCU は Telemetry に基づいて経路候補を評価し、現在の Selected Path を維持するか、新しい Best Path へ切り替えるかを判断する。

---

## 3. 基本構造

RCU の判断は以下の3段階で構成される。

1. Candidate Filtering
2. Score Evaluation
3. Switching Decision

---

## 4. Candidate Filtering

RCU は、スコア計算の前に使用不可経路を除外する。

### 4.1 除外条件

以下の条件に該当する経路は候補から除外する。

- trust violation
- node failure
- policy violation
- hard stale telemetry
- route unavailable

### 4.2 ルール

```text
If trust_violation(path) = true, reject path.
If node_failure(path) = true, reject path.
If policy_violation(path) = true, reject path.
If telemetry_state(path) = hard_invalid, reject path.
```

候補が存在しない場合、RCU は `NO_ROUTE` または `ESCALATE_SWITCH` を出力する。

---

## 5. Score Evaluation

RCU は、有効な経路候補に対して以下の3つのスコアを評価し、経路選択に使用する。

- CongestionScore(path)
- PerformanceScore(path)
- StabilityScore(path)

### 5.1 Congestion Benefit

CongestionScore は小さいほど良いため、統合時には以下のように反転する。

```text
CongestionBenefit(path) = 1 - CongestionScore(path)
```

### 5.2 Final Score

```text
FinalScore(path) =
  Wc * CongestionBenefit(path) +
  Wp * PerformanceScore(path) +
  Ws * StabilityScore(path)
```

### 5.3 初期重み

```text
Wc = 0.4
Wp = 0.3
Ws = 0.3
```

---

## 6. Best Path と Selected Path

RCU は以下の2つを区別する。

- Best Path
  現時点で最も高い FinalScore を持つ経路

- Selected Path
  現在実際に使用している経路

Best Path と Selected Path は一致しなくてもよい。

---

## 7. Switching Decision

RCU は、Best Path が存在しても即時切替は行わない。
改善量、安定性、継続時間を評価して判断する。

### 7.1 Improvement

```text
Improvement =
  FinalScore(BestPath) - FinalScore(SelectedPath)
```

### 7.2 切替条件

```text
If Improvement > switch_margin
  AND StabilityScore(SelectedPath) < switch_stability_threshold
  AND persistence_degradation(SelectedPath) > persistence_limit
then SWITCH
else KEEP
```

### 7.3 戻り条件

```text
If Improvement > return_margin
  AND StabilityScore(BestPath) > return_stability_threshold
  AND persistence_recovery(BestPath) > recovery_limit
then RETURN or SWITCH_BACK
```

### 7.4 初期値例

```text
switch_margin = 0.10
return_margin = 0.15

switch_stability_threshold = 0.40
return_stability_threshold = 0.60

persistence_limit = 3 cycles
recovery_limit = 5 cycles
```

戻り条件は切替条件より厳しくする。

---

## 8. Decision Outputs

RCU は以下の出力を持つ。

- KEEP
- SWITCH
- DEGRADED_SWITCH
- ESCALATE_SWITCH
- NO_ROUTE

---

## 9. Resolver Escalation

RCU 単独で判断できない場合、Resolver へ判断を委譲する。

### 9.1 エスカレーション条件

- no trusted route
- multiple candidates with similar score
- degraded-only candidates
- policy conflict
- unstable telemetry confidence
- repeated switch attempts without convergence

### 9.2 ルール

```text
If no trusted route exists, escalate.
If score difference between top candidates < epsilon, escalate.
If only degraded paths remain, escalate.
If repeated switching does not converge, escalate.
```

---

## 10. 結論

本モデルにより、RCU は以下を実現する。

- 制約条件に基づく候補除外
- 複数スコアに基づく経路評価
- ヒステリシスを用いた安定した切替判断

---

## 11. 次のステップ

- RCU Model 全体への統合
- Simulation への実装
- Resolver 連携条件の詳細化
