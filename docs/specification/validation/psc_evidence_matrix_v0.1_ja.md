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

| RULE | 問題 | 設計意図 | シナリオ | Log Ref | 状態 |
|------|------|----------|----------|----------|------|
| RULE-01_KEEP_score | 小さな score 変動による不要切替 | hysteresis による安定経路維持 | stable / degraded / recovery_hold | `LOG-DEG-01` | Verified |
| RULE-02_SWITCH_score | 明確な score 優位があるにもかかわらず切替されない危険 | score_gap が switch_threshold に達した場合に best path へ切替 | switch_score | `LOG-SW-01` | Verified |
| RULE-04_BLOCK_trust | trust block された path への危険な切替 | score または trust-switch rule が切替を選好しても unsafe switch candidate を block する | trust_block_vs_switch | `LOG-TRUST-BLOCK-01` | Verified |
| RULE-05_ESCALATE_conflict | trust / stability / score 競合による曖昧判断 | Resolver へ仲裁要求 | oscillation / resolver_switch | `LOG-RES-01` | Verified |
| RULE-07_DEGRADE_trigger | 選択中 path の trust 低下または invalid 化 | NORMAL から DEGRADED への安全側遷移 | degraded | `LOG-DEG-01` | Verified |
| RULE-08_DEGRADE_keep | DEGRADED 中の不要な fallback 切替 | degraded mode でも安定 path を維持 | degraded_keep | `LOG-DEG-02` | Verified |
| RULE-09_DEGRADE_switch | trust 低下時に現在 path が維持不能 | degraded fallback path へ切替 | degraded | `LOG-DEG-01` | Verified |
| RULE-10_RECOVERY_trigger | trusted path 回復後の復帰判定 | 安定・信頼条件を満たした場合のみ NORMAL 復帰 | degraded_recovery / recovery_hold | `LOG-REC-01` | Verified |
| RULE-11_RECOVERY_cooldown | 復帰直後の再劣化・再切替 | recovery cooldown による復帰後安定化 | degraded_recovery / recovery_hold | `LOG-DEG-01` | Verified |
| RULE-12_COOLDOWN_active | Resolver 介入直後の連続 escalation | cooldown による oscillation 抑制 | oscillation / resolver_switch | `LOG-OSC-01` | Verified |
| RULE-13_RESOLVER_keep | Resolver 介入時に切替不要 | Resolver 判断による KEEP | oscillation / resolver_keep | `LOG-RES-02` | Verified |
| RULE-14_RESOLVER_switch | ローカル RCU 判断では安全に決めきれない競合 | Resolver 主導の明示的切替 | resolver_switch | `LOG-RES-01` | Verified |
| RULE-15_RECOVERY_CANDIDATE | 回復 path を即時復帰させる危険 | recovery candidate として段階評価へ移す | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-16_RECOVERY_VALIDATION_START | 回復 path の安定性確認不足 | validation phase 開始 | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-18_RETURN_ELIGIBLE | 復帰可能条件の不明瞭化 | return switch 前の eligibility 確定 | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-19_RETURN_SWITCH | v0.2 staged recovery の復帰実行 | validation 済み path へ制御された復帰 | recovery_return_v02 | `LOG-RR-01` | Verified |
| RULE-20_RETURN_KEEP | 復帰候補が条件未達のまま切替される危険 | current path 維持 | recovery_return_keep | `LOG-RR-02` | Verified |
| RULE-21_RETURN_RAMP_ADVANCE | ramp 中の進行条件不明瞭 | 安定時のみ recovered weight を増加 | recovery_ramp_v03 | `LOG-RAMP-01` | Experimental |
| RULE-22_RETURN_RAMP_HOLD | ramp 中の一時停止条件不明瞭 | 条件未達時に ramp を維持 | ramp_hold_insufficient_observation | `LOG-RAMP-HOLD-INSUFF-01`; `RAW-RAMP-HOLD-INSUFF-01` | Verified |
| RULE-23_RETURN_RAMP_ABORT | 不安定 path への早期復帰 | ramp 中の異常検知時に復帰を中断 | recovery_ramp_v03 / soft_abort_hold_and_reobserve / hard_abort_ramp_down / emergency_cut_no_fallback / two_path_degraded_abort | `LOG-RAMP-03`; `LOG-ABORT-01` | Experimental |
| RULE-24_RETURN_RAMP_COMPLETE | recovery 完了判定の不明瞭化 | progressive reintegration 完了を確定 | recovery_ramp_v03 | `LOG-RAMP-03` | Experimental |
| RULE-25_RETURN_RAMP_START | recovery 直後の急激な全量復帰 | progressive return ramp 開始 | recovery_ramp_v03 | `LOG-RAMP-02` | Experimental |

