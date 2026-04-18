# PSC Resolver Model v0.2（日本語版）


## ドキュメント情報

- ドキュメント名 : PSC Resolver Model
- バージョン     : v0.2
- プロジェクト   : PSC / Photon System Controller
- レイヤ         : PSCOS（制御層）
- ドキュメント種別 : 仕様書
- ステータス     : Draft
- 作成者         : T. Hirose
- 作成日         : 2026-03
- 最終更新       : 2026-04
- 言語           : 日本語

---

## 1. 目的

本ドキュメントは、PSC Fabric における Resolver モデルを定義する。

Resolver は、RCU の判断だけでは最終決定に十分でない場合に、
上位レベルの意思決定を行う。

Resolver の役割は以下の通り：

- RCUでは扱えない高度なルーティング判断の処理
- 複数条件間の競合解決
- 劣化経路（degraded）の利用判断
- policy・trust・recovery条件の統合

Resolver は PSC Fabric における **上位意思決定レイヤ** を構成する。

---

## 2. スコープ

本モデルは以下を定義する：

- Resolver の責務
- 起動条件
- 入力構造
- 出力構造
- 判断対象
- RCUとの関係

本ドキュメントは以下を含まない：

- RCUの通常ルーティングロジック
- Routing Table構造
- Telemetry生成
- 実データ転送
- AI推論実装

---

## 3. 設計原則

### 3.1 責務分離

- Telemetry：状態生成
- Routing Table：状態保持
- RCU：通常判断
- Resolver：上位意思決定

Resolver は RCU を置き換えるものではない。
RCUの判断が最終決定として不十分な場合に起動される。

これには以下を含む：

- RCUが有効な判断を出せない場合
- RCUの暫定判断が曖昧な場合
- 評価基準間に競合が存在する場合

Resolver は仲裁を行い、最終決定を生成する。

### 3.2 条件付き起動

Resolver は常時動作するのではなく、必要時のみ起動される。

### 3.3 多要素判断

Resolver は以下を統合する：

- congestion
- health
- availability
- trust
- policy
- recovery条件

### 3.4 説明可能性

Resolver の全ての判断は説明可能でなければならない。

---

## 4. Resolver 起動条件

Resolver は以下の条件で起動される。

### 4.1 有効経路なし

RCUが有効な経路を選択できない場合。

例：

- 全候補が UNAVAILABLE
- trust_mode=require により全候補が除外
- degraded候補が存在しない

### 4.2 ポリシー競合

複数のポリシーが衝突し、RCUでは解決できない場合。

例：

- latency と trust の優先順位競合
- stability と failover の緊急性競合

### 4.3 曖昧または競合する候補集合

候補評価が曖昧または競合している場合に起動される。

典型条件：

- `score_gap < epsilon`
- trust差が大きい
- stability差が大きい
- return評価とbaseline評価の乖離

例：

- `return_score` と `final_score` が異なる候補を選択
- スコアは近いが trust が異なる
- スコアは近いが stability が異なる

### 4.4 劣化経路判断

制約付き経路（RESTRICTED / trust制限）の使用可否判断が必要な場合。

### 4.5 Recovery復帰仲裁

復帰候補が有効になったが、最終切替が曖昧な場合。

---

## 5. Resolver入力

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

## 6. Resolver出力

```text
ResolverDecision {
    final_decision_type
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

## 7. 判断対象

### 7.1 経路選択上書き

RCUの暫定判断を上書きするかを決定する。

### 7.2 劣化経路許可

制約付き経路の使用可否を決定する。

### 7.3 経路なし判定

有効な経路が存在しないかを決定する。

### 7.4 Recovery復帰仲裁

復帰候補を選択するか、現状維持するかを決定する。

前提：

```text
RETURN_ELIGIBLE ≠ RETURN_SWITCH
```

---

## 8. 判断タイプ

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

### 8.1 各判断タイプの定義

#### KEEP

現在の経路を維持する

#### SWITCH

より適切な経路へ切り替える

#### DEGRADED_SWITCH

制約付き経路へ切り替える

#### NO_ROUTE

経路が存在しない

#### HOLD

状態を一時保持する

#### RETURN

元の経路へ復帰する

---

## 9. 判断モデル

Resolver は以下のステップで最終判断を決定する。

### 9.1 エスカレーション理由検証

RCUから渡されたエスカレーション理由を検証する。

対象：

- 有効経路なし
- ポリシー競合
- 曖昧な候補
- 劣化判断要求
- Recovery判断要求

この理由により、評価モードが決定される。

### 9.2 候補再評価

候補経路を再評価する。

評価項目：

- availability_state
- trust制約
- degraded許可
- recovery条件
- telemetry信頼度

---

### 9.3 曖昧性／競合検出

RCUの暫定結果が最終判断として不十分かを判定する。

典型指標：

- 小さい `score_gap`
- 大きい `trust_gap`
- 大きい `stability_gap`
- baseline評価とrecovery評価の乖離

曖昧または競合が検出された場合、Resolver が仲裁を行う。

### 9.4 ポリシー解決

ポリシー間の競合を解決し、優先順位を決定する。

例：

- trust優先
- latency優先
- stability優先
- 接続性優先

必要に応じて：

- degradedモード許可
- trust制約緩和
- recovery遅延

### 9.5 最終決定

ResolverDecisionType のいずれかを選択する。

### 9.6 出力構築

最終的な決定結果を構築する。

```text
ResolverDecision {
    final_decision_type
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

## 10. Trust と Policy の扱い

Resolver は trust と policy を最終制約として扱う。

例：

- trust_mode=require の厳格適用
- degraded時の trust例外許可
- 高優先度通信における policy override
- recovery時の stability優先

---

## 11. Recovery考慮

```text
RETURN_ELIGIBLE ≠ RETURN
```

復帰可能であっても即時復帰は保証されない。

また：

- recovery検証と最終切替は別フェーズである
- 最終復帰は競合仲裁により上書きされる可能性がある

---

## 12. 説明可能性

Resolver は以下を説明可能でなければならない：

- なぜRCUの判断が不十分だったのか
- なぜその経路が選択されたのか
- なぜdegraded経路が許可されたのか
- なぜ復帰が保持または実行されたのか

---

## 13. まとめ

Resolver モデルは：

- RCUからエスカレーションされた判断を受け取り
- policy / trust / telemetry / recovery条件を統合し
- 最終的な高レベル意思決定を行う

Resolver により：

- 通常判断は高速に（RCU）
- 高度判断は柔軟に（Resolver）

---

## 14. Resolver拡張（v0.2.x）

コア原則：

```text
RCU tentative decision ≠ Resolver final decision
```

関連原則：

```text
RETURN_ELIGIBLE ≠ RETURN_SWITCH
RETURN_SWITCH ≠ FINAL_DECISION
```
---