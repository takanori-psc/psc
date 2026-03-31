# 補足（重要な設計確定点）

このv0.1で確定している前提：

- Telemetry = 状態生成
- Routing Table = 保存
- RCU = 意思決定
- congestion_score = 加算モデル
- health と availability は分離
- trust は参照（非所有）
