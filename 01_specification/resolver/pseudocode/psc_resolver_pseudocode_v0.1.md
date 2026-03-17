# PSC Resolver Pseudocode v0.1
---
DependsOn: psc_resolver_spec_v0.1 (JA/EN)
Date: 2026-02-23

## 0. Data Model (Abstract)

### 0.1 Enums

State = { CALM, WARM, HOT, EMERGENCY }

BudgetStage = { STOP, LOW, MID, HIGH }

FlowClass = { SYSTEM, REALTIME, INTERACTIVE, BULK }

Freshness = { FRESH, STALE, EXPIRED }

DecisionMode = { RECOMMEND, ENFORCE }

### 0.2 Core Inputs

FlowRequest:
- flow_id
- src
- dst
- class: FlowClass
- intent: { NewFlow | Continue | Reroute | Burst | Recovery }
- ttl_hint (optional)        # "期限" の抽象ヒント
- latency_hint (optional)    # 低遅延指向など（段階でも良い）

LocalState:
- resolver_state: State
- link_state: { UP, DEGRADED, FLAPPING, DOWN } per link
- queue_state: { LIGHT, BUSY, SATURATED } per queue
- err_state: { NONE, WARN, SEVERE }
- compute_state: { OK, PRESSURE, OVERLOAD }

NeighborView:
- heat_reports[]: { node_id, state: State, age, confidence }
- hints[]: GossipHint

Policy:
- trust_domain_rules
- isolation_rules
- forbidden_links / forbidden_peers
- class_priority_order (default: SYSTEM > REALTIME > INTERACTIVE > BULK)

### 0.3 Outputs

Recommend:
- path_id
- queue_id
- rate_hint: BudgetStage
- stickiness_hint: { KEEP, RELAX }
- token (optional)
- reason_codes[]

Enforce:
- FreezeRoutes(scope, duration)
- Quarantine(target, mode)
- AllowDeny(class_allowlist, class_denylist)
- Cap(class, stage)
- BudgetOverride[class] = BudgetStage
- TokenRules override

Decision:
- mode: DecisionMode
- recommend (if mode=RECOMMEND)
- enforce   (if mode=ENFORCE)

Token:
- class
- scope: { QUEUE | PATH }
- ttl
- priority

---

## 1. Top-Level Resolve()

function Resolve(req: FlowRequest, local: LocalState, neigh: NeighborView, policy: Policy) -> Decision:
    # 1) 状態更新（FSM）
    new_state = UpdateResolverState(local, neigh)
    local.resolver_state = new_state

    # 2) モード選択（遠山モデル：普段は助言、非常時は強制）
    if local.resolver_state == EMERGENCY:
        return ResolveEmergency(req, local, neigh, policy)
    else:
        return ResolveAdvisory(req, local, neigh, policy)

---

## 2. State Machine (UpdateResolverState)

function UpdateResolverState(local: LocalState, neigh: NeighborView) -> State:
    # ※段階制・多段降格禁止・ヒステリシス前提
    # ※EMERGENCY昇格は「二段ロック」(local proof + neighbor confirmation)

    s = local.resolver_state

    # --- helper predicates (段階で判定する) ---
    local_hot = (AnyQueueSATURATED(local) or AnyLinkFLAPPING(local) or local.err_state == WARN)
    local_severe = (local.err_state == SEVERE or AnyLinkDOWN(local) or ManyQueuesSATURATED(local))

    neigh_hot_confirm = NeighborConfirm(neigh, min_state=HOT, freshness=FRESH, min_confidence="MED", min_count="N")
    neigh_warm_confirm = NeighborConfirm(neigh, min_state=WARM, freshness=FRESH, min_confidence="MED", min_count="N")

    recovered_local = LocalRecoveredLongEnough(local)         # ヒステリシス：時間要素は内部で扱う
    recovered_neigh = NeighborRecoveredLongEnough(neigh)

    # --- transitions ---
    if s == CALM:
        if local_severe:
            # ショック級：即時EMERGENCYも許す（設計で許可した場合のみ）
            if neigh_hot_confirm:
                return EMERGENCY
            # 近傍確認が無いならHOT止まり（噂だけで暴走しない）
            return HOT
        if local_hot or neigh_warm_confirm:
            return WARM
        return CALM

    if s == WARM:
        if local_severe and neigh_hot_confirm:
            return EMERGENCY
        if local_hot:
            return HOT
        if recovered_local and recovered_neigh:
            return CALM
        return WARM

    if s == HOT:
        if local_severe and neigh_hot_confirm:
            return EMERGENCY
        if recovered_local and recovered_neigh:
            return WARM
        return HOT

    if s == EMERGENCY:
        # 降格は一段だけ
        if recovered_local and recovered_neigh:
            return HOT
        return EMERGENCY

