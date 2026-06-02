# PSC LIGHT Observation Glossary v0.1（日本語版）

## 1. Document Information

- Document Name : PSC LIGHT Observation Glossary
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Telemetry / Fast Mode / Validation
- Document Type : Glossary
- Status : Published Draft
- Author : T. Hirose
- Created : 2026-06-02
- Last Updated : 2026-06-02
- Language : Japanese

- Related Documents:
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC LIGHT Observation Validation Plan v0.1
  - PSC Telemetry Model v0.2
  - PSC RCU Recovery Return Model v0.2
  - PSC Evidence Matrix v0.1

---

## 2. 目的

本 Glossary は、現在の PSC LIGHT Observation validation scenario、
evidence log、および promotion 議論で使用する用語を定義する。

以下の用語は PSC の挙動を説明するものであり、一般的な業界用語の
定義だけを示すものではない。PSC において LIGHT Observation は
意図的に保守的な観測モードであり、観測を軽くしたこと自体は
return ramp advance を許可する理由にはならない。

---

## 3. 用語

### 3.1 LIGHT Observation

- Definition: full density の telemetry ではなく、最小限の安全な telemetry set を使用する reduced observation mode。
- PSC Context: LIGHT Observation は recovery 中の telemetry cost や latency を下げる可能性があるが、RCU と Resolver が利用できる evidence は FULL Observation より少ない。
- Why it matters: PSC は reduced evidence を、より厳しい gating、freshness check、confidence check、hold behavior、または Resolver review で補償しなければならない。LIGHT Observation は、それ自体では ramp advancement を許可しない。
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`, `RULE-23_RETURN_RAMP_ABORT`, `RULE-05_ESCALATE_conflict`

### 3.2 FULL Observation

- Definition: PSC control decision で、より高密度かつ完全な telemetry を使用する保守的な observation mode。
- PSC Context: FULL Observation は recovery ramp validation と abort behavior の baseline mode である。stability、trust、path health、hard failure detection に対してより強い evidence を提供する。
- Why it matters: LIGHT Observation が advance、hold、abort、escalate のどれを選べるかを判断するための比較基準になる。
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-23_RETURN_RAMP_ABORT`

### 3.3 False Negative

- Definition: actual path instability が存在するにもかかわらず、LIGHT Observation がそれを直接検出できない状態。
- PSC Context: `light_false_negative` validation scenario は、instability が存在する一方で LIGHT sample が acceptable に見える recovery ramp をモデル化する。
- Why it matters: false negative の後に return ramp を advance すると、不安定な path へ traffic を戻す可能性がある。そのため PSC は、安全な advance を証明する evidence が不足しているとして `RULE-22_RETURN_RAMP_HOLD` を emit する。
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`

### 3.4 Masked Instability

- Definition: stability proxy は healthy に見えるが、hidden instability がまだ存在する状態。
- PSC Context: `light_masked_instability` scenario は、acceptable な proxy signal の背後に risk が隠れる reduced observation をモデル化する。
- Why it matters: PSC は proxy を truth ではなく evidence として扱う。hidden instability を否定できない場合、Resolver は return ramp を安全に advance できないため、PSC は `RULE-22_RETURN_RAMP_HOLD` を emit する。
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`, `RULE-05_ESCALATE_conflict`

### 3.5 Stale Telemetry

- Definition: telemetry は存在するが、現在の decision に対して許容される freshness window を超えて古くなった状態。
- PSC Context: `light_stale_telemetry` scenario は、outdated な LIGHT telemetry と ramp advancement に不足する confidence をモデル化する。
- Why it matters: 古い telemetry は現在の path state を表していない可能性がある。PSC は stale evidence では recovered path traffic の増加を正当化できないため、`RULE-22_RETURN_RAMP_HOLD` を emit する。
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`

### 3.6 Telemetry Freshness

- Definition: PSC decision に使用される telemetry の age と validity window。
- PSC Context: Freshness は LIGHT Observation の minimum input の一つである。sample は trust、stability、confidence、ramp-state decision を支えるために十分 current でなければならない。
- Why it matters: reduced observation では、accepted sample が現在状態を代表していない risk が高くなる。freshness が missing または stale の場合、PSC は advance せず hold しなければならない。
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`

### 3.7 Observation Confidence

