# PSC Fast Mode Bundle Capacity Control v0.1

## 1. Document Information

- Document Name : PSC Fast Mode Bundle Capacity Control
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Control Plane / Fast Mode / Capacity Control
- Document Type : Design Draft
- Status : Draft
- Language : Japanese

- Related Models:
  - PSC Fast Mode Security Boundary Model v0.1
  - PSC Fast Mode LIGHT Observation Boundary v0.1
  - PSC RCU Recovery Return Model v0.2
  - PSC Recovery Return Abort Handling v0.1
  - PSC Telemetry Model v0.2

---

## 2. 目的

本ドラフトは、Fast Mode bundle 内の 1 本以上の物理 lane が degraded になった場合の
PSC Fast Mode における capacity stabilization と source throttling の挙動を定義する。

Fast Mode は CPU node PSC と local device node PSC、GPU node PSC、または
NVMe node PSC の間にある isolated 1-hop trusted local capacity-control mode である。
general routing mode でも complex arbitration mode でもない。

例:

```text
CPU PSC
<-> local device node PSC / GPU node PSC / NVMe node PSC
```

単一の Fast Mode bundle 内には複数の physical lane が存在し得る。
lane capacity が変化した場合、PSC は即時に full utilization へ戻そうとするのではなく、
bundle capacity を安定化しなければならない。

---

## 3. 範囲

本ドラフトは以下を扱う。

- boundary isolation control
- lane degradation detection
- effective bundle capacity calculation
- source throttling requests
- capacity stabilization margin
- capacity recovery ramp
- bundle failure conditions
- no-capacity-margin conditions
- observation and evidence requirements

本ドラフトは以下を定義しない。

- general PSC routing fallback
- complex multi-path Resolver arbitration
- device-internal bottleneck diagnosis
- Fast Mode packet format
- production threshold values
- simulation behavior
- validator behavior
- Evidence Matrix entries

---

## 4. Key Concepts

| Term | Meaning |
|------|---------|
| Fast Mode Bundle | PSC endpoint 間の direct trusted Fast Mode connection。複数 physical lane を含み得る |
| Lane Health | lane 単位の operational condition。healthy、degraded、unavailable、failed など |
| Bundle Health | lane health、capacity、confidence、policy から導出される Fast Mode Bundle 全体の health |
| Effective Capacity | unavailable lane を除外し、degradation と safety margin を適用した usable capacity |
| Safety Margin | lane degradation 後の overload と oscillation を防ぐための reserved capacity headroom |
| Source Throttle | source-side PSC に offered traffic の reduction または shaping を求める policy-controlled request |
| Capacity Recovery Ramp | capacity evidence が安定した後、allowed utilization を段階的に回復する制御 |
| NO_CAPACITY_MARGIN | remaining capacity が traffic demand を安全に吸収できない状態 |
| Boundary Gate | local trusted 1-hop containment と explicit exit / fallback handoff を強制する最小 Fast Mode boundary logic |
| Capacity Manager | lane health、bundle health、effective capacity、safety margin、throttling、recovery ramp を扱う最小 Fast Mode capacity logic |
| LANE_LOSS | lane exclusion と firmware-visible warning を必要とする physical / structural lane failure class |

---

## 5. 設計原則

### 5.1 Isolated 1-Hop Trusted Local Mode

Fast Mode は trusted local domain と 1-hop local connection に限定される。

主な想定関係は以下である。

```text
CPU node PSC
<-> local device node PSC / GPU node PSC / NVMe node PSC
```

Fast Mode は CPU node と local node area の間に isolation されたままでなければならない。
routing fabric へ自動的に escape してはならない。

normal PSC routing または fabric control は、explicit Fast Mode exit または
fallback handoff の後にのみ再開できる。

### 5.2 Fast Mode は alternate routing ではない

Fast Mode bundle degradation は、別 route が存在することを仮定してはならない。

CPU PSC と GPU PSC が direct trusted bundle で通信する場合、
bundle は複数 lane を持ち得るが、それらの lane は normal PSC fabric における
独立 routing path ではない。

Fast Mode は general routing を行ってはならず、complex multi-path Resolver arbitration を
含むべきではない。本モデルにおける Resolver involvement は、authorization、policy、
boundary decision、suspension、fallback handoff に限定される。

### 5.3 utilization 復帰の前に capacity を安定化する

lane capacity が低下した場合、PSC はまず新しい effective capacity に対して
traffic を安定化しなければならない。

即時 full-capacity restoration は remaining lane を overload させ、
oscillation を生む可能性がある。

### 5.4 Source-side control は第一級の制御である

destination-side または bundle-side capacity が低下した場合、
source-side PSC は offered traffic rate を下げる必要があり得る。