---

## 3. Advisory Mode Resolve (CALM/WARM/HOT)

function ResolveAdvisory(req, local, neigh, policy) -> Decision:
    # 3.1 予算段階（Budget）を決定（段階制）
    budgets = ComputeBudgets(local.resolver_state)

    # 3.2 Token要否判定（軽い予約）
    token_needed = IsTokenRequired(req)
    token = null
    if token_needed:
        if budgets[req.class] == STOP:
            # 予約段階で抑止（BULK STOPなど）
            return RecommendDeferOrDrop(req, local, budgets, reason="BUDGET_STOP")
        token = MintToken(req, local, budgets)

    # 3.3 候補生成：Fixed + Gossip（鮮度フィルタ）
    candidates = GenerateCandidates(req, local, neigh, policy)

    # 3.4 可能性フィルタ（禁止・隔離・DOWN等）
    feasible = FilterFeasible(candidates, req, local, policy)
    if feasible is empty:
        return RecommendDeferOrDrop(req, local, budgets, reason="NO_FEASIBLE_PATH")

    # 3.5 辞書順スコアリング（Safety > Stability > Load > Preference）
    best = SelectBestLexicographic(feasible, req, local, neigh, policy)

    # 3.6 Sticky（既存フローは維持優先）
    best = ApplySticky(req, best, local)

    # 3.7 rate_hint（段階）と理由コード
    rate_hint = budgets[req.class]
    reasons = BuildReasonCodes(best, req, local, neigh, policy)

    rec = Recommend(
        path_id=best.path_id,
        queue_id=best.queue_id,
        rate_hint=rate_hint,
        stickiness_hint=StickyHint(req, local),
        token=token,
        reason_codes=reasons
    )

    return Decision(mode=RECOMMEND, recommend=rec)

---

## 4. Emergency Mode Resolve (EMERGENCY)

function ResolveEmergency(req, local, neigh, policy) -> Decision:
    # 4.1 強制セット（遠山の桜吹雪）
    # 影響範囲は最小にする：affected scope を推定して限定適用
    scope = EstimateAffectedScope(local, neigh)

    budgets = ComputeBudgets(EMERGENCY)   # SYSTEM HIGH / BULK STOP など

    enforce = Enforce()
    enforce.FreezeRoutes(scope=scope, duration="T_freeze")
    enforce.Quarantine(target=SuspectTargets(local, neigh), mode="ISOLATE_OR_LIMIT")
    enforce.AllowDeny(
        class_allowlist=[SYSTEM, REALTIME, INTERACTIVE],   # 例：INTERACTIVEはLOWで残す
        class_denylist=[BULK]
    )
    enforce.Cap(class=BULK, stage=STOP)
    enforce.Cap(class=INTERACTIVE, stage=LOW)
    enforce.BudgetOverride = budgets
    enforce.TokenRules = "STRICT"  # 新規/変更は原則SYSTEMのみ

    # 4.2 ルーティング決定は固定候補のみ（救急車モード）
    if budgets[req.class] == STOP:
        # 非常時は明確に抑止
        return Decision(mode=ENFORCE, enforce=enforce)

    # 可能なら固定候補から推奨も返す（ただし実装層は強制の範囲内で）
    candidates = GenerateFixedCandidates(req, policy)
    feasible = FilterFeasible(candidates, req, local, policy)
    if feasible not empty:
        best = SelectBestLexicographic(feasible, req, local, neigh, policy)
        # Emergency中は Sticky より Safety を優先しても良い（方針で決める）
        # best = ApplyEmergencyBias(best)

        # 付加情報として「推奨」を同梱したい場合は Enforce 内に hint として持たせる
        enforce.HintRecommend = { path_id=best.path_id, queue_id=best.queue_id }

    return Decision(mode=ENFORCE, enforce=enforce)

