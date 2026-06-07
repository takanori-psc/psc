# PSC Recovery Return Abort Handling v0.1

## 1. Document Information

- Document Name : PSC Recovery Return Abort Handling
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / RCU / Resolver / Recovery Return
- Document Type : Design Draft
- Status : Draft
- Language : Japanese

- Related Models:
  - PSC RCU Recovery Return Model v0.2
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC Resolver Model v0.2
  - PSC Evidence Matrix v0.1

---

## 2. 目的

本ドラフトは、Return Ramp 中に `RULE-23_RETURN_RAMP_ABORT` が発火した後に
PSC が何を行うべきかを定義する。

`RULE-23_RETURN_RAMP_ABORT` は、常に即時 path cut を意味するわけではない。
これは現在の recovery return attempt が中断されたことを意味する。

Abort 後、PSC は hard failure または emergency safety condition でない限り、
攻撃的な path 変更の前に Traffic Stabilization Phase に入るべきである。

---

## 3. 範囲

本ドラフトは以下を扱う。

- `RULE-23_RETURN_RAMP_ABORT` 後の制御挙動
- Traffic Stabilization Phase の挙動
- SOFT_ABORT、HARD_ABORT、EMERGENCY_CUT の分類
- 二経路 degraded case
- source-side PSC への escalation
- `RULE-22_RETURN_RAMP_HOLD` と `RULE-23_RETURN_RAMP_ABORT` の違い
- 新しい Return Ramp attempt を開始する前に必要な条件

本ドラフトは以下を定義しない。

- production threshold
- 最終的な traffic shaping algorithm
- packet format 変更
- simulation 実装
- Evidence Matrix 上の昇格状態

---

## 4. 設計原則

### 4.1 Abort は attempt の中断を意味する

`RULE-23_RETURN_RAMP_ABORT` は、現在の recovery return attempt を終了させる。

これは必ずしも即時 path cut を意味しない。
正しい応答は、abort class、観測された risk、利用可能な代替 path、
policy、traffic class に依存する。

### 4.2 攻撃的変更の前に安定化する

Abort 後、PSC は条件が明確に unsafe でない限り、
攻撃的な path 変更を行う前に現在の traffic allocation を安定化すべきである。

### 4.3 Advance へ直接戻らない

`RULE-23_RETURN_RAMP_ABORT` 後、PSC は
`RULE-21_RETURN_RAMP_ADVANCE` を直接再開してはならない。

PSC は Resolver re-evaluation を通過し、適切な場合のみ、
versioned Return Ramp start rule から再開しなければならない。
`RULE-19_RETURN_SWITCH` は Verified 済みの v0.2 direct return rule として
維持され、Return Ramp start の運用上の所有権を意味しない。
現在の v0.3 experimental ramp-start implementation は
`RULE-25_RETURN_RAMP_START` を使用する。

---

## 5. Traffic Stabilization Phase

Traffic Stabilization Phase は、abort 自体が oscillation や unsafe redistribution を
引き起こすことを防ぐための post-abort control phase である。

この phase で PSC は以下を行うべきである。

- それ以上の Return Ramp Advance を停止する
- 安全な場合、一時的に現在の traffic weight を維持する
- policy が許可する場合、source-side PSC に flow reduction を要求する
- observation density を上げる、または LIGHT observation を FULL observation へ昇格する
- Resolver re-evaluation を発火する

この phase は、Resolver が以下のいずれかを判断した場合にのみ終了する。

- 現在の allocation を安全に維持できる
- suspect recovered path を ramp down する必要がある
- traffic を known stable allocation へ移すべきである
- emergency transition が必要である
- 後で新しい Return Ramp attempt を開始できる

---

## 6. Abort Behavior Classes

### 6.1 SOFT_ABORT

SOFT_ABORT は、evidence が suspicious だが conclusively unsafe ではない場合に適用する。

例:

- suspicious telemetry
- trust drop
- stale evidence
- conflicting evidence
- backup path degradation
- LIGHT observation confidence の低下

期待される挙動:

- 現在の recovery return attempt を abort する
- それ以上の ramp advance を停止する
- 安全な場合、一時的に現在の traffic weight を維持する
- policy が許可する場合、source traffic を低減する
- observation density を上げる、または LIGHT を FULL observation へ昇格する
- Resolver re-evaluation を要求する

SOFT_ABORT では、現在の allocation を急激に再配分するより維持する方が安全な場合、
recovered path を自動的に cut すべきではない。

### 6.2 HARD_ABORT

HARD_ABORT は、明確な instability が観測された場合に適用する。

例:

