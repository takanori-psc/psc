# PSC 制御フローレビュー所見

このレビューは、現在のリポジトリ状態を authoritative として扱う。対象は、公開済み /
draft 仕様、Evidence Matrix、validation logs、controlled simulation code、および現在の
rule consistency cleanup である。このレビュー成果物では、公開済み仕様と simulation code は
変更していない。

## 更新済み所見

- 公開済み RCU Decision Model の内部処理段階は、ローカルな運用 `RULE-*` ではなく
  `STEP-*` label を使用する。運用 `RULE-*` の所有権は Evidence Matrix / validation
  namespace が定義する。
- `RULE-04_BLOCK_trust` は Active / Verified の safety block rule としてカバー済みである。
  `RULE-02_SWITCH_score` および `RULE-03_SWITCH_trust` より優先され、最終結果は
  `BLOCK_SWITCH` になる。
- `RULE-17_RECOVERY_VALIDATION_PASS` は Legacy Concept である。現在の運用挙動は
  `RULE-16_RECOVERY_VALIDATION_START` から `reason="VALIDATION_PASSED"` を伴って
  `RULE-18_RETURN_ELIGIBLE` へ直接遷移する。
- `RULE-21_RETURN_ESCALATE` は Legacy Concept である。運用 `RULE-21` の所有権は
  `RULE-21_RETURN_RAMP_ADVANCE` に一本化されている。
- `RULE-19_RETURN_SWITCH` は Verified v0.2 direct return rule のままである。
  `RULE-25_RETURN_RAMP_START` は experimental v0.3 ramp-entry candidate であり、
  `RULE-19` と意味的に同一ではない。
- LIGHT observation policy は Hold が authoritative である。LIGHT は FULL に昇格するか、
  明示的な LIGHT promotion gates が定義され満たされない限り、
  `RULE-22_RETURN_RAMP_HOLD` を emit または resolve しなければならない。
- `ramp_light_tolerates_moderate_dip` を含む historical v0.3 LIGHT advance logs は、
  現在の LIGHT policy ではなく historical experimental behavior として扱う。

## 残る制約

- collision matrix は部分的な arbitration model であり、PSC 全体を網羅する rule arbitration
  engine ではない。現在の coverage は core keep / switch / trust / block / escalation rules と
  recovery ramp hold / abort / complete rules に集中している。
- `RULE-06..21` は collision arbitration に完全統合されていない。これらの一部は active PSC
  degraded / resolver / recovery rules だが、collision predicates と priorities は future work である。
- `RULE-03_SWITCH_trust` は collision matrix namespace では active だが、単独で final switch
  action になる専用 scenario がないため、Evidence Matrix の Verified coverage にはまだ昇格していない。
- `RULE-25_RETURN_RAMP_START` は正式な v0.3 integration まで `RULE-01..24` verified namespace の外にある。
  専用の integration decision なしに Verified へ昇格したり `RULE-19` に統合したりしない。
- Abort handling は `RULE-23_RETURN_RAMP_ABORT` を emit するが、post-abort outcomes はまだ
  first-class operational rules ではなく、主に scenario categories として表現されている。
- scoring、filtering、resolver、degraded、recovery、LIGHT helper logic は controlled simulation
  scripts 間で重複している。

## 運用上の重要度

- もっとも重要な namespace risk は明示的な所有関係によって抑制されている。公開済み model stage は
  `STEP-*`、運用 rule は Evidence Matrix `RULE-*`、obsolete な rule meaning は Legacy Concept、
  v0.3 candidate は Experimental として扱う。
- 残る risk は behavioral drift である。現在の documentation が Hold または candidate-only と扱う箇所でも、
  executable historical scenarios が LIGHT advance や experimental ramp start behavior を示す可能性がある。
- collision matrix の結論は local arbitration conclusion として読むべきであり、PSC 全体の完全な
  precedence guarantee ではない。

## 推奨対応

- Evidence Matrix / validation namespace を authoritative operational rule registry として維持する。
- `RULE-03_SWITCH_trust` を Verified coverage に昇格する前に、単独 final-action の専用 validation
  scenario を追加する。
- `RULE-25_RETURN_RAMP_START` は、v0.3 integration で formal traceability、validation coverage、
  および `RULE-19_RETURN_SWITCH` との明示的な関係が追加されるまで experimental として扱う。
- 現在の LIGHT policy を runtime で強制する必要がある場合は、FULL promotion または明示的な LIGHT
  promotion gates なしに LIGHT が advance できないよう、executable v0.3 LIGHT / ramp scenarios を更新する。
- collision matrix を拡張する場合は、degraded / resolver / recovery rules に対して実際の predicates と
  traceable priorities を追加する。bare placeholders を operational definitions として扱わない。
- rule namespace が安定した後、重複している simulation helpers を shared support module に抽出することを検討する。
