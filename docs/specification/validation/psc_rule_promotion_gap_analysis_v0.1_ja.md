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
`RULE-23_RETURN_RAMP_ABORT`、`RULE-24_RETURN_RAMP_COMPLETE` について、当初の
evidence gap、Verified 昇格時に解消された gap、および現在残る作業を追跡する。

本書は RULE status の正本ではない。status と Verified scope の正本は Evidence Matrix
であり、本書はその状態を説明する gap-closure record である。Promotion Criteria、
Evidence Matrix、simulation、validator、log の変更は本書の対象外とする。

---

## 2. 参照範囲

| 種別 | 参照 |
|------|------|
| Promotion criteria | `docs/specification/validation/psc_rule_promotion_criteria_v0.1_ja.md` |
| Authoritative Evidence Matrix | `docs/specification/validation/psc_evidence_matrix_v0.1_ja.md` |
| Recovery ramp scenarios | `sim/02_controlled/06_recovery_return_v02/` |
| LIGHT observation scenarios | `sim/02_controlled/07_light_observation_stub/` |
| Abort handling scenarios | `sim/02_controlled/08_recovery_abort_handling/` |
| Validator | `scripts/validate_evidence_rules.py` |

---

## 3. 現在の全体状況

Evidence Matrix では、RULE-21 through RULE-24 は次の限定 scope で Verified へ
昇格済みである。LIGHT observation に基づく advance は Hold、LIGHT observation
coverage とその他の scope 外 evidence は Hold または Experimental、ramp engine 内部の
`RECOVERED_PATH_UNSTABLE` / `RECOVERED_PATH_INVALID` abort trace は Experimental の
ままであり、Verified scope に含まれない。

| RULE | 現在の状態 | Verified scope | Scope 外 |
|------|------------|----------------|----------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Verified（FULL のみ） | FULL advance の positive / negative evidence | LIGHT advance は Hold |
| `RULE-22_RETURN_RAMP_HOLD` | Verified（限定 scope） | FULL / `INSUFFICIENT_OBSERVATION` hold | LIGHT hold coverage は Verified scope 外 |
| `RULE-23_RETURN_RAMP_ABORT` | Verified（限定 scope） | 4 つの FULL abort class | LIGHT delayed abort と ramp engine 内部 abort trace は Experimental / scope 外 |
| `RULE-24_RETURN_RAMP_COMPLETE` | Verified（FULL のみ） | FULL completion と post-completion state | LIGHT completion は scope 外 |

---

## 4. RULE-21_RETURN_RAMP_ADVANCE Gap Analysis

### 4.1 Available Evidence

| 種別 | Evidence |
|------|----------|
| Scenario | `mini_psc_rcu_decision_v03_recovery_ramp_observation.py`: `ramp_complete`（positive）、`ramp_abort_full_stability_dip`（negative） |
| Raw log | `ramp_complete_run.txt` (`RAW-RAMP-FULL-ADV-01`)、`ramp_abort_full_stability_dip_run.txt` (`RAW-RAMP-ABORT-FULLDIP-01`) |
| Verified log | `rcu_decision_v03_ramp_full_advance_validation_log.md` (`LOG-RAMP-FULL-ADV-01`) |
| Validator | `ScenarioCheck.name=ramp_complete` と `ScenarioCheck.name=ramp_abort_full_stability_dip` |
| Matrix mapping | FULL advance sequence と instability 時の advance 不発火を Verified 行へ mapping |

### 4.2 Resolved Gaps

- FULL observation で `0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90` の advance sequence を確認した。
- `category=switch`、FULL observation、`RECOVERED_PATH_STABLE`、completion 到達を validator が assert する。
- instability が advance 予定 step の直前に発生した場合、RULE-21 と RULE-24 が発火せず、weight が `0.10` のままであることを negative evidence で確認した。

### 4.3 Remaining Gaps

- `ramp_increment`、advance threshold、FULL observation condition の formal specification integration。
- LIGHT observation の false-positive / false-negative 境界と promotion gate の追加検証。

### 4.4 Gap Closure

