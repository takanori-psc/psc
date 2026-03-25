# PSC Control Plane Model v0.1

## Document Information

* Document Name: PSC Control Plane Model
* Version: v0.1
* Project: PSC
* Layer: PSC Fabric
* Status: Draft
* Author: T. Hirose
* Language: Japanese

---

## 1. Purpose

本書は、PSC Fabric における Control Plane の責務、制御構造、構成要素間の連携、および制御ループの基本動作を定義することを目的とする。

PSC における Control Plane は、単一の独立機能ではなく、Fabric 状態を観測し、判断し、制御し、結果を再観測するための継続的な制御ループとして機能する。

本書は特に以下を対象とする。

- Fabric 状態変化に対する制御の基本構造
- Resolver、RCU、TMU、TEU の役割分離
- Local 制御と Fabric-wide 制御の整理
- 制御トリガ、判断、実行、フィードバックの流れ

---

## 2. Scope

本書の対象範囲は以下とする。

- PSC Fabric における Control Plane の論理構造
- 制御に関与する主要構成要素の責務
- 制御ループの入力、判断、実行、再評価の流れ
- Fabric-wide 制御と Local 制御の役割分担
- Resolver と RCU の接続関係

本書は以下を直接の対象外とする。

- 個別の経路計算アルゴリズム詳細
- Packet format 詳細
- Transfer execution の物理実装詳細
- Telemetry message format 詳細
- Security policy field のビット定義詳細

これらは関連仕様書で定義する。

---

## 3. Design Principles

PSC Control Plane は以下の設計原則に従うものとする。

### 3.1 Control Plane as a Control Loop

Control Plane は静的な管理機構ではなく、状態監視、判断、制御、実行、再評価から成る継続的な制御ループとして構成されなければならない。

### 3.2 Separation of Responsibilities

各構成要素は責務分離されなければならない。

- Resolver は判断理由および上位制御判断を担う
- RCU は経路選択および経路切替判断を担う
- TMU はタイミング制御、抑制条件、再評価周期管理を担う
- TEU は実際の転送実行を担う
- Monitoring / Telemetry は状態入力および結果観測を担う

### 3.3 Event-driven Control

Control Plane は event-driven を基本としなければならない。
ただし、安定性確保のために周期的再評価を併用してもよい。

### 3.4 Hierarchical Control Scope

Control Plane は Local 制御と Fabric-wide 制御を区別しなければならない。
すべての制御判断を常に Fabric-wide に拡張してはならない。

### 3.5 Stability over Excessive Reactivity

Control Plane は過剰反応を避けるため、ヒステリシス、抑制時間、再評価閾値を考慮しなければならない。

---

## 4. Control Plane Overview

PSC における Control Plane は、Fabric の状態を観測し、必要に応じて経路、転送、制御方針を調整するための統合制御系である。

Control Plane は以下の制御ループとして定義される。

1. 状態入力を受け取る
2. 状態変化を評価する
3. 必要時に Resolver または RCU を起動する
4. 判断結果を TMU により時間制御する
5. TEU が実行する
6. 実行結果を Telemetry により再観測する
7. 必要に応じて再評価する

このループは Fabric の継続動作中に反復される。

---

## 5. Functional Components

### 5.1 Resolver

Resolver は、RCU による通常の評価および選択機構では決定不可能な状態、
または通常制御では解決できない例外的状態を解消するために起動される上位判断機構である。

Resolver は以下を担う。

- competing policy の整理
- degraded mode 判断
- trust collapse 時の代替方針決定
- policy violation 時の例外制御判断
- 通常ルーティングでは解決できない条件の解決

Resolver は常時経路計算器として振る舞ってはならない。

### 5.2 Routing Control Unit (RCU)

RCU は通常時の経路選択および経路切替の主体である。

RCU は以下を担う。

- 利用可能経路の評価
- policy / trust / congestion / stability 条件を反映した経路選択
- failover candidate の維持
- route switch 条件の判定
- route invalidation 時の再選択

RCU は即時性が求められる判断を担当する。

### 5.3 Transfer Management Unit (TMU)

TMU は制御の時間的整合性を担う。

TMU は以下を担う。

- trigger timing 管理
- hold-down / hysteresis 制御
- retry / reevaluation timing
- periodic reevaluation scheduling
- escalation delay 管理

TMU は単なるタイマーではなく、過剰な制御変動を抑制するための時間制御機構として機能する。

### 5.4 Transfer Execution Unit (TEU)

TEU は Control Plane で確定した判断を Data Plane 実行へ反映する。

TEU は以下を担う。

