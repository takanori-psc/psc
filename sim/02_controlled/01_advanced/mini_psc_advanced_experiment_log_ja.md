## v08d - Policy-aware Routing

- Algorithm: Cost-based route selection + Hysteresis + Policy

- Feature:
  - ルーティング判断に policy を導入
  - 同じ状態でも policy によって Selected route が変化
  - hysteresis margin を policy ごとに切替
  - stability / latency の2モードを比較

- Result:
  - 成功:
    - policy による挙動分岐を実装
    - 同一条件で異なる route selection を確認
    - PSC Routing に意思決定レイヤを導入

  - 観察:
    - stability policy では current route の維持が優先された
    - latency policy では better route を即時採用した
    - Step 5 / Step 6 にて、両 policy の差が明確に観測された
    - hysteresis は固定機構ではなく、policy に従う制御要素として機能した

  - 課題:
    - policy は固定設定であり動的切替が未実装
    - policy decision の優先順位設計は未整理
    - より複雑な topology での差分確認が必要

  - 次のステップ:
    - adaptive policy の導入
    - ratio-based hysteresis の導入
    - Resolver との接続を意識した設計へ拡張

- 実行結果:

### v08d - Policy: stability (Execution Log)

```text
Policy: stability
Step 5: KEEP
Step 6: KEEP

=== Policy-aware Routing Simulation v08d ===
Source: nodeA
Destination: nodeF
Policy: stability
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
    Decision: SELECT
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
    Decision: KEEP
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
    Decision: KEEP
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
    Decision: KEEP
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
    Decision: KEEP
    Reason: Keep current route (within policy margin)
    Policy check: current_cost=7, best_cost=6, margin=3, policy=stability
    
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
    Decision: KEEP
    Reason: Keep current route (within policy margin)
    Policy check: current_cost=7, best_cost=5, margin=3, policy=stability
    
```

---

### v08d - Policy: latency (Execution Log)

```text
Policy: latency
Step 5: SWITCH
Step 6: SWITCH

=== Policy-aware Routing Simulation v08d ===
Source: nodeA
Destination: nodeF
Policy: latency
Hysteresis Margin: 0
    
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
    Decision: SELECT
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
    Decision: KEEP
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
    Decision: KEEP
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
    Decision: KEEP
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
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
    Decision: SWITCH
    Reason: Switch route (better route found under latency policy)
    Policy check: current_cost=7, best_cost=6, margin=0, policy=latency
    
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
      ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
    
    Selected route:
      ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
    Decision: SWITCH
    Reason: Switch route (better route found under latency policy)
    Policy check: current_cost=8, best_cost=5, margin=0, policy=latency
```

- Insight:
  - PSC Routing は最短経路問題ではなく、
    policy によって最適性の定義が変化する制御問題である

---

## v09 - Policy-aware Routing + Resolver Escalation

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation

- Feature:
  - stability / latency の policy 構造を維持
  - Resolver の必要時介入条件を追加
  - improvement threshold に基づく escalation を導入
  - local policy decision と resolver decision の役割を分離

- Result:
  - 成功:
    - Resolver が常時介入せず、必要時のみ介入する構造を実装
    - stability policy 下でも改善幅が十分な場合に route switch が発生することを確認
    - policy layer と resolver layer の二層制御の基本挙動を確認

  - 観察:
    - Step 5 では improvement = 1 のため Resolver は介入せず KEEP
    - Step 6 では improvement = 2 に達し Resolver が介入して ESCALATE_SWITCH
    - hysteresis により local policy は keep 寄りに動作しつつ、
      resolver が一定条件で上位判断を行う構造が成立した
    - PSC Routing は単純な policy routing ではなく、
      local stability と higher-level intervention を組み合わせた制御モデルへ拡張可能であることを確認した

  - 課題:
    - Resolver reason のログ表現がまだ粗い
    - improvement threshold は固定値であり動的化されていない
    - trust / untrusted 制約をまだ統合していない
    - Resolver の介入条件優先順位は今後整理が必要

  - 次のステップ:
    - v09a としてログ表現を整理
    - trusted / untrusted path 制約の追加
    - adaptive threshold / adaptive policy の検討
    - より複雑な topology での再検証

- 実行結果:

### v09 - Policy: stability (Execution Log)

```text
Policy: stability
Step 5: KEEP
Step 6: ESCALATE_SWITCH

=== Policy-aware Routing Simulation v09 ===
Source: nodeA
Destination: nodeF
Policy: stability
Hysteresis Margin: 3
Resolver improvement threshold: 2

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
Decision: SELECT
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
Decision: KEEP
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
Decision: KEEP
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
Decision: KEEP
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
Decision: KEEP
Reason: No escalation
Policy check: current_cost=7, best_cost=6, margin=3, policy=stability

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
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: ESCALATE_SWITCH
Reason: Escalate: improvement 2 >= threshold 2
Policy check: current_cost=7, best_cost=5, margin=3, policy=stability
```

