# PSC Address Format v0.1

## ドキュメント情報

ドキュメント名 : PSC Address Format
バージョン     : v0.1
プロジェクト   : PSC / Photon System Controller
レイヤ         : PSC Fabric
ドキュメント種別 : 仕様書
ステータス     : Draft

作成者         : T. Hirose
作成日         : 2026-03
最終更新       : 2026-03

言語           : Japanese

---

## 1. 目的

PSC Address Format は、
PSC Fabric 内部でルーティングおよび転送実行に使用される
ネイティブアドレス構造を定義する。

このアドレス形式は、
明確な階層構造を提供し、
効率的なルーティング、
スケーラブルなシステム展開、
およびシンプルなハードウェア実装を
実現することを目的としている。

PSCアドレスは、
PSC Fabric 内における通信エンドポイントの
物理的および論理的な位置を表す。

---

## 2. 設計目標

PSC Address Format は以下の設計目標を持つ。

- Scalability（スケーラビリティ）

アドレス構造は、
小規模なローカルPSCシステムから
大規模な分散インフラストラクチャまで
対応可能でなければならない。

- Hierarchical Routing（階層ルーティング）

アドレス形式は、
Fabric、Cluster、Node、Port からなる
PSC Fabric の階層トポロジーを
反映する構造でなければならない。

- Hardware Efficiency（ハードウェア効率）

RCU、TMU、TEU などの PSC モジュール内部で
効率的にハードウェア実装できる形式であること。

- Deterministic Routing（決定的ルーティング）

ルーティング判断は、
複雑な変換処理を必要とせず、
アドレスフィールドから直接導出できること。

- Future Expandability（将来拡張性）

グローバルアドレスや
論理サービス識別など、
将来のPSC拡張を許容できる構造とする。

---

## 3. アドレス形式概要

PSC は固定長の 64ビットアドレスを使用する。

アドレスは
4つの階層フィールドで構成される。

- Fabric ID
- Cluster ID
- Node ID
- Port ID

アドレス構造

Fabric ID : Cluster ID : Node ID : Port ID

各フィールドは
PSC Fabric トポロジーの階層を表す。

---

## 4. ビット割り当て

PSCネイティブアドレスは固定長の64ビット構造であり、
以下の4つのフィールドで構成される。

Address Bit Layout (64-bit)

| Fabric ID | Cluster ID | Node ID | Port ID |
|-----------|------------|---------|---------|
| 16 bits   | 16 bits    | 24 bits | 8 bits  |

この割り当ては
スケーラビリティと
ハードウェア効率のバランスを考慮している。

---

## 5. フィールド定義

### 5.1 Fabric ID

Fabric ID は
PSC Fabric ドメインを識別する。

Fabric は
PSCノードが PSC Fabric リンクによって
相互接続されるルーティングドメインを表す。

大規模構成では
複数の Fabric が存在する可能性がある。

最大 Fabric 数: 65536

### 5.2 Cluster ID

Cluster ID は
Fabric 内のノードグループを識別する。

Cluster は
物理または論理的なグループを表すことができる。

例

- ラックグループ
- ローカル計算クラスタ
- データセンターセグメント
- エッジクラスタ

Cluster による組織化は
ルーティングのスケーラビリティと
管理性を向上させる。

Fabric あたり最大 Cluster 数: 65536

### 5.3 Node ID

Node ID は
Cluster 内の PSC ノードを識別する。

Node は
PSC Fabric に接続された
デバイスまたは処理要素を表す。

例

- CPUノード
- GPUノード
- メモリノード
- ストレージノード
- ネットワークノード
- アクセラレータノード

Node ID は
Cluster 内で一意でなければならない。

Cluster あたり最大 Node 数: 16777216

### 5.4 Port ID

Port ID は
Node 内の通信エンドポイントを識別する。

Port は
PSC通信インターフェースまたは
内部機能エンドポイントを表す。

例:

- PSC光ポート
- 内部デバイスインターフェース
- 論理通信エンドポイント

Node あたり最大 Port 数: 256

---

## 6. ルーティングでの利用

PSCのルーティング判断は
主に Routing Control Unit（RCU）によって処理される。

階層型アドレス構造により、
アドレスフィールド解析による
ルーティング判断が可能になる。

ルーティング階層

- Fabricレベル
- Clusterレベル
- Nodeレベル
- Portレベル

この構造により
大規模PSC Fabric においても
効率的なルーティングが可能となる。

---

## 7. 解決レイヤとの関係

64ビットPSCアドレスは、
PSC Fabric 内で使用される
ネイティブ転送アドレスである。

以下のような上位識別子は

- 論理サービス名
- グローバル識別子
- 仮想ノード参照
- アプリケーションレベルオブジェクト識別子

Resolver などの上位レイヤで
解決される。

解決モデル例:
```
Logical Name
      ↓
Resolver
      ↓
PSC Native Address (64bit)
```
この分離により
PSC Fabric のルーティングシステムは
シンプルで効率的に保たれる。

---

## 8. アドレス例

例アドレス

1 : 2 : 100 : 3

Fabric 1
Cluster 2
Node 100
Port 3

例使用ケース

GPUノードがメモリノードに
データ要求を行う場合

送信元アドレス

1 : 2 : 50 : 1

宛先アドレス

1 : 2 : 100 : 3

---

## 9. 将来拡張

将来の PSC バージョンでは
以下のような拡張が追加される可能性がある。

- 階層ルーティングドメイン
- Spine-Leaf トポロジ識別子
- グローバルPSCアドレス
- 論理サービスアドレス
- 機能レベルアドレス

現在の 64ビット構造は
これらの拡張と互換性を保つよう
設計されている。

---

## 10. まとめ

PSC Address Format v0.1 は
PSC Fabric 内部で使用される
64ビット階層型アドレスを定義する。

この構造は
Fabric ID、Cluster ID、Node ID、Port ID
のフィールドで構成される。

この設計により
スケーラブルなルーティング、
効率的なハードウェア実装、
および PSC システムの
明確な階層構造が実現される。

PSC ネイティブアドレスは
Fabric レベルの通信に焦点を当てており、
より上位の識別は
上位解決レイヤによって処理される。