---

### 2.1 RULE-22 Verified Scope Note

`RULE-22_RETURN_RAMP_HOLD` は、FULL observation における
`reason=INSUFFICIENT_OBSERVATION` の hold evidence について Verified とする。

LIGHT Observation シナリオは、この Verified 範囲には含まれない。

この status は、RULE-22 の全 reason、全 observation mode、または
v0.3 Recovery Ramp behavior 全体の検証完了を意味しない。

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

| Scenario | Purpose | Log Ref |
|----------|---------|----------|
| stable | 通常時の KEEP / SWITCH 抑制確認 | `LOG-DEG-01` |
| switch_score | threshold 未満の RULE-01 keep と threshold 到達時の RULE-02 switch 確認 | `LOG-SW-01` |
| trust_block_vs_switch | RULE-04 trust block が RULE-02 score switch および RULE-03 trust switch より優先され、BLOCK_SWITCH になることを確認 | `LOG-TRUST-BLOCK-01` |
| oscillation | ECMP 的な score 追従と比較した oscillation 抑制確認 | `LOG-OSC-01` |
| resolver_switch | trust / stability 競合時の Resolver 主導切替確認 | `LOG-RES-01` |
| degraded | trust 低下時の DEGRADED 遷移と fallback 確認 | `LOG-DEG-01` |
| degraded_keep | current degraded path が維持可能かつ candidate が recovery eligible でない場合の DEGRADED keep 確認 | `LOG-DEG-02` |
| degraded_recovery | DEGRADED から NORMAL への安全復帰確認 | `LOG-REC-01` |
| recovery_hold | 回復後も current path を維持する conservative hold 確認 | `LOG-HOLD-01` |
| recovery_return_v02 | Recovery Candidate -> Validation -> Return Eligible -> Return Switch 確認 | `LOG-RR-01` |
| recovery_return_keep | improvement が return_margin 未満の場合の Return Eligible -> Return Keep 確認 | `LOG-RR-02` |
| recovery_ramp_v03 | progressive ramp / abort / complete / observation policy 確認 | `LOG-RAMP-03` |
| ramp_hold_insufficient_observation | `FULL` observation の mid-ramp `INSUFFICIENT_OBSERVATION` で recovered weight が維持され、同一 HOLD step の ramp advance / abort / complete / emergency transition が抑制されることを確認 | `LOG-RAMP-HOLD-INSUFF-01`; `RAW-RAMP-HOLD-INSUFF-01` |
| light_false_negative | 実際の instability が LIGHT observation で検出されない場合に ramp を hold することを確認 | `LOG-LIGHT-HOLD-01`; `RAW-LIGHT-FN-01` |
| light_stale_telemetry | telemetry が古い場合に LIGHT observation が ramp を hold することを確認 | `LOG-LIGHT-HOLD-01`; `RAW-LIGHT-ST-01` |
| light_masked_instability | sparse evidence により instability が隠れる場合に LIGHT observation が ramp を hold することを確認 | `LOG-LIGHT-HOLD-01`; `RAW-LIGHT-MI-01` |
| soft_abort_hold_and_reobserve | SOFT_ABORT で allocation を保持し、observation 強化と Resolver re-evaluation を行うことを確認 | `LOG-ABORT-01`; `RAW-ABORT-SOFT-01` |
| hard_abort_ramp_down | HARD_ABORT で suspect recovered path を ramp down し source-side PSC に通知することを確認 | `LOG-ABORT-01`; `RAW-ABORT-HARD-01` |
| emergency_cut_no_fallback | EMERGENCY_CUT で unsafe path を除外し、capacity margin 不足時に fallback transfer を block することを確認 | `LOG-ABORT-01`; `RAW-ABORT-EMERG-01` |
| two_path_degraded_abort | safe alternate が存在しない二経路 degraded abort で Resolver least-bad arbitration を行うことを確認 | `LOG-ABORT-01`; `RAW-ABORT-2PATH-01` |