---

## v09a - Policy-aware Routing + Resolver Escalation (Log-refined)

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation

- Feature:
  - stability / latency の policy 構造を維持
  - Resolver の必要時介入条件を追加
  - improvement threshold に基づく escalation を導入
  - policy phase / resolver phase / final reason を分離してログ出力
  - local policy decision と resolver decision の役割を明示

- Result:
  - 成功:
    - Resolver が常時介入せず、必要時のみ介入する構造を実装
    - stability policy 下でも improvement が threshold に達した場合に route switch が発生することを確認
    - policy layer と resolver layer の二層制御の基本挙動を、説明可能なログ形式で確認

  - 観察:
    - Step 5 では improvement = 1 のため Resolver は介入せず KEEP
    - Step 6 では improvement = 2 に達し Resolver が介入して ESCALATE_SWITCH
    - hysteresis により local policy は keep 寄りに動作しつつ、
      resolver が一定条件で上位判断を行う構造が成立した
    - PSC Routing は単純な shortest path 制御ではなく、
      local stability と higher-level intervention を組み合わせた hierarchical control に拡張可能であることを確認した

  - 課題:
    - latency policy 側での v09a 比較ログは未取得
    - improvement threshold は固定値であり動的化されていない
    - trusted / untrusted 制約をまだ統合していない
    - Resolver の介入条件優先順位は今後整理が必要

  - 次のステップ:
    - latency policy でも v09a ログを取得して比較
    - trusted / untrusted path 制約の追加
    - adaptive threshold / adaptive policy の検討
    - より複雑な topology での再検証

- 実行結果:

### v09a - Policy: stability (Execution Log)

```text
Policy: stability
Step 5: KEEP
Step 6: ESCALATE_SWITCH

=== Policy-aware Routing Simulation v09a ===
Source: nodeA
Destination: nodeF
Policy: stability
Hysteresis Margin: 3
Resolver improvement threshold: 2

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
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial route selected

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
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Decision: KEEP
Policy phase: improvement=1, margin=3 -> within hysteresis, keep current route
Resolver phase: improvement=1 < threshold=2 -> no escalation
Final reason: Keep current route
Policy check: current_cost=7, best_cost=6, margin=3, improvement=1, policy=stability

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
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: ESCALATE_SWITCH
Policy phase: improvement=2, margin=3 -> within hysteresis, keep current route
Resolver phase: improvement=2 >= threshold=2 -> escalate
Final reason: Resolver switched to better route
Policy check: current_cost=7, best_cost=5, margin=3, improvement=2, policy=stability
```

- Insight:
  - PSC Routing は local policy のみによる制御ではなく、
    必要時のみ上位判断を行う hierarchical control へ拡張できる
  - hysteresis による安定性維持と、
    Resolver による条件付き介入は両立可能である

---

### v09a - Policy: latency (Execution Log)

```text
Policy: latency
Step 5: SWITCH
Step 6: SWITCH

=== Policy-aware Routing Simulation v09a ===
Source: nodeA
Destination: nodeF
Policy: latency
Hysteresis Margin: 0
Resolver improvement threshold: 2

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
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial route selected

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
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SWITCH
Policy phase: improvement=1, margin=0 -> switch under latency policy
Resolver phase: not used
Final reason: Switch route under latency policy
Policy check: current_cost=7, best_cost=6, margin=0, improvement=1, policy=latency

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
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: SWITCH
Policy phase: improvement=3, margin=0 -> switch under latency policy
Resolver phase: not used
Final reason: Switch route under latency policy
Policy check: current_cost=8, best_cost=5, margin=0, improvement=3, policy=latency
```

- Insight:
    - latency policy では better route が見つかった時点で policy phase が即時に switch を決定し、
      Resolver は判断に関与しない

    - v09a により、stability policy と latency policy で
      local policy layer と resolver layer の役割分担が変化することを確認できた

- Next:
    - v10: trusted / untrusted を導入し、prefer_trusted policy で route selection を拡張する

---

## v10 - Trust-aware Route Selection (prefer_trusted)

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection

- Feature:
  - trusted / untrusted 属性をノードに導入
  - trust-aware route filtering を追加
  - `TRUST_MODE = prefer_trusted` により、trusted path を優先選択
  - trusted path が存在する場合、untrusted path より trust 条件を優先
  - trust phase / policy phase / resolver phase を分離してログ出力

