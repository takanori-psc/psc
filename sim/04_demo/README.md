# PSC Demo

This directory provides the easiest way to experience PSC behavior.  
（このディレクトリは、PSCの動作を最も簡単に体験するための入口です）

If you are new to PSC, start here.  
（PSCを初めて見る場合は、まずここから始めてください）

---

## 🚀 Quick Start（クイックスタート）

### Static Demo（静的デモ）

```bash
python3 run_psc_demo.py
```
Basic trust-aware routing decision.
（信頼性を考慮した基本的なルート選択）

### Dynamic Demo（動的デモ）
```bash
python3 run_psc_dynamic_demo.py
```
Adaptive routing with changing network conditions.
（ネットワーク状態の変化に応じた適応的ルーティング）

## 🔍 What you will see（確認できる内容）
- Static Demo
  - Route comparison
    （ルート比較）
  - Cost + trust evaluation
    （コストと信頼性の評価）
  - Final route decision
    （最終ルート選択）

- Dynamic Demo
  - Step-by-step routing decisions
    （ステップごとのルート選択）
  - Trust degradation events
    （信頼性低下イベント）
  - Route switching behavior
    （ルート切替動作）

## 🧠 Recommended Order（推奨順）
1. run_psc_demo.py
   Static demo（静的デモ）
2. run_psc_dynamic_demo.py
   Dynamic demo（動的デモ）

Start with the static demo to understand the concept,
then run the dynamic demo to see adaptive behavior.
（まず静的デモで基本概念を理解し、その後動的デモで適応動作を確認してください）

## ⚠ Notes（補足）
These demos are intentionally simplified for clarity.
（これらのデモは理解しやすさを重視して簡略化されています）

They demonstrate PSC concepts, not the full implementation.
（最終的な実装ではなく、PSCの概念を示すためのものです）
