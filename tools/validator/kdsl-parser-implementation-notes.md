# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated / phase6c-r1c-migrated / phase6c-compact-migrated
phase1_pull_request: 38
phase1_squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
phase6a_pull_request: 56
phase6a_squash_commit: bedd63937a9ef746962836833d24ad77ff3f09d0
phase6b_pull_request: 57
phase6b_squash_commit: 54c214587cedfc4af634edba9d3df7cdea30d524
phase6c_r1c_compat_pull_request: 59
phase6c_r1c_compat_squash_commit: e20ebde511ce860faf9224f0b5902c08309a0a6f
phase6c_r1c_checker_pull_request: 61
phase6c_r1c_checker_squash_commit: a81bb8cae5aefd4020c0df004c616d5e4f834cee
phase6c_compact_compat_pull_request: 63
phase6c_compact_compat_squash_commit: 2df06525265b7fdf56b449447967f5e681534615
phase6c_compact_checker_pull_request: 65
phase6c_compact_checker_squash_commit: 4d4a5f7b6580ecec44636f8e09e163540fb17770
latest_workflow: 29230246858 / 297 / success
phase6_tracking_issue: 55
validator_authority: non-authoritative

## 1. Purpose

Provide source-spanned parser foundations and migrate validator structure incrementally without changing canonical safety, authority, runtime, or release meanings.

```text
parser/AST != semantic equivalence proof
parser/AST != safety proof
parser/AST != authority
parser/AST != RT:v
parser/AST != release readiness
```

## 2. Phase 1 compatibility parser

```text
tools/validator/kdsl_parser.py
tools/validator/kdsl_parser_adapter.py
```

Core model:

```text
DocumentNode
EnvelopeNode
FieldNode
SourceSpan
ParseIssue
DiagnosticBag
```

Remaining namespace-adapter consumers:

```text
kdsl_safety_gate.py
kdsl_packet.py
kdsl_packet_normalization.py
```

R1C no longer installs the Phase 1 namespace adapter. CompactPrompt never used that namespace adapter; it now uses an explicit AST v2 compatibility view.

## 3. Phase 6A design contract

```text
docs/design/kdsl-semantic-parser-v2.md
docs/reviews/kdsl-phase6a-semantic-parser-foundation.md
```

Selected direction:

```text
additive typed document/header/envelope/field/value AST
raw + normalized channels
multiple-envelope/context representation
explicit compatibility views
checker-by-checker parity migration
legacy adapter retirement only after evidence
```

## 4. Phase 6B typed AST v2

Implementation:

```text
tools/validator/kdsl_parser_v2.py
tools/validator/kdsl_parse_v2.py
tools/validator/run_parser_v2_samples.py
tools/validator/samples/parser-v2/*
```

Node surface:

```text
DocumentNodeV2
HeaderNode
EnvelopeNodeV2
FieldNodeV2
SourceSpanV2
DiagnosticV2
ScalarNode
BlockScalarNode
JsonNode
EmptyNode
InvalidNode
MappingNode / MappingEntryNode
SequenceNode / SequenceItemNode
RecordSequenceNode
FenceNode / MarkdownNode / TextNode
```

Implemented properties:

```text
ordered document children
formal KDSL header axes
multiple envelope exposure
raw source + normalized value channels
nested typed values with source spans
duplicate envelope/field/mapping-key diagnostics
invalid JSON diagnostics
unclosed fence diagnostics
active-document fenced-example isolation
CRLF normalization
UTF-8/Japanese exact wording preservation
unknown header values retained without inference
```

## 5. Phase 6C R1C path

Compatibility implementation:

```text
tools/validator/kdsl_parser_v2_compat.py
tools/validator/kdsl_parser_v2_r1c_parity.py
tools/validator/run_parser_v2_r1c_parity_samples.py
```

Current checker path:

```text
input
→ AST v2 R1C compatibility extraction
→ no R1C schema: Full R1 fallback/out-of-scope
→ R1C schema present: legacy-v2 parity guard
→ mismatch: fail before semantic validation
→ match: existing R1C semantic validation
```

Retained semantic rules:

```text
required field/order rules
structured JSON rules
RT state/basis rules
NEXT proposal_only boundary
COMMIT actual/proposed/permission boundary
optional-block validation
PKT:v1 prohibition
```

Correctives:

```text
fenced repository examples→legacy-compatible scope selection
AST v2 active-document policy unchanged
SAFETY_GATES standalone marker/R1C optional field ambiguity→selected R1C scope限定
marker registry restored in finally
same-marker divergence→semantic validation前にfail
```

## 6. Phase 6C CompactPrompt path

Compatibility implementation:

```text
tools/validator/kdsl_parser_v2_compact_compat.py
tools/validator/kdsl_parser_v2_compact_parity.py
tools/validator/run_parser_v2_compact_parity_samples.py
```

Current checker path:

```text
input
→ CompactPromptCompatibilityView
→ legacy-v2 structural parity guard
→ mismatch: fail before semantic validation
→ match: AST v2 scope/header/block/duplicate extraction
→ existing CompactPrompt semantic and safety validation
```

Migrated structural surface:

```text
CompactPrompt detection
KDSL-CP / KDSL-CP漢 shorthand
legacy-compatible scope
profile/mode/safety/lexicon headers
typed CompactBlockNodeV2
block order/content/source span
duplicate block order
```

Retained semantic rules:

```text
mode/safety/lexicon validity
KDSL-CP漢 conflict checks
required/empty block rules
mixed-key and duplicate warnings
restricted free-text alias detection
CP-Lift triggers and prohibition-clause exception
PKT:v1 prohibition
PACKET_DRAFT non-executable checks
```

Legacy extraction helpers remain only for the in-process parity guard.

## 7. Verification

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
Phase 6C R1C parity suite: 10 / failed 0
Phase 6C CompactPrompt parity suite: 12 / failed 0
CompactPrompt checker migration suite: 4 / failed 0
unified runners: 12
unified expectations: 295 / failed 0
workflow: KDSL Validation
workflow run: 29230246858 / #297 / success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

Permanent CompactPrompt migration boundaries:

```text
profile-only/no-shorthand
same-key duplicate warning
mixed standard/kanji warning
fenced scope excluding following notes
```

## 8. Unified runner output policy

```text
successful child runner: compact total/failed summary
failed or malformed child runner: full stdout/stderr
missing summary: failure
non-zero child exit: failure
```

Output compaction changes observability only and does not weaken the suite.

## 9. Current limitations

```text
not a complete YAML parser
not a complete JSON5 parser
not a natural-language semantic parser
R1C parity proves selected structural contract only
R1C full semantic equivalence not proven
CompactPrompt structural parity != meaning-preservation proof
Full R1 compatibility view not implemented
Safety Gate/Packet/Normalization compatibility views not implemented
legacy namespace adapter remains for three checker families
legacy adapter retirement proof incomplete
same-marker multiple-envelope semantics not generally defined
no alias inference
no unknown schema inference
no implicit defaults
```

## 10. Next migration order

```text
Safety Gate compatibility view/parity pilot
Safety Gate checker migration after parity evidence
Packet compatibility view/migration
Packet Normalization compatibility view/migration
Phase 6D mutation/property/repository corpus
legacy adapter retirement decision
```

Stop migration when:

```text
expected checker exits change without specification approval
protected wording/raw text changes
Safety Gate state/composition meaning changes
CP-Lift or restricted-alias meaning changes
RT/NEXT/COMMIT input changes
unknown schema/default inference is required
Packet execution/normalization boundary weakens
```

## 11. Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser or semantic failure
```
