# PSC Fabric State Model v0.1

## ドキュメント情報

- ドキュメント名   : PSC Fabric State Model
- バージョン       : v0.1
- プロジェクト     : PSC / Photon System Controller
- レイヤ           : PSC Fabric
- ドキュメント種別 : 仕様書
- ステータス       : Draft
- 作成者           : T. Hirose
- 作成日           : 2026-03
- 最終更新         : 2026-03
- 言語             : Japanese

---

## 1. 目的

本ドキュメントは PSC Fabric における **Fabric State Model** を定義する。

Fabric State Model は、PSC Fabric の状態を **簡潔で安定した状態表現**として定義し、以下の制御機能の共通基盤として使用される。

- routing decision
- congestion control
- fabric monitoring
- control node policy
- telemetry interpretation
- optimization interaction

PSC では数値最適化のみを用いるのではなく、
**state-based control** に基づく制御モデルを採用する。

これにより PSC Fabric は

- 安定した挙動
- 制御の単純化
- 状態の理解容易性

を実現する。

---

## 2. 状態モデル思想

PSC Fabric は内部的には多くの数値情報を扱う。

例:

- link utilization
- queue depth
- latency
- packet retry
- error rate
- thermal condition

しかし PSC の制御判断は、
これらの数値を直接使用するのではなく **Fabric State** に変換して行う。

```
Telemetry Metrics
        ↓
State Evaluation
        ↓
Fabric State
        ↓
Routing / Control / Policy
```

Fabric State の評価は、Telemetry 情報に基づき
PSC Fabric Node、Routing Control Unit (RCU)、または Control Node によって実行される場合がある。

これにより PSC Fabric は中央集権的制御に依存せず、
分散的かつ自律的な状態評価を行うことができる。

この設計により PSC は

- 過度な数値最適化を避ける
- 制御安定性を確保する
- 実装を簡潔に保つ

ことができる。

---

## 3. Official Fabric State Levels（公式 Fabric 状態）

PSC Fabric の公式状態は以下の **4段階**とする。

| State     | Description                             |
| --------- | --------------------------------------- |
| CALM      | Fabric が安定しており、負荷が低い状態   |
| WARM      | Fabric が通常負荷で稼働している状態     |
| HOT       | Fabric が高負荷または混雑状態に近い状態 |
| EMERGENCY | Fabric の深刻な混雑または障害状態       |

これらの状態は

- Routing decisions
- Congestion avoidance
- Control node actions

などに利用される。

---

## 4. Fabric State の意味

### 4.1 CALM

CALM 状態は Fabric が **低負荷で安定している状態**である。

特徴

- low utilization
- minimal congestion
- stable latency

Routing では通常、CALM 経路が優先される。

---

### 4.2 WARM

WARM 状態は Fabric が **通常稼働状態**である。

特徴

- moderate utilization
- normal latency
- stable throughput

PSC Fabric の通常運用はこの状態を想定する。

---

### 4.3 HOT

HOT 状態は Fabric が **高負荷状態**にあることを示す。

特徴

- high utilization
- queue buildup
- congestion risk

Routing は HOT 経路を可能な限り回避する。

---

### 4.4 EMERGENCY

EMERGENCY 状態は **重大な混雑または障害状態**を示す。

特徴

- severe congestion
- packet drops
- link failure impact

Routing は EMERGENCY 経路を使用してはならない。

---

## 5. Link State

Fabric State に加えて、PSC はリンク単位の状態も定義する。

| State    | Description       |
| -------- | ----------------- |
| NORMAL   | 正常動作          |
| DEGRADED | 性能低下状態      |
| FAILED   | リンク断          |

Link State は Fabric State 評価の入力として使用される。

---

## 6. Node State

PSC ノードは以下の状態を持つ。

| State      | Description      |
| ---------- | ---------------- |
| NORMAL     | 正常動作         |
| OVERLOADED | 高負荷状態       |
| ISOLATED   | Fabric から隔離  |
| FAILED     | ノード障害       |

Node State も Fabric State の評価要素となる。

---

## 7. State Transition

Fabric State は Telemetry 情報に基づき動的に変化する。
Fabric State はリンク単位、ノード単位、または Fabric 全体単位で評価される場合がある。

例:

CALM → WARM
WARM → HOT
HOT → EMERGENCY

また、状態回復時には

EMERGENCY → HOT
HOT → WARM
WARM → CALM

のような遷移が行われる。

状態遷移には **ヒステリシス**を設け、
Fabric State の頻繁な振動（state oscillation）を防止し、
Routing および Fabric 制御の安定性を確保することが望ましい。

---

## 8. Routing Interaction

Routing Control Unit (RCU) は Fabric State を参照して
経路選択を行う。

一般的な優先順位

```
CALM > WARM > HOT > EMERGENCY
```

EMERGENCY 状態の経路は原則として使用しない。
WARM または CALM の代替経路が存在する場合、Routing は HOT 状態の経路を回避することが望ましい。

---

## 9. Control Node Interaction

Control Node は Fabric State を監視し、

- congestion mitigation
- policy adjustment
- topology management

などの判断に利用する。

Control Node は Fabric State を直接変更するのではなく、
ポリシーや設定を通じて Fabric の挙動を調整する。

---

## 10. AI Interaction

AI Control Node は Fabric Telemetry を分析し、
より細かい状態評価を内部的に使用することができる。

例:

- ACTIVE
- BUSY
- CRITICAL

など。

ただし PSC Fabric に影響を与える制御判断は、
**必ず Official Fabric State (CALM/WARM/HOT/EMERGENCY)**
に変換された後に適用される。

この設計により PSC は

- AI依存を避ける
- 状態モデルの安定性を維持する
- AI実装の差異を吸収する

ことができる。

---

PSC Fabric 内における AI parallel work は、Official Fabric State に従って制御されなければならない。

基本動作は以下とする。

- CALM
  学習、相談、最適化のための AI parallel work を許可できる。

- WARM
  AI parallel work は対象範囲および深さを制限して実行する。

- HOT
  Fabric の安定性および転送性能を維持するため、非必須の AI parallel work は破棄しなければならない。

ただし、最小限の危険判定および保護動作は維持される場合がある。

- EMERGENCY
  AI parallel work は停止し、最小限の safety-preserving function のみを許可する。

AI parallel work は、PSC Fabric の default fast transfer path を阻害してはならない。

AI の詳細挙動、相談ルール、および safety mechanism は別の AI behavior specification で定義することが望ましい。

---

## 11. 設計原則

PSC Fabric State Model は以下の原則に基づく。

- state-based control
- stable interpretation
- human readability
- AI compatibility
- implementation simplicity
- fast-path preservation

Fabric State は PSC Fabric の
**共通制御言語**として機能する。
