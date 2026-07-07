# Public Readiness Notes

status: rc1-experimental-preview
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

## 2. Reasons not to treat as stable yet

```text
仕様がdraft/preview段階
validatorはpartial heuristic lint helpers
外部向けREADME/導入ガイドがdraft
用語が内部運用寄り
MidFD実例が内部文脈を含む
KDSL-DP/ADPS境界が公開説明にはまだ重い
sample期待値はrunnerで固定中
GitHub Actions未構成
```

## 3. Publicization risks

```text
未成熟な仕様が外部に正本扱いされる
KDSL-DPを実行指示と誤解される
RT:v条件が簡略化され、build passと混同される
NEXT/COMMITの権限分離が抜ける
AI coding promptの安全gateが外部で弱化される
validator passが承認/RT:v/release readinessの代替に見える
```

## 4. Minimum before stable public release

stable化前に必要:

```text
public-facing READMEの確定
introductory overviewの確定
minimal examples without private/MidFD-specific context
KDSL-DP boundary warningの目立つ配置
R1 quickstart
validator maturity/limitationsの明記
template usage warning
sample expectation runner確認
GitHub Actions検討
stable tag/release policy
U明示承認
```

## 5. Candidate stable public package

公開可能な最小subset候補:

```text
README.md
LICENSE
spec/core/*
spec/r1/r1-result-spec.md
spec/lint/kdsl-lint-checklist.md
spec/bridge/kdsl-adps-bridge.md
spec/manifest.md
spec/glossary.md
docs/project-status.md
docs/overview.md
examples/public/*
tools/validator/README.md
tools/validator/run_samples.py
```

## 6. Public messaging draft

```text
KDSL is a safety-gate-preserving semi-structured prompt notation for Human-AI work contracts.
R1 is an evidence-oriented result specification for reviewing AI-assisted work.
This project is an experimental preview.
Validator helpers are heuristic lint tools, not proof systems or release authorities.
License: MIT.
```

日本語案:

```text
KDSLは、AIへの作業指示から禁止・承認・未確認・停止条件を落とさないための半構造化prompt記法です。
R1は、AIの作業結果を人間が検収可能にするための結果証跡仕様です。
この仕様はexperimental previewです。
validator helperはヒューリスティックなlint補助であり、証明器や承認者ではありません。
License: MIT。
```

## 7. Public readiness checklist

| Check | Required for stable | Status |
|---|---:|---|
| LICENSE decided | yes | MIT |
| External README | yes | draft |
| Private examples removed or separated | yes | partial |
| KDSL-DP warning prominent | yes | partial |
| R1 quickstart | yes | pending |
| Validator implementation status clear | yes | partial / heuristic |
| Sample expectation runner | yes | added |
| GitHub Actions | no | not_configured |
| No public release assets | yes | pass |
| Tag policy clear | yes | partial |

## 8. Recommendation

```text
Keep public experimental preview.
Do not present as stable/public-ready.
Do not attach Release Assets.
Do not create stable v1.1.0 without U explicit approval.
```
