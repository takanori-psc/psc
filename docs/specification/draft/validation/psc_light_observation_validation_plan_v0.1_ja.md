# PSC LIGHT Observation Validation Plan v0.1

## 1. Document Information

- Document Name : PSC LIGHT Observation Validation Plan
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Telemetry / Fast Mode / Validation
- Document Type : Validation Draft
- Status : Draft
- Language : Japanese

- Related Models:
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC Evidence Matrix v0.1
  - PSC RCU Recovery Return Model v0.2
  - PSC Resolver Specification v0.1

---

## 2. 目的

本ドラフトは、`RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` を Hold から昇格検討する前に必要となる最小検証計画を定義する。

ここでは、まだ LIGHT validation の本実装は行わない。
LIGHT observation が staged recovery ramp advance に使えるほど安全かを判断するために、何を観測し、何を simulation 化し、何を check すべきかを整理する。

現在の位置づけ:

```text
RULE-21_RETURN_RAMP_ADVANCE (LIGHT)
  -> Hold
```

この Hold は、LIGHT 固有の failure mode が validation scenario として表現され、期待される制御挙動へ対応付けられるまで外さない。

---

## 3. 検証原則

LIGHT observation は telemetry density を減らしてもよいが、recovery ramp が advance / hold / abort / escalate した理由を説明する能力を減らしてはならない。

したがって、検証では RULE の有無だけでなく、制御意図を確認する。

最初の validation layer が答えるべき問いは以下である。

```text
PSC は scenario に対して期待される behavior category を選んだか
```

v0.1 では数値 threshold の比較までは不要とする。

---

## 4. Scenario Set

| Scenario | 表す risk | 最小 stimulus | Expected behavior category | Candidate RULE evidence |
|----------|-----------|---------------|----------------------------|-------------------------|
| light_false_negative | 不安定性があるが LIGHT observation では直接検出できない | recovery ramp 中に隠れた stability dip が発生 | hold_or_escalate | `RULE-22_RETURN_RAMP_HOLD` または `RULE-05_ESCALATE_conflict` |
| light_telemetry_gap | 必須 LIGHT input が利用できない | trust、stability proxy、freshness、confidence の欠落 | hold | `RULE-22_RETURN_RAMP_HOLD` |
| light_stale_telemetry | telemetry は存在するが freshness window を超過 | ramp decision で古い sample が使われる | hold | `RULE-22_RETURN_RAMP_HOLD` |
| light_masked_instability | sparse sampling が短時間の instability を隠す | accepted sample の間で stability dip が発生 | hold_or_escalate | `RULE-22_RETURN_RAMP_HOLD` または `RULE-05_ESCALATE_conflict` |
| light_delayed_abort | LIGHT では FULL より instability 検知が遅れる | LIGHT delay 後に hard failure または severe instability が見える | abort | `RULE-23_RETURN_RAMP_ABORT` |
| light_resolver_escalation | LIGHT evidence だけでは recovery と risk を区別できない | trust / stability / confidence が競合 | escalation_and_cooldown | `RULE-05_ESCALATE_conflict`, `RULE-12_COOLDOWN_active` |

---

## 5. Expected Behavior Categories

validator は RULE matching に加えて behavior category を扱える構造にする。

| Category | 意味 | Acceptable evidence |
|----------|------|---------------------|
| switch | PSC が selected path または ramp target を意図的に切り替える | scenario が switch を期待し、switch RULE が出る |
| hold | PSC が current selected path または ramp weight を維持する | KEEP または HOLD RULE が出る |
| abort | unsafe evidence により recovery ramp advancement を停止する | `RULE-23_RETURN_RAMP_ABORT` が出る |
| escalation | 曖昧な制御判断を Resolver へ委譲する | `RULE-05_ESCALATE_conflict` が出る |
| escalation_and_cooldown | escalation 後に連続 arbitration を抑制する | escalation RULE と cooldown RULE が両方出る |
| fallback | degraded fallback path へ入る、または利用する | DEGRADED trigger / switch RULE が出る |

これにより、検証を以下から一段進める。

```text
RULE が出たか
```

から、

```text
出た RULE は期待される制御意図と整合しているか
```

へ進める。

---

## 6. Hold 解除 Gate

`RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` は、以下の gate をすべて満たすまで Hold のままとする。

| Gate | Requirement |
|------|-------------|
| Scenario coverage | Section 4 の LIGHT 固有 scenario が runnable または manual traceable validation case として存在する |
| Expected category mapping | 各 scenario に expected behavior category が宣言されている |
| Missing telemetry handling | 必須 LIGHT input 欠落時に ramp advance しない |
| Stale telemetry handling | stale telemetry で ramp advance しない |
| Masked instability handling | sparse evidence が曖昧な場合は hold または Resolver escalation になる |
| Delayed abort handling | LIGHT observation でも severe instability は abort になる |
| Resolver escalation handling | 曖昧な LIGHT evidence は escalation でき、その後 cooldown に入る |
| Evidence Matrix integration | 実行 evidence が存在した後、scenario、RULE、STEP、log reference が追加されている |

---

## 7. Validator Structure Extension Draft

現在の `scripts/validate_evidence_rules.py` は、scenario output に expected RULE identifier が出るかを検証している。

次の構造では、この挙動を維持したまま、任意の behavior intent metadata を追加する。

提案形:

```python
ScenarioCheck(
    name="resolver_switch",
    command=(...),
    expected_rules=(...),
    expected_category="escalation_and_cooldown",
)
```

初期 category は string-based かつ non-numeric のままでよい。
validator は以下を満たした場合に pass とする。

1. command が正常終了する。
2. 必須 RULE identifier がすべて出る。
3. scenario の expected behavior category が、観測された RULE family により満たされる。

これは structure extension として扱う。
threshold comparison、step ordering、telemetry value check は最初の拡張では scope 外に残す。

---

## 8. Existing Scenario の初期 Category Mapping

| Existing scenario | Current expected RULE basis | Proposed expected category |
|-------------------|-----------------------------|----------------------------|
| switch_score | `RULE-01_KEEP_score`, `RULE-02_SWITCH_score` | switch |
| resolver_switch | `RULE-05_ESCALATE_conflict`, `RULE-14_RESOLVER_switch`, `RULE-12_COOLDOWN_active` | escalation_and_cooldown |
| recovery_return_v02 | `RULE-15`, `RULE-16`, `RULE-18`, `RULE-19` | switch |
| degraded | `RULE-07`, `RULE-09` | fallback |
| recovery_hold | `RULE-10`, `RULE-11`, keep behavior | hold |

この mapping は暫定であり、LIGHT 固有 scenario 追加時に調整する。

---

## 9. Non-Goals

本計画では以下を定義しない。

- LIGHT の最終 threshold
- production telemetry schema
- Fast Mode packet format
- numeric pass / fail comparison
- Resolver 内部 arbitration logic
- LIGHT advance の Verified 昇格

---

## 10. Next Work

1. Section 4 の 6 scenario に対応する LIGHT scenario stub または scripted case を追加する。
2. `ScenarioCheck` に任意の `expected_category` field を追加する。
3. emitted RULE identifier から category を推定する小さな helper を追加する。
4. LIGHT 専用 validation log を生成する。
5. log が存在した後に Evidence Matrix を更新する。
