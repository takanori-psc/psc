# PSC RULE Promotion Criteria v0.1

## Document Information

| 項目 | 内容 |
|------|------|
| Document ID | `PSC-RULE-PROMOTION-CRITERIA-v0.1-ja` |
| Title | PSC RULE-21 through RULE-24 Promotion Criteria |
| Version | v0.1 |
| Language | Japanese |
| Status | Draft |
| Scope | `RULE-21_RETURN_RAMP_ADVANCE` through `RULE-24_RETURN_RAMP_COMPLETE` |
| Related Document | `docs/specification/validation/psc_evidence_matrix_v0.1_ja.md` |

---

## 1. 目的

本書は、PSC の v0.3 recovery ramp 系 RULE である
`RULE-21_RETURN_RAMP_ADVANCE`、`RULE-22_RETURN_RAMP_HOLD`、
`RULE-23_RETURN_RAMP_ABORT`、`RULE-24_RETURN_RAMP_COMPLETE` を
Experimental から Verified へ昇格するための基準と、各 RULE の現在の
基準充足状態を定義する。

本書は昇格基準とその充足結果を記述する draft であり、RULE status の正本ではない。
RULE status の正本は Evidence Matrix とし、本書の記述は Evidence Matrix の
status を上書きしない。

---

## 2. 現在の状態

対象 RULE は、`psc_evidence_matrix_v0.1_ja.md` で追跡される。
`RULE-21_RETURN_RAMP_ADVANCE` は FULL observation evidence について Verified であり、
`RULE-22_RETURN_RAMP_HOLD` は FULL observation における
`reason=INSUFFICIENT_OBSERVATION` の covered hold evidence について Verified であり、
`RULE-23_RETURN_RAMP_ABORT` は `SOFT_ABORT` / `HARD_ABORT` / `EMERGENCY_CUT` /
`DEGRADED_ABORT` の FULL abort class evidence について Verified であり、
`RULE-24_RETURN_RAMP_COMPLETE` は FULL observation の completion および
post-completion state evidence について Verified である。

| RULE | 現在の状態 | 現在の位置づけ |
|------|------------|----------------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Verified（FULL のみ） | ramp 条件成立時に recovered path の traffic weight を段階的に増やす RULE。現在の Verified scope は FULL observation evidence に限定される。LIGHT observation ベースの advance は Hold のまま維持する |
| `RULE-22_RETURN_RAMP_HOLD` | Verified | ramp 中に進行条件が不足する場合、現 weight を維持する RULE。現在の Verified scope は FULL / `INSUFFICIENT_OBSERVATION` evidence に限定される |
| `RULE-23_RETURN_RAMP_ABORT` | Verified | ramp 中に recovered path の不安定化を検知した場合、復帰を中断する RULE。現在の Verified scope は `SOFT_ABORT` / `HARD_ABORT` / `EMERGENCY_CUT` / `DEGRADED_ABORT` の FULL abort class evidence に限定される |
| `RULE-24_RETURN_RAMP_COMPLETE` | Verified（FULL のみ） | recovered path への段階的 reintegration 完了を確定する RULE。現在の Verified scope は FULL observation の completion および post-completion state evidence に限定される |

LIGHT observation evidence および各 RULE の現在の Verified scope 外の evidence は、
明示された範囲で引き続き Hold または Experimental として扱う。

---

## 3. 共通昇格条件

各 RULE の Verified 昇格と現在の基準充足状態は、少なくとも以下の条件で判定する。

| 必須 evidence | 要件 |
|---------------|------|
| Scenario file | RULE を単独または明確な主対象として発火させる再現可能な scenario file が存在すること |
| Raw log | scenario file の実行結果として、RULE 名、入力状態、判断理由、最終 action を含む raw log が存在すること |
| Expected result | scenario の期待結果が category、reason、最終 action として明示されていること |
| Validator check | scenario 実行または集約 validator により、期待 category、RULE 名、主要 safety condition が assert されること |
| Evidence Matrix mapping | RULE、scenario、raw log、verified log、Evidence Step、Trace Summary の対応が Evidence Matrix で追跡可能な粒度で整理されていること |

Verified 昇格は、単にログが存在することではなく、再実行可能性と traceability が
確保されていることを条件とする。

