# PSC Fast Mode Flow Buffer Model v0.1

## 1. Document Information

- Document Name : PSC Fast Mode Flow Buffer Model
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Fast Mode / Flow Buffer
- Document Type : Design Draft
- Status : Draft
- Language : Japanese

- Related Models:
  - PSC Fast Mode Bundle Capacity Control v0.1
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC Recovery Return Abort Handling v0.1
  - PSC Telemetry Model v0.2

---

## 2. 目的

本ドラフトは、Fast Mode における Flow Buffer の役割、PSC の責務分離、
および運用モデルを整理するための概念モデルである。

Flow Buffer の主目的は、Fast Mode の安定運用である。
Fast Mode では、光リンク上の瞬間的な転送揺らぎ、lane 間の微小な到着差、
GPU 側の DMA 受信や処理タイミングの揺らぎが発生し得る。
Flow Buffer はこれらの短時間の変動を吸収し、Basket Stream の連続転送を
安定して維持するための調整領域として機能する。

Flow Buffer は PSC 本体から分離されるべきである。
PSC は control plane として状態監視、傾向把握、policy 判断、Pause / Abort 判断を行う。
一方、Flow Buffer の FIFO 管理、メモリ管理、DMA 制御、GPU 向け転送は
data movement に近い実装責務であり、PSC の主制御 logic と密結合すべきではない。

この分離により、PSC は Flow Buffer の内部実装に依存せず、
状態情報に基づく安定性判断だけを行える。

---

## 3. 範囲

本ドラフトは以下を扱う。

- Fast Mode における Flow Buffer の基本役割
- Flow Buffer を PSC 本体から分離する理由
- PSC と Flow Buffer Manager の責務分離
- Flow Buffer の hardware independence
- Flow Buffer の monitoring model
- Flow Buffer 起因または関連する例外処理
- Flow Buffer 状態ログの利用方針

本ドラフトは以下を定義しない。

- Flow Buffer の具体的な容量値
- production threshold
- メモリ種別ごとの実装方式
- DMA engine の詳細仕様
- GPU 側 queueing algorithm
- simulation 実装
- Evidence Matrix entries

---

## 4. Fast Mode Basic Principle

Fast Mode は以下の基本遷移を持つ。

```text
START
↓
STREAM
↓
COMPLETE
```

Fast Mode は、事前に確立された trusted channel 上で動作する。
通常状態では、Basket Stream の転送中に PSC の継続的な介入を必要としない。

Fast Mode の基本動作は以下である。

- 事前確立チャネルを使用する
- START 後、Basket Stream を連続転送する
- 通常時は PSC の per-basket intervention を要求しない
- COMPLETE により転送単位を終了する

PSC は Fast Mode の通常転送 path に常時介入するのではなく、
状態監視と例外判断に集中する。

---

## 5. Flow Buffer Concept

Flow Buffer は、Fast Mode の転送 path における短時間の流量変動を吸収するための
buffering component である。

Flow Buffer の目的は以下である。

- 瞬間的な転送揺らぎ吸収
- GPU 側処理遅延吸収
- Fast Mode 安定化

Flow Buffer は「調整池」または「平滑化バッファ」として機能する。
source 側から到着する Basket Stream と、GPU 側または device 側が実際に
消費できる rate の間に短時間の差が生じた場合、Flow Buffer はその差分を一時的に吸収する。

通常状態では、Flow Buffer は空に近い状態を維持すべきである。
Flow Buffer が常時高い occupancy を維持している場合、それは一時的な揺らぎではなく、
capacity mismatch、GPU 側処理遅延、DMA congestion、または link / trust degradation の
兆候である可能性がある。

Flow Buffer は throughput を恒常的に増やすための蓄積領域ではない。
Fast Mode の安定運用において、Flow Buffer は短時間の jitter を吸収する safety component として扱う。

---

## 6. Responsibility Separation

PSC と Flow Buffer Manager は、責務を明確に分離する。

### 6.1 PSC の責務

PSC は Flow Buffer の状態を control plane から監視し、必要な判断を行う。

PSC の責務は以下である。

- Occupancy 監視
- Trend 監視
- Alert 判定
- Pause / Abort 判断

PSC は Flow Buffer の内部処理を管理しない。
PSC は FIFO pointer、memory allocation、DMA descriptor、GPU 向け転送順序などを
直接制御しない。

### 6.2 Flow Buffer Manager の責務

Flow Buffer Manager は Flow Buffer の実データ処理を管理する。

Flow Buffer Manager の責務は以下である。

- FIFO 管理
- メモリ管理
- DMA 制御
- GPU 向け転送

