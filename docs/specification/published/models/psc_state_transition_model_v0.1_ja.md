# PSC 状態遷移モデル v0.1

## ドキュメント情報

- Document Name : PSC State Transition Model
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

本ドキュメントは、PSC（Photon System Controller）における状態遷移モデルを定義する。
本モデルは、システムの安定性維持、異常時対応、および安全な復帰を目的として設計されている。

状態遷移は固定されたルールに基づき実行され、曖昧な判断や不安定な切替を抑制する。

---

## 状態定義（State Definitions）

### CALM

システムが安定した通常状態。
最適な経路および制御が維持され、外部変動の影響は最小限である。

- 安定性：高
- 変動：低
- Resolver関与：なし

---

### WARM

軽微な変動や負荷増加が検知される状態。
システムは安定を維持しつつ、状況の監視と評価を行う。

- 安定性：中〜高
- 変動：中
- Resolver関与：基本なし

---

### HOT

競合・曖昧性・信頼低下が発生する状態。
通常のRCU判断では解決が困難なケースが増加する。

- 安定性：低〜中
- 変動：高
- Resolver関与：条件付きで発動（競合・曖昧性発生時）

---

### EMERGENCY

重大な障害または異常により、通常制御が維持できない状態。
システムは最小限の機能を維持しつつ、制御を制限する。
通常の最適化処理は停止され、決定は安全性を最優先とした制約付きで行われる。

- 安定性：極低
- 変動：不定
- Resolver関与：制限またはバイパス

---

## 状態遷移ルール（Transition Rules）

### CALM → WARM

軽微な負荷増加または変動が検知された場合に遷移。

---

### WARM → HOT

競合、曖昧性、または信頼低下が一定閾値を超えた場合に遷移。

---

### HOT → EMERGENCY

重大な障害または制御不能状態が検知された場合に遷移。

---

### EMERGENCY → HOT

最低限の制御条件が回復した場合に遷移。

---

### HOT → WARM

競合および曖昧性が解消され、安定性が回復した場合に遷移。

---

### WARM → CALM

システムが十分に安定し、変動が解消された場合に遷移。

---

## Recovery手順（Recovery Procedure）

復帰処理は段階的かつ状態依存で実行される。
これにより、不必要な振動（オシレーション）を防止する。

1. 最低限の制御条件を満たす
2. EMERGENCY → HOT に遷移
3. HOT状態にて評価を実施
4. HOT → WARM に遷移
5. WARM → CALM に遷移

---

## Resolver関与（Resolver Involvement）

Resolverは特定の状態に固定されるものではなく、
競合や曖昧性が増加する状況に応じて動的に関与する。

- CALM / WARM：関与なし、または最小限
- HOT：競合・曖昧性発生時に条件付きで発動
- EMERGENCY：関与は制限される、またはバイパスされる

---

## 設計原則（Design Principles）

1. 状態遷移は明確な条件に基づく
2. 不必要な経路切替を抑制する
3. 異常時は安全側に動作する
4. 復帰は段階的に実行する
5. すべての判断は追跡可能である

---
