# Phase 6C-4 — CompactPrompt Checker Structural Migration

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 65
implementation_source_head: 58da11b3d9089c97716692d18585fbab23ca4f2d
implementation_squash_commit: 4d4a5f7b6580ecec44636f8e09e163540fb17770
workflow_run_id: 29230246858
workflow_run_number: 297
workflow_conclusion: success

## 1. Goal

Move CompactPrompt structural extraction to the integrated AST v2 compatibility view without changing semantic or safety decisions.

```text
structure migration only
legacy-v2 parity guard retained
semantic/safety policy unchanged
```

## 2. Integrated runtime path

```text
input
→ CompactPromptCompatibilityView
→ legacy-v2 structural parity guard
→ mismatch: fail before semantic validation
→ match: AST v2 scope/header/block/duplicate extraction
→ existing CompactPrompt semantic and safety checks
```

Active files:

```text
tools/validator/kdsl_compact_prompt.py
tools/validator/kdsl_parser_v2_compact_compat.py
tools/validator/kdsl_parser_v2_compact_parity.py
```

## 3. Migrated structural surface

```text
CompactPrompt detection
KDSL-CP / KDSL-CP漢 shorthand
legacy-compatible scope
profile/mode/safety/lexicon header values
standard structural blocks
kanji-v1 structural blocks
block order/content
same-key duplicate order
```

The active checker now obtains this surface from `CompactPromptCompatibilityView`.

## 4. Legacy parity guard

The legacy extraction helpers remain in `kdsl_compact_prompt.py` only as the comparison side of the in-process guard.

```text
detect_profile
detect_shorthand
extract_scope
header_value
parse_blocks
```

A structural mismatch is emitted as:

```text
CompactPrompt parser parity guard: <mismatch>
```

and validation stops before semantic decisions.

```text
parity failure→fail closed
parity pass→semantic validation may continue
parity pass != semantic equivalence
```

## 5. Semantic and safety policy retained

Unchanged:

```text
mode:=readable|min|dense|lock
safety:=normal|lock-critical|lock-all
lexicon:=standard|kanji-v1
mode:dense-ja prohibition
KDSL-CP漢 mode/lexicon conflict checks
required/empty block decisions
mixed standard/kanji warning
same-key duplicate warning
restricted free-text alias detection
CP-Lift trigger detection
CP-Lift prohibition-clause exception behavior
PKT:v1 prohibition
PACKET_DRAFT non-executable marker checks
```

Critical boundary:

```text
implementation/repo/runtime/public/data/source-of-truth/AI coding trigger→CP-Lift
CP-Lift先:=profile:dev-prompt
KDSL-CP漢 alias:=構造KEY位置のみ
```

## 6. Permanent migration corpus

Added active-checker cases:

```text
profile-only / no shorthand: pass
same-key duplicate block: warn
mixed standard/kanji structural keys: warn
Markdown fenced scope with trigger wording after fence: pass
```

Added equivalent parity cases for the same four inputs.

The fenced case proves that notes following the closing fence are not interpreted as active CompactPrompt instructions and therefore do not trigger CP-Lift.

## 7. Verification

```text
workflow run: 29230246858 / #297
KDSL Validation: success
Packet Semantic Property: success
```

Corpus totals:

```text
Phase 1 parser/adapter: 11 / failed 0
Phase 6B parser-v2: 12 / failed 0
Phase 6C R1C parity: 10 / failed 0
Phase 6C CompactPrompt parity: 12 / failed 0
CompactPrompt checker migration: 4 / failed 0
unified runners: 12
unified expectations: 295 / failed 0
```

The 295 total is the prior 287 expectations plus four parity cases and four active-checker migration cases.

## 8. Authority boundary

```text
validator/CI pass != semantic equivalence
validator/CI pass != complete safety proof
validator/CI pass != U approval
validator/CI pass != RT:v
validator/CI pass != execution authority
validator/CI pass != release readiness
```

No operation in this phase changed:

```text
stable/public-ready status
tag
release
Release Assets
Packet execution state
```

## 9. Current state

```text
CompactPrompt compatibility view: integrated
CompactPrompt parity checker: integrated
CompactPrompt active checker migration: integrated
legacy-v2 parity guard: active
CP-Lift semantics: unchanged
restricted alias semantics: unchanged
Packet boundary semantics: unchanged
```

## 10. Remaining migration targets

```text
Safety Gate compatibility view/migration
Packet compatibility view/migration
Packet Normalization compatibility view/migration
Full R1 compatibility view/migration
Phase 6D mutation/property/repository corpus
legacy adapter retirement decision
```

The Phase 1 namespace adapter remains required by:

```text
kdsl_safety_gate.py
kdsl_packet.py
kdsl_packet_normalization.py
```

## 11. Next safe step

Recommended next phase:

```text
Phase 6C-5 Safety Gate compatibility view and parity pilot
```

Required boundary:

```text
Safety Gate records/registry/state/order extraction only
existing gate semantics and composition checks unchanged
checker switch deferred until parity evidence
```

## 12. Closeout decision

```text
Phase 6C-4 CompactPrompt checker migration: integrated
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
Packet executable: no
Packet state: not_normalized
public_ready: no
stable_release: none
Release Assets: none
```