---

## 5. RULE Definitions

| RULE | Summary |
|------|---------|
| RULE-01_KEEP_score | score 差または改善幅が小さい場合、現行 path を維持する |
| RULE-02_SWITCH_score | score_gap が switch_threshold に達した場合、best path へ切り替える |
| RULE-04_BLOCK_trust | explicit trust_block または trust threshold 未満を検出した場合に切替を禁止する。これらは別原因だが、結果はいずれも同じ safety outcome として、score / trust による switch candidate より先に switch を block する |
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
| RULE-20_RETURN_KEEP | return 条件未達時、復帰切替せず current path を維持する |
| RULE-21_RETURN_RAMP_ADVANCE | ramp 条件成立時に recovered path の traffic weight を段階的に増やす |
| RULE-22_RETURN_RAMP_HOLD | ramp 中に進行条件が不足する場合、現 weight を維持する |
| RULE-23_RETURN_RAMP_ABORT | ramp 中に recovered path の不安定化を検知した場合、復帰を中断する |
| RULE-24_RETURN_RAMP_COMPLETE | recovered path への段階的 reintegration 完了を確定する |
| RULE-25_RETURN_RAMP_START | v0.3 の progressive recovery ramp を開始する |

---

## 6. STEP Traceability

| RULE | Scenario | Evidence Step | Trace Summary | Log Ref |
|------|----------|---------------|---------------|--------------|
| RULE-01_KEEP_score | stable / degraded_recovery / resolver_switch | STEP 1 / STEP 6 / STEP 2 | 小幅改善や cooldown 中の不要切替を hysteresis で抑制 | `LOG-SW-01`; `LOG-REC-01`; `LOG-RES-01` |
| RULE-02_SWITCH_score | switch_score | STEP 2 | score_gap が threshold 到達後に A -> B へ切替 | `LOG-SW-01` |
| RULE-04_BLOCK_trust | trust_block_vs_switch | STEP 0 | B を trust-blocked として block し、`RULE-02_SWITCH_score` と `RULE-03_SWITCH_trust` より優先され、final action `BLOCK_SWITCH` になる | `LOG-TRUST-BLOCK-01` |
| RULE-05_ESCALATE_conflict | resolver_switch / oscillation | STEP 1 / STEP 4 | trust conflict / oscillation 条件で Resolver へ escalation | `LOG-RES-01`; `LOG-OSC-01` |
| RULE-07_DEGRADE_trigger | degraded / degraded_keep | STEP 3 / STEP 1 | selected path の reject / unsafe により DEGRADED へ遷移 | `LOG-DEG-01`; `LOG-DEG-02` |
| RULE-08_DEGRADE_keep | degraded_keep | STEP 2 | health-valid な degraded fallback を維持 | `LOG-DEG-02` |
| RULE-09_DEGRADE_switch | degraded / degraded_keep | STEP 3 / STEP 1 | unsafe / invalid path から fallback path へ切替 | `LOG-DEG-01`; `LOG-DEG-02` |
| RULE-10_RECOVERY_trigger | degraded_recovery / recovery_hold | STEP 3 / STEP 4 | stable trusted path を確認して NORMAL へ復帰 | `LOG-REC-01`; `LOG-HOLD-01` |
| RULE-11_RECOVERY_cooldown | degraded_recovery / recovery_hold | STEP 4-5 / STEP 5-6 | recovery 直後の再評価を cooldown で抑制 | `LOG-REC-01`; `LOG-HOLD-01` |
| RULE-12_COOLDOWN_active | resolver_switch / oscillation | STEP 2-3 / STEP 2-3 | Resolver 介入後の連続 escalation / switch を抑制 | `LOG-RES-01`; `LOG-OSC-01` |
| RULE-13_RESOLVER_keep | resolver_keep / oscillation | STEP 1 / STEP 4 | Resolver が同一選択を維持し不要切替を回避 | `LOG-RES-02`; `LOG-OSC-01` |
| RULE-14_RESOLVER_switch | resolver_switch / oscillation | STEP 1 | Resolver が競合を解決し A/B 間を明示切替 | `LOG-RES-01`; `LOG-OSC-01` |
| RULE-15_RECOVERY_CANDIDATE | recovery_return_v02 | STEP 6 | recovered path を即時復帰せず候補登録 | `LOG-RR-01` |
| RULE-16_RECOVERY_VALIDATION_START | recovery_return_v02 | STEP 7 | recovery candidate の validation phase を開始 | `LOG-RR-01` |
| RULE-18_RETURN_ELIGIBLE | recovery_return_v02 / recovery_return_keep | STEP 7 / STEP 4 | validation passed 後に return eligibility を確定 | `LOG-RR-01`; `LOG-RR-02` |
| RULE-19_RETURN_SWITCH | recovery_return_v02 | STEP 7 | eligible path へ controlled return switch | `LOG-RR-01` |
| RULE-20_RETURN_KEEP | recovery_return_keep | STEP 4 | return_margin 未満のため current path を維持 | `LOG-RR-02` |
| RULE-22_RETURN_RAMP_HOLD | light_false_negative / light_stale_telemetry / light_masked_instability | STEP 0 / STEP 0 / STEP 0 | LIGHT recovery ramp を false-negative、stale、masked instability の evidence 条件で hold する。evidence は利用可能だが、現在の Verified scope 外である | `RAW-LIGHT-FN-01`; `RAW-LIGHT-ST-01`; `RAW-LIGHT-MI-01`; `LOG-LIGHT-HOLD-01` |
| RULE-22_RETURN_RAMP_HOLD | ramp_hold_insufficient_observation | STEP 9 -> STEP 10 | STEP 9 で `RULE-21_RETURN_RAMP_ADVANCE` が emit され ramp が `0.10` から `0.30` へ進んだ後、STEP 10 で `category=hold`、`reason=INSUFFICIENT_OBSERVATION`、`observation_mode=FULL`、`state_transition=RAMPING->RAMPING` を伴う `RULE-22_RETURN_RAMP_HOLD` が emit される。`recovered_weight_before=0.30` と `recovered_weight_after=0.30` を維持し、同一 HOLD step では advance / abort / complete / emergency transition marker を emit しない | `LOG-RAMP-HOLD-INSUFF-01`; `RAW-RAMP-HOLD-INSUFF-01`; validator `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_hold_insufficient_observation`) |
| RULE-23_RETURN_RAMP_ABORT | soft_abort_hold_and_reobserve / hard_abort_ramp_down / emergency_cut_no_fallback / two_path_degraded_abort | STEP 0 / STEP 0 / STEP 0 / STEP 0 | active Return Ramp attempt を abort し、abort class に応じて stabilization、ramp-down、emergency cut、または two-path degraded arbitration を適用 | `RAW-ABORT-SOFT-01`; `RAW-ABORT-HARD-01`; `RAW-ABORT-EMERG-01`; `RAW-ABORT-2PATH-01`; `LOG-ABORT-01` |

