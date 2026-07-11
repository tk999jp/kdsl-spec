# Experimental Validator Helpers

目的: KDSL / R1 / R1C / Template / CompactPrompt / Safety Gate Registry をPython等で機械検査するための experimental heuristic lint helper 置き場。

status: experimental-heuristic-helpers
implementation: partial
project_status: ../../docs/project-status.md
source_specs:

```text
spec/core/kdsl-spec.md
spec/lint/kdsl-lint-checklist.md
spec/lint/kdsl-compact-prompt-lint.md
spec/lint/kdsl-safety-gate-registry-lint.md
spec/lint/kdsl-r1c-lint.md
spec/r1/r1-result-spec.md
spec/r1/r1c-compact-result-schema.md
spec/bridge/kdsl-adps-bridge.md
spec/bridge/kdsl-cp-packet-bridge.md
spec/registry/kdsl-safety-gate-registry.md
spec/registry/kdsl-safety-gate-composition.md
templates/README.md
```

## 位置づけ

```text
Validator helpers:=形式/整合性/欠落/権限衝突を検査する補助器
Validator helpers != 承認者
Validator helpers != Runtime確認者
Validator helpers != 要件判断者
Validator helpers != D禁止解除者
Validator helpers != release readiness判定者
Validator helpers != semantic equivalence proof
Validator helpers != safety proof
Validator helpers != execution authority
Validator helpers != canonical promotion authority
```

## 現在の実装範囲

```text
r1_required_blocks.py:
  KDSL_RESULT required block presence lint

r1_rt_basis.py:
  RT:v basis wording heuristic lint
  RT/VERIFY/S field scoped
  文書全体の説明語だけではRT:v根拠扱いしない

r1_authority_guard.py:
  NEXT/COMMIT authority-shape heuristic lint
  同一行key-valueと簡易複数行blockを対象

kdsl_template_refs.py:
  known template reference and safety gate lint

kdsl_template_expansion.py:
  template expansion evidence lint
  実際のtemplate全文展開照合ではない

kdsl_compact_prompt.py:
  CompactPrompt profile/shorthand detection
  mode/safety/lexicon value lint
  standard/kanji-v1 required block lint
  representative restricted alias lint
  representative CP-Lift trigger lint
  Packet draft boundary lint

kdsl_safety_gate.py:
  SAFETY_GATES block detection
  kdsl-sg@0.1-draft registry check
  known Safety Gate ID/state check
  id/state/scope/reason required field check
  satisfied evidence/authority check
  dev-prompt baseline gate check
  representative additive composition check

kdsl_r1c.py:
  KDSL_RESULT + kdsl-r1c@0.1-draft detection
  Full R1 fallback/out-of-scope separation
  canonical required field presence/order
  short alias rejection
  JSON-compatible structured field lint
  VERIFY class separation
  RT state/basis heuristic lint
  NEXT proposal_only lint
  COMMIT actual/proposed/permission basis lint

kdsl_validate.py:
  target wrapper: r1 / prompt / compact / safety-gate / r1c / all

run_samples.py:
  sample expectation runner
```

## Verification state

Historical checkpoints:

```text
CompactPrompt first slice:
  total: 23 / failed: 0

Safety Gate first slice:
  total: 34 / failed: 0

R1C first slice candidate:
  total: 49 / failed: 0
```

Repository examples included in the suite:

```text
examples/safety-gates/dev-prompt-safety-gates.example.md
examples/r1c/r1c-success.example.md
examples/r1c/r1c-blocked.example.md
examples/r1c/r1c-needs-user.example.md
```

Evidence:

```text
tools/validator/verification/kdsl_compact_prompt_verify.md
tools/validator/verification/kdsl_safety_gate_verify.md
tools/validator/verification/kdsl_r1c_verify.md
```

## 目的

```text
KDSL_PROMPTの必須要素欠落検出
Template参照の未読/未定義検出
KDSL-CP/KDSL-CP漢の必須block欠落検出
kanji-v1構造aliasのfree-text誤用検出
代表的CP-Lift条件検出
Packet draftの実行可能誤認検出
R1/KDSL_RESULTの必須block欠落検出
RT:v根拠語のfield-scoped検出
NEXT/COMMIT権限混同のshape検出
Safety Gate registry/ID/state/field欠落検出
Safety Gate baseline/compositionの代表的欠落検出
R1C schema/field/type/order欠落検出
R1C RT/NEXT/COMMIT境界検出
R1C Full R1 fallback分離
EVIDENCEの観測/推論/未観測/未確認分離検査設計
AUTHORITYのcommit/push/release衝突検査設計
```

## 非目的