- Result:
  - 成功:
    - trusted / untrusted を用いた経路制約を実装
    - `prefer_trusted` により trusted path が優先されることを確認
    - trust phase が route selection の最上流で動作することを確認
    - trust 制約により routing behavior が安定化するケースを確認

  - 観察:
    - Step 1 から Step 6 まで一貫して `A-B-D-F` が選択された
    - `A-C-D-F` や `A-C-E-F` は untrusted node を含むため候補として優先されなかった
    - trust phase が route 候補を先に絞るため、policy / resolver の出番が大きく減少した
    - trust 制約は route flexibility を下げる一方で、routing stability を高める効果を持つ可能性がある

  - 課題:
    - trusted path が実質一択となり、route variation が観測しにくい
    - policy / resolver の差分が trust phase に隠れやすい
    - trust 条件が強すぎる場合の柔軟性低下をどう扱うか未整理
    - `require_trusted` や trusted route 不在時の挙動は未検証

  - 次のステップ:
    - v10a としてログ表現を整理
    - trust 条件を変えて route variation が出るケースを再実験
    - `nodeD` を untrusted にするなど、trusted path 固定を崩す条件を試す
    - `require_trusted` モードの挙動を検証する

- 実行結果:

### v10 - Policy: stability / Trust mode: prefer_trusted (Execution Log)

```text
Policy: stability
Trust mode: prefer_trusted

=== Policy-aware Routing Simulation v10 ===
Source: nodeA
Destination: nodeF
Policy: stability
Trust mode: prefer_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: TRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Trust phase: prefer_trusted -> selected best trusted route
Trusted path: True

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial route selected

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Trust phase: prefer_trusted -> selected best trusted route
Trusted path: True

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Trusted path: True

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 11
Trust phase: prefer_trusted -> selected best trusted route
Trusted path: True

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 11
Trusted path: True

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 11
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 11
Trust phase: prefer_trusted -> selected best trusted route
Trusted path: True

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 11
Trusted path: True

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 11
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Trust phase: prefer_trusted -> selected best trusted route
Trusted path: True

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Trusted path: True

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: BUSY
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Trust phase: prefer_trusted -> selected best trusted route
Trusted path: True

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Trusted path: True

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
```

- Insight:
    - trust-aware route selection は policy / resolver より前段で route 候補を絞り込む
    - `prefer_trusted` により trusted path が固定されると、routing behavior はむしろ安定化する
    - trust 制約は安全性だけでなく、routing の揺れを抑える制御要素としても機能しうる

- Next:
    - v10a: trust phase のログ表現整理
    - trusted path が固定されすぎない条件を作り、route variation を再観測する

---

## v10a - Trust-aware Route Selection (prefer_trusted fallback)

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection

- Feature:
  - trusted / untrusted 属性をノードに導入
  - `TRUST_MODE = prefer_trusted` を維持
  - v10a では trusted path 固定を崩すため、`nodeD` を untrusted に変更
  - trusted path 不在時の fallback behavior を確認
  - trust phase / policy phase / resolver phase を分離してログ出力

- Result:
  - 成功:
    - trusted path が存在しない場合に `prefer_trusted` が untrusted route へ fallback することを確認
    - trust phase が使えない状況では、policy / resolver 層が再び routing decision の中心になることを確認
    - v10 と v10a の比較により、trust 制約の強さが routing stability と flexibility を変化させることを確認

  - 観察:
    - 全ステップで `Trusted candidates: 0` となり、trusted path は存在しなかった
    - trust phase は常に `fallback to untrusted route` を返した
    - Step 5 では improvement = 1 のため policy / resolver ともに KEEP
    - Step 6 では improvement = 2 に達し Resolver が介入して ESCALATE_SWITCH
    - 挙動全体は v09a (stability) に近く、trusted path 不在時には trust layer の影響が後退することが分かった

  - 課題:
    - trusted path が 0 のケースでは trust-aware routing の差分が薄くなり、通常 routing に近づく
    - fallback 時の優先度や penalty 設計は未導入
    - `require_trusted` モードでの no-route behavior は未検証
    - latency policy と組み合わせた fallback behavior も未検証

  - 次のステップ:
    - latency policy で v10a を実行し、fallback + latency の挙動を確認する
    - `require_trusted` モードで trusted route 不在時の挙動を確認する
    - fallback 時の penalty や trust weight の導入を検討する
    - trust / policy / resolver の優先順位整理を進める

- 実行結果:

### v10a - Policy: stability / Trust mode: prefer_trusted (Execution Log)

```text
Policy: stability
Trust mode: prefer_trusted

=== Policy-aware Routing Simulation v10a ===
Source: nodeA
Destination: nodeF
Policy: stability
Trust mode: prefer_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: UNTRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial route selected

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Decision: KEEP
Policy phase: improvement=1, margin=3 -> within hysteresis, keep current route
Resolver phase: improvement=1 < threshold=2 -> no escalation
Final reason: Keep current route
Policy check: current_cost=7, best_cost=6, margin=3, improvement=1, policy=stability

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: ESCALATE_SWITCH
Policy phase: improvement=2, margin=3 -> within hysteresis, keep current route
Resolver phase: improvement=2 >= threshold=2 -> escalate
Final reason: Resolver switched to better route
Policy check: current_cost=7, best_cost=5, margin=3, improvement=2, policy=stability
```
- Insight:
    - trusted path が存在しない場合、prefer_trusted は untrusted route への fallback として機能する
    - trust layer が使えない状況では、routing decision は再び policy / resolver 層へ戻る
    - v10 と v10a の比較により、trust 制約は routing の安定性と柔軟性の両方に強く影響することを確認できた

