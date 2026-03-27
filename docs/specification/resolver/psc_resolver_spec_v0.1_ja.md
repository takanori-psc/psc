# PSC Resolver 仕様書 v0.1

English version: [psc_resolver_spec_v0.1_en.md](psc_resolver_spec_v0.1_en.md)

## Document Information

- Document Name : Resolver Specification
- Version       : v0.1
- Project       : PSC / Photon System Controller
- Layer         : PSC Fabric
- Document Type : Specification
- Component     : Resolver
- Status        : Draft
- Author        : T. Hirose
- Created       : 2026-03
- Last Updated  : 2026-03
- Language      : Japanese

## 0. 設計哲学

本仕様は
PSC Resolver Design Philosophy v1.0
に準拠する。

Resolverは最適化装置ではない。
それは構造安定化装置である。

本仕様に記載される全ての機構は、
以下の原則を遵守しなければならない。

- 継続的なグローバル最適化を行わない
- 状態ベースの協調を行う
- ローカル優先の自律性を尊重する
- 構造的安定性が危険にさらされた場合のみ介入する
- Resolverは実行主体ではなく、制約と決定を定義する意思決定モジュールである。 
- Resolverは説明可能かつ再現可能な意思決定を行わなければならない。

---

## 1. 概要

ResolverはPSCにおける意思決定制御モジュールである。
Resolverはハイブリッド権限モデルで動作する。

- 平常時：助言（Advisory）
- 非常時：強制（Authoritative）

設計原則：
- 数値最適化に依存しない状態ベース制御
- ローカル優先の安定性
- Gossipによる適応補助
- 軽量予約モデル（Token/Budget方式）

Resolverは経路制御そのものを実行する装置ではなく、
その説明責任を持つ意思決定主体である。
Resolverは実行を行わず、システムに対する制約と意思決定を出力する。
Resolverは常時稼働する制御主体ではなく、必要時にのみ介入する意思決定モジュールである。
Resolverの出力は実行指示ではなく、実行層に対する制約定義として解釈されなければならない。

---

## 2. 権限モデル

### 2.1 助言モード（CALM / WARM / HOT）

Resolverは以下を出力する。

- Recommend{path_id, queue_id, rate_hint}
- Optional Token{class, scope, ttl}
- ReasonCodes[]

最終実行はSwitching Coreが行う。

### 2.2 強制モード（EMERGENCY）

Resolverは以下を出力する。

- Enforce{FreezeRoutes, Quarantine, Allow/Deny, Cap}
- Budget段階の上書き
- TokenRulesの上書き

実行層はこれに従わなければならない。

Authoritativeモードにおいては、Enforce出力はRecommend出力より常に優先される。
すべての決定は再現可能かつ決定順序が決定的でなければならない。
強制モード時、Switching CoreはResolverの指示を必ずログに記録しなければならない。
Resolverの動作モードは状態機械（Section 3）と連動して決定される。

---

## 3. 状態機械

状態遷移は厳密に段階ベースで行われる。
複数段飛びの降格は許可されない。

状態：

- CALM
- WARM
- HOT
- EMERGENCY

Resolverの出力は状態に依存して変化する。
CALMでは助言中心、EMERGENCYでは強制中心の出力となる。
EMERGENCY状態では、Resolverは安全側に倒す操作のみを許可する。

### 3.1 昇格ルール

CALM → WARM：
- ローカルな輻輳またはリンク劣化
- Freshな近傍ノードの熱上昇

WARM → HOT：
- 継続的な飽和
- リンクフラッピング
- 警告レベルのエラー

HOT → EMERGENCY：
二段階ロックが必要：
A) ローカルの重大異常
B) 近傍確認（Freshかつ十分な信頼度）

### 3.2 降格ルール

EMERGENCY → HOT：
- ローカルおよび近傍の安定回復が継続

HOT → WARM：
- キューとリンクが安定化

WARM → CALM：
- 十分な時間、静穏状態が継続

ヒステリシスを適用する。

### 3.3 決定論的遷移保証

Resolverは以下を保証しなければならない。

- 予測可能な状態遷移
- 間欠的不安定下での発振防止
- 有界な反応時間

回復閾値は昇格閾値より厳しくなければならない。
複数段飛びの降格は禁止されたままである。

---

### 3.4 状態ごとの強制ポリシー

