# PSC Fast Mode Security Boundary Model v0.1（日本語版）

---

# Document Information

- Document Name : PSC Fast Mode Security Boundary Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSC Fabric / Security Layer
- Document Type : Specification
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-05
- Last Updated  : 2026-05
- Language      : Japanese

---

# 1. Overview

Fast Mode は、PSC Fabric 内における限定的な超低遅延通信モードである。

このモードは一般的なルーティング最適化機能ではなく、
限定された安全ドメイン内部においてのみ利用可能な、
制限付き高速実行モードとして定義される。

Fast Mode は以下を目的とする。

- CPU ノードと内部接続デバイス間の高速通信
- GPU ノード間の限定的高速データ転送
- Rack-local AI/HPC 処理最適化
- 超低遅延通信経路の提供
- PSC Fabric 内部帯域の効率利用

一方で Fast Mode は、
通常 PSC Routing に存在する複数の安全制御を簡略化または省略する可能性があるため、
厳格なセキュリティ境界管理を必要とする。

そのため Fast Mode は、
信頼済みローカルドメイン内部のみで利用可能とする。

---

# 2. Fast Mode Definition

Fast Mode は、
PSC Fabric 内部において限定条件下で許可される、
超低遅延・高帯域転送モードである。

Fast Mode は以下条件を満たす場合のみ許可される。

- PSC 1-hop 接続以内
- Trusted Local Domain 内部デバイス
- 同一 Secure Domain 内部
- 信頼済みノード間通信
- Resolver により許可された通信

Fast Mode は通常 Routing Mode と異なり、
一般 Fabric Routing を目的としない。

そのため、
Fast Mode パケットは通常 PSC Routing Fabric への転送を禁止する。

Fast Mode は、
一般 Routing Fabric の拡張用途として利用してはならない。

---

# 3. Security Boundary Principles

Fast Mode は高速性を優先する代わりに、
利用可能範囲を厳格に制限する。

以下を Fast Mode Security Boundary の基本原則とする。

## 3.1 Restricted Local Domain

Fast Mode は、
Rack-local または Node-local 範囲に限定する。

外部ネットワークまたは不明ノードへの転送は禁止する。

---

## 3.2 One-hop Limitation

Fast Mode は、
複数 PSC 経由通信を禁止する。

許可される経路は以下のみとする。

- CPU PSC → GPU PSC
- CPU PSC → Trusted Internal Device PSC
- GPU PSC → Trusted Local GPU Fabric Node
- CPU PSC → Local Memory Node PSC
- CPU PSC → Local Storage Node PSC

PSC を 2 個以上経由する経路は禁止する。

---

## 3.3 Managed GPU Local Fabric

GPU 間 Fast Mode 通信は、
Resolver により認証された Local GPU Fabric Domain 内部に限り許可される。

Local GPU Fabric Domain は、
CPU PSC または Management PSC により管理されなければならない。

GPU ノードは、
独自に Fast Mode Domain を拡張、
接続、または連結してはならない。

GPU 間 Fast Mode 通信は、
CPU 管理下に存在する同系統 Trusted Local Domain 内部に限定される。

---

## 3.4 Resolver Authority

Fast Mode 利用可否は、
Resolver による認証およびポリシー判定を必要とする。

未認証ノードは Fast Mode 参加を禁止する。

---

## 3.5 Isolation Principle

Fast Mode Domain は、
通常 Routing Domain と分離する。

Fast Mode 内部通信は、
通常 PSC Fabric Routing へ直接流入してはならない。

Fast Mode 通信は、
標準 Routing Telemetry および Routing 制御経路から
論理的に分離可能でなければならない。

---

## 3.6 Physical Port and Domain Limitation

Fast Mode は 1-hop 接続を前提とするため、
同時に接続可能な Fast Mode 対象は、
PSC が持つ物理ポート数、光チャネル数、
または割当可能なレーン数によって制限される。

ただし Fast Mode の制限は、
単純な物理ポート数のみで定義されるものではない。

Fast Mode は、
Resolver により認証された Trusted Local Domain 内部において、
管理可能な範囲でのみ許可される。

Fast Mode の接続規模は、
local port/channel capacity、
Domain 管理能力、
および Security Policy によって制限される。

---

# 4. Allowed Topologies

以下構成を許可対象とする。

- CPU ↔ GPU 直結構成
- CPU ↔ NVMe 高速接続
- Trusted Local GPU Fabric
- Trusted AI Processing Fabric
- Internal Accelerator Fabric
- Shared Memory Pool Fabric
- Trusted Local Memory Fabric

---

# 5. Forbidden Topologies

以下構成は禁止対象とする。

- PSC multi-hop Fast Mode
- Cross-rack Fast Mode
- Internet-routed Fast Mode
- Unknown node participation
- Unauthenticated device access
- External relay routing
- Dynamic unverified topology expansion
- Resolver bypass routing
- Autonomous GPU mesh expansion
- Unmanaged inter-domain Fast Mode bridging

---

# 6. Domain Identification

Fast Mode Domain は、
通常 Routing Domain と分離管理する。

各 Domain は以下情報を持つ。

- Domain ID
- Trust Level
- Resolver Policy ID
- Allowed Node Group
- Security Classification

Resolver は、
通信開始前に Domain 整合性を検証する。

---

# 7. Resolver Involvement

Resolver は Fast Mode 制御において重要な役割を持つ。

Resolver は以下を管理する。

- Fast Mode 利用許可
- Domain 検証
- Trust Validation
- 異常検知
- Fast Mode 停止判断
- Fallback 制御

危険状態検出時、
Resolver は Fast Mode を即時停止可能とする。

---

# 8. Fallback and Recovery

Fast Mode 異常時、
PSC は通常 Routing Mode へ安全に復帰する。

復帰時は以下を実施する。

- Fast Mode 停止
- Routing 再評価
- Trust 再検証
- Resolver 再認証
- Cooldown 適用
- Recovery Procedure 実行

異常状態からの即時再突入は禁止する。

---

# 9. Design Principles

Fast Mode 設計原則を以下とする。

- 高速化より安全性を優先する
- 信頼済みローカル通信のみ許可する
- Resolver による制御権限を維持する
- Domain 境界を明確化する
- Fabric 汚染拡大を防止する
- AI 暴走時の隔離を可能にする
- 通常 Routing への安全復帰を保証する

Fast Mode は、
PSC Fabric 全体を高速化する機能ではない。

Fast Mode は、
限定された安全領域内部のみで許可される、
制限付き高速通信機能である。

Fast Mode は、
PSC Fabric における
「信頼済み高速局所領域」を定義するための機能である。
