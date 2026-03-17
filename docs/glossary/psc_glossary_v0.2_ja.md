PSC Terminology

PSC Glossary v0.2

Core System
PSC

Photon System Controller

光ファブリック通信を制御する通信プロセッサ。
従来の CPU-centric bus architecture を
fabric-driven architecture に置き換える。

PSC Fabric

PSCが管理する通信ファブリック。

特徴

ノード接続

分散通信

ルーティング可能

chunk transport

receiver-driven transfer

将来的には GAIOSネットワークの基盤になる。

Fabric-driven Architecture

コンピュータの通信を
CPUバスではなく ファブリックネットワークで構成する設計。

Optical Interconnect Types

PSCでは光通信を 2つの領域に分けて扱う。

Optical PCIe Domain

PCI Express プロトコルを
光リンク上で伝送する領域。

Protocol : PCIe
Medium   : Optical

役割

既存PCIe互換

GPU / NVMe接続

OS / Driver互換維持

セキュリティ

Trusted Local Domain

外部ネットワークからは直接到達できない。

PSC Fabric Domain

PSCが制御するネイティブ通信ファブリック。

Protocol : PSC Fabric Protocol
Medium   : Optical

特徴

ノード通信

Fabric routing

chunk transport

policy control

用途

ブレード間通信

ラック内通信

クラスタ通信

GAIOSネットワーク

Optical Interconnect Comparison
	Optical PCIe	PSC Fabric
Architecture	CPU bus	Fabric network
Protocol	PCIe	PSC Fabric Protocol
Control	CPU Root Complex	PSC
Security Scope	Trusted Local	Compute Network
Exposure	Internal	Potentially external
PSC Port Model

PSCの全ファブリックポートは
共通物理仕様を持つ。

ポートの役割は
論理設定によって決定される。

Port Mode

ポートが使用する通信モード。

例

PSC_NATIVE
PCIe_TUNNEL
PCIe_BRIDGE
MANAGEMENT
Security Class

ポートの信頼レベル。

例

LOCAL_TRUSTED
RACK_TRUSTED
CLUSTER_TRUSTED
EXTERNAL_PUBLIC
Policy Profile

ポート通信の許可ルール。

制御項目

接続許可ドメイン

転送方向

帯域制限

経路制御

可視性

Security Domains

PSC Fabricでは
通信範囲をドメインで分離する。

Trusted Device Domain

ノード内部の信頼領域。

例

CPU

Memory

GPU

NVMe

外部から直接アクセス不可。

Fabric Domain

PSC間通信を行う計算ファブリック。

例

ブレード間通信

ラック内通信

クラスタ通信

Open Network Domain

GAIOSネットワーク接続領域。

外部ノードと通信可能。

PSC Internal Modules
Resolver

転送要求の評価と制御方針決定。

Scheduler

転送スケジューリング。

RCU

Routing Control Unit

ファブリック経路計算。

TMU

Transfer Management Unit

転送管理。

chunk分割

フロー制御

TEU

Transfer Execution Unit

データ転送実行。

OMU

Optical Monitoring Unit

光リンク監視。

Telemetry / Fault Monitor

システム監視と故障検出。

SPU

Security Policy Unit

セキュリティポリシー管理。

ポート属性管理

ドメイン制御

アクセス判定

隔離制御

Transfer Model
Receiver-driven Transfer

受信側が転送を制御。

Chunk Transport

データをチャンク単位で転送。

Credit Flow Control

バッファベースのフロー制御。

Fabric State Model

CALM
低負荷状態

WARM
負荷増加

HOT
高負荷状態

EMERGENCY
異常状態

Fabric Topology

Mesh

Hierarchical Fabric

Spine-Leaf Fabric

Implementation Phases

Phase1
PCIe Bridge PSC

Phase2
Hybrid Fabric

Phase3
Native PSC Fabric

Phase4
Optical Fabric
