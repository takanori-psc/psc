# PSC Evidence Matrix v0.1

## 1. 概要

本マトリクスは、PSC の設計思想、制御 RULE、検証シナリオ、
および観測ログ間の追跡可能性 (Traceability) を確保するための
検証対応表である。

ここで扱う RULE 名は、主に `sim/02_controlled` 配下の
シミュレーション trace に出力される `RULE-xx_NAME` を基準とする。
公開仕様文書内の一般ルール番号とは一部異なる場合があるため、
本ファイルでは「実行ログで確認できる証拠」を優先する。

---

## 2. 検証マッピング

| RULE | 問題 | 設計意図 | シナリオ | 証拠ログ | 状態 |
|------|------|----------|----------|----------|------|
| RULE-01_KEEP_score | 小さな score 変動による不要切替 | hysteresis による安定経路維持 | stable / degraded / recovery_hold | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-02_SWITCH_score | 明確な score 優位があるにもかかわらず切替されない危険 | score_gap が switch_threshold に達した場合に best path へ切替 | switch_score | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md` | Verified |
| RULE-05_ESCALATE_conflict | trust / stability / score 競合による曖昧判断 | Resolver へ仲裁要求 | oscillation / resolver_switch | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md` | Verified |
| RULE-07_DEGRADE_trigger | 選択中 path の trust 低下または invalid 化 | NORMAL から DEGRADED への安全側遷移 | degraded | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-08_DEGRADE_keep | DEGRADED 中の不要な fallback 切替 | degraded mode でも安定 path を維持 | degraded_keep | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md` | Verified |
| RULE-09_DEGRADE_switch | trust 低下時に現在 path が維持不能 | degraded fallback path へ切替 | degraded | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-10_RECOVERY_trigger | trusted path 回復後の復帰判定 | 安定・信頼条件を満たした場合のみ NORMAL 復帰 | degraded_recovery / recovery_hold | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md` | Verified |
| RULE-11_RECOVERY_cooldown | 復帰直後の再劣化・再切替 | recovery cooldown による復帰後安定化 | degraded_recovery / recovery_hold | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md` | Verified |
| RULE-12_COOLDOWN_active | Resolver 介入直後の連続 escalation | cooldown による oscillation 抑制 | oscillation / resolver_switch | `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md` | Verified |
| RULE-13_RESOLVER_keep | Resolver 介入時に切替不要 | Resolver 判断による KEEP | oscillation / resolver_keep | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_rule_unification_log.md` | Verified |
| RULE-14_RESOLVER_switch | ローカル RCU 判断では安全に決めきれない競合 | Resolver 主導の明示的切替 | resolver_switch | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md` | Verified |
| RULE-15_RECOVERY_CANDIDATE | 回復 path を即時復帰させる危険 | recovery candidate として段階評価へ移す | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-16_RECOVERY_VALIDATION_START | 回復 path の安定性確認不足 | validation phase 開始 | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-18_RETURN_ELIGIBLE | 復帰可能条件の不明瞭化 | return switch 前の eligibility 確定 | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-19_RETURN_SWITCH | v0.2 staged recovery の復帰実行 | validation 済み path へ制御された復帰 | recovery_return_v02 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md` | Verified |
| RULE-19_RETURN_RAMP_START | recovery 直後の急激な全量復帰 | progressive return ramp 開始 | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | Experimental |
| RULE-20_RETURN_KEEP | 復帰候補が条件未達のまま切替される危険 | current path 維持 | recovery_return_keep | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md` | Verified |
| RULE-21_RETURN_RAMP_ADVANCE | ramp 中の進行条件不明瞭 | 安定時のみ recovered weight を増加 | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_full_light_observation_validation_log.md` | Experimental |
| RULE-22_RETURN_RAMP_HOLD | ramp 中の一時停止条件不明瞭 | 条件未達時に ramp を維持 | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | Experimental |
| RULE-23_RETURN_RAMP_ABORT | 不安定 path への早期復帰 | ramp 中の異常検知時に復帰を中断 | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | Experimental |
| RULE-24_RETURN_RAMP_COMPLETE | recovery 完了判定の不明瞭化 | progressive reintegration 完了を確定 | recovery_ramp_v03 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | Experimental |

---

## 3. Status Definitions

| Status | Meaning |
|--------|---------|
| Verified | シナリオおよびログにより挙動確認済み |
| Experimental | 拡張実験段階であり、仕様統合前の継続検証対象 |
| Implemented | 実装上の RULE として存在するが、専用ログでの証拠整理が未完了 |
| Planned | 将来検証予定 |

---

## 4. Scenario Definitions

