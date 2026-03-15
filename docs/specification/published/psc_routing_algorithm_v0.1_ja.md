# PSC ルーティングアルゴリズム仕様 v0.1

## Document Information

- ドキュメント名: PSC Routing Algorithm
- プロジェクト : PSC / Photon System Controller
- レイヤ : PSC Fabric
- ドキュメント種別 : 仕様書
- ステータス : Draft
- 作成者 : T. Hirose
- 作成日 : 2026-03
- 最終更新 : 2026-03
- 言語 : Japanese

---

## 1. 目的

本ドキュメントは PSC Fabric において
RCU（Routing Control Unit）が使用する
ルーティングアルゴリズムを定義する。

本仕様で定義するルーティングアルゴリズムは、
単純な最短経路選択ではなく、Fabric 状態、混雑度、ポリシー、信頼性、および障害状況を考慮しながら
安定性を優先して経路を決定するための判断規則である。

本仕様では主に以下を扱う。

- Routing decision logic
- Route scoring
- Congestion-aware routing
- Policy-aware routing
- Trust-aware routing
- Failover decision
- Adaptive routing
- Fabric state interaction

---

## 2. 適用範囲

本仕様は PSC Fabric における
ノード間転送のための ルート選定ロジック を対象とする。

本仕様には以下を含む。

- 候補ルートの評価方法
- ルートスコアの算出方針
- Fabric 状態に応じたルーティング制御
- 混雑・障害・信頼性に応じた経路切替
- ポリシー制約を考慮したルート選択

本仕様には以下を含まない。

- ルーティングテーブルの物理保存形式
- アドレス形式の詳細
- パケット構造の詳細
- 転送フロー全体の詳細
- 暗号鍵管理の詳細

これらは別仕様で定義する。

---

## 3. 設計思想

PSC Routing Algorithm は、
高スループットのみを目的とした数値最適化型アルゴリズムではなく、
安定・継続・制御可能性を優先する状態ベース型ルーティングとして設計する。

基本思想は以下の通りである。

### 3.1 Stability First

ルーティングは、瞬間的な最短性能よりも
Fabric 全体の安定性を優先する。

### 3.2 State-aware Routing

ルーティング判断は、リンク単体の状態だけでなく
Fabric 全体の状態（CALM / WARM / HOT / EMERGENCY）を考慮する。

### 3.3 Policy-constrained Routing

利用可能なルートであっても、
セキュリティ・分離・優先度・帯域予約などのポリシーに反する場合は選択しない。

### 3.4 Trust-weighted Routing

リンクやノードの信頼度は
ルート選択に直接影響する。

### 3.5 Graceful Degradation

障害や混雑が発生した場合でも
完全停止ではなく、可能な範囲で機能を維持する方向でルーティングを行う。

### 3.6 Hysteresis-based Switching

ルート切替は頻繁に揺れ動かないよう、
ヒステリシスを持たせて安定化する。

### 3.7 Single-active-route 原則

PSC Routing Algorithm v0.1 では **単一アクティブルート方式** を採用する。

RCU は各転送に対して 1 本のプライマリルートを選択し、
そのルートを用いてデータ転送を行う。

Fabric 状態変化に伴う制御複雑化やルーティング振動を抑えるため、
本バージョンではマルチパスルーティングは採用しない。

ただし、フェイルオーバに備えて **バックアップルート候補** を保持することは許可される。

これらのバックアップルートは同時トラフィック分散には使用されず、
アクティブルートが利用不能または劣化した場合の高速フェイルオーバのために予約される。

マルチパスルーティングは将来の PSC Fabric 拡張として導入される可能性がある。

---

## 4. ルーティング目的

PSC Routing Algorithm の目的は以下の通りである。

- 送信元から宛先までの有効ルートを選定する
- Fabric の混雑集中を緩和する
- 障害リンク・障害ノードを回避する
- セキュリティポリシーに適合する経路のみを選ぶ
- 信頼性の高い経路を優先する
- Fabric 状態に応じて安全側に制御する
- 経路切替の振動を抑制する