各状態は、自動的に対応する制御制約を有効化する。

#### CALM
- マルチパス経路有効
- 学習および予測有効
- Budget制限なし

#### WARM
- 経路更新頻度を制限
- Budget上限を縮小
- 安全余裕を増加
- Gossip頻度をわずかに増加

#### HOT
- 安定経路集合を強制
- 非重要トラフィックを抑制
- 優先クラスを保護
- 近傍状態ブロードキャスト有効

#### EMERGENCY
- ホワイトリスト経路のみ許可
- 外部リンク制限または隔離
- 署名付き制御プレーン更新を必須化
- 必要に応じて隔離モード有効
- FailMode既定値：CLOSED

---

### 3.5 状態スコープモデル

状態は複数スコープに存在する。

- LinkState
- LocalDomainState
- NodeState

昇格は可能な限り局所に留めるべきである。
グローバル昇格は最終手段である。

NodeStateは、複数リンク劣化が観測された場合、
または整合性侵害が検出された場合に昇格する。

NodeState EMERGENCYは、
そのリンクが最後に残ったアップリンクである場合を除き、
単一LinkStateのみを理由に発動すべきではない。

---

### 3.6 既定タイミングパラメータ（推奨）

T1 = 2s  
T2 = 1s  
R1 = 10s  
R2 = 30s  
R3 = 60s + authorization

ヒステリシスは必須である。

### 3.7 LinkState更新ループ（参考疑似コード）

本節は参考実装ガイドラインである。
明示的に記載されない限り、NON-NORMATIVEとする。
LinkStateはLocalDomainStateおよびNodeStateの集約ロジックへ入力される。

// 各リンクごとに実行
state LinkState = CALM

loop FastLoop every 50ms:
  m = read_counters(link)
  win.update(m)            // moving window / EMA / ring buffer

loop DecisionLoop every 500ms:
  trg_warm  = win.q_occ_p95 > 0.70 for >= T1  OR win.crc_rate > WARN for >= T1
  trg_hot   = win.q_occ_p95 > 0.90 for >= T2  OR win.drop_rate > DROP_WARN for >= T2 OR win.flap_10s >= 2
  trg_em_a  = win.link_down OR win.crc_rate > FATAL OR win.flap_30s >= 3
  trg_em_b  = neighbor_confirm_fresh(link, min_stage=HOT, min_conf=CONF_MIN)

// 昇格（厳格な段階ベース）
if LinkState == HOT and trg_em_a and trg_em_b:
    LinkState = EMERGENCY; emit_state_hint()
else if LinkState == WARM and trg_hot:
    LinkState = HOT; emit_state_hint()
else if LinkState == CALM and trg_warm:
    LinkState = WARM; emit_state_hint()

// 降格（ヒステリシス）
if LinkState == EMERGENCY and stable_for(R3) and authorized():
    LinkState = HOT; emit_state_hint()
else if LinkState == HOT and stable_for(R2):
    LinkState = WARM; emit_state_hint()
else if LinkState == WARM and stable_for(R1):
    LinkState = CALM; emit_state_hint()

function stable_for(duration):
  return (win.q_occ_p95 < 0.60 AND win.drop_rate < DROP_OK AND win.crc_rate < OK AND no_flap) for >= duration

### 3.8 近傍確認（Fresh / Confidence）— 二段階ロックB

#### 3.8.1 目的

neighbor_confirm_fresh() は
HOT → EMERGENCY 昇格のための第二段階ロックを提供する。

目的：
- 単一ノードによる誤昇格を防止する
- 悪意ある、またはノイズ的な近傍ヒントに耐性を持たせる
- 状態共有のみで軽量なシグナリングを維持する

---

#### 3.8.2 入出力

入力：
- link_id
- min_stage（既定値：HOT）
- min_conf（既定値：CONF_MIN）

出力：
- Boolean（確認条件を満たす場合 true）

---

#### 3.8.3 StateHint メッセージ形式

StateHint {
  sender_id
  domain_id
  stage              // CALM/WARM/HOT/EMERGENCY
  scope              // LinkState | LocalDomainState | NodeState
  target             // link_id or domain_id (recommended)
  age                // seconds since observed
  confidence         // LOW | MID | HIGH
  reason_codes[]     // optional
  nonce
  timestamp
  signature          // REQUIRED for HOT/EMERGENCY
}