- Definition: completeness、freshness、observation mode を考慮した後、PSC が observed telemetry に割り当てる decision confidence。
- PSC Context: LIGHT Observation は、少ない signal、低い telemetry density、または proxy measurement に依存するため confidence が低くなり得る。
- Why it matters: Confidence は evidence が advance を支えられるか、hold すべきか、escalation すべきかを決める。confidence が不足する場合、return ramp は Hold に留まる。
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`, `RULE-05_ESCALATE_conflict`

### 3.8 Hold

- Definition: current selected path または current return ramp weight を維持する PSC behavior category。
- PSC Context: LIGHT validation では、evidence が `RETURN_RAMP_ADVANCE` に不足する場合に `expected_category=hold` を使用する。
- Why it matters: Hold は、不確実な observation によって recovered path への exposure が増えることを防ぐ保守的な結果である。
- Related Rules: `RULE-22_RETURN_RAMP_HOLD`, `RULE-20_RETURN_KEEP`, `RULE-11_RECOVERY_cooldown`

### 3.9 Return Ramp

- Definition: recovered path の traffic weight を段階的に増やす progressive reintegration process。
- PSC Context: Return Ramp は recovery validation の後、full traffic return の前に実行される。reintegration 中も observable であり abortable である。
- Why it matters: ramp は traffic allocation を即時切替ではなく段階的に変えることで、recovery risk を制限する。
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`, `RULE-23_RETURN_RAMP_ABORT`, `RULE-24_RETURN_RAMP_COMPLETE`

### 3.10 Return Ramp Advance

- Definition: Return Ramp 中に recovered-path traffic weight を増やす PSC decision。
- PSC Context: FULL Observation では stable evidence の後に advance が可能である。一方 LIGHT Observation では、promotion conditions が満たされるまで advance は blocked のままである。
- Why it matters: Advance は recovered path への exposure を増加させる。false negative、stale telemetry、masked instability の risk が未解決の場合、PSC は LIGHT evidence だけで advance してはならない。
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`

### 3.11 RULE-22_RETURN_RAMP_HOLD

- Definition: Return Ramp が current weight を維持すべき場合、つまり advancement conditions が満たされていない場合に emit される PSC rule。
- PSC Context: 現在の LIGHT validation scenarios では、false negative、stale telemetry、masked instability、telemetry gap など insufficient-evidence cases にこの rule を使用する。
- Why it matters: この rule は、PSC が LIGHT Observation を advance 許可として扱わず、意図的に conservative hold behavior を選んだことを記録する。
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-23_RETURN_RAMP_ABORT`, `RULE-05_ESCALATE_conflict`

### 3.12 Observation Promotion

- Definition: LIGHT Observation behavior を Hold status から formal advance eligibility へ進める process。
- PSC Context: Promotion は、minimum telemetry、freshness bounds、confidence floors、false negative bounds、masked-instability handling、evidence logs が定義された後の `RULE-21_RETURN_RAMP_ADVANCE (LIGHT)` にのみ適用される。
- Why it matters: Promotion は、performance や低い telemetry cost だけが ramp advance の理由になることを防ぐ。
- Related Rules: `RULE-21_RETURN_RAMP_ADVANCE`, `RULE-22_RETURN_RAMP_HOLD`

### 3.13 Observation Escalation

- Definition: reduced または conflicting observation evidence を local LIGHT decision path だけで解決せず、Resolver review に送る PSC behavior。
- PSC Context: LIGHT Observation は、trust、stability proxy、freshness、confidence が recovery と risk を区別できない場合に escalation することがある。
- Why it matters: Escalation は、hold だけでは ambiguous evidence を説明または arbitration できない場合でも PSC safety を維持する。
- Related Rules: `RULE-05_ESCALATE_conflict`, `RULE-12_COOLDOWN_active`, `RULE-22_RETURN_RAMP_HOLD`

---

## 4. Validation Alignment

現在の LIGHT Observation validation scenarios では、これらの用語を以下のように使用する。

| Scenario | Term focus | Expected category | Expected rule | Reason |
|----------|------------|-------------------|---------------|--------|
| light_false_negative | False Negative | hold | `RULE-22_RETURN_RAMP_HOLD` | `OBSERVATION_FALSE_NEGATIVE` |
| light_stale_telemetry | Stale Telemetry | hold | `RULE-22_RETURN_RAMP_HOLD` | `STALE_TELEMETRY` |
| light_masked_instability | Masked Instability | hold | `RULE-22_RETURN_RAMP_HOLD` | `MASKED_INSTABILITY` |

これらの scenarios は、ramp advancement の promotion criteria が明示的に
満たされるまで、LIGHT Observation が conservative に扱われることを確認する。
