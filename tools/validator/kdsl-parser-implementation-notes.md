# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated
phase1_pull_request: 38
phase1_squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
phase6a_pull_request: 56
phase6a_squash_commit: bedd63937a9ef746962836833d24ad77ff3f09d0
phase6b_pull_request: 57
phase6b_squash_commit: 54c214587cedfc4af634edba9d3df7cdea30d524
phase6b_workflow_run: 29222907053 / 257 / success
phase6_tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Replace duplicated envelope and field scanning with source-spanned parser foundations while preserving existing semantic validators and their safety boundaries.

```text
parser/AST != semantic equivalence proof
parser/AST != safety proof
parser/AST != authority
parser/AST != RT:v
parser/AST != release readiness
```

## Phase 1 compatibility parser

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

Existing adapter consumers:

```text
kdsl_r1c.py
kdsl_packet.py
kdsl_packet_normalization.py
kdsl_safety_gate.py
```

Semantic rules remain in their checker modules. Phase 6B does not migrate these checkers and does not remove `kdsl_parser_adapter.py`.

## Phase 6A design contract

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

## Phase 6B typed AST v2

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

## Verification

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
unified runners: 9
unified expectations: 269 / failed 0
workflow: KDSL Validation
workflow run: 29222907053 / #257 / success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

The 269 total is the aggregate of the previously integrated 257 expectations and the successful 12-case parser-v2 runner. The unified runner rejects missing summaries and failed child runners.

## Current limitations

```text
not a complete YAML parser
not a complete JSON5 parser
not a natural-language semantic parser
Phase 1 first-match envelope API remains for existing checkers
AST v2 compatibility views not implemented
checker migration not started
legacy namespace adapter remains
legacy-vs-v2 parity proof incomplete
active-document/raw-envelope contexts are first slice only
no alias inference
no unknown schema inference
no implicit defaults
```

## Phase 6C next step

```text
R1CCompatibilityView pilot
legacy-vs-v2 field/order/value/raw-text parity
existing R1C expected exits retained
legacy adapter retained until broader migration evidence
```

Stop migration when:

```text
RT/NEXT/COMMIT input changes
protected wording/raw text changes
unknown schema/default inference is required
legacy/v2 outputs or expected exits disagree
```

## Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser or semantic failure
```