---

## 4. RULE-21_RETURN_RAMP_ADVANCE 昇格基準

### 4.1 昇格対象の意味

`RULE-21_RETURN_RAMP_ADVANCE` は、recovered path が十分に安定し、
return ramp を進めても安全と判断できる場合に、recovered path 側の
traffic weight を段階的に増加させる RULE である。

### 4.2 必須 evidence

| 必須 evidence | 基準 |
|---------------|------|
| Scenario file | FULL observation に基づき、安定条件成立時のみ ramp advance が発生する scenario が存在すること |
| Raw log | `RULE-21_RETURN_RAMP_ADVANCE`、advance 前後の weight、安定条件、observation mode を記録すること |
| Expected result | expected category が ramp advance であり、weight が定義済み step 幅で増加すること |
| Validator check | advance 条件成立時のみ weight が増加し、hold / abort 条件では増加しないことを assert すること |
| Evidence Matrix mapping | `RULE-21_RETURN_RAMP_ADVANCE` と FULL observation scenario / raw log / verified log の対応が追跡可能であること |

### 4.3 LIGHT observation に関する保留条件

`RULE-21_RETURN_RAMP_ADVANCE` は、LIGHT observation に基づく advance については
Hold のまま維持する。

LIGHT observation による false-positive / false-negative behavior が十分に
境界付けられるまで、LIGHT observation は `RULE-21_RETURN_RAMP_ADVANCE` の
Verified evidence として扱わない。特に以下が未整理の場合、LIGHT advance は
昇格対象外とする。

- 実際には不安定な path を LIGHT observation が安定と誤判定する false-positive の上限
- 実際には安定な path を LIGHT observation が不安定または不十分と誤判定する false-negative の扱い
- LIGHT observation から FULL observation へ昇格する条件
- LIGHT observation の不足時に `RULE-22_RETURN_RAMP_HOLD` を選ぶ境界

### 4.4 昇格結果

`RULE-21_RETURN_RAMP_ADVANCE` は、FULL observation について、専用 scenario、
raw log、verified log、および advance sequence / negative check を assert
する validator check が揃ったため、FULL observation evidence について
Verified へ昇格した。

positive evidence として `ramp_complete` scenario が
`0.10 -> 0.30 -> 0.50 -> 0.70 -> 0.90` の 4 回の advance と、それに続く
`RULE-24_RETURN_RAMP_COMPLETE` を示す。negative evidence として
`ramp_abort_full_stability_dip` scenario が、advance 予定 step の直前で
instability が検知された場合に `RULE-21_RETURN_RAMP_ADVANCE` が一度も
emit されないことを示す。

LIGHT observation に基づく advance は、Section 4.3 の条件が満たされるまで
Hold のまま維持する。ramp_increment、advance threshold の仕様本文への
formal integration も別作業として残る。

---

## 5. RULE-22_RETURN_RAMP_HOLD 昇格基準

### 5.1 昇格対象の意味

`RULE-22_RETURN_RAMP_HOLD` は、return ramp 中に advance 条件が不足する場合、
現在の traffic weight を維持し、早期復帰や不必要な切替を防ぐ RULE である。

### 5.2 必須 evidence

| 必須 evidence | 基準 |
|---------------|------|
| Scenario file | FULL observation における観測不足により ramp hold が発生する scenario が存在すること |
| Raw log | `RULE-22_RETURN_RAMP_HOLD`、hold reason、observation condition、hold 前後の weight を記録すること |
| Expected result | expected category が hold であり、recovered path の weight が増加しないこと |
| Validator check | hold reason と weight unchanged を assert し、advance / abort との誤分類がないことを確認すること |
| Evidence Matrix mapping | FULL observation scenario、raw log、verified log、Evidence Step の対応が追跡可能であること |

### 5.3 昇格時の確認点

`RULE-22_RETURN_RAMP_HOLD` の現在の Verified scope は、FULL observation における
`INSUFFICIENT_OBSERVATION` reason のみを対象とする。LIGHT Observation reason は
evidence として利用可能だが、現在の Verified scope には含まれない。

RULE-22 coverage を将来拡張する場合は、以下の hold reason を明示的に区別した上で、
Verified scope へ含めるかを判断する。

