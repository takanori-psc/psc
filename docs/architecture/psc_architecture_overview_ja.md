# PSC Architecture Overview

## Document Information

- Document Name: PSC Architecture Overview
- Version      : v0.1
- Project      : PSC / Photon System Controller
- Layer        : Architecture
- Status       : Draft
- Author       : T. Hirose
- Language     : Japanese (JA)

---

## 1. Overview

本ドキュメントは PSC (Photon System Controller) の
**全体アーキテクチャ構造**を概説する。

PSC はコンピュータシステムにおける
データ移動処理を CPU から分離し、
専用の Fabric 制御プロセッサによって管理する
**Fabric-centric 通信アーキテクチャ**である。

PSCは以下の要素によって構成される。

- PSC Node
- PSC Fabric
- Resolver
- Transfer Pipeline

---

## 2. PSC Node

PSC Node は PSC Fabric に接続される
通信制御ノードである。

PSC Node は以下の主要モジュールを持つ。

- Session Manager  
- Flow Queue Manager  
- Transfer Scheduler (DRR)  
- Routing Engine  
- Backpressure Controller  
- DMA Engine  
- Resolver  

PSC Node はデータ転送の制御を担当し、
CPU や GPU、メモリ、ストレージなどの
システムコンポーネント間のデータ移動を管理する。

---

## 3. PSC Fabric

PSC Fabric は
PSC Node を相互接続する通信ネットワークである。

PSC Fabric は以下の特徴を持つ。

- Optical Link based interconnect
- Cut-through forwarding
- Multi-path routing
- Adaptive congestion avoidance

PSC Fabric は
ノード間の高速データ転送を実現する。

---

## 4. Transfer Pipeline

PSC ではデータ転送は
以下のパイプラインによって処理される。

1. Transfer Session Creation
2. Chunk Segmentation
3. Flow Queue Scheduling
4. Fabric Routing
5. Receiver Reordering
6. DMA Write

PSC はデータを Chunk 単位で転送することで
効率的な転送制御とエラー回復を実現する。

---

## 5. Resolver

Resolver は PSC Node 内に存在する
軽量な制御モジュールである。

Resolver は Fabric 状態を観測し、
以下のような裁定を行う。

- Routing decision adjustment
- Congestion mitigation
- Flow prioritization adjustment
- Exceptional condition arbitration

Resolver は高度な中央制御ではなく、
**分散型 Fabric 制御の裁定役**として動作する。

---

## 6. Control Model

PSC Fabric は
以下の3層の制御モデルによって動作する。

Fast Path Control

- DRR Scheduler
- Normal Routing

Local Protection

- Backpressure
- Flow Control

Distributed Arbitration

- Resolver based decision

この構造により PSC Fabric は
高いスループットと安定性を両立する。

---

## 7. Summary

PSC Architecture は

- Fabric-centric design
- Distributed control model
- Chunk-based data transport
- Receiver-driven transfer

という思想に基づいて設計されている。

PSC は従来の CPU 中心アーキテクチャとは異なり、
データ移動制御を Fabric 側に委譲することで
高いスケーラビリティを実現する。
