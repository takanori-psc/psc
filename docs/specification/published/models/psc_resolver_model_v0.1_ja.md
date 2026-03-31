# PSC Resolver Model v0.1

## ドキュメント情報

- ドキュメント名   : PSC Resolver Model
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

本ドキュメントは、PSC Fabric における Resolver Model を定義する。

Resolver は、RCU が単独では有効な経路判断を確定できない場合に、
複数の制約条件・状態情報・方針を統合して上位判断を行う。

Resolver は以下を目的とする。

- RCU では解決できない例外的な経路判断を扱う
- 複数の競合条件を統合して最終判断を行う
- degraded fallback の可否を判断する
- policy / trust / recovery 条件を含む高次判断を行う

Resolver は PSC Fabric における**上位意思決定層**である。

---

## 2. Scope（適用範囲）

本モデルは以下を定義する。

- Resolver の責務
- 起動条件
- 入力構造
- 出力構造
- 判断対象
- Resolver と RCU の関係

以下は対象外とする。

- RCU の通常経路選択ロジック
- Routing Table の構造定義
- Telemetry の生成方式
- 物理転送処理
- AI 推論実装の詳細

---

## 3. Design Principles（設計原則）

### 3.1 Separation of Responsibilities

- Telemetry：状態生成
- Routing Table：状態保持
- RCU：通常の経路判断
- Resolver：例外時の上位判断

Resolver は通常経路選択の代替ではなく、
RCU で解決困難な条件に対してのみ介入する。

### 3.2 Exceptional Invocation

Resolver は常時介入せず、必要時のみ起動される。

### 3.3 Multi-factor Decision

Resolver は単一指標ではなく、以下を統合して判断する。

- congestion
- health
- availability
- trust
- policy
- recovery condition

### 3.4 Explainability

Resolver の判断は説明可能であり、
判断理由を出力可能でなければならない。

---

## 4. Resolver Invocation Conditions

Resolver は以下の条件で起動される。

### 4.1 No Valid Path

RCU が有効な経路を選択できない場合。

例：

- 全候補が UNAVAILABLE
- trust_mode=require により候補消滅
- degraded candidate も存在しない

### 4.2 Policy Conflict

複数の policy 条件が競合し、
RCU の単純スコアリングでは優劣を決定できない場合。

例：

- latency 優先と trust 優先の衝突
- stability 優先と failover 必要性の衝突

### 4.3 Ambiguous Best Candidate

複数候補が近接しており、
RCU が有意差を確定できない場合。

### 4.4 Degraded Fallback Decision

RESTRICTED 経路または trust 制約付き経路を
利用すべきか判断が必要な場合。

### 4.5 Recovery Decision

障害・劣化からの回復時に、
元の経路へ復帰すべきか、現経路を維持すべきか判断が必要な場合。

---

## 5. Resolver Inputs

Resolver は以下の入力を受け取る。

### 5.1 Transfer Request

```text
TransferRequest {
    src
    dst
    class
    qos
    deadline
}
```

### 5.2 Candidate Paths

```text
ResolverCandidatePath {
    path_id
    hops[]
    link_ids[]
    node_ids[]
    base_cost
    estimated_cost
    current_rank
}
```

### 5.3 Telemetry Summary

```text
ResolverTelemetrySummary {
    congestion_score
    health_state
    availability_state
    trust_score_ref
    scope_level
    confidence
}
```

### 5.4 Routing Policy

```text
ResolverPolicyContext {
    mode
    hysteresis_margin
    trust_mode
    degraded_mode_allowed
    recovery_preference
}
```

### 5.5 RCU Context

```text
ResolverRCUContext {
    selected_path_id
    best_path_id
    tentative_decision
    escalation_reason
}
```

---

## 6. Resolver Outputs

Resolver は以下を出力する。

```text
ResolverDecision {
    final_decision_type   // ResolverDecisionType
    selected_path_id
    rationale {
        type
        details
    }
    override_policy {
        degraded_mode
        trust_exception
        recovery_hold
    }
}
```

