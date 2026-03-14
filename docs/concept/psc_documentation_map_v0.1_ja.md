# PSC ドキュメンテーションマップ

プロジェクト: PSC / Photon System Controller  
ドキュメント種別: Documentation Map  
ステータス: Draft  

---

# 1. 概要

本ドキュメントは、PSC に関するドキュメント体系の構造を説明するものである。

PSC のドキュメントは、概念設計・アーキテクチャ設計・詳細仕様を
明確に分離するため、複数のレイヤーで構成されている。

PSC のドキュメント構造は、以下のレイヤー構造に従う。

```
PSC Concept
↓
PSC Architecture
↓
PSC Specification
```


---

# 2. PSC ドキュメント構造

## 2.1 コンセプトレイヤー

Concept ドキュメントは、PSC の高位概念および設計思想を説明する。

配置場所:

```
docs/concept
```

主なドキュメント:

- PSC Concept
- PSC Architecture Map
- PSC Documentation Map

これらのドキュメントでは主に以下を説明する。

- PSC の設計思想
- Fabric-centric computing の基本概念
- システム全体の高位構造

---

## 2.2 仕様レイヤー

Specification ドキュメントは、PSC を構成する各要素の詳細設計を定義する。

配置場所:

```
docs/specification
```
主な仕様グループ:

### Addressing

- PSC Address Format
- PSC Node Addressing Model

### Packet

- PSC Packet Structure

### Port Model

- PSC Port Model

### Routing

- PSC Routing Model
- PSC Routing Algorithm
- PSC Routing Table Model

### Transfer

- PSC Transfer Flow

これらの仕様は、PSC Fabric の基本動作を定義する。

---

# 3. 仕様ドキュメントの関係

PSC の仕様ドキュメントは、以下のような構造で整理される。

```
PSC Fabric

├ Addressing
│ ├ PSC Address Format
│ └ PSC Node Addressing Model
│
├ Packet
│ └ PSC Packet Structure
│
├ Port
│ └ PSC Port Model
│
├ Routing
│ ├ PSC Routing Model
│ ├ PSC Routing Algorithm
│ └ PSC Routing Table Model
│
└ Transfer
  └ PSC Transfer Flow
 ```

---

# 4. 今後追加される可能性のあるドキュメント

将来的に、以下のドキュメントが追加される可能性がある。

Architecture:

- PSC Fabric Architecture
- PSC Node Architecture
- PSC Routing Pipeline Architecture

Protocol:

- PSC Transport Model
- PSC Security Model
- PSC Congestion Control Model

System:

- PSC Native System Architecture
- PSC Hybrid System Architecture

---

# 5. このマップの目的

Documentation Map は、以下を目的としている。

- PSC ドキュメント体系の構造を理解しやすくする
- PSC 仕様ドキュメントへのナビゲーションを提供する
- ドキュメント間の整合性維持を支援する
- PSC アーキテクチャの将来拡張を支援する

---

# 6. プロジェクト

PSC  
Photon System Controller

Fabric-centric distributed computer architecture
