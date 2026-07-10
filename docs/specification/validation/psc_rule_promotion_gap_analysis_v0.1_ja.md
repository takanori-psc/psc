# PSC RULE Promotion Gap Analysis v0.1

## Document Information

| 項目 | 内容 |
|------|------|
| Document ID | `PSC-RULE-PROMOTION-GAP-ANALYSIS-v0.1-ja` |
| Title | PSC RULE-21 through RULE-24 Evidence Gap Analysis |
| Version | v0.1 |
| Language | Japanese |
| Status | Draft |
| Scope | `RULE-21_RETURN_RAMP_ADVANCE` through `RULE-24_RETURN_RAMP_COMPLETE` |
| Related Criteria | `docs/specification/validation/psc_rule_promotion_criteria_v0.1_ja.md` |
| Related Evidence Matrix | `docs/specification/validation/psc_evidence_matrix_v0.1_ja.md` |

---

## 1. 目的

本書は、`RULE-21_RETURN_RAMP_ADVANCE`、`RULE-22_RETURN_RAMP_HOLD`、
`RULE-23_RETURN_RAMP_ABORT`、`RULE-24_RETURN_RAMP_COMPLETE` について、
Experimental / Hold から Verified へ昇格するための evidence coverage と
不足点を整理する draft である。

本書は gap analysis であり、既存 RULE の status を変更しない。
Evidence Matrix、promotion criteria、simulation file、log file、validator file は
本ステップでは変更しない。

---

## 2. 参照範囲

本分析では以下を参照対象とする。

| 種別 | 参照 |
|------|------|
| Promotion criteria | `docs/specification/validation/psc_rule_promotion_criteria_v0.1_ja.md` |
| Evidence Matrix | `docs/specification/validation/psc_evidence_matrix_v0.1_ja.md` |
| Recovery ramp scenarios | `sim/02_controlled/06_recovery_return_v02/` |
| LIGHT observation scenarios | `sim/02_controlled/07_light_observation_stub/` |
| Abort handling scenarios | `sim/02_controlled/08_recovery_abort_handling/` |
| Validator | `scripts/validate_evidence_rules.py` |

---

## 3. 現在の全体状況

Evidence Matrix 上では、`RULE-22_RETURN_RAMP_HOLD` は FULL observation における
`reason=INSUFFICIENT_OBSERVATION` の covered hold evidence について Verified として扱われる。
LIGHT Observation coverage は現在の Verified scope 外である。その他の対象 RULE は
引き続き Experimental であり、coverage の成熟度は RULE ごとに異なる。

| RULE | 現在の状態 | Coverage Summary | 主な不足 |
|------|------------|------------------|----------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Experimental / LIGHT は Hold | FULL observation の ramp advance ログは存在する | 専用 validator check、LIGHT false-positive / false-negative 境界、仕様本文への条件統合が不足 |
| `RULE-22_RETURN_RAMP_HOLD` | Verified | FULL `ramp_hold_insufficient_observation` scenario、raw log、verified log、validator assertion が現在の Verified scope を構成する。LIGHT hold scenario はその scope 外の evidence として残る | 仕様本文への formal integration は evidence status とは別作業として残る |
| `RULE-23_RETURN_RAMP_ABORT` | Experimental | abort class 別 scenario、raw log、verified log、validator check が存在する | abort threshold、post-abort state assertion の統一、全 abort scenario の structured result 化が不足 |
| `RULE-24_RETURN_RAMP_COMPLETE` | Experimental | ramp complete の raw / verified log は存在する | 専用 scenario 分離、validator check、completion threshold と post-completion state assertion が不足 |

---

## 4. RULE-21_RETURN_RAMP_ADVANCE Gap Analysis

### 4.1 利用可能な scenario file

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | recovery ramp v0.3 の FULL / LIGHT observation を含む統合 scenario |