- Next:
    - v10a の latency policy 実験を追加し、fallback + latency の挙動を確認する

---

### v10a - Policy: latency / Trust mode: prefer_trusted (Execution Log)

```text
Policy: latency
Trust mode: prefer_trusted

=== Policy-aware Routing Simulation v10a ===
Source: nodeA
Destination: nodeF
Policy: latency
Trust mode: prefer_trusted
Hysteresis Margin: 0
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: UNTRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial route selected

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 5
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 7
Trusted path: False

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SWITCH
Policy phase: improvement=1, margin=0 -> switch under latency policy
Resolver phase: not used
Final reason: Switch route under latency policy
Policy check: current_cost=7, best_cost=6, margin=0, improvement=1, policy=latency

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
Trust phase: prefer_trusted -> no trusted route available, fallback to untrusted route
Trusted candidates: 0
Untrusted candidates: 4
Trusted path: False

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Trusted path: False

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: SWITCH
Policy phase: improvement=3, margin=0 -> switch under latency policy
Resolver phase: not used
Final reason: Switch route under latency policy
Policy check: current_cost=8, best_cost=5, margin=0, improvement=3, policy=latency
```
- Insight:
    - trusted path 不在時、prefer_trusted は untrusted route への fallback として機能する
    - latency policy では fallback 後の routing decision は policy phase が即時に主導し、Resolver は関与しない
    - v10a により、trust unavailable 状態では policy 設定の違いが再び routing behavior を大きく左右することを確認できた

---

## v10b - Trust-aware Route Selection (require_trusted / no-route case)

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection

- Feature:
  - trusted / untrusted 属性をノードに導入
  - `TRUST_MODE = require_trusted` を適用
  - trusted path が存在しない場合は fallback を許可しない
  - trust phase / policy phase / resolver phase を分離してログ出力
  - no-route case を明示的に扱う

- Result:
  - 成功:
    - `require_trusted` により trusted path が必須条件として機能することを確認
    - trusted path 不在時に routing が `NO_ROUTE` となることを確認
    - trust layer が下位の policy / resolver より前段で routing 可否を決定することを確認

  - 観察:
    - 全ステップで `Trusted candidates: 0` となり、trusted path は存在しなかった
    - trust phase は常に `require_trusted -> no trusted route available` を返した
    - すべてのステップで `Decision: NO_ROUTE` となった
    - policy / resolver 層は routing 候補が存在しないため判断に関与しなかった
    - `require_trusted` は routing quality の制御ではなく、routing 可否そのものを制御する強い制約であることが分かった

  - 課題:
    - strict trust 制約は到達性を失わせる可能性がある
    - trusted path 不在時の代替動作は未設計
    - Resolver による trust constraint 緩和や例外処理は未実装
    - 実運用では `NO_ROUTE` 時の復旧方針や policy fallback が必要になる可能性がある

  - 次のステップ:
    - `POLICY = stability` でも同条件を確認し、`require_trusted` が policy 非依存で `NO_ROUTE` になるか確認する
    - trusted route 不在時に Resolver が constraint relaxation を提案する設計を検討する
    - `prefer_trusted` + penalty 方式との比較を行う
    - trust 制約違反時の degraded mode / emergency mode を検討する

- 実行結果:

### v10b - Policy: latency / Trust mode: require_trusted (Execution Log)

