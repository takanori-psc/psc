# PSC Fabric Switch Node Architecture Model v0.1

## Document Information

- Document Name : PSC Fabric Switch Node Architecture Model
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Hardware / Fabric Switch Node
- Document Type : Specification
- Status : Draft
- Author : T. Hirose
- Created : 2026-08
- Last Updated : 2026-08
- Language : Japanese

---

## 1. 目的

本書は、共通PSC chiplet architectureを使用するPSC Fabric Switch Node固有の
node structure、port allocation、route structure、failure handling、capacity model、
control architectureを定義する。

---

## 2. Scope

本書のscopeは以下である。

- System A / System Bによるdual-system Fabric Switch Node
- 32-port PSC Switch 2台による64-port node
- CPU Node、external PSC Fabric、Inter-System Cross-Connectへのlogical port allocation
- route selection、failure handling、capacityおよびdegraded operationの設計意図
- optical portをlogical interfaceとして扱う方針
- dedicated hardwareとRISC-V Control Clusterの役割分担

optical physical layerの詳細、上位制御policy、Recovery Return / Return Ramp、Resolver、
trust / security policyの詳細は本書で再定義しない。

---

## 3. Terminology

| Term | Meaning |
|------|---------|
| Fabric Switch Node | System AとSystem Bの2つのPSC Switchで構成するnode |
| System A / System B | 相互に独立した2つのswitch system |
| CPU Node Connection | 単一の対応CPU Nodeへ接続する各system 8-port group |
| External Route | external PSC Fabricへ接続する8-port logical route group |
| Inter-System Cross-Connect | 反対systemのexternal route群を利用するための8-port inter-system route |
| Logical Port | PSC Fabric interfaceおよび対応するbandwidth unit |
| Route Capacity | logical port line rateの合計。guaranteed effective bandwidthではない |

---

## 4. Node Role

PSC Fabric Switch Nodeは、単一CPU Nodeとexternal PSC Fabricの間を接続し、
System A / System B、複数external route、Inter-System Cross-Connectにより経路選択肢を
提供する。node固有の構成を定義する本書と、共通chipletを定義する
`PSC Chiplet Architecture Model v0.1`の責任範囲を分離する。

本書で定義する64-port PSC Fabric Switch Nodeはラック全体ではなく、ラック内の
1つの`PSC計算グループ`に属する。1つのFabric Switch Nodeは、同じグループ専属の
1つのCPU NodeへA/B合計16 logical portsで接続する。

---

## 5. Default Node Structure

```text
PSC Fabric Switch Node
├ System A PSC Switch: 32 logical ports
└ System B PSC Switch: 32 logical ports
```

node全体は64 logical portsである。各systemは独立したPSC Switchとして構成し、
RISC-V Control Clusterを使用する。設計は継続中である。

### 5.1 ラック内グループスケーリング

1つのPSC計算グループは以下で構成する。

- 1つのPSC Fabric Switch Node
  - System A PSC Switch
  - System B PSC Switch
- 1つの対応CPU Node
  - PSC-A
  - PSC-B
- そのCPU Node専属のLocal Nodes
  - GPU Node
  - AI Long-Term Memory Node
  - Storage Node

```text
PSC Rack
├ Compute Group 0
│  ├ PSC Fabric Switch Node 0
│  ├ CPU Node 0
│  └ Dedicated Local Nodes
├ Compute Group 1
│  ├ PSC Fabric Switch Node 1
│  ├ CPU Node 1
│  └ Dedicated Local Nodes
├ Compute Group 2 (optional)
└ Compute Group 3 (optional)
```

physical rackには複数の独立したPSC計算グループを搭載できる。現時点では1、2、
または4 groupsを構成候補とするが、v0.1ではrack当たりのgroup数を固定仕様または
必須product configurationとして確定しない。group数はphysical space、power、
cooling、weight、optical cabling、maintainabilityによって決定する。

各groupのCPU NodeとLocal Nodesはそのgroup専属であり、Local Nodesを複数の
PSC計算グループ間で共有する構成は現在のbase modelに含めない。各groupは、
rack-level architecture内で独立して隔離可能なfailure domainとして扱う。ただし、
rack電源、cooling、physical structure、management infrastructureなどのrack-level
resourceは共通failure factorとなる可能性がある。1 groupのCPU Nodeまたは
Fabric Switch Nodeが停止しても、共有rack-level failureが発生していない限り、
rack内のother groupsは原則として継続可能とする。

group間通信は各Fabric Switch Nodeのexternal PSC Fabric routeを通じて行う。
rack内PSC計算グループ間のdedicated direct connectionは現時点の必須仕様としない。

現在の800 Gb/s logical-port assumptionによる単純line-rate例を以下に示す。

| Compute Groups per Rack | Aggregate CPU-Node Line Rate | Aggregate External Physical Line Rate |
|-------------------------|------------------------------|---------------------------------------|
| 1 | 12.8 Tb/s | 25.6 Tb/s |
| 2 | 25.6 Tb/s | 51.2 Tb/s |
| 4 | 51.2 Tb/s | 102.4 Tb/s |

