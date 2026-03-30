# PSC ルーティングテーブルモデル v0.1

## ステータス

本ドキュメントはアーカイブ版である。
後継:
- PSC Routing Table Model v0.2

## Document Information

- ドキュメント名: PSC Routing Table Model
- バージョン : v0.1
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
**ルーティングテーブルモデル**を定義する。

ルーティングテーブルモデルは

- ルート情報の表現
- ルート情報の保存
- ルート情報の参照

の方法を定義する。

本仕様では主に以下を扱う。

- ルートエントリ構造
- Next Hop 表現
- ルート状態
- ポリシー属性
- マルチパス対応

---

## 2. 設計目標

PSC ルーティングテーブルモデルは以下を目的とする。

1. Port-to-Port 論理ルーティングのサポート
2. Node-to-Node 物理転送構造との整合
3. ポリシー・状態・ドメインを考慮したルート選択
4. マルチパスおよびフェイルオーバー対応
5. ノード規模からファブリック規模までのスケール
6. RCU / TMU / TEU が利用可能なルート情報構造

---

## 3. 基本モデル

### 3.1 Primary routing abstraction

PSC ルーティングは論理的には

Port → Port

通信として定義される。

ルーティングテーブルは
**宛先 Port に対して使用する経路**
を決定するために使用される。

### 3.2 Underlying forwarding context

論理ルーティングは Port ベースであるが
実際の転送は PSC ノードおよび PSC リンク上で行われる。

つまり実際の通信は

Node → Node

の形になる。

そのためルーティングテーブルには

- 論理ルート情報
- 物理トポロジー情報

の両方が含まれる。

### 3.3 Two-layer route representation

PSC routing table は二層構造のルート表現を採用する。

- Logical routing layer
  Destination Port -> Candidate Next Hop Port

- Physical context layer
  Destination Node / Next Hop Node / Domain context

これにより PSC は

- Port ベース通信抽象
- 物理トポロジー認識ルーティング

を両立することができる。

---

## 4. ルーティングテーブル構造

### 4.1 Route entry concept

ルーティングテーブルは **Route Entry** の集合で構成される。

各 Route Entry は宛先通信エンドポイントへの
転送経路候補を表す。

Route Entry は以下の種類を持つことがある。

- primary path
- alternate path
- failover path
- restricted path
- adaptive routing candidate

### 4.2 Recommended route entry fields

PSC Route Entry は以下のフィールドを持つことができる。

Destination fields

- Destination Port ID
- Destination Node ID
- Destination Domain ID

Next Hop fields

- Next Hop Port ID
- Next Hop Node ID

Attribute fields

- Path Class
- Policy Flags
- Trust Level

Route state fields

- Route State
- Priority
- Cost / Score
- Validity
- Update Timestamp

### 4.3 Minimal required fields

最小限必要なフィールド

- Destination Port ID
- Next Hop Port ID
- Next Hop Node ID
- Route State
- Priority

---

## 5. ルートエントリフィールド

### 5.1 Destination Port ID

宛先となる PSC Port を識別する。

例:

- GPU service port
- storage endpoint port
- memory access port
- control channel port
- security-managed port

PSC ルーティングの主要キーである。

### 5.2 Destination Node ID

宛先 Port を所有する PSC Node を示す。

用途:

- トポロジー管理
- ノード障害対応
- ルート集約
- ドメインルーティング

### 5.3 Destination Domain ID

宛先が属するルーティングドメイン。

例:

- Port domain
- Node domain
- Cluster domain
- Fabric domain

### 5.4 Next Hop Port ID

転送時に使用する次ホップ Port。

PSC では Next Hop の主要表現として使用される。

TMU / TEU はこの Port を使用して
実際の転送インターフェースを決定する。

### 5.5 Next Hop Node ID

Next Hop Port が属する PSC Node を示す。

用途

- トポロジー管理
- ノード障害検出
- クラスタルーティング
- 階層型ルーティング

### 5.6 Path Class

ルートの種類を示す。

例

- normal
- low_latency
- high_bandwidth
- secure
- isolated
- failover
- maintenance

### 5.7 Policy Flags

ルーティング制約。

例

- ISOLATE
- RESTRICT_FORWARD
- INSPECT
- PRIORITY_SECURITY
- LOCAL_ONLY
- FABRIC_ONLY

