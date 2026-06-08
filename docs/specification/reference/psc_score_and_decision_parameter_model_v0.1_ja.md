# PSC Score and Decision Parameter Model v0.1（日本語版）

## 1. Document Information

- Document Name : PSC Score and Decision Parameter Model
- Version : v0.1
- Project : PSC (Photon System Controller)
- Layer : PSCOS / PSC Fabric
- Document Type : Reference / Parameter Model
- Status : Draft
- Author : T. Hirose
- Created : 2026-06-08
- Last Updated : 2026-06-08
- Language : Japanese

---

## 2. 目的

本ドキュメントは、PSC の score model と decision parameter を、
実装・検証・仕様文書間で参照しやすいように整理する参照モデルである。

本モデルは以下を扱う。

- score の種類
- score の意味
- decision layer ごとの重み付け
- score 算出に利用する低レベル観測パラメータ
- 合成 score ごとの入力関係

本ドキュメントは、既存の `RULE-*` ID、verified evidence、simulation logs を変更しない。

---

## 3. Score Types

| Score | 日本語での意味 | 主に見るもの | 高い場合の扱い | 性質 |
|-------|----------------|--------------|----------------|------|
| `congestion_score` | 混雑スコア | 使用率、バッファ、リトライ、遅延、packet loss | 高いほど混んでいるため不利 | マイナス要素 |
| `performance_score` | 性能スコア | throughput、低遅延性 | 高いほど性能が良い | プラス要素 |
| `stability_score` | 安定性スコア | 変動、悪化傾向、継続的不安定さ | 高いほど安定している | プラス要素 |
| `trust_score` | 信頼スコア | path の信頼度、policy 適合、検証状態、観測された挙動 | 高いほど安全に選びやすい | プラス要素 |
| `final_score` | 通常時の経路スコア | congestion の低さ + performance | 高い path が通常時の候補になる | 通常選択用 |
| `resolver_score` | Resolver 判断スコア | trust + stability + performance | Resolver が安全な path を選ぶ時に使う | Resolver 選択用 |
| `return_score` | 復帰判断スコア | stability + trust + performance | recovery 後に戻してよい path か見る | Recovery 選択用 |
| `priority` | RULE 優先度スコア | RULE 同士の強さ | 高い RULE が最終判断に勝つ | RULE 衝突解決用 |

---

## 4. Score Interpretation

### 4.1 Congestion Score

```text
congestion_score =
  utilization の影響
+ buffer pressure の影響
+ retry / retransmission の影響
+ latency の影響
+ packet loss の影響
```

`congestion_score` は高いほど不利である。
通常時の `final_score` へ統合する場合は、以下のように反転して扱う。

```text
congestion_benefit = 1 - congestion_score
```

### 4.2 Performance Score

```text
performance_score =
  throughput の良さ
+ latency の少なさ
```

`performance_score` は高いほど有利である。

### 4.3 Stability Score

```text
stability_score =
  1 - instability

instability =
  variance の大きさ
+ trend による悪化方向
+ duration / persistence による不安定状態の継続
```

`stability_score` は瞬間値ではなく、timestamp を持つ観測履歴から算出する。
実装上は Observation 側の ring buffer または time window により評価する。
具体的な window 秒数やサンプル数は固定せず、configurable parameter として扱う。

### 4.4 Trust Score

`trust_score` は、静的な認証・検証状態だけではなく、
動的な Trust Event によって変化し得る。

Trust Event の例:

- authentication failure
- policy violation
- signature mismatch
- abnormal communication
- attack indicators

`trust_score` と `trust_block` は分離する。

- `trust_score`
  path の選好または減点に使う評価要素。
- `trust_block`
  trust threshold 未満、explicit trust_block、または重大違反時の除外条件。

---

## 5. Composite Score Model

### 5.1 Normal Final Score

通常時の `final_score` は、normal selection 用の score である。
基本構成は congestion の低さ + performance とする。

```text
final_score =
  Wc * congestion_benefit +
  Wp * performance_score
```

`stability_score` は通常時 `final_score` の主要構成要素ではない。
ただし、hysteresis、eligibility、Resolver、Recovery では重要な判断要素として扱う。

`cost_score` と `power_score` は将来拡張として追加可能だが、
v0.1 / v0.2 の中核判断には含めない。

### 5.2 Resolver Score

Resolver Active 時は、通常時の `final_score` ではなく
`resolver_score` を優先する。

```text
resolver_score =
  Wr_trust * trust_score +
  Wr_stability * stability_score +
  Wr_performance * performance_score
```

重みの順序は以下とする。

```text
Trust > Stability > Performance
```

trust threshold 未満の path は、`resolver_score` 比較の前に除外する。

