# PSC Resolver Arbitration Extension Model v0.2.x（日本語版）

---

## コア原則

```text
RCUの暫定判断 ≠ Resolverの最終判断
```

---

## 解釈

- Resolver は「RCUが決定不能な場合」だけでなく、
  「RCUの判断が曖昧または競合している場合」にも介入する
- 特に、score差が小さい一方で trust または stability に有意差がある場合、
  通常スコアのみでは最終判断できない
- このとき Resolver は競合仲裁レイヤとして機能する

---

## ESCALATE 条件

```text
ESCALATE if:

score_gap < epsilon
AND
(trust_gap > trust_conflict_threshold
 OR
 stability_gap > stability_conflict_threshold)
```

---

## 指標定義

```text
score_gap     = |best.final_score - selected.final_score|
trust_gap     = |best.trust - selected.trust|
stability_gap = |stability_score(best) - stability_score(selected)|
```

---

## 設計上の意味

- `score_gap` は「通常評価上の差の小ささ」を表す
- `trust_gap` は「信頼性の差」を表す
- `stability_gap` は「安定性の差」を表す
- score差が十分小さい場合、trust / stability の差が最終判断に影響する

---

## Resolver の役割

- RCUの暫定判断を再評価する
- trust / stability / recovery条件を含めて仲裁する
- keep / switch の最終決定を返す

---

## 仲裁フロー

```text
RCU
→ best candidate 算出
→ score_gap / trust_gap / stability_gap 計算
→ ESCALATE 判定
→ Resolver 仲裁
→ final decision
```

---

## 状態

- v0.2.x Recovery Return モデルと整合
- multi-candidate 検証結果と整合
- Resolver を「例外処理」から「競合仲裁」へ拡張

---

## 次のステップ

- 既存 Resolver Model v0.1 への反映
- 閾値（epsilon / trust_conflict_threshold / stability_conflict_threshold）の固定
