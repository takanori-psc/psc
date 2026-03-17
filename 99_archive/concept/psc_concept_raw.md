# PSC コンセプト

## 目的

個人コンピューターの通信管理をCPUから分離し、
将来の光インターコネクトおよびネットワークコンピューター構成への移行を可能にする。
## 背景（Background）

現在の個人用コンピューターは、CPUを中心とした制御構造を採用している。
すべてのデータ転送はCPUまたはCPU管理下のDMAによって制御される。

しかし近年、以下の要因により通信量が急激に増加している：

- GPUによる大規模並列処理
- 高速NVMeストレージの普及
- AI処理の常時実行
- 高速ネットワーク通信

これらの通信をCPUが管理し続けることは、効率および電力消費の観点から限界に近づいている。

この問題を解決するため、通信管理をCPUから分離した新しい制御機構が必要となる。



## 解決策の概要（Overview of the Solution）

PSC（Photon System Controller）は、コンピューター内部および外部の通信管理を専門に担当する独立制御ユニットである。

PSCは以下の機能を持つ：

- モジュール間通信の管理
- 転送経路の確立
- CPU非介入でのデータ転送制御
- 電気および光インターコネクトの両対応

これによりCPUは純粋な処理に専念でき、システム全体の効率が向上する。



## PSCの基本アーキテクチャ（PSC Architecture）

PSCは、システム内の通信管理を専門に行う独立制御ユニットであり、
CPU、GPU、メモリ、ストレージ、ネットワークインターフェース等の各モジュール間の
データ転送を管理する。

PSCは以下の主要構成要素を持つ：

### 1. 転送管理ユニット（Transfer Management Unit, TMU）

各モジュール間のデータ転送要求を管理し、
最適な転送経路を決定する。

### 2. 経路制御ユニット（Routing Control Unit, RCU）

物理的および論理的な通信経路を確立する。
これには電気インターコネクトおよび光インターコネクトの両方が含まれる。

### 3. 転送実行ユニット（Transfer Execution Unit, TEU）

確立された経路に基づき、実際のデータ転送を実行する。
CPUの介入なしに高速なデータ転送を可能にする。

### 4. インターコネクトインターフェース（Interconnect Interface, ICI）

以下のインターコネクトに接続する：

- 電気インターコネクト（PCIe等）
- 光インターコネクト（将来仕様）

これによりPSCは現在のシステムと将来の光ベースシステムの両方に対応可能となる。

### 5. 制御インターフェース（Control Interface）

CPUからの初期設定および管理命令を受け取る。
通常動作時の通信管理はPSCが自律的に実行する。

### 6. 光監視ユニット（Optical Monitoring Unit, OMU）

光インターコネクトを使用する場合、レーザー発信部および受信部の健全性を監視し、
リンク品質を維持するための管理を行う。

OMUは以下を監視・管理する：

- 送信光出力（Tx power）
- 受信光強度（Rx power）
- 温度（レーザーモジュール温度）
- 誤り率統計（BER/FEC）
- リンクの再トレーニングおよび補正

これにより、光リンクの劣化や異常を早期に検出し、
システム全体の安定稼働を支援する。



### 光リンク寿命管理（Optical Link Lifecycle Management）

OMUは光リンクの長期的な劣化状態を監視し、
レーザー発信部および受信部の寿命管理を行う。

監視項目：

- 送信光出力の長期変化
- 受信光強度の長期変化
- レーザーバイアス電流の変化
- 温度履歴
- 誤り率の長期統計
- 累積動作時間

PSCはこれらの情報を基にリンクの劣化状態を判定し、
必要に応じて以下のアクションを実行する：

- CPUまたは管理システムへの警告通知
- 該当ユニットの交換推奨通知
- リンク性能の制限または停止
- 代替経路への切替（利用可能な場合）

これにより、予防保守およびシステム信頼性の維持が可能となる。



