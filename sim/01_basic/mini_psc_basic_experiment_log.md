# Mini PSC Experiment Log

## v01 - Basic Routing

- Algorithm: BFS（幅優先探索）
- Feature:
  - 最短経路探索
  - CONGESTEDノードは通らない

- Result:
  - 成功:
    - 混雑時に代替ルートへ切り替え成功

  - 実行結果:
    ```
    === Normal route ===
    Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF']

    === After congestion at nodeD ===
    Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
    ```

---

## v02 - Cost-based Routing

- Algorithm: Dijkstra（最小コスト経路）
- Feature:
  - ノード状態に応じたコスト導入
    - NORMAL = 1
    - WARNING = 5
    - CONGESTED = 100
  - 完全ブロックではなく重み付けによる経路選択

- Result:
  - 成功:
    - ノード状態に応じたコストベースの経路選択が正常に動作
    - 混雑状態（WARNING / CONGESTED）に応じて代替ルートへ自動切替
    - PSCの状態駆動型ルーティングモデルの基本動作を確認

  - 観察:
    - WARNING と CONGESTED の両方で同一の代替ルートが選択された
    - 現在のネットワーク構成では中間的な判断差が現れにくい

  - 課題:
    - ノードコストのみでは経路の多様性が表現できない
    - トポロジが単純でスケーラビリティ評価ができない

  - 次のステップ:
    - リンクコスト（距離 / 転送負荷）を導入
    - WARNING と CONGESTED の挙動差が出る構造を設計

  - 実行結果:
    ```
    === Normal ===
    Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
    Cost: 3

    === WARNING at nodeD ===
    Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
    Cost: 3

    === CONGESTED at nodeD ===
    Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
    Cost: 3
    ```

  - Insight:
    - ノード状態のみの制御では経路選択の表現力が不足することを確認

---

## v03 - Link Cost Routing

- Algorithm: Dijkstra（最小コスト経路）
- Feature:
  - ノード状態コストに加えてリンクコストを導入
  - 経路長と混雑状態の両方を考慮したルーティング
  - WARNING と CONGESTED の中間判断を表現可能にした

- Result:
  - 成功:
    - Normal時は短いルートを選択
    - WARNING時は軽度混雑でも短いルートを維持
    - CONGESTED時は遠回りルートへ切り替え成功
    - ノード状態とリンク距離を組み合わせた経路判断を確認

  - 観察:
    - 状態コストだけでは表現しにくかった中間判断が可能になった
    - 経路長を加えることでPSCらしい選択挙動が見え始めた

  - 課題:
    - コスト値は固定であり動的変化しない
    - ノード数が少なく複数候補経路の複雑性は未検証
    - 負荷履歴やポリシー要素は未導入

  - 次のステップ:
    - ノード数を増やす
    - ランダム負荷変動を導入
    - ログ出力を強化し、選択理由を可視化する

  - 実行結果:
    ```
    === Normal ===
    Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
    Cost: 6

    === WARNING at nodeD ===
    Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
    Cost: 8

    === CONGESTED at nodeD ===
    Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
    Cost: 9
    ```

  - Insight:
    - PSCの経路判断にはノード状態だけでなくリンク距離・転送コストの概念が重要

---

## v04 - Reason Logging

- Algorithm: Dijkstra（最小コスト経路）
- Feature:
  - 候補ルートごとのコストを可視化
  - 選択されたルートとその理由を出力
  - 状態変化に対する判断根拠を確認可能にした

- Result:
  - 成功:
    - 各候補ルートのコスト比較を表示可能
    - 選択ルートと選択理由を可視化
    - PSCの判断過程をログとして確認可能

  - 観察:
    - WARNING時は混雑があっても短距離ルートが維持された
    - CONGESTED時は代替ルートへの切替理由が明確になった

  - 課題:
    - 現在は候補ルートを手動で定義している
    - 理由説明は固定文であり、より汎用的な説明生成が必要
    - トポロジ拡張時のログ量増加に未対応

  - 次のステップ:
    - 候補ルート自動列挙の導入
    - ランダム負荷変動への対応
    - 動的な理由生成ロジックの検討