```text
Policy: latency
Trust mode: require_trusted

=== Policy-aware Routing Simulation v10b ===
Source: nodeA
Destination: nodeF
Policy: latency
Trust mode: require_trusted
Hysteresis Margin: 0
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: UNTRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  None | Cost: inf
Trust phase: require_trusted -> no trusted route available
Trusted candidates: 0
Untrusted candidates: 4

Selected route:
  None | Cost: None
Decision: NO_ROUTE
Policy phase: no candidate route available
Resolver phase: not used
Final reason: No route available under current trust mode

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  None | Cost: inf
Trust phase: require_trusted -> no trusted route available
Trusted candidates: 0
Untrusted candidates: 4

Selected route:
  None | Cost: None
Decision: NO_ROUTE
Policy phase: no candidate route available
Resolver phase: not used
Final reason: No route available under current trust mode

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  None | Cost: inf
Trust phase: require_trusted -> no trusted route available
Trusted candidates: 0
Untrusted candidates: 4

Selected route:
  None | Cost: None
Decision: NO_ROUTE
Policy phase: no candidate route available
Resolver phase: not used
Final reason: No route available under current trust mode

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  None | Cost: inf
Trust phase: require_trusted -> no trusted route available
Trusted candidates: 0
Untrusted candidates: 4

Selected route:
  None | Cost: None
Decision: NO_ROUTE
Policy phase: no candidate route available
Resolver phase: not used
Final reason: No route available under current trust mode

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  None | Cost: inf
Trust phase: require_trusted -> no trusted route available
Trusted candidates: 0
Untrusted candidates: 4

Selected route:
  None | Cost: None
Decision: NO_ROUTE
Policy phase: no candidate route available
Resolver phase: not used
Final reason: No route available under current trust mode

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: BUSY
  nodeE: NORMAL
  nodeF: NORMAL

Best computed route:
  None | Cost: inf
Trust phase: require_trusted -> no trusted route available
Trusted candidates: 0
Untrusted candidates: 4

Selected route:
  None | Cost: None
Decision: NO_ROUTE
Policy phase: no candidate route available
Resolver phase: not used
Final reason: No route available under current trust mode
```
- Insight:
    - require_trusted は trust 制約を routing の優先条件ではなく必須条件として扱う
    - trusted path が存在しない場合、routing は fallback せず NO_ROUTE になる
    - trust layer が strict mode になると、policy / resolver より前段で system behavior を停止させうる

---

## v11 - Trust Failure Handling + Resolver-managed Degraded Fallback

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection + Trust Failure Recovery

- Feature:
  - `TRUST_MODE = require_trusted` を通常モードとして維持
  - trusted path 不在時に trust failure を明示
  - Resolver が必要時のみ介入
  - operation mode を `NORMAL` から `DEGRADED` へ遷移
  - untrusted fallback を一時許可
  - trust failure / resolver override / degraded mode / fallback reason をログ出力

- Result:
  - 成功:
    - strict trust constraint 下での trust failure を明示的に検出できる構造を導入
    - trusted path 不在時に Resolver-managed degraded fallback を行う基本動作を実装
    - `require_trusted` による停止を、制御付き例外処理へ拡張する方向性を確認
    - trust / policy / resolver に加えて operational recovery の層を導入した

  - 観察:
    - 全ステップで primary route search は `TRUSTED_ONLY` 条件下で `NO ROUTE` となった
    - trust failure 発生後、Resolver は override を有効化し untrusted fallback を許可した
    - Step 1 で operation mode は `NORMAL -> DEGRADED` に遷移した
    - degraded mode 維持下でも route re-selection は継続し、
      Step 5 / Step 6 で fallback route の切り替えが発生した
    - v10b の `NO_ROUTE` は、v11 では controlled degraded recovery に変換できることを確認した

  - 課題:
    - degraded mode 中の route switching は現状 fallback route の再選択が優先されており、
      stability / latency policy の適用境界がまだ粗い
    - degraded mode 解除条件は未実装
    - fallback 許可条件は現在単純ルールであり、policy ごとの厳密化が未実装
    - fallback route に対する penalty や trust weight は未導入

- 次のステップ:
    - degraded mode 中に policy / resolver をどう再適用するか整理する
    - degraded mode から normal mode への復帰条件を追加する
    - fallback route に penalty / trust weight を導入する
    - stability / latency の差分が degraded mode 中にどう表れるかを明確化する

### v11 - Policy: stability / Trust mode: require_trusted (Execution Log)

```text
=== Policy-aware Routing Simulation v11 ===
Source: nodeA
Destination: nodeF
Policy: stability
Initial trust mode: require_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: UNTRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: SELECT
Policy phase: initial selection after degraded fallback
Resolver phase: override enabled
Final reason: degraded fallback route selected
Fallback reason: preserve connectivity

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=3, improvement=0, policy=stability

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=3, improvement=0, policy=stability

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: BUSY
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=8, best_cost=5, margin=3, improvement=3, policy=stability
```

- Insight:
    - strict trust constraint は system を `NO_ROUTE` に到達させうる
    - v11 では Resolver-managed degraded fallback により、
      trust failure を停止ではなく制御付き例外処理として扱える
    - PSC Routing は route selection だけでなく、
      trust constraint violation 時の operational recovery へ拡張される
    - degraded mode 導入により、到達性維持と制御継続を両立できる可能性が見えた

---

### v11 - Policy: latency / Trust mode: require_trusted (Execution Log)

