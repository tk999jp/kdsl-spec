# Public Readiness Notes

status: phase5-public-hardening-integrated
last_updated: 2026-07-12
project_status: docs/project-status.md
public_recommendation: experimental_preview_only
stable_recommendation: not_ready
license: MIT

## 1. Current decision

```text
public: yes
release: v1.1.0-rc1
release_class: experimental preview
public_ready: no
stable_release: none
Release Assets: none
tag: v1.1.0-rc1
license: MIT
```

Phase 5のpublic-facing hardeningとrequired-check repository enforcementは統合済みです。
ただし、これはpublic-ready/stable release承認ではありません。

```text
public documentation hardening: complete
required KDSL Validation ruleset: active
stable readiness: not_ready
stable/public-ready authority: none
```

## 2. Phase 5 integration evidence

```text
PR #50:
  squash_commit: 49b6c865af046d44efc04a46d851aed55d222a61
  workflow_run: 239 / success
  scope: Core / Glossary / Converter synchronization

PR #51:
  squash_commit: 442d53226c7d0fd000ed1f93efc28ccbb367b129
  workflow_run: 246 / success
  scope: README / Overview / R1 Quickstart / public examples

PR #52:
  squash_commit: 88f3d94b0c5915a74f3654e0407bffda3bb9f4c3
  workflow_run: 250 / success
  scope: Phase 5 closeout / status canonical reorganization
```

Validation scope:

```text
workflow: .github/workflows/validator.yml
jobs:
  KDSL Validation
  Packet Semantic Property
unified_expectations: 257
failed: 0
validator_authority: non_authoritative
```

## 3. Repository enforcement

```text
ruleset_name: Protect main with KDSL Validation
ruleset_id: 18832171
status: Active
target: default branch / main
bypass_list: empty
require_pull_request_before_merging: yes
required_approvals: 0
allowed_merge_method: Squash
required_status_check: KDSL Validation
require_branch_up_to_date: yes
restrict_deletions: yes
block_force_pushes: yes
```

Verification evidence:

```text
U共有Settings画面: Ruleset created / Active / applies to main
verification_pull_request: 53
verification_head: b78ee593d6dfb42a6edfce53701c510b39f83067
workflow_run: 252 / success
merge: not executed
close_without_merge: completed
```

```text
required KDSL Validation activation: confirmed
workflow success != semantic equivalence proof
workflow success != complete safety proof
workflow success != RT:v
workflow success != release readiness
```

## 4. Completed experimental-preview criteria

```text
public-facing README: integrated
introductory overview: integrated
Core/Profile/Glossary formal axes: synchronized
Converter source priority and A-G contract: synchronized
minimal public examples: separated and non-normative
KDSL-DP direct-execution warning: prominent
Packet non-executable warning: prominent
R1 quickstart: integrated
validator maturity/limitations: explicit
example/template authority warning: explicit
sample expectation runner: configured
GitHub Actions workflow: configured
required KDSL Validation ruleset: active
existing tag movement prohibition: retained
Release Assets prohibition: retained
```

## 5. Stable/public-ready blockers

Repository enforcement is no longer a blocker.
The remaining blockers are specification maturity and release authority.

### Specification maturity

```text
full YAML/KDSL semantic parser: not implemented
full natural-language negation/exception reasoning: not implemented
full semantic equivalence proof: not proven
complete safety proof: not proven
Packet normalization completion: not proven
KDSL-Packet: non-executable
canonical P1/P1L target schema: unresolved
```

These gaps do not invalidate the experimental preview. They prevent claiming production-grade proof or executable Packet readiness.

### Release authority

```text
U stable/public-ready explicit approval: not granted
stable tag creation authority: none
release authority: none
Release Assets authority: none
```

## 6. Release-readiness decision

```text
review_status: complete
public_experimental_preview: continue
repository_enforcement: active
public_ready: no
stable_release: no
release_candidate_promotion: no
Packet executable promotion: no
```

Reason:

```text
public-facing documentation is sufficient for experimental preview use
required repository enforcement is active
validator remains non-authoritative/partial
semantic/safety completion is not proven
stable/public-ready U approval is absent
```

## 7. Publicization risks retained

```text
experimental previewがstable/canonical standard扱いされる
KDSL-DPが実行指示と誤解される
Packet draftが実行契約と誤解される
RT:vがbuild/test/CI passと混同される
NEXT/COMMITの権限分離が抜ける
validator passが承認/RT:v/release readinessの代替に見える
public exampleが実行権限に見える
```

## 8. Public package for experimental preview

```text
README.md
LICENSE
spec/core/*
spec/profiles/*
spec/lexicons/*
spec/registry/*
spec/packet/*
spec/r1/*
spec/lint/*
spec/bridge/*
spec/manifest.md
spec/glossary.md
spec/glossary-v2-draft.md
docs/project-status.md
docs/overview.md
docs/r1-quickstart.md
docs/public-readiness.md
examples/public/*
tools/validator/README.md
tools/validator/run_all_samples.py
.github/workflows/validator.yml
```

The inclusion of v2-draft subordinate files does not promote them to stable/canonical executable specifications.

## 9. Public messaging

```text
KDSL is a safety-gate-preserving semi-structured prompt notation for Human-AI work contracts.
R1 is an evidence-oriented result specification for reviewing AI-assisted work.
This project is a public experimental preview, not a stable standard.
Validator helpers are heuristic lint tools, not proof systems or release authorities.
KDSL-Packet remains non-executable.
License: MIT.
```

日本語:

```text
KDSLは、AIへの作業指示から禁止・承認・未確認・停止条件を落とさないための半構造化prompt記法です。
R1は、AIの作業結果を人間が検収可能にするための結果証跡仕様です。
このrepositoryは公開済みexperimental previewであり、stable standardではありません。
validator helperはヒューリスティックなlint補助であり、証明器や承認者ではありません。
KDSL-Packetはnon-executableです。
License: MIT。
```

## 10. Final checklist

| Check | Required for experimental preview | Required for stable | Status |
|---|---:|---:|---|
| LICENSE | yes | yes | pass / MIT |
| Public README | yes | yes | pass |
| Overview | yes | yes | pass |
| Core/Profile/Glossary alignment | yes | yes | pass |
| Public examples separated | yes | yes | pass |
| KDSL-DP warning | yes | yes | pass |
| Packet non-executable warning | yes | yes | pass |
| R1 quickstart | yes | yes | pass |
| Validator limitations clear | yes | yes | pass |
| Unified sample runner | yes | yes | pass / 257 |
| GitHub Actions workflow | yes | yes | pass |
| Required KDSL Validation ruleset | no | yes | pass / active |
| No Release Assets | yes | until approved | pass |
| Existing tag movement prohibited | yes | yes | pass |
| Release-readiness review | yes | yes | complete / not_ready |
| U explicit stable approval | no | yes | pending |

## 11. Next safe steps

```text
P0: integrate activation closeout and close Issue #39
P1: continue semantic/parser/safety proof maturation as separate phases
Hold: stable tag/release/Release Assets/public-ready promotion
```

```text
NEXT:=proposal only
NEXT実行許可扱禁止
stable/public-ready化→別途U明示承認必須
```