### 4.2 利用可能な raw log

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_scenario_run.txt` | FULL observation 指定なしの v0.3 ramp advance trace |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | FULL / LIGHT observation mode を含む ramp advance trace |

### 4.3 利用可能な verified log / Matrix mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | baseline / ramp_complete における progressive ramp advance を記録 |
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_full_light_observation_validation_log.md` | FULL と LIGHT の observation policy 差分を記録 |
| Evidence Matrix | `recovery_ramp_v03` / `LOG-RAMP-01` として Experimental に mapping 済み |

### 4.4 validator coverage

`scripts/validate_evidence_rules.py` の `CATEGORY_RULES` には
`RULE-21_RETURN_RAMP_ADVANCE` が `switch` category として登録されている。
しかし、`SCENARIOS` には `RULE-21_RETURN_RAMP_ADVANCE` を期待 RULE とする
専用 check は存在しない。

現状の validator coverage は間接的であり、advance 前後の weight、FULL observation、
hold / abort 条件で advance しないことを assert していない。

### 4.5 不足 evidence

| 不足項目 | 内容 |
|----------|------|
| 専用 validator check | FULL observation で安定条件成立時のみ `RULE-21_RETURN_RAMP_ADVANCE` が出ること |
| negative check | hold / abort 条件では recovered weight が増えないこと |
| structured result | expected category、rule、weight delta、observation mode を機械的に assert できる戻り値 |
| specification integration | ramp_increment、advance threshold、FULL observation condition の仕様本文への統合 |
| LIGHT boundary | LIGHT observation による advance の false-positive / false-negative 境界定義 |

### 4.6 Promotion blocker

`RULE-21_RETURN_RAMP_ADVANCE` は FULL observation に限定すれば昇格候補に近いが、
専用 validator と仕様統合が不足している。

LIGHT observation に基づく `RULE-21_RETURN_RAMP_ADVANCE` は Hold のまま維持する。
LIGHT observation の false-positive / false-negative behavior が十分に境界付けられ、
LIGHT から FULL へ昇格する条件、または LIGHT advance を許可する promotion gate が
定義されるまで、LIGHT-based advance を Verified evidence として扱ってはならない。

---

## 5. RULE-22_RETURN_RAMP_HOLD Gap Analysis

