PSC Architecture Specification v0.2（日本語版）

This document is an archived version.
The official specification is:
docs/specification/published/architecture/psc_architecture_spec_v1.0_en.md

Photon System Controller (PSC)

Version: 0.2
Status: Draft
Author: T. Hirose


1. 概要 (Overview)

1.1 目的

Photon System Controller（PSC）は、データ転送管理を中央処理装置（CPU）から分離するために設計された通信およびファブリック制御アーキテクチャである。

現代のコンピュータシステムでは、GPU、ストレージ装置、ネットワークインターフェース、アクセラレータなどの異種コンポーネント間で大量のデータ転送が行われている。

従来のアーキテクチャでは、これらの転送の多くをCPU、またはCPUが管理するDMAエンジンが調整している。

しかし、システムの複雑さと帯域要求が増大するにつれ、この集中型モデルは効率が低下し、CPUに不要な制御負荷を与えるようになる。

PSCは、システムノード間の通信を管理する専用のファブリックコントローラを導入する。
転送制御およびルーティングをPSCに委譲することで、CPUは通信管理の大部分から解放される。

1.2 コンセプト

PSCは、すべてのシステム構成要素を通信ファブリックに接続されたノードとして扱う。

ノードの例：

CPUノード

GPUノード

ストレージノード

ネットワークノード

アクセラレータノード

PSCノード（ファブリックコントローラ）

データ転送は、各操作ごとにCPUの介入を必要とせず、PSCが管理するファブリックを通じてノード間で直接実行される。

PSCは以下の役割を持つ：

高速スイッチングファブリック

分散型転送制御システム

PSCシステムは複数の通信ドメインを持つことができる。

主な通信ドメインは以下である。

PSC Fabric Domain

PSCネイティブ通信環境であり、ノード間転送の主要通信基盤となる。

Optical PCIe Domain

PCIeプロトコルを光リンク上で動作させる互換通信ドメイン。
既存GPUやNVMeなどのPCIeデバイスとの統合を可能にする。

1.3 設計目標

PSCは以下の目標を持って設計されている。

大量データ移動におけるCPU関与の削減

異種コンポーネント間通信のスケーラビリティ確保

マルチパス転送およびストライピング転送のサポート

光インターコネクトとの統合

既存の電気バスアーキテクチャからの段階的移行

大規模コンピュートファブリックの基盤構築

1.4 アーキテクチャ範囲

PSCアーキテクチャは以下を定義する。

ファブリックアドレスとノード識別

ノード発見および起動手順

転送プロトコルとフロー制御

混雑管理とスケジューリング

PSC内部モジュール構造

スケーラブルなファブリックトポロジ

1.5 進化パス

PSCは複数段階で進化するよう設計されている。

初期段階では、PSCはPCIeベースシステムに接続されたブリッジ型ファブリックコントローラとして動作する。

その後、

ハイブリッド環境

完全光ノード環境

へ段階的に移行できる。

この方式により、既存プラットフォームとの互換性を維持しながらPSCを導入できる。


2. 設計思想 (Design Philosophy)

PSCはファブリック中心通信アーキテクチャとして設計されている。

従来のバス拡張ではなく、通信そのものをシステムの基本機能として扱う。

2.1 すべてはノードである (Everything is a Node)

PSCではすべての参加者をノードとして扱う。

例：

CPUノード

GPUノード

ストレージノード

ネットワークノード

アクセラレータノード

PSCノード

PSCは特定デバイスに固定階層を与えない。

通信はノード間で行われる。

2.2 Fabric-First Architecture

従来のコンピュータ

CPU → バス → デバイス

PSC

ファブリック → ノード

通信ファブリックが

ルーティング

混雑管理

転送許可

帯域利用最適化

を担当する。

2.3 受信側主導フロー制御 (Receiver Driven Flow Control)

PSCは受信側主導モデルを採用する。

転送前に

転送要求

受信準備確認

転送許可

データ送信

完了通知

を行う。

2.4 チャンク転送モデル

PSCでは転送を**Chunk（チャンク）**に分割する。

利点：

スケジューリング効率

マルチパス転送

ストライピング

局所再送

2.5 分散型混雑認識

PSCは中央制御を持たない。

各PSCがローカル状態を監視する。

状態モデル：

CALM

WARM

HOT

EMERGENCY

2.6 Local-First Stability

PSCは局所安定化を優先する。

混雑時

ローカル抑制

経路変更

転送制限

を行う。

2.7 段階的導入

PSCは段階的に導入できる。

電気バス環境
↓
ハイブリッド環境
↓
完全光ファブリック


3. 用語定義 (Terminology)

Node

PSCファブリックに接続された任意の計算・通信要素。

PSC Node

通信制御を行うファブリックコントローラ。

Fabric

PSCノードとリンクで構成される通信ネットワーク。

