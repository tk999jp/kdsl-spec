# KDSL Common Parser / AST Phase 1

status: implementation-candidate
phase: common parser / validator foundation
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

## Core model

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
nested mapping/list/record structure
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

## Checker migration

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
```

The unified runner aggregates all suite totals and fails when any runner fails or omits a summary.

## Known limits

```text
not a complete YAML parser
not a complete JSON5 parser
not a natural-language semantic parser
first matching envelope per marker
no alias inference
no unknown schema inference
no implicit defaults
```

## Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser or semantic failure
```
