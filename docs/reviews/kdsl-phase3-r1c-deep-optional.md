# Phase 3 — R1C Deep Optional-Block Round-Trip

status: implementation-candidate
review_date: 2026-07-12
branch: agent/kdsl-phase3-r1c-deep-optional
target: main

## Scope

```text
EVIDENCE exact classification lint
AUTHORITY six-rail deep lint
ANNUNCIATOR structural preservation
SAFETY_GATES dedicated expansion/reconstruction
cross-field contradiction checks
optional order/property mutation checks
```

## Selected model

```text
model: kdsl-r1c-optional-blocks@0.1-draft
parent: kdsl-r1c@0.1-draft
canonical parent: spec/r1/r1-result-spec.md
```

## Compatibility

```text
canonical R1 remains authoritative
R1C required field names/order unchanged
existing 181 unified expectations retained
valid SAFETY_GATES optional block moves from blocked to structural_pass
unknown/ambiguous/lossy optional block→fail / Full R1 fallback
```

## Verification target

```text
existing unified suite: 181 / failed 0
Phase 3 optional-block property suite: 34 / failed 0
expected unified total: 215 / failed 0
```

## Safety boundaries

```text
SEMANTIC_EQUIVALENCE:not_proven
FULL_SAFETY_PROOF:not_proven
EXECUTION_AUTHORITY:none
RT:v decision:none
```

## Non-actions

```text
Packet executable化なし
Packet normalized化なし
stable/tag/release/Release Assets操作なし
source branch削除なし
public-ready宣言なし
```