Port

PSCノードの接続インターフェース。

Link

2ポート間通信路。

Transfer

ノード間の論理データ転送。

Chunk

PSC内部の最小転送単位。

Route

PSCファブリック内経路。

Credit

送信許可単位。

Fabric Domain

同一アドレス環境PSC集合。


4. ポートアーキテクチャ

PSCは統一ポートモデルを採用する。

接続可能対象：

compute node

storage node

network node

accelerator node

PSC node

ポート数

PSC基本構成

32ポート

推奨

16 active
16 reserved

4.9 ポートポリシーモデル

PSCポートは統一された物理インターフェースを持つが、
論理ポリシーにより動作を制御できる。

Port Mode

ポートの通信モードを定義する。

例：

PSC_NATIVE

PCIe_TUNNEL

MANAGEMENT


Security Class

ポートの信頼レベルを定義する。

例：

LOCAL_TRUSTED

FABRIC_TRUSTED

EXTERNAL


Policy Profile

ポートに適用される通信ポリシー。

例：

ルーティング制限

帯域制御

転送許可制御

可視性制御


5. ノードアドレス

PSCは階層アドレスを採用する。

Fabric Domain
   ↓
PSC
   ↓
Node

構造

(Fabric Domain ID, PSC ID, Node ID)

PSC UID

128bit

PSC ID

16bit


6. Bootとノード発見

起動時

Hardware Init

Port detection

PSC UID verification

Neighbor discovery

Fabric formation


7. 転送プロトコル

PSC転送

TRANSFER_REQUEST
↓
TRANSFER_GRANT
↓
DATA_CHUNK
↓
TRANSFER_COMPLETE


8. チャンクとフロー制御

推奨Chunk

4KB
8KB
16KB
64KB

PSCは

credit-based flow control

を採用。


9. SchedulerとResolver

Scheduler

転送選択

帯域割当

Resolver

混雑検知

制御ポリシー

状態

CALM
WARM
HOT
EMERGENCY


10. PSC内部構造

PSC内部モジュール

RCU (Routing Control Unit)

TMU (Transfer Management Unit)

TEU (Transfer Execution Unit)

OMU (Optical Monitoring Unit)

Scheduler

Resolver

SPU (Security Policy Unit)

SPUはPSC内部のセキュリティポリシーを管理するモジュールである。

主な役割：

ポートセキュリティ分類

ドメイン分離制御

転送認可確認

ポリシー評価

PSC転送パイプライン

ノード転送要求
      │
      ▼
+------------+
|  Resolver  |
+------------+
      │
      ▼
+-------------+
|  Scheduler  |
+-------------+
      │
      ▼
+----------------------+
| SPU (Security Policy)|
| セキュリティポリシー |
+----------------------+
      │
      ▼
+----------------------+
| RCU ルーティング制御 |
+----------------------+
      │
      ▼
+----------------------+
| TMU 転送管理ユニット |
+----------------------+
      │
      ▼
+----------------------+
| TEU 転送実行ユニット |
+----------------------+
      │
      ▼
+----------------------+
| PSC Fabric Switching |
|        Core          |
+----------------------+
      │
      ▼
        PSC Fabric


11. Fabricトポロジ

PSCは以下をサポート

single PSC

multi PSC fabric

partial mesh

hierarchical


12. 実装フェーズ

Phase1

PCIe接続PSC

Phase2

Hybrid Fabric

Phase3

Native PSC Fabric

Phase4

Optical Fabric


13. 今後の研究

将来の研究領域

高度混雑制御

スケジューリング改善

大規模Fabric

光デバイス統合

Fabric OS

14. Open Design Items（設計上の未確定事項）

以下の項目は、PSCプロトコル初期設計段階で確認された設計課題であり、
今後の仕様改訂において整理および明確化される予定である。


14.1 Domain Naming Alignment

PSC Port Model における Domain Scope と、
PSC Packet 構造における Fabric Domain フィールドの命名および
分類体系は、将来の仕様改訂において整合させる必要がある。


14.2 Trust Level Definition

Security Tag 内の Trust Level フィールドの定義とライフサイクルは
今後明確化される必要がある。

Trust Level は以下のいずれか、または組み合わせにより
決定される可能性がある。

- Port Security Class
- セッション認証結果
- 動的ポリシー評価


14.3 Sequence Number と Chunk ID の意味の分離

Sequence Number と Chunk ID の機能的役割は
マルチパス転送および再順序処理をサポートするために
明確に区別して定義する必要がある。


14.4 Integrity Tag Coverage

Integrity Tag が保護する範囲について、
今後仕様として定義する必要がある。

候補として以下が考えられる。

- パケットヘッダのみを保護
- パケット全体（ペイロードを含む）を保護

End of PSC Architecture Specification v0.2