ルール：
stage >= HOT のHintは有効な署名を必ず含まなければならない。

---

#### 3.8.4 Freshnessルール

HintがFreshである条件：

age <= FRESH_MAX(stage, scope)

推奨既定値：

HOT + LinkState: 2s  
HOT + LocalDomainState: 5s  
EMERGENCY: 5s  

ローカルリンクがフラッピングしている場合、
Freshness windowは縮小すべきである。

CONF_MIN の既定値：MID

FRESH_MAX と REPLAY_MAX は実装設定可能であるべきである。

---

#### 3.8.5 Confidenceモデル（離散）

Confidenceレベル：

LOW:
- 弱い異常、または短時間の異常

MID:
- 継続的な異常、または複数の弱い異常

HIGH:
- 重大な異常（link down, fatal CRC）
  または多症状の継続異常

送信側ルール：
- EMERGENCY段階は HIGH confidence を必須とする
- HOT段階は MID または HIGH が望ましい

受信側ルール：
- confidence < min_conf のHintは無視する

---

#### 3.8.6 Quorumポリシー

確認には K 個の異なる近傍ノードが必要である。

既定値：
- K = 1（小規模プロトタイプ）
- K = 2（推奨）
- K = 3（敵対的ドメイン）

制約：
- 異なる sender_id が必要
- domain_id ごとに最大1件まで

---

#### 3.8.7 スコープ一致ルール

確認が有効となる条件：

1) 近傍が同一リンクについて LinkState(stage >= min_stage) を報告
OR
2) 近傍が LocalDomainState(stage >= min_stage) を報告し、
   reason_codes に INTEGRITY または WIDE_FAILURE を含む
OR
3) 近傍が NodeState(stage >= min_stage) を報告し、
   ローカルノード側でも複数リンク劣化を観測している

---

#### 3.8.8 リプレイおよび偽装防護

受信側は以下の場合Hintを拒否しなければならない：

- 署名が無効（必要な場合）
- timestamp が REPLAY_MAX より古い（推奨：30s）
- nonce が既出
- sender が trust set に存在しない（secured domains）

非保護ドメインでは：
- K MUST be >= 2
- domain_id filtering REQUIRED if available

---

#### 3.8.9 規範定義

neighbor_confirm_fresh(link, min_stage, min_conf) は、
以下を満たす K 個以上の有効な StateHints が存在する場合 true を返す：

- stage >= min_stage
- confidence >= min_conf
- freshness 条件を満たす
- 署名が有効（必要な場合）
- 異なる送信者制約を満たす

それ以外の場合は false を返す。

### 3.9 参考疑似コード（NON-NORMATIVE）

function neighbor_confirm_fresh(link, min_stage=HOT, min_conf=CONF_MIN):

  valid = []

  for hint in inbox.hints_for(target=link.id):

    if hint.stage < min_stage:
        continue

    if hint.confidence < min_conf:
        continue

    if not is_fresh(hint):
        continue

    if hint.stage >= HOT and not verify_signature(hint):
        continue

    if is_replay(hint):
        continue

    valid.append(hint)

  valid = distinct_by_sender(valid)

  if domain_id_known:
      valid = cap_one_per_domain(valid)

  return count(valid) >= K

### 3.10 Reason Code標準化

Reason codes は相互運用性およびシミュレーションのために
標準化されるべきである。

推奨ベースセット：

FLAP              // link instability
CRC_WARN          // warning-level errors
CRC_FATAL         // fatal-level errors
SATURATION        // queue saturation
DROP_EXCESS       // sustained drop rate
INTEGRITY         // signature or security anomaly
WIDE_FAILURE      // multi-link degradation
LOCAL_ONLY        // confined local anomaly

ルール：
- reason_codes は情報用途であり、stageロジックを上書きしてはならない
- 複数の reason_codes を含めてもよい
- EMERGENCY段階では少なくとも1つの reason_code を必須とする

### 3.11 シミュレーション用スコアリングモデル（NON-NORMATIVE）

本節はシミュレーション専用の評価モデルを定義する。
これはResolverの規範的な状態ベース制御ロジックを変更しない。

Resolverの運用上の判断は引き続き状態ベースで行われる。
スコアリングモデルは以下にのみ使用される：

- 閾値調整
- 安定性解析
- フラッピング耐性評価
- 変更圧評価

---

