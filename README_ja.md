# Photon System Controller (PSC)

🇯🇵 日本語 | 🇺🇸 English → README.md

安定性と信頼性に基づいて、最も安定し信頼できるネットワーク経路を動的に選択する
ファブリック駆動型システムです。単なる最短経路選択ではありません。

---

## なぜ PSC なのか？

- 不安定なネットワーク経路を自動的に回避
- 生の速度よりも信頼性と安定性を優先
- ネットワーク状態の変化に応じてリアルタイムに適応
- 意思決定をネットワークファブリック内部へ移動

PSC は単なるデータ転送層ではなく、
**意思決定を行うルーティングシステム**です。

PSC は通常動作、劣化、回復のすべての段階において、
即時的な性能改善よりも安定性を優先します。

---

## PSC とは何か？

PSC（Photon System Controller）は、従来の CPU 中心設計から脱却し、
システム制御とデータ移動を通信ファブリック中心へ移す
ファブリック中心型コンピュータアーキテクチャです。

PSC では、通信ファブリック自体が協調制御とデータフローの中心になります。

中央集権的な制御に依存せず、
ファブリック内で分散的に意思決定を行います。

---

## 設計思想

PSC は単なる高速通信だけを目的としたものではありません。
大規模分散システムにおいて、安定性、信頼性を考慮した制御、
封じ込め、回復性を重視するように設計されています。

- English:
  docs/specification/published/vision/psc_design_philosophy_v0.1_en.md

- Japanese:
  docs/specification/published/vision/psc_design_philosophy_v0.1_ja.md

---

## スタートガイド（RCU Decision v0.1）

ここが PSC の中核です。

RCU Decision Model は、PSC が以下をどのように実現するかを定義します。

- 不安定経路の回避
- 信頼性と安定性を優先する判断
- 制御された切替による oscillation 防止

PSC を理解するには、ここから始めてください。
このモデルは、シミュレーションログによって実装・検証済みです。

### 1. 仕様を読む

docs/specification/published/models/psc_rcu_decision_model_v0.1_ja.md

### 2. シミュレーションを実行

> すべての例は Python 3 環境を前提としています。

```bash
python3 sim/02_controlled/02_rcu_decision_v01/mini_psc_rcu_decision_v01.py
```

## 検証 / Evidence

PSC の検証挙動は、RULE、シナリオ、ログを対応付ける
追跡可能なマッピングとして整理されています。

参照:

- docs/specification/validation/psc_evidence_matrix_v0.1_en.md
- docs/specification/validation/psc_evidence_matrix_v0.1_ja.md

推奨される検証フロー:

1. 仕様文書を読む
2. シミュレーションシナリオを実行する
3. Evidence Matrix を開く
4. 対応するログを確認する

この追跡可能性により、PSC の挙動は再現可能で、
監査可能であり、RULE ベースの制御判断と直接対応付けられます。

### 3. ログを確認

sim/02_controlled/02_rcu_decision_v01/

詳細な検証トレーサビリティは以下にあります。

docs/specification/validation/psc_evidence_matrix_v0.1_ja.md

確認ポイント:

- resolver_stability_conflict
- degraded / recovery behavior
- trust-aware decisions

---

## 検証ログ

以下のログは、PSC RCU Decision Model v0.1 の挙動を再現可能な形で検証するものです。
各ログは完全に再現可能であり、RULE ベースの意思決定 trace と直接対応しています。

すべてのログはシミュレーションから直接生成されており、
実際の実行挙動を反映しています。

### 1. Resolver 安定性競合 + クールダウン

**シナリオ:**
スコアがほぼ同等の経路間で安定性の競合が発生し、
Resolver へのエスカレーションが発生します。
クールダウンは連続エスカレーションを防ぎ、
ヒステリシスは安定性を維持します。

```bash
python3 sim/02_controlled/02_rcu_decision_v01/mini_psc_rcu_decision_v01.py
```

**ログ:**
`rcu_decision_v01_resolver_stability_conflict_cooldown_rule_log.md`

**ポイント:**