```text
Policy: latency
Trust mode: require_trusted

=== Policy-aware Routing Simulation v11 ===
Source: nodeA
Destination: nodeF
Policy: latency
Initial trust mode: require_trusted
Hysteresis Margin: 0
Resolver improvement threshold: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: UNTRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: SELECT
Policy phase: initial selection after degraded fallback
Resolver phase: override enabled
Final reason: degraded fallback route selected
Fallback reason: preserve connectivity

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=0, improvement=0, policy=latency

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 4
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=4, best_cost=4, margin=0, improvement=0, policy=latency

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=0, improvement=0, policy=latency

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=6, best_cost=6, margin=0, improvement=0, policy=latency

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: BUSY
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 5
Decision: DEGRADED_SWITCH
Policy phase: trust failure forced degraded fallback path selection
Resolver phase: override enabled
Final reason: Switched to degraded fallback route
Degraded mode: ACTIVE
Fallback reason: preserve connectivity
Policy check: current_cost=8, best_cost=5, margin=0, improvement=3, policy=latency
```

- Insight:
    - v11 では stability / latency の両 policy で trust failure recovery が成立することを確認した
    - degraded mode では trust failure recovery が優先されるため、
      policy 差分は route quality の最適化よりも fallback 後の再選択挙動に表れやすい
    - v11 の主眼は policy 比較だけでなく、trust violation 下でも制御継続できる operational recovery の確認にある

---

## v12 - Degraded Mode Policy Refinement

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection + Trust Failure Recovery + Degraded Mode Policy Refinement

- Feature:
  - `TRUST_MODE = require_trusted` を維持
  - trusted route 不在時に trust failure を検出
  - Resolver により degraded fallback を許可
  - degraded mode 専用の switching margin を導入
  - untrusted fallback route に penalty を導入
  - trusted route が一定ステップ連続で復帰した場合、`DEGRADED -> NORMAL` へ戻る recovery 条件を追加
  - degraded mode 中にも stability / latency とは別の判断境界を持たせる構造を導入

- Result:
  - 成功:
    - degraded mode 専用の route switching policy を導入できた
    - untrusted fallback route に対して penalty を付与する基本構造を実装できた
    - trusted route 復帰時に `DEGRADED -> NORMAL` へ戻る recovery 制御を実装できた
    - trust failure / degraded fallback / degraded switching / normal recovery を一連の制御フローとして表現できた

  - 観察:
    - Step 1 / Step 2 では trusted route `A-B-D-F` が選択され、通常の NORMAL mode routing として動作した
    - Step 3 では trusted route が失われ、trust failure 検出後に Resolver が override を有効化し、`NORMAL -> DEGRADED` へ遷移した
    - Step 3 では fallback penalty を含めても improvement が大きく、degraded mode policy により `A-C-E-F` へ `DEGRADED_SWITCH` が発生した
    - Step 4 では fallback 候補が変化したが improvement が 0 のため KEEP となり、degraded mode 専用の switching 境界が機能した
    - Step 5 では trusted route が再び利用可能になったが、recovery counter が 1/2 のため即時復帰はせず、degraded mode を維持したまま better route へ切り替えた
    - Step 6 では trusted route availability が 2 step 連続となり、`DEGRADED -> NORMAL` の recovery が発生した
    - v11 では degraded mode に入ると fallback reselection が優先されやすかったが、v12 では degraded mode 内にも独立した switching policy と recovery condition を持たせる方向性を確認できた

  - 課題:
    - fallback penalty は固定値であり、trust severity や node risk に応じた可変化は未実装
    - recovery 条件は単純な consecutive step 条件であり、安定性評価としてはまだ粗い
    - degraded mode 中に trusted route が復帰した際の優先順位設計はさらに精密化の余地がある
    - latency policy 側で degraded switch margin / recovery 条件がどう振る舞うかは未確認

  - 次のステップ:
    - fallback penalty を trust weight / risk weight に拡張する
    - degraded recovery 条件を throughput / stability / trust confidence に基づいて高度化する
    - latency policy でも v12 を実行し、degraded mode 中の挙動差を比較する
    - degraded mode を単なる例外状態ではなく、制御された運用モードとして定義していく

- 実行結果:

### v12 - Policy: stability / Trust mode: require_trusted (Execution Log)

