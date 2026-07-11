# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-11

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本は `spec/manifest.md` と `spec/core/*` / `spec/profiles/*` / `spec/r1/*` / `spec/lint/*` / `spec/bridge/*` / `spec/registry/*` を参照します。

## 1. Current public state

```yaml
current_public_state:
  repository_visibility: public
  published_release: v1.1.0-rc1
  release_class: experimental_preview
  release_type: prerelease
  public_ready: no
  stable_release: none
  release_assets: none
  license: MIT
```

```text
public: yes
public-ready: no
stable: no
```

現在の状態は「公開済み experimental preview」であり、正式public-ready/stable releaseではありません。

Policy:

```text
v0.1.0-draft tag:=履歴として維持
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft設計/validator改善:=継続
既存tag移動禁止
Release Assets操作禁止
stable/public-ready化→別途U明示承認必須
```

## 2. Integrated workstreams

### PR #1 — v2 CompactPrompt architecture

```yaml
v2_compact_prompt_integration:
  source_branch: feature/kdsl-v2-compact-prompt
  pull_request: 1
  merge_method: squash
  merge_status: merged
  squash_commit: ae55f845018c0e8208d9e07c9814bc48035b2ef8
  review_close_commit: ef801fa23abb0d235df8c7e9a1ea929d5bf26b97
  scope:
    - CompactPrompt profile
    - kanji-v1 lexicon
    - CompactPrompt lint specification
    - CP-Lift boundary
    - future Packet non-executable boundary
  stable_effect: none
```

### PR #2 — CompactPrompt validator first slice

```yaml
compact_prompt_validator_integration:
  source_branch: agent/kdsl-compact-validator
  pull_request: 2
  merge_method: squash
  merge_status: merged
  squash_commit: c9e6dc5d8aaf4f5860fe2bab9d69247b41fc3b82
  verified_implementation_head: 2b50ed1
  scope:
    - CompactPrompt profile/shorthand detection
    - mode/safety/lexicon value lint
    - required block lint
    - kanji-v1 restricted alias lint
    - representative CP-Lift trigger lint
    - Packet draft boundary lint
    - wrapper target compact
```

### PR #3 — Validator CI baseline

```yaml
validator_ci_integration:
  source_branch: agent/kdsl-validator-ci
  pull_request: 3
  merge_method: squash
  merge_status: merged
  squash_commit: 8505c16b44b4a95892e8d2f3f44119a2ad31afde
  review_close_commit: eea2f9f3f3f15062ef24820f0efdc3fc85868146
  workflow: .github/workflows/validator.yml
  runner: ubuntu-latest
  python: "3.11"
  permissions: contents-read
  timeout_minutes: 5
  triggers:
    - pull_request -> main
    - push -> main
    - workflow_dispatch
  command: python tools/validator/run_samples.py
```

### PR #4 — Safety Gate Registry v0.1 draft

```yaml
safety_gate_registry_integration:
  registry: kdsl-sg@0.1-draft
  source_branch: agent/kdsl-safety-gate-registry
  pull_request: 4
  approval_status: user_approved
  approval_date: 2026-07-11
  merge_method: squash
  merge_status: merged
  source_head: 194d7f36efe0d653c28f4f10e52ec37807f2424b
  squash_commit: e1ab32e398751dcb5bc38bec8325aeded798d843
  validator_ci_run_id: 29141378172
  validator_ci_run_number: 23
  validator_ci_conclusion: success
  specification_status: v2_draft_integrated
  states:
    - hold
    - satisfied
    - blocked
    - na
  ids:
    - SG-DESIGN
    - SG-SCOPE
    - SG-EVIDENCE
    - SG-RUNTIME
    - SG-AUTHORITY
    - SG-ROLLBACK
    - SG-PUBLIC
    - SG-DATA
    - SG-KDSL-DP
    - SG-STOP
  stable_effect: none
```

### PR #5 — Safety Gate Registry validator first slice

```yaml
safety_gate_validator_integration:
  source_branch: agent/kdsl-safety-gate-validator
  pull_request: 5
  merge_method: squash
  merge_status: merged
  source_head: bc49316ba83ef59a7c49f6ae24a29f581e2ea16c
  squash_commit: 05773b4426481b783f2aeb55f1bcbcc50c17ee93
  workflow: Validator CI
  workflow_run_id: 29143048337
  workflow_run_number: 33
  workflow_status: completed
  workflow_conclusion: success
  sample_total: 34
  sample_failed: 0
  actual_repository_example_checked: examples/safety-gates/dev-prompt-safety-gates.example.md
  stable_effect: none
```

## 3. Current architecture direction

```text
v2-draft architecture:=main統合済み
CompactPrompt validator first slice:=main統合済み
Validator CI baseline:=main統合済み
Safety Gate Registry:=main統合済み
Safety Gate Registry validator first slice:=main統合済み
KDSL-Packet:=draft-non-executable
R1C:=未定義
stable/tag/release/Release Assets操作:=別途U明示承認必須
```

## 4. License state

```yaml
license:
  type: MIT
  file: LICENSE
  approved_by_user: 2026-07-07
  scope:
    - specifications
    - documentation
    - examples
    - templates
    - validator helper code
```

## 5. Validator maturity

