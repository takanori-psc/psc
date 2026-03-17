# Internal Topology v0.1 (Single PC)

Status: Draft
Date: 2026-02-27
Parent: RCU Spec v0.1 (Internal)

---

## 0. Purpose

RCUが扱う内部ノード/リンク/ポートの一覧を固定し、
PathComputation と Failover の前提を定義する。

---

## 1. Nodes

| NodeId | Type | Notes |
|---|---|---|
| CPU  | compute | Control Interfaceのみ（データパスは原則PSC管理） |
| GPU0 | device  |  |
| RAM  | memory  |  |
| NVMe0| storage |  |
| NIC0 | network |  |

---

## 2. Ports (ICI)

| PortId | Side | ConnectedTo | LinkType | Notes |
|---|---|---|---|---|
| P0 | PSC/ICI | GPU0  | PCIe |  |
| P1 | PSC/ICI | NVMe0 | PCIe |  |
| P2 | PSC/ICI | NIC0  | PCIe |  |
| P3 | PSC/ICI | RAM   | internal | （任意：内部バス扱い） |

---

## 3. Links

| LinkId | PortId | State | NominalBW | Retrain | Notes |
|---|---|---|---|---|---|
| L0 | P0 | UP | TBD | yes/no |  |
| L1 | P1 | UP | TBD | yes/no |  |
| L2 | P2 | UP | TBD | yes/no |  |
| L3 | P3 | UP | TBD | n/a |  |

---

## 4. Default Paths (初期パス)

| PathId | Src | Dst | Hops (Node/Port/Link...) | Cap | FailoverList |
|---|---|---|---|---|---|
| PATH_GPU0_TO_NVME0 | GPU0 | NVMe0 | GPU0 -> P0/L0 -> PSC -> P1/L1 -> NVMe0 | 1.00 | [retrain(L0), set_fec_strong(L0), cap_path(0.80), cap_path(0.50), cap_path(0.25), retrain(L1), set_fec_strong(L1), cap_path(0.80), cap_path(0.50), cap_path(0.25), teardown(PATH_GPU0_TO_NVME0)] |
| PATH_GPU0_TO_NIC0  | GPU0 | NIC0  | GPU0 -> P0/L0 -> PSC -> P2/L2 -> NIC0  | 1.00 | [retrain(L0), set_fec_strong(L0), cap_path(0.80), cap_path(0.50), cap_path(0.25), retrain(L2), set_fec_strong(L2), cap_path(0.80), cap_path(0.50), cap_path(0.25), teardown(PATH_GPU0_TO_NIC0)] |
| PATH_NVME0_TO_NIC0 | NVMe0| NIC0  | NVMe0-> P1/L1 -> PSC -> P2/L2 -> NIC0  | 1.00 | [retrain(L1), set_fec_strong(L1), cap_path(0.80), cap_path(0.50), cap_path(0.25), retrain(L2), set_fec_strong(L2), cap_path(0.80), cap_path(0.50), cap_path(0.25), teardown(PATH_NVME0_TO_NIC0)] |

## 5. Failover Policy (暫定)

- Link DOWN: failover_list の先頭へ即時切替
- Link DEGRADED: cap適用 → しきい値超過でfailover
- Recovery: ヒステリシス時間を置いて段階復帰

(Parameters)
- degrade_threshold: TBD
- flap_guard_time: TBD
- recovery_probe_interval: TBD

---

## 6. Default Parameters (v0.1 initial)

- flap_guard_time_ms: 500
- recovery_probe_interval_ms: 2000
- degrade_error_threshold: 1e-6         # error_rateがこれを超えたらDEGRADED候補
- down_confirm_window_ms: 50            # DOWN判定の最小確定窓
- degrade_confirm_window_ms: 200        # DEGRADED判定の確定窓
- cap_step_table:
  - DEGRADED_L1: 0.80
  - DEGRADED_L2: 0.50
  - DEGRADED_L3: 0.25

## 7. Cap / Degrade Rule (v0.1)

- LinkState=DOWN:
  - 即時 FAILOVER（failover_list 先頭へ）
- LinkState=DEGRADED:
  - capを段階適用（0.80 → 0.50 → 0.25）
  - 0.25適用後も stall/retry が改善しない場合 FAILOVER
- LinkState=UP へ復帰:
  - 直ちに戻さない（flap_guard_time_ms 経過後に RECOVERY）
  - RECOVERY中は probe（recovery_probe_interval_ms）し、安定なら段階的にcap解除

## 8. FailoverList Generation (Internal v0.1)

前提：内部は基本的に「PSCを経由する1ホップ経路」なので、
failoverは「同一リンク内の代替（lane/port設定変更）」を第一優先とする。

FailoverListの優先順位：
1) 同一Portでの再トレーニング（retrain）
2) 同一Portでのrate/fec変更（低速化 + 強FEC）
3) 代替Port（存在する場合のみ。v0.1では未定義）
4) 最終手段：該当PathをTEARDOWNしてTMUに拒否（capacity=0で通知）

---

End of Internal Topology v0.1
