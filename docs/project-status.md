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

## 3. Current validator workstream

```yaml
compact_prompt_validator_workstream:
  branch: agent/kdsl-compact-validator
  target_branch: main
  status: experimental_first_slice
  merge_status: not_merged
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

Direction:

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft architecture:=main統合済み
CompactPrompt validator:=first slice review中
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
    - required block presence lint
    - RT:v basis wording heuristic lint
    - NEXT/COMMIT authority-shape heuristic lint
    - template reference lint
    - template expansion evidence lint
  candidate_branch_scope:
    - CompactPrompt required block lint
    - CompactPrompt mode/safety/lexicon lint
    - kanji-v1 restricted alias lint
    - representative CP-Lift lint
    - Packet draft boundary lint
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
isolated test pass != full sample runner pass
validator pass != U承認
validator pass != RT:v
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != release readiness
```

## 6. Safety status

```text
意味保持 > safety gate保持
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test pass != RT:v
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

## 7. Validation and integration evidence

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
compact_prompt_isolated_validation:
  date: 2026-07-11
  method: isolated local Python execution
  direct_cases:
    standard_valid: 0
    kanji_valid: 0
    missing_block: 2
    restricted_alias: 2
    cp_lift_required: 2
  wrapper_cases:
    compact_valid: 0
    compact_invalid: 2
  existing_example_spot_checks:
    prompt_improver: 0
    blog_meta_kanji_corrected: 0
    novel_review_kanji_corrected: 0
  full_repository_runner: not_executed
```

```text
isolated validation details:
  tools/validator/verification/kdsl_compact_prompt_verify.md

expected post-change sample count:
  23
```

## 8. Known gaps before validator merge or stable

```text
full repository sample runner未実行
Windows PowerShell/Python環境でのcheckout確認未実行
GitHub Actions未構成
full parserなし
full natural-language semantic parserなし
full negation parserなし
Packet schema/BASE/TASK/FLOW/SG/R1C registry未定義
KDSL-Packetはdraft-non-executable
v2 public-facing overview未確定
```

## 9. Recommended positioning

```text
Use as:
  experimental preview
  safety-gate-preserving prompt notation draft
  CompactPrompt architecture draft
  heuristic validator helper candidate
  internal/public review candidate

Do not present as:
  stable standard
  production-ready validator suite
  proof system
  approval/runtime/release substitute
  executable Packet specification
```

## 10. Next safe steps

```text
P0: agent/kdsl-compact-validatorをlocal checkout
P1: python tools/validator/run_samples.py
P2: CompactPrompt examplesを--target compactで検証
P3: sample total=23 / failed=0確認後にPR review/merge判断
P4: R1C / Safety Gate registry / Packet registryを別Phaseで検討
Hold: v1.1.0 stable / tag / release / Release Assets
```
