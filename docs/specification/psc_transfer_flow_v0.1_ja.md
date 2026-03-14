# PSC Transfer Flow v0.1

## 1. 目的

PSC Transfer Flow は、PSC Fabric 内におけるデータ転送の動作モデルを定義する。

本仕様は、転送がどのように開始され、認可され、スケジュールされ、
送信され、確認され、再送され、完了するかを、
PSC の受信側主導かつチャンクベースの通信モデルに基づいて記述する。

本仕様は、パケットフォーマットそのものではなく、
転送ライフサイクルの挙動に重点を置く。

---

## 2. 設計原則

PSC Transfer Flow は以下の原則に基づく。

- 受信側主導の転送認可
- チャンクベース転送
- クレジットベースフロー制御
- ポリシー考慮型スケジューリング
- 混雑時の適応的ルーティング
- 局所的な再送と回復

PSC は、転送を単一の巨大な処理として扱わない。
代わりに、各転送は状態遷移とチャンク単位処理から成る
制御されたシーケンスとして管理される。

---

## 3. 転送モデル概要

PSC の転送は、概ね以下の段階で進行する。

1. Transfer Request
2. Transfer Evaluation
3. Transfer Grant
4. Transfer Scheduling
5. Chunk Transmission
6. Acknowledgement and Credit Update
7. Completion
8. 必要に応じて Retry または Abort

このモデルにより、受信側が転送条件を受理していない限り、
データは送信されない。

---

## 4. 主要エンティティ

以下の要素が PSC Transfer Flow に関与する。

### Source Node
転送されるデータを保持または提供するノード。

### Destination Node
データを受信するノード。

### Source PSC
送信側で転送動作を調整する PSC。

### Destination PSC
受信側で転送受理を判定する PSC。

### Resolver
ファブリック状態およびポリシー制約を評価する。

### Scheduler
転送実行のタイミングと優先度を決定する。

### SPU
セキュリティおよびドメイン越境規則を検証する。

### RCU
経路およびルーティング動作を選択する。

### TMU
転送コンテキストを生成し追跡する。

### TEU
チャンク送受信を実行する。

---

## 5. 転送状態

PSC Transfer Flow は以下の初期状態モデルを用いる。

### IDLE
有効な転送コンテキストが存在しない状態。

### REQUESTED
転送要求が発行されたが、まだ受理されていない状態。

### EVALUATING
受信側が資源、ポリシー、準備状況を検証している状態。

### GRANTED
転送が認可され、必要資源が確保された状態。

### SCHEDULED
Scheduler ポリシーに従い実行待ちとなっている状態。

### ACTIVE
チャンク送信中の状態。

### PAUSED
ポリシー、混雑、資源制約などにより一時停止された状態。

### RETRY
失敗したチャンクまたは転送区間を再送中の状態。

### COMPLETING
最終チャンク配送後、完了処理を行っている状態。

### COMPLETED
転送が正常終了した状態。

### ABORTED
完了前に転送が中止された状態。

### FAULTED
回復不能な異常またはセキュリティ違反が発生した状態。

---

## 6. 転送状態機械

典型的な PSC 転送は以下の流れを取る。

IDLE
→ REQUESTED
→ EVALUATING
→ GRANTED
→ SCHEDULED
→ ACTIVE
→ COMPLETING
→ COMPLETED

派生パスとして以下があり得る。

- ACTIVE → PAUSED
- PAUSED → ACTIVE
- ACTIVE → RETRY
- RETRY → ACTIVE
- REQUESTED → ABORTED
- EVALUATING → ABORTED
- ACTIVE → ABORTED
- ACTIVE → FAULTED

---

## 7. Transfer Request フェーズ

PSC の受信側主導モデルでは、
転送は受信側の要求または認可に基づいて開始される。

要求段階では以下を含む。

- source node 識別
- destination node 識別
- 要求転送サイズ
- transfer type
- priority class
- セキュリティおよびドメイン検証コンテキスト
- 希望ポリシーヒント

Transfer Request は実行保証ではない。
これは候補となる転送コンテキストを生成するだけである。

---

## 8. Transfer Evaluation フェーズ

評価段階では、destination PSC が
転送続行可否を判定する。

評価項目は以下を含む。

