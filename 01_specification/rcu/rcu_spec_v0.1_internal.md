# RCU 詳細設計 v0.1 (Internal Scope)

Status: Draft  
Date: 2026-02-27  
Parent: PSC Concept v1.0  

---

## 0. スコープ

本RCUは単一PC内部（GPU / RAM / NVMe / Network I/F）を対象とする。  
外部ノード（他PSC）は扱わない。

物理リンクは主に電気インターコネクト（PCIe等）を対象とし、  
将来の光リンクにも拡張可能な抽象構造とする。

---

## 1. RCUの責務

### 1.1 RCUが担当すること（空間制御）

- 物理リンク選択（port / lane / link）
- 論理パス選択（path_id）
- パスの確立・維持・撤去（setup / active / teardown）
- フェイルオーバ（代替経路への切替）
- リンク品質に応じた制限（cap / degrade）
- 再トレーニング要求の発行

### 1.2 RCUが担当しないこと

- 転送優先順位決定（TMUの責務）
- 実データ転送（TEUの責務）
- 生のリンク監視計測（ICI / OMUの責務）

整理：

TMU = 時間制御  
RCU = 空間制御  
TEU = 実行

---

## 2. インターフェース

### 2.1 入力

TMU → RCU  
TransferRequest { src, dst, class, size_hint, qos, deadline? }

ICI → RCU  
LinkState { link_id, state, bw, latency_hint, error_rate, retrain_need }

OMU → RCU（光構成時）  
OpticalHealth { link_id, tx_power, rx_power, temp, ber, aging_score }

TEU → RCU  
PathStats { path_id, throughput, stall, retry, drop }

CI（管理） → RCU  
Policy { allowlist, denylist, maintenance_mode, power_cap }

---

### 2.2 出力

RCU → ICI  
ConfigureLink { link_id, rate, fec_mode, retrain, enable }

RCU → TEU  
PathPlan { path_id, hops[], cap, failover_list[], ttl, epoch }

RCU → TMU  
PathOffer { src, dst, path_id, capacity, cost, risk, ttl }

---

## 3. 内部構成

+-----------------------+
|   (1) Topology Manager |
+-----------+-----------+
            |
            v
+-----------+-----------+
|   (2) Path Computation |
+-----------+-----------+
            |
            v
+-----------+-----------+
|   (3) Path Lifecycle   |
+-----------+-----------+
            |
            v
+-----------+-----------+
| (4) Failover & Recovery|
+-----------------------+

---

### 3.1 Topology Manager

- ノード/リンク構造保持
- LinkState履歴管理
- Policy反映
- 禁止リンク管理

### 3.2 Path Computation

- 候補経路生成
- 劣化リンク回避
- コスト評価

例：

cost = latency + (error_rate * risk_weight)

### 3.3 Path Lifecycle

- NEW
- SETUP
- ACTIVE
- DEGRADED
- FAILOVER
- RECOVERY
- TEARDOWN

epoch + ttl により古い設定の適用を防止する。

### 3.4 Failover & Recovery

- 障害検知
- 即時切替
- フラップ防止ヒステリシス
- 段階的復旧

---

## 4. データモデル

### 4.1 LinkState

- state: UP / DOWN / DEGRADED / TRAINING
- bw
- latency_hint
- error_rate
- health
- last_change

### 4.2 Path

- path_id
- hops[]
- cap
- cost
- ttl
- epoch

### 4.3 TransferClass（暫定）

- CONTROL
- LATENCY
- BULK
- BACKGROUND

---

## 5. 状態遷移

NEW → SETUP → ACTIVE  
ACTIVE → DEGRADED → ACTIVE  
ACTIVE → FAILOVER → ACTIVE  
FAILOVER → RECOVERY → ACTIVE  
(any) → TEARDOWN

---

## 6. Failover Execution Algorithm (v0.1)

本節では、FailoverListに基づく実行順序を定義する。

### 6.1 トリガー条件

注: 時間定数・閾値（degrade_confirm_window_ms / flap_guard_time_ms など）は topology_internal_v0.1 に従う。

Failoverは以下の条件で開始される：

1. LinkState = DOWN
2. DEGRADED状態が degrade_confirm_window_ms を超過
3. PathStats.stall または retry が閾値を超過
4. OMUが深刻な劣化を報告

---

### 6.2 実行アルゴリズム（擬似コード）

function handle_path_degradation(path_id):

    for action in FailoverList[path_id]:

        if action == retrain(link):
            if retrain(link) == SUCCESS:
                if link_stable():
                    return ACTIVE

        if action == set_fec_strong(link):
            apply_strong_fec(link)
            if link_stable():
                return DEGRADED

        if action == cap_path(value):
            apply_cap(path_id, value)
            if performance_improves():
                return DEGRADED

        if action == teardown(path_id):
            teardown(path_id)
            notify_TMU_capacity_zero(path_id)
            return TEARDOWN

    return FAILOVER

---

### 6.3 Recovery Procedure

function handle_recovery(path_id):

    wait(flap_guard_time_ms)

    if link_stable_for(recovery_probe_interval_ms):

        gradually_remove_cap(path_id)
        return ACTIVE

    else:
        remain_in_DEGRADED

---

### 6.4 安全機構

- epoch番号により古いFailover処理を無効化する
- ttl切れのPathPlanは自動破棄する
- 同一pathで同時に複数Failoverを走らせない（排他制御）

---

End of RCU Specification v0.1