---

## 5. ルーティング判断モデル (Routing Decision Model)

PSC ではルーティング判断を
以下の多段階モデルで実施する。

### 5.1 Decision Stages

- Candidate Route Discovery
- Route Eligibility Check
- Route Scoring
- Route Ranking
- Route Selection
- Route Lock / Hold
- Re-evaluation Trigger

### 5.2 Candidate Route Discovery

RCU はルーティングテーブルおよび Fabric 状態情報を参照し、
送信元ノードから宛先ノードまで到達可能な候補ルートを抽出する。

候補ルート抽出時には以下を考慮する。

- 到達可能性
- Hop 数
- 中継ノード種別
- 使用可能リンク
- Fabric 状態
- Policy 制約
- 障害情報

### 5.3 Route Eligibility Check

抽出された候補ルートに対して、
以下の条件を満たすルートのみを有効候補とする。

- リンク状態が利用可能である
- 中継ノードがルーティング許可状態である
- Security Policy に違反しない
- 宛先まで論理的に到達可能である
- EMERGENCY 制限対象に該当しない

### 5.4 Route Scoring

有効候補ルートには
複数要素に基づくスコアを付与する。

### 5.5 Route Ranking

候補ルートをスコア順に並べる。

### 5.6 Route Selection

最上位ルートを基本選択とするが、
ヒステリシス条件、保持時間、現在使用中ルートとの差分を考慮して
実際の切替可否を判定する。

### 5.7 Route Lock / Hold

一度選択したルートは一定期間保持し、
軽微なスコア変動だけでは切替しない。

### 5.8 Re-evaluation Trigger

以下の条件で再評価を行う。

- リンク障害発生
- ノード障害発生
- 混雑度しきい値超過
- Fabric State 変化
- Security Policy 更新
- Trust Score 低下
- 一定周期タイマ満了

---

## 6. ルートスコアモデル

各候補ルートには、複数の評価要素をもとに
総合スコアを付与する。

### 6.1 Score Components

ルートスコアは以下の要素で構成される。

- Base Reachability Score
- Hop Count Penalty
- Congestion Penalty
- Reliability Bonus / Penalty
- Trust Bonus / Penalty
- Policy Fitness Modifier
- Fabric State Modifier
- Failover Penalty
- Stability Bonus

### 6.2 Basic Concept

スコアは以下の考え方で設計する。

- 到達可能であることが最優先
- Hop 数は少ない方が望ましい
- 混雑リンクを含むルートは減点
- 信頼性の高いリンクは加点
- 信頼度の低いノードやリンクは減点
- ポリシー適合ルートを優先
- 障害回避直後の不安定ルートは慎重に扱う
- 現在ルートが十分良好なら保持を優先

### 6.3 Abstract Formula

概念式は以下の通りである。

RouteScore =
  Reachability
  - HopPenalty
  - CongestionPenalty
  ± ReliabilityAdjustment
  ± TrustAdjustment
  + PolicyAdjustment
  + FabricStateAdjustment
  - FailoverPenalty
  + StabilityBonus

本バージョンでは概念モデルのみを定義し、
具体的な係数値は実装依存または将来仕様で定義する。

---

## 7. 混雑考慮ルーティング

### 7.1 Purpose

混雑が一部リンクや一部ノードに集中した場合、
PSC はトラフィックを分散し、Fabric 全体の安定性を維持する。

### 7.2 Congestion Inputs

混雑評価には以下の情報を利用できる。

- リンク利用率
- バッファ占有率
- キュー長
- 再送増加傾向
- クレジット不足頻度
- 遅延増大傾向
- Telemetry / Fault Monitor からの輻輳通知

### 7.3 Congestion Response

混雑が検出された場合、RCU は以下を行う。

- 混雑リンクを含むルートの減点
- 代替ルートの再評価
- 非優先トラフィックの遠回り許容
- 高優先トラフィックの保護
- HOT / EMERGENCY では安全側制御を強化