- 実行結果:
    ```
    === Normal ===
    Candidate routes:
    - nodeA -> nodeB -> nodeD -> nodeF | Cost: 6
    - nodeA -> nodeC -> nodeE -> nodeF | Cost: 9

    Selected route:
    - nodeA -> nodeB -> nodeD -> nodeF | Cost: 6

    Reason:
    - All nodes are in NORMAL state
    - Shorter route has the lowest total cost

    === WARNING at nodeD ===
    Candidate routes:
    - nodeA -> nodeB -> nodeD -> nodeF | Cost: 8
    - nodeA -> nodeC -> nodeE -> nodeF | Cost: 9

    Selected route:
    - nodeA -> nodeB -> nodeD -> nodeF | Cost: 8

    Reason:
    - nodeD is WARNING
    - Upper route is still cheaper than lower route

    === CONGESTED at nodeD ===
    Candidate routes:
    - nodeA -> nodeC -> nodeE -> nodeF | Cost: 9
    - nodeA -> nodeB -> nodeD -> nodeF | Cost: 15

    Selected route:
    - nodeA -> nodeC -> nodeE -> nodeF | Cost: 9

    Reason:
    - nodeD is CONGESTED
    - Congested route became more expensive than alternative route
    ```

  - Insight:
    - PSCでは経路選択そのものだけでなく、判断根拠の可視化も重要

---

## v05 - Dynamic State Routing

- Algorithm: Dijkstra（最小コスト経路）
- Feature:
  - ノード状態をステップごとにランダム変化
  - 各ステップでルートを再計算
  - 動的環境における経路選択の変化を確認

- Result:
  - 成功:
    - ノード状態の時間変化に応じてルートが動的に切り替わることを確認
    - WARNING 状態では短距離ルート維持、CONGESTED 状態では代替ルート切替の傾向を確認
    - 静的モデルで確認した挙動が動的シミュレーションでも再現された

  - 観察:
    - nodeD が CONGESTED の場合、下ルートへの切替が複数回確認された
    - 全体が軽負荷のときは上ルートが優先された
    - nodeA の状態変化は現在のコスト計算に直接反映されていない

  - 課題:
    - ノード状態変化が完全ランダムであり、現実的な負荷遷移モデルではない
    - start node の状態を評価対象に含めるか未検討
    - ステップ間の履歴やヒステリシス（過去状態の影響）は未導入
    - 候補ルートの比較理由はまだ自動表示されない

  - 次のステップ:
    - 状態遷移モデルをランダムから制御可能な形へ変更
    - 前回ルートとの比較表示を追加
    - ルート変更回数やノード使用率を集計
    - 判断理由ログを動的シミュレーションにも統合

  - 実行結果:
    ```
    === Dynamic Simulation ===

    --- Step 1 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: CONGESTED
      nodeD: WARNING
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 2 ---
    Node states:
      nodeA: CONGESTED
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: WARNING
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 12

    --- Step 3 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: WARNING
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

    --- Step 4 ---
    Node states:
      nodeA: WARNING
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 10

    --- Step 5 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

    --- Step 6 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: WARNING

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 7 ---
    Node states:
      nodeA: WARNING
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: WARNING
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 8 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

    --- Step 9 ---
    Node states:
      nodeA: WARNING
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: WARNING
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 10 ---
    Node states:
      nodeA: WARNING
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: CONGESTED

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 19
    ```

  - Insight:
    - PSCは静的な経路選択だけでなく、時間変化する状態に追従して再判断する制御モデルとして成立する可能性がある

---

## v06 - Dynamic Routing Analysis

- Algorithm: Dijkstra（最小コスト経路）
- Feature:
  - 動的シミュレーションに分析機能を追加
  - ルート変更回数を集計
  - ノード使用率を集計
  - ルート履歴を保存