Flow Buffer Manager は、PSC に対して monitoring に必要な状態情報を提供する。
ただし、Fast Mode の Pause、Rate Down、Abort のような control decision は
PSC の判断領域である。

---

## 7. Hardware Independence

Flow Buffer は、特定の memory technology に依存しない概念 component として定義する。

Flow Buffer は以下の実装を許容する。

- DDR5
- DDR6
- HBM
- MRAM
- 将来の Optical Memory

PSC は Flow Buffer の内部 memory technology を前提にして判断してはならない。
PSC が監視するのは、Flow Buffer Manager から提供される状態情報である。

このため、PSC の control logic は以下のような hardware-independent な情報に基づくべきである。

- current occupancy
- occupancy trend
- fill / drain behavior
- health state
- alert state

memory technology 固有の latency、retention、wear、bandwidth、thermal behavior は、
Flow Buffer Manager または lower implementation layer が吸収する。

---

## 8. Monitoring Model

PSC は Flow Buffer の内部処理ではなく、運用状態を監視する。

Flow Buffer monitoring の例は以下である。

| Metric | Meaning |
|--------|---------|
| Current Occupancy | 現在の Flow Buffer 使用量 |
| Peak Occupancy | 観測 window 内の最大使用量 |
| Fill Rate | source 側から Flow Buffer へ流入する rate |
| Drain Rate | Flow Buffer から GPU / device 側へ流出する rate |
| Health State | Flow Buffer Manager が報告する health |

PSC はこれらの状態から、Flow Buffer が一時的な揺らぎを吸収しているのか、
継続的な capacity mismatch に近づいているのかを判断する。

特に、以下のような傾向は PSC の注意対象となる。

- Current Occupancy が継続的に増加する
- Peak Occupancy が繰り返し高い水準に到達する
- Fill Rate が Drain Rate を長時間上回る
- Health State が degraded または unstable を示す

本ドラフトでは具体的な threshold は定義しない。

---

## 9. Exception Handling

Flow Buffer または周辺状態が unsafe になる場合、PSC は Fast Mode の継続可否を判断する。

例外条件の例は以下である。

- Buffer Critical
- Hardware Failure
- Link Failure
- Trust Degradation

PSC は必要に応じて以下を実施できる。

```text
PAUSE
RATE DOWN
ABORT
```

### 9.1 PAUSE

PAUSE は、Fast Mode の転送を一時停止し、Flow Buffer の drain、
状態観測、または Resolver / policy review の時間を確保するために使用する。

### 9.2 RATE DOWN

RATE DOWN は、source 側の offered traffic を低減し、
Flow Buffer occupancy の上昇を抑えるために使用する。

RATE DOWN は、Flow Buffer がまだ critical failure ではないが、
trend と health state が安定運用上のリスクを示している場合に有効である。

### 9.3 ABORT

ABORT は、Fast Mode の継続が unsafe である場合に使用する。

例:

- Flow Buffer が critical state に到達した
- hardware failure により Flow Buffer の信頼性が維持できない
- link failure により Basket Stream の継続性が失われた
- trust degradation により Fast Mode boundary を維持できない

ABORT 後の復帰や fallback の詳細は、Recovery Return および Abort Handling 側のモデルに委ねる。

---

## 10. Logging

Flow Buffer 状態はログ対象とする。

Flow Buffer state の例は以下である。

```text
NORMAL
ELEVATED
HIGH
CRITICAL
```

ログには、少なくとも以下のような情報を含めることが望ましい。

- timestamp
- Flow Buffer state
- current occupancy
- peak occupancy
- fill rate
- drain rate
- health state
- PSC action

Flow Buffer log は、設備改善および容量設計に利用する。
特に、Peak Occupancy、Fill Rate、Drain Rate、RATE DOWN 発生頻度、
PAUSE / ABORT 発生条件は、将来の capacity planning と simulation input になる。

---

## 11. Future Work

本ドラフトでは Flow Buffer State Threshold の固定値を定義しない。

Flow Buffer の threshold、state transition、capacity margin、RATE DOWN 条件、
PAUSE 条件、ABORT 条件は、将来の simulation により決定する。

将来の作業は以下である。

1. Flow Buffer occupancy simulation を定義する。
2. Basket Stream rate と GPU drain behavior の simulation model を作成する。
3. NORMAL / ELEVATED / HIGH / CRITICAL の state transition 条件を検証する。
4. Flow Buffer log を capacity planning input として整理する。
5. Hardware implementation ごとの monitoring abstraction を定義する。

本書では概念モデルのみ定義する。
