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

本ドキュメントは PSC Fabric における Telemetry 機構を定義する。

PSC は Fabric-centric distributed computer architecture を採用しており、
Fabric の状態観測および運用監視は Telemetry によって実現される。

Telemetry Model は以下を定義する。

- Fabric 状態の観測方法
- Telemetry 情報の種類
- Telemetry の利用目的
- Control Plane との関係

Telemetry は PSC Fabric の **観測機構（Observation System）**として機能する。

---

## 2. Scope（適用範囲）

本ドキュメントは以下を対象とする。

- PSC Fabric における Telemetry 情報の概念
- Telemetry 情報の分類
- Telemetry と Control Plane の関係

以下は本仕様の対象外とする。

- Telemetry データフォーマット
- Telemetry 転送プロトコル
- Telemetry データ保存方式

これらは別仕様書で定義する。

---

## 3. Design Principles（設計原則）

PSC Telemetry は以下の設計原則に基づく。

## 3.1 Observability

PSC Fabric は Telemetry により
Fabric の状態を観測可能とする。

## 3.2 Low Overhead

Telemetry は Fabric 動作に影響を与えないよう
低オーバーヘッドで動作する。

## 3.3 Distributed Collection

Telemetry 情報は
Fabric 内の各ノードで収集される。

## 3.4 Scalability

Telemetry は
小規模システムから大規模 Fabric まで
スケール可能な設計とする。

---

## 4. Telemetry Overview（Telemetry概要）

PSC Fabric の Telemetry は
Fabric の状態情報を収集する仕組みである。

Telemetry は主に以下の目的で使用される。

- Fabric 状態監視
- Control Plane の観測入力
- 運用監視
- 障害検出

Telemetry は PSC Fabric の観測基盤として機能する。

---

## 5. Telemetry Sources（Telemetry情報源）

Telemetry 情報は
PSC Fabric 内の各ノードから生成される。

主な Telemetry Source

- Compute Node
- Memory Node
- Storage Node
- Fabric Node
- Gateway Node

各ノードは
自身の状態および Fabric 状態に関する情報を生成する。

---

## 6. Telemetry Information Types（Telemetry情報種類）

Telemetry 情報は以下の種類を含む。

例

- Link Status
- Node Status
- Traffic Statistics
- Congestion Indicators
- Error Events

これらの情報により
PSC Fabric の状態が観測可能となる。

---

## 7. Telemetry Flow（Telemetryフロー）

Telemetry 情報は
Fabric 内で収集および利用される。

基本的な流れ

Node Telemetry
↓
Telemetry Collection
↓
Control Plane Observation
↓
Fabric Control Decision

Telemetry は Control Plane の
観測入力として使用される。

---

## 8. Telemetry and Control Plane（Control Plane連携）

Telemetry は Control Plane の
観測機構として機能する。

Control Plane は Telemetry 情報を使用して

- Fabric 状態分析
- Routing 調整
- 混雑制御
- 障害対応

を行う。

---

## 9. Telemetry and Management Plane（Management Plane連携）

Telemetry は Management Plane による
運用監視にも使用される。

例

- Fabric 監視
- パフォーマンス分析
- 障害診断
- 運用ログ

Management Plane は Telemetry を用いて
Fabric の運用状態を把握する。

---

## 10. Summary（まとめ）

PSC Telemetry Model は
PSC Fabric の観測機構を定義する。

Telemetry は

- Fabric 状態観測
- Control Plane の観測入力
- Management Plane の監視基盤

として機能する。

Telemetry により PSC Fabric は
観測可能で適応可能な分散システムを実現する。

---
