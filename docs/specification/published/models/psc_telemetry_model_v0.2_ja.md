# PSC Telemetry Model v0.2（日本語版）

## 1. ドキュメント情報

- ドキュメント名   : PSC Telemetry Model
- バージョン       : v0.2
- プロジェクト     : PSC (Photon System Controller)
- レイヤ           : PSCOS / PSC Fabric
- ドキュメント種別 : Specification / Model
- ステータス       : Draft
- 作成者           : T. Hirose
- 作成日           : 2026-04-02
- 最終更新         :2026-04-02
- 言語             :日本語

---

## 2. 目的

本モデルは、RCU（Routing Control Unit）および Resolver が意思決定に使用する観測データの構造を定義する。

本モデルの設計方針は以下とする。

- Telemetry は事実ではなく「観測結果」である
- 観測データには不確実性が含まれる
- RCU は不確実性を考慮して判断を行う

---

## 3. 設計原則

### 3.1 Telemetry = Evidence

Telemetry は真実ではない。
RCU は Telemetry を「証拠」として扱い、信頼度に応じて重み付けする。

### 3.2 Granularityの明確化

すべてのメトリクスは以下の2軸を持つ。

- 時間粒度（Temporal Resolution）
- 空間粒度（Spatial Scope）

### 3.3 Adaptive Sampling

観測頻度は固定としない。
状態に応じて動的に変更する。

---

## 4. Telemetry Granularity

### 4.1 Temporal Resolution（時間粒度）

各メトリクスは基準周期（Base Interval）を持ち、状態に応じて観測頻度を変化させる。

#### Link Metrics

- Base Interval: 10ms
- 高負荷時: 1〜5ms
- 安定時: 50ms

#### Node Metrics

- Base Interval: 100ms
- 劣化時: 50ms

#### Path Metrics

- Base Interval: 200ms
- 不安定時: 50〜100ms

### 4.2 Adaptive Samplingルール

以下の条件で観測頻度を引き上げる。

- パケットロス増加
- レイテンシ急変
- リトライ増加
- ハートビート欠落
- 信頼度低下

安定状態が一定期間継続した場合、基準周期へ戻す。

### 4.3 Spatial Scope（空間粒度）

| 種類           | 単位       |
| :------------- | :--------- |
| Link Metrics   | Per-Link   |
| Node Metrics   | Per-Node   |
| Path Metrics   | Per-Path   |
| Aggregated     | 集約単位   |

---

## 5. データ品質属性

すべての Telemetry データは以下の属性を持つ。

- value（観測値）
- confidence（信頼度）
- freshness（更新時刻）
- source_reliability（情報源）

### 5.1 confidence

confidence は以下の要素から構成される。

```
confidence =
  measurement_quality ×
  sampling_density ×
  consistency ×
  source_factor
```

#### 要素定義

- measurement_quality
  計測精度、異常有無

- sampling_density
  サンプル密度

- consistency
  時系列整合性

- source_factor
  情報源の信頼度

### 5.2 source_reliability

| 種別       | 目安       |
| :--------- | :--------- |
| hardware   | 0.9〜1.0   |
| software   | 0.6〜0.85  |
| derived    | 0.3〜0.7   |

### 5.3 freshness

freshness は更新時刻である。
RCU は現在時刻との差分（Age）で評価する。

---

## 6. Telemetry定義

### 6.1 Link Metrics

- utilization
- latency
- retry_rate
- packet_loss
- buffer_pressure

### 6.2 Node Metrics

- node_health_state
- processing_load
- failure_state

### 6.3 Path Metrics

- end_to_end_latency
- stability
- throughput_estimate

---

## 7. 派生スコア

### 7.1 Congestion Score

リンクの負荷状態を表す。

### 7.2 Health Score

ノード状態を表す。

### 7.3 Stability Score

変動性を表す。

---

## 8. Decay / Aging

### 8.1 基本方針

古いデータは即時破棄しない。
時間経過に応じて重みを減衰させる。

### 8.2 減衰モデル

```
weight = confidence × exp(-λ × Age)
```

### 8.3 最小保持

短時間は最低重みを保持する。

### 8.4 失効条件

以下の場合のみ無効とする。

- 長時間更新なし
- 情報源異常
- ポリシー違反

---

## 9. RCU入力インターフェース

### 9.1 入力構造

```
metric_name
scope_id
raw_value
normalized_value
confidence
timestamp
source
trend
variance
sample_count
```

### 9.2 使用ルール

- raw_value は記録用
- normalized_value は評価用
- trend は方向判定に使用
- variance は安定性評価に使用

---

## 10. 結論

本モデルは以下を実現する。

- 不確実性を考慮した意思決定
- 状態変化への高速追従
- ノイズ耐性のある制御

---

## 11. 次のステップ

- RCU評価関数の設計
- Degraded制御仕様
- Resolver発火条件