### 5.1 利用可能な scenario file

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/07_light_observation_stub/light_false_negative.py` | LIGHT observation false negative 時の hold |
| `sim/02_controlled/07_light_observation_stub/light_stale_telemetry.py` | stale telemetry 時の hold |
| `sim/02_controlled/07_light_observation_stub/light_masked_instability.py` | masked instability 時の hold |
| `sim/02_controlled/07_light_observation_stub/light_telemetry_gap_stub.py` | LIGHT 固有 required telemetry gap の design stub |
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | recovery ramp 中の runnable FULL observation `ramp_hold_insufficient_observation` trace |

### 5.2 利用可能な raw log

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/07_light_observation_stub/logs/raw/light_false_negative_run.txt` | `reason=OBSERVATION_FALSE_NEGATIVE` |
| `sim/02_controlled/07_light_observation_stub/logs/raw/light_stale_telemetry_run.txt` | `reason=STALE_TELEMETRY` |
| `sim/02_controlled/07_light_observation_stub/logs/raw/light_masked_instability_run.txt` | `reason=MASKED_INSTABILITY` |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | FULL / LIGHT ramp 中の hold trace |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/ramp_hold_insufficient_observation_run.txt` | `reason=INSUFFICIENT_OBSERVATION`、`category=hold`、`observation_mode=FULL`、および `0.30 -> 0.30` の ramp level 維持 |

### 5.3 利用可能な verified log / Matrix mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/07_light_observation_stub/logs/verified/light_observation_hold_validation_log.md` | LIGHT false-negative / stale / masked instability の hold を記録 |
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_ramp_hold_insufficient_observation_validation_log.md` | prior ramp advance 後の FULL `INSUFFICIENT_OBSERVATION` hold を記録 |
| Evidence Matrix | `ramp_hold_insufficient_observation` が Verified evidence に mapping 済み。LIGHT scenario は現在の Verified scope 外の evidence として記録される |

### 5.4 validator coverage

`scripts/validate_evidence_rules.py` は以下の three runnable LIGHT scenarios を
直接 check している。

| Validator scenario | Expected RULE | Expected category |
|--------------------|---------------|-------------------|
| `light_false_negative` | `RULE-22_RETURN_RAMP_HOLD` | `hold` |
| `light_stale_telemetry` | `RULE-22_RETURN_RAMP_HOLD` | `hold` |
| `light_masked_instability` | `RULE-22_RETURN_RAMP_HOLD` | `hold` |

validator は LIGHT scenario について RULE と category を検出するが、これらの
LIGHT check は現在の Verified scope 外である。`ramp_hold_insufficient_observation`
については、reason、observation mode、state transition、ramp level 維持、
直前 step の advance、同一 step の advance / abort / complete / emergency 不発火も
assert する。

### 5.5 不足 evidence

| 不足項目 | 内容 |
|----------|------|
| LIGHT telemetry gap runnable coverage | `light_telemetry_gap_stub.py` は LIGHT 固有 design stub のままであり、今回の FULL observation ramp-hold evidence では昇格しない |
| specification integration | v0.3 ramp behavior 全体の hold / advance / abort 遷移は、仕様本文への formal integration が別途必要 |

### 5.6 Promotion blocker

`RULE-22_RETURN_RAMP_HOLD` は、Evidence Matrix 上の Verified status に必要な
covered FULL-observation hold scope の evidence set、すなわち
`INSUFFICIENT_OBSERVATION` の runnable scenario、raw log、verified log、
validator assertion が揃った。

これは LIGHT Observation scenario を現在の Verified scope に含めるものではなく、
LIGHT-based ramp advance の昇格でもなく、v0.3 ramp 仕様全体の formal integration
完了を意味するものでもない。

---

## 6. RULE-23_RETURN_RAMP_ABORT Gap Analysis

### 6.1 利用可能な scenario file

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/08_recovery_abort_handling/soft_abort_hold_and_reobserve.py` | `SOFT_ABORT` |
| `sim/02_controlled/08_recovery_abort_handling/hard_abort_ramp_down.py` | `HARD_ABORT` |
| `sim/02_controlled/08_recovery_abort_handling/emergency_cut_no_fallback.py` | `EMERGENCY_CUT` |
| `sim/02_controlled/08_recovery_abort_handling/two_path_degraded_abort.py` | `DEGRADED_ABORT` / `NO_SAFE_ALTERNATE` |
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | recovery ramp 中の abort trace |
| `sim/02_controlled/07_light_observation_stub/light_delayed_abort_stub.py` | LIGHT delayed abort の design stub |

### 6.2 利用可能な raw log

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/soft_abort_hold_and_reobserve_run.txt` | `SOFT_ABORT` / `abort_and_stabilize` |
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/hard_abort_ramp_down_run.txt` | `HARD_ABORT` / `hard_abort_ramp_down` |
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/emergency_cut_no_fallback_run.txt` | `EMERGENCY_CUT` / `NO_CAPACITY_MARGIN` |
| `sim/02_controlled/08_recovery_abort_handling/logs/raw/two_path_degraded_abort_run.txt` | `DEGRADED_ABORT` / `NO_SAFE_ALTERNATE` |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_scenario_run.txt` | recovery ramp abort trace |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | FULL / LIGHT observation abort trace |

### 6.3 利用可能な verified log / Matrix mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/08_recovery_abort_handling/logs/verified/recovery_abort_stabilization_validation_log.md` | soft / hard / emergency / two-path degraded abort を記録 |
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | ramp abort behavior を記録 |
| Evidence Matrix | abort handling scenarios が `LOG-ABORT-01` と `RAW-ABORT-*` へ mapping 済み |

### 6.4 validator coverage

`scripts/validate_evidence_rules.py` は以下の abort handling scenarios を直接 check している。