Source throttling は policy controlled かつ explainable でなければならない。

Fast Mode が safe margin を維持できない場合、source traffic を throttle するか、
Fast Mode を suspend すべきである。

### 5.5 判断には observation evidence が必要である

capacity change は evidence によって裏付けられなければならない。
LIGHT observation が不十分な場合、PSC は utilization を増やす前に
observation density を上げる、または FULL observation へ昇格すべきである。

---

## 6. Minimum Fast Mode Logic

Fast Mode v0.1 は必要最小限の logic だけを保持すべきである。

```text
Fast Mode Logic =
Boundary Gate
+ Capacity Manager
```

### 6.1 Boundary Gate

Boundary Gate は以下を扱う。

- 1-hop enforcement
- trusted local domain validation
- CPU node <-> local device node containment
- routing fabric isolation
- explicit exit / fallback handoff

Boundary Gate は route search や general PSC path selection を行わない。

### 6.2 Capacity Manager

Capacity Manager は以下を扱う。

- lane health
- bundle health
- effective capacity
- baseline and dynamic safety margin
- source throttle
- capacity recovery ramp

Capacity Manager は unrelated fabric path 間の arbitration を行わない。
local Fast Mode bundle capacity と source-side pressure を制御する。

---

## 7. Capacity Planning and Double Margin

Fast Mode capacity は二つの異なる margin で計画すべきである。

### 7.1 Hardware-Level Headroom

node designer は maximum theoretical node bandwidth を見積もるべきである。

required optical channel count は、target device が maximum expected load を
margin 付きで実行できるよう hardware-level headroom を持って選択すべきである。

### 7.2 PSC Control-Level Safety Margin

PSC はさらに control-level safety margin を適用する。

PSC は operational margin を予約し、margin consumption を監視する。
この margin は jitter、retry、transient delay variance、recovery ramp uncertainty を吸収するために使われる。

Fast Mode は normal operation において raw 100% physical capacity に依存すべきではない。
specific margin values は implementation and simulation dependent のままとする。
simulation は後で margin rule と recovery behavior を tune すべきである。

unexplained noise、jitter、retry、delay variance、または instability が
PSC safety margin の大部分を繰り返し消費する場合、Fast Mode は bundle を unstable と分類し、
suspend または downgrade してよい。

---

## 8. Scope Control for Node-Internal Causes

Fast Mode v0.1 は PSC-visible lane / bundle capacity と boundary isolation に集中する。

primary Fast Mode logic からは以下の device-internal causes を除外する。

- GPU thermal throttle
- VRAM pressure
- DMA congestion
- node-internal bottlenecks
- application-local scheduling limits

これらは後で external node-side capacity reports として表現してよい。
Fast Mode v0.1 はこれらの原因を内部で診断または arbitrate しようとすべきではない。

---

## 9. Lane Degradation Detection

PSC は以下の evidence により lane degradation を検出すべきである。

- lane down または unavailable signal
- optical error または link quality degradation
- retry、loss、corruption indicator の増加
- lane throughput の低下
- latency または variance の増加
- stale または conflicting telemetry
- observation confidence の低下
- lane-loss または reinitialization 後の repeated lane-loss

Lane health classes:

| Lane Health | Description |
|-------------|-------------|
| HEALTHY | policy と safety margin の範囲内で expected traffic を運べる |
| DEGRADED | reduced confidence または reduced capacity の下で利用可能 |
| LIMITED | throttled または restricted condition 下でのみ利用可能 |
| UNAVAILABLE | 一時的に traffic を運べない |
| FAILED | recovery validation に成功するまで除外すべき |

### 9.1 Lane-Loss Handling

`LANE_LOSS` は normal quality degradation ではなく、physical または structural failure class として扱うべきである。

`LANE_LOSS` に入った lane は `FAILED` として mark し、Fast Mode capacity から除外すべきである。
`LANE_LOSS` の automatic runtime recovery を仮定してはならない。

Recovery は以下のいずれかを必要とすべきである。

- system power cycle
- explicit maintenance action
- hardware reinitialization

同じ lane-loss condition が reinitialization または power cycle 後に再発する場合、
PSC はその lane または bundle の Fast Mode を disabled のまま維持し、
RED firmware-level warning を emit すべきである。

operator または maintenance system は以下を inspect すべきである。

- optical cable
- connector
- optical module
- rack / node joint
- PSC endpoint
- related physical layer

---

## 10. Effective Bundle Capacity

Effective Capacity は、lane health と safety margin を考慮した現在の usable bundle capacity である。

概念式:

```text
raw_lane_capacity = sum(healthy_lane_capacity + degraded_lane_usable_capacity)
effective_capacity = raw_lane_capacity - safety_margin
```

