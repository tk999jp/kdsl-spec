# Phase 2 — Safety Semantics / Multi-Generation Inheritance

status: implementation-candidate
review_date: 2026-07-12
branch: agent/kdsl-phase2-safety-semantics
target: main

## Scope

```text
bounded protected-language semantic IR
strong/weak concept patterns by Safety Gate ID
condition/exception atom capture
deep scope relation model
multi-generation DAG inheritance
multi-parent aggregate conflict handling
property and repository-example suites
```

## Selected boundary

```text
model: kdsl-safety-language@0.1-draft
FULL_SEMANTIC_EQUIVALENCE:not_proven
FULL_SAFETY_PROOF:not_proven
EXECUTION_AUTHORITY:none
```

## Compatibility

```text
existing Safety Gate registry IDs/states unchanged
pairwise checker warning compatibility retained
new graph checker is strict deep-scope enforcement surface
existing 147 expectations must remain unchanged
```

## Required verification

```text
existing unified suite: 147 / failed 0
Phase 2 property suite: 32 / failed 0
Phase 2 repository examples: 2 / failed 0
expected unified total: 181 / failed 0
```

## Non-actions

```text
Safety Gate automatic satisfactionなし
full natural-language semantic proofなし
authority付与なし
RT:v判定なし
Packet executionなし
stable/tag/release/Release Assets操作なし
```