| Validator scenario | Expected RULE | Expected category |
|--------------------|---------------|-------------------|
| `soft_abort_hold_and_reobserve` | `RULE-23_RETURN_RAMP_ABORT` | `abort_and_stabilize` |
| `hard_abort_ramp_down` | `RULE-23_RETURN_RAMP_ABORT` | `hard_abort_ramp_down` |
| `emergency_cut_no_fallback` | `RULE-23_RETURN_RAMP_ABORT` | `emergency_cut_no_fallback` |
| `two_path_degraded_abort` | `RULE-23_RETURN_RAMP_ABORT` | `two_path_degraded_arbitration` |

現在の validator は RULE と category を検出できる。
ただし、abort class、fallback block reason、source notification、
stabilization action の個別 assertion は scenario 出力文字列への包含確認に依存している。

### 6.5 不足 evidence

| 不足項目 | 内容 |
|----------|------|
| structured result 統一 | `two_path_degraded_abort.py` は structured result 化済みだが、他 abort scenarios は plain string return のまま |
| abort class assertion | `SOFT_ABORT`、`HARD_ABORT`、`EMERGENCY_CUT`、`DEGRADED_ABORT` を validator が明示 assert する必要がある |
| post-abort state assertion | allocation hold、ramp down、path exclusion、least-bad arbitration などを機械検証する必要がある |
| threshold integration | abort threshold と observation mode 別 threshold を仕様本文へ統合する必要がある |
| LIGHT delayed abort | `light_delayed_abort_stub.py` の正式 runnable / raw / verified coverage が未完了 |

### 6.6 Promotion blocker

`RULE-23_RETURN_RAMP_ABORT` は scenario と raw log の coverage が最も広い。
一方で、abort class ごとの post-abort outcome を validator が十分に構造化して
検証しているとは言えない。Verified 昇格前に、abort scenarios の structured result を
統一し、fallback block reason と stabilization action を明示 assertion にする必要がある。

---

## 7. RULE-24_RETURN_RAMP_COMPLETE Gap Analysis

### 7.1 利用可能な scenario file

| Scenario file | Coverage |
|---------------|----------|
| `sim/02_controlled/06_recovery_return_v02/mini_psc_rcu_decision_v03_recovery_ramp_observation.py` | recovery ramp complete を含む統合 scenario |

### 7.2 利用可能な raw log

