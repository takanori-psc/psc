# PSC Rack-local Secure Domain Model v0.1

## ドキュメント情報

- Document Name : PSC Rack-local Secure Domain Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSCOS (Control Layer)
- Document Type : Specification
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-04
- Last Updated  : 2026-04
- Language      : Japanese

---

## 概要（Overview）

本ドキュメントは、PSCにおけるラック内限定の高速かつ制限付き通信ドメイン（Rack-local Secure Domain）を定義する。

本モデルは、性能向上と隔離性を両立することを目的とし、同一ラック内のCPU直結ノード間において軽量化された制御を適用する。

ラック外通信および境界ノードを経由する通信は、本モデルの対象外とし、通常のPSCポリシー制御へ戻る。

本モデルは、単一ホップ通信（single-hop）に限定することで、
遅延のばらつき（ジッター）を最小化し、
安定かつ予測可能な通信特性を提供する。

---

## 適用範囲（Scope）

本モデルは以下のノードに適用される：

- 同一ラック内のCPUノード
- 上記CPUノードに直結された以下のノード
  - Memoryノード
  - GPUノード
  - Storageノード

---

## 非適用範囲（Out of Scope）

以下の通信は本モデルの対象外とする：

- ラック外ノードとの通信
- Switch Nodeを経由する通信
- Boundary Node（IOノード）を通過する通信
- multi-hop通信（CPU直結接続を超えて、1つ以上の中継ノードを含む経路）

---

## 定義（Definition）

Rack-local Secure Domainは、同一ラック内においてCPU直結で構成される限定通信ドメインである。

本ドメイン内では、通信範囲が限定されることを前提として、ポリシー評価の一部を軽量化することが可能となる。

---

## Fast Mode成立条件（Eligibility Conditions）

以下の条件をすべて満たす場合に限り、Rack-local Secure Fast Modeを適用する：

- source.rack_id == destination.rack_id
- 通信経路にSwitch Nodeが含まれない
- 通信経路にBoundary Nodeが含まれない
- hop_count == 1（CPU直結範囲内）
- 通信が追跡可能である（Traceabilityが維持される）

いずれかの条件を満たさない場合、通信は通常のPSCポリシー制御へ戻る。

---

## 制御ルール（Control Rules）

### ドメイン内通信

- 軽量化されたポリシー評価を適用
- RCU主体での意思決定
- 高速通信を優先

### 境界通過時

- フルポリシー評価を強制
- Resolverによる介入が可能

### 違反時

- 即時にFast Modeを解除
- 通常PSC制御へフォールバック

---

## 状態モデルとの連携（State Integration）

### CALM

- Rack-local Secure Fast Mode利用可能
- 安定した高速通信を維持

### WARM

- Fast Mode維持
- 一部通信に対して監視強化

### HOT

- Fast Mode制限
- Resolver介入による制御強化

### EMERGENCY

- ラック単位での隔離を実施
- 外部通信遮断
- 最小限の内部通信のみ許可（Degraded Operation）

---

## 設計原則（Design Principles）

1. 高速化は限定範囲内でのみ適用する
2. 境界通過時は必ず制御を強化する
3. 通信の追跡可能性を維持する
4. 異常時は隔離と縮退を優先する
5. 無制御な伝播を防止する

---