- 受信バッファ空き容量
- フロークレジット容量
- セキュリティポリシー検証
- ドメイン越境認可
- destination node の準備状態
- 現在の混雑状態
- 経路成立性

評価結果は以下になり得る。

- grant
- defer
- reject
- quarantine

---

## 9. Transfer Grant フェーズ

評価に成功した場合、受信側は transfer grant を発行する。

grant は転送の初期動作条件を定義する。

含まれ得る内容：

- transfer identifier
- 許可チャンクサイズ
- 初期クレジット割当
- 許可経路スコープ
- セキュリティ強制レベル
- policy profile
- retry 制限

grant 発行後、その転送はスケジューリング対象となる。

---

## 10. Scheduling フェーズ

Scheduler は、認可済み転送をいつ実行するか決定する。

判断要素は以下を含む。

- priority class
- policy profile
- congestion state
- route availability
- credit availability
- transfer type
- ローカルキュー深度

PSC のスケジューリングは単純な最大スループット志向ではない。
安定性考慮型かつポリシー考慮型である。

例：

- memory 系トラフィックは低遅延優先
- bulk storage 系トラフィックはスループット整形
- secure または quarantined トラフィックは遅延または隔離

---

## 11. Active Transfer フェーズ

スケジュールされると、転送は ACTIVE 状態へ入る。

ACTIVE 状態では：

- TEU がチャンク送信を行う
- RCU が経路を選択する
- TMU / TEU がクレジット制限を強制する
- SPU がセキュリティ規則を維持する
- Scheduler が必要に応じて送信形状を制御する

少なくとも1つのチャンクが
送信中、飛行中、または確認待ちである間、
転送は ACTIVE に留まる。

---

## 12. チャンク送信モデル

PSC の転送はチャンク単位で実行される。

各チャンクは以下を持つ制御対象の輸送要素である。

- chunk identity
- 転送内オフセット
- transfer association
- route selection
- credit cost
- acknowledgement status

チャンクベース実行の利点：

- 細粒度スケジューリング
- マルチパス分散
- 選択的再送
- 局所的混雑適応

---

## 13. クレジットフロー制御

PSC は受信側管理のクレジットフロー制御を採用する。

受信側は送信許可量を credit unit で通知する。

### Credit Rules

1. 十分な credit がなければチャンク送信はできない。
2. チャンク送信時に credit は消費される。
3. 受信側が進行を受理すると credit は返却または更新される。
4. 混雑時には credit policy を厳しくできる。
5. PAUSED や security-restricted 状態では credit を凍結できる。

これにより受信側オーバーフローを防ぎ、送信速度を安定化できる。

---

## 14. Acknowledgement モデル

PSC はチャンク進行確認と再送判断のために acknowledgement を用いる。

acknowledgement はチャンク粒度で動作可能とする。

主な結果：

- accepted
- delayed
- rejected
- integrity failure
- policy violation

acknowledgement は以下にも用いられる。

- credit refresh
- progress tracking
- completion detection
- retry trigger

---

## 15. Pause / Resume 動作

継続実行が一時的に不適切または危険な場合、
転送は PAUSED 状態へ入ることがある。

主な要因：

- 混雑悪化
- credit 枯渇
- 経路不安定
- 受信側圧力
- ポリシー制限
- セキュリティ検査

以下が回復すれば resume できる。

- credit 回復
- 混雑緩和
- 経路正常化
- ポリシー許可

pause は failure を意味しない。

---

## 16. Retry モデル

PSC は可能な限り、
転送全体のやり直しではなく局所再送を行う。

再送は以下の場合に発生し得る。

- chunk loss が検出された場合
- integrity verification failure
- link failure により転送が中断した場合
- 一時的経路障害

### Retry Rules

1. 可能なら失敗チャンクのみ再送する。
2. 再送経路は元経路と異なってよい。
3. retry budget は transfer ごとに追跡する。
4. 継続的失敗は ABORTED または FAULTED へ昇格し得る。
5. セキュリティ由来の失敗は再送を省略し fault へ直行し得る。

このモデルは効率と耐障害性を向上させる。

---

## 17. Abort と Fault 処理

### ABORTED
完了前に意図的終了された状態。

主な理由：

