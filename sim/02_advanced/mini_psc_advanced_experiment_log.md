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