この表はlogical port line rateの単純合計であり、effective bandwidth、upstream Fabric
capacity、power、cooling、cabling、weight、maintainabilityを保証しない。

---

## 6. System A / System B Architecture

System AとSystem Bは同じ32-port構成を持つ。

| Port Group | Ports per System | Role |
|------------|------------------|------|
| CPU Node Connection | 8 | 単一の対応CPU Nodeとの専用接続 |
| Inter-System Cross-Connect | 8 | 反対systemへの系統間route |
| External PSC Fabric | 16 | 8-port external route 2本 |
| Total | 32 | 1 systemのlogical port総数 |

各systemのpower、Port Chiplet、optical wiring、upstream switchなどは、可能な限り
異なるfailure domainへ分離する。

---

## 7. Port Configuration

### 7.1 System A

- CPU Node Connection: 8 ports（CPU Node内PSC-Aへ接続）
- A-to-B Cross-Connect Route: 8 ports
- A-1 Route: 8 external ports
- A-2 Route: 8 external ports

### 7.2 System B

- CPU Node Connection: 8 ports（CPU Node内PSC-Bへ接続）
- B-to-A Cross-Connect Route: 8 ports
- B-1 Route: 8 external ports
- B-2 Route: 8 external ports

各systemのCPU Node向け8 portsは、複数CPU Nodeへ1 portずつ割り当てるものではない。
System Aの8 portsとSystem Bの8 portsは、すべて同じ単一CPU Nodeへ接続する。

### 7.3 Logical Port and Optical Interface

CPU Node connection、external Fabric connection、Inter-System Cross-Connectは、
標準構成では光接続を前提とする。1 portは総帯域800 Gb/sのlogical PSC portとして
扱う。この値は現在のdesign assumptionであり、確定したphysical product specification
ではない。また、800 Gb/sを単一physical laneと解釈しない。

physical lane数、lane speed、modulation、wavelength、Duplex、FEC、connector、
transceiver、reach、optical power budgetは未確定である。Pluggable Optics、Onboard
Optics、External Optical Engine、Co-Packaged Opticsを将来候補として残す。
将来の同一board内または同一package内実装でshort-reach electrical connectionを
使用する可能性を禁止しない。実際の電気・光変換はPSC package内部または外部へ
配置可能であり、logical route structureは採用する光実装方式から独立して定義する。

---

## 8. External Route Structure

各systemの16 external portsは、独立した2つの8-port routeへ分割する。

```text
System A: A-1 (8) + A-2 (8)
System B: B-1 (8) + B-2 (8)
```

1 external routeの想定physical line-rate capacityは以下である。

`800 Gb/s × 8 ports = 6.4 Tb/s`

1 systemのexternal physical capacityは以下である。

`6.4 Tb/s × 2 routes = 12.8 Tb/s`

Fabric Switch Node全体では以下となる。

`12.8 Tb/s × 2 systems = 25.6 Tb/s`

---

## 9. Inter-System Cross-Connect

各方向のCross-Connectは8 logical ports、想定6.4 Tb/sである。

- A-to-B: System AからSystem BのB-1 / B-2を利用するためのroute
- B-to-A: System BからSystem AのA-1 / A-2を利用するためのroute

Cross-Connectは単なる予備portではなく、反対systemのexternal route群を利用する
ためのinter-system routeである。external route failure、external path failure、
congestion avoidance、route switching、staged recoveryで使用できる。

A Switch自体が完全停止した場合、A-to-B Cross-Connectは使用できない。B Switch自体が
完全停止した場合もB-to-A Cross-Connectは使用できない。この場合、CPU Node側から
正常な反対systemを直接選択する。

---

## 10. CPU Node Connectivity

CPU NodeとFabric Switch NodeはA/B合計16 logical portsで接続する。

- System A 8 ports -> 同一CPU Node内PSC-A
- System B 8 ports -> 同一CPU Node内PSC-B
- per-system capacity: `800 Gb/s × 8 = 6.4 Tb/s`
- A/B aggregate physical line rate: `6.4 Tb/s × 2 = 12.8 Tb/s`

CPU Node内PSC-A / PSC-B間にはCross-Connectを設けない。CPU Node配下のlocal nodeが
両systemへ直接接続され、source sideで正常systemを選択できるためである。片system
全体が停止した場合、残存systemの8 ports、最大想定6.4 Tb/sで継続する。

---

## 11. Route Selection

各systemでは、CPU Node側から入る最大8 ports分のtrafficに対し、同じ6.4 Tb/sの
capacityを持つ3つのroute candidateを用意する。

- System A: A-1、A-2、A-to-B Cross-Connect
- System B: B-1、B-2、B-to-A Cross-Connect

normal operationでは同一systemの2 external routesを使用する。failureまたはcongestion
時は、同一systemのremaining external route、Cross-Connect経由のopposite-system route、
またはCPU Nodeによるopposite systemのdirect selectionを選択肢とする。

detailed route policy、staged recovery、Return Ramp、Resolver arbitration、trust / security
policyは上位PSC control modelに委ね、本書では検証RULEを重複定義しない。