- sender cancellation
- receiver rejection
- timeout
- administrative policy
- unrecoverable congestion

### FAULTED
重大または不正条件が発生した状態。

主な理由：

- security violation
- repeated integrity failure
- unrecoverable route collapse
- illegal state transition
- internal PSC malfunction

ABORTED と FAULTED は異なる。
Abort は制御された終了、
Fault は異常終了である。

---

## 18. Completion フェーズ

必要な全チャンクが配送・受理されると、
転送は COMPLETING に入る。

完了処理は以下を含む。

- 最終 acknowledgement 検証
- transfer accounting update
- 資源解放
- credit reconciliation
- telemetry update

成功すれば COMPLETED へ遷移する。

---

## 19. マルチパス転送動作

ポリシーとトポロジが許せば、
PSC はチャンクを複数経路に分散できる。

マルチパスの利点：

- スループット向上
- リンク利用率向上
- 耐障害性向上

必要条件：

- chunk identity 保持
- acknowledgement tracking
- 再順序許容
- route-aware retry behavior

HOT または EMERGENCY では、
回復目的でない限りマルチパスを抑制・制限すべきである。

---

## 20. 混雑状態との連動

転送挙動は PSC fabric state に適応しなければならない。

### CALM
- 通常スケジューリング
- 通常 credit 発行
- multipath 許可
- throughput 最適化許可

### WARM
- 中程度の shaping
- 強い striping の抑制
- 安定経路優先
- 選択的転送許可制御

### HOT
- より厳しい admission control
- 同時転送数削減
- 優先度強制
- 低優先度転送 pause の可能性

### EMERGENCY
- 必須トラフィックのみ優先
- 非重要転送は停止または拒否
- 強い局所安定化
- quarantine / protection 動作有効化

---

## 21. 転送制御の責務分担

各 PSC モジュールは以下の役割を持つ。

### Resolver
ファブリック状態に照らして転送適格性を判断する。

### Scheduler
転送実行タイミングを決める。

### SPU
セキュリティおよびドメイン規則を検証する。

### RCU
経路選択とパス適応を行う。

### TMU
転送状態、credit、retry context を保持する。

### TEU
チャンク送受信動作を実行する。

### OMU
リンク劣化情報を通知し適応に反映させる。

### Telemetry / Fault Monitor
進行状況、異常、エスカレーションを記録する。

---

## 22. 初期転送ポリシールール

### Rule 1
すべての transfer はちょうど1つの Transfer ID を持つ。

### Rule 2
grant なしに ACTIVE に入ってはならない。

### Rule 3
利用可能 credit なしに chunk を送信してはならない。

### Rule 4
paused transfer は明示 abort されない限り context を保持する。

### Rule 5
retry 時に経路が変わっても transfer identity は保持する。

### Rule 6
security policy は performance policy に優先し得る。

### Rule 7
FAULTED 状態の transfer は直接 ACTIVE に戻ってはならない。

### Rule 8
completion には配送進行だけでなく受理確認も必要である。

---

## 23. 転送フロー例

例：

1. Destination が block transfer を要求する。
2. destination PSC がバッファとポリシー準備を評価する。
3. chunk size と初期 credit を含む grant を発行する。
4. Scheduler が実行順に配置する。
5. TEU がチャンク送信を行う。
6. 受信側が受理済みチャンクを acknowledge し credit を返す。
7. 1つのチャンクが integrity verification に失敗する。
8. そのチャンクのみ別経路で retry する。
9. 残りチャンクが正常完了する。
10. transfer は COMPLETING を経て COMPLETED へ入る。

---

## 24. 設計上の意義

PSC Transfer Flow は以下の利点を持つ。

1. Receiver-safe transfer execution  
   受信準備が整わない限りデータを送らない。

2. Chunk-level adaptability  
   転送を細粒度で調整、再送、迂回できる。

3. Congestion-aware behavior  
   実際のファブリック状態に応じて転送が適応する。

4. Policy-native communication  
   セキュリティとドメイン規則が転送全体を通じて有効である。

---

## 25. Open Design Notes

今後の詳細化対象：

- grant message の正確な構造
- acknowledgement の詳細符号化
- retry budget policy
- timeout model
- multipath 時の再順序処理
- Trust Level と transfer admission の関係