### 5.3 Return Score

Recovery 復帰では、通常時の `final_score` ではなく
`return_score` を使用する。

```text
return_score =
  Wret_stability * stability_score +
  Wret_trust * trust_score +
  Wret_performance * performance_score
```

重みの順序は以下とする。

```text
Stability > Trust > Performance
```

`return_score` は復帰可否の判断であり、通常選択の `final_score` とは分離する。

---

## 6. Decision Weight Meaning

| 判断場面 | 一番重いもの | 次に重いもの | 最後に見るもの |
|----------|--------------|--------------|----------------|
| 通常時 | congestion の低さ / performance | しきい値 / hysteresis | trust block / escalation |
| Resolver 判断 | Trust | Stability | Performance |
| Recovery 復帰 | Stability | Trust | Performance |

要点:

- 通常時:
  速くて空いている path を候補にする。
- Resolver:
  速さより、信頼できて安定している path を選ぶ。
- Recovery:
  まず安定していることを最優先にする。

PSC は速い path を単純に選ぶのではなく、混雑・性能・信頼・安定性を分離して評価し、
状態に応じて重みを変える。

---

## 7. Low-Level Observation Parameters

### 7.1 Score Inputs

| Score | 低レベル観測パラメータ | 種別 |
|-------|------------------------|------|
| `congestion_score` | `utilization` | link 使用率 |
| `congestion_score` | `buffer_pressure` / `buffer` | バッファ詰まり |
| `congestion_score` | `retry_rate` / `retry` | 再送 / リトライ |
| `congestion_score` | `latency` | link 遅延 |
| `congestion_score` | `packet_loss` | packet loss |
| `performance_score` | `throughput` / `throughput_estimate` | 実効 throughput |
| `performance_score` | `latency` / `end_to_end_latency` | end-to-end 遅延 |
| `stability_score` | `variance` | 観測値のばらつき |
| `stability_score` | `trend` | 悪化 / 改善方向 |
| `stability_score` | `duration` | 状態継続時間 |
| `stability_score` | `persistence` | 不安定状態の継続度 |
| `stability_score` | `timestamp` | 履歴評価用の時刻 |
| `stability_score` | ring buffer / time window | 履歴保持単位 |
| `trust_score` | `CRC/error_rate` | 通信エラー率 |
| `trust_score` | `link_stability` / link flapping | link 安定性 |
| `trust_score` | `thermal_state` | 温度状態 |
| `trust_score` | `power_stability` | 電源安定性 |
| `trust_score` | `firmware_integrity` | firmware 改ざん有無 |
| `trust_score` | `hardware_diagnostics` | HW 自己診断 |
| `trust_score` | `secure_boot_validation` | secure boot 検証 |
| `trust_score` | `signature_validation` / `signature_mismatch` | 署名検証 |
| `trust_score` | `authentication_result` / authentication failure | 認証状態 |
| `trust_score` | `policy_validation_result` | policy 適合 |
| `trust_score` | `abnormal_communication` | 異常通信 |
| `trust_score` | `attack_indicators` | 攻撃兆候 |
| `health_score` / Eligibility | `node_health_state` | node 健全性 |
| `health_score` / Eligibility | `failure_state` | failure 状態 |
| `health_score` / Eligibility | `processing_load` | node 処理負荷 |
| `health_score` / Eligibility | `route_availability` | route 利用可否 |
| `health_score` / Eligibility | `telemetry_freshness` / `freshness` | 更新時刻 |
| `health_score` / Eligibility | `confidence` | 観測信頼度 |
| `health_score` / Eligibility | `source_reliability` | 情報源信頼度 |

### 7.2 Composite Score Inputs

| Composite Score | 利用する派生スコア | 元になる低レベル観測 |
|-----------------|--------------------|----------------------|
| `final_score` | `congestion_score`, `performance_score` | utilization, buffer, retry, latency, packet_loss, throughput |
| `resolver_score` | `trust_score`, `stability_score`, `performance_score` | trust 系 HW / 検証情報、variance, trend, duration, throughput, latency |
| `return_score` | `stability_score`, `trust_score`, `performance_score` | variance, trend, duration, trust 系 HW / 検証情報、throughput, latency |

---

## 8. PSC Decision Parameters

Decision Parameters は、score 算出後に RULE Engine が判断を確定するための
しきい値、window、cooldown などの制御パラメータである。

これらは score そのものではない。
score をどう解釈し、どの RULE を発動させるかを決める境界条件である。