---

## 12. Failure Handling

- 1つの8-port external routeがfailureしても、同一systemのもう1 routeが正常で十分な
  capacityを持つ場合は、入力全量を処理でき、直ちにcapacity degradationとはならない。
- 同一systemの2 external routesが使用不能でも、opposite systemの2 routesが正常で
  十分なavailable capacityを持つ場合、Cross-Connect経由でbandwidthを維持できる。
- 上記ではroute redundancyは低下するが、available bandwidthは必ずしも低下しない。
- remaining effective capacityがrequired bandwidthを下回った時点でcapacity-degraded
  operationへ移行する。
- System AまたはBのSwitch全体が停止した場合、CPU Nodeはremaining systemを選択し、
  maximum connection line rateは12.8 Tb/sから6.4 Tb/sへ低下する。
- node全体のcommon failureまたはA/B simultaneous failureはnode単体では継続できない。

Cross-ConnectおよびA-1 / A-2 / B-1 / B-2は、見かけだけのredundancyを避けるため、
power、Port Chiplet、optical wiring、upstream switchの過度な共有を避ける。

---

## 13. Capacity and Degraded Operation

| Connection / Route | Calculation | Assumed Line Rate |
|--------------------|-------------|-------------------|
| CPU Node connection per system | 800 Gb/s × 8 | 6.4 Tb/s |
| CPU Node connection across A/B | 6.4 Tb/s × 2 | 12.8 Tb/s |
| One external route | 800 Gb/s × 8 | 6.4 Tb/s |
| External capacity per system | 6.4 Tb/s × 2 | 12.8 Tb/s |
| Node-wide external physical capacity | 12.8 Tb/s × 2 | 25.6 Tb/s |
| One directional Cross-Connect route | 800 Gb/s × 8 | 6.4 Tb/s |

これらはlogical port line rateの単純合計であり、guaranteed effective bandwidthではない。
protocol overhead、control traffic、Telemetry、retransmission、buffer contentionを考慮した
effective bandwidthは、将来のsimulationおよびimplementation evaluationで決定する。

以下は運用状態を説明するための概念的label例である。

- NORMAL
- ROUTE_REDUNDANCY_DEGRADED
- CRITICAL_SINGLE_PATH
- CAPACITY_DEGRADED
- ISOLATED

`NORMAL`と`ISOLATED`は既存PSC modelでも使用されるため、本書はこの集合を新しい正式な
state modelとして定義しない。正式なstate名、transition、thresholdは既存state modelとの
整合確認後に別途定義する。

---

## 14. Control Architecture

### 14.1 Dedicated Hardware

- link heartbeat monitoring
- timeout detection
- transfer gate control
- emergency cut
- fault event latch
- minimum fault-information retention

### 14.2 RISC-V Control Cluster

- fault-cause classification
- route-state management
- route selection
- A/B inter-system coordination
- notification to other nodes
- Telemetry aggregation
- input provision for Hold / Switch / Return decisions
- log management

### 14.3 Higher-Level PSC Control Models

- detailed route-selection policy
- staged recovery and Return Ramp
- Resolver arbitration
- trust and security policy

firmwareへ全処理を集中させず、immediate safety actionはdedicated hardware、policyと
coordinationはRISC-Vおよびhigher-level control modelが担当する。

---

## 15. Telemetry and Logging

Port Chipletとcontrol planeは少なくとも以下を区別して報告・管理する。

- optical lane-level degradation
- logical port-level degradation
- route-group-level degradation
- complete route loss

link state、capacity indication、failure domain、route availability、Cross-Connect使用状態を
Telemetryとして集約し、route selectionとfault analysisへ提供する。Lane Remapping、FEC、
optical module recovery、physical-layer retransmissionは本書のscope外である。

---

## 16. Design Status and Future Work

本モデルはDraftであり、以下は未確定またはfuture workである。

- 800 Gb/s logical port assumptionのproduct specification化
- effective bandwidth、oversubscription、buffer contentionのsimulation
- physical optical lane、modulation、wavelength、Duplex、FEC、connector、reach、power budget
- Pluggable / Onboard / External Engine / Co-Packaged Opticsの選択
- failure-domain分離のphysical implementation
- conceptual operational labelsと既存state modelの正式な対応
- route selection、capacity degradation、recovery thresholdの実装別定義
- 将来候補文書`PSC Optical Interface Model`

正式参照文書:

- `docs/specification/published/models/psc_chiplet_architecture_model_v0.1_ja.md`
- `docs/specification/published/models/psc_resolver_arbitration_extension_model_v0.2x_ja.md`
- `docs/specification/published/models/psc_trust_model_v0.1_ja.md`
- `docs/specification/published/models/psc_state_transition_model_v0.1_ja.md`
- `docs/specification/published/models/psc_fast_mode_security_boundary_model_v0.1_ja.md`
- `docs/specification/published/models/psc_rcu_recovery_return_model_v0.2_ja.md`
- `docs/specification/published/models/psc_recovery_return_extension_model_v0.2x_ja.md`