---

## 7. Decision Targets

Resolver は主に以下を判断対象とする。

### 7.1 Path Selection Override

RCU の暫定判断を上書きし、別経路を最終選択すべきかを判断する。

### 7.2 Degraded Path Approval

通常時には選択されない制約付き経路を、例外的に許可すべきかを判断する。

### 7.3 No-route Determination

有効経路が存在しない場合に、経路確立不能として扱うべきかを判断する。

### 7.4 Recovery Hold / Return

回復時において、元経路へ戻すべきか、現経路を維持すべきかを判断する。

---

## 8. Resolver Decision Types

Resolver は以下の決定タイプを持つ。

```text
ResolverDecisionType {
    KEEP
    SWITCH
    DEGRADED_SWITCH
    NO_ROUTE
    HOLD
    RETURN
}
```

### 8.1 Decision Type Definitions

### 8.1.1 KEEP

現在の Selected Path を維持する。

### 8.1.2 SWITCH

より適切な経路へ切替する。

### 8.1.3 DEGRADED_SWITCH

制約付き（RESTRICTED または trust 制約）の経路へ切替する。

### 8.1.4 NO_ROUTE

有効な経路が存在せず、経路確立不能と判断する。

### 8.1.5 HOLD

回復可能性がある場合に、即時切替や復帰を行わず現状態を維持する。

### 8.1.6 RETURN

回復が確認された場合に、元の経路へ復帰する。

---

## 9. Decision Model

Resolver は以下の手順で最終判断を行う。

### 9.1 Validate Escalation Reason

RCU からの委譲理由を確認する。

- No valid path
- Policy conflict
- Ambiguous candidate
- Degraded decision required
- Recovery decision required

委譲理由に基づき、適用すべき判断モードを決定する。

### 9.2 Re-evaluate Candidate Set

候補経路を再評価する。

評価対象：

- availability_state
- trust 制約
- degraded 許容性
- recovery 状態
- telemetry の信頼度（confidence）

### 9.3 Apply Policy Resolution

競合する policy 条件を統合し、優先順位を決定する。

例：

- trust 優先
- latency 優先
- stability 優先
- connectivity（接続維持）優先

必要に応じて：

- degraded mode の許可
- trust 制約の緩和
- recovery の遅延

を判断する。

### 9.4 Determine Final Action

ResolverDecisionType のいずれかを最終決定する。

### 9.5 Output Construction

最終判断を以下の形式で出力する。

```text
ResolverDecision {
    final_decision_type   // ResolverDecisionType
    selected_path_id
    rationale {
        type
        details
    }
    override_policy {
        degraded_mode
        trust_exception
        recovery_hold
    }
}
```

---

## 10. Trust and Policy Handling

Resolver は trust および policy を
単なるペナルティではなく、最終制約条件として扱うことができる。

例：

- trust_mode=require の厳格適用
- degraded mode における trust 例外許可
- 高優先度 transfer に対する policy override
- recovery 中の安定性優先判断

---

## 11. Recovery Considerations

Resolver は回復判断において以下を考慮する。

- 一時的回復か持続的回復か
- 元経路の trust / health / congestion 状態
- 現在の selected path の安定性
- 復帰による振動リスク

Resolver は、
回復を検知しても即時復帰を強制しない。

---

## 12. Explainability Requirements

Resolver は少なくとも以下を説明可能でなければならない。

- なぜ RCU の判断では不十分だったか
- なぜその最終経路を選択したか
- なぜ degraded path を許可したか
- なぜ復帰を保留または実施したか

---

## 13. Summary（まとめ）

Resolver Model は、

- RCU から委譲された例外判断を受け取り
- policy / trust / telemetry / recovery 条件を統合し
- PSC Fabric の最終的な上位経路判断を行う

上位意思決定機構である。

Resolver により PSC は、

- 通常時の高速判断（RCU）
- 例外時の高次判断（Resolver）

を両立できる。