### 5.8 Trust Level

通信の信頼レベルを表す。

### 5.9 Route State

ルート状態。

例

- healthy
- degraded
- congested
- restricted
- blocked
- failed
- standby

### 5.10 Priority

同一宛先に複数ルートがある場合の優先度。

### 5.11 Cost / Score

ルート評価値。

例

- hop cost
- policy weight
- congestion penalty

### 5.12 Validity

ルートの有効状態。

例

- valid
- temporarily_invalid
- expired
- quarantined

### 5.13 Update Timestamp

ルート最終更新時刻。

---

## 6. ルーティングテーブル構成

### 6.1 Destination-based indexing

PSC routing table は
**Destination Port ID** をキーとして管理する。

### 6.2 Secondary indexing

以下のインデックスを持つことができる。

- Destination Node ID
- Destination Domain ID
- Next Hop Port ID
- Next Hop Node ID
- Path Class
- Route State

### 6.3 Route Set

同一 Destination Port に対して
複数 Route Entry を持つ。

これを **Route Set** と呼ぶ。

例

- Primary Route
- Alternate Route
- Failover Route
- Adaptive Route

---

## 7. マルチパス対応

### 7.1 Multiple candidate routes

PSC routing table は
単一宛先に対して複数ルートを保持できる。

用途

- resilience
- congestion avoidance
- adaptive routing
- topology flexibility

### 7.2 Route set example

Destination Port : P100

Candidate Routes

- Next Hop Port P210  Priority 100
- Next Hop Port P218  Priority 80
- Next Hop Port P233  Priority 60

### 7.3 Selection behavior

ルート選択は routing table 自体では実行しない。

ルート候補は RCU によって評価される。

評価要素

- route state
- policy constraints
- trust level
- priority
- score
- topology condition

---

## 8. フェイルオーバー対応

優先ルートが使用不能になった場合
RCU は代替ルートを選択する。

フェイルオーバールーティングでは
最適ではないが有効なルートを使用する場合がある。

例

- longer path
- reduced bandwidth path
- restricted security route

---

## 9. 適応ルーティング対応

### 9.1 Runtime route variation

ルート状態は以下により変化する。

- congestion
- thermal pressure
- optical degradation
- retry escalation
- policy change

### 9.2 Stable adaptation

安定性確保のため以下を使用する。

- hysteresis
- cooldown
- dampening

### 9.3 Relationship to Fabric State

Route Entry の評価は
Fabric State によって変化する場合がある。

CALM
安定ルート優先

WARM
軽度の負荷分散

HOT
混雑回避優先

EMERGENCY
安全性・生存性優先

---

## 10. ドメイン対応ルーティング

PSC routing table は
ドメイン単位ルーティングをサポートする。

例

- Node domain
- Cluster domain
- Fabric domain

---

## 11. ルートエントリライフサイクル

### 11.1 Creation

- topology discovery
- static configuration
- policy provisioning

### 11.2 Update

- topology change
- link state change
- congestion

### 11.3 Invalidation

- path failure
- node failure
- policy restriction

### 11.4 Removal

無効化されたルートエントリは
即時削除または
履歴保持目的で保持される場合がある。

---

## 12. PSCモジュールとの関係

Resolver
ルーティング意図決定

SPU
セキュリティ制御

RCU
ルーティングテーブル管理

TMU
転送リソース管理

TEU
実際のデータ転送

---

## 13. ルートエントリ例

Destination Port ID : PORT_GPU_014
Destination Node ID : NODE_022
Destination Domain  : CLUSTER_A

Next Hop Port ID    : PORT_FABRIC_EGRESS_03
Next Hop Node ID    : NODE_007

Path Class          : low_latency
Policy Flags        : RESTRICT_FORWARD
Trust Level         : trusted_internal

Route State         : healthy
Priority            : 100
Cost / Score        : 18
Validity            : valid
Update Timestamp    : T+002145

---

## 14. 将来拡張

- route scoring model
- route compression
- telemetry integration
- optical path awareness

---

## 15. まとめ

PSC Routing Table Model v0.1 は
PSC Fabric における
RCU が使用するルーティングテーブル構造を定義する。

特徴

- Port-to-Port routing
- Node context awareness
- policy-aware routing
- multi-path support
- failover support
- domain scalability
