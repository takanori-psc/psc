# PSC ポートモデル v0.1

## Document Information

- ドキュメント名: PSC Port Model
- プロジェクト : PSC / Photon System Controller
- レイヤ : PSC Fabric
- ドキュメント種別 : 仕様書
- ステータス : Draft
- 作成者 : T. Hirose
- 作成日 : 2026-03
- 最終更新 : 2026-03
- 言語 : Japanese 

---

## 1. 目的

PSC Port は特定デバイス専用の固定インターフェースとして  
定義されるものではない。

代わりに、各ポートは **Role-based Communication Endpoint**  
として定義される。

ポートの挙動は以下によって決定される。

- Policy
- Trust Class
- Domain
- Transfer Requirements

これにより PSC はポートを  
固定バス接続ではなく **適応型ファブリックエンドポイント**  
として扱うことができる。

---

## 2. 設計思想

### 2.1 従来のポートモデル

ポートはデバイス種別ごとに固定される。

例

- GPU Port
- Storage Port
- Network Port

### 2.2 PSC Port Model

PSC ポートは **論理通信ロール**である。

ポートは主に

- 接続デバイスの種類

ではなく

- 役割
- セキュリティレベル
- 通信ポリシー
- ドメイン
- 転送特性

によって定義される。

---

## 3. Port Definition

PSC Port は PSC Fabric に接続される  
通信エンドポイントである。

接続対象

- ローカルデバイス
- 他 PSC ノード
- ファブリックリンク

各ポートは以下を持つ。

- Port ID
- Port Role
- Port Mode
- Security Class
- Policy Profile
- Domain Scope
- Link State
- Capability Flags

---

## 4. Port Structure

```
PSC Port
├ Port ID
├ Port Role
├ Port Mode
├ Security Class
├ Policy Profile
├ Domain Scope
├ Link State
└ Capability Flags
```

---

## 5. Port ID

Port ID は PSC ノード内で  
通信エンドポイントを識別する ID である。

条件:

- PSC ノード内で一意
- Resolver / Scheduler / RCU / TMU が使用
- ルーティングテーブルにマッピング
- 物理配線を変えずに論理ロール変更可能

例:

- Port 0x01
- Port 0x02
- Port 0x03

---

## 6. Port Role

ポートの現在の論理役割。

例:

- Compute
- Memory
- Storage
- Network
- Fabric
- Management

---

## 7. Port Mode

ポートの動作モード。

- Endpoint Mode
- Fabric Link Mode
- Relay Mode
- Isolated Mode
- Maintenance Mode

---

## 8. Security Class

ポートに適用される信頼レベル。

- System
- Trusted
- User
- External
- Quarantined

---

## 9. Policy Profile

通信の振る舞いを決定する。

- Latency Optimized
- Throughput Optimized
- Secure
- Balanced
- Resilient

---

## 10. Domain Scope

ポート通信可能範囲。

- Local Node
- Local Fabric
- Cluster
- Global Fabric
- External Boundary

---

## 11. Link State

リンク状態:

- DOWN
- INIT
- READY
- DEGRADED
- RESTRICTED
- FAULT

---

## 12. Capability Flags

ポートが持つ能力。

例:

- Chunk Transfer Supported
- Credit Flow Control Supported
- Secure Tag Enforcement Supported
- Multi-path Eligible
- Fabric Relay Allowed

---

## 13. Dynamic Role Binding

PSC ポートは固定役割ではない。

条件:

- security constraint
- topology policy
- Resolver approval
- Scheduler / RCU 更新
- active transfer drain

---

## 14. Port Control Ownership

各モジュールの役割。

- Resolver 
- Scheduler 
- SPU 
- RCU 
- TMU 
- TEU 
- OMU 
- Telemetry / Fault Monitor

---

## 15. Fabric State による挙動

- CALM
- WARM
- HOT
- EMERGENCY

---

## 16. 初期ポートポリシールール

Rule 1  
すべてのポートは 1つの Security Class を持つ。

Rule 2  
すべてのポートは 1つの Policy Profile を持つ。

Rule 3  
Port Role は PSC 制御下でのみ変更可能。

Rule 4  
External / Quarantined は System 権限を直接取得できない。

Rule 5  
Fabric Role ポートは routing validation を必要とする。

Rule 6  
Domain 拡張はポリシー認可が必要。

Rule 7  
DEGRADED / FAULT 状態ではポリシー降格が起こり得る。

---

## 17. Port Table 例

Port ID   Role        Mode            Security   Policy        Domain  
0x01      Compute     Endpoint        Trusted    Latency       Local Node  
0x02      Memory      Endpoint        System     Latency       Local Node  
0x03      Storage     Endpoint        User       Throughput    Cluster  
0x04      Fabric      Fabric Link     Trusted    Balanced      Cluster  
0x05      Network     Relay           External   Secure        External Boundary  
0x06      Management  Maintenance     System     Resilient     Local Node  


## 18. 設計上の意義

PSC Port Model は以下の利点を持つ。

1. **Device abstraction**  
ポートは特定デバイスに固定されない。

2. **Policy-native communication**  
通信ポリシーとセキュリティがポート定義の一部になる。

3. **Fabric adaptability**  
ポートはトポロジー・ワークロード・障害状態に応じて再利用できる。

