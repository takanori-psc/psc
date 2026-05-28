# PSC Fast Mode LIGHT Observation Boundary v0.1

## 1. Document Information

- Document Name : PSC Fast Mode LIGHT Observation Boundary
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Telemetry / Fast Mode
- Document Type : Design Draft
- Status : Draft
- Language : Japanese

- Related Models:
  - PSC Fast Mode Security Boundary Model v0.1
  - PSC Telemetry Model v0.2
  - PSC RCU Recovery Return Model v0.2
  - PSC Evidence Matrix v0.1

---

## 2. 目的

本ドラフトは、Fast Mode を PSC の主制御モデルへ統合する前に、LIGHT observation の安全境界を定義するための設計メモである。

LIGHT observation は、FULL observation の一般的な代替ではない。
telemetry cost や latency を下げる可能性がある一方で、RCU および Resolver が利用できる evidence を減らす制限付き観測モードである。

本ドキュメントの目的は、以下の危険な流れを防ぐことである。

```text
Fast Mode
-> observation 省略
-> recovery ramp advance
-> 不安定 path への誤復帰
```

このため、`RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` は、本ドラフトの安全条件を満たすまで Hold のままとする。

---

## 3. 範囲

本ドラフトは以下を扱う。

- LIGHT observation の未定義リスク
- FULL observation と LIGHT observation の差分
- LIGHT observation 下での recovery ramp advance の安全条件
- `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` の昇格条件

本ドラフトは以下を定義しない。

- Fast Mode routing model 全体
- Fast Mode packet format
- Fast Mode authorization flow
- production 用の最終 threshold

---

## 4. 設計原則

LIGHT observation は、PSC の stability-first control principle を弱めてはならない。

観測を減らす場合、PSC はより厳しい gating、遅い ramp advance、短い telemetry freshness window、または Resolver review によって補償しなければならない。

観測省略が許容されるのは、その path を advance してよい理由を説明できる場合に限る。

---

## 5. 未定義リスク

| Risk | 説明 | 影響 |
|------|------|------|
| False negative | 不安定性が存在するが観測されない | unsafe な ramp advance |
| Telemetry gap | 必要 metric が欠落または stale | decision confidence の低下 |
| Trust degradation latency | 最後の accepted sample 後に trust が低下 | abort または fallback が遅れる |
| Stability dip masking | sparse sampling により短時間の不安定化が隠れる | recovered path が安定に見える |
| Source bias | LIGHT mode が少数 telemetry source に依存する | evidence diversity の低下 |
| Resolver blind spot | Resolver へ渡る context が減る | arbitration quality の低下 |
| Fast Mode isolation effect | Fast Mode traffic が通常 routing telemetry から分離される | 観測 state と routing state がずれる |

---

## 6. FULL / LIGHT Observation 比較

| Item | FULL Observation | LIGHT Observation |
|------|------------------|-------------------|
| Primary goal | safety と evidence completeness | lower latency と lower telemetry cost |
| Telemetry density | 高い | 低い |
| Required metrics | trust, stability, health, freshness, confidence, path behavior | minimum safe subset のみ |
| Stability detection | 直接かつ反復的 | 部分的または遅延 |
| False negative tolerance | 低い | 明示的な上限が必要 |
| Recovery ramp advance | stable evidence 後に許可 | promotion conditions まで Hold |
| Abort behavior | instability 時に即時 abort | hard failure は常に即時 abort |
| Resolver involvement | evidence が明確なら任意 | confidence 低下時は必須 |
| Evidence Matrix status | FULL は正式統合候補 | LIGHT は Hold |

---

## 7. LIGHT Observation の最小入力

LIGHT observation が recovery ramp decision に参加するには、少なくとも以下の入力が必要である。

- path health
- trust score
- stability score または stability proxy
- telemetry freshness
- telemetry confidence
- hard failure indicator
- observation mode identifier

これらのいずれかが利用できない場合、LIGHT observation は `RETURN_RAMP_ADVANCE` を発火してはならない。

---

## 8. Safety Boundary Rules

### 8.1 evidence 欠落時は advance しない

trust、stability、confidence、freshness のいずれかが欠落する場合、PSC は現在の ramp weight を維持しなければならない。

期待される挙動:

```text
RULE-22_RETURN_RAMP_HOLD
```

### 8.2 hard failure は常に abort する

LIGHT observation は通常 telemetry を減らしてもよいが、hard failure indicator を無視してはならない。

期待される挙動:

```text
RULE-23_RETURN_RAMP_ABORT
```

### 8.3 confidence 低下時は gating を厳しくする

telemetry confidence が低下している場合、LIGHT observation は FULL observation より厳しい trust / stability 条件を要求しなければならない。

### 8.4 曖昧な場合は Resolver review または Hold

LIGHT observation が stable recovery と masked instability を区別できない場合、判断は escalation または hold されなければならない。

### 8.5 performance だけで昇格しない

throughput 向上や latency 低下だけでは、LIGHT observation 下の ramp advance 条件として不十分である。

---

## 9. RULE-21 LIGHT 昇格条件

`RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` は、以下の条件が定義された場合にのみ Hold から Formal integration candidate へ昇格できる。

| Condition | Requirement |
|-----------|-------------|
| Minimum telemetry set | LIGHT で必須となる入力が明示されている |
| Freshness bound | telemetry age の最大許容値が定義されている |
| Confidence floor | LIGHT advance に必要な最低 confidence が定義されている |
| False negative bound | stability 見逃し許容範囲が定義されている |
| Abort override | hard failure abort が常時有効である |
| Resolver fallback | 曖昧な LIGHT evidence は hold または escalation される |
| Ramp rate limit | LIGHT advance は FULL より速くならない |
| Validation log | 専用 LIGHT validation log が存在する |
| Evidence Matrix update | LIGHT behavior が scenario、STEP、log に対応付けられている |

これらを満たすまで、LIGHT advance は Hold のままとする。

---

## 10. 暫定判断

現時点の設計判断は以下である。

```text
RULE-21_RETURN_RAMP_ADVANCE (FULL)
  -> Formal integration candidate

RULE-21_RETURN_RAMP_ADVANCE (LIGHT)
  -> Hold
```

これにより、安全境界を維持したまま Fast Mode の探索を継続できる。

---

## 11. 次の作業

1. LIGHT telemetry の最小入力セットを定義する。
2. LIGHT observation 用の freshness / confidence threshold を定義する。
3. 専用の LIGHT recovery ramp validation scenario を追加する。
4. 検証後に Evidence Matrix を更新する。
5. LIGHT advance を RULE-21 variant とするか、独立 RULE 番号に分離するか判断する。