```text
=== Policy-aware Routing Simulation v12 ===
Source: nodeA
Destination: nodeF
Policy: stability
Initial trust mode: require_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2
Degraded switch margin: 2
Degraded fallback penalty: 2
Recovery required steps: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: TRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial trusted route selected

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=8, best_cost=8, margin=3, improvement=0, policy=stability, operation_mode=NORMAL

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: CONGESTED
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 16

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
Decision: DEGRADED_SWITCH
Policy phase: improvement=9, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=16, best_cost=7, margin=3, improvement=9, policy=stability, operation_mode=DEGRADED

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: CONGESTED
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Action: enable untrusted fallback
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 9
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9
Decision: KEEP
Policy phase: no improvement
Resolver phase: degraded mode policy applied
Final reason: Keep current degraded route
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=9, margin=3, improvement=0, policy=stability, operation_mode=DEGRADED

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 1/2
  Recovery decision: STAY_DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: improvement=3, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=6, margin=3, improvement=3, policy=stability, operation_mode=DEGRADED

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 2/2
  Recovery decision: RESTORE_NORMAL
  Operation mode: DEGRADED -> NORMAL

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability, operation_mode=NORMAL
```
- Insight:
    - v12 では degraded mode が単なる fallback 状態ではなく、
       専用の switching margin と recovery condition を持つ制御モードとして扱われ始めた
    - trust failure 時にも到達性を維持しつつ、
      trusted route 復帰後には normal mode へ戻る運用が可能になった
    - fallback penalty の導入により、
      untrusted route を完全禁止ではなく「不利な候補」として扱う方向性が見えた
    - PSC Routing は route selection / trust control / resolver intervention に加えて、
      operational mode transition を含む多層制御へ拡張されつつある

---

## v12c - Degraded Mode Policy Boundary Comparison

- Algorithm: Cost-based route selection + Hysteresis + Policy + Resolver Escalation + Trust-aware Route Selection + Trust Failure Recovery + Degraded Mode Boundary Comparison

- Feature:
  - `TRUST_MODE = require_trusted` を維持
  - trusted route 不在時に trust failure を検出
  - Resolver override により degraded fallback を許可
  - degraded mode 内で policy boundary の差を比較するための境界ケースを導入
  - Step 4 において improvement = 1 の比較条件を意図的に生成
  - stability policy と latency policy が degraded mode で異なる判断を示すかを検証
  - degraded mode 中の route switching と normal recovery の流れを継続して確認

- Result:
  - 成功:
    - degraded mode 中の policy boundary 差を明示できた
    - Step 4 で improvement = 1 の条件を生成できた
    - stability policy では小さな改善に対して KEEP を維持した
    - latency policy では同一条件で `DEGRADED_SWITCH` を実行した
    - degraded mode においても policy の性格差が実際の route switching に反映されることを確認できた

  - 観察:
    - Step 3 では trust failure 検出後、Resolver override により `NORMAL -> DEGRADED` が発生し、fallback route `A-C-E-F` が選択された
    - v12c / stability の Step 4 では `current_cost = 9`, `best_cost = 8`, `improvement = 1` となり、`degraded_margin = 2` のため KEEP となった
    - v12c / latency の Step 4 では同じく `current_cost = 9`, `best_cost = 8`, `improvement = 1` だったが、`degraded_margin = 0` のため `DEGRADED_SWITCH` が発生した
    - これにより、degraded mode 中でも stability は小幅改善では current route を維持し、latency は小幅改善でも即時に better route へ切り替えることを確認できた
    - Step 5 / Step 6 では trusted route の復帰と `DEGRADED -> NORMAL` recovery も継続して正常に動作した
    - v12 で導入した degraded mode が、v12c では単なる fallback 状態ではなく policy-sensitive control mode として扱えることが示された

  - 課題:
    - fallback penalty は依然として固定値であり、trust severity や route risk に応じた動的重み付けは未実装
    - recovery 条件は連続ステップ数ベースであり、throughput や trust confidence を考慮した高度化の余地がある
    - 今回の差分は単一の境界ケースであり、複数の負荷パターンやより複雑な topology での再確認が必要
    - degraded mode の route comparison に trust weight / risk weight を導入した場合の policy 差は今後の検証対象

  - 次のステップ:
    - fallback penalty を adaptive trust weight / risk weight に拡張する
    - degraded recovery 条件を throughput / stability / trust confidence を含む形に高度化する
    - より複雑なトポロジや複数候補ルート条件で degraded policy boundary を検証する
    - v13 では trust / risk weighting を導入し、fallback route 評価を固定 penalty から拡張する

- 実行結果:

### v12c - Policy: stability / Trust mode: require_trusted (Execution Log)

```text
=== Policy-aware Routing Simulation v12c ===
Source: nodeA
Destination: nodeF
Policy: stability
Initial trust mode: require_trusted
Hysteresis Margin: 3
Resolver improvement threshold: 2
Degraded switch margin: 2
Degraded fallback penalty: 2
Recovery required steps: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: TRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial trusted route selected

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=8, best_cost=8, margin=3, improvement=0, policy=stability, operation_mode=NORMAL

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: CONGESTED
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 16

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
Decision: DEGRADED_SWITCH
Policy phase: improvement=9, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=16, best_cost=7, margin=3, improvement=9, policy=stability, operation_mode=DEGRADED

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: CONGESTED
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9
Decision: KEEP
Policy phase: improvement=1, degraded_margin=2 -> within degraded margin
Resolver phase: degraded mode policy applied
Final reason: Keep current degraded route
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=8, margin=3, improvement=1, policy=stability, operation_mode=DEGRADED

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 1/2
  Recovery decision: STAY_DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: improvement=3, degraded_margin=2 -> beyond degraded margin
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 2
Fallback penalty: 2
Policy check: current_cost=9, best_cost=6, margin=3, improvement=3, policy=stability, operation_mode=DEGRADED

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 2/2
  Recovery decision: RESTORE_NORMAL
  Operation mode: DEGRADED -> NORMAL

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=6, best_cost=6, margin=3, improvement=0, policy=stability, operation_mode=NORMAL
```
### v12c - Policy: latency / Trust mode: require_trusted (Execution Log)