---

### 6.1 Trust Switch Coverage Note

`RULE-03_SWITCH_trust` は collision matrix 上では active rule であるが、
本 Evidence Matrix version では Verified に昇格しない。
`trust_block_vs_switch` では suppressed switch candidate として出現するが、
`RULE-03_SWITCH_trust` が final switch action になる専用 validation scenario は
現時点では存在しない。

---

## 7. LIGHT Observation Evidence Details

| シナリオ | Scenario File | RULE | Expected Category | Reason | Raw Log | Verified Log | Coverage Status | Verified Scope |
|----------|---------------|------|-------------------|--------|---------|--------------|-----------------|----------------|
| light_false_negative | `sim/02_controlled/07_light_observation_stub/light_false_negative.py` | RULE-22_RETURN_RAMP_HOLD | hold | OBSERVATION_FALSE_NEGATIVE | `RAW-LIGHT-FN-01` | `LOG-LIGHT-HOLD-01` | Evidence available, outside the current Verified scope | Excluded |
| light_stale_telemetry | `sim/02_controlled/07_light_observation_stub/light_stale_telemetry.py` | RULE-22_RETURN_RAMP_HOLD | hold | STALE_TELEMETRY | `RAW-LIGHT-ST-01` | `LOG-LIGHT-HOLD-01` | Evidence available, outside the current Verified scope | Excluded |
| light_masked_instability | `sim/02_controlled/07_light_observation_stub/light_masked_instability.py` | RULE-22_RETURN_RAMP_HOLD | hold | MASKED_INSTABILITY | `RAW-LIGHT-MI-01` | `LOG-LIGHT-HOLD-01` | Evidence available, outside the current Verified scope | Excluded |