---

## 5. Candidate Generation

function GenerateCandidates(req, local, neigh, policy) -> CandidateSet:
    fixed = GenerateFixedCandidates(req, policy)

    # Gossip候補は鮮度で分類
    gossip_fresh = []
    gossip_stale = []
    for h in neigh.hints:
        f = ClassifyFreshness(h, req.class)
        if f == FRESH:
            gossip_fresh.append(HintToCandidate(h))
        else if f == STALE:
            gossip_stale.append(HintToCandidate(h))
        else:
            continue

    # 上限を設ける（噂話で振り回されない）
    gossip_fresh = Limit(gossip_fresh, K=2)
    gossip_stale = Limit(gossip_stale, K=1)

    # HOTではより保守的
    if local.resolver_state == HOT:
        gossip_stale = []     # or keep but lowest score

    return Dedup(fixed ∪ gossip_fresh ∪ gossip_stale)

---

## 6. Feasibility Filter

function FilterFeasible(candidates, req, local, policy) -> list:
    out = []
    for c in candidates:
        if ViolatesPolicy(c, req, policy):
            continue
        if UsesDownLink(c, local):
            continue
        if BreaksIsolation(c, req, policy):
            continue
        out.append(c)
    return out

---

## 7. Lexicographic Scoring

function SelectBestLexicographic(cands, req, local, neigh, policy) -> Candidate:
    # スコアは「数値」ではなく段階（Rank）で比較
    best = null
    for c in cands:
        rank = (
            SafetyRank(c, req, local, policy),
            StabilityRank(c, req, local, neigh),
            LoadRank(c, req, local),
            PreferenceRank(c, req, policy)
        )
        if best is null or rank > best.rank:   # 辞書順比較
            best = { candidate=c, rank=rank }
    return best.candidate

---

## 8. Sticky + Anti-Chatter

function ApplySticky(req, best, local) -> Candidate:
    if req.intent == Continue:
        # 既存フローは変更しない（原則）
        return KeepExistingIfValid(best, local)
    if req.intent == Reroute:
        if InCooldown(req.flow_id, local):
            return KeepExistingIfValid(best, local)
    return best

---

## 9. Budget Table (Stage)

function ComputeBudgets(state: State) -> map[FlowClass]BudgetStage:
    if state == CALM:
        return {SYSTEM:HIGH, REALTIME:HIGH, INTERACTIVE:HIGH, BULK:HIGH}
    if state == WARM:
        return {SYSTEM:HIGH, REALTIME:HIGH, INTERACTIVE:HIGH, BULK:MID}
    if state == HOT:
        return {SYSTEM:HIGH, REALTIME:HIGH, INTERACTIVE:MID, BULK:LOW}
    if state == EMERGENCY:
        return {SYSTEM:HIGH, REALTIME:MID, INTERACTIVE:LOW, BULK:STOP}

---

## 10. Rank Definitions (Stage)

SafetyRank = { DENY, RISKY, OK, PREFERRED }
- DENY: policy violation / isolation break / down link
- RISKY: degraded or flapping risk
- OK: safe and permitted
- PREFERRED: safe + trusted + low loop risk

StabilityRank = { CHAOTIC, UNSTABLE, STABLE, CALM }
- based on gossip freshness + neighbor agreement + local state

LoadRank = { SATURATED, BUSY, LIGHT }
- derived from queue/link stage

PreferenceRank = { BAD, OK, GOOD }
- class-based preference (realtime: latency path, bulk: avoid hot, etc.)

End of pseudocode v0.1