```text
=== Policy-aware Routing Simulation v12c ===
Source: nodeA
Destination: nodeF
Policy: latency
Initial trust mode: require_trusted
Hysteresis Margin: 0
Resolver improvement threshold: 2
Degraded switch margin: 0
Degraded fallback penalty: 2
Recovery required steps: 2

Trust table:
  nodeA: TRUSTED
  nodeB: TRUSTED
  nodeC: UNTRUSTED
  nodeD: TRUSTED
  nodeE: UNTRUSTED
  nodeF: TRUSTED

--- Step 1 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: SELECT
Policy phase: initial selection
Resolver phase: not needed
Final reason: Initial trusted route selected

--- Step 2 ---
Node states:
  nodeA: NORMAL
  nodeB: BUSY
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 8
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=8, best_cost=8, margin=0, improvement=0, policy=latency, operation_mode=NORMAL

--- Step 3 ---
Node states:
  nodeA: NORMAL
  nodeB: CONGESTED
  nodeC: NORMAL
  nodeD: CONGESTED
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Reason: preserve connectivity

Operation mode:
  NORMAL -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 16

Selected route:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 7
Decision: DEGRADED_SWITCH
Policy phase: improvement=9, degraded_margin=0 -> switch in degraded latency mode
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 0
Fallback penalty: 2
Policy check: current_cost=16, best_cost=7, margin=0, improvement=9, policy=latency, operation_mode=DEGRADED

--- Step 4 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: CONGESTED
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: NO ROUTE

Trust phase:
  require_trusted -> no trusted route available

Trust failure:
  Detected: YES
  Reason: no trusted path from nodeA to nodeF

Resolver decision:
  Override: YES
  Reason: preserve connectivity

Operation mode:
  DEGRADED -> DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeC', 'nodeE', 'nodeF'] | Cost: 9

Selected route:
  ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8
Decision: DEGRADED_SWITCH
Policy phase: improvement=1, degraded_margin=0 -> switch in degraded latency mode
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 0
Fallback penalty: 2
Policy check: current_cost=9, best_cost=8, margin=0, improvement=1, policy=latency, operation_mode=DEGRADED

--- Step 5 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: BUSY
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 1/2
  Recovery decision: STAY_DEGRADED

Fallback route search:
  Mode: ALLOW_UNTRUSTED_FALLBACK
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
  Penalty applied to untrusted route: 2

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeE', 'nodeF'] | Cost: 8

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: DEGRADED_SWITCH
Policy phase: improvement=2, degraded_margin=0 -> switch in degraded latency mode
Resolver phase: degraded mode policy applied
Final reason: Switched route under degraded mode policy
Degraded mode: ACTIVE
Degraded switch margin: 0
Fallback penalty: 2
Policy check: current_cost=8, best_cost=6, margin=0, improvement=2, policy=latency, operation_mode=DEGRADED

--- Step 6 ---
Node states:
  nodeA: NORMAL
  nodeB: NORMAL
  nodeC: NORMAL
  nodeD: NORMAL
  nodeE: NORMAL
  nodeF: NORMAL

Primary route search:
  Mode: TRUSTED_ONLY
  Result: ROUTE FOUND
  Route: ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Recovery check:
  Trusted route available: YES
  Recovery counter: 2/2
  Recovery decision: RESTORE_NORMAL
  Operation mode: DEGRADED -> NORMAL

Current route re-evaluated:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6

Selected route:
  ['nodeA', 'nodeB', 'nodeD', 'nodeF'] | Cost: 6
Decision: KEEP
Policy phase: current route is already the best route
Resolver phase: not needed
Final reason: Keep current route
Policy check: current_cost=6, best_cost=6, margin=0, improvement=0, policy=latency, operation_mode=NORMAL
```

- Insight:
    - v12c では degraded mode 内の policy boundary 差を明示的に確認できた
    - 同一の improvement = 1 条件において、stability は KEEP、latency は DEGRADED_SWITCH を選択した
    - これにより、degraded mode が単なる例外状態ではなく、policy-sensitive な運用制御モードとして機能することを確認できた
    - PSC Routing は trust failure recovery だけでなく、degraded operational policy の差分表現まで扱える段階に進んだ

---