`ramp_complete` と `ramp_abort_full_stability_dip`、対応する 2 raw log、
`LOG-RAMP-FULL-ADV-01`、advance transition / mode / reason / completion / forbidden
abort の validator assertion、および Evidence Matrix の RULE-21 Verified mapping により、
FULL observation scope の evidence gap は閉じた。LIGHT advance は Hold のままである。

---

## 5. RULE-22_RETURN_RAMP_HOLD Gap Analysis

### 5.1 Available Evidence

| 種別 | Evidence |
|------|----------|
| Scenario | `mini_psc_rcu_decision_v03_recovery_ramp_observation.py`: `ramp_hold_insufficient_observation` |
| Raw log | `ramp_hold_insufficient_observation_run.txt` (`RAW-RAMP-HOLD-INSUFF-01`) |
| Verified log | `rcu_decision_v03_ramp_hold_insufficient_observation_validation_log.md` (`LOG-RAMP-HOLD-INSUFF-01`) |
| Validator | `ScenarioCheck.name=ramp_hold_insufficient_observation` |
| Matrix mapping | FULL / `INSUFFICIENT_OBSERVATION` hold を Verified 行へ mapping |

LIGHT の `light_false_negative`、`light_stale_telemetry`、`light_masked_instability`
scenario と `LOG-LIGHT-HOLD-01` / `RAW-LIGHT-*` も利用可能だが、現在の Verified
scope 外の evidence である。`light_telemetry_gap_stub.py` は design stub である。

### 5.2 Resolved Gaps

- FULL observation で `reason=INSUFFICIENT_OBSERVATION` の runnable hold trace を取得した。
- STEP 9 の advance 後、STEP 10 で `0.30 -> 0.30`、`RAMPING->RAMPING` を維持することを確認した。
- 同一 step の advance / abort / complete / emergency 不発火を validator が assert する。

### 5.3 Remaining Gaps

- ramp の hold / advance / abort 遷移の formal specification integration。
- LIGHT observation 境界（telemetry gap を含む）の追加検証。

### 5.4 Gap Closure

`ramp_hold_insufficient_observation`、`RAW-RAMP-HOLD-INSUFF-01`、
`LOG-RAMP-HOLD-INSUFF-01`、reason / category / mode / state transition / unchanged
weight / forbidden outcome の validator assertion、および Evidence Matrix の RULE-22
Verified mapping により、FULL / `INSUFFICIENT_OBSERVATION` scope の gap は閉じた。

---

## 6. RULE-23_RETURN_RAMP_ABORT Gap Analysis

### 6.1 Available Evidence

| Abort class | Scenario | Raw log | Verified log |
|-------------|----------|---------|--------------|
| `SOFT_ABORT` | `soft_abort_hold_and_reobserve` | `RAW-ABORT-SOFT-01` | `LOG-ABORT-01` |
| `HARD_ABORT` | `hard_abort_ramp_down` | `RAW-ABORT-HARD-01` | `LOG-ABORT-01` |
| `EMERGENCY_CUT` | `emergency_cut_no_fallback` | `RAW-ABORT-EMERG-01` | `LOG-ABORT-01` |
| `DEGRADED_ABORT` | `two_path_degraded_abort` | `RAW-ABORT-2PATH-01` | `LOG-ABORT-01` |

4 scenario はそれぞれ `scripts/validate_evidence_rules.py` の同名 `ScenarioCheck` で
検証され、Evidence Matrix の RULE-23 Verified 行へ mapping されている。

### 6.2 Resolved Gaps

- 4 つの FULL abort class の runnable scenario、raw log、verified log を揃えた。
- abort class、reason、post-abort state、cross-class exclusion を validator が assert する。
- fallback block、Resolver re-evaluation、source notification など class 固有の結果を確認した。

### 6.3 Remaining Gaps

- abort threshold と observation-mode-specific threshold の formal specification integration。
- LIGHT delayed abort の runnable / raw / verified coverage の追加検証。
- ramp engine 内部の `RECOVERED_PATH_UNSTABLE` / `RECOVERED_PATH_INVALID` abort trace の追加検証。これは Experimental のままである。

### 6.4 Gap Closure