## CPUとPSCの関係（Relationship between CPU and PSC）

従来のコンピューターアーキテクチャでは、CPUがシステム全体の制御を担当し、
データ転送の管理もCPUまたはCPU管理下のDMAによって行われていた。

PSCを導入したシステムでは、通信管理機能はCPUからPSCへ移譲される。

CPUの役割：

- 計算処理の実行
- アプリケーションの実行
- PSCへの初期設定および制御命令の送信

PSCの役割：

- モジュール間通信の管理
- データ転送の自律実行
- 転送経路の最適化

これにより、CPUは通信管理から解放され、
純粋な処理ユニットとして機能することが可能となる。

これは、DMAがCPUの負荷を軽減したのと同様に、
PSCがシステム全体の通信管理負荷を軽減する進化形である。

PSCは初期設定後、自律的に通信管理を実行する。
通常の通信動作においてCPUの継続的な介入は不要である。



## PSCを導入したシステム構成（System Architecture with PSC）

PSCを導入したシステムでは、各コンポーネントはPSCを中心とした通信構造を持つ。

従来の構成：

CPU → 各コンポーネントを個別に制御

PSC導入後の構成：

CPU → 処理専用ユニット
PSC → 通信管理専用ユニット

各コンポーネント（GPU、メモリ、ストレージ、ネットワーク）は、
CPUではなくPSCを介して通信を行う。

これにより、以下の利点が得られる：

- CPU負荷の大幅な削減
- 並列通信の効率化
- 通信経路の最適化
- 将来の光インターコネクトへの直接対応

PSCはシステム内の通信ハブとして機能し、
システム全体の通信効率を向上させる。



## ネットワークコンピューターへの進化（Evolution toward Network Computing）

PSCを備えた個人コンピューターは、単なる独立した計算機ではなく、
ネットワーク全体の構成ノードとして機能することが可能となる。

PSCは以下の通信を効率的に管理できる：

- ローカルコンポーネント間通信
- 他のコンピューターとの通信
- 外部ネットワークとの通信

これにより、複数のPSC搭載コンピューターは、
統合された分散コンピューターシステムとして動作することが可能となる。

この構造は、将来の光インターコネクトネットワークにおいて、
極めて高い効率と拡張性を提供する。



## PSCの実装形態（Implementation Model）

PSCは、システム設計および技術進化段階に応じて、複数の実装形態を取ることが可能である。

### 1. 拡張カード型（Expansion Card Model）

PSCはPCIeカード等の拡張カードとして実装される。

特徴：

- 既存のコンピューターに追加可能
- 段階的導入が可能
- 開発および検証が容易

これはPSCの初期導入形態として適している。

### 2. チップセット統合型（Chipset Integration Model）

PSCはマザーボードのチップセットに統合される。

特徴：

- レイテンシの低減
- システム統合性の向上
- 消費電力の最適化

これはPSCの標準実装形態となる。

### 3. CPU統合型（CPU Integrated Model）

PSCはCPU内部に統合される。

特徴：

- 最大の通信効率
- 最小のレイテンシ
- 完全なシステム統合

これは将来の完全統合型アーキテクチャで採用される。

### 4. 独立プロセッサ型（Dedicated Processor Model）

PSCは独立した専用プロセッサとして実装される。

特徴：

- 最大の柔軟性
- 大規模システムへの対応
- ネットワークコンピューティング環境への最適化

これはデータセンターおよび分散コンピューティング環境に適している。



## PSCを導入したシステムの構造図（System Structure Diagram）

図1は、PSCを導入したシステムの基本構造を示す。

この構造では、PSCはシステム内の通信ハブとして機能し、
GPU、メモリ、ストレージ、およびネットワークインターフェース等の
各コンポーネント間の通信を管理する。

CPUはPSCに対して制御および設定を行うが、
通常のデータ転送はPSCによって自律的に管理される。

これにより、CPUは通信管理から解放され、
処理専用ユニットとして動作することが可能となる。

