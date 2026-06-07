# PSC 初期転送状態からの分岐一覧

この文書は新しい仕様ではない。現在の Evidence Matrix と review diagrams から派生した
review / navigation aid である。`NORMAL_TRANSFER` / initial forwarding state から到達可能な
分岐を、現在状態 -> 条件 -> 選択される RULE -> 次状態として確認しやすくする。

この文書が答える問いは、「PSC が現在ここにいる。次に何が起こり得るか？」である。
初期転送、DEGRADED、RECOVERY、RETURN、RETURN_RAMP、LIGHT_POLICY、LEGACY の順に、
PSC の現在位置から次の分岐を素早く確認するために使う。

## 読み方

- 現在状態から読む。
- 条件に合う行を探す。
- 選択される RULE をたどって次状態へ進む。
- Legacy Concept の行は active runtime path として扱わない。

## PSCを見るときのおすすめ順

1. 全体像
2. Quick Reference
3. 詳細分岐
4. Legacy / Historical Notes

## 全体像

```text
NORMAL_TRANSFER
│
├─ RULE-01_KEEP_score
├─ RULE-02_SWITCH_score
├─ RULE-03_SWITCH_trust
├─ RULE-04_BLOCK_trust
├─ RULE-05_ESCALATE_conflict ───────────────▶ RESOLVER_REVIEW
└─ RULE-07_DEGRADE_trigger
        │
        ▼
     DEGRADED
        │
        ├─ RULE-08_DEGRADE_keep
        ├─ RULE-09_DEGRADE_switch
        └─ RULE-10_RECOVERY_trigger
                │
                ▼
          RECOVERY
                │
        RULE-15_RECOVERY_CANDIDATE
                │
        RULE-16_RECOVERY_VALIDATION_START
                │
        RULE-18_RETURN_ELIGIBLE
                │
        ┌───────┴───────────────────────────┐
        │                                   │
      v0.2                                v0.3
        │                                   │
 RULE-19_RETURN_SWITCH             RULE-25_RETURN_RAMP_START
        │                                   │
        ▼                                   ▼
 NORMAL_TRANSFER                    RETURN_RAMP
                                            │
                      ┌─────────────────────┼─────────────────────┐
                      │                     │                     │
        RULE-22_RETURN_RAMP_HOLD  RULE-21_RETURN_RAMP_ADVANCE  RULE-23_RETURN_RAMP_ABORT
                      │                     │                     │
                      └──────────▶ RETURN_RAMP ◀──────────────────┘
                                            │
                              RULE-24_RETURN_RAMP_COMPLETE
                                            │
                                            ▼
                                     NORMAL_TRANSFER

LIGHT_POLICY:
  LIGHT observation は、FULL promotion または explicit LIGHT promotion gates まで
  RULE-22_RETURN_RAMP_HOLD を基本経路とする。
```

## PSC Control Flow Quick Reference

| 領域 | 主な分岐 | 選択される RULE | 次状態 / 結果 | status |
|------|----------|-----------------|---------------|--------|
| 初期転送 / NORMAL | 現在経路を維持 | RULE-01_KEEP_score | NORMAL_TRANSFER | Verified |
| 初期転送 / NORMAL | ローカルスコアによる切替 | RULE-02_SWITCH_score | NORMAL_TRANSFER | Verified |
| 初期転送 / NORMAL | trust による switch 候補経路 | RULE-03_SWITCH_trust | NORMAL_TRANSFER | Active。Verified final-action coverage は未整備 |
| 初期転送 / NORMAL | unsafe / trust-blocked switch を block | RULE-04_BLOCK_trust | BLOCK_SWITCH | Verified safety block |
| 初期転送 / NORMAL | ambiguity / conflict を Resolver に委譲 | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Verified |
| 初期転送 / NORMAL | 利用可能な信頼済み経路がない | RULE-07_DEGRADE_trigger | DEGRADED | Verified |
| DEGRADED | fallback を維持 / 切替 | RULE-08_DEGRADE_keep / RULE-09_DEGRADE_switch | DEGRADED | Verified |
| DEGRADED | 安定した信頼済み回復経路を検出 | RULE-10_RECOVERY_trigger | RECOVERY_CANDIDATE | Verified |
| Recovery validation | 候補経路を登録し検証を開始 | RULE-15_RECOVERY_CANDIDATE / RULE-16_RECOVERY_VALIDATION_START | VALIDATING | Verified |
| Recovery validation | 検証通過後に return eligible | RULE-18_RETURN_ELIGIBLE | RETURN_ELIGIBLE | Verified。`RULE-17` は emit しない |
| Return execution | v0.2 direct return | RULE-19_RETURN_SWITCH | NORMAL_TRANSFER / RECOVERY_COOLDOWN | Verified v0.2 |
| Return execution | return margin 不足 | RULE-20_RETURN_KEEP | NORMAL_TRANSFER | Verified |
| Return execution | v0.3 progressive ramp 開始 | RULE-25_RETURN_RAMP_START | RETURN_RAMP | Experimental。`RULE-19` と同義ではない |
| Return ramp | hold / advance / abort / complete | RULE-22 / RULE-21 / RULE-23 / RULE-24 | RETURN_RAMP / ABORT_STABILIZATION / NORMAL_TRANSFER | Experimental。`RULE-21` owner は `RULE-21_RETURN_RAMP_ADVANCE` |
| LIGHT policy | FULL promotion または explicit gates まで Hold | RULE-22_RETURN_RAMP_HOLD | RETURN_RAMP | current authoritative policy |
| LIGHT policy | hard failure / unsafe recovered path | RULE-23_RETURN_RAMP_ABORT | ABORT_STABILIZATION | safety-first |
| LIGHT policy | ambiguous evidence | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Verified escalation |
| Legacy / reserved | validation pass marker / return escalation / future slot | RULE-17 / RULE-21_RETURN_ESCALATE / RULE-06 | active runtime path なし | Legacy Concept / future reserved |

