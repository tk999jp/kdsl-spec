# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-active
phase1_pull_request: 38
phase1_squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
phase6_tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Replace duplicated envelope and field scanning with one source-spanned parser foundation while preserving the existing semantic validators and their safety boundaries.

```text
parser/AST != semantic equivalence proof
parser/AST != safety proof
parser/AST != authority
parser/AST != RT:v
parser/AST != release readiness
```

## Phase 1 core model

```text
DocumentNode
EnvelopeNode
FieldNode
SourceSpan
ParseIssue
DiagnosticBag
```

The parser retains:

```text
normalized UTF-8 text
raw field text
field order
field duplicates
source line/column spans
inline and multiline values
nested mapping/list/record helper structures
exact strings
```

## Supported envelopes

```text
KDSL_RESULT
PACKET_DRAFT
NORMALIZATION_DRAFT
SAFETY_GATES
KDSL_PROMPT / KDSL_PROMPT_PREVIEW
structural round-trip result envelopes
```

## Phase 1 parser features

```text
tab-indentation diagnostics
duplicate-field diagnostics
multiline JSON-compatible value capture
block-scalar capture
nested scalar mapping
simple sequence parsing
list-record parsing
nested list parsing
source-span output
legacy checker adapters
```

## Checker migration baseline

The following major semantic checkers use the common parser adapters for input extraction:

```text
kdsl_r1c.py
kdsl_packet.py
kdsl_packet_normalization.py
kdsl_safety_gate.py
```

Semantic rules remain in their existing checker modules. The adapter changes input interpretation, not authority or safety policy.

## Unified execution

```text
run_all_samples.py
  run_samples.py
  run_safety_gate_samples.py
  run_r1c_roundtrip_samples.py
  run_parser_samples.py
  later Phase 2-4 suites
```

The unified runner aggregates all suite totals and fails when any runner fails or omits a summary.

Current integrated checkpoint:

```text
unified expectations: 257 / failed 0
parser/adapter suite: 11 / failed 0
required workflow/check: KDSL Validation
```

## Phase 1 known limits

```text
not a complete YAML parser
not a complete JSON5 parser
not a natural-language semantic parser
first matching envelope per marker
field-only AST
nested source spans are not first-class nodes
legacy namespace adapter remains
no alias inference
no unknown schema inference
no implicit defaults
```

## Phase 6A direction

Design and review documents:

```text
docs/design/kdsl-semantic-parser-v2.md
docs/reviews/kdsl-phase6a-semantic-parser-foundation.md
```

Selected direction:

```text
additive typed document/header/envelope/field/value AST
raw + normalized value channels
multiple-envelope/context representation
explicit compatibility views
checker-by-checker parity migration
legacy adapter retirement only after evidence
```

Phase 6A changes design/status only. It does not implement AST v2 and does not change semantic policy.

## Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser or semantic failure
```
