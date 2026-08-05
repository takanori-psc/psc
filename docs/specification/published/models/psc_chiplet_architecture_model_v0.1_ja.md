# PSC Chiplet Architecture Model v0.1

## Document Information

- Document Name : PSC Chiplet Architecture Model
- Version : v0.1
- Project : PSC / Photon System Controller
- Layer : PSC Hardware
- Document Type : Specification
- Status : Draft
- Author : T. Hirose
- Created : 2026-03
- Last Updated : 2026-08
- Language : Japanese

---

## 1. 目的

本書は、PSC Endpoint、PSC Switch、PSC Fabric Coreに共通するPSCデバイスの
チップレットアーキテクチャモデルを定義する。PSCは単一のmonolithic chipではなく、
機能単位のchipletを組み合わせるscalable fabric deviceとして設計する。

---

## 2. 設計思想

### 2.1 Modular Architecture

機能単位をchipletとして分離し、製品モデル間で再利用する。

### 2.2 Scalable Fabric

ポート数、処理能力、control core数をchiplet構成により拡張可能とする。

### 2.3 Unified Device Architecture

PSC Endpoint、PSC Switch、PSC Fabric Coreは、同じ基本chiplet architectureを使用し、
ポートロール、chiplet数、control core数により製品ロールを構成する。

---

## 3. PSC Chiplet Structure

PSC packageの基本構造を以下に示す。

```text
PSC Package
├ Switching Core Chiplet
├ Port Chiplet(s)
├ Telemetry / Security Chiplet
└ RISC-V Control Cluster
```

各chipletは専用機能を担当し、Internal Interconnectを介して連携する。

---

## 4. Chiplet Types

### 4.1 Switching Core Chiplet

data planeの中核として以下を担当する。

- fabric switching
- packet forwarding
- internal routing
- crossbar / NoC management

### 4.2 Port Chiplet

PSC Fabricの論理ポートインターフェースを提供し、以下を担当する。

- logical port control
- link state management
- port buffer management
- Telemetry
- fault detection
- configurable port role management

ポートロールの例を以下に示す。

- Fabric Port
- Endpoint Port
- Storage Port
- Trusted Port
- Restricted Port
- External Domain Port

Port Chipletが光変換器を必ず内蔵するとは定めない。電気・光変換機能は、PSC package
内部または外部のいずれに配置してもよい。

### 4.3 Telemetry / Security Chiplet

以下のFabric監視およびsecurity機能を提供する。

- fabric telemetry
- congestion monitoring
- security enforcement
- trust evaluation support

### 4.4 RISC-V Control Cluster

PSC control planeとして以下を担当する。

- fabric initialization
- policy management
- security and trust management
- routing control
- telemetry aggregation
- fault management

control core数は製品モデルとchiplet規模に応じてスケールする。

---

## 5. Internal Interconnect

chiplet間は低遅延・高帯域のInternal NoCまたはchiplet fabric linkで接続する。
具体的なprotocol、lane構成、帯域およびphysical implementationは今後の実装検討で
定義する。

---

## 6. Port and Optical Interface Model

PSCの外部接続、node接続およびInter-System Cross-Connectは、光接続を基本方針とする。
本書の「ポート」はPSC Fabricのlogical interfaceおよび対応するbandwidth unitを表し、
特定の光実装方式を確定するものではない。

将来のphysical implementation候補には以下を含む。

- Pluggable Optics
- Onboard Optics
- External Optical Engine connected through a short-reach electrical interface
- Co-Packaged Optics

physical lane数、lane speed、modulation、wavelength、Duplex、FEC、connector、
transceiver、reach、optical power budgetは未確定である。logical route structureは、
採用する光実装方式から独立して定義する。詳細は将来の
`PSC Optical Interface Model`候補または実装別仕様で扱う。

Fabric Switch Nodeなどの製品モデルで「1 port 800 Gb/s」を使用する場合、その値は
1つのlogical PSC port全体のdesign assumptionであり、単一physical laneを意味しない。

---

## 7. Product Model Scaling

PSCは共通chiplet architectureを基盤として複数の製品モデルを構成する。

| Product Model | Primary Role |
|---------------|--------------|
| PSC Endpoint | computeまたはlocal node connection |
| PSC Switch | rack / fabric switching |
| PSC Fabric Core | cluster core fabric |

製品モデルは主に以下でスケールする。

- port count
- chiplet count
- control core count
- configured port roles

共通の32-port PSC chipletは、製品モデルごとに異なるport roleを割り当てて使用できる。
32-port構成はlogical port countを表し、特定のphysical optical implementationを
固定しない。

### 7.1 PSC Switch Product Overview

PSC Switchは共通PSC chiplet architectureを使用する製品モデルである。
PSC Fabric Switch NodeはSystem A / System Bの2系統で構成し、各系統に32-portの
PSC Switchを使用するため、node全体では64 portsとなる。

各系統の詳細なport allocation、Inter-System Cross-Connect、external route structure、
route selectionおよびfailure handlingは、
`PSC Fabric Switch Node Architecture Model v0.1`で定義する。
Fabric Switch Nodeの制御にはRISC-V Control Clusterを使用する。この設計は継続中である。

関連文書:

- `docs/specification/published/models/psc_fabric_switch_node_architecture_model_v0.1_ja.md`

### 7.2 CPU Node PSC Product Role Example

CPU Node内には共通32-port PSC chipletをSystem A / System B用に各1 chip配置する。

各PSC chipのport roleは以下とする。

- 8 ports: 対応するPSC Fabric Switch systemとの接続
- 24 ports: CPU Node配下のlocal nodeとの接続

CPU Node内のPSC-AとPSC-Bの間には、Fabric Switch NodeのようなInter-System
Cross-Connect portを設けない。配下nodeがPSC-A / PSC-Bの両系統へ直接接続でき、
送信元側で正常系統を選択できるためである。

CPU Node配下のlocal nodeは、そのCPU Node専属とする。想定例は以下である。

- GPU Node
- AI Long-Term Memory Node
- Storage Node

片系PSCまたは片系linkの障害時は正常系統を使用する。24 local portsのnode別割当は
未確定であり、本書では固定しない。上記node typeは非規範的な構成例である。

### 7.3 Rack-Level Horizontal Scaling

PSC製品モデルは、rack内で複数の独立した`PSC計算グループ`へ水平スケールできる。
1つのPSC計算グループは、1つのPSC Fabric Switch Node、1つの対応CPU Node、および
そのCPU Node専属のLocal Nodesで構成する。Fabric Switch Nodeはrack全体ではなく、
1つのPSC計算グループに対応する。

rack当たりのgroup数候補、group間通信、failure domainの扱い、およびcapacity scalingは、
`PSC Fabric Switch Node Architecture Model v0.1`で扱う。

---

## 8. Future Extension

将来拡張の候補を以下に示す。

- high-density Port Chiplet
- AI-assisted fabric control
- distributed control model
- advanced security functions
- product-specific chiplet count and control-core scaling
- detailed optical interface and implementation-specific specifications