- 明確な path instability
- hard failure signal
- severe loss
- link quality collapse
- FULL observation 下での反復 validation failure

期待される挙動:

- 現在の recovery return attempt を abort する
- それ以上の ramp advance を停止する
- suspect recovered path を ramp down する、または traffic を known stable allocation へ移す
- Resolver re-evaluation を発火する
- traffic reduction または priority preservation が必要な場合、source-side PSC に通知する

HARD_ABORT は迅速な traffic movement を必要とする場合があるが、
forwarding がまだ安全な場合は controlled transition を優先すべきである。

### 6.3 EMERGENCY_CUT

EMERGENCY_CUT は、forwarding 継続が unsafe な場合に適用する。

例:

- link down
- optical failure
- severe corruption
- unsafe forwarding
- contain できない integrity failure

期待される挙動:

- unsafe path を即時 cut または exclude する
- emergency transition handling に入る
- Resolver および source-side PSC に通知する
- policy が許可し viable path が存在する場合、高優先度 traffic を維持する
- 必要に応じて低優先度 traffic を defer または shed する

EMERGENCY_CUT は、本ドラフトで immediate cut を default behavior とする唯一の class である。

---

## 7. 二経路 degraded case

candidate path が二つしかなく、両方が degraded である場合、
PSC は fully safe path が存在すると仮定してはならない。

Resolver は以下に基づき least-bad allocation を選択しなければならない。

- trust
- stability
- path health
- telemetry freshness and confidence
- policy
- traffic class
- failure containment risk

取り得る結果には以下が含まれる。

- switching が risk を増やすため current path を維持する
- recovered path の traffic を減らすが limited allocation は維持する
- より degraded 度の低い path へ traffic を移す
- source-side traffic reduction を要求する
- high-priority traffic を維持し low-priority traffic を defer する
- どちらの path も forwarding に安全でない場合、emergency transition に入る

二経路 degraded case は通常の return optimization ではなく、
controlled risk management problem である。

---

## 8. Source-Side Escalation

PSC は source side と destination side の両方に存在し得る。
そのため abort handling は、local path action だけでは不十分な場合、
source-side PSC に通知してよい。

Source-side escalation は以下を要求し得る。

- traffic rate reduction
- low-priority traffic の defer
- high-priority traffic の preserve
- burst traffic の一時 shaping
- recovery-sensitive transfer の delayed retry

すべての source-side action は policy controlled でなければならない。

destination-side または fabric-side PSC は、
policy authorization なしに traffic を一方的に drop、defer、
reprioritize できると仮定してはならない。

---

## 9. RULE-22_RETURN_RAMP_HOLD との差分

| Item | RULE-22_RETURN_RAMP_HOLD | RULE-23_RETURN_RAMP_ABORT |
|------|--------------------------|---------------------------|
| Meaning | recovery attempt は active のまま | 現在の recovery attempt は abort される |
| Ramp state | 現在の ramp weight を維持 | ramp advance を停止し active return から離脱 |
| Next action | 観測を継続し、後で advance 可能 | stabilization と Resolver re-evaluation へ進む |
| Direct RULE-21 resume | hold 条件が解消すれば可能 | 不可 |
| Restart requirement | restart 不要 | versioned ramp-start rule から新しい ramp を開始する必要がある |

`RULE-22_RETURN_RAMP_HOLD` は active recovery attempt 内の pause である。
`RULE-23_RETURN_RAMP_ABORT` はその attempt を終了する。

---

## 10. Post-Abort State Flow

期待される post-abort flow は以下である。

```text
RULE-23_RETURN_RAMP_ABORT
-> Traffic Stabilization Phase
-> Resolver re-evaluation
-> one of:
   - hold stabilized allocation
   - ramp down suspect recovered path
   - move to known stable allocation
   - request source-side flow reduction
   - emergency cut / emergency transition
   - restart a new Return Ramp through the versioned Return Ramp start rule
     (currently RULE-25_RETURN_RAMP_START in the v0.3 experimental implementation)
```

PSC は `RULE-23_RETURN_RAMP_ABORT` から
`RULE-21_RETURN_RAMP_ADVANCE` へ直接遷移してはならない。

---

## 11. Draft Validation Direction

本ドキュメントは draft extension のみである。

今後の検証作業は以下の順序で進める。

1. scenario stub
2. simulation
3. validator extension
4. Evidence Matrix update

候補 scenario:

- stale または conflicting telemetry による soft abort
- clear instability による hard abort
- link down または optical failure による emergency cut
- 二経路 degraded Resolver arbitration
- abort 後の source-side traffic reduction request