```yaml
validator:
  maturity: experimental_heuristic_helpers
  implementation: partial
  authority: non_authoritative
  current_main_scope:
    - KDSL_RESULT required block presence lint
    - RT:v basis wording heuristic lint
    - NEXT/COMMIT authority-shape heuristic lint
    - template reference lint
    - template expansion evidence lint
    - CompactPrompt required block lint
    - CompactPrompt mode/safety/lexicon lint
    - kanji-v1 restricted alias lint
    - representative CP-Lift lint
    - Packet draft boundary lint
    - Safety Gate registry name lint
    - Safety Gate known ID/state lint
    - Safety Gate required field lint
    - Safety Gate satisfied evidence/authority lint
    - dev-prompt baseline Safety Gate lint
    - representative Safety Gate composition lint
  wrapper_targets:
    - r1
    - prompt
    - compact
    - safety-gate
    - all
  ci:
    status: integrated
    workflow: .github/workflows/validator.yml
    command: python tools/validator/run_samples.py
    expected_sample_total: 34
    latest_pr_validation:
      pull_request: 5
      run_id: 29143048337
      run_number: 33
      conclusion: success
  specified_not_implemented:
    - protected wording semantic equivalence lint for SG references
    - parent-child Safety Gate inheritance lint
    - aggregate composite state calculation
    - full trigger context parser
  not_scope:
    - semantic equivalence proof
    - safety proof
    - full template expansion proof
    - full YAML parser
    - full natural-language parser
    - full negation parser
    - runtime verification
    - user approval
    - execution authority
    - release readiness judgment
```

Constraints:

```text
validator未実行→pass扱禁止
validator pass != U承認
validator pass != RT:v
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != safety proof
validator pass != execution authority
validator pass != release readiness
CI pass != U承認
CI pass != RT:v
CI pass != semantic equivalence
CI pass != safety proof
CI pass != stable/public-ready判断
CI pass != tag/release/Release Assets許可
Safety Gate validator pass != Packet/R1C readiness
```

## 6. Safety status

```text
意味保持 > safety gate保持
safety > high-risk判定 > mode > profile
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
KDSL_RESULT NEXT:=提案, 実行許可扱禁止
KDSL_RESULT COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
public履歴/公開済tag/Release Assets保護
lexicon != mode/profile
unknown profile/mode/safety/lexicon/envelope/registry/ID推測禁止
構造aliasはKEY位置のみ
保護語の一字短縮禁止
KDSL-CP実装指示禁止
Registry ID != permission
state:satisfied != unrelated authority
hold/blocked gate削除禁止
specialized gate != broader gate解除
current Full KDSL:=SG ID + complete protected wording
SG ID-only compression禁止
KDSL-Packet直接実行禁止
PKT:v1使用禁止
```

## 7. Validation evidence

### CompactPrompt Windows verification

```yaml
compact_prompt_windows_validation:
  date: 2026-07-11
  environment: Windows PowerShell 5.1 / repository checkout
  branch: agent/kdsl-compact-validator
  verified_implementation_head: 2b50ed1
  command: python tools/validator/run_samples.py
  total: 23
  failed: 0
  compact_examples: 4/4 pass
  worktree: clean
  branch_tracking: synchronized
  diff_check: pass
```

### Safety Gate validator verification

```yaml
safety_gate_validator_validation:
  date: 2026-07-11
  isolated_direct_cases: 8
  isolated_unexpected_exits: 0
  pull_request: 5
  source_head: bc49316ba83ef59a7c49f6ae24a29f581e2ea16c
  workflow: Validator CI
  workflow_run_id: 29143048337
  run_number: 33
  status: completed
  conclusion: success
  sample_total: 34
  failed: 0
  actual_repository_example: pass
  meaning: expected exit-code regression check only
```

Verification details:

```text
tools/validator/verification/kdsl_compact_prompt_verify.md
tools/validator/verification/kdsl_safety_gate_verify.md
docs/reviews/kdsl-validator-ci-baseline.md
docs/reviews/kdsl-safety-gate-registry-design.md
docs/reviews/kdsl-safety-gate-registry-integration.md
docs/reviews/kdsl-safety-gate-validator-first-slice.md
```

## 8. Known gaps before stable

```text
full YAML parserなし
full natural-language semantic parserなし
full negation parserなし
protected wording semantic equivalence lintなし
Safety Gate parent-child inheritance lintなし
Safety Gate aggregate state lintなし
R1C schema未定義
Packet schema未定義
BASE/TASK/FLOW registry未定義
Packet lint未定義
KDSL-Packetはdraft-non-executable
v2 public-facing overview未確定
CI required check/branch protection未設定
```

## 9. Recommended positioning

```text
Use as:
  experimental preview
  safety-gate-preserving prompt notation draft
  CompactPrompt architecture draft
  Safety Gate Registry v2-draft
  heuristic validator helper
  validator sample CI baseline
  internal/public review candidate

Do not present as:
  stable standard
  production-ready validator suite
  proof system
  approval/runtime/release substitute
  SG ID-only executable contract
  executable Packet specification
```

## 10. Next safe steps

```text
P0: local mainをorigin/mainへ同期 / 34 sample runner再確認
P1: R1C compact schema設計
P2: Packet BASE/TASK/FLOW registry・schema・lint設計
P3: Safety Gate protected wording/inheritance validator拡張
P4: public-facing v2 overview検討
P5: CI required check / branch protection化は別途U明示承認後に検討
Hold: v1.1.0 stable / tag / release / Release Assets
```
