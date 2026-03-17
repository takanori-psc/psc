#PSC Node Type Model v0.1

## ドキュメント情報

- ドキュメント名   : PSC Node Type Model
- バージョン       : v0.1
- プロジェクト     : PSC / Photon System Controller
- レイヤ           : PSC Fabric
- ドキュメント種別 : 仕様書
- ステータス       : Draft
- 作成者           : T. Hirose
- 作成日           : 2026-03
- 最終更新         : 2026-03
- 言語             : Japanese

---

## 1. Purpose（目的）

本ドキュメントは、PSC Fabric において使用される ノードタイプ（Node Type） を定義する。

PSC は Fabric-centric distributed computer architecture を採用しており、
システムを構成する各要素は PSC Fabric 上の ノード（Node） として接続される。

ノードタイプモデルは以下を定義する。

- ノードの役割分類
- 各ノードタイプの責務
- ノードと PSC Plane（Data / Control / Management）の関係
- ノードタイプの拡張性

本モデルは PSC Fabric 上での 機能分離、制御構造、拡張性 を明確にすることを目的とする。

---

## 2. Scope（適用範囲）

本ドキュメントは以下を対象とする。

- PSC Fabric 上のノードの論理分類
- ノードの基本的な責務定義
- ノードタイプと Fabric 機能の関係

以下は本ドキュメントの対象外とする。

- ノード内部の実装詳細
- ノードのハードウェア構成
- ノード間通信プロトコルの詳細

これらは別仕様書で定義する。

---

## 3. Design Principles（設計原則）

PSC Node Type Model は以下の設計原則に基づく。

## 3.1 Role Separation

PSC はシステムの安定性と拡張性のため、
ノードの役割を明確に分離する。

## 3.2 Fabric-Centric Design

PSC Fabric がシステム通信の中心となるため、
すべてのノードは Fabric を介して通信する。

## 3.3 Distributed Autonomy

PSC Fabric は分散型制御モデルを採用し、
ノードは自律的に機能する。

## 3.4 Extensibility

PSC Node Type Model は将来的なノードタイプの追加を想定し、
拡張可能な構造を持つ。

---

## 4. Node Type Overview（ノードタイプ概要）

PSC Fabric では以下の基本ノードタイプを定義する。

| Node Type       | Role                  |
| --------------- | ----------------------|
| Compute Node    | 計算処理ノード        |
| Memory Node     | メモリ資源提供ノード  |
| Storage Node    | 永続ストレージノード  |
| Fabric Node     | Fabric転送ノード      |
| Gateway Node    | 外部接続ノード        |
| Control Node    | Fabric制御ノード      |
| Management Node | 運用管理ノード        |

PSC は以下の思想を採用する。

資源提供ノード、転送ノード、制御ノード、管理ノードを
アーキテクチャ上の異なる役割として明確に分離する。

この役割分離により PSC Fabric は
高い拡張性と安定した運用構造を実現する。

---

## 5. Node Type Definitions（ノードタイプ定義）

## 5.1 Compute Node

Compute Node はアプリケーション実行および計算処理を行うノードである。

主な役割

- アプリケーション処理
- データ処理
- PSC Fabric へのリクエスト生成
- データ受信

Compute Node は PSC Fabric を通じて
メモリ・ストレージ・アクセラレータにアクセスする。

## 5.2 Memory Node

Memory Node は PSC Fabric 上にメモリ資源を提供するノードである。

主な役割

- メモリ領域提供
- 高帯域データ供給
- 低遅延データアクセス

Memory Node は分散メモリプールとして機能する。

## 5.3 Storage Node

Storage Node は永続データストレージを提供するノードである。

主な役割

- 永続データ保存
- 大容量データ提供
- 分散ストレージ構成

Storage Node は PSC Fabric 上で
分散ストレージシステムを形成する。

## 5.4 Fabric Node

Fabric Node は PSC Fabric の接続性を維持するノードである。

主な役割

- パケット転送
- 経路中継
- Fabric 接続維持
- 転送効率の確保

Fabric Node は PSC Fabric の
ネットワーク基盤ノードとして機能する。

## 5.5 Gateway Node

Gateway Node は PSC Fabric と外部ネットワークを接続するノードである。

主な役割

- 外部ネットワーク接続
- 異種プロトコル接続
- Fabric 境界管理

Gateway Node は PSC Fabric の境界ノードとして機能する。

## 5.6 Control Node

Control Node は PSC Fabric の制御機能を担当するノードである。

主な役割

- Fabric 制御
- ルーティング方針管理
- 制御情報配布
- Fabric 状態収束

Control Node は PSC Fabric の Control Plane の中核となる。

## 5.7 Management Node

Management Node は PSC Fabric の運用管理を担当するノードである。

主な役割

- 監視
- 設定管理
- ログ管理
- 運用制御

Management Node は PSC Fabric の Management Plane の中核となる。

---

## 6. Node Type and Plane Relationship（Planeとの関係）

PSC は以下の Plane 構造を持つ。

| Plane            | 主なノード                                    |
| ---------------- | --------------------------------------------- |
| Data Plane       | Compute / Memory / Storage / Fabric / Gateway |
| Control Plane    | Control Node                                  |
| Management Plane | Management Node                               |

この構造により PSC は

- 通信
- 制御
- 運用

を分離したアーキテクチャを実現する。

---

## 7. Dedicated vs Combined Deployment

PSC は Control Node と Management Node の論理分離を基本とする。

理由

- 障害影響の局所化
- セキュリティ強化
- 運用安定性向上

実装上は物理的な同居が可能な場合もあるが、
PSC 標準アーキテクチャでは 専任ノード構成を推奨する。

---

## 8. Node Type Extensibility

PSC Node Type Model は将来的な拡張を想定する。

例

- Accelerator Node
- Service Node
- Hybrid Node

新しいノードタイプは PSC Fabric の設計原則に従い追加できる。

---

## 9. Summary

PSC Node Type Model は PSC Fabric を構成するノードの役割を定義する。

PSC は以下の思想を採用する。

- 資源ノード
- 転送ノード
- 制御ノード
- 管理ノード

をアーキテクチャ上の 独立した役割として定義する。

これにより PSC Fabric は

- 分散制御
- 高い拡張性
- 安定した運用

を実現する。