| Parameter | 日本語での意味 | 主な用途 | 関連 layer / RULE |
|-----------|----------------|----------|-------------------|
| `switch_threshold` / `switch_margin` | 切替しきい値 | `score_gap` または improvement が十分大きい場合のみ switch を許可する | Normal Selection / `RULE-01`, `RULE-02` |
| `trust_threshold` | trust 下限 | threshold 未満の path を Eligibility で除外する | Eligibility / `RULE-04`, `RULE-07`, `RULE-09` |
| `trust_switch_threshold` | trust switch しきい値 | trust が十分高い候補を trust-driven switch candidate として扱う | Resolver / Trust Switch / `RULE-03` |
| `trust_block_threshold` | trust block しきい値 | threshold 未満の trust を block cause として扱う。explicit `trust_block` とは原因を分離するが outcome は同じ `BLOCK_SWITCH` | Eligibility / `RULE-04` |
| `return_threshold` / `return_margin` | 復帰しきい値 | Recovery candidate の improvement が十分な場合のみ return を許可する | Recovery Selection / `RULE-19`, `RULE-20` |
| `return_trust_threshold` | 復帰 trust 下限 | Recovery return candidate が復帰候補になれる trust 条件 | Recovery Selection / `RULE-15`, `RULE-18` |
| `return_stability_threshold` | 復帰 stability 下限 | Recovery return candidate が復帰候補になれる stability 条件 | Recovery Selection / `RULE-15`, `RULE-18` |
| `resolver_trigger_threshold` / `epsilon` | Resolver 発動しきい値 | `score_gap` が小さく、trust / stability conflict がある場合に Resolver へ渡す | Resolver Selection / `RULE-05` |
| `trust_conflict_threshold` | trust conflict しきい値 | trust 差が大きく、local decision で決めにくい場合に conflict と扱う | Resolver Selection / `RULE-05`, `RULE-14` |
| `stability_conflict_threshold` | stability conflict しきい値 | stability 差が大きく、local decision で決めにくい場合に conflict と扱う | Resolver Selection / `RULE-05`, `RULE-14` |
| `stability_window` | stability 評価 window | `variance` / `trend` / `duration` を評価する観測履歴範囲 | Observation / Stability |
| `persistence_limit` | 継続判定しきい値 | 一時的な変動ではなく、継続した degradation の場合のみ switch / escalation を許可する | Hysteresis / `RULE-01`, `RULE-02` |
| `cooldown_steps` | cooldown step 数 | 連続 switch / 連続 escalation を抑制する | Cooldown / `RULE-11`, `RULE-12` |
| `resolver_cooldown_steps` | Resolver cooldown step 数 | Resolver 実行後の再 escalation を抑制する | Resolver Cooldown / `RULE-12` |
| `recovery_cooldown_steps` | Recovery cooldown step 数 | recovery 直後の再切替を抑制する | Recovery Cooldown / `RULE-11` |

### 8.1 Decision Flow

PSC の score / parameter / rule の関係は以下の順序で整理する。

```text
Observation Parameters
  utilization, latency, retry, trust events, timestamp, confidence, ...

↓

Derived Scores
  congestion_score, performance_score, stability_score, trust_score

↓

Composite Scores
  final_score, resolver_score, return_score

↓

Decision Parameters
  switch_threshold, trust_threshold, return_threshold,
  resolver_trigger_threshold, stability_window, cooldown_steps

↓

RULE Engine
  RULE-01_KEEP_score, RULE-02_SWITCH_score, RULE-04_BLOCK_trust,
  RULE-05_ESCALATE_conflict, RULE-11_RECOVERY_cooldown,
  RULE-12_COOLDOWN_active, ...
```

### 8.2 Parameter Notes

- `switch_threshold` と `switch_margin` は、文脈により同系の切替境界として扱われる。
- `return_threshold` と `return_margin` は、Recovery return の境界として扱われる。
- `resolver_trigger_threshold` は、実装や文書内では `epsilon` として表れる場合がある。
- `stability_window` は固定秒数ではなく、configurable parameter とする。
- `cooldown_steps` は汎用名であり、実装上は `resolver_cooldown_steps` と
  `recovery_cooldown_steps` に分かれる場合がある。
- explicit `trust_block` と `trust_block_threshold` 未満は別原因だが、
  outcome は同じ `RULE-04_BLOCK_trust` による `BLOCK_SWITCH` として扱える。

---

## 9. Notes

- `policy_validation_result` は低レベルの物理観測ではない。
  ただし、`trust_score` と Eligibility に入る制御観測パラメータとして扱う。
- `priority` は path score ではなく、RULE 同士の衝突解決に使う優先度である。
- 本ドキュメントの score 名は、PSC RCU Decision Model、Telemetry Model、
  Trust Model、Recovery Return Model と整合する参照名として扱う。