4 つの abort handling scenario、`RAW-ABORT-*`、`LOG-ABORT-01`、abort class /
reason / post-abort state / cross-class exclusion の validator assertion、および Evidence
Matrix の RULE-23 Verified mapping により、4 FULL abort class scope の gap は閉じた。
この closure は ramp engine 内部 abort trace を含まない。

---

## 7. RULE-24_RETURN_RAMP_COMPLETE Gap Analysis

### 7.1 Available Evidence

| 種別 | Evidence |
|------|----------|
| Scenario | `mini_psc_rcu_decision_v03_recovery_ramp_observation.py`: `ramp_complete` (`scenario_steps=22`) |
| Raw log | `ramp_complete_run.txt` (`RAW-RAMP-FULL-ADV-01`) |
| Verified log | `rcu_decision_v03_ramp_complete_validation_log.md` (`LOG-RAMP-COMPLETE-01`) |
| Validator | `ScenarioCheck.name=ramp_complete` |
| Matrix mapping | FULL completion と post-completion state を Verified 行へ mapping |

### 7.2 Resolved Gaps

- STEP 17 の `recovered_weight=1.00`、`evacuation_weight=0.00`、`RAMP_TARGET_REACHED` を確認した。
- STEP 18-19 の recovery cooldown と STEP 20-21 の `mode=NORMAL` を確認した。
- RULE-24 と RULE-25 が各 1 回だけ出現し、abort、追加 advance、重複 completion がないことを validator が assert する。

### 7.3 Remaining Gaps

- completion threshold (`ramp_max_weight=1.00`) の formal specification integration。
- LIGHT observation 下の completion 境界の追加検証。

### 7.4 Gap Closure

`ramp_complete`、`RAW-RAMP-FULL-ADV-01`、`LOG-RAMP-COMPLETE-01`、completion /
post-completion / single-occurrence / forbidden-abort の validator assertion、および
Evidence Matrix の RULE-24 Verified mapping により、FULL completion scope の gap は閉じた。

---

## 8. Gap Closure Summary

| RULE | 閉じた scope | Closure chain |
|------|---------------|---------------|
| RULE-21 | FULL advance positive / negative | 2 scenarios -> 2 raw logs -> `LOG-RAMP-FULL-ADV-01` -> dedicated assertions -> Matrix mapping |
| RULE-22 | FULL / `INSUFFICIENT_OBSERVATION` hold | scenario -> `RAW-RAMP-HOLD-INSUFF-01` -> `LOG-RAMP-HOLD-INSUFF-01` -> dedicated assertions -> Matrix mapping |
| RULE-23 | 4 FULL abort classes | 4 scenarios -> 4 `RAW-ABORT-*` logs -> `LOG-ABORT-01` -> class-specific assertions -> Matrix mapping |
| RULE-24 | FULL completion / post-completion | scenario -> `RAW-RAMP-FULL-ADV-01` -> `LOG-RAMP-COMPLETE-01` -> dedicated assertions -> Matrix mapping |

---

## 9. Remaining Work

1. RULE-21 through RULE-24 と ramp state transition の formal specification integration。
2. `ramp_increment` と advance threshold の明文化。
3. abort threshold と observation-mode-specific threshold の明文化。
4. completion threshold の明文化。
5. LIGHT observation の hold / advance / complete 境界、false-positive / false-negative、telemetry gap、promotion gate の追加検証。
6. ramp engine 内部の `RECOVERED_PATH_UNSTABLE` / `RECOVERED_PATH_INVALID` abort trace の runnable evidence、raw log、verified log、validator assertion の追加。

これらは現在の限定 scope 付き Verified status を取り消す gap ではない。追加 scope の
昇格または formal specification integration に必要な残作業である。

---

## 10. 結論

Evidence Matrix を正本として、RULE-21 through RULE-24 はそれぞれ上記の限定 scope で
Verified へ昇格済みであり、昇格に必要だった evidence gap は閉じている。LIGHT
observation coverage、scope 外 evidence、および ramp engine 内部 abort trace は Hold
または Experimental のまま維持する。残る gap は formal specification integration と
追加 scope の検証に限定される。
