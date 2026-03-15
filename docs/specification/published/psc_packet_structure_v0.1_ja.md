# PSC Fabric Packet Structure v0.1

## Document Information

- ドキュメント名: PSC Fabric Packet Structureバージョン : v0.1
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

PSC Fabric Packet は PSC Fabric 内で使用される
基本的な転送単位である。

このパケットは以下の情報を運ぶ。

- ルーティング情報
- セキュリティコンテキスト
- 転送制御
- チャンク化されたデータペイロード

PSC パケットは適応型光ファブリック上での
受信側主導チャンク転送に最適化されている。

---

## 2. 設計原則

PSC Packet の設計は以下の原則に従う。

Fabric-native

PSC Packet は従来のバスや IP ネットワークではなく  
PSC Fabric ルーティングのために設計されている。

Receiver-driven transfer

転送は送信側ではなく  
**受信側によって開始および制御される。**

Chunk transport

大きな転送は **Chunk** に分割される。

利点

- 混雑制御
- フロー制御
- 部分再送
- マルチパススケジューリング

Policy-aware communication

パケットヘッダにはセキュリティおよびドメイン情報が含まれ  
以下を可能にする。

- SPU によるポリシー適用
- ドメイン制御
- セキュアルーティング

---

## 3. パケット構造概要

PSC Packet は以下の要素で構成される。

- PSC Header
- Routing Information
- Security Tag
- Transfer Control
- Chunk Descriptor
- Payload Data

### 3.1 論理構造

```
PSC Packet
┌─────────────────────┐
│ PSC Header          │
├─────────────────────┤
│ Routing Information │
├─────────────────────┤
│ Security Tag        │
├─────────────────────┤
│ Transfer Control    │
├─────────────────────┤
│ Chunk Descriptor    │
├─────────────────────┤
│ Payload Data        │
└─────────────────────┘
```
---

## 4. PSC Header

PSC Header はパケットの基本識別情報を定義する。

### 4.1 フィールド

- Version
- Packet Type
- Packet Length
- Transfer ID
- Sequence Number
- Flags

### 4.2 フィールド説明

Version  
PSC プロトコルバージョン。  
将来のプロトコル拡張を可能にする。

Packet Type  
パケットの動作を定義する。

初期タイプ

- REQUEST
- DATA
- ACK
- FLOW_CONTROL
- CONTROL
- FAULT
- TELEMETRY

Packet Length  
パケットの総サイズ。

Transfer ID  
転送セッションの一意識別子。

Sequence Number  
転送内でのチャンク順序番号。

Flags  
制御フラグ。

例

- RETRY
- PRIORITY
- SECURE_PATH
- MULTIPATH
- PARTIAL_CHUNK

---

## 5. Routing Information

Routing フィールドは PSC Fabric が
パケット経路を決定するために使用する。

### 5.1 フィールド

- Source Node ID
- Destination Node ID
- Source Port ID
- Destination Port ID
- Fabric Domain
- Path Hint
- Hop Count

### 5.2 フィールド説明

Source Node ID
送信元 PSC ノード。

Destination Node ID
宛先 PSC ノード。

Source Port ID
送信元論理ポート。
PSC Port Model v0.1 によって定義される。


Destination Port ID
宛先論理ポート。

Fabric Domain
ルーティングスコープ。

例

- LOCAL
- CLUSTER
- GLOBAL
- EXTERNAL

Path Hint
RCU ルーティングのヒント。

例

- LOW_LATENCY
- HIGH_BANDWIDTH
- RESILIENT

Hop Count
ルーティングループを防止する。

---

## 6. Security Tag

Security Tag は  
**SPU (Security Policy Unit)** によって評価される。

### 6.1 フィールド

- Security Class
- Trust Level
- Domain Authorization
- Policy Flags
- Integrity Tag

### 6.2 フィールド説明

Security Class
ポートの Security Class と一致する。

- SYSTEM
- TRUSTED
- USER
- EXTERNAL
- QUARANTINED

Trust Level
追加の信頼評価。

Domain Authorization
許可されたドメイン範囲。

Policy Flags
セキュリティ動作フラグ。

例

- INSPECT
- ISOLATE
- PRIORITY_SECURITY
- RESTRICT_FORWARD

Integrity Tag
パケット整合性検証フィールド。

---

## 7. Transfer Control

Transfer Control は PSC の
受信側主導転送モデルを支える。

### 7.1 フィールド

- Transfer Type
- Transfer State
- Flow Credit
- Priority Class
- Retry Counter

### 7.2 フィールド説明

Transfer Type

- STREAM
- BLOCK
- MEMORY
- CONTROL
- TELEMETRY

Transfer State
転送状態。

例

- INIT
- ACTIVE
- PAUSED
- RETRY
- COMPLETE

Flow Credit
受信側が許可する残りクレジット。
フロー制御に使用される。

Priority Class
スケジューラ優先度。

例

- REALTIME
- HIGH
- NORMAL
- BACKGROUND

Retry Counter
再送回数。

## 8. Chunk Descriptor

PSC 転送はチャンク単位で行われる。

Chunk Descriptor は
データ断片を定義する。

### 8.1 フィールド

- Chunk ID
- Chunk Offset
- Chunk Size
- Total Transfer Size
- Chunk Flags

### 8.2 フィールド説明

Chunk ID
チャンク番号。

Chunk Offset
転送内バイトオフセット。

Chunk Size
チャンクサイズ。

Total Transfer Size
全体転送サイズ。

Chunk Flags

例

- FIRST_CHUNK
- LAST_CHUNK
- PARTIAL
- RECOVERY

---

## 9. Payload Data

実際の転送データ。

Payload 例

- メモリデータ
- ファイルブロック
- モデルパラメータ
- 推論テンソル
- ストレージオブジェクト
- 制御メッセージ

PSC はペイロード意味を定義しない。
ペイロード解釈は

- PSCOS
- アプリケーション層

が行う。

---

## 10. Packet Lifecycle

典型的な PSC パケット処理

Receiver Node
```
Transfer Request  
↓  
Resolver  
↓  
Scheduler  
↓  
SPU Validation  
↓  
RCU Route Selection  
↓  
TMU Transfer Context  
↓  
TEU Packet Generation  
↓  
PSC Fabric Routing  
↓  
Destination PSC
```
---

## 11. Error Handling

エラーは複数層で発生する可能性がある。

例

- Security violation
- Route failure
- Link degradation
- Flow control violation
- Integrity mismatch

対処

- Retry
- Reroute
- Quarantine
- Drop
- Fault escalation

---

## 12. Packet Types Summary

- REQUEST        転送要求
- DATA           チャンクデータ
- ACK            チャンク確認
- FLOW_CONTROL   クレジット更新
- CONTROL        PSC 制御メッセージ
- FAULT          エラー通知
- TELEMETRY      監視データ