- Result:
  - 成功:
    - 動的環境下でのルート履歴とノード使用率を取得可能
    - ルート変更頻度を定量的に評価可能
    - 分析フェーズとしての基本機能を確認

  - 観察:
    - 今回の実行ではルート変更回数は 0 回だった
    - 全ステップで nodeA -> nodeB -> nodeD -> nodeF が選択された
    - 下ルートは一度も選択されず、使用ノードが上ルート側に完全に偏った

  - 課題:
    - 現在のトポロジとコスト設定では上ルートが強すぎる
    - 動的状態変化があっても代替ルートを選ぶ条件が十分に発生しない
    - 分析結果が単一ルート固定になりやすく、比較評価が難しい

  - 次のステップ:
    - 下ルートのリンクコストを少し下げる
    - WARNING / CONGESTED のコスト差を再調整する
    - 特定ノード（例: nodeD）に意図的な高負荷を与えるテストを追加
    - ルート変更が起きやすいテストケースを別途用意する

  - 実行結果:
    ```
    === Dynamic Simulation + Analysis ===

    --- Step 1 ---
    Node states:
      nodeA: CONGESTED
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: WARNING
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 2 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: WARNING

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 3 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

    --- Step 4 ---
    Node states:
      nodeA: NORMAL
      nodeB: WARNING
      nodeC: NORMAL
      nodeD: WARNING
      nodeE: WARNING
      nodeF: WARNING

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 14

    --- Step 5 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: CONGESTED
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

    --- Step 6 ---
    Node states:
      nodeA: NORMAL
      nodeB: WARNING
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: CONGESTED
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 7 ---
    Node states:
      nodeA: CONGESTED
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: WARNING
      nodeE: WARNING
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 8 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: WARNING

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    --- Step 9 ---
    Node states:
      nodeA: WARNING
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

    --- Step 10 ---
    Node states:
      nodeA: CONGESTED
      nodeB: WARNING
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 10

    === Analysis Result ===

    Total route changes: 0

    Node usage count:
      nodeA: 10
      nodeB: 10
      nodeD: 10
      nodeF: 10

    Route history:
      Step 1: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 2: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 3: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 4: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 5: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 6: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 7: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 8: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 9: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 10: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
    ```

  - Insight:
    - PSCは状態変化があっても、コスト優位なルートを安定維持する傾向を示した
    - 一方で、経路切替の挙動を十分に評価するには、トポロジとコスト設定の再調整が必要

---

## v07 - Controlled Route Switching

- Algorithm: Dijkstra（最小コスト経路）
- Feature:
  - ノード状態をランダムではなく制御条件で変化
  - nodeD を周期的に CONGESTED 化
  - nodeC を周期的に WARNING 化
  - 意図的にルート切替が発生する条件を作成

- Result:
  - 成功:
    - ルート切替が意図通り発生することを確認
    - 条件に応じて上ルート / 下ルートが切り替わることを確認
    - Total route changes = 3 を記録

  - 観察:
    - 通常時は下ルート（nodeA -> nodeC -> nodeE -> nodeF）が優先された
    - nodeC が WARNING のとき、上ルートへ切り替わった
    - nodeD が CONGESTED のとき、下ルートへ戻る挙動が確認された
    - コスト条件を調整することで、経路選択の感度を制御できることが分かった

  - 課題:
    - 現在の切替条件は手動で設計しており、現実的な負荷モデルではない
    - 下ルートが通常時に優先される理由をさらに整理する必要がある
    - 頻繁な切替に対する安定化機構（ヒステリシス）は未導入

  - 次のステップ:
    - ヒステリシスを導入して不要なルート変更を抑制
    - 切替理由を毎回ログ出力する
    - 切替感度と安定性のバランスを評価する

  - 実行結果:
    ```
    === Controlled Switching Simulation ===

    --- Step 1 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    --- Step 2 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    --- Step 3 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    --- Step 4 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    --- Step 5 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 9
      → Route CHANGED

    --- Step 6 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
      → Route CHANGED

    --- Step 7 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    --- Step 8 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    --- Step 9 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    --- Step 10 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 9
      → Route CHANGED

    === Analysis ===
    Total route changes: 3

    Route history:
      Step 1: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 2: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 3: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 4: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 5: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 6: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 7: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 8: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 9: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 10: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
    ```

  - Insight:
    - PSCの経路切替挙動は、状態変化だけでなくコスト設定の設計によって大きく左右される
    - 経路切替を評価するには、ランダム負荷だけでなく制御されたテスト条件が有効

---

## v08 - Hysteresis Routing

- Algorithm: Dijkstra + Hysteresis（最小コスト経路 + 切替抑制）
- Feature:
  - 現在ルートを一定条件下で維持するヒステリシス機構を追加
  - Best route（計算上の最安ルート）と Selected route（採用ルート）を分離
  - 経路切替の安定化を試行

