# Public Readiness Notes

status: v2-draft-hardening
last_updated: 2026-07-12
project_status: docs/project-status.md
public_recommendation: experimental_preview_only
stable_recommendation: not_yet
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

現時点の判断は「公開済み experimental preview」とする。
正式なpublic-ready/stable releaseではない。

## 2. Current validation evidence

```text
workflow: .github/workflows/validator.yml
workflow_name: KDSL Validation
unified_runner: python tools/validator/run_all_samples.py
focused_job: Packet Semantic Property
latest_verified_merged_pr: #50 / success
current_candidate_pr: #51 / validation success recorded in PR
unified_expectations: 257
failed: 0
required_check_activation: pending / issue #39
validator_authority: non_authoritative
```

Merge condition for each candidate:

```text
latest candidate HEADのKDSL Validation成功必須
latest candidate HEADのPacket Semantic Property成功必須
過去run成功のみで最新HEAD成功扱禁止
```

境界:

```text
workflow success != required-check activation
validator pass != semantic equivalence proof
validator pass != complete safety proof
validator pass != RT:v
validator pass != U承認
validator pass != release readiness
```

## 3. Phase 5 public-facing candidates

```text
Core formal axes sync: main integrated by PR #50
Glossary formal axes sync: main integrated by PR #50
Converter GitHub source priority/A-G/CP-Lift sync: main integrated by PR #50
External README simplification: PR #51 candidate
Introductory overview refresh: PR #51 candidate
R1 quickstart: PR #51 candidate
Public example boundary guide: PR #51 candidate
Public R1 examples current-contract alignment: PR #51 candidate
KDSL-DP normalization-path correction: PR #51 candidate
obsolete public README draft retirement: PR #51 candidate
```

Candidate integration does not change stable/public-ready status.

## 4. Reasons not to treat as stable yet

```text
仕様がdraft/preview段階
validatorはpartial heuristic lint helpers
public-facing documentsはPhase 5 review中
用語の一部が内部運用寄り
full YAML/KDSL semantic parserなし
full natural-language negation/exception reasoningなし
full semantic equivalence/safety proofなし
KDSL-Packetはnon-executable
required KDSL Validation repository setting未設定
release-readiness final review未完了
U stable/public-ready明示承認なし
```

## 5. Publicization risks

```text
未成熟な仕様が外部にstable/canonical standard扱いされる
KDSL-DPを実行指示と誤解される
Packet draftを実行契約と誤解される
RT:v条件が簡略化され、build/test passと混同される
NEXT/COMMITの権限分離が抜ける
AI coding promptのsafety gateが外部で弱化される
validator passが承認/RT:v/release readinessの代替に見える
public exampleが実行権限に見える
```

## 6. Minimum before stable public release

stable化前に必要:

```text
public-facing README確定
introductory overview確定
Core/Profile/Glossary正式値同期
minimal public examples確定
KDSL-DP boundary warning確認
Packet non-executable boundary warning確認
R1 quickstart確定
validator maturity/limitations確認
template/example non-normative warning確認
sample expectation runner確認
required KDSL Validation check activation
stable tag/release policy確定
release-readiness final review
U明示承認
```

## 7. Candidate stable public package

```text
README.md
LICENSE
spec/core/*
spec/profiles/*
spec/r1/r1-result-spec.md
spec/lint/kdsl-lint-checklist.md
spec/bridge/kdsl-adps-bridge.md
spec/manifest.md
spec/glossary.md
docs/project-status.md
docs/overview.md
docs/r1-quickstart.md
examples/public/*
tools/validator/README.md
tools/validator/run_all_samples.py
.github/workflows/validator.yml
```

Packet/R1C/Safety Semantics v2-draft subordinate filesをstable packageへ含めるかは、release-readiness reviewで別途判定する。

## 8. Public messaging candidate

```text
KDSL is a safety-gate-preserving semi-structured prompt notation for Human-AI work contracts.
R1 is an evidence-oriented result specification for reviewing AI-assisted work.
This project is an experimental preview.
Validator helpers are heuristic lint tools, not proof systems or release authorities.
KDSL-Packet remains non-executable.
License: MIT.
```

日本語案:

```text
KDSLは、AIへの作業指示から禁止・承認・未確認・停止条件を落とさないための半構造化prompt記法です。
R1は、AIの作業結果を人間が検収可能にするための結果証跡仕様です。
この仕様はexperimental previewです。
validator helperはヒューリスティックなlint補助であり、証明器や承認者ではありません。
KDSL-Packetは現在もnon-executableです。
License: MIT。
```

## 9. Public readiness checklist

| Check | Required for stable | Status |
|---|---:|---|
| LICENSE decided | yes | MIT |
| External README | yes | candidate / PR #51 |
| Introductory overview | yes | candidate / PR #51 |
| Core/Profile/Glossary v2 alignment | yes | partial / Core+Glossary+Converter integrated |
| Private examples excluded from candidate subset | yes | pass |
| Public examples non-normative boundary | yes | candidate / PR #51 |
| KDSL-DP warning prominent | yes | candidate / PR #51 |
| Packet non-executable warning prominent | yes | candidate / PR #51 |
| R1 quickstart | yes | candidate / PR #51 |
| Validator implementation status clear | yes | candidate / heuristic |
| Unified sample expectation runner | yes | 257 / failed 0 |
| GitHub Actions workflow | yes | configured |
| Required KDSL Validation check | yes | pending / issue #39 |
| No public release assets | yes | pass |
| Existing tag movement prohibited | yes | pass |
| Stable tag/release policy | yes | partial |
| Release-readiness review | yes | pending |
| U explicit stable approval | yes | pending |

## 10. Recommendation

```text
Keep public experimental preview.
Continue Phase 5 public-facing v2 hardening.
Do not present as stable/public-ready.
Do not attach Release Assets.
Do not move existing tags.
Do not create stable v1.1.0 without U explicit approval.
```