図1：PSCを導入したシステム構造


```text
              [ CPU ]
                 |
                 v
              [ PSC ]
        +----+----+----+----+
        |    |    |    |    |
      GPU   RAM  NVMe Network
```



## PSC内部構造（Internal Architecture）

PSCは複数の内部機能ユニットによって構成され、
これらが連携して通信管理機能を実現する。

図2はPSCの内部構造の概念図を示す。

PSCの主要内部ユニット：

- Transfer Management Unit（TMU）
- Routing Control Unit（RCU）
- Transfer Execution Unit（TEU）
- Interconnect Interface（ICI）
- Control Interface（CI）



### PSC Responsibility Charter（責任分界）

**Resolver（決定権/説明責任）**
- 平時：助言（Recommend）を出す。実行の最終権限は下位層。
- 異常時：強制（Enforce）を出す。ただし目的は全体最適ではなく、異常拡散の防止と局所安定の回復。
- Resolverは「転送を実行しない」「経路計算を独占しない」。

**RCU（経路の生成と評価）**
- トポロジ・リンク状態・混雑状態を元に、候補パス集合を生成し評価する。
- Resolverが出すToken/Budget/ReasonCodeを制約条件として解釈できる。

**FCU / Switching Core（実行と即応）**
- データ転送・スイッチングの最終実行責任を持つ。
- 低遅延の局所制御（キュー/バッファ/スケジューリング）を担う。

**TMU/TEU（転送管理/転送実行）**
- 転送単位の受付・分割・優先・再送・完了管理。
- TEUは最終的な送受を行い、実測テレメトリをOMUへ返す。

**OMU（観測と異常検出）**
- 観測（E/Q/L等）と閾値判定、状態推定（CALM/WARM/HOT/EMERGENCY）を行う。
- Resolver/RCU/FCUに状態イベントを配信する（数値の共有より“状態”共有が優先）。



## PSC Interface Definition（インターフェース定義）

PSC内部ユニット間のインターフェースを以下に定義する。

### 1. TMU ⇄ RCU Interface

目的：
転送要求に対する経路決定要求および結果の受け渡し。

入力（TMU → RCU）：
- TransferRequest { src, dst, size, class, priority }
- Optional Token / Budget constraints

出力（RCU → TMU）：
- PathCandidateList
- SelectedPath
- ReasonCode

---

### 2. RCU ⇄ FCU / Switching Core Interface

目的：
選択された経路の実行設定。

入力：
- PathConfig
- EnforcementRules（Resolver経由）

出力：
- PathActivationStatus
- QueueAssignment

---

### 3. TEU ⇄ ICI Interface

目的：
物理転送の実行。

入力：
- TransferSegment
- TargetLinkID

出力：
- TransferComplete
- RetryRequest
- ErrorSignal

---

### 4. OMU ⇄ Resolver / RCU Interface

目的：
状態共有および異常通知。

出力：
- StateEvent { CALM | WARM | HOT | EMERGENCY }
- TelemetrySummary { E, Q, L }
- LinkHealthStatus

---

### 5. PSC ⇄ CPU Control Interface

目的：
初期設定および管理。

入力：
- ConfigurationCommand
- PolicyUpdate
- ModeChange

出力：
- StatusReport
- FaultNotification
- LifecycleAlert



### 各ユニットの役割（Functional Responsibilities）

 Transfer Management Unit（TMU）：
 通信要求の受付および転送管理を行う。
 転送優先順位の決定および転送スケジューリングを担当する。

 Routing Control Unit（RCU）：
 転送経路の決定および設定を行う。
 電気インターコネクトおよび光インターコネクトの経路制御を行う。

 Transfer Execution Unit（TEU）：
 実際のデータ転送を実行する。
 高効率かつ低レイテンシの転送を実現する。

 Interconnect Interface（ICI）：
 外部インターコネクトとの物理接続を提供する。
 PCIeおよび将来の光インターコネクトに対応する。

 Control Interface（CI）：
 CPUとの制御通信を行う。
 初期設定、状態監視、および制御命令の受信を担当する。

