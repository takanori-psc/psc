# PSC Routing Model v0.1
PSC ルーティングモデル v0.1

## Document Information

- Document Name: PSC Routing Model
- Version: v0.1
- Project: PSC / Photon System Controller
- Layer: PSC Fabric
- Status: Draft
- Author: T. Hirose
- Language: Japanese

---

## 1. Purpose
目的

本ドキュメントは PSC Fabric におけるルーティングモデルを定義する。

PSC Routing Model は、PSC Fabric 上で PSC ノード・ポート・クラスタ間の転送経路がどのように決定されるか、またトポロジー・障害・負荷状況・将来的な多層ファブリック拡張に対してルーティング制御がどのように適応するかを説明する。

本仕様は、主に論理的なルーティングアーキテクチャと RCU（Routing Control Unit）の制御動作に焦点を当てる。

---

## 2. Design Goals
設計目標

PSC ルーティングモデルは以下の目標を持って設計される。

1. ノードスケール・クラスタスケール・ファブリックスケールの通信に対応するスケーラブルなルーティング
2. メッシュトポロジーおよび将来の階層型ファブリックへの対応
3. 厳密な全体同期を必要としないローカル自律型制御
4. 障害・混雑状況下でも動作するフェイルオーバーおよび適応型ルーティング
5. ポリシーや転送クラスが要求する場合の決定論的動作の維持
6. PSC の状態ベース制御アーキテクチャとの統合

---

## 3. Routing Principles
ルーティング基本原則

PSC ルーティングは以下の原則に基づく。

### 3.1 State-based routing
状態ベースルーティング

ルーティング判断は、精密な全体最適化ではなく抽象化された状態情報に基づいて行われる。

ルーティングに関係する状態例：

- CALM
- WARM
- HOT
- EMERGENCY

### 3.2 Local-first decision model
ローカル優先決定モデル

ルーティングは可能な限りローカルなトポロジー情報とローカルな状態情報を優先して決定する。

PSC ルーティングは、部分的なトポロジー情報しか存在しない場合でも動作可能でなければならない。

### 3.3 Policy-aware path selection
ポリシー考慮型経路選択

PSC のルーティングは単純な最短経路だけで決定されない。

以下の要素も考慮される。

- セキュリティポリシー
- 信頼レベル
- 転送クラス
- 分離ドメイン
- 混雑状態
- 障害状態
- 冗長性要求

### 3.4 Multi-path capable architecture
マルチパス対応アーキテクチャ

PSC ルーティングは、トポロジーが許す場合に複数の有効経路を扱える必要がある。

マルチパスは以下の用途に使用される。

- 耐障害性
- フェイルオーバー
- 混雑回避
- 負荷分散
- 高可用性

---

## 4. Routing Architecture
ルーティングアーキテクチャ

PSC ルーティングは階層的な決定・実行モデルとして構成される。

### 4.1 Routing-related modules
ルーティング関連モジュール

ルーティングに関係する主要モジュール：

- Resolver  
  ルーティング意図とポリシー制約を決定する

- Scheduler  
  ルーティング優先度および転送スケジュールを調整する

- SPU（Security Policy Unit）  
  セキュリティポリシーと転送制約を適用する

- RCU（Routing Control Unit）  
  論理経路の選択とルーティング情報の管理を行う

- TMU（Transfer Management Unit）  
  ルート決定を転送スケジュールとリソース割り当てへ変換する

- TEU（Transfer Execution Unit）  
  実際のパケット / チャンク転送を実行する

### 4.2 RCU の責任

RCU は以下の役割を持つ。

- ルート情報の管理
- 候補経路の選択
- 経路の有効性評価
- 障害や混雑によるルート変更
- TMU へのルート出力

RCU はデータ転送を直接実行しない。

---

## 5. Routing Domains
ルーティングドメイン

PSC Fabric のルーティングは階層ドメインに分かれる。

### 5.1 Port domain
ポートドメイン

最小単位のルーティング範囲。

ノード内部または直接接続インターフェース間の通信を定義する。

### 5.2 Node domain
ノードドメイン

単一 PSC ノード内部のルーティング。

例：