```text
AIの判断を代行しない
ユーザー承認を代行しない
実機Runtime確認を代行しない
仕様変更の可否を判断しない
D禁止を解除しない
曖昧ログの意味を断定しない
template全文展開を証明しない
自然言語の意味等価性を証明しない
safety proofとして扱わない
operation authorityを付与しない
full parserとして扱わない
full YAML/JSON parserとして扱わない
full negation parserとして扱わない
release readinessを判定しない
R1C canonical/stable promotionを判定しない
Packet readinessを判定しない
```

## 想定構成

```text
tools/validator/
  README.md
  r1-validator-design.md
  kdsl-template-lint-design.md
  r1_required_blocks.py
  r1_rt_basis.py
  r1_authority_guard.py
  kdsl_template_refs.py
  kdsl_template_expansion.py
  kdsl_compact_prompt.py
  kdsl-compact-prompt-implementation-notes.md
  kdsl_safety_gate.py
  kdsl-safety-gate-implementation-notes.md
  kdsl_r1c.py
  kdsl-r1c-implementation-notes.md
  kdsl_validate.py
  kdsl_validate_usage.md
  run_samples.py
  samples/*
  verification/*
```

## Safety Gate first-slice checks

```text
registry:=kdsl-sg@0.1-draft
known IDs:=SG-DESIGN/SG-SCOPE/SG-EVIDENCE/SG-RUNTIME/SG-AUTHORITY/SG-ROLLBACK/SG-PUBLIC/SG-DATA/SG-KDSL-DP/SG-STOP
states:=hold|satisfied|blocked|na
required fields:=id/state/scope/reason
state:satisfied→evidence/authority必須
state:blocked→evidence欠落warn
state:na→reason必須
dev-prompt baseline:=SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP
representative composition:=rollback/data/public/runtime/KDSL-DP
```

Boundary:

```text
SAFETY_GATES blockなし→対象外pass/info
current Full KDSL protected wording検査→未実装
parent-child inheritance lint→未実装
aggregate state calculation→未実装
```

## R1C first-slice checks

```text
schema:=kdsl-r1c@0.1-draft
envelope:=KDSL_RESULT
required fields:=STATUS/PHASE/S/FILES/WHY/CMD/VERIFY/RT/RISK/NEXT/COMMIT
short aliases:=禁止
FILES/CMD/RISK:=JSON array<string>
VERIFY:=pass/fail/not_run arrays
RT:=state/basis
NEXT.authority:=proposal_only
COMMIT:=actual/proposed/permission_basis
Full R1 without SCHEMA:=out-of-scope pass/info
unknown SCHEMA:=fail
```

Boundary:

```text
inline JSON-compatible valueのみ
multi-line structured value未実装
Full R1 semantic validationの代替ではない
R1C validator pass != R1C canonical/stable promotion
R1C validator pass != Packet readiness
```

## 設計方針

```text
軽量lint helperとして扱う
検査項目を仕様として固定しすぎない
R1/CompactPrompt/Safety Gate/R1C validatorを優先
Template lintは未読/未定義/権限衝突を優先
KDSL parserは過剰に厳密化しない
Markdown + code block + key-value風blockの軽量検査から始める
validator passの過信を避ける
```

## 検査レベル

```text
ERROR:
  safety gate破損
  権限事故
  RT:v誤認
  必須block/field欠落
  CP-Lift漏れ
  unknown SG/schema
  必須composition欠落
  R1C JSON型/order/NEXT/COMMIT違反

WARN:
  曖昧/弱化
  推奨block欠落
  構造key混在
  blocked evidence欠落
  actual commit + permission basis不整合

INFO:
  任意改善
  表記揺れ
  対象外
  Full R1 fallback
```

## Sample expectation runner

```text
python tools/validator/run_samples.py
```

このrunnerは、サンプルファイルと期待exit codeのズレを検出するための補助です。
runner passも、承認/RT:v/safety proof/release readinessを意味しません。

GitHub Actions:

```text
workflow: .github/workflows/validator.yml
trigger: pull_request/main push/workflow_dispatch
command: python tools/validator/run_samples.py
```

## Known limitations

```text
文字列/軽量構造lint中心
single SAFETY_GATES blockのみ解析
first KDSL_RESULT blockのみ解析
R1C multi-line JSON未対応
full parserなし
full YAML/JSON parserなし
full natural-language semantic parserなし
full negation parserなし
full template expansion proofなし
Safety Gate triggerの例示/実操作完全識別なし
protected wording semantic lintなし
parent-child inheritance lintなし
R1C round-trip semantic proofなし
runtime実行なし
source authenticity判断なし
approval delegationなし
```

## Safety first

```text
validator未実行→pass扱禁止
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != safety proof
validator pass != execution authority
validator pass != release readiness
Safety Gate validator pass != Packet readiness
R1C validator pass != canonical/stable promotion
R1C validator pass != Packet readiness
validator failure時→該当箇所を修正またはU確認
```
