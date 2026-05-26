# PSC Quick Start

この文書は、PSC simulation を実行し、
生成された検証ログを確認するための最短導線です。

PSC の挙動は、RULE、シナリオ、ログの対応関係によって検証されます。
目的は単に demo を動かすことではなく、
制御判断がどのように生成されるかを確認することです。

---

## 前提

すべての例は Python 3 環境を前提としています。

---

## 1. RCU Decision v0.1 Simulation を実行する

```bash
python3 sim/02_controlled/02_rcu_decision_v01/mini_psc_rcu_decision_v01.py
```

この simulation は、RCU Decision Model v0.1 の中核挙動を検証します。

- trust-aware path selection
- stability-preserving KEEP behavior
- Resolver escalation
- degraded operation
- controlled recovery
- cooldown による oscillation resistance

---

## 2. 生成ログを確認する

生成ログは以下に出力されます。

`sim/02_controlled/02_rcu_decision_v01/logs/`

| シナリオ | ログ |
| --- | --- |
| Resolver 安定性競合 + クールダウン | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_stability_conflict_cooldown_rule_log.md` |
| Degraded -> Recovery -> Stabilization | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md` |
| Resolver による切替判断 | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md` |

---

## 3. RULE 参照と挙動を比較する

Evidence Matrix を開きます。

- English: docs/specification/validation/psc_evidence_matrix_v0.1_en.md
- Japanese: docs/specification/validation/psc_evidence_matrix_v0.1_ja.md

各シナリオが明示的な RULE 判断にどう対応しているかを確認します。

| 挙動 | RULE examples |
| --- | --- |
| 曖昧な path conflict | `RULE-05_ESCALATE_conflict` |
| cooldown suppression | `RULE-12_COOLDOWN_active` |
| degraded fallback | `RULE-09_DEGRADE_switch`, `RULE-08_DEGRADE_keep` |
| recovery transition | `RULE-10_RECOVERY_trigger`, `RULE-11_RECOVERY_cooldown` |
| Resolver switch | `RULE-14_RESOLVER_switch` |

---

## 4. Quick Demo を実行する

| Demo | Command | 目的 |
| --- | --- | --- |
| Static Demo | `python3 sim/04_demo/run_psc_demo.py` | 基本的な trust-aware routing と安定 path 優先 |
| Dynamic Demo | `python3 sim/04_demo/run_psc_dynamic_demo.py` | path 条件変化に対する適応挙動 |

---

## 5. Core Model を読む

simulation 実行後に、model specification を読むと理解しやすくなります。

- English: docs/specification/published/models/psc_rcu_decision_model_v0.1_en.md
- Japanese: docs/specification/published/models/psc_rcu_decision_model_v0.1_ja.md

重要なのは PSC の制御挙動です。
PSC は、不安定なピークスループットよりも、
破綻しにくく安定した判断を優先します。