Quick Reference 上の `RULE-22 / RULE-21 / RULE-23 / RULE-24` は、それぞれ
`RULE-22_RETURN_RAMP_HOLD`、`RULE-21_RETURN_RAMP_ADVANCE`、
`RULE-23_RETURN_RAMP_ABORT`、`RULE-24_RETURN_RAMP_COMPLETE` を指す。
historical v0.3 LIGHT advance logs は現在の LIGHT policy ではない。

---

## NORMAL

## 初期転送 / NORMAL 分岐

| 現在状態 | 条件 | 選択される RULE | 次状態 | 備考 / status |
|----------|------|-----------------|--------|---------------|
| NORMAL_TRANSFER / initial forwarding state | 現在経路を維持する。score improvement が hysteresis / switch threshold に届かない | RULE-01_KEEP_score | NORMAL_TRANSFER | Verified keep rule |
| NORMAL_TRANSFER / initial forwarding state | ローカルスコアが明確に優位で、trust block や escalation が不要 | RULE-02_SWITCH_score | NORMAL_TRANSFER | Verified local switch rule |
| NORMAL_TRANSFER / initial forwarding state | trust により switch 候補経路が選好される | RULE-03_SWITCH_trust | NORMAL_TRANSFER | collision matrix 上では active。ただし final-action 専用 coverage がないため Verified 昇格は保留 |
| NORMAL_TRANSFER / initial forwarding state | score / trust switch 候補経路が unsafe または trust-blocked path を指す | RULE-04_BLOCK_trust | NORMAL_TRANSFER / BLOCK_SWITCH | Verified safety block。`RULE-02_SWITCH_score` と `RULE-03_SWITCH_trust` より優先され、`BLOCK_SWITCH` を生成する |
| NORMAL_TRANSFER / initial forwarding state | trust / stability / score の conflict または ambiguity があり local action で決めない | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Verified escalation rule |
| NORMAL_TRANSFER / initial forwarding state | 選択済み / 現在経路が invalid、または利用可能な信頼済み経路がない | RULE-07_DEGRADE_trigger | DEGRADED | Verified degrade entry rule |

---

## DEGRADED

## DEGRADED 分岐

| 現在状態 | 条件 | 選択される RULE | 次状態 | 備考 / status |
|----------|------|-----------------|--------|---------------|
| DEGRADED | maintainable fallback を維持できる | RULE-08_DEGRADE_keep | DEGRADED | Verified degraded keep rule |
| DEGRADED | degraded fallback の切替が必要 | RULE-09_DEGRADE_switch | DEGRADED | Verified degraded switch rule |
| DEGRADED | 安定した信頼済み回復経路が存在する | RULE-10_RECOVERY_trigger | RECOVERY_CANDIDATE / NORMAL recovery path | Verified recovery trigger |

---

## RECOVERY

## Recovery Validation 分岐

| 現在状態 | 条件 | 選択される RULE | 次状態 | 備考 / status |
|----------|------|-----------------|--------|---------------|
| DEGRADED / recovery path | 回復経路が trust / stability candidate threshold を満たす | RULE-15_RECOVERY_CANDIDATE | RECOVERY_CANDIDATE | Verified recovery candidate rule |
| RECOVERY_CANDIDATE | 候補経路の検証期間を開始または継続する | RULE-16_RECOVERY_VALIDATION_START | VALIDATING | Verified validation start rule |
| VALIDATING | 検証期間が完了し、return eligibility を満たす | RULE-18_RETURN_ELIGIBLE | RETURN_ELIGIBLE | Verified。現在の code は `RULE-16` から `RULE-18` へ直接進み、`reason="VALIDATION_PASSED"` を使う |
| VALIDATING | validation pass を独立 stage として表す旧概念 | RULE-17_RECOVERY_VALIDATION_PASS | VALIDATION_PASS_LEGACY | Legacy Concept only。active runtime path ではない |