- `RULE-05_ESCALATE_conflict` が競合する path 間の曖昧性を検出
- Resolver は不要な切替を避ける（KEEP 相当の判断）
- `RULE-12_COOLDOWN_active` が連続エスカレーションを抑制
- `RULE-01_KEEP_score` がヒステリシスにより安定性を維持

### 2. Degraded → Recovery → Stabilization

**シナリオ:**
全 path の trust が低下し、degraded operation が強制されます。
システムは安全側へ fallback し、その後条件が改善すると回復します。

```bash
python3 sim/02_controlled/02_rcu_decision_v01/mini_psc_rcu_decision_v01.py
```

**ログ:**
`rcu_decision_v01_degraded_switch_recovery_rule_log.md`

**ポイント:**

- `RULE-09_DEGRADE_switch` が障害条件下で fallback path を選択
- `RULE-08_DEGRADE_keep` が degraded mode における不要な切替を防止
- `RULE-10_RECOVERY_trigger` が条件改善時に通常動作へ復帰
- `RULE-11_RECOVERY_cooldown` が遷移を安定化
- `RULE-01_KEEP_score` が回復後の安定動作を保証

### 3. Resolver による切替判断

**シナリオ:**
スコアがほぼ同等で trust に大きな差がある場合、
Resolver へのエスカレーションが発生します。
Resolver は選択中 path を明示的に切り替えます。

```bash
python3 sim/02_controlled/02_rcu_decision_v01/mini_psc_rcu_decision_v01.py
```

**ログ:**
`sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md`

**ポイント:**

- `RULE-05_ESCALATE_conflict` が trust conflict により発火
- `RULE-14_RESOLVER_switch` が明示的な path switch（A → B）を実行
- `RULE-12_COOLDOWN_active` が連続エスカレーションを防止
- `RULE-01_KEEP_score` が新しい選択を安定化

## これらのログが示すこと

- PSC は曖昧な状況で不要な切替を避ける
- PSC は trust 条件が失敗した場合に安全に degraded へ移行する
- PSC は oscillation なしに予測可能に回復する
- すべての判断は明示的な RULE 定義へ追跡できる

> PSC は最適化エンジンではありません。
> **障害時にも破綻しない意思決定エンジン**です。

### リカバリ挙動（重要）

PSC は保守的なリカバリ戦略を採用しています。

一度劣化した path が回復し、再び最良性能の path になった場合でも、
現在選択中の path が安定かつ信頼できる状態であれば、
PSC は即座に切り戻しません。

この挙動は、性能改善の追従よりも安定性を優先し、
回復後の不要な切替を防ぐためのものです。

### リカバリ挙動の比較（v0.1 vs v0.2）

以下の比較ログは、保守的な recovery hold（v0.1）と
段階的 recovery return（v0.2）の違いを示します。

**ログ:**
[Recovery Comparison Log (v0.1 vs v0.2)](sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_vs_v01_recovery_hold_log.md)

**主な違い:**

- v0.1:
  元の path が回復しても、現在の安定 path を維持する

- v0.2:
  段階的復帰を導入:
  RECOVERY_CANDIDATE → VALIDATION → RETURN_ELIGIBLE → RETURN_SWITCH

この比較は、PSC が安定性の保証を維持しながら、
安定性優先の挙動から制御された適応性へ発展することを示しています。

---

## クイックデモ

PSC には 2 種類のデモモードがあります。

### 1. 静的デモ（基本挙動）

PSC が trust と cost に基づいて経路を選択する様子を確認できます。

**確認できる内容:**

- 基本的な trust-aware routing
- 最短 path よりも安定した path を優先

```bash
python3 sim/04_demo/run_psc_demo.py
```

---

### 2. 動的デモ（適応挙動）

PSC が変化するネットワーク状態にどのように反応するかを確認できます。

**確認できる内容:**

- リアルタイムな routing adaptation
- 不安定 path の回避
- trust に基づく意思決定の変化

```bash
python3 sim/04_demo/run_psc_dynamic_demo.py
```

---

## アーキテクチャ概要

PSC は、システム制御を中央集権的な CPU から通信ファブリックへ移します。