#### 3.11.1 目的

スコアリングモデルは、
状態遷移ルールを変更することなく
不安定圧力を定量化する。

これにより、以下の制御実験が可能となる：

- リンクフラッピング強度
- 再経路変更頻度
- Token発行圧力
- EMERGENCY昇格タイミング

このモデルは数値最適化器として解釈されてはならない。

---

#### 3.11.2 ウィンドウ定義

シミュレーションウィンドウ：

WINDOW = 10 seconds（推奨）

各指標はウィンドウごとに評価される。

---

#### 3.11.3 入力カウンタ（各ウィンドウ）

F = link state transitions（UP↔DOWN count）

R = reroute executions

T = token issued count

---

#### 3.11.4 スコアリング式（Aggressive Profile v1）

スコアリング式（Aggressive Profile v1）：

S = F + 2R + 1.5T

ここで：

- F は物理的不安定性を表す
- R は経路不安定性を表す
- T は制御プレーン圧力を表す

T の重みは変更圧感度を反映する。

---

#### 3.11.5 状態マッピング（シミュレーション専用）

CALM        : S ≤ 2
WARM        : 3 ≤ S ≤ 5
HOT         : 6 ≤ S ≤ 9
EM_CANDIDATE: S ≥ 10

---

#### 3.11.6 EMERGENCY確認（シミュレーション）

EMERGENCYへの遷移条件：

- S ≥ 10 が2ウィンドウ連続

このシミュレーションルールは、
Section 3.1 で定義された規範的な二段階ロック機構を上書きしない。

規範的昇格ルールが優先される。

---

#### 3.11.7 観測された挙動特性（プロトタイプ結果）

プロトタイプシミュレーションでは以下の分離が得られた：

- 軽微フラップ（F ≤ 2, T minimal）：
  CALMで安定

- 中程度フラップ（F ≈ 4, low T）：
  一時的にHOT、自己回復

- 重度フラップ（F ≥ 8）：
  2ウィンドウ後に HOT → EMERGENCY

- 制御プレーンスラッシング（low F, high T）：
  継続時にEMERGENCY発動

- 軽微な制御変動：
  EM昇格なしでHOTに留まる

これは過剰感度なしに
明確な状態分離を示している。

---

#### 3.11.8 設計解釈

このスコアリングモデルは以下を示す：

- Token圧力は有効な早期警告信号である
- 物理的不安定と制御的不安定の両方を観測可能でなければならない
- AggressiveなToken重み付けは
  データセンター級環境において早期封じ込めを改善する

T の重みは展開プロファイルごとに調整してもよい。

---

#### 3.11.9 制約

- 本モデルは状態ベースロジックを置き換えてはならない
- 数値最適化依存を導入してはならない
- 任意かつシミュレーション専用でなければならない

### 3.12 イベント伝播モデル

Resolver通信はイベント駆動型の伝播モデルに従う。

通常運用時、PSCノードは
グローバル同期のための周期的制御トラフィックを
生成すべきではない。

状態情報は不安定イベントが発生したときにのみ伝播される。

---

#### 3.12.1 一次伝播スコープ

ノードが局所的な不安定イベント
（輻輳、キュー溢れ、リンク劣化など）を検出した場合、
イベントはまず直接接続された近傍PSCノードのみに
伝播されるべきである。

この1ホップ伝播は、
安定時には制御プレーンを静かに保ちながら、
局所協調を迅速に実現する。

---

#### 3.12.2 拡張伝播

1ホップを超える伝播は、以下の場合にのみ許可される：

- システム状態が HOT または EMERGENCY に達した場合
- 局所封じ込めに失敗した場合
- 複数ドメインにまたがる不安定が検出された場合

このような場合、イベントは次ホップへ伝播してもよく、
より広範な安定化応答を調整するために使用される。

---

#### 3.12.3 距離に基づく影響減衰

イベントの影響度は、
伝播距離に応じて減衰しなければならない。

近傍ノードは受信イベントを実行可能な信号として扱い、
より遠方のノードは助言的ヒントとして扱うべきである。

この機構により、
局所障害に対する不要なグローバル反応を防ぐ。

---

#### 3.12.4 グローバル昇格

ネットワーク全体への伝播は、
通常運用時には避けるべきである。

グローバル安定化動作は、以下の場合にのみ発生すべきである：