| Hold reason | 必要な確認 |
|-------------|------------|
| `OBSERVATION_FALSE_NEGATIVE` | 実際の instability が LIGHT observation で十分に検出できない場合に hold すること |
| `STALE_TELEMETRY` | telemetry が古い場合に advance せず hold すること |
| `MASKED_INSTABILITY` | sparse evidence により instability が隠れる場合に hold すること |
| `INSUFFICIENT_OBSERVATION` | advance 判定に必要な観測情報が不足する場合に hold すること |

### 5.4 昇格結果

`RULE-22_RETURN_RAMP_HOLD` は、FULL observation における
`reason=INSUFFICIENT_OBSERVATION` について、scenario、raw log、verified log、
および hold reason / weight unchanged / advance・abort との非混同を確認する
validator check が揃ったため、この evidence scope について Verified へ昇格した。

LIGHT observation reason および Section 5.3 に示す現在の Verified scope 外の
hold reason は、追加検証が完了するまで Hold または Experimental のまま維持する。

---

## 6. RULE-23_RETURN_RAMP_ABORT 昇格基準

### 6.1 昇格対象の意味

`RULE-23_RETURN_RAMP_ABORT` は、return ramp 中に recovered path の不安定化、
安全境界違反、または fallback 不成立を検知した場合に、復帰試行を中断する RULE である。

### 6.2 必須 evidence

| 必須 evidence | 基準 |
|---------------|------|
| Scenario file | soft abort、hard abort、emergency cut、two-path degraded abort の各 abort class を再現する scenario が存在すること |
| Raw log | `RULE-23_RETURN_RAMP_ABORT`、abort class、abort reason、fallback 可否、stabilization action を記録すること |
| Expected result | expected category が abort class ごとに定義され、return ramp attempt が aborted になること |
| Validator check | abort class、fallback block reason、stabilization action、source notification の有無を assert すること |
| Evidence Matrix mapping | abort handling scenario、raw log、verified log、Evidence Step の対応が追跡可能であること |

### 6.3 昇格時の確認点

`RULE-23_RETURN_RAMP_ABORT` の Verified 昇格には、abort class ごとの結果が
混同されていないことが必要である。

| Abort class | Expected result |
|-------------|-----------------|
| `SOFT_ABORT` | allocation を維持し、observation 強化と Resolver re-evaluation へ進むこと |
| `HARD_ABORT` | suspect recovered path を ramp down し、source-side PSC に通知すること |
| `EMERGENCY_CUT` | unsafe path を除外し、capacity margin 不足時には fallback transfer を block すること |
| `DEGRADED_ABORT` | safe alternate が存在しない場合、Resolver が least-bad arbitration を行うこと |

### 6.4 昇格結果

`RULE-23_RETURN_RAMP_ABORT` は、`SOFT_ABORT`、`HARD_ABORT`、`EMERGENCY_CUT`、
`DEGRADED_ABORT` の 4 abort class について、専用 scenario、raw log、
verified log、および abort class / reason / post-abort state /
cross-class exclusion を assert する validator check が揃ったため、
これらの FULL abort class evidence について Verified へ昇格した。

v0.3 recovery ramp engine 内部で emit される
`reason=RECOVERED_PATH_UNSTABLE` / `reason=RECOVERED_PATH_INVALID` の
abort trace、および LIGHT delayed abort の design stub
(`light_delayed_abort_stub.py`) は、この Verified scope に含まれない。
abort threshold の仕様本文への formal integration も別作業として残る。

---

## 7. RULE-24_RETURN_RAMP_COMPLETE 昇格基準

### 7.1 昇格対象の意味

`RULE-24_RETURN_RAMP_COMPLETE` は、recovered path への progressive reintegration が
完了条件を満たした場合に、return ramp の完了を確定する RULE である。

### 7.2 必須 evidence

