# PSC Concept

English version: [psc_concept_en.md](psc_concept_en.md)

本ドキュメントはPSCの最終コンセプトを示すものである。  
初期のドラフトは 99_archive/concept/ に保存されている。

## ドキュメント情報

- 名称: PSC Concept
- バージョン: v0.1
- プロジェクト: PSC / Photon System Controller
- ドキュメント分類: Concept
- 状態: Draft
- 作成者: T. Hirose
- 言語: 日本語

---

## 1. Introduction

PSC（Photon System Controller）は  
コンピュータシステムの通信構造を再設計することを目的とした  
研究プロジェクトである。

従来のコンピュータアーキテクチャでは  
CPUがシステム全体の中心となり、

- 計算
- 制御
- データ移動

の多くを担ってきた。

しかし現代のコンピューティング環境では  
計算性能の向上よりも  
**データ移動の効率化**が重要な課題となっている。

PSCはこの問題に対して  
**通信を中心としたコンピュータアーキテクチャ**を提案する。

---

## 2. Data Movement Crisis

近年のコンピュータシステムでは  
計算性能の向上が続いている一方で、

**データ移動のコスト**が  
システム全体の性能を制約する要因になりつつある。

プロセッサ性能の向上に対して

- メモリ帯域
- デバイス通信
- ノード間通信

などのデータ移動コストは  
相対的に大きくなっている。

この問題はしばしば

**Data Movement Crisis**

と呼ばれる。

PSCはこの課題に対して  
通信構造そのものを再設計することで  
解決を試みる。

PSCでは

- 通信を中心としたアーキテクチャ設計
- Fabricによるデータ移動管理
- 分散制御による通信最適化

などの手法を用いることで  
データ移動の効率化を目指す。

---

## 3. Communication-Centric Computing

PSCの基本思想は  
**Communication-Centric Computing**である。

これは

「計算よりも通信を中心にシステムを設計する」

という考え方である。

従来のコンピュータは

```
CPU
↓
Bus
↓
Device
```

という構造で構築されてきた。

PSCではこの構造を拡張し

```
Fabric
↓
Node
```


という構造を中心とする。

通信ネットワーク（Fabric）が  
システム全体の基盤となる。

---

## 4. Fabric-First Architecture

PSCでは  
**Fabric-First Architecture**を採用する。

これは

「通信ネットワークを  
コンピュータアーキテクチャの中心に置く」

という設計思想である。

Fabricは単なる通信経路ではなく

- データ移動
- 負荷分散
- 経路制御
- 混雑制御

などを担う重要なシステム要素となる。

---

## 5. Everything is a Node

PSCでは  
システム内のすべての要素を  
**Node**として扱う。

例

- CPU
- GPU
- Memory
- Storage
- Accelerator
- Network Interface

これらはすべて  
Fabricに接続されたノードとして扱われる。

このモデルにより  
システム構成の柔軟性と拡張性が向上する。

---

## 6. Receiver-Driven Data Movement

PSCでは  
データ転送を

**Receiver-Driven**

で制御する。

これは

「受信側が転送を主導する」

という通信モデルである。

この方式により

- バックプレッシャ制御
- 混雑回避
- 安定した通信

を実現できる。

---

## 7. Distributed Control

PSCは  
**分散制御型の通信アーキテクチャ**である。

通信制御は  
単一の中央制御ではなく

複数の制御モジュールによって  
分散的に行われる。

これにより

- スケーラビリティ
- 可用性
- 障害耐性

を向上させることができる。

---

## 8. Towards Large-Scale Fabric Computing

PSCは  
将来的に

- 大規模分散コンピューティング
- データセンターアーキテクチャ
- 光通信ファブリック

などへの応用を視野に入れている。

PSCは  
**通信中心のコンピューティング基盤**を構築することを目標としている。