**重要な考え方:**

- 制御はファブリック全体に分散される
- データフローと意思決定が統合される

![PSC Architecture Concept](diagrams/concept/psc_concept_architecture_comparison_v0.1.png)

この図は、従来の CPU 中心アーキテクチャと
PSC のファブリック駆動モデルを比較しています。

---

### Resolver 制御モデル

この図は、PSC 内部で意思決定がどのように行われるかを示します。

**主な挙動:**

- 通常時は RCU が自律的に動作
- escalation または override が必要な場合のみ Resolver が介入
- 意思決定制御は実行から分離される

![PSC Resolver Control Model](diagrams/control/psc_resolver_control_model_v0.1.png)

PSC は単なるデータ転送システムではありません。
**意思決定を内包したファブリックアーキテクチャ**です。

---

## データ転送フロー

この図は、PSC がファブリック内でデータ転送判断をどのように実行するかを示します。

**注目ポイント:**

- コンポーネント間のデータフロー
- routing decision が転送挙動へ与える影響
- 制御層と実行層の相互作用

![PSC Transfer Flow](diagrams/fabric/psc_transfer_flow_v0.1.png)

---

## ファブリック内部構造

この図は、PSC ファブリックの内部構造を示します。

**注目ポイント:**

- 各モジュールの役割（RCU, TMU, TEU, OMU）
- 制御と実行の分離
- ファブリック内部でコンポーネントがどのように接続されるか

![PSC Fabric Internal Architecture](diagrams/fabric/psc_fabric_internal_architecture_v0.1.png)

---

## コアアーキテクチャ構成要素

PSC はファブリック内部に専用の制御モジュールを導入します。

- Resolver（意思決定制御モジュール）
- RCU（routing control unit）
- TMU（transfer management unit）
- TEU（transfer execution unit）
- OMU（optical monitoring unit）

各コンポーネントは、ファブリック内で明確に定義された役割を持ちます。

Resolver はシステム全体の挙動を定義し、
RCU は通常条件下で自律的に動作します。

---

## ドキュメント

PSC を理解するには、以下から始めてください。

- [Architecture Overview](docs/architecture/psc_architecture_overview_en.md)
- [Architecture Map](docs/architecture/psc_architecture_map_v0.1_en.md)
- [Specification](docs/specification/)

---

## 仕様

### 公開済み文書

- PSC AI Behavior Model v0.1

  - English: docs/specification/published/psc_ai_behavior_model_v0.1_en.md
  - Japanese: docs/specification/published/psc_ai_behavior_model_v0.1_ja.md

これらの文書は、安定した参照レベルの仕様です。

---

### Draft 文書

- Routing Model
- Congestion Control Model

これらは現在開発中であり、変更される可能性があります。

---

### コア仕様

- Resolver Specification v0.1
  → docs/specification/resolver/psc_resolver_spec_v0.1.md

Resolver は、状態ベース制御、権限モード、制約ベース出力を含む
PSC の意思決定制御モデルを定義します。

---

## 主要コンセプト

PSC は以下の原則に基づいています。

- ファブリック駆動型コンピュータアーキテクチャ
- 受信側主導データ転送
- チャンクベース転送
- 輻輳認識ルーティング
- ポリシー認識ルーティング
- 信頼性考慮ルーティング
- 適応型ファブリック制御

---

## システムアーキテクチャ

PSC は以下を接続する通信ファブリックを導入します。

- CPU
- GPU
- メモリ
- ストレージ
- ネットワーク
- アクセラレータ

すべての通信は PSC Fabric を通過します。

---

## 記事

コンセプト解説はこちら。

[https://zenn.dev/takanori_psc/articles/73827700dc68a6](https://zenn.dev/takanori_psc/articles/73827700dc68a6)

---

## プロジェクト状況

PSC Fabric Specification v0.1 は現在開発中です。

---

## 作者

T. Hirose
Independent architecture research project

---

## コントリビューション

貢献、議論、アイデアを歓迎します。

`CONTRIBUTING.md` を参照してください。

---
