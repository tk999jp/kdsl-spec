# Public Readiness Notes

status: private-draft
public_recommendation: not_yet

## 1. Current decision

```text
public: not_yet
release: none
Release Assets: none
tag: not_created
```

現時点では、public化しない。

## 2. Reasons not to publish yet

```text
仕様がdraft段階
validator実装が未着手
外部向けREADME/導入ガイドが未整備
用語が内部運用寄り
MidFD実例が内部文脈を含む
ライセンス未判断
KDSL-DP/ADPS境界が公開説明にはまだ重い
```

## 3. Publicization risks

```text
未成熟な仕様が外部に正本扱いされる
KDSL-DPを実行指示と誤解される
RT:v条件が簡略化され、build passと混同される
NEXT/COMMITの権限分離が抜ける
AI coding promptの安全gateが外部で弱化される
```

## 4. Minimum before public

公開前に必要:

```text
LICENSE判断
public-facing README
introductory overview
minimal examples without private/MidFD-specific context
KDSL-DP boundary warning
R1 quickstart
template usage warning
tag/release policy
```

## 5. Candidate public package

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
docs/overview.md
examples/public/*
```

公開非推奨候補:

```text
examples/midfd/*
private operational templates with repo-specific assumptions
internal review notes
```

## 6. Public messaging draft

```text
KDSL is a safety-gate-preserving semi-structured prompt notation for Human-AI work contracts.
R1 is an evidence-oriented result specification for reviewing AI-assisted work.
This project is experimental and should not be used to bypass human approval, runtime verification, or release controls.
```

日本語案:

```text
KDSLは、AIへの作業指示から禁止・承認・未確認・停止条件を落とさないための半構造化prompt記法です。
R1は、AIの作業結果を人間が検収可能にするための結果証跡仕様です。
この仕様は、承認・実機確認・release判断を代替するものではありません。
```

## 7. Public readiness checklist

| Check | Required | Status |
|---|---:|---|
| LICENSE decided | yes | pending |
| External README | yes | pending |
| Private examples removed or separated | yes | pending |
| KDSL-DP warning prominent | yes | partial |
| R1 quickstart | yes | pending |
| Validator implementation status clear | yes | pass |
| No public release assets | yes | pass |
| Tag policy clear | yes | partial |

## 8. Recommendation

```text
Keep private.
Continue internal use and design refinement.
Do not create public release.
Do not attach Release Assets.
```
