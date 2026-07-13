# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated / phase6c-r1c-checker-migrated
phase1_pull_request: 38
phase1_squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
phase6a_pull_request: 56
phase6a_squash_commit: bedd63937a9ef746962836833d24ad77ff3f09d0
phase6b_pull_request: 57
phase6b_squash_commit: 54c214587cedfc4af634edba9d3df7cdea30d524
phase6c_compat_pull_request: 59
phase6c_compat_squash_commit: e20ebde511ce860faf9224f0b5902c08309a0a6f
phase6c_checker_pull_request: 61
phase6c_checker_squash_commit: a81bb8cae5aefd4020c0df004c616d5e4f834cee
phase6c_checker_workflow: 29224617949 / 289 / success
phase6_tracking_issue: 55
validator_authority: non-authoritative

## 1. Purpose

Provide source-spanned parser foundations and migrate semantic checkers incrementally without changing canonical safety, authority, runtime, or release meanings.

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

Retained capabilities:

```text
normalized UTF-8 text
raw field text
field order and duplicate detection
source line/column spans
inline and multiline values
nested mapping/list/record helper structures
exact strings
legacy checker adapters
```

Remaining adapter consumers after Phase 6C-2:

```text
kdsl_packet.py
kdsl_packet_normalization.py
kdsl_safety_gate.py
```

`kdsl_r1c.py` no longer installs the Phase 1 namespace adapter.

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

## 5. Phase 6C-1 R1C compatibility view

Implementation:

```text
tools/validator/kdsl_parser_v2_compat.py
tools/validator/kdsl_parser_v2_r1c_parity.py
tools/validator/run_parser_v2_r1c_parity_samples.py
```

Compared contract:

```text
KDSL_RESULT envelope presence
legacy-compatible scope lines
field order
raw field values
relative field line numbers
duplicate field order
```

Fenced example correction:

```text
legacy parser selects fenced repository R1C example
AST v2 active-document excludes fenced envelope
R1CCompatibilityView selects the legacy-compatible scope
selected scope is parsed in raw-envelope context
AST v2 active-document policy remains unchanged
```

## 6. Phase 6C-2 R1C checker migration

`kdsl_r1c.py` now uses `R1CCompatibilityView` for structural extraction.

Runtime path:

```text
input
→ AST v2 compatibility extraction
→ no R1C schema: Full R1 fallback/out-of-scope
→ R1C schema present: legacy-v2 parity guard
→ mismatch: fail before semantic validation
→ match: existing R1C semantic validation
```

Semantic rules retained:

```text
required field/order rules
structured JSON rules
RT state/basis rules
NEXT proposal_only boundary
COMMIT actual/proposed/permission boundary
optional-block validation
PKT:v1 prohibition
```

### Full R1 fallback correction

The parity guard is applied only after an R1C schema marker is found.

```text
Full R1 KDSL_RESULT != automatic R1C target
schema absent→R1C out-of-scope
```

### Optional SAFETY_GATES correction

`SAFETY_GATES:` is both:

```text
standalone envelope marker
R1C optional field
```

Within an already selected R1C compatibility scope only:

```text
SAFETY_GATES temporarily treated as field
scope parsed
marker registry restored in finally
```

General AST v2 and standalone Safety Gate behavior remain unchanged.

## 7. Verification

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
Phase 6C R1C parity suite: 10 / failed 0
unified runners: 10
unified expectations: 279 / failed 0
workflow: KDSL Validation
workflow run: 29224617949 / #289 / success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

Permanent Phase 6C-2 guard cases:

```text
R1C optional SAFETY_GATES parity
same-marker divergence rejected before semantic validation
```

Temporary diagnostic runners used during corrective isolation were removed before the final workflow run. The complete unified runner was restored.

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
Full R1 compatibility view not implemented
CompactPrompt compatibility view not implemented
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
CompactPrompt header/structural compatibility
Safety Gate records
Packet
Packet Normalization
Phase 6D mutation/property/repository corpus
legacy adapter retirement decision
```

Stop migration when:

```text
expected checker exits change without specification approval
protected wording/raw text changes
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
