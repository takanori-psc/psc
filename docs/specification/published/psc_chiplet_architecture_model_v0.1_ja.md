# PSC Chiplet Architecture Model v0.1 (JP)

## ドキュメント情報

- Document Name: PSC Chiplet Architecture Model
- Version: v0.1
- Project: PSC / Photon System Controller
- Layer: PSC Hardware
- Status: Draft
- Author: T. Hirose
- Language: Japanese

---

## 1. 目的

本ドキュメントは PSC デバイスの
チップレットアーキテクチャモデルを定義する。

PSC はスケーラブルな Fabric デバイスとして設計されており、
単一モノリシックチップではなく チップレットベース構造を前提とする。

チップレット構造により以下を実現する。

- スケーラブルなポート構成
- 複数製品モデルへの展開
- 制御プレーンの柔軟な拡張
- 製造コストの最適化

---

## 2. 設計思想

PSC ハードウェアは以下の設計思想に基づく。

## 2.1 Modular Architecture

機能単位ごとにチップレットを分離する。

## 2.2 Scalable Fabric

ポート数や処理能力をチップレット追加で拡張可能とする。

## 2.3 Unified Device Architecture

PSC Endpoint / PSC Switch / PSC Fabric Core のすべてを
共通の基本アーキテクチャで構成する。

---

## 3. PSC チップレット構造

PSC パッケージは複数のチップレットで構成される。

例：
```
PSC Package
├ Switching Core Chiplet
├ Port Chiplet(s)
├ Telemetry / Security Chiplet
└ RISC-V Control Cluster
```
各チップレットは専用機能を担当する。

---
 
## 4. チップレットタイプ

PSC は主に以下のチップレットで構成される。

## 4.1 Switching Core Chiplet
 
Fabric スイッチング処理を担当する。

主な役割
 
- Fabric switching
- Packet forwarding
- Internal routing
- Crossbar / NoC 管理
 
データプレーンの中心となる。
 
## 4.2 Port Chiplet

Fabric ポートインターフェースを提供する。

主な役割
 
- 光リンク制御
- ポートバッファ管理
- ポート状態監視
- ポートロール設定

ポートは設定により役割を変更できる。

例：
 
- Fabric port
- Endpoint port
- Trusted port
- Restricted port
 
## 4.3 Telemetry / Security Chiplet
 
Fabric 状態監視およびセキュリティ機能を提供する。
 
主な役割
 
- Fabric Telemetry
- Congestion monitoring
- Security enforcement
- Trust evaluation support

Routing Pipeline の状態情報を提供する。
 
## 4.4 RISC-V Control Cluster
 
PSC の Control Plane を担当する。
 
主な役割
 
- Fabric 初期化
- Policy 管理
- Security 管理
- Trust 管理
- Routing 制御
- Telemetry 集約
- 障害管理
 
コア数はチップレット規模に応じてスケーリングされる。

---

## 5. 内部インターコネクト
 
チップレット間は高速内部インターコネクトで接続される。
 
例：
 
- Internal NoC
- High-speed chiplet fabric
 
この内部接続は PSC Fabric の性能を維持するため
低遅延・高帯域で設計される。

---

## 6. ポート構成モデル
 
PSC ポートは固定用途ではなく
設定により役割を変更可能である。
 
例：
```
Port Role Examples
 
Fabric Port
Endpoint Port
Storage Port
Trusted Port
External Domain Port
```
ポート設定は Control Plane により管理される。

---

## 7. 製品モデルスケーリング
 
PSC は共通チップレット構造を基盤として
複数の製品モデルを構成する。
 
例：
 
| モデル          | 用途           |
| --------------- | -------------- |
| PSC Endpoint    | 計算ノード接続 |
| PSC Switch      | ラックスイッチ |
| PSC Fabric Core | クラスタ中核   |
 
各モデルは
 
- ポート数
- チップレット数
- 制御コア数
 
によって差別化される。

---
 
## 8. 将来拡張
 
将来的には以下の拡張が考えられる。
 
- 高密度ポートチップレット
- AI支援 Fabric 制御
- 分散制御モデル
- 高度なセキュリティ機能
 