PSC は raw lane capacity を traffic admission に直接公開すべきではない。
traffic admission は effective capacity に基づくべきである。

Effective Capacity inputs:

- healthy lane 数
- degraded lane 数
- lane ごとの usable capacity
- lane confidence
- telemetry freshness
- bundle policy
- safety margin
- traffic class

---

## 11. Safety Margin

Safety Margin は、degradation 後の remaining lane が saturation へ追い込まれることを防ぐ
reserved bundle capacity である。

Safety Margin は以下の場合に増やすべきである。

- 1 本以上の lane が degraded になった
- observation confidence が低下した
- telemetry が stale または conflicting である
- lane recovery が直近である
- traffic が bursty である
- Resolver が bundle を unstable と分類した

Safety Margin は、capacity recovery validation window を通じて stable evidence が継続した後にのみ減らしてよい。

---

## 12. Source Throttle

offered traffic が effective capacity を超える場合、PSC は source-side throttling を要求すべきである。

Source Throttle は以下を要求し得る。

- offered rate の低減
- 一時的な burst shaping
- low-priority traffic の defer
- high-priority traffic の preserve
- capacity-sensitive transfer の delayed retry

すべての source throttling は policy controlled でなければならない。

Source Throttle が期待される条件:

- 1 本以上の lane が degraded または unavailable になった
- remaining lane の capacity margin が不足している
- bundle health が LIMITED になった
- recovery ramp が active だが未完了である
- full utilization に対する observation confidence が不足している

---

## 13. Capacity Recovery Ramp

capacity が回復した場合でも、PSC は即時に full utilization へ戻してはならない。

Capacity Recovery Ramp は、以下の条件を満たした後にのみ allowed utilization を段階的に増やす。

- failed または degraded lane が recovery を報告している
- telemetry freshness が許容範囲内である
- confidence が十分である
- lane stability が validation window を通じて継続している
- bundle health が degraded ではない
- Resolver または policy が recovery を許可している

ramp は以下を満たすべきである。

- current effective capacity から開始する
- allowed utilization を段階的に増やす
- safety margin を維持する
- telemetry が suspicious になった場合は stop または hold する
- hard failure または unsafe evidence が現れた場合は abort する

この挙動は Recovery Return および Recovery Abort Handling と同じ
stability-first principle に従う。

---

## 14. No-Capacity-Margin Conditions

`NO_CAPACITY_MARGIN` は、lane degradation 後の remaining bundle capacity が
offered traffic を安全に受け入れられない場合に発生する。

これは、少なくとも 1 本の lane が healthy な場合でも発生し得る。

期待される挙動:

- bundle が prior capacity で継続可能だと仮定しない
- forwarding が安全に継続可能な場合、current state を hold する
- source reduction を要求する
- observation density を上げる、または LIGHT を FULL observation へ昇格する
- ambiguity が残る場合は Resolver re-evaluation を発火する
- capacity evidence が安定するまで immediate full recovery を避ける

`NO_CAPACITY_MARGIN` は bundle failure と同義ではない。
これは current offered load に対して remaining capacity が safe admission に不足していることを意味する。

---

## 15. Bundle Failure Conditions

Fast Mode Bundle は以下の場合 unavailable と見なすべきである。

- すべての lane が failed または unavailable である
- lane loss により safe Fast Mode operation を維持できない
- forwarding safety を維持できない
- optical failure が bundle 全体に影響している
- severe corruption が検出された
- source throttling でも traffic を十分に減らせず safe forwarding を維持できない
- policy が Fast Mode 継続利用を禁止している

期待される挙動:

```text
Fast Mode unavailable
-> exit or suspend Fast Mode
-> fall back to normal PSC behavior if available
-> notify Resolver and source-side PSC
```

normal PSC behavior への fallback は条件付きである。
有効な normal PSC path が存在し、policy が許可する場合にのみ使用する。

Fast Mode は routing fabric へ自動的に escape してはならない。
normal PSC routing または fabric control は、explicit Fast Mode exit または
fallback handoff の後にのみ再開できる。

---

## 16. Fast Mode Host and Firmware Notification

PSC は Fast Mode protection action を自律的に実行する。

Host、OS、UEFI、BIOS、firmware notification は visibility、user warning、
event logging、maintenance guidance のために存在する。
critical Fast Mode protection を PSC が実行するために OS participation を必要としてはならない。

### 16.1 Severity Levels