---

## 7.1 Return Ramp Hold Evidence Details

`RULE-22_RETURN_RAMP_HOLD` は、以下の FULL /
`INSUFFICIENT_OBSERVATION` coverage 行についてのみ Verified とする。
LIGHT Observation coverage は Section 7 に別掲し、現在の Verified scope 外とする。

| シナリオ | Scenario File | RULE | Expected Category | Reason | Observation Mode | Condition | Raw Log | Verified Log | Validator | 状態 | Note |
|----------|---------------|------|-------------------|--------|------------------|-----------|---------|--------------|-----------|------|------|
| ramp_hold_insufficient_observation | `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | RULE-22_RETURN_RAMP_HOLD | hold | INSUFFICIENT_OBSERVATION | FULL | STEP 9 で `0.10` から `0.30` へ advance し、STEP 10 で `0.30 -> 0.30` を保持する。`state_transition=RAMPING->RAMPING` であり、同一 step の advance / abort / complete / emergency transition は発生しない | `RAW-RAMP-HOLD-INSUFF-01` | `LOG-RAMP-HOLD-INSUFF-01` | reason / category / observation mode / state transition / unchanged ramp level / previous-step advance / forbidden outcomes in `scripts/validate_evidence_rules.py` (`ScenarioCheck.name=ramp_hold_insufficient_observation`) | Verified | この FULL observation hold reason について runnable scenario、raw log、verified log、validator assertion が揃った |

---

## 8. Recovery Abort Handling Evidence Details

| シナリオ | Scenario File | RULE | Expected Category | Abort Class | Fallback Block Reason | Raw Log | Verified Log | 状態 |
|----------|---------------|------|-------------------|-------------|-----------------------|---------|--------------|------|
| soft_abort_hold_and_reobserve | `sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py` | RULE-23_RETURN_RAMP_ABORT | abort_and_stabilize | SOFT_ABORT | N/A | `RAW-ABORT-SOFT-01` | `LOG-ABORT-01` | Experimental |
| hard_abort_ramp_down | `sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py` | RULE-23_RETURN_RAMP_ABORT | hard_abort_ramp_down | HARD_ABORT | N/A | `RAW-ABORT-HARD-01` | `LOG-ABORT-01` | Experimental |
| emergency_cut_no_fallback | `sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py` | RULE-23_RETURN_RAMP_ABORT | emergency_cut_no_fallback | EMERGENCY_CUT | NO_CAPACITY_MARGIN | `RAW-ABORT-EMERG-01` | `LOG-ABORT-01` | Experimental |
| two_path_degraded_abort | `sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py` | RULE-23_RETURN_RAMP_ABORT | two_path_degraded_arbitration | DEGRADED_ABORT | NO_SAFE_ALTERNATE | `RAW-ABORT-2PATH-01` | `LOG-ABORT-01` | Experimental |

---

## 9. v0.3 Experimental RULE 統合候補

| RULE | 分類 | Summary | Next |
|------|------|----------|----------|
| RULE-25_RETURN_RAMP_START | 正式統合候補 | v0.3 ramp の開始点 | RULE-19 との差分明文化 |
| RULE-21_RETURN_RAMP_ADVANCE (FULL) | 正式統合候補 | 安定時のみ weight 増加 | advance 条件定義 |
| RULE-22_RETURN_RAMP_HOLD | 正式統合候補 | 観測待ちで weight 維持 | hold / advance / abort 遷移定義 |
| RULE-23_RETURN_RAMP_ABORT | 正式統合候補 | 不安定化時に復帰中断 | abort threshold 定義 |
| RULE-24_RETURN_RAMP_COMPLETE | 正式統合候補 | reintegration 完了確定 | completion 条件定義 |
| RULE-21_RETURN_RAMP_ADVANCE (LIGHT) | 保留 | 観測省略時の安全境界不足 | Fast Mode 仕様と接続 |

注記:

- v0.3 ramp behavior は formal specification integration の対象として残る。`RULE-22_RETURN_RAMP_HOLD` は、本 matrix では `INSUFFICIENT_OBSERVATION` を含む covered hold evidence について Verified とする。
- 正式統合候補は「仕様へ取り込む価値がある」という分類であり、Verified への昇格ではない。
- `RULE-19_RETURN_SWITCH` は、Verified 済みの v0.2 direct return rule として維持する。
- `RULE-25_RETURN_RAMP_START` は、Experimental な v0.3 ramp entry rule である。direct return execution point を progressive ramp start に置き換えるが、`RULE-19_RETURN_SWITCH` と意味的に同一ではない。
- `RULE-25_RETURN_RAMP_START` は、formal integration が完了するまで `RULE-01` through `RULE-24` の Verified namespace 外に置く。
- `RULE-21_RETURN_RAMP_ADVANCE (FULL)` は、ramp advancement の experimental / formal integration candidate として維持する。
- `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` は Hold のまま維持する。現在の authoritative LIGHT policy では、LIGHT observation は FULL observation へ昇格するか、明示的な LIGHT promotion gates が定義され満たされるまで、`RULE-22_RETURN_RAMP_HOLD` を emit または resolve しなければならない。
- `ramp_light_tolerates_moderate_dip` を含む historical v0.3 LIGHT advance logs は experimental history として保持するが、現在の expected LIGHT policy として扱ってはならない。
- Verified 昇格には、遷移条件、threshold、FULL / LIGHT observation の扱いを仕様本文へ統合する必要がある。

---

## 10. Log References

- `LOG-DEG-01`: `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_rule_validation_log.md`
- `LOG-DEG-02`: `sim/02_controlled/04_degraded/logs/rcu_decision_v01_degraded_keep_validation_log.md`
- `LOG-ABORT-01`: `sim/02_controlled/08_recovery_abort_handling/logs/verified/recovery_abort_stabilization_validation_log.md`
- `LOG-HOLD-01`: `sim/02_controlled/05_recovery_hold/logs/rcu_decision_v01_recovery_hold_behavior_log.md`
- `LOG-LIGHT-HOLD-01`: `sim/02_controlled/07_light_observation_stub/logs/verified/light_observation_hold_validation_log.md`
- `LOG-OSC-01`: `sim/02_controlled/03_oscillation/logs/rcu_decision_v01_oscillation_ecmp_comparison_log.md`
- `LOG-REC-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_degraded_switch_recovery_rule_log.md`
- `LOG-RES-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_switch_rule_log.md`
- `LOG-RES-02`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_resolver_rule_unification_log.md`
- `LOG-RR-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_recovery_return_validation_log.md`
- `LOG-RR-02`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v02_return_keep_validation_log.md`
- `LOG-RAMP-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_full_light_observation_validation_log.md`
- `LOG-RAMP-02`: `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt`
- `LOG-RAMP-03`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md`
- `LOG-RAMP-HOLD-INSUFF-01`: `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_ramp_hold_insufficient_observation_validation_log.md`
- `LOG-SW-01`: `sim/02_controlled/02_rcu_decision_v01/logs/rcu_decision_v01_switch_score_validation_log.md`
- `LOG-TRUST-BLOCK-01`: `sim/02_controlled/09_rule_collision_matrix/logs/trust_block_vs_switch_validation_log.md`
- `RAW-RAMP-HOLD-INSUFF-01`: `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_hold_insufficient_observation_run.txt`
- `RAW-LIGHT-FN-01`: `sim/02_controlled/07_light_observation_stub/logs/raw/light_false_negative_run.txt`
- `RAW-LIGHT-ST-01`: `sim/02_controlled/07_light_observation_stub/logs/raw/light_stale_telemetry_run.txt`
- `RAW-LIGHT-MI-01`: `sim/02_controlled/07_light_observation_stub/logs/raw/light_masked_instability_run.txt`
- `RAW-ABORT-SOFT-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/soft_abort_hold_and_reobserve_run.txt`
- `RAW-ABORT-HARD-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/hard_abort_ramp_down_run.txt`
- `RAW-ABORT-EMERG-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/emergency_cut_no_fallback_run.txt`
- `RAW-ABORT-2PATH-01`: `sim/02_controlled/08_recovery_abort_handling/logs/raw/two_path_degraded_abort_run.txt`

---

## 11. Glossary References

- `GLOSSARY-LIGHT-JA-01`: `docs/specification/published/glossary/psc_light_observation_glossary_v0.1_ja.md`