- Result:
  - 成功:
    - ヒステリシス付きの経路選択ロジックを実装
    - Best route と Selected route の比較表示を追加
    - 切替理由をログとして可視化

  - 観察:
    - 今回の実行では Best route と Selected route は全ステップで一致した
    - ヒステリシス機構は動作しているが、現在の閾値では切替抑制効果はほぼ現れなかった
    - ルート変更回数は v07 と同じ 3 回だった

  - 課題:
    - HYSTERESIS_MARGIN = 2 では差が小さすぎる可能性がある
    - 現在のコスト差では、切替判断がそのまま通りやすい
    - 「切り替えない」ケースを意図的に作る条件設計が必要

  - 次のステップ:
    - HYSTERESIS_MARGIN を引き上げて再実験
    - コスト差が小さい（接戦状態）ケースを作る
    - ヒステリシスが実際に route を保持する例を観測する

  - 実行結果:
    ```
    === Controlled Switching Simulation + Hysteresis ===

    --- Step 1 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Best route selected

    --- Step 2 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Best route selected

    --- Step 3 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Best route selected

    --- Step 4 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Best route selected

    --- Step 5 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 9

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 9
    Reason: Route changed (better route exceeded hysteresis margin)

    --- Step 6 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Route changed (better route exceeded hysteresis margin)

    --- Step 7 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Best route selected

    --- Step 8 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Best route selected

    --- Step 9 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: NORMAL
      nodeD: CONGESTED
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8

    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 8
    Reason: Best route selected

    --- Step 10 ---
    Node states:
      nodeA: NORMAL
      nodeB: NORMAL
      nodeC: WARNING
      nodeD: NORMAL
      nodeE: NORMAL
      nodeF: NORMAL

    Best computed route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 9

    Selected route:
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 9
    Reason: Route changed (better route exceeded hysteresis margin)

    === Analysis ===
    Total route changes: 3

    Route history:
      Step 1: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 2: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 3: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 4: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 5: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
      Step 6: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 7: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 8: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 9: ['nodeA', 'nodeC', 'nodeE', 'nodeF']
      Step 10: ['nodeA', 'nodeB', 'nodeD', 'nodeF']
    ```

  - Insight:
    - ヒステリシスは実装するだけでは十分な効果を発揮せず、閾値設計とコスト構造に強く依存する
    - PSCにおける安定化制御は、単純な最短経路計算とは別の設計問題として扱う必要がある

---

## v08b - Hysteresis Activation

- Algorithm: Dijkstra + Hysteresis（最小コスト経路 + 切替抑制強化）

- Feature:
  - HYSTERESIS_MARGIN を拡大（=3）
  - 小さなコスト差では経路を切替しない制御を導入
  - 「Keep current route（維持）」の明示ログを追加

- Result:
  - 成功:
    - ヒステリシスによる経路維持が発生
    - 「切り替えない」ケースを初めて観測
    - Best route と Selected route が分離される挙動を確認

  - 観察:
    - Step 5 にて、代替経路が出現したが current route を維持
    - Step 6 にて、同コストまたは近似コストの別経路が出現しても維持
    - ヒステリシスによる切替抑制が明確に可視化された
    - ヒステリシスによる「非最適でも維持する」挙動が確認された

  - 課題:
    - 維持中の current route のコストが再評価されていない
    - 状態変化が selected cost に反映されない問題あり
    - 同コスト維持とヒステリシス維持の区別が曖昧

  - 次のステップ:
    - current route のコストを毎ステップ再評価
    - reason logging の分類強化
    - 挙動の整合性改善（v08cへ）

  - 実行結果:
  ```
  === Controlled Switching Simulation + Hysteresis v08b ===
  Source: nodeA
  Destination: nodeF
  Hysteresis Margin: 3
  
  --- Step 1 ---
  Node states:
    nodeA: NORMAL
    nodeB: NORMAL
    nodeC: NORMAL
    nodeD: NORMAL
    nodeE: NORMAL
    nodeF: NORMAL
  
  Best computed route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  
  Selected route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  Reason: Initial route selected
  
  --- Step 2 ---
  Node states:
    nodeA: NORMAL
    nodeB: BUSY
    nodeC: NORMAL
    nodeD: NORMAL
    nodeE: NORMAL
    nodeF: NORMAL
  
  Best computed route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  
  Selected route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  Reason: Keep current route (same as best route)
  
  --- Step 3 ---
  Node states:
    nodeA: NORMAL
    nodeB: CONGESTED
    nodeC: NORMAL
    nodeD: NORMAL
    nodeE: NORMAL
    nodeF: NORMAL
  
  Best computed route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  
  Selected route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  Reason: Keep current route (same as best route)
  
  --- Step 4 ---
  Node states:
    nodeA: NORMAL
    nodeB: CONGESTED
    nodeC: BUSY
    nodeD: NORMAL
    nodeE: NORMAL
    nodeF: NORMAL
  
  Best computed route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
  
  Selected route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  Reason: Keep current route (same as best route)
  
  --- Step 5 ---
  Node states:
    nodeA: NORMAL
    nodeB: NORMAL
    nodeC: BUSY
    nodeD: NORMAL
    nodeE: NORMAL
    nodeF: NORMAL
  
  Best computed route:
    ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
  
  Selected route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  Reason: Keep current route (within hysteresis margin)
  Hysteresis check: current_cost=5, best_cost=6, margin=3
  
  --- Step 6 ---
  Node states:
    nodeA: NORMAL
    nodeB: NORMAL
    nodeC: NORMAL
    nodeD: BUSY
    nodeE: NORMAL
    nodeF: NORMAL
  
  Best computed route:
    ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
  
  Selected route:
    ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
  Reason: Keep current route (within hysteresis margin)
  Hysteresis check: current_cost=5, best_cost=5, margin=3
  ```