- ローカルスイッチング
- 内部フォワーディング
- ローカルポリシー適用
- デバイス間転送

### 5.3 Cluster domain
クラスタドメイン

共有トポロジーで動作する PSC ノード群。

例：

- ワークステーションクラスタ
- ラックスケール構成
- アクセラレータクラスタ
- ストレージクラスタ

### 5.4 Fabric domain
ファブリックドメイン

PSC Fabric 全体を対象とするルーティング。

機能：

- マルチクラスタ通信
- 大規模経路選択
- 階層型ルーティング拡張
- 将来の Spine-Leaf / Optical Fabric

---

## 6. RCU Routing Model
RCU ルーティングモデル

### 6.1 Route input
RCU の入力

- 送信元アドレス
- 宛先アドレス
- ソースドメイン
- 宛先ドメイン
- 転送クラス
- ポリシーフラグ
- 信頼レベル
- ノード状態
- ファブリック状態
- 障害情報
- 混雑情報
- トポロジー情報

### 6.2 Route output
RCU 出力

- 次ホップ
- パスクラス
- 代替経路
- フェイルオーバー経路
- ルーティング制限
- 分離制約

### 6.3 Route decision modes
ルーティングモード

- Normal routing
- Restricted routing
- Isolated routing
- Failover routing
- Adaptive routing

### 6.4 Loose consistency
緩い整合性モデル

PSC ルーティングは完全同期を必要としない。

特徴：

- ローカル経路の正確性を優先
- 古い情報の許容
- 部分情報でも安全な経路選択
- 完全収束なしでもフェイルオーバー可能

---

## 7. Mesh Routing
メッシュルーティング

### 7.1 Default topology
PSC Fabric の基本トポロジーは Partial Mesh。

### 7.2 Mesh routing behavior
メッシュでは以下を考慮する。

- hop 数
- リンク状態
- 混雑状態
- ポリシー
- 冗長性

### 7.3 Mesh routing characteristics

- 直接経路
- 代替経路
- ローカル再ルーティング
- 経路多様性
- 部分障害耐性

### 7.4 Route preference

優先順位：

1 Policy
2 Security
3 Path health
4 Congestion
5 Hop efficiency

---

## 8. Spine-Leaf Routing
Spine-Leaf ルーティング

将来の階層型 PSC Fabric に対応。

構造：

Leaf  
↓  
Spine  
↓  
Leaf

特徴：

- ローカルルーティング
- Spine 経由通信
- ドメイン境界処理
- 経路集約

---

## 9. Failover Routing
フェイルオーバールーティング

リンク / ノード / トポロジー障害時のルーティング。

トリガー例：

- リンク障害
- ノード障害
- セキュリティイベント
- 混雑
- 光信号劣化

動作：

1 無効経路の削除
2 代替経路探索
3 ポリシー保持
4 TMU 通知
5 ルート振動抑制

---

## 10. Adaptive Routing
適応型ルーティング

PSC Fabric は負荷や状態変化に適応する。

入力例：

- ノード温度
- 転送キュー
- 混雑
- リトライ率
- リンク品質
- OMU データ

適応は以下の制約内で行われる：

- security policy
- trust
- domain isolation
- transfer class

安定性のため

- hysteresis
- cooldown
- state thresholds

を使用する。

Fabric Stateとの関係：

CALM  
通常ルーティング

WARM  
軽い適応

HOT  
負荷回避

EMERGENCY  
生存優先

---

## 11. Routing Constraints
ルーティング制約

PSC は以下を必ず遵守する。

- セキュリティ制約
- ドメイン分離
- 転送クラス
- 安全性
- フェイルオーバー

短い経路でもポリシー違反なら使用しない。

---

## 12. Future Extensions
将来拡張

将来仕様：

- ルートメトリック
- ルートスコア
- マルチパス負荷分散
- 光経路認識
- トラストドメイン
- クラスタゲートウェイ
- ルート集約

---

## 13. Summary
まとめ

PSC Routing Model v0.1 は PSC Fabric のルーティング基盤を定義する。

特徴：

- Local-first routing
- Mesh routing
- Spine-leaf routing
- Failover routing
- Adaptive routing
- 分散ルーティング
