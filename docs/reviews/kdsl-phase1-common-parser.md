# Phase 1 — Common Parser / Validation Foundation

status: implementation-candidate
review_date: 2026-07-12
repository: tk999jp/kdsl-spec
base: main@ca258df765a93ac7e1fed64a2d845897c78fa7cd

## Scope

```text
common source-spanned parser/AST
common diagnostics
major-checker legacy adapters
multiline JSON-compatible field handling
parser positive/negative samples
unified all-suite runner
stable required-check workflow name
required-check activation runbook
```

## Architecture

```text
raw UTF-8 text
→ DocumentNode
→ EnvelopeNode
→ ordered FieldNode + SourceSpan
→ checker adapter
→ existing semantic checker
→ common diagnostic/result surface
```

The parser does not reinterpret protected wording, Safety Gate state, authority, or runtime evidence.

## Migrated checkers

```text
R1C
Packet
Packet Normalization
Safety Gate
```

Existing semantic rules remain authoritative. Adapter use must preserve all existing expected exits.

## Validation plan

```text
existing core/Packet/Normalization suite
Safety Gate extension suite
R1C round-trip/property suite
new parser/AST suite
unified aggregate runner
```

## CI model

Final workflow/check name:

```text
workflow: KDSL Validation
job/check: KDSL Validation
```

This name is intentionally stable so it can be selected as the required status check for `main`.

## Required-check limitation

The connected GitHub tool can edit workflow files and PRs but does not expose repository ruleset or branch-protection mutation. Therefore:

```text
workflow/check implementation:=in scope
required-check repository setting:=manual activation runbook
activation status must not be claimed until GitHub settings evidence exists
```

## Non-actions

```text
semantic equivalence claimなし
Safety Gate自動satisfied化なし
authority付与なし
RT:v判定変更なし
Packet executable化なし
stable/tag/release/Release Assets操作なし
```