- EMERGENCY状態が複数ドメインへ伝播した場合
- 指定された調停ノードが
  より広い介入が必要と判断した場合

この設計により、
大規模障害時には迅速応答を可能にしつつ、
PSCの「静かなネットワーク」哲学を維持する。

---

## 4. 予約モデル（Light）

Budget/Token は継続的なレート制御ではなく、
受付制御および変更圧制御を担う。
rate_hint は助言値であり、
Budget制約下では実行層によって制限されてもよい。

強いレート制限が必要な場合、
それは Budget ではなく Enforcement（例：Cap/Throttle）として
表現されるべきである。

本予約モデルは帯域保証を目的とせず、
過負荷伝播の封じ込めを目的とする。
TokenおよびBudgetは、実行層に対する制約条件として解釈される。

### 4.1 Budget（段階ベース）

Budget[class] ∈ {STOP, LOW, MID, HIGH}

状態ごとの既定値：

CALM:
- All HIGH

WARM:
- BULK = MID

HOT:
- BULK = LOW
- INTERACTIVE = MID

EMERGENCY:
- SYSTEM = HIGH
- REALTIME = MID
- INTERACTIVE = LOW
- BULK = STOP

### 4.2 Token利用

以下にはTokenが必要：

- NewFlow
- Reroute
- Burst
- Recovery

Tokenは保証ではなく許可である。

TTLが適用される。

---

## 5. 候補生成

候補集合 C は次で定義される：Fixed ∪ Gossip（Fresh/Valid）

### 5.1 固定経路

事前定義：
- PathA（低遅延）
- PathB（負荷回避）
- PathC（信頼優先）

### 5.2 Gossip経路

GossipHint は以下を含む：

- prefer_path
- avoid_link
- stage
- age
- confidence

Freshnessフィルタリング：
- REALTIME: 短い有効期限
- BULK: より長い許容

### 5.3 非常時モード

固定経路のみを使用する。
Gossipの影響は最小化される。

---

## 6. スコアリングモデル（辞書順）

本モデルは数値最適化を回避し、
辞書順によって安全性を優先する。
本スコアリングはResolverの意思決定ロジックを置き換えるものではない。

1. SafetyRank
2. StabilityRank
3. LoadRank
4. PreferenceRank

Sticky routing が優先される。

Sticky routing は、
安全性または強制制約が変更を要求しない限り、
既存フローと経路の対応を保持しなければならない。

Sticky preference は
SafetyRank の順序を上書きしてはならない。

---

## 7. 強制セット（非常時専用）

強制は必要最小限のスコープで適用される。
これらの強制操作は、ResolverのAuthoritative決定に基づいて適用される。

- FreezeRoutes(scope, duration)
- Quarantine(target, mode)
- Allow/Deny class control
- Cap(class, stage)

FailMode の既定値は CLOSED

---

## 8. チャタリング防止機構

- 状態遷移ヒステリシス
- Sticky flow preservation
- Reroute cooldown
- Gossip aging weight reduction

---

## 9. 今後の課題

- シミュレーションパラメータ調整
- Token TTL最適化
- Budgetマッピング較正
- セキュリティ境界の形式化

---

## 10. 決定保証（Decision Guarantees）

- Resolverは決定論的でなければならない（Deterministic）
- 同一入力に対して同一出力を保証
- 決定順序は固定される（Decision Order）
- 候補が空集合になった場合：
  - 必ずフォールバック動作を行う
  - Advisory：Hold
  - Authoritative：Closed / Enforced
- 未定義状態は禁止

---

##11. 監査性（Auditability）

- Resolverのすべての決定は追跡可能でなければならない
- Authoritativeモードではログ必須
- ログは以下を含む：
  - 入力状態（State / Telemetry / Policy）
  - 候補集合
  - フィルタリング過程
  - 最終決定
  - ReasonCodes
- 決定は再現可能でなければならない（Replay可能）

---


v0.1 終了

## リリースノート（v0.1 FINAL）
- 段階ベースResolverコアを定義（CALM/WARM/HOT/EMERGENCY）
- HOT→EMERGENCY の二段階ロックを規定
- LinkState参考ループを追加（NON-NORMATIVE）
- シミュレーション用スコアリングモデルを追加（NON-NORMATIVE, Aggressive Profile v1）
- イベント伝播モデルを追加（イベント駆動・距離減衰型）