図2：PSC内部構造概念図


```text
             [ Control Interface ]
                      |
                      v
                    [ TMU ]
                      |
                      v
                    [ RCU ]
                      |
                      v
                    [ TEU ]
                      |
                      v
                    [ ICI ]
```



## PSC動作フロー（Operational Flow）

PSCは以下の基本動作フローに従って通信管理を実行する。

1. 通信要求の受信

各コンポーネント（CPU、GPU、ストレージ、ネットワーク等）から
通信要求がInterconnect Interface（ICI）を通じてPSCに送信される。

2. 転送管理

Transfer Management Unit（TMU）が通信要求を受信し、
転送の優先順位およびスケジューリングを決定する。

3. 経路決定

Routing Control Unit（RCU）が最適な転送経路を決定し、
必要なインターコネクト設定を行う。

4. 転送実行

Transfer Execution Unit（TEU）が実際のデータ転送を実行する。

5. 監視および補正

Optical Monitoring Unit（OMU）が光リンクの状態を監視し、
必要に応じて補正または再トレーニングを実行する。

6. 完了通知

転送完了後、PSCは必要に応じてコンポーネントまたはCPUに完了通知を行う。



## 障害検出およびフェイルオーバー（Fault Detection and Failover）

PSCは通信中のリンクおよびコンポーネントの状態を監視し、
異常を検出した場合は適切な対処を行う。

対処例：

- リンク再トレーニング
- 出力補正
- 代替経路への切替
- CPUまたは管理システムへの通知

これにより、システムの継続動作および信頼性が確保される。



## 設計目標（Design Goals）

PSCは以下の設計目標に基づいて設計される：

- 通信管理のCPUからの完全分離
- 高効率かつ低レイテンシ通信の実現
- 光インターコネクトへの対応
- 高い信頼性および保守性
- 将来の分散ネットワークコンピューティングへの対応



## PSC State Model v1（制御状態モデル）

PSCは数値を直接共有する制御系ではなく、
「状態（State）」を共有する分散制御系である。

内部観測値（E/Q/L 等）は直接制御に使用されず、
状態推定を通して抽象化される。

PSCは以下の4状態を持つ。

### 1. CALM

正常状態。
通信は安定しており、局所最適化のみが行われる。

Resolverは助言（Recommend）のみを出す。
強制は行わない。

---

### 2. WARM

軽度負荷上昇または品質劣化の兆候。

局所制御は継続するが、
Resolverは軽度の制約（Token/Budget調整）を出すことができる。

異常拡散防止のための予防的制御段階。

---

### 3. HOT

明確な混雑または品質低下。

Resolverは制御介入を強める。
経路変更、帯域制限、優先制御が発動可能。

局所最適よりも安定回復を優先する。

---

### 4. EMERGENCY

重大な障害または崩壊リスク。

Resolverは強制（Enforce）を発行する。
凍結、遮断、隔離、強制切替を許可。

目的は全体最適ではなく、
「異常の封じ込め」と「局所安定の回復」。

---

## 状態遷移原則（State Transition Principles）

- 状態は単一数値で決定されない。
- ヒステリシスを持つ。
- 上昇遷移と下降遷移は対称でない。
- 数値共有より状態共有を優先する。

例：

CALM → WARM       : E_light または Q_light 超過
WARM → HOT        : E_heavy または Q_heavy 超過
HOT → EMERGENCY   : E_critical または L_critical

EMERGENCY → HOT   : 回復条件 + 時間安定
HOT → WARM        : 低負荷持続
WARM → CALM       : 長時間安定



## 将来拡張（Future Extensions）

PSCは将来の光CPU、光メモリ、および完全光インターコネクトに対応するよう設計される。
