# PSC Telemetry Model v0.1

## ドキュメント情報

- ドキュメント名   : PSC Telemetry Model
- バージョン       : v0.1
- プロジェクト     : PSC / Photon System Controller
- レイヤ           : PSC Fabric
- ドキュメント種別 : 仕様書
- ステータス       : Draft
- 作成者           : T. Hirose
- 作成日           : 2026-03
- 最終更新         : 2026-03
- 言語             : Japanese

---

## 1. Purpose（目的）

本ドキュメントは、PSC Fabric における Telemetry Model を定義する。

Telemetry Model は、Fabric の観測情報を収集・正規化・評価し、
Routing および Control Plane が利用可能な状態情報へ変換する。

本モデルは以下の出力を提供する。

- congestion_score（混雑評価）
- health_state（健全性状態）
- availability_state（利用可能性状態）
- trust_score_ref（参照情報、任意）

Telemetry は PSC Fabric の単なる観測機構ではなく、
**Routing に利用可能な状態を生成する評価モデル**として機能する。

---

## 2. Scope（適用範囲）

本ドキュメントは以下を対象とする。

- Telemetry Entry 構造
- 入力パラメータ
- 出力パラメータ
- 評価単位
- 状態評価モデル
- 更新モデル
- Routing Table との接続

以下は対象外とする。

- Telemetry データフォーマット
- Telemetry 転送プロトコル
- Telemetry データ保存方式
- Routing 意思決定ロジック
- Trust 評価の詳細アルゴリズム

---

## 3. Design Principles（設計原則）

### 3.1 Separation of Responsibilities

- Telemetry : 状態生成
- Routing Table : 状態保持
- RCU : 意思決定

責務は厳密に分離する。

### 3.2 Observability

Telemetry は観測可能な情報および外部参照情報に基づく。

### 3.3 Stability over Noise

一時的な変動よりも持続的な状態を優先して評価する。

### 3.4 Routing-facing Simplicity

出力は Routing が直接利用可能な形式とする。

## 4. Telemetry Entry Model

Telemetry は評価単位ごとに以下の構造で表現される。

```text
TelemetryEntry {
    telemetry_id
    target_type
    target_id
    scope_level
    timestamp
    input_snapshot
    evaluated_state
    update_reason
    confidence
    ttl
}
```

### フィールド定義

- telemetry_id
  エントリ識別子

- target_type
  対象種別（LINK / NODE / PATH / FABRIC）

- target_id
  対象識別子

- scope_level
  評価スコープ

- timestamp
  評価時刻

- input_snapshot
  入力値セット

- evaluated_state
  出力状態

- update_reason
  更新理由

- confidence
  評価信頼度

- ttl
  有効期限

---

## 5. Input Parameters

Telemetry は以下の入力を使用する。

### 5.1 Observed Inputs（観測入力）

#### Link関連

- link utilization
- latency
- retry count
- packet loss
- error rate
- credit starvation
- link state（up/down）

#### Node関連

- node state
- processing backlog
- queue occupancy
- buffer pressure
- retry concentration
- timeout events

#### Queue / Buffer

- queue depth
- queue saturation ratio
- buffer occupancy
- sustained backlog duration

### 5.2 Referenced Inputs（参照入力）

#### Policy関連

- policy constraints
- routing class requirements

#### Trust / Security関連

- trust classification
- attestation result
- security alert state

※ trust は Telemetry による直接生成対象ではなく、参照情報とする。

---

## 6. Output Parameters

Telemetry は Routing 向けに以下を出力する。

### 6.1 congestion_score

混雑状態を示す連続値。

例：

- 範囲 : 0.0 – 100.0
- 高いほど混雑

### 6.2 health_state

対象の内部健全性。

```text
HEALTHY
DEGRADED
FAILED
```

### 6.3 availability_state

Routing リソースとしての利用可能性。

```text
AVAILABLE
RESTRICTED
UNAVAILABLE
```

---

### 6.4 trust_score_ref（任意）

外部 Trust モデルによる参照値。

---

## 7. Evaluation Units

Telemetry は以下の単位で評価される。

### 7.1 Link-level

最小単位。混雑評価の基本。

### 7.2 Node-level

ノード内部状態を評価。

### 7.3 Path-level

複数要素の集約評価。

### 7.4 Fabric-level

全体状態の評価。

---

## 8. Congestion Score Model

congestion_score は加算モデルで評価する。

```text
congestion_score =
  utilization_score
+ buffer_pressure_score
+ latency_penalty
+ retry_penalty
+ loss_penalty
+ credit_starvation_penalty
+ persistence_modifier
- recovery_modifier
- stability_modifier
```

### 設計方針

- 単一指標で判断しない
- 持続的状態を重視
- 回復は慎重に評価
- ヒステリシスを適用

---

## 9. Health State Evaluation

```text
if hard_failure:
    FAILED
elif persistent_degradation:
    DEGRADED
else:
    HEALTHY
```

### 判定例

#### FAILED

- link down
- node unreachable
- fatal error

#### DEGRADED

- 高遅延継続
- retry多発
- buffer圧迫

---

## 10. Availability State Evaluation

```text
if unavailable_condition:
    UNAVAILABLE
elif restricted_condition:
    RESTRICTED
else:
    AVAILABLE
```

### 判定例

#### UNAVAILABLE

- link down
- isolation
- administrative disable

#### RESTRICTED

- policy制限
- trust制限
- 性能低下

---

## 11. Update Model

Telemetry は以下の更新方式を持つ。

### 11.1 Periodic Update

定期更新

### 11.2 Event-driven Update

障害・状態変化時

### 11.3 Threshold Trigger

閾値超過時

### 11.4 Hysteresis

状態振動の抑制

---

## 12. Routing Table Interface

Telemetry は Routing Table に対し以下の形式で供給される。

```text
RoutingTelemetryBinding {
    target_id
    target_type
    congestion_score
    health_state
    availability_state
    trust_score_ref
    timestamp
    confidence
    ttl
}
```

---

## 13. Summary（まとめ）

PSC Telemetry Model は、

- Fabric 状態を観測し
- 状態を評価し
- Routing が利用可能な形式で提供する

評価モデルである。

Telemetry により PSC Fabric は

- 観測可能
- 状態認識可能
- 適応可能

な分散システムとして機能する。
