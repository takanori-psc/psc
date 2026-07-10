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
Experimental から Verified へ昇格するために必要な evidence を定義する。

本書は昇格基準を定義する draft であり、現時点で既存 RULE の状態を変更しない。
Evidence Matrix の編集も本ステップでは行わない。

---

## 2. 現在の状態

対象 RULE は、`psc_evidence_matrix_v0.1_ja.md` で追跡される。
`RULE-22_RETURN_RAMP_HOLD` は FULL observation における
`reason=INSUFFICIENT_OBSERVATION` の covered hold evidence について Verified であり、
その他の対象 RULE は引き続き Experimental である。

| RULE | 現在の状態 | 現在の位置づけ |
|------|------------|----------------|
| `RULE-21_RETURN_RAMP_ADVANCE` | Experimental | ramp 条件成立時に recovered path の traffic weight を段階的に増やす候補 RULE |
| `RULE-22_RETURN_RAMP_HOLD` | Verified | ramp 中に進行条件が不足する場合、現 weight を維持する RULE。現在の Verified scope は FULL / `INSUFFICIENT_OBSERVATION` evidence に限定される |
| `RULE-23_RETURN_RAMP_ABORT` | Experimental | ramp 中に recovered path の不安定化を検知した場合、復帰を中断する候補 RULE |
| `RULE-24_RETURN_RAMP_COMPLETE` | Experimental | recovered path への段階的 reintegration 完了を確定する候補 RULE |

残る Experimental RULE は、実験シナリオおよび raw / verified log により挙動の一部が
確認されている。ただし、Verified へ昇格するには、シナリオ、ログ、期待結果、
validator check、Evidence Matrix mapping が一貫して揃っている必要がある。

---

## 3. 共通昇格条件

各 RULE を Verified へ昇格するには、少なくとも以下を満たす必要がある。

| 必須 evidence | 要件 |
|---------------|------|
| Scenario file | RULE を単独または明確な主対象として発火させる再現可能な scenario file が存在すること |
| Raw log | scenario file の実行結果として、RULE 名、入力状態、判断理由、最終 action を含む raw log が存在すること |
| Expected result | scenario の期待結果が category、reason、最終 action として明示されていること |
| Validator check | scenario 実行または集約 validator により、期待 category、RULE 名、主要 safety condition が assert されること |
| Evidence Matrix mapping | RULE、scenario、raw log、verified log、Evidence Step、Trace Summary の対応が Evidence Matrix へ追加可能な粒度で整理されていること |

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
| Evidence Matrix mapping | `RULE-21_RETURN_RAMP_ADVANCE` と FULL observation scenario / raw log / verified log の対応を追加できること |

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
| Evidence Matrix mapping | FULL observation scenario、raw log、verified log、Evidence Step の対応を追加できること |

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
| Evidence Matrix mapping | abort handling scenario、raw log、verified log、Evidence Step の対応を追加できること |

### 6.3 昇格時の確認点

`RULE-23_RETURN_RAMP_ABORT` の Verified 昇格には、abort class ごとの結果が
混同されていないことが必要である。

| Abort class | Expected result |
|-------------|-----------------|
| `SOFT_ABORT` | allocation を維持し、observation 強化と Resolver re-evaluation へ進むこと |
| `HARD_ABORT` | suspect recovered path を ramp down し、source-side PSC に通知すること |
| `EMERGENCY_CUT` | unsafe path を除外し、capacity margin 不足時には fallback transfer を block すること |
| `DEGRADED_ABORT` | safe alternate が存在しない場合、Resolver が least-bad arbitration を行うこと |

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
| Validator check | completion threshold、最終 allocation、post-completion state、追加 advance 不要を assert すること |
| Evidence Matrix mapping | complete scenario、raw log、verified log、Evidence Step の対応を追加できること |

### 7.3 昇格時の確認点

`RULE-24_RETURN_RAMP_COMPLETE` は、単に weight が最大値に到達したことだけでは
Verified にしない。以下の条件が揃う必要がある。

- completion threshold が仕様上定義されていること
- completion 直前まで abort condition が成立していないこと
- completion 後の state が安定していること
- completion 後に不要な additional advance が発生しないこと

---

## 8. 昇格判定の順序

RULE-21 から RULE-24 は相互に依存するため、昇格判定は以下の順序で行う。

1. `RULE-22_RETURN_RAMP_HOLD` の観測不足時の安全側動作を確認する。
2. `RULE-23_RETURN_RAMP_ABORT` の異常時中断動作を確認する。
3. `RULE-21_RETURN_RAMP_ADVANCE` の FULL observation advance 条件を確認する。
4. `RULE-24_RETURN_RAMP_COMPLETE` の完了条件を確認する。

この順序により、advance / complete を検証する前に、hold / abort による安全側の
停止条件が定義されていることを確認する。

---

## 9. 非目標

本書では以下を行わない。

- 既存 RULE の status を Experimental から Verified へ変更すること
- `psc_evidence_matrix_v0.1_ja.md` を編集すること
- RULE-25 の昇格基準を定義すること
- LIGHT observation に基づく `RULE-21_RETURN_RAMP_ADVANCE` を Verified とみなすこと

---

## 10. 次ステップ

本 draft の次ステップは以下である。

1. 各 RULE に対応する scenario file と raw log の不足分を確認する。
2. validator check の assert 項目を scenario ごとに明文化する。
3. Evidence Matrix に追加する mapping 案を別ステップで作成する。
4. LIGHT observation の false-positive / false-negative 境界を定義する。
5. 条件が揃った RULE から Verified 昇格候補としてレビューする。