---

## v08c - Cost Consistency & Logging Improvement

- Algorithm: Dijkstra + Hysteresis（コスト再評価 + ログ改善）

- Feature:
  - current route のコストを毎ステップ再計算
  - selected route の cost を現在状態に同期
  - reason logging を詳細化
  - decision check（判定条件ログ）を追加

- Result:
  - 成功:
    - current route のコスト再評価が正常動作
    - 状態変化がルーティングコストに正しく反映
    - ログの一貫性と解釈性が向上

  - 観察:
    - Step 4 にて、current route cost が 5 → 7 に変化（状態反映）
    - Step 5 にて、best cost 6 に対して current cost 7 だが維持
    - Step 6 にて、best cost 5 に対しても改善幅不足により維持
    - 全体として安定寄り（保守的）な挙動を示す
    - 改善幅が閾値未満の場合、切替が明確に抑制されることを確認

  - 課題:
    - HYSTERESIS_MARGIN = 3 ではやや抑制が強い
    - 中程度の改善でも切替が発生しないケースあり
    - equal-cost alternative の観測は未確認

  - 次のステップ:
    - HYSTERESIS_MARGIN の再調整（3 → 2）
    - 改善量ベース or 比率ベースのヒステリシス導入検討
    - v08d でポリシー制御の進化へ
    
  - 実行結果:
   ```
   === Controlled Switching Simulation + Hysteresis v08c ===
   Source: nodeA
   Destination: nodeF
   Hysteresis Margin: 3
   
   --- Step 1 ---
   Node states:
     nodeA: NORMAL
     nodeB: NORMAL
     nodeC: NORMAL
     nodeD: NORMAL
     nodeE: NORMAL
     nodeF: NORMAL
   
   Best computed route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   
   Selected route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   Reason: Initial route selected
   
   --- Step 2 ---
   Node states:
     nodeA: NORMAL
     nodeB: BUSY
     nodeC: NORMAL
     nodeD: NORMAL
     nodeE: NORMAL
     nodeF: NORMAL
   
   Best computed route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   
   Current route re-evaluated:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   
   Selected route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   Reason: Keep current route (same as best route)
   
   --- Step 3 ---
   Node states:
     nodeA: NORMAL
     nodeB: CONGESTED
     nodeC: NORMAL
     nodeD: NORMAL
     nodeE: NORMAL
     nodeF: NORMAL
   
   Best computed route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   
   Current route re-evaluated:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   
   Selected route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
   Reason: Keep current route (same as best route)
   
   --- Step 4 ---
   Node states:
     nodeA: NORMAL
     nodeB: CONGESTED
     nodeC: BUSY
     nodeD: NORMAL
     nodeE: NORMAL
     nodeF: NORMAL
   
   Best computed route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
   
   Current route re-evaluated:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
   
   Selected route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
   Reason: Keep current route (same as best route)
   
   --- Step 5 ---
   Node states:
     nodeA: NORMAL
     nodeB: NORMAL
     nodeC: BUSY
     nodeD: NORMAL
     nodeE: NORMAL
     nodeF: NORMAL
   
   Best computed route:
     ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
   
   Current route re-evaluated:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
   
   Selected route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
   Reason: Keep current route (within hysteresis margin)
   Decision check: current_cost=7, best_cost=6, margin=3
   
   --- Step 6 ---
   Node states:
     nodeA: NORMAL
     nodeB: NORMAL
     nodeC: NORMAL
     nodeD: BUSY
     nodeE: NORMAL
     nodeF: NORMAL
   
   Best computed route:
     ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
   
   Current route re-evaluated:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
   
   Selected route:
     ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
   Reason: Keep current route (within hysteresis margin)
   Decision check: current_cost=7, best_cost=5, margin=3
   ```

---

## Overall Insight

- PSC Routing は単なる最短経路探索ではなく、
  状態・履歴・制御ポリシーを含む制御システムとして設計されるべきである
- ヒステリシスは経路安定化に有効だが、
  閾値設計によって挙動が大きく変化する
- 今後はポリシー制御や適応型制御への拡張が必要