| Severity | Meaning | Expected Notification | Expected Fast Mode Action |
|----------|---------|-----------------------|---------------------------|
| GREEN | normal Fast Mode operation | warning 不要 | normal Fast Mode を継続 |
| YELLOW | Fast Mode は operational のままだが quality が degraded | boot 後の OS-level notification と system event log | shutdown せず継続し、必要に応じて throttle または capacity reduction |
| RED | Fast Mode を安全に維持できない、または initialization が critical Fast Mode condition を検出 | UEFI / BIOS / firmware-level warning | Fast Mode を disable または suspend し、可能なら normal PSC behavior を使用 |
| BLACK | PSC または required base fabric を安全に initialize できない | firmware / service-level failure indication | boot block または service intervention が必要になり得る |

### 16.2 YELLOW Conditions

YELLOW conditions は degraded だが operational な Fast Mode behavior を示す。
system は shutdown せず継続すべきである。

例:

- `LANE_DEGRADATION`
- `MARGIN_CONSUMPTION_HIGH`
- `NOISE_DEGRADATION`
- `SOURCE_THROTTLE_ACTIVE`
- `FAST_MODE_DEGRADED`
- operational のままの `BUNDLE_UNSTABLE`

user-facing warning example:

```text
Fast Mode link quality is degraded. PSC is reducing transfer rate to maintain stability.
```

### 16.3 RED Conditions

RED conditions は Fast Mode を安全に維持できないことを示す。

これらは OS boot 前、または Fast Mode initialization 中に検出され得る。
RED conditions は UEFI / BIOS / firmware level で visible であるべきである。
OS に到達しない場合や、OS boot 前に Fast Mode が disabled になる場合があるためである。

期待される挙動:

- Fast Mode を disable または suspend する
- 可能な場合は normal PSC behavior を使って継続する
- failed lane を excluded のまま維持する
- firmware-visible diagnostic information を記録する
- hardware inspection または maintenance を案内する

例:

- `LANE_LOSS`
- `OPTICAL_MODULE_FAILURE`
- `CONNECTOR_FAULT`
- `PSC_PHY_FAILURE`
- `FAST_MODE_INITIALIZATION_FAILURE`
- system power cycle または reinitialization 後の repeated lane-loss

user-facing warning example:

```text
PSC Fast Mode critical warning: lane loss detected. Fast Mode has been disabled. Check optical cable, connector, optical module, rack/node joint, or PSC endpoint.
```

### 16.4 BLACK Conditions

BLACK conditions は normal Fast Mode degradation の範囲外である。

PSC または required base fabric を安全に initialize できないことを示す。
normal boot が block される、または service intervention が必要になる場合がある。

### 16.5 OS vs Firmware Responsibility

PSC は protection を自律的に実行しなければならない。

OS notification は以下のために使う。

- user visibility
- event logging
- maintenance guidance
- operational status display

YELLOW conditions は boot 後に OS へ report してよい。

RED conditions は UEFI / BIOS / firmware level で report すべきである。
Fast Mode が OS boot 前に disabled になる場合や、OS に到達しない場合があるためである。

base PSC initialization が unsafe な場合、BLACK conditions は normal boot を妨げ得る。

---

## 17. Expected Behavior Examples

| Case | Condition | Expected Behavior |
|------|-----------|-------------------|
| A | 8 lanes healthy | Effective capacity は 100% のまま |
| B | 1 lane degraded | Effective capacity を下げ、offered load が safe capacity を超える場合は source throttle を要求 |
| C | capacity restored | Capacity Recovery Ramp により utilization を full capacity へ段階的に戻す |
| D | remaining lanes have insufficient margin | `NO_CAPACITY_MARGIN` を emit または classify し、安全な場合は current state を hold して source reduction を要求 |
| E | bundle failure | Fast Mode を unavailable とし、可能な場合は normal behavior へ fallback |
| F | lane loss | lane を FAILED として mark し、Fast Mode capacity から除外して RED firmware-level warning を emit |

---

## 18. Observation and Evidence Requirements

PSC は capacity decision を説明するために十分な evidence を保持しなければならない。

Minimum evidence:

- bundle identifier
- lane identifiers
- lane health state
- bundle health state
- effective capacity
- safety margin
- offered traffic estimate
- source throttle request state
- observation mode
- telemetry freshness
- telemetry confidence
- Resolver decision または policy reason
- notification severity
- host / firmware notification state
- lane-loss recurrence state

LIGHT observation が capacity increase に十分な evidence を提供できない場合、
PSC は capacity recovery を hold するか FULL observation へ昇格しなければならない。

---

## 19. Draft Validation Direction

本ドキュメントは draft specification のみである。

将来の validation work では以下を追加し得る。

- lane degradation source throttle scenario
- no-capacity-margin scenario
- capacity recovery ramp scenario
- bundle failure fallback scenario
- host / firmware notification severity scenario
- lane-loss recurrence scenario
- LIGHT-to-FULL observation promotion scenario

本ドキュメントでは simulation、validator、Evidence Matrix、published specification の更新は定義しない。
