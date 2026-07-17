# Phase 8 — Shared AST v2 P1L First-Class Integration

status: validation-candidate
tracking_issue: 128
base: main@220547f0aa8f5c5ef95dec5387f7942f50fc9511
implementation_head: fac700a82986144d49d8077c078e75f4c7b5d0ef

## Goal

Promote `P1L:` recognition from checker-local mutation into the shared typed AST v2 parser while preserving all non-executable contract boundaries.

## Change

```text
shared KNOWN_ENVELOPES += P1L
legacy colon-P1 detection → kdsl_p1_contract.py
P1/P1L consumers → kdsl_p1_contract imports
kdsl_p1_bootstrap.py → removed
```

## Compatibility requirements

```text
P1L raw-envelope parse remains structurally identical
active-document fenced examples remain inert
P1 compact line remains dedicated-scanner input, not AST envelope
legacy colon P1 remains blocked
Packet P1 normalization/property consumers remain unchanged semantically
```

## Targeted validation

```text
Phase 8 shared AST compatibility corpus: success
P1L/P1 contract corpus: 14 / failed 0
Packet→P1L/P1 normalization corpus: 17 / failed 0
clean branch implementation job: 29612877656 / success
```

The targeted result is implementation evidence only. Required repository checks must still run on the review head before merge.

## Non-executable boundary

```text
P1L AST recognition != executable contract
BINDING.executable:false
Packet remains non-executable/not_normalized
semantic_equivalence:not_proven
execution_authority:none
RT:v/NEXT/COMMIT meanings unchanged
```

## Non-goals

```text
runtime binding
K1/PF1 schema
P1 compact AST redesign
Packet normalized-state promotion
stable/public-ready/tag/release/Release Assets operations
```