### 7.4 Localized vs Fabric-wide Congestion

局所混雑とFabric 全体の広域混雑を区別する。

- 局所混雑  
  特定リンクや特定区間のみ減点する

- 広域混雑  
  Fabric 全体で積極的な負荷抑制モードへ移行する

---

## 8. ポリシー考慮ルーティング

### 8.1 Purpose

ルートは到達可能であっても、
Security Policy や運用ポリシーに反する場合は選択してはならない。

### 8.2 Policy Examples

考慮対象となるポリシー例は以下の通りである。

- ノード間通信許可 / 禁止
- セキュリティゾーン分離
- 優先通信の専用経路
- 帯域予約経路
- 特定リンクの利用制限
- 特定ノード経由禁止
- 管理トラフィックの優先経路
- 障害時限定ルートの使用条件

### 8.3 Policy Enforcement Rule

ポリシー違反ルートは
スコア低下ではなく 原則として除外 とする。

ただし、EMERGENCY 状態で明示的に許可された例外ポリシーがある場合のみ、
限定的に使用可能とする。

---

## 9. 信頼性考慮ルーティング

### 9.1 Purpose

PSC はリンクやノードの状態を単なる Up / Down で扱わず、
信頼度の連続的評価 を用いてより安定した経路選択を行う。

### 9.2 Trust Factors

Trust 評価には以下を利用できる。

- エラー率
- CRC / integrity error 発生頻度
- リンク再訓練頻度
- 過去の断続障害履歴
- 遅延のばらつき
- ノード健全性情報
- セキュリティ警告
- OMU による光品質低下通知

### 9.3 Trust Handling

高 Trust のリンク / ノードを優先する

低 Trust のリンク / ノードを含むルートは減点する

Trust がしきい値を下回る場合は候補除外可能とする

断続障害中の経路は Failover 後もしばらく慎重に扱う

---

## 10. フェイルオーバ判断

### 10.1 Purpose

使用中ルートに障害または重大劣化が発生した場合、
PSC は速やかに代替ルートへ切替える。

### 10.2 Failover Triggers

フェイルオーバの主なトリガは以下の通りである。

- Link Down
- Node Unreachable
- Error burst
- Trust collapse
- Severe congestion
- Policy invalidation
- Fabric State escalation

### 10.3 Failover Behavior

フェイルオーバ時は以下を原則とする。

- 現在ルートを失効または劣化判定する
- 代替候補ルートを再評価する
- 最上位安全ルートを選択する
- 必要に応じて転送レートや優先度を調整する
- 状態安定まで過度な再切替を防ぐ

### 10.4 Failover Classes

フェイルオーバは以下の分類を持つ。

Soft Failover
- 軽度混雑や品質低下による再選定

Hard Failover
- リンク断やノード障害による即時切替

Emergency Failover
- Fabric 全体保護のための強制迂回または通信制限

---

## 11. 適応型ルーティング

### 11.1 Purpose

PSC は静的ルーティングだけでなく、
Fabric 状態の変化に応じてルート選択を適応的に変化させる。

### 11.2 Adaptation Principle

ただし、PSC の適応は
過敏なリアルタイム最適化ではなく、
安定化を前提とした緩やかな適応 とする。

### 11.3 Adaptive Inputs

混雑傾向

エラー傾向

Fabric State

トラフィック種別

ノード重要度

Policy 更新

Trust 履歴

### 11.4 Adaptation Constraints

適応制御には以下の制約を設ける。

ルート変更頻度制限

最小保持時間

状態遷移ヒステリシス

EMERGENCY 時の自由度制限

管理トラフィックの保護

---

## 12. Fabric 状態連動

PSC Routing Algorithm は
Fabric State Model と密接に連携する。

### 12.1 CALM

通常安定状態。

通常スコアリングを使用

効率と安定性のバランスをとる

軽微な負荷分散を許可

