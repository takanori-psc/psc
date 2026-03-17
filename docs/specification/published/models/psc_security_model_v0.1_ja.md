# PSC Security Model v0.1

## ドキュメント情報

- ドキュメント名   : PSC Security Model
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

本ドキュメントは PSC Fabric における **Security Model（セキュリティモデル）** を定義する。

PSC Security Model は、PSC Fabric 全体における  
**信頼性およびセキュリティ状態を評価・管理するための枠組み**を提供する。

従来のネットワークセキュリティモデルが主にアクセス制御に依存するのに対し、  
PSC は **セキュリティ評価を Fabric の挙動およびルーティング判断に直接統合する**。

このセキュリティモデルにより PSC Fabric は以下を実現する。

- ノード信頼性の評価
- 経路信頼性の評価
- 異常または悪意ある挙動の検出
- 信頼性の低い Fabric 要素の制限
- Fabric 全体の安定性維持

---

## 2. Scope（適用範囲）

本仕様は以下を定義する。

- PSC Fabric における Trust（信頼）の概念
- Node Trust 評価
- Route Trust 評価
- Trust 状態モデル
- セキュリティとルーティングシステムの相互関係

本ドキュメントでは以下は定義しない。

- 暗号プロトコル
- 認証メカニズム
- 証明書インフラ

これらは別仕様で定義される可能性がある。

---

## 3. Design Principles（設計原則）

PSC Security Model は以下の設計原則に従う。

## 3.1 Trust-aware Fabric

PSC Fabric はルーティングおよび制御判断において  
**信頼状態を考慮する必要がある**。

セキュリティ評価は Fabric 制御プロセスの一部として扱われる。

## 3.2 Behavior-based Evaluation

Trust 評価は静的設定だけでなく  
**観測された挙動**を考慮する必要がある。

## 3.3 Distributed Security

セキュリティ評価は PSC ノード全体に分散して動作する。

各ノードはローカル観測に基づいて  
Trust 状態を独立して評価できる。

## 3.4 Stability Preservation

セキュリティ機構は Fabric の安定性を損なってはならない。

Trust 評価は制御された予測可能な方法で動作する必要がある。

---

## 4. Trust Concept（Trust概念）

PSC Fabric において **Trust は Fabric 構成要素の信頼性および安全状態を表す概念**である。

Trust 評価は以下に適用される可能性がある。

- ノード
- リンク
- ルーティング経路
- Fabric 領域

Trust は PSC コンポーネント間の相互作用に影響を与える。

Trust レベルが低い場合、  
ルーティング制限または隔離が行われる可能性がある。

---

## 5. Trust Types（Trust種類）

PSC は以下の2種類の Trust を定義する。

| Trust Type  | Description                       |
|-------------|-----------------------------------|
| Node Trust  | 特定の PSC ノードに対する信頼評価 |
| Route Trust | ルーティング経路に対する信頼評価  |

これらの Trust はルーティングおよび制御挙動に影響を与える。

---

## 6. Trust Sources（Trust情報源）

Trust 評価は以下の2種類の情報源を使用する。

| Source        | Description                                |
|---------------|--------------------------------------------|
| Static Trust  | 管理設定またはポリシーにより定義された信頼 |
| Dynamic Trust | 実行時の挙動観測から導出される信頼         |

---

## 7. Trust State Model（Trust状態モデル）

PSC は信頼状態を以下の簡易状態モデルで表現する。

| Trust State | Description                         |
|-------------|-------------------------------------|
| TRUSTED     | 高信頼 Fabric コンポーネント        |
| NORMAL      | 通常信頼状態                        |
| RESTRICTED  | 制限付き利用状態                    |
| BLOCKED     | Fabric との通常通信が禁止された状態 |

これらの状態は Trust 条件を簡潔に表現する。

---

## 8. Node Trust Evaluation（ノード信頼評価）

Node Trust は以下の要因によって影響を受ける。

- 管理者による静的信頼設定
- ノードの役割および認証状態
- エラー率の異常
- 異常なトラフィック挙動
- Telemetry の不整合
- 繰り返されるルーティング失敗

Node Trust 評価は PSC ノードまたは制御要素によって行われる。

---

## 9. Route Trust Evaluation（経路信頼評価）

Route Trust は PSC Fabric 内の経路の信頼性を評価する。

Route Trust は以下に依存する可能性がある。

- 中継ノードの Trust 状態
- リンク安定性
- エラー履歴
- ルーティング異常
- 不審なトラフィック挙動

低信頼ノードを通過する経路は  
ペナルティまたは制限を受ける可能性がある。

---

## 10. Trust Evaluation Process（Trust評価プロセス）

Trust 評価は通常以下の流れで行われる。
```
Telemetry Observation
↓
Behavior Analysis
↓
Static Trust + Dynamic Trust
↓
Effective Trust State
```
Trust 評価は Fabric 動作中に継続的に行われる可能性がある。

---

## 11. Interaction with Routing（ルーティング連携）

ルーティング判断は Trust 評価を考慮する。

典型的なルーティング判断要素：
```
Congestion State
+
Fabric State
+
Trust State
+
Policy
↓
Routing Decision
```
低信頼要素を含む経路は  
可能であれば回避される。

---

## 12. Trust Recovery（Trust回復）

異常挙動が解消された場合、Trust 状態は回復する可能性がある。

回復メカニズムの例：

- 安定観測期間
- 過去の異常ペナルティの減衰
- 正常なルーティング挙動

Trust 回復は振動を防ぐため  
段階的に行われる。

---

## 13. Future Extensions（将来拡張）

将来の拡張例：

- reputation システム
- 異常検知アルゴリズム
- AI 支援 Trust 評価
- Fabric 間 Trust 交換
- セキュアなルーティングドメイン

---

## 14. Summary（まとめ）

PSC Security Model は PSC Fabric のための  
**分散型 Trust ベースセキュリティフレームワーク**を定義する。

主要原則：

- trust-aware routing
- 挙動ベース信頼評価
- 分散セキュリティ運用
- 安定した Trust 状態モデル

Trust 評価をルーティングおよびポリシー制御と統合することで  
PSC Fabric は複雑で動的な環境でも信頼性の高い動作を維持できる。