- selected route に基づく転送実行
- execution 状態反映
- transfer failure 通知
- execution result の上位通知

### 5.5 Monitoring and Telemetry

Monitoring / Telemetry は Control Plane の入力およびフィードバック源である。

取得対象には以下を含んでもよい。

- link utilization
- queue growth
- retransmission increase
- credit starvation
- node reachability
- trust degradation
- policy invalidation
- latency growth
- error burst
- fault notification

---

## 6. Control Scope

### 6.1 Local Control

Local Control は単一ノードまたは近傍制御領域に限定された制御である。

例:

- 単一リンク障害への切替
- 近傍混雑回避
- 局所的 failover
- port-level policy enforcement

### 6.2 Fabric-wide Control

Fabric-wide Control は広域状態に基づく調整である。

例:

- 広域輻輳状態への方針変更
- trust domain 異常への広域反応
- degraded mode への遷移
- policy-wide rerouting guidance

Fabric-wide Control は必要時のみ発動されるべきであり、常時適用を前提としてはならない。

### 6.3 Scope Escalation

Local 問題が以下の条件を満たす場合、Control Plane は Fabric-wide 制御へ escalation してもよい。

- 局所再制御で安定化できない
- 複数ノードへ影響が波及している
- trust または policy 条件が局所範囲を超えている
- degraded mode 判断が必要である

---

## 7. Trigger Conditions

Control Plane は以下の条件で制御処理を開始または再評価しなければならない。

- link down
- node unreachable
- severe congestion detection
- error burst detection
- trust collapse
- policy invalidation
- route score degradation
- transfer execution failure
- periodic reevaluation timer expiration

Resolver は、RCU による通常の評価および選択機構では決定不可能な状態を解消するために起動される。
Resolver の起動は、以下の条件のいずれかを満たす場合に発生してもよい。

- RCU により、policy、trust、および基本到達性条件を満たす route が選択できない場合
- policy 制約を満たす route が存在しない場合
- trusted route が存在しない場合
- route selection において複数の候補が同等評価となり、優先順位を決定できない場合
- degraded mode への遷移判断が必要な場合
- 選択された route が継続的に実行失敗している場合

---

## 8. Control Loop Sequence

PSC Control Plane は概ね以下の順序で動作する。

1. Monitoring / Telemetry が状態変化を検出する
2. TMU が即時処理対象か遅延処理対象かを判定する
3. RCU が通常経路再評価を行う
4. 必要時に Resolver が上位判断を行う
5. 判断結果に基づき TMU が適用タイミングを決定する
6. TEU が転送または切替を実行する
7. 実行結果が Monitoring / Telemetry に反映される
8. 必要に応じて次の制御ループへ進む

---

## 9. Resolver and RCU Relationship

Resolver と RCU は同一責務ではない。

- RCU は operational route control を担う
- Resolver は exceptional or higher-order decision を担う

通常時は RCU が優先されるべきである。
Resolver は例外的または上位方針調整が必要な場合にのみ関与するべきである。

この分離により、通常時の制御応答性と、異常時の判断柔軟性を両立する。

---

## 10. Stability Control

Control Plane は制御の安定性を維持するため、以下を考慮しなければならない。

- hysteresis
- minimum hold time
- reevaluation interval
- switching suppression
- escalation threshold
- recovery threshold

一時的な変動により不要な route flap または制御振動を発生させてはならない。

---

## 11. Failure Handling

Control Plane は以下の異常に対応できなければならない。

- path invalidation
- repeated execution failure
- telemetry inconsistency
- unavailable trusted route
- persistent congestion
- policy-compliant route exhaustion

必要に応じて以下を行ってもよい。

- degraded mode 遷移
- fallback route 許可
- route isolation
- temporary control suppression
- resolver escalation

---

## 12. Future Extensions

将来的に Control Plane は以下を拡張対象として含んでもよい。

- multi-layer control hierarchy
- AI-assisted prediction support
- predictive congestion avoidance
- region-level coordinator
- distributed control cooperation
- adaptive policy weighting

ただし v0.1 では、基本的な event-driven control loop を優先する。

---

## 13. Summary

PSC Control Plane は、Fabric 状態を観測し、評価し、判断し、実行し、再観測するための統合制御ループである。

本モデルでは、Resolver、RCU、TMU、TEU、Monitoring / Telemetry の責務分離を維持しつつ、Local 制御と Fabric-wide 制御を接続する構造を定義した。

本書は PSC Fabric を単なる接続構造ではなく、自律的に制御される Fabric-centric distributed computer architecture として成立させるための基盤仕様である。

---


