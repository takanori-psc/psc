# Human-AI Control Plane Model v0.1

## Document Information

- Document Name : Human-AI Control Plane Model
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : Operational Control Layer
- Document Type : Conceptual Architecture Model
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-05
- Last Updated  : 2026-05
- Language      : Japanese

---

## 1. Overview

本モデルは、

- Human
- Local AI
- Cloud AI
- Execution Environment

が混在する次世代AI運用環境における、
制御構造・責任分離・信頼境界を定義する。

従来のAI利用モデルでは、
Human は単なる利用者（User）として扱われることが多かった。

しかし実際の複数AI運用環境では、
Human は単なる利用者ではなく：

- AI選択
- 出力比較
- 実行承認
- 信頼判断
- 境界管理
- エスカレーション判断

を行う制御主体として機能する。

本モデルでは、
この人間側制御主体を
Human Resolver と定義する。

さらに、
Human Resolver を中心として構成される：

- Local AI
- Cloud AI
- Execution Environment

を含む全体制御構造を、
Human-AI Control Plane と定義する。

---

## 2. Operational Structure

### 2.1 Basic Structure

```text
+--------------------------------------------------+
|              Human Resolver Plane                |
|--------------------------------------------------|
| AI selection                                     |
| Output comparison                                |
| Trust evaluation                                 |
| Execution approval                               |
| Arbitration                                      |
| Boundary control                                 |
+--------------------------------------------------+

        ↓                ↓                ↓

+----------------+  +----------------+  +----------------+
| Local AI Plane |  | Cloud AI Plane |  | Execution Plane|
|----------------|  |----------------|  |----------------|
| Local LLM      |  | ChatGPT        |  | Terminal       |
| Qwen           |  | Codex Cloud    |  | Git            |
| Continue       |  | Remote Agents  |  | File System    |
+----------------+  +----------------+  +----------------+
```

本構造では、
Human Resolver が中央制御主体として機能し、
複数AIおよび実行環境を統合管理する。

---

## 3. Human Resolver Concept

Human Resolver は、
複数AI環境における最終制御主体である。

Human Resolver は以下を担当する：

- AI出力比較
- 実行可否判断
- Trust境界判定
- 意味衝突解決
- 実行承認
- エージェント切替
- 異常時停止判断

Human Resolver は、
単なる operator ではなく、
AI運用系全体における
Arbitration Layer として機能する。

---

## 4. Operational Boundary Concept

複数AI運用環境では、
以下の境界が混在する：

- Local AI Boundary
- Cloud AI Boundary
- Execution Boundary
- Trust Boundary
- Human Approval Boundary

これらの境界は、
単純な Local / Cloud 区分ではなく、
実際には：

- 外部通信
- Plugin
- IDE integration
- Telemetry
- Remote execution
- File access
- Git operation

などによって相互接続される。

そのため：

```text
Local LLM = trusted
```

とは限らない。

本モデルでは、
実行可能性・外部接続性・制御権限を含めた
Operational Trust に基づいて
Trust Boundary を定義する。

---

## 5. Multi-Agent Operational Environment

現代のAI運用環境では、
複数AIが異なる役割を持ちながら
並列動作する構造が一般化しつつある。

例：

| Plane          | Role                       |
| -------------- | -------------------------- |
| Local AI       | Semantic analysis          |
| Cloud AI       | Arbitration / reasoning    |
| Execution AI   | Implementation / execution |
| Human Resolver | Final decision making      |

この構造では、
各AIが異なる得意分野を担当する。

そのため、
単一AIによる完全制御ではなく、
複数AI間の比較・検証・調停が重要となる。

---

## 6. Execution Separation

AI実行環境では、
Human execution と AI-assisted execution を
明確に分離する必要がある。

例：

| Environment    | Purpose                 |
| -------------- | ----------------------- |
| Human Terminal | Manual execution        |
| AI Terminal    | Agent execution         |
| Editor         | Source modification     |
| External AI    | Reasoning / arbitration |

この視覚的・構造的分離は：

- 誤操作防止
- 実行主体識別
- Trust管理
- Execution tracing

において重要となる。

---

## 7. Multi-Surface Confusion

複数AI・複数UI環境では：

- Chat UI
- IDE
- Terminal
- Agent console
- Git operation
- Browser

が混在する。

このとき、
Human 側で：

- 誰が実行したか
- どのAIが提案したか
- 何が実行済みか
- Trust対象は何か

が曖昧化する可能性がある。

本モデルでは、
この問題を：

```text
Multi-Surface Confusion
```

として定義する。

---

## 8. Design Principles

本モデルは以下の原則に基づく：

- Human-centered control
- Trust separation
- Multi-agent arbitration
- Explicit execution approval
- Operational boundary visibility
- Human-readable execution tracing
- Layered trust validation

Human-AI運用環境では、
Human を除外した完全自律制御ではなく、
Human Resolver を含む階層型制御構造が重要となる。