| Scenario | Purpose | 主なログ |
|----------|---------|----------|
| stable | 通常時の KEEP / SWITCH 抑制確認 | `rcu_decision_v01_degraded_rule_validation_log.md` |
| switch_score | threshold 未満の RULE-01 keep と threshold 到達時の RULE-02 switch 確認 | `rcu_decision_v01_switch_score_validation_log.md` |
| oscillation | ECMP 的な score 追従と比較した oscillation 抑制確認 | `rcu_decision_v01_oscillation_ecmp_comparison_log.md` |
| resolver_switch | trust / stability 競合時の Resolver 主導切替確認 | `rcu_decision_v01_resolver_switch_rule_log.md` |
| degraded | trust 低下時の DEGRADED 遷移と fallback 確認 | `rcu_decision_v01_degraded_rule_validation_log.md` |
| degraded_keep | current degraded path が維持可能かつ candidate が recovery eligible でない場合の DEGRADED keep 確認 | `rcu_decision_v01_degraded_keep_validation_log.md` |
| degraded_recovery | DEGRADED から NORMAL への安全復帰確認 | `rcu_decision_v01_degraded_switch_recovery_rule_log.md` |
| recovery_hold | 回復後も current path を維持する conservative hold 確認 | `rcu_decision_v01_recovery_hold_behavior_log.md` |
| recovery_return_v02 | Recovery Candidate -> Validation -> Return Eligible -> Return Switch 確認 | `rcu_decision_v02_recovery_return_validation_log.md` |
| recovery_return_keep | improvement が return_margin 未満の場合の Return Eligible -> Return Keep 確認 | `rcu_decision_v02_return_keep_validation_log.md` |
| recovery_ramp_v03 | progressive ramp / abort / complete / observation policy 確認 | `rcu_decision_v03_recovery_ramp_validation_log.md` |

---

## 5. RULE Definitions

| RULE | Summary |
|------|---------|
| RULE-01_KEEP_score | score 差または改善幅が小さい場合、現行 path を維持する |
| RULE-02_SWITCH_score | score_gap が switch_threshold に達した場合、best path へ切り替える |
| RULE-05_ESCALATE_conflict | trust / stability / score の競合がある場合、Resolver に判断を委譲する |
| RULE-07_DEGRADE_trigger | 現在選択中の path が reject / invalid になった場合、DEGRADED へ遷移する |
| RULE-08_DEGRADE_keep | DEGRADED 中でも、現在の fallback path が維持可能なら切替しない |
| RULE-09_DEGRADE_switch | DEGRADED 中に維持不能な path から fallback path へ切り替える |
| RULE-10_RECOVERY_trigger | 安定かつ trusted な path が確認された場合、NORMAL 復帰を開始する |
| RULE-11_RECOVERY_cooldown | recovery 直後に cooldown を適用し、再切替を抑制する |
| RULE-12_COOLDOWN_active | Resolver cooldown 中は再 escalation / 再 switch を抑制する |
| RULE-13_RESOLVER_keep | Resolver が切替不要と判断した場合、現在 path を維持する |
| RULE-14_RESOLVER_switch | Resolver が明示的により安全な path へ切り替える |
| RULE-15_RECOVERY_CANDIDATE | 回復 path を候補として登録し、即時復帰ではなく検証へ進める |
| RULE-16_RECOVERY_VALIDATION_START | recovery candidate の validation phase を開始する |
| RULE-18_RETURN_ELIGIBLE | validation を満たした回復 path を return eligible と判定する |
| RULE-19_RETURN_SWITCH | v0.2 の staged recovery で eligible path へ復帰切替する |
| RULE-19_RETURN_RAMP_START | v0.3 の progressive recovery ramp を開始する |
| RULE-20_RETURN_KEEP | return 条件未達時、復帰切替せず current path を維持する |
| RULE-21_RETURN_RAMP_ADVANCE | ramp 条件成立時に recovered path の traffic weight を段階的に増やす |
| RULE-22_RETURN_RAMP_HOLD | ramp 中に進行条件が不足する場合、現 weight を維持する |
| RULE-23_RETURN_RAMP_ABORT | ramp 中に recovered path の不安定化を検知した場合、復帰を中断する |
| RULE-24_RETURN_RAMP_COMPLETE | recovered path への段階的 reintegration 完了を確定する |

---

## 6. STEP Traceability

| RULE | Scenario | Evidence Step | Related Trace | Evidence Log |
|------|----------|---------------|---------------|--------------|
| RULE-02_SWITCH_score | switch_score | STEP 2 | STEP 1: `RULE-01_KEEP_score` は score_gap が switch_threshold 未満のため A を維持; STEP 2: `RULE-02_SWITCH_score` は score_gap が switch_threshold に達したため A -> B へ切替 | `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md` |
| RULE-08_DEGRADE_keep | degraded_keep | STEP 2 | STEP 1: `RULE-09_DEGRADE_switch` は A unsafe 後に fallback B を選択; STEP 2: `RULE-08_DEGRADE_keep` は current degraded path B が health-valid かつ A が recovery eligible でないため B を維持 | `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md` |
| RULE-20_RETURN_KEEP | recovery_return_keep | STEP 4 | STEP 4: `RULE-18_RETURN_ELIGIBLE` が B を eligible と判定; STEP 4: `RULE-20_RETURN_KEEP` は improvement が return_margin 未満のため A を維持 | `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md` |

---

## 7. 推奨される次の補完

1. v0.3 系 RULE は Experimental のまま、仕様統合後に Verified へ昇格する。
2. 専用 validation log が存在する残りの Verified RULE に STEP traceability を追加する。
