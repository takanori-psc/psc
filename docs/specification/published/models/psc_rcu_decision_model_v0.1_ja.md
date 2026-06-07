# PSC RCU Decision Model v0.1（日本語版）

## 1. Document Information

- Document Name : PSC RCU Decision Model
- Version : v0.1
- Project : PSC (Photon System Controller)
- Layer : PSCOS / PSC Fabric
- Document Type : Specification / Model
- Status : Draft
- Author : T. Hirose
- Created : 2026-04-02
- Last Updated : 2026-04-02
- Language : Japanese

---

## 2. 目的

本モデルは、RCU（Routing Control Unit）の経路選択および切替判断ロジックを定義する。

RCU は Telemetry に基づいて経路候補を評価し、現在の Selected Path を維持するか、新しい Best Path へ切り替えるかを判断する。

運用上の `RULE-*` ID は、現在の Evidence Matrix / validation namespace で定義される。
本モデル内の STEP / 処理段階は、公開モデルの内部処理ステージを示すものであり、運用ルール ID ではない。

---

## 3. 基本構造

本節は、既存の `RULE-*` 所有関係、verified evidence、simulation logs を変更せず、
PSC score model と resolver priority logic の解釈を明確化する。

RCU の判断は以下の4層で構成される。

| Layer | 名称 | 主な基準 | 目的 |
|-------|------|----------|------|
| Layer 1 | Eligibility | trust threshold、policy compliance、verification state、`trust_block` | 選択に参加できない path を除外する |
| Layer 2 | Normal Selection | congestion の低さ + performance による `final_score` | 通常時の候補を選択する |
| Layer 3 | Resolver Selection | trust + stability + performance による `resolver_score` | Resolver Active 時に keep / switch を裁定する |
| Layer 4 | Recovery Selection | stability + trust + performance による `return_score` | Recovery 後の復帰可否を判断する |

Layer 1 で hard exclusion された path は、後続 layer の score 比較で再採用してはならない。

---

## 4. Layer 1: Eligibility

RCU は、スコア計算の前に使用不可経路を除外する。

### 4.1 除外条件

以下の条件に該当する経路は候補から除外する。

- trust threshold 未満
- trust violation / `trust_block`
- node failure
- policy violation
- verification state failure
- hard stale telemetry
- route unavailable

規制違反リスクは policy violation として扱い、trust / policy 判定に含める。

`trust_score` と `trust_block` は分離する。

- `trust_score`
  path の選好または減点に使う評価要素。
- `trust_block`
  threshold 未満または重大違反時の除外条件。

### 4.2 処理ステップ

```text
If trust_violation(path) = true, reject path.
If trust_block(path) = true, reject path.
If node_failure(path) = true, reject path.
If policy_violation(path) = true, reject path.
If verification_state(path) = failed, reject path.
If telemetry_state(path) = hard_invalid, reject path.
```

候補が存在しない場合、RCU は `NO_ROUTE` または `ESCALATE_SWITCH` を出力する。

---

## 5. Layer 2: Normal Selection

RCU は、有効な経路候補に対して通常時の `final_score` を評価し、候補選択に使用する。

- CongestionScore(path)
- PerformanceScore(path)

### 5.1 Congestion Benefit

CongestionScore は小さいほど良いため、統合時には以下のように反転する。

```text
CongestionBenefit(path) = 1 - CongestionScore(path)
```

### 5.2 Final Score

```text
FinalScore(path) =
  Wc * CongestionBenefit(path) +
  Wp * PerformanceScore(path)
```

`FinalScore` は通常時の候補選択用 score であり、基本構成は
congestion の低さ + performance である。

StabilityScore は通常時 `FinalScore` の主要構成要素ではない。
ただし、hysteresis、eligibility、Resolver activation、Resolver arbitration、
Recovery return では重要な判断要素として扱う。

`cost_score` と `power_score` は将来拡張として追加可能だが、
v0.1 / v0.2 の中核判断には含めない。

### 5.3 Stability Score

```text
instability = f(variance, trend, duration)
StabilityScore(path) = 1 - instability
```

StabilityScore は瞬間値ではなく、観測履歴から算出する。
観測値には timestamp を持たせる。
実装上は Observation 側の ring buffer または time window により評価する前提とする。
具体的な window 秒数は固定せず、configurable parameter として扱う。

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

## 8. Resolver Escalation

RCU 単独で判断できない場合、Resolver へ判断を委譲する。

### 8.1 エスカレーション条件

- no trusted route
- multiple candidates with similar score
- degraded-only candidates
- policy conflict
- unstable telemetry confidence
- repeated switch attempts without convergence

### 8.2 処理ステップ

```text
If no trusted route exists, escalate.
If score difference between top candidates < epsilon, escalate.
If only degraded paths remain, escalate.
If repeated switching does not converge, escalate.
```

---

## 9. Layer 3: Resolver Selection

Resolver Active 時は、通常時の `FinalScore` ではなく `ResolverScore` を優先する。

Resolver Active 条件の例:

- trust conflict
- stability degradation
- ambiguous score result
- `RULE-05` / `RULE-06` / `RULE-14` など Resolver 関連 rule の発動

```text
ResolverScore(path) =
  Wr_trust * TrustScore(path) +
  Wr_stability * StabilityScore(path) +
  Wr_performance * PerformanceScore(path)
```

重みの順序は以下とする。

```text
Trust > Stability > Performance
```

Trust が threshold 未満の path は、ResolverScore 比較の前に除外する。

---

## 10. Layer 4: Recovery Selection

Recovery 復帰では、通常時の `FinalScore` ではなく `ReturnScore` を使用する。

```text
ReturnScore(path) =
  Wret_stability * StabilityScore(path) +
  Wret_trust * TrustScore(path) +
  Wret_performance * PerformanceScore(path)
```

重みの順序は以下とする。

```text
Stability > Trust > Performance
```

`ReturnScore` は復帰可否の判断であり、通常選択の `FinalScore` とは分離する。

---

## 11. Decision Outputs

RCU は以下の出力を持つ。

- KEEP
- SWITCH
- DEGRADED_SWITCH
- ESCALATE_SWITCH
- NO_ROUTE

---

## 12. 結論

本モデルにより、RCU は以下を実現する。

- 制約条件に基づく候補除外
- 通常選択、Resolver 選択、Recovery 選択の score 分離
- ヒステリシスを用いた安定した切替判断

---

## 13. 次のステップ

- RCU Model 全体への統合
- Simulation への実装
- Resolver 連携条件の詳細化
