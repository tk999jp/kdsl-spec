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
ただし、正式なpublic-ready/stable releaseではない。

## 2. Current validation evidence

```text
workflow: .github/workflows/validator.yml
workflow_name: KDSL Validation
unified_runner: python tools/validator/run_all_samples.py
focused_job: Packet Semantic Property
latest_verified_pr: #48
latest_verified_run: #224
unified_expectations: 257
failed: 0
required_check_activation: pending / issue #39
validator_authority: non_authoritative
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

## 3. Reasons not to treat as stable yet

```text
仕様がdraft/preview段階
validatorはpartial heuristic lint helpers
外部向けREADME/導入ガイドがdraft
Core/Profile/Glossaryのv2 public-facing同期が進行中
用語が内部運用寄り
MidFD実例が内部文脈を含む
KDSL-DP/ADPS境界が公開説明にはまだ重い
full YAML/KDSL semantic parserなし
full semantic equivalence/safety proofなし
KDSL-Packetはnon-executable
required KDSL Validation repository setting未設定
```

## 4. Publicization risks

```text
未成熟な仕様が外部にstable/canonical standard扱いされる
KDSL-DPを実行指示と誤解される
Packet draftを実行契約と誤解される
RT:v条件が簡略化され、build/test passと混同される
NEXT/COMMITの権限分離が抜ける
AI coding promptの安全gateが外部で弱化される
validator passが承認/RT:v/release readinessの代替に見える
```

## 5. Minimum before stable public release

stable化前に必要:

```text
public-facing READMEの確定
introductory overviewの確定
Core/Profile/Glossaryの正式値同期
minimal examples without private/MidFD-specific context
KDSL-DP boundary warningの目立つ配置
Packet non-executable boundary warningの目立つ配置
R1 quickstart
validator maturity/limitationsの明記
template usage warning
sample expectation runner確認
required KDSL Validation check activation
stable tag/release policy
release-readiness review
U明示承認
```

## 6. Candidate stable public package

公開可能な最小subset候補:

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
examples/public/*
tools/validator/README.md
tools/validator/run_all_samples.py
.github/workflows/validator.yml
```

Packet/R1C/Safety Semantics v2-draft subordinate filesをstable packageへ含めるかは、release-readiness reviewで別途判定する。

## 7. Public messaging draft

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

## 8. Public readiness checklist

| Check | Required for stable | Status |
|---|---:|---|
| LICENSE decided | yes | MIT |
| External README | yes | draft |
| Introductory overview | yes | draft |
| Core/Profile/Glossary v2 alignment | yes | in_progress |
| Private examples removed or separated | yes | partial |
| KDSL-DP warning prominent | yes | partial |
| Packet non-executable warning prominent | yes | partial |
| R1 quickstart | yes | pending |
| Validator implementation status clear | yes | partial / heuristic |
| Unified sample expectation runner | yes | 257 / failed 0 |
| GitHub Actions workflow | yes | configured |
| Required KDSL Validation check | yes | pending / issue #39 |
| No public release assets | yes | pass |
| Tag policy clear | yes | partial |
| Release-readiness review | yes | pending |
| U explicit stable approval | yes | pending |

## 9. Recommendation

```text
Keep public experimental preview.
Continue Phase 5 public-facing v2 hardening.
Do not present as stable/public-ready.
Do not attach Release Assets.
Do not move existing tags.
Do not create stable v1.1.0 without U explicit approval.
```
