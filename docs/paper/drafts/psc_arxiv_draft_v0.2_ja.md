# PSC：高帯域コンピューティングファブリック向け

# Trust-Aware 安定化制御アーキテクチャ

T. Hirose

arXiv投稿向けドラフト v0.2

---

## Abstract（概要）

現代のコンピューティングシステムは、CPU、GPU、メモリ、ストレージ、アクセラレータ、およびネットワークインタフェース間における高帯域通信への依存を急速に強めている。デバイス並列性およびデータ移動量が増加し続ける中、CPU中心型の通信管理や、純粋に性能のみを追従するルーティング方式は、輻輳、不安定リンク、経路振動、および連鎖障害へ increasingly exposed となっている。

本論文では PSC（Photon System Controller）を提案する。PSC は、通信管理を CPU から分離し、Fabric 内部へ Trust-aware かつ状態遷移ベースのルーティング安定化制御を導入する、Fabric-centric 通信制御アーキテクチャである。

PSC は以下の三機能を分離して構成される：

- Transfer Management
- Routing Control
- Transfer Execution

Routing Control Unit（RCU）は高速な局所経路評価を行い、上位 Resolver が曖昧・劣化・ポリシー競合状態を調停する。

PSC は、瞬間スコアのみを追従する従来型ルーティングとは異なり：

- 現在最良スコア経路
- 実際に運用中の経路

を明確に分離し、

- hysteresis
- trust validation
- recovery guard
- cooldown rule

を適用することで、不必要な切替を抑制する。

本論文では：

- PSC architecture
- RCU decision model
- Resolver arbitration model
- telemetry / trust assumptions
- trusted local communication 用 Fast Mode security boundary

を説明する。

制御シミュレーションでは、PSC は ECMP 的 score-following baseline と比較して routing oscillation を抑制することを確認した。

ある不安定経路シナリオでは：

| Method             | Switches (10 steps) |
| ------------------ | ------------------- |
| ECMP-like baseline | 9                   |
| PSC                | 1                   |

となり、PSC は一度のみ切替を行った後、安定経路を維持した。

さらに degraded fallback および staged recovery return も検証した。

本結果は preliminary ではあるが、PSC の中心思想：

```text
短期性能最大化より、
Fabric stability、
Explainability、
Controlled recovery
を優先する
```

ことを示している。

---

## 1. Introduction

高性能コンピューティングシステムは、 increasingly data movement dominated な構造へ移行している。

CPU、GPU、メモリプール、NVMe、アクセラレータ、およびネットワークインタフェースは、従来の host-centric 制御モデルを超える速度でデータ交換を行っている。

多くの従来型システムでは：

- CPU
- CPU管理 DMA

がデータ移動の開始・監視・調停を担ってきた。

しかしこの構造は：

- always-on AI workload
- GPU-to-GPU communication
- high-speed storage
- low-latency fabric

によって限界へ近づいている。

PSC は、異なる設計方向を提案する。

すなわち：

```text
通信管理そのものを、
Fabric の第一級機能へ昇格させる
```

という方向である。

PSC は interconnect を単なる受動転送路として扱わず：

- state evaluation
- route selection
- policy enforcement
- fault containment
- degradation recovery

を実施可能な active control layer として扱う。

PSC の中心思想は：

```text
瞬間スループット最大化
```

ではない。

むしろ：

- stable
- explainable
- policy-consistent

な通信維持を目的とする。

特に大規模 heterogeneous fabric では、短期 score 変化へ過敏に反応すると：

- route oscillation
- instability
- cascading control behavior

が発生する。

本論文の主な貢献は以下である：

1. transfer management / route control / transfer execution を分離した Fabric-centric communication architecture として PSC を提案

2. candidate filtering / route scoring / switching / degraded fallback / recovery を分離した RCU decision model を定義

3. ambiguity / trust conflict / degraded operation / recovery return を扱う explainable arbitration layer として Resolver を定義

4. oscillation suppression / degraded fallback / staged recovery を示す controlled simulation result を提示

---

## 2. Motivation and Problem Statement

高帯域 computing fabric は、以下の recurring control problem を抱える：

- local / fabric-wide congestion
- unstable or flapping links
- over-reactive path selection による routing oscillation
- policy / security boundary conflict
- node / link / telemetry source trust degradation
- unsafe recovery
- local failure の fabric-wide propagation

従来 routing / load-balancing は：

- reachability
- shortest path
- cost minimization
- load distribution

を重視してきた。

しかし Fabric instability 環境では、それだけでは不十分である。

瞬間的 best score path が：

- low trust
- high variance
- recent failure history

を持つ場合、それは operationally unsafe となり得る。

同様に recovery path も：

```
回復した = 即 traffic 復帰可能
```

ではない。

PSC は routing を：

```text
純粋最適化問題
```

ではなく、

```text
stability-preserving control problem
```

として扱う。

Fabric は：

```
今どの経路が最良か
```

だけでなく、

```text
今切り替えるべきか
```

を判断しなければならない。
