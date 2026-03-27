# PSC Operation Mode Model v0.1（Draft）

## Document Information

* Document Name: PSC Operation Mode Model
* Version: v0.1
* Project: PSC (Photon System Controller)
* Layer: PSC Fabric / Control Model
* Status: Draft
* Author: T. Hirose
* Language: Japanese

---

## 1. Purpose

本仕様は、PSC Fabricにおける運用状態（Operation Mode）を定義し、
各状態において許可される経路選択、フォールバック、回復動作を規定することを目的とする。

本モデルは、Routing Model、Trust Model、Resolver Modelの上位制御として機能し、
システム全体の安定性・信頼性・継続性を保証する。

---

## 2. Scope

本仕様は以下を対象とする：

- PSC Fabricにおける運用状態の定義
- 各状態における許可動作および制限
- 状態遷移条件
- Recoveryおよび安定性確認動作

以下は本仕様の対象外とする：

- 経路探索アルゴリズム（Routing Model）
- 信頼度算出ロジック（Trust Model）
- 経路コスト算出ロジック
- Resolver内部アルゴリズム

---

## 3. Operation Modes

PSCは以下の運用状態を持つ：

### 3.1 NORMAL

通常運用状態。

- trusted経路の存在を前提とする
- 通常のPolicy（latency / stability）が適用される
- hysteresisが有効
- degraded fallbackは禁止

---

### 3.2 TRUST_FAILURE

trusted経路が存在しない状態。

- 通常運用の前提が崩れた状態
- Routing結果としてtrusted routeが存在しない
- Resolverへエスカレーションされる

※ 本状態は短期間の遷移状態として扱うことも可能

---

### 3.3 DEGRADED

劣化運用状態。

- Resolverの判断によりfallbackが許可された状態
- allow_untrusted_fallbackが有効
- trust weightを考慮した経路選択が可能
- 接続維持を優先

---

### 3.4 RECOVERY

回復確認状態。

- trusted経路が再び利用可能になった後の検証フェーズ
- 即時NORMAL復帰は行わない
- 一定期間の安定性確認を実施

---

## 4. Mode Definitions

### 4.1 NORMAL

許可動作：

- trusted route のみ使用
- policy適用（latency / stability）
- hysteresis適用
- 通常のroute switch判定

制限：

- untrusted routeの使用禁止
- degraded fallback禁止

---

### 4.2 TRUST_FAILURE

trusted経路が存在しない状態。

本状態は、trusted route消失を検出した際に一時的に遷移する状態であり、
通常は短時間でDEGRADEDまたは他の状態へ遷移する。
本状態は異常検出およびResolver判断のトリガとして機能する。

許可動作：

- trusted routeの探索
- Resolverへの通知

制限：

- 通常通信の継続不可
- fallback未許可

---

### 4.3 DEGRADED

許可動作：

- untrusted / limited route使用（条件付き）
- trust weightを考慮した経路選択
- degraded専用のswitch基準適用

制限：

- securityレベルの低下を許容
- 通常時と同一のpolicy基準は適用しない場合がある
- DEGRADED状態では、信頼性制約（Trust制約）を部分的に緩和し、
  接続維持を優先するが、許可範囲はPolicyおよびResolver判断により制限される

### 4.4 RECOVERY

許可動作：

- trusted routeの監視
- 安定性確認（カウンタ / 時間ベース）

制限：

- 即時NORMAL復帰禁止
- 不安定時はDEGRADEDへ戻る

---

## 5. State Transition Conditions

### 5.1 NORMAL → TRUST_FAILURE

条件：

- trusted routeが存在しない

---

### 5.2 TRUST_FAILURE → DEGRADED

条件：

- Resolverがfallbackを許可

---

### 5.3 DEGRADED → RECOVERY

条件：

- trusted routeが再び利用可能
- recovery条件開始トリガを満たす

---

### 5.4 RECOVERY → NORMAL

条件：

- trusted routeが一定期間安定
- 例：連続Nステップ成功（RECOVERY_REQUIRED_STEPS）

---

### 5.5 RECOVERY → DEGRADED

条件：

- trusted routeが再び消失または不安定化

---

## 6. Inputs and Outputs

### 6.1 Inputs

- Routing結果（best route / cost）
- trusted routeの有無
- trust level情報
- policy判定結果
- hysteresis判定結果
- Resolver override判断
- node状態（NORMAL / BUSY / CONGESTED）

---

### 6.2 Outputs

- 現在のoperation mode
- trusted only制約の有効/無効
- fallback許可/禁止
- route switch許可/保留
- recovery開始/継続/中止

---

## 7. Recovery and Stability Policy

- recoveryは即時復帰ではなく段階的に行う
- 安定判定には以下を使用可能：
  - 連続成功回数
  - 時間ベース
  - エラー率
- 不安定と判定された場合はDEGRADEDへ戻る

---

## 8. Design Principles

- Routingと制御を分離する
- 安全性と継続性のバランスを取る
- 状態遷移は明示的に定義する
- 一時的変動に対する耐性を持つ（hysteresis / recovery）

---

## 9. Open Design Items

- TRUST_FAILUREを状態として保持するか、イベントとして扱うか
- RECOVERYの判定基準（時間 vs 回数）
- DEGRADED中のpolicy基準の詳細定義
- Fabric State Model（CALM / WARM / HOT / EMERGENCY）との統合方法

