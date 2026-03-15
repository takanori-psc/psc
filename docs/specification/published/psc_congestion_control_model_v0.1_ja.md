# PSC Congestion Control Model v0.1

## ドキュメント情報

- ドキュメント名   : PSC Congestion Control Model
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

## 1. 目的

本ドキュメントは PSC Fabric における **Congestion Control Model（輻輳制御モデル）** を定義する。

Congestion Control Model は、PSC Fabric 内で発生する輻輳を検出・表現・通知・緩和する方法を定義する。

これにより PSC は以下を維持する。

- 安定したパケット転送
- 予測可能なレイテンシ挙動
- 公平なリソース利用
- ルーティングの適応性
- Fabric 全体の信頼性

本モデルは PSC ノードおよび制御要素が使用する  
**論理的な輻輳処理フレームワーク**を定義する。

---

## 2. 適用範囲

本仕様は以下の輻輳制御要素を対象とする。

- 輻輳検出
- 輻輳状態表現
- 輻輳通知
- 輻輳時のルーティング適応
- フロー制御メカニズム
- Fabric安定化メカニズム

本ドキュメントでは以下は定義しない。

- セキュリティ動作
- トラフィックポリシー
- Fabric管理操作

これらは別仕様で定義される。

---

## 3. 設計目標

PSC Congestion Control Model は以下の設計目標を持つ。

### 3.1 Fabric Stability

輻輳制御は **短期的な最大スループットより Fabric の安定性**を優先する。

### 3.2 Distributed Operation

PSC Fabric は **分散自律環境**で動作するため、  
輻輳処理は中央集権制御に依存してはならない。

### 3.3 Local-first Reaction

ノードは主に **ローカルに観測できる状態**に基づいて反応し、  
同時に Fabric 全体の安定性に貢献する。

### 3.4 Routing Cooperation

輻輳制御は PSC のルーティング機構と協調し、  
過負荷経路を回避できるようにする。

### 3.5 Lightweight Signaling

輻輳通知は **コンパクトで効率的**である必要がある。

### 3.6 Oscillation Avoidance

ヒステリシスやダンピング機構により  
ルート振動や不安定なフィードバックを防止する。

---

## 4. 輻輳概念

PSC は輻輳を **Fabricレベルの状態**として扱う。

輻輳はトラフィック要求が Fabric の転送能力を超えたときに発生する。

主な原因例：

- 出力ポート競合
- 経路集中
- 宛先側制約
- ノード内部リソース制限
- 障害によるトラフィック再ルーティング

PSC 輻輳制御は以下の原則に基づく。

- 輻輳を早期検出する
- 安定した状態表現を用いる
- 輻輳情報は限定的範囲で伝播する
- ルーティングは段階的に適応する
- 必要に応じて負荷を低減する
- 回復は慎重に行う

---

## 5. 輻輳観測ポイント

PSCノード内の複数の場所で輻輳が観測される。

### 5.1 Port-level Observation

ポートは以下を観測する。

- 出力キュー増加
- 送信延期の繰り返し
- リンク利用率飽和
- 転送完了率低下

### 5.2 Path-level Observation

ルーティング要素は以下から輻輳を推定できる。

- 下流からの輻輳報告
- 経路レイテンシ増加
- 経路性能低下
- パケット蓄積傾向

### 5.3 Node-level Observation

ノード内部輻輳は以下で検出される。

- 内部バッファ圧迫
- 転送スケジューリング滞留
- 転送エンジン遅延
- 内部リソース枯渇

### 5.4 Destination-side Observation

受信ノードは以下の場合に輻輳を通知できる。

- 受信バッファ枯渇
- ストレージ書き込み能力不足
- 処理能力低下

---

## 6. 輻輳状態モデル

PSC は **多段階輻輳状態モデル**を使用する。

### 6.1 Congestion States

- NORMAL  
  輻輳なし

- WATCH  
  輻輳兆候

- CONGESTED  
  転送効率低下

- SEVERE  
  深刻な輻輳

### 6.2 State Philosophy

PSC は数値最適化ではなく  
**状態ベース制御**を採用する。

### 6.3 State Transition Principles

状態遷移原則：

- 悪化は継続的圧力が必要
- 回復はより強い証拠が必要
- severeは持続的過負荷

---

## 7. 輻輳指標

状態判断には複数指標を使用する。

### 7.1 Primary Indicators

- キュー占有率
- キュー増加速度
- 送信停止時間
- 転送遅延
- 再送頻度
- バッファ圧力

### 7.2 Secondary Indicators

- 下流輻輳通知
- 経路バランス変化
- レイテンシ変動
- 宛先バックプレッシャ

### 7.3 Composite Evaluation

複数指標を組み合わせ  
最終的に輻輳状態へマッピングする。

---

## 8. 輻輳通知

輻輳情報はノード間で通知される。

### 8.1 Signaling Purpose

- 上流ノードへの通知
- 適応ルーティング
- トラフィック抑制
- Fabric安定化

### 8.2 Signaling Characteristics

通知は以下の特性を持つ。

- コンパクト
- イベント駆動または周期
- レート制限
- 状態変化なし時抑制
- ローカル範囲

### 8.3 Signaling Scope

通知対象：

- 上流ノード
- ルーティング制御
- Control Plane
- Telemetry

### 8.4 Signaling Granularity

通知粒度：

- port
- link
- path
- node
- destination

---

## 9. 輻輳時ルーティング動作

ルーティングは輻輳制御と協調する。

### 9.1 Basic Routing Reaction

- 輻輳経路の優先度低下
- 代替経路選択
- マルチパス分散
- 不安定経路回避

### 9.2 Gradual Adaptation

急激な経路変更は避ける。

### 9.3 Path Penalty

輻輳経路は一時的ペナルティを受ける。

### 9.4 Recovery Behavior

回復は慎重に行う。

---

## 10. フロー制御戦略

ルーティングだけでは不十分な場合がある。

### 10.1 Flow Control Purpose

過負荷伝播を防ぐ。

### 10.2 Flow Control Actions

- 転送ペーシング
- 同時転送数制限
- バースト制御
- 非重要トラフィック遅延
- 制御トラフィック優先

### 10.3 Receiver-aware Behavior

PSC は **receiver-driven transfer** を採用するため  
宛先準備状態を考慮する。

### 10.4 Control Traffic Protection

制御トラフィックは飢餓状態にならないよう保護する。

---

## 11. 安定化メカニズム

安定化メカニズム。

### 11.1 Hysteresis

異なる閾値を使用する。

### 11.2 Persistence Timers

状態遷移に最低持続時間。

### 11.3 Rate Limiting

通知と経路変更を制限。

### 11.4 Damping

反応後は観測待ち。

### 11.5 Local-first Mitigation

まずローカル対処。

---

## 12. 他PSCモデルとの関係

関連仕様：

- PSC Fabric State Model
- PSC Routing Model
- PSC Routing Table Model
- PSC Routing Algorithm
- PSC Routing Decision Pipeline
- PSC Control Plane Model
- PSC Telemetry Model

---

## 13. 将来拡張

- 数値閾値モデル
- クラス別輻輳制御
- ポリシー連携
- フェアネス
- admission control
- hierarchical congestion domain
- multi-fabric coordination

---

## 14. まとめ

PSC Congestion Control Model は  
PSC Fabric の分散輻輳制御フレームワークを定義する。

主要原則：

- 早期検出
- 状態ベース制御
- 制御通知
- ルーティング協調
- 適応フロー制御
- ヒステリシス回復

これにより PSC Fabric は  
**中央集権制御なしで安定運用**が可能となる。
