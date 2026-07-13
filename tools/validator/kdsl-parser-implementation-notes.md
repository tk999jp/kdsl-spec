# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated / phase6c-r1c-compat-integrated
phase1_pull_request: 38
phase1_squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
phase6a_pull_request: 56
phase6a_squash_commit: bedd63937a9ef746962836833d24ad77ff3f09d0
phase6b_pull_request: 57
phase6b_squash_commit: 54c214587cedfc4af634edba9d3df7cdea30d524
phase6b_workflow_run: 29222907053 / 257 / success
phase6c_r1c_pull_request: 59
phase6c_r1c_squash_commit: e20ebde511ce860faf9224f0b5902c08309a0a6f
phase6c_r1c_workflow_run: 29223392311 / 263 / success
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

Semantic rules remain in their checker modules. Phase 6C-1 does not switch these checkers and does not remove `kdsl_parser_adapter.py`.

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

## Phase 6C-1 R1C compatibility view

Implementation:

```text
tools/validator/kdsl_parser_v2_compat.py
tools/validator/kdsl_parser_v2_r1c_parity.py
tools/validator/run_parser_v2_r1c_parity_samples.py
```

Compatibility contract:

```text
KDSL_RESULT envelope presence
legacy-compatible scope lines
field order
raw field values
relative field line numbers
duplicate field order
```

The compatibility view reconstructs legacy values from AST v2 raw source. It does not use normalized values to replace quoted/protected/multiline source text.

### Fenced example corrective

Initial parity runs exposed a real scope-selection difference:

```text
legacy parser: selects KDSL_RESULT inside repository Markdown fence
AST v2 active-document: excludes fenced envelope
```

Correction:

```text
R1CCompatibilityView independently selects the first legacy-compatible R1C scope
selected scope is parsed in AST v2 raw-envelope context
AST v2 active-document fence policy remains unchanged
```

This is a compatibility-surface correction, not a general active-document semantic change.

## Verification

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
Phase 6C R1C parity suite: 8 / failed 0
unified runners: 10
unified expectations: 277 / failed 0
workflow: KDSL Validation
final workflow run: 29223392311 / #263 / success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

Corrective history:

```text
run #261: KDSL Validation failure / fenced scope mismatch
run #262: KDSL Validation failure / compact failure output enabled
run #263: success after compatibility scope correction
```

## Unified runner output policy

```text
successful child runner: compact total/failed summary
failed or malformed child runner: full stdout/stderr
missing summary: failure
non-zero child exit: failure
```

Output compaction changes observability only and does not weaken the suite.

## Current limitations

```text
not a complete YAML parser
not a complete JSON5 parser
not a natural-language semantic parser
Phase 1 parser remains active for existing semantic checkers
R1CCompatibilityView is not yet wired into kdsl_r1c.py
Packet/Normalization/Safety Gate compatibility views not implemented
legacy namespace adapter remains
same-marker duplicate-envelope parity not proven
legacy adapter retirement proof incomplete
active-document/raw-envelope contexts are first slice only
no alias inference
no unknown schema inference
no implicit defaults
```

## Phase 6C-2 next step

```text
switch kdsl_r1c.py structural extraction to explicit R1CCompatibilityView
dual-run or parity guard during migration
existing R1C expected exits retained
legacy adapter retained for Packet/Normalization/Safety Gate
```

Stop migration when:

```text
R1C expected exits change
RT/NEXT/COMMIT inputs change
protected wording/raw text changes
fenced/unfenced scope compatibility changes
unknown schema/default inference is required
```

## Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser or semantic failure
```