### 12.2 WARM

負荷上昇または軽度異常状態。

混雑ペナルティを強める

Trust の重みを増やす

不安定リンクを避け始める

ルート再評価頻度を上げる

### 12.3 HOT

高負荷または異常拡大状態。

安定ルート優先

低優先トラフィックを遠回りまたは抑制

リスクの高いリンクを強く回避

Failover に備えた予備ルート確保を強化

### 12.4 EMERGENCY

重大障害または保護優先状態。

生存性最優先

Policy 例外は明示許可のみ

高優先通信のみ維持可能

低信頼ルートは原則除外

ルート選択自由度を縮小し安全側へ固定する

---

## 13. ルート安定化制御

### 13.1 Need for Stability Control

ルートスコアが短時間で揺れると
頻繁な経路切替によりかえって Fabric が不安定化する。

### 13.2 Stability Measures

そのため PSC では以下を導入する。

- Minimum Route Hold Time
- Score Improvement Threshold
- Switch Cooldown Timer
- Recovery Observation Window
- Hysteresis Margin

### 13.3 Switching Rule

新ルート候補が存在しても、
以下の条件を満たさない限り切替しない。

現行ルートが失効した

新ルートが明確に優位である

安全性上ただちに切替が必要

Hold Time が満了している

---

## 14. 他モジュールとの連携

### 14.1 Resolver

転送意図や優先度を提供する

Routing 再評価要求を発行できる

### 14.2 Scheduler

トラフィック優先度や割当方針を提供する

経路選択後の実行順序に影響する

### 14.3 SPU

セキュリティポリシー検査を行う

禁止経路を除外する

### 14.4 TMU

転送単位やチャンク特性を提供する

転送継続性に応じたルート保持を支援する

### 14.5 TEU

実行時の転送結果をフィードバックする

実ルート品質情報を返す

### 14.6 OMU

光品質、リンク劣化、警告情報を提供する

### 14.7 Telemetry / Fault Monitor

混雑・障害・劣化・異常傾向を集約し、RCU に通知する

---

## 15. 高レベル疑似コード

```text
function select_route(source, destination, transfer_context):

    candidates = discover_routes(source, destination)

    eligible_routes = []
    for route in candidates:
        if not is_reachable(route):
            continue
        if not policy_allows(route, transfer_context):
            continue
        if not fabric_state_allows(route):
            continue
        eligible_routes.append(route)

    if eligible_routes is empty:
        return NO_ROUTE

    for route in eligible_routes:
        route.score = evaluate_route_score(route, transfer_context)

    ranked_routes = sort_by_score_descending(eligible_routes)

    best_route = ranked_routes[0]

    if should_keep_current_route(best_route) == true:
        return current_route
    else:
        return best_route
```

---
        
## 16. 本仕様の非目標

本バージョンでは以下は未定義とする。

- 数式係数の厳密値
- 学習型最適化の導入
- 分散ルーティング制御プロトコル詳細
- 大規模 Fabric での経路計算分散方式
- マルチパス転送の詳細仕様
- QoS クラス定義の完全版

これらは将来バージョンで拡張する。

---

## 17. 今後の拡張候補

- Multi-path routing
- Predictive congestion avoidance
- Learning-assisted scoring
- Hierarchical routing domains
- Topology-aware large-scale route aggregation
- Trust decay / recovery model
- Fabric-wide reroute coordination

---

## 18. まとめ

PSC Routing Algorithm は、
PSC Fabric における経路選択を
単純な最短経路問題ではなく、
Fabric 安定性・混雑・信頼性・ポリシー・障害回避を統合した制御問題として扱う。

本仕様 v0.1 では、
Routing decision logic、Route scoring、Congestion-aware routing、Policy-aware routing、Trust-aware routing、Failover decision、Adaptive routing、Fabric state interaction の
基本構造を定義した。

今後は本仕様をもとに
係数モデル、状態遷移条件、ルート保持条件、マルチパス制御などを拡張していく。