| 必須 evidence | 基準 |
|---------------|------|
| Scenario file | ramp start、advance、hold 判定通過、complete までを再現する scenario が存在すること |
| Raw log | `RULE-24_RETURN_RAMP_COMPLETE`、最終 weight、completion condition、NORMAL 復帰状態を記録すること |
| Expected result | expected category が ramp complete であり、recovered path の reintegration が完了していること |
| Validator check | `recovered_weight=1.00`、`evacuation_weight=0.00`、`reason=RAMP_TARGET_REACHED`、所定 step での completion、RULE-24 の単一発火、completion 後の追加 advance / duplicate completion / abort 不発火、recovery cooldown、NORMAL への遷移を assert すること |
| Evidence Matrix mapping | complete scenario、raw log、verified log、Evidence Step の対応が追跡可能であること |

### 7.3 昇格時の確認点

evidence-based Verified status では、単に最大 weight 値が出現したことだけで
`RULE-24_RETURN_RAMP_COMPLETE` を Verified にしない。executable scenario と log で
completion target への到達を明示し、以下の結果を assert する必要がある。

- 所定の completion step で `recovered_weight=1.00`、`evacuation_weight=0.00`、
  `reason=RAMP_TARGET_REACHED` が emit されること
- `RULE-24_RETURN_RAMP_COMPLETE` が 1 回だけ発火すること
- completion 後に追加 advance、duplicate completion、abort が発生しないこと
- recovery cooldown を経て NORMAL state へ遷移すること

`ramp_max_weight=1.00` を formal specification 上の completion threshold として
定義する作業は別の Remaining Work であり、現在の evidence-based な限定 Verified
scope の条件には含めない。

### 7.4 昇格結果

`RULE-24_RETURN_RAMP_COMPLETE` は、FULL observation の completion および
post-completion evidence の限定 scope について Verified である。専用 scenario
（`ramp_complete`、`scenario_steps=22`）、raw log、verified log、および
completion state / post-completion state / no additional advance を assert
する validator check が揃っている。

executable scenario と log は STEP 17 で `recovered_weight=1.00`、
`evacuation_weight=0.00`、`reason=RAMP_TARGET_REACHED` を伴う completion を示し、
validator はその step で emit された値を assert する。validator は設定値自体や
formal specification 上の定義を assert しない。`ramp_max_weight=1.00` を正式な
completion threshold として定義する作業は、evidence-based Verified status とは
別作業として残る。

completion 直前まで abort condition が成立していないことは、
`RULE-23_RETURN_RAMP_ABORT` が出力全体に出現しないことを validator が
assert することで確認する。completion 後の state が安定していることは、
STEP 18-19 の `RULE-11_RECOVERY_cooldown` と STEP 20-21 の
`RULE-01_KEEP_score`（`mode=NORMAL`）で確認する。validator はさらに、RULE-24 が
1 回だけ発火し、STEP 17 後に追加 advance、duplicate completion、ramp restart が
発生しないことを確認する。

LIGHT observation 下の completion behavior は、この Verified scope に
含まれない。

---

## 8. 基準充足確認の順序

RULE-21 から RULE-24 は相互に依存するため、昇格時の基準充足は以下の順序で
確認した。

1. `RULE-22_RETURN_RAMP_HOLD` の観測不足時の安全側動作を確認する。
2. `RULE-23_RETURN_RAMP_ABORT` の異常時中断動作を確認する。
3. `RULE-21_RETURN_RAMP_ADVANCE` の FULL observation advance 条件を確認する。
4. `RULE-24_RETURN_RAMP_COMPLETE` の完了条件を確認する。

この順序により、advance / complete の基準充足を確認する前に、hold / abort による
安全側の停止条件が定義されていることを確認した。

---

## 9. 非目標

本書の対象外は以下である。

- Evidence Matrix を正本とする RULE status を、本書単独で決定または上書きすること
- RULE-25 の昇格基準を定義すること
- LIGHT observation に基づく `RULE-21_RETURN_RAMP_ADVANCE` を Verified とみなすこと

---

## 10. 次ステップ

現在残る作業は以下である。これらは evidence-based Verified status とは別の
formal specification integration または追加検証として扱う。

1. RULE-21 through RULE-24 を formal specification へ統合する。
2. ramp_increment / advance threshold を正式仕様化する。
3. abort threshold を正式仕様化する。
4. completion threshold を正式仕様化する。
5. LIGHT observation 境界を追加検証する。
6. ramp engine 内部の `RECOVERED_PATH_UNSTABLE` /
   `RECOVERED_PATH_INVALID` abort trace を追加検証する。
