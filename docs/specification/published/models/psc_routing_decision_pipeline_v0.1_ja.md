# PSC ルーティング決定パイプライン仕様 v0.1

## ドキュメント情報

- ドキュメント名   : PSC Routing Decision Pipeline
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

本ドキュメントは PSC Fabric における
**Routing Decision Pipeline（ルーティング決定パイプライン）**を定義する。

Routing Decision Pipeline は
RCU（Routing Control Unit）が 転送経路を決定する際の判断処理の流れを定義する。

PSC におけるルーティングは単純な最短経路選択ではなく、

- Fabric 状態
- 混雑状況
- ポリシー
- セキュリティ
- 信頼性

などの複数要素を考慮した 多段階判断モデルとして設計される。

本仕様では

- ルーティング判断の入力
- 判断パイプライン
- 経路評価
- 最終ルート選択

を定義する。

---

## 2. Scope（適用範囲）

本仕様は以下を対象とする。

対象：

- PSC Fabric 内のルーティング判断
- RCU による経路決定処理

対象外：

- Routing Table の構造（PSC Routing Table Model）
- Routing Algorithm の詳細
- Congestion Control の詳細

それらは別仕様で定義される。

---

## 3. Routing Decision Concept（ルーティング決定概念）

PSC のルーティング判断は
段階的評価パイプラインとして実行される。

基本構造：
```
Packet / Transfer Request
        ↓
Routing Context Construction
        ↓
Policy Evaluation
        ↓
Security Validation
        ↓
Congestion Evaluation
        ↓
Routing Table Lookup
        ↓
Route Scoring
        ↓
Final Route Selection
```
この構造により PSC は

- 柔軟なルーティング制御
- Fabric 状態への適応
- 政策・信頼・混雑の統合制御

を実現する。

---

## 4. Decision Inputs（入力情報）

Routing Decision Pipeline は
以下の情報を入力として使用する。

### 4.1 Packet Information

パケットヘッダ情報：

- Destination Address
- Source Address
- Packet Type
- Transfer Class
- Priority

### 4.2 Routing Context

RCU はルーティング判断前に
Routing Context を構築する。

Routing Context には以下が含まれる。

- Destination Node
- Source Node
- Current Node
- Transfer Type
- Priority Level

### 4.3 Fabric State

Fabric の状態情報：

- Fabric Load
- Link State
- Node State
- Failure Status

これらは Telemetry Model により取得される。

### 4.4 Policy Information

Policy Model に基づく制御情報：

例：

- 許可ノード
- 禁止ノード
- 優先経路
- QoS ポリシー

### 4.5 Security Information

Security Model に基づく情報：

例：

- Trust Level
- Node Authentication
- Security Domain

---

## 5. Decision Pipeline Stages（判断パイプライン）

Routing Decision Pipeline は
以下の段階で処理を行う。

### 5.1 Routing Context Construction

RCU はパケット情報から
Routing Context を生成する。

ここでは

- 宛先
- 転送タイプ
- 優先度

などが整理される。

### 5.2 Policy Evaluation

Policy Engine により
ポリシー制御が適用される。

例：

- 禁止ルートの除外
- 優先ルート指定
- QoS 制御

### 5.3 Security Validation

Security Model に基づき

- Trust Domain
- Security Policy
- Access Control

が確認される。

不正な経路は除外される。

### 5.4 Congestion Evaluation

Fabric Telemetry を参照し
混雑状態を評価する。

評価対象：

- Link Load
- Node Load
- Queue Depth

混雑度の高い経路は
優先度が低下する。

### 5.5 Routing Table Lookup

Routing Table を参照し
候補経路セット（Candidate Routes） を取得する。

Routing Table Model により
以下が取得される。

- Next Hop
- Path Cost
- Route Attributes

### 5.6 Route Scoring

各候補経路に対して
スコアリングを行う。

評価要素例：

- Path Cost
- Congestion Level
- Policy Priority
- Trust Level
- Reliability

スコアは
Routing Algorithm で定義されたスコアリング方法に基づいて計算される

### 5.7 Final Route Selection

スコアリング結果から
最適経路を決定する。

選択方法例：

- Best Score Selection
- Weighted Random
- Load Distribution

最終的な Next Hop が決定される。

決定された Next Hop は
転送実行層（Transfer Execution Layer）へ通知される。

---

## 6. Interaction with Fabric Control（Fabric制御連携）

Routing Decision Pipeline は
Fabric Control と連携する。

関係モジュール：

- Fabric State Model
- Congestion Control Model
- Telemetry Model
- Policy Model
- Security Model

これらの情報を統合することで
PSC は 適応型ルーティング制御を実現する。

---

## 7. Fault Handling（障害処理）

障害発生時：

- Link Failure
- Node Failure
- Fabric Partition

RCU は

- 該当経路の除外
- 代替経路選択
- Routing Table 更新

を実施する。

---

## 8. Future Extension（将来拡張）

将来的には以下の拡張が考えられる。

- AI / Learning based routing
- Dynamic policy adaptation
- Predictive congestion avoidance
- Multi-path routing optimization
