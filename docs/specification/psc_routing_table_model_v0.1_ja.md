# PSC Routing Table Model v0.1

PSC ルーティングテーブルモデル v0.1

## Document Information

- Document Name: PSC Routing Table Model
- Version: v0.1
- Project: PSC / Photon System Controller
- Layer: PSC Fabric
- Status: Draft
- Author: T. Hirose
- Language: Japanese

---

## 1. Purpose

目的

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

## 2. Design Goals

設計目標

PSC ルーティングテーブルモデルは以下を目的とする。

1. Port-to-Port 論理ルーティングのサポート  
2. Node-to-Node 物理転送構造との整合  
3. ポリシー・状態・ドメインを考慮したルート選択  
4. マルチパスおよびフェイルオーバー対応  
5. ノード規模からファブリック規模までのスケール  
6. RCU / TMU / TEU が利用可能なルート情報構造

---

## 3. Basic Model

基本モデル

### 3.1 Primary routing abstraction

主要ルーティング抽象

PSC ルーティングは論理的には

Port → Port

通信として定義される。

ルーティングテーブルは
**宛先 Port に対して使用する経路**
を決定するために使用される。

---

### 3.2 Underlying forwarding context

物理転送コンテキスト

論理ルーティングは Port ベースであるが  
実際の転送は PSC ノードおよび PSC リンク上で行われる。

つまり実際の通信は

Node → Node

の形になる。

そのためルーティングテーブルには

- 論理ルート情報
- 物理トポロジー情報

の両方が含まれる。

---

### 3.3 Two-layer route representation

二層ルート表現

PSC routing table は二層構造を採用する。

Logical routing layer

Destination Port
    ↓
Next Hop Port

---

Physical context layer

Destination Node
Next Hop Node
Domain Context

これにより PSC は

- Port ベース通信
- トポロジー認識ルーティング

の両方を実現する。

---

## 4. Routing Table Structure

ルーティングテーブル構造

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

---

### 4.2 Recommended route entry fields

PSC Route Entry は以下のフィールドを持つことができる。

Destination

Destination Port ID
Destination Node ID
Destination Domain ID

Next Hop

Next Hop Port ID
Next Hop Node ID

Attributes

Path Class
Policy Flags
Trust Level

State

Route State
Priority
Cost / Score
Validity
Update Timestamp

---

### 4.3 Minimal required fields

最小限必要なフィールド

Destination Port ID
Next Hop Port ID
Next Hop Node ID
Route State
Priority

---

## 5. Route Entry Fields

ルートエントリフィールド

### 5.1 Destination Port ID

宛先となる PSC Port を識別する。

例

- GPU service port
- storage endpoint port
- memory access port
- control channel port

PSC ルーティングの主要キーである。

---

### 5.2 Destination Node ID

宛先 Port を所有する PSC Node を示す。

用途

- トポロジー管理
- ノード障害対応
- ルート集約
- ドメインルーティング

---

### 5.3 Destination Domain ID

宛先が属するルーティングドメイン

例

- Port domain
- Node domain
- Cluster domain
- Fabric domain

---

### 5.4 Next Hop Port ID

転送時に使用する次ホップ Port。

PSC では Next Hop の主要表現として使用される。

TMU / TEU はこの Port を使用して  
実際の転送インターフェースを決定する。

---

### 5.5 Next Hop Node ID

Next Hop Port が属する PSC Node を示す。

用途

- トポロジー管理
- ノード障害検出
- クラスタルーティング
- 階層型ルーティング

---

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

---

### 5.7 Policy Flags

ルーティング制約

例

- ISOLATE
- RESTRICT_FORWARD
- INSPECT
- PRIORITY_SECURITY
- LOCAL_ONLY
- FABRIC_ONLY

---

### 5.8 Trust Level

通信の信頼レベルを表す。

---

### 5.9 Route State

ルート状態

例

- healthy
- degraded
- congested
- restricted
- blocked
- failed
- standby

---

### 5.10 Priority

同一宛先に複数ルートがある場合の優先度。

---

### 5.11 Cost / Score

ルート評価値

例

- hop cost
- policy weight
- congestion penalty

---

### 5.12 Validity

ルートの有効状態

例

- valid
- temporarily_invalid
- expired
- quarantined

---

### 5.13 Update Timestamp

ルート最終更新時刻

---

## 6. Route Table Organization

### 6.1 Destination-based indexing

PSC routing table は  
**Destination Port ID** をキーとして管理する。

---

### 6.2 Secondary indexing

以下のインデックスを持つことができる。

- Destination Node ID
- Destination Domain ID
- Next Hop Port ID
- Next Hop Node ID
- Path Class
- Route State

---

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

## 7. Multi-Path Support

PSC routing table は  
マルチパスルーティングをサポートする。

例

Destination Port : P100

Candidate Routes

- Next Hop Port P210  Priority 100
- Next Hop Port P218  Priority 80
- Next Hop Port P233  Priority 60

---

## 8. Failover Support

優先ルートが使用不能になった場合  
RCU は代替ルートを選択する。

フェイルオーバールーティングでは
最適ではないが有効なルートを使用する場合がある。

例

- longer path
- reduced bandwidth path
- restricted security route

---

## 9. Adaptive Routing Support

ルート状態は以下により変化する。

- congestion
- thermal pressure
- optical degradation
- retry escalation
- policy change

安定性確保のため以下を使用する。

- hysteresis
- cooldown
- dampening

---

## 10. Domain-aware Routing

PSC routing table は  
ドメイン単位ルーティングをサポートする。

例

- Node domain
- Cluster domain
- Fabric domain

---

## 11. Route Entry Lifecycle

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

---

## 12. Interaction with PSC Modules

Resolver  
- ルーティング意図決定

SPU  
- セキュリティ制御

RCU  
- ルーティングテーブル管理

TMU  
- 転送リソース管理

TEU  
- 実際のデータ転送

---

## 13. Example Route Entry

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

## 14. Future Extensions

将来拡張

- route scoring model
- route compression
- telemetry integration
- optical path awareness

---

## 15. Summary

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
