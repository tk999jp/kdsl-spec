# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-11

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本は `spec/manifest.md` と `spec/core/*` / `spec/r1/*` / `spec/lint/*` / `spec/bridge/*` を参照します。

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

## 2. Integrated v2 architecture

```yaml
v2_compact_prompt_integration:
  source_branch: feature/kdsl-v2-compact-prompt
  target_branch: main
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

## 3. Integrated CompactPrompt validator

```yaml
compact_prompt_validator_integration:
  source_branch: agent/kdsl-compact-validator
  target_branch: main
  pull_request: 2
  merge_method: squash
  merge_status: merged
  squash_commit: c9e6dc5d8aaf4f5860fe2bab9d69247b41fc3b82
  verified_implementation_head: 2b50ed1
  verification_record_commit: 8edc0c2
  scope:
    - CompactPrompt profile/shorthand detection
    - mode/safety/lexicon value lint
    - required block lint
    - kanji-v1 restricted alias lint
    - representative CP-Lift trigger lint
    - Packet draft boundary lint
    - combined wrapper compact target
    - sample expectation integration
```

## 4. Integrated validator CI baseline

```yaml
validator_ci_integration:
  source_branch: agent/kdsl-validator-ci
  target_branch: main
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

Direction:

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft architecture:=main統合済み
CompactPrompt validator first slice:=main統合済み
Validator CI baseline:=main統合済み
stable/tag/release/Release Assets操作:=別途U明示承認必須
```

## 5. License state

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

## 6. Validator maturity

```yaml
validator:
  maturity: experimental_heuristic_helpers
  implementation: partial
  authority: non_authoritative
  current_main_scope:
    - required block presence lint
    - RT:v basis wording heuristic lint
    - NEXT/COMMIT authority-shape heuristic lint
    - template reference lint
    - template expansion evidence lint
    - CompactPrompt required block lint
    - CompactPrompt mode/safety/lexicon lint
    - kanji-v1 restricted alias lint
    - representative CP-Lift lint
    - Packet draft boundary lint
  ci:
    status: integrated
    workflow: .github/workflows/validator.yml
    command: python tools/validator/run_samples.py
    expected_sample_total: 23
  not_scope:
    - semantic equivalence proof
    - full template expansion proof
    - full natural-language parser
    - full negation parser
    - runtime verification
    - user approval
    - release readiness judgment
```

Constraints:

```text
validator未実行→pass扱禁止
validator pass != U承認
validator pass != RT:v
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != release readiness
CI pass != U承認
CI pass != RT:v
CI pass != semantic equivalence
CI pass != safety proof
CI pass != stable/public-ready判断
CI pass != tag/release/Release Assets許可
```

## 7. Safety status

```text
意味保持 > safety gate保持
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
KDSL_RESULT NEXT:=提案, 実行許可扱禁止
KDSL_RESULT COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
public履歴/公開済tag/Release Assets保護
lexicon != mode/profile
unknown lexicon/alias推測禁止
構造aliasはKEY位置のみ
保護語の一字短縮禁止
KDSL-CP実装指示禁止
Packet registry未定義→KDSL-Packet直接実行禁止
PKT:v1使用禁止
```

## 8. Validation and integration evidence

```yaml
main_sample_validation:
  date: 2026-07-07
  command: python tools/validator/run_samples.py
  result: pass
  total: 16
  failed: 0
  meaning: pre-CompactPrompt sample expectations passed locally
```

```yaml
compact_prompt_windows_validation:
  date: 2026-07-11
  environment: Windows PowerShell 5.1 / repository checkout
  branch: agent/kdsl-compact-validator
  verified_implementation_head: 2b50ed1
  full_sample_runner:
    command: python tools/validator/run_samples.py
    total: 23
    failed: 0
  examples:
    blog_meta_standard: pass
    blog_meta_kanji: pass
    novel_review_kanji: pass
    prompt_improver: pass
  repository_state:
    worktree: clean
    branch_tracking: synchronized
    diff_check: pass
```

```yaml
compact_prompt_validator_merge:
  pull_request: 2
  source_head: 45a526b52ac403169eca59d02af8e7b77f0e5d6e
  squash_commit: c9e6dc5d8aaf4f5860fe2bab9d69247b41fc3b82
  merged: true
  stable_effect: none
```

```yaml
validator_ci_pr_validation:
  date: 2026-07-11
  pull_request: 3
  source_head: dff75994c818e8a103bd2c94646c26ec8f8209d1
  workflow: Validator CI
  workflow_run_id: 29137196847
  run_number: 1
  status: completed
  conclusion: success
  expected_sample_summary: total 23 / failed 0
  squash_commit: 8505c16b44b4a95892e8d2f3f44119a2ad31afde
```

```text
verification details:
  tools/validator/verification/kdsl_compact_prompt_verify.md
  docs/reviews/kdsl-validator-ci-baseline.md
```

## 9. Known gaps before stable

```text
full parserなし
full natural-language semantic parserなし
full negation parserなし
Packet schema/BASE/TASK/FLOW/SG/R1C registry未定義
KDSL-Packetはdraft-non-executable
v2 public-facing overview未確定
```

## 10. Recommended positioning

```text
Use as:
  experimental preview
  safety-gate-preserving prompt notation draft
  CompactPrompt architecture draft
  heuristic validator helper
  validator sample CI baseline
  internal/public review candidate

Do not present as:
  stable standard
  production-ready validator suite
  proof system
  approval/runtime/release substitute
  executable Packet specification
```

## 11. Next safe steps

```text
P0: local mainをorigin/mainへ同期
P1: R1C / Safety Gate registry / Packet registryを別Phaseで設計
P2: public-facing v2 overview検討
P3: CI required check / branch protection化は別途U明示承認後に検討
Hold: v1.1.0 stable / tag / release / Release Assets
```
