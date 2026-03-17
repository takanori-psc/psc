# PSC Overview

English version: [psc_overview_en.md](psc_overview_en.md)

## ドキュメント情報

- 名称: PSC Overview
- バージョン: v0.1
- プロジェクト: PSC / Photon System Controller
- ドキュメント分類: Overview
- 状態: Draft
- 作成者: T. Hirose
- 言語: 日本語

---

## 1. Overview

PSC（Photon System Controller）は  
コンピュータシステムにおける **データ移動管理をCPUから分離するための  
Fabric-centric通信アーキテクチャ**である。

従来のコンピュータシステムでは、  
CPUがデータ移動の制御を中心的に担っている。

PSCはこの構造を再設計し、

- データ転送制御
- 経路選択
- 混雑制御
- 通信ポリシー

などを **専用通信コントローラ（PSC）に委譲する**ことで  
スケーラブルな通信基盤を実現する。

PSCは単なるインターコネクトではなく、  
**Fabric中心の分散コンピュータアーキテクチャ**を目指している。

PSCは将来的に、
大規模分散計算システムや次世代データセンターアーキテクチャへの
応用を視野に入れている。

---

## 2. Problem

従来のコンピュータアーキテクチャには  
以下のような構造的な制約が存在する。

### CPU-Centric Communication

多くのシステムでは  
データ移動の制御がCPUに集中している。

その結果、

- CPU負荷の増大
- スケール時のボトルネック
- 通信効率の低下

が発生する。

### DMA Dependency

データ移動は主にDMAによって行われるが  
DMAは以下の制約を持つ。

- 転送粒度が大きい
- 柔軟な経路制御が難しい
- 複雑な通信パターンに弱い

### Data Movement Bottleneck

現代のコンピュータでは  
計算性能よりも **データ移動** が  
主要なボトルネックになりつつある。

### Scalability Limitation

CPU中心のバス構造は  
システム拡張時に以下の問題を生む。

- 接続数制限
- 帯域共有
- トポロジー制約

---

## 3. PSC Core Idea

PSCはこれらの問題を解決するために  
以下の設計思想を採用する。

### Fabric-First Architecture

通信ネットワークを  
システムの中心構造として設計する。

### Everything is a Node

すべてのシステム要素を  
**Node** として扱う。

例：

- CPU
- GPU
- Memory
- Storage
- Accelerator
- Network Interface

### Receiver-Driven Transfer

データ転送は  
**受信側主導（Receiver-Driven）**で行われる。

これにより

- バックプレッシャ制御
- 輻輳回避
- 安定したスループット

を実現する。

### Chunk-Based Transport

データは **Chunk単位**で分割され  
柔軟なルーティングと転送制御が可能になる。

### Policy-Aware Routing

ルーティングは

- ポリシー
- 負荷
- 信頼度

などを考慮して決定される。

### Distributed Congestion Control

PSC Fabricでは  
分散型の輻輳制御を採用する。

---

## 4. PSC Architecture

PSCシステムは  
以下の主要要素で構成される。

### Nodes

コンピュータシステムの構成要素。

例：

- CPU Node
- GPU Node
- Memory Node
- Storage Node
- Accelerator Node

### PSC Controllers

PSC Controllerは  
ノード間通信を制御する。

主な役割

- 転送制御
- ルーティング
- 混雑管理

### PSC Fabric

PSC Fabricは  
ノード間を接続する通信ネットワークである。

特徴

- 高帯域
- 低遅延
- 多経路通信

### Transfer Pipeline

PSCは  
データ転送のためのパイプライン構造を持つ。

例

- Request
- Scheduling
- Routing
- Transfer
- Completion

---

## 5. PSC Control Model

PSCは複数の制御モジュールで構成される。

主要モジュール：

- Resolver
- Scheduler
- SPU
- RCU
- TMU
- TEU
- OMU

これらのモジュールは協調して

- 転送制御
- 経路決定
- 状態監視

を行う。

---

## 6. PSC Fabric Model

PSC Fabricは  
以下の通信モデルに基づいて動作する。

- Fabric Domain
- Node Addressing
- Transfer Protocol
- Chunk Transport
- Multi-Path Routing

これにより

- 高スケーラビリティ
- 高可用性
- 高効率通信

を実現する。

---

## 7. PSC Evolution Path

PSCは段階的な導入を想定している。

### Phase 1

PCIe Bridge PSC

既存システムに  
PSCを追加する形で導入。

### Phase 2

Hybrid Fabric

PCIeとPSC Fabricの  
ハイブリッド構成。

### Phase 3

Native PSC Fabric

PSC Fabric中心の  
システム構成。

### Phase 4

Optical Fabric

光通信を前提とした  
大規模Fabricシステム。

---

## 8. Future Topics

今後の研究テーマ：

- Resolver拡張
- Fabric状態最適化
- ポート役割自動決定
- トポロジー適応

重要キーワード

- State-Driven Fabric Control
- Adaptive Fabric Topology
- Resolver-Driven Fabric Optimization

---

PSCは  
**通信中心のコンピュータアーキテクチャ**を目指す  
研究プロジェクトであり、

将来的には  
大規模分散コンピューティングの新しい基盤となることを目標としている。
