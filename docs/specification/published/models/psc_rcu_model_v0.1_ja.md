# PSC RCU Model v0.1

## ドキュメント情報

- ドキュメント名   : PSC Routing Control Unit Model
- バージョン       : v0.1
- プロジェクト     : PSC / Photon System Controller
- レイヤ           : PSCOS（Control Layer）
- ドキュメント種別 : 仕様書
- ステータス       : Draft
- 作成者           : T. Hirose
- 作成日           : 2026-03
- 最終更新         : 2026-03
- 言語             : Japanese

---

## 1. Purpose（目的）

本ドキュメントは、PSC Fabric における Routing Control Unit（RCU）Model を定義する。

RCU は以下を目的とする：

- Routing Table および Telemetry の状態を基に
- 最適な経路を選択し
- 状態変化に応じて経路切替を制御する

RCU は PSC Fabric における**意思決定層**である。

---

## 2. Scope（適用範囲）

本モデルは以下を定義する：

- RCU の責務
- 入力構造
- 出力構造
- 意思決定パイプライン
- 経路選択および切替ロジック

以下は対象外とする：

- Routing Table の構造定義
- Telemetry の生成ロジック
- Resolver の詳細仕様
- 物理転送処理

---

## 3. Design Principles（設計原則）

### 3.1 Separation of Responsibilities

- Telemetry：状態生成
- Routing Table：状態保持
- RCU：意思決定

### 3.2 Best vs Selected の分離

RCU は以下を明確に区別する：

- Best Path：理論的最適経路
- Selected Path：実際に使用中の経路

この分離により安定性と適応性を両立する。

### 3.3 Stability over Aggressiveness

頻繁な切替を避け、安定性を優先する。

### 3.4 Explainability

RCU の判断は説明可能でなければならない。

---

## 4. RCU Inputs

RCU は以下の入力を受け取る。

### 4.1 Routing Candidates（Routing Table）

```text
PathCandidate {
    path_id
    hops[]
    link_ids[]
    node_ids[]
    base_cost
    capacity
}
```

### 4.2 Telemetry Binding

```text
RoutingTelemetryBinding {
    target_id
    congestion_score
    health_state
    availability_state
    trust_score_ref
}
```

### 4.3 Routing Policy

```text
RoutingPolicy {
    mode                // latency / stability / trust
    hysteresis_margin
    trust_mode          // off / prefer / require
}
```

### 4.4 Transfer Request（TMU）

```text
TransferRequest {
    src
    dst
    class
    qos
    deadline
}
```

---

## 5. RCU Outputs

RCU は以下を出力する。

```text
PathDecision {
    selected_path_id
    decision_type   // KEEP / SWITCH / DEGRADED_SWITCH / ESCALATE
    reason {
        type
        details
    }
}
```

---

## 6. Decision Pipeline

RCU の意思決定は以下の段階で構成される。

### 6.1 Phase 1: Candidate Filtering

利用不可能な経路を除外する。

#### Availability Filter

- availability_state == UNAVAILABLE → 除外
- availability_state == RESTRICTED → Degraded Mode または policy 条件下で許可
- availability_state == AVAILABLE → 許可

#### Trust Filter

- trust_mode == require → 非信頼経路を除外
- trust_mode == prefer → 信頼経路を優先（除外はしない）
- trust_mode == off → フィルタなし

### 6.2 Phase 2: Scoring

各経路に対し、少なくとも以下を含むスコアを計算する。

```text
total_cost =
    base_cost
  + congestion_penalty
  + trust_penalty
  + availability_penalty
```

### 6.3 Phase 3: Best Path Selection

最も低コストの経路を Best Path とする。

### 6.4 Phase 4: Switching Decision

現在の Selected Path と比較する。

```text
if improvement > hysteresis_margin:
    SWITCH
else:
    KEEP
```

---

## 7. Decision Types

RCU は以下の決定を行う。

### 7.1 KEEP

現在の経路を維持する。

### 7.2 SWITCH

より良い経路へ切替する。

### 7.3 DEGRADED_SWITCH

制約下で利用可能な代替経路へ切替する。

### 7.4 ESCALATE

RCU 単体で判断できない場合、Resolver へ委譲する。

---

## 8. Degraded Mode

以下の場合、Degraded Mode に移行する。

- 有効な経路が存在しない
- trust 制約により経路が制限される
- 全体的な性能低下

Degraded Mode では：

- 制約を緩和した経路選択を行う
- 接続維持を優先する

---

## 9. Trust Handling

RCU における trust の扱い：

- trust は Telemetry からの参照情報とする
- trust_mode により挙動を変更する

例：

- off：無視
- prefer：優先
- require：必須

---

## 10. State Transition Considerations

RCU は状態遷移において以下を考慮する：

- hysteresis による振動抑制
- 一時的な変動の無視
- 回復の慎重な評価

---

## 11. Summary（まとめ）

RCU Model は：

- Telemetry と Routing Table を入力とし
- 経路を評価し
- 適切な経路選択および切替を行う

PSC Fabric の意思決定機構である。

RCU により PSC は：

- 安定性
- 適応性
- 説明可能性

を持つルーティングを実現する。