| Raw log | Coverage |
|---------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_scenario_run.txt` | `RULE-24_RETURN_RAMP_COMPLETE`、`recovered_weight=1.00`、`evacuation_weight=0.00` |
| `sim/02_controlled/06_recovery_return_v02/logs/raw/recovery_ramp_v03_full_light_run.txt` | FULL observation mode での complete trace |

### 7.3 利用可能な verified log / Matrix mapping

| Evidence | Coverage |
|----------|----------|
| `sim/02_controlled/06_recovery_return_v02/logs/rcu_decision_v03_recovery_ramp_validation_log.md` | ramp_complete scenario と `RULE-24_RETURN_RAMP_COMPLETE` を記録 |
| Evidence Matrix | `recovery_ramp_v03` / `LOG-RAMP-03` として Experimental に mapping 済み |

### 7.4 validator coverage

`scripts/validate_evidence_rules.py` の `CATEGORY_RULES` には
`RULE-24_RETURN_RAMP_COMPLETE` が `switch` category として登録されている。
しかし、`SCENARIOS` には `RULE-24_RETURN_RAMP_COMPLETE` を期待 RULE とする
専用 check は存在しない。

現状では completion threshold、final allocation、post-completion state、
additional advance が発生しないことを validator が assert していない。

### 7.5 不足 evidence

| 不足項目 | 内容 |
|----------|------|
| 専用 scenario | ramp complete を単独主対象にした再現 scenario |
| 専用 validator check | `RULE-24_RETURN_RAMP_COMPLETE` と final allocation の assertion |
| completion threshold | completion の判定閾値を仕様本文で明示する必要がある |
| post-completion state | completion 後に stable state であることの raw / validator evidence |
| no additional advance | complete 後に不要な additional advance が出ないことの assertion |

### 7.6 Promotion blocker

`RULE-24_RETURN_RAMP_COMPLETE` は raw / verified log には現れているが、
promotion criteria が要求する validator check と completion condition の仕様化が不足している。
現時点では Verified 昇格には早い。

---

## 8. Validator Coverage Summary

| RULE | Current validator coverage | Gap |
|------|----------------------------|-----|
| `RULE-21_RETURN_RAMP_ADVANCE` | category mapping には存在するが、専用 scenario check なし | FULL advance 条件、weight delta、negative check が不足 |
| `RULE-22_RETURN_RAMP_HOLD` | 現在の Verified scope では FULL `ramp_hold_insufficient_observation` scenario を直接 check する。LIGHT hold check は scope 外の coverage として維持 | LIGHT reason-specific assertion、weight unchanged check は将来 coverage work として残る |
| `RULE-23_RETURN_RAMP_ABORT` | four abort handling scenarios を直接 check | abort class / fallback reason / post-abort action の構造化 assertion が不足 |
| `RULE-24_RETURN_RAMP_COMPLETE` | category mapping には存在するが、専用 scenario check なし | completion threshold、final allocation、post-completion state check が不足 |

`scripts/validate_evidence_rules.py` の現状は、Evidence Matrix の代表 RULE が
出力に現れることを確認する smoke / traceability validator として有効である。
Verified 昇格用には、RULE-21 through RULE-24 専用の state assertion を追加する必要がある。

---

## 9. 推奨昇格順序

昇格作業は以下の順序を推奨する。

1. `RULE-22_RETURN_RAMP_HOLD`
2. `RULE-23_RETURN_RAMP_ABORT`
3. `RULE-21_RETURN_RAMP_ADVANCE (FULL only)`
4. `RULE-24_RETURN_RAMP_COMPLETE`

理由:

- `RULE-22` は LIGHT hold の safety boundary を固める前提であり、LIGHT advance を抑止する基盤になる。
- `RULE-23` は unsafe path への復帰を止める安全側 RULE であり、advance / complete より先に固めるべきである。
- `RULE-21` は FULL observation に限定してから昇格判断する。LIGHT-based advance は Hold のまま維持する。
- `RULE-24` は advance / hold / abort の境界が固まった後に completion condition として昇格判断する。

---

## 10. 主要 blocker 一覧

| RULE | Promotion blocker |
|------|-------------------|
| `RULE-21_RETURN_RAMP_ADVANCE` | LIGHT false-positive / false-negative 境界未定義、FULL advance 専用 validator 不足 |
| `RULE-22_RETURN_RAMP_HOLD` | FULL / `INSUFFICIENT_OBSERVATION` の covered hold behavior について evidence blocker は解消済み。LIGHT Observation coverage と v0.3 仕様全体への formal integration は別作業として残る |
| `RULE-23_RETURN_RAMP_ABORT` | abort class ごとの post-abort action assertion 不足、structured result 統一不足 |
| `RULE-24_RETURN_RAMP_COMPLETE` | completion threshold、final allocation、post-completion state の validator 不足 |

---

## 11. 結論

現時点で `RULE-22_RETURN_RAMP_HOLD` は、FULL / `INSUFFICIENT_OBSERVATION` hold
evidence について、Evidence Matrix 上の Verified status に必要な scenario / raw log /
verified log / Evidence Matrix mapping / validator assertion が揃った。
LIGHT Observation scenario は現在の Verified scope 外に残る。残る Experimental RULE の中では、
`RULE-23_RETURN_RAMP_ABORT` が次の昇格候補である。

`RULE-21_RETURN_RAMP_ADVANCE` は FULL observation に限定すれば昇格候補になり得るが、
LIGHT observation に基づく advance は Hold のまま維持する。
false-positive / false-negative behavior が十分に境界付けられるまで、
LIGHT-based advance を Verified evidence として扱ってはならない。

`RULE-24_RETURN_RAMP_COMPLETE` は completion trace は存在するが、
専用 validator と completion condition の仕様化が不足しているため、
RULE-21 / RULE-22 / RULE-23 の境界整理後に昇格判断する。
