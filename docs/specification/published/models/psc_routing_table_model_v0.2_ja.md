# PSC Routing Table Model v0.2

## Document Information

- ドキュメント名: PSC Routing Table Model
- バージョン : v0.2
- プロジェクト : PSC / Photon System Controller
- レイヤ : PSC Control Plane
- ドキュメント種別 : Model Specification
- ステータス : Review
- 作成者 : T. Hirose
- 作成日 : 2026-03
- 最終更新 : 2026-03
- 言語 : Japanese

---

## 1. Overview

本ドキュメントは PSC Fabric において RCU（Routing Control Unit）が使用する
**ルーティングテーブルモデル**を定義する。

本モデルは以下を統合的に扱う。

- マルチパス構造
- Policy / Trust / Congestion 統合
- 経路状態管理（Failover / Degraded / Recovery）
- 説明可能かつ再現可能なルーティング判断

---

## 2. Design Principles

### 2.1 Receiver-driven Routing

ルーティングは送信側ではなく受信側（Fabric / RCU）によって制御される。

### 2.2 Explainable Decision Model

経路選択は常に説明可能かつ再現可能である必要がある。

### 2.3 Multi-dimensional Evaluation

以下を統合的に評価する。

- topology
- congestion
- trust
- policy
- stability

### 2.4 Separation of Roles

- Routing Table : 情報保持
- RCU : 意思決定
- Resolver : 例外判断

---

## 3. Data Model

PSC Routing Table は以下の二層構造を採用する。

```
Routing Table
 ├─ Destination Entry
 │   ├─ Path Entry
 │   ├─ Path Entry
 │   └─ Path Entry
```

---

## 4. Destination Entry

### 4.1 概要

Destination Entry は宛先単位の集約情報を保持する。

### 4.2 フィールド

- destination_id

- destination_prefix

- address_type

- reachable

- selected_path_id

- best_path_id

- fallback_path_id

- policy_profile

- trust_requirement

- entry_version

- last_updated

### 4.3 説明

- selected_path_id
  現在使用中の経路

- best_path_id
  評価上最も優れた経路

- fallback_path_id
  フェイルオーバー候補

### 4.4 policy_profile

例:

- latency
- stability
- trusted
- bulk

### 4.5 trust_requirement

例:

- off
- prefer_trusted
- require_trusted

---

## 5. Path Entry

### 5.1 概要

Path Entry は宛先への個別経路候補を表す。

### 5.2 識別情報

- path_id
- destination_id
- next_hop_port
- next_hop_node
- hop_count
- hop_list

### 5.3 コスト・評価

- base_cost
- dynamic_cost
- total_score

※評価式は別仕様（Congestion / Policy / RCU）で定義する

### 5.4 Trust

- trust_level
- trust_score

### 5.5 Congestion

- congestion_score

Telemetry に基づく経路混雑状態を表す。

### 5.6 状態

- health_state
- availability_state
- path_state

#### health_state

- NORMAL
- WARNING
- CONGESTED
- DEGRADED
- FAILED

#### availability_state

- AVAILABLE
- LIMITED
- UNAVAILABLE

#### path_state

- SETUP
- ACTIVE
- STANDBY
- FAILOVER
- RECOVERY
- TEARDOWN

### 5.7 性能推定

- bandwidth_estimate
- latency_estimate
- loss_estimate

### 5.8 Policy

- policy_flags

例:

- LOW_LATENCY
- STABILITY
- TRUST_REQUIRED
- BULK_TRANSFER
- SECURITY_RESTRICTED

### 5.9 運用フラグ

- is_selected

- is_backup

- valid_until

- last_evaluated

---

## 6. Routing Table Behavior

### 6.1 Route Selection

Routing Table 自体は選択を行わない。
RCU が判断を行う。

### 6.2 Best vs Selected

- best_path : 評価上最良
- selected_path : 実際に使用中

### 6.3 Failover

selected_path が使用不能な場合：

- fallback_path
- または degraded path

を使用する。

### 6.4 Degraded Operation

以下を許容する場合がある：

- trust低下
- 帯域低下
- 遅延増加

---

## 7. Interaction with RCU

RCU は以下を実施する：

- Path 評価
- Best Path 計算
- Selected Path 制御
- Failover / Recovery

---

## 8. Interaction with Resolver

Resolver は以下で介入する：

- trusted path 不在
- policy conflict
- degraded 継続判断
- 複数評価軸競合

---

## 9. Indexing

### Primary

- destination_id

### Secondary

- next_hop_port
- path_state
- trust_level
- policy_flags

---

## 10. Lifecycle

- Creation (topology discovery / configuration)
- Update (telemetry / congestion / policy)
- Invalidation (failure / restriction)
- Removal (expiration / cleanup)

---

## 11. Example

### Destination Entry

```YAML
Destination Entry:
  destination_id: dst_mem_0042
  selected_path_id: path_02
  best_path_id: path_01
  fallback_path_id: path_03
  policy_profile: stability
  trust_requirement: prefer_trusted
```

### Path Entry

```YAML
Path Entry:
  path_id: path_02
  next_hop_port: port_3
  next_hop_node: node_07
  hop_count: 4

  base_cost: 12
  dynamic_cost: 5
  total_score: 17

  trust_level: TRUSTED
  congestion_score: 3

  health_state: NORMAL
  availability_state: AVAILABLE
  path_state: ACTIVE

  is_selected: true
```

---

## 12. Design Considerations

### 12.1 Logical vs Physical Separation

論理ルーティング（Port）と物理経路（Node）は分離される。

### 12.2 Scalability

Destination / Path 分離によりスケーラブルな設計を実現する。

### 12.3 Extensibility

新たな評価軸（AI / telemetry / optical特性）を追加可能。

---

## 13. Future Work

- Congestion Model 統合
- Telemetry Model 定義
- RCU Evaluation Function 定義
- Hardware optimized representation

---

## 14. Summary

PSC Routing Table Model v0.2 は

- Destination / Path 二層構造
- multi-path routing
- policy / trust / congestion 統合
- failover / degraded 対応

を備えた PSC の中核モデルである。
