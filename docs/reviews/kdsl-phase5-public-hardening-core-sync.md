# Phase 5 — Public-facing v2 hardening / Core sync

status: implementation-candidate
review_date: 2026-07-12
branch: agent/kdsl-phase5-public-hardening-core-sync
target: main

## Scope

```text
Core formal profile values synchronized with v2 manifest
lexicon/envelope axes added to Core entry contract
rulebook classified as v1.1 legacy compatibility name
legacy rulebook automatic correction prohibited
public readiness GitHub Actions evidence refreshed
required check activation retained as pending / issue #39
```

## Decision

```text
formal profile values:
  compact-prompt
  dev-prompt
  converter
  lint

legacy:
  rulebook
```

`rulebook` has no current profile canonical file and appears only in legacy Core/Glossary text. It is retained as a compatibility name but is not a formal v2 profile value.

```text
rulebook新規使用禁止
rulebookを正式v2 profile扱い禁止
legacy rulebook入力→用途確認なしにcompact-prompt/lintへ自動補正禁止
```

## Public readiness correction

Previous public-readiness text stated that GitHub Actions was not configured. Current repository evidence shows:

```text
workflow: .github/workflows/validator.yml
jobs:
  KDSL Validation
  Packet Semantic Property
latest_verified_run: #224
unified_expectations: 257
failed: 0
```

Boundary retained:

```text
workflow success != required-check activation
validator pass != semantic equivalence proof
validator pass != complete safety proof
validator pass != RT:v
validator pass != U承認
validator pass != release readiness
```

## Non-actions

```text
stable/public-ready promotionなし
tag/release/Release Assets操作なし
Packet executable化なし
R1C canonical replacementなし
semantic equivalence/safety proof宣言なし
required repository check有効化なし
main直接更新なし
```

## Remaining Phase 5 work

```text
spec/glossary.md formal profile wording sync
converter profile source-of-truth and A-G selection sync
README/overview public-facing simplification
R1 quickstart
external example separation
required KDSL Validation check activation / issue #39
release-readiness final review
```