---

## RETURN

## Return Execution 分岐

| 現在状態 | 条件 | 選択される RULE | 次状態 | 備考 / status |
|----------|------|-----------------|--------|---------------|
| RETURN_ELIGIBLE | v0.2 direct return を実行する | RULE-19_RETURN_SWITCH | NORMAL_TRANSFER / RECOVERY_COOLDOWN | Verified v0.2 direct return rule |
| RETURN_ELIGIBLE | return margin が不足し現在経路を維持する | RULE-20_RETURN_KEEP | NORMAL_TRANSFER | Verified return keep rule |
| RETURN_ELIGIBLE | v0.3 progressive ramp に入る | RULE-25_RETURN_RAMP_START | RETURN_RAMP | Experimental v0.3 ramp entry。`RULE-19_RETURN_SWITCH` と意味的に同一ではない |

---

## RETURN_RAMP

## Return Ramp 分岐

| 現在状態 | 条件 | 選択される RULE | 次状態 | 備考 / status |
|----------|------|-----------------|--------|---------------|
| RETURN_RAMP | 追加観測が必要、または advance 条件が成立しない | RULE-22_RETURN_RAMP_HOLD | RETURN_RAMP | Experimental hold rule。LIGHT policy の current authoritative behavior でもある |
| RETURN_RAMP | FULL observation または promoted evidence が stable で advance 条件を満たす | RULE-21_RETURN_RAMP_ADVANCE | RETURN_RAMP | operational `RULE-21` owner。FULL または promoted evidence only |
| RETURN_RAMP | 回復経路が unstable / invalid、hard failure、または abort class に該当 | RULE-23_RETURN_RAMP_ABORT | ABORT_STABILIZATION | Experimental abort rule |
| RETURN_RAMP | progressive ramp が target weight に到達する | RULE-24_RETURN_RAMP_COMPLETE | NORMAL_TRANSFER / RECOVERY_COOLDOWN | Experimental ramp complete rule |

---

## LIGHT_POLICY

## LIGHT Policy 分岐

| 現在状態 | 条件 | 選択される RULE | 次状態 | 備考 / status |
|----------|------|-----------------|--------|---------------|
| LIGHT_BOUNDARY | LIGHT observation が missing / stale / low confidence、または explicit promotion gate がない | RULE-22_RETURN_RAMP_HOLD | RETURN_RAMP | 現在の authoritative LIGHT policy |
| LIGHT_BOUNDARY | hard failure または unsafe 回復経路を検出 | RULE-23_RETURN_RAMP_ABORT | ABORT_STABILIZATION | safety-first abort |
| LIGHT_BOUNDARY | evidence が ambiguous で local decision に十分でない | RULE-05_ESCALATE_conflict | RESOLVER_REVIEW | Resolver review に委譲 |
| LIGHT_BOUNDARY | FULL に昇格、または explicit LIGHT promotion gates が定義され満たされる | versioned normal ramp path | FULL observation / RETURN_RAMP | FULL observation / normal ramp path に合流する |
| LIGHT_BOUNDARY | historical v0.3 log で LIGHT advance が観測される | RULE-21_RETURN_RAMP_ADVANCE | 非 current policy | `ramp_light_tolerates_moderate_dip` などは historical experimental behavior。現在の LIGHT policy として扱わない |

---

## LEGACY

## Legacy / Historical Notes

| 現在状態 | 条件 | 選択される RULE | 次状態 | 備考 / status |
|----------|------|-----------------|--------|---------------|
| VALIDATING | validation pass を独立 stage として記録する旧表現 | RULE-17_RECOVERY_VALIDATION_PASS | VALIDATION_PASS_LEGACY | Legacy Concept。現在の code は `RULE-16` -> `RULE-18` に直接遷移する |
| RETURN / escalation history | v0.2 recovery return escalation label | RULE-21_RETURN_ESCALATE | RESOLVER_REVIEW / legacy only | Legacy Concept。operational `RULE-21` owner ではない |
| reserved namespace | 将来用途の予約番号 | RULE-06 | なし | future reserved。現在の active Evidence Matrix owner はない |

## 注意事項

- collision matrix は partial arbitration only であり、complete PSC-wide rule arbitration ではない。
- `RULE-03_SWITCH_trust` は Verified 昇格前に dedicated final-action validation scenario が必要である。
- `RULE-25_RETURN_RAMP_START` は formal v0.3 integration まで Experimental のままである。
