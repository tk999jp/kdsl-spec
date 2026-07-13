# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated / phase6c-r1c-migrated / phase6c-compact-migrated / phase6c-safety-gate-migrated
phase1_pull_request: 38
phase1_squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
phase6a_pull_request: 56
phase6a_squash_commit: bedd63937a9ef746962836833d24ad77ff3f09d0
phase6b_pull_request: 57
phase6b_squash_commit: 54c214587cedfc4af634edba9d3df7cdea30d524
phase6c_r1c_pull_requests: 59 / 61
phase6c_r1c_squashes: e20ebde511ce860faf9224f0b5902c08309a0a6f / a81bb8cae5aefd4020c0df004c616d5e4f834cee
phase6c_compact_pull_requests: 63 / 65
phase6c_compact_squashes: 2df06525265b7fdf56b449447967f5e681534615 / 4d4a5f7b6580ecec44636f8e09e163540fb17770
phase6c_safety_gate_pull_requests: 67 / 69
phase6c_safety_gate_squashes: 604e4e1f8f8c601f7054b15b38e3c5db40d88056 / bfc034c44473232cee5107c53483a0b080e25a46
latest_workflow: 29231502084 / 305 / success
phase6_tracking_issue: 55
validator_authority: non-authoritative

## 1. Purpose

Provide source-spanned parser foundations and migrate validator structural extraction checker by checker without changing canonical safety, authority, runtime, or release meanings.

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

Remaining active namespace-adapter consumers after Phase 6C-6:

```text
kdsl_packet.py
kdsl_packet_normalization.py
```

No longer active namespace-adapter consumers:

```text
kdsl_r1c.py
kdsl_safety_gate.py
```

CompactPrompt never used the namespace adapter; it now uses an explicit AST v2 compatibility view.

The adapter file remains because Packet and Packet Normalization still depend on it. Removal is prohibited until their migration and regression evidence are complete.

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
ScalarNode / BlockScalarNode / JsonNode / EmptyNode / InvalidNode
MappingNode / MappingEntryNode
SequenceNode / SequenceItemNode / RecordSequenceNode
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

```text
compatibility view: tools/validator/kdsl_parser_v2_compat.py
parity checker: tools/validator/kdsl_parser_v2_r1c_parity.py
active checker: tools/validator/kdsl_r1c.py
```

Runtime path:

```text
input
→ AST v2 R1C compatibility extraction
→ no R1C schema: Full R1 fallback/out-of-scope
→ R1C schema present: legacy-v2 parity guard
→ mismatch: fail before semantic validation
→ match: existing R1C semantic validation
```

Retained:

```text
required field/order and JSON rules
RT state/basis
NEXT proposal_only
COMMIT actual/proposed/permission
optional-block validation
PKT:v1 prohibition
```

Correctives:

```text
fenced examples→legacy-compatible scope selection
SAFETY_GATES marker/R1C field ambiguity→selected scope限定
same-marker divergence→semantic validation前にfail
```

## 6. Phase 6C CompactPrompt path

```text
compatibility view: tools/validator/kdsl_parser_v2_compact_compat.py
parity checker: tools/validator/kdsl_parser_v2_compact_parity.py
active checker: tools/validator/kdsl_compact_prompt.py
migration runner: tools/validator/run_compact_migration_samples.py
```

Runtime path:

```text
input
→ CompactPromptCompatibilityView
→ legacy-v2 parity guard
→ mismatch: fail before semantic validation
→ match: AST v2 scope/header/block/duplicate extraction
→ existing CompactPrompt semantic/safety validation
```

Retained:

```text
mode/safety/lexicon validity
KDSL-CP漢 conflicts
required/empty blocks
mixed-key/duplicate warnings
restricted free-text alias detection
CP-Lift triggers and prohibition exception
PKT:v1 and Packet non-executable checks
```

## 7. Phase 6C Safety Gate path

```text
compatibility view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
active checker: tools/validator/kdsl_safety_gate.py
migration runner: tools/validator/run_safety_gate_migration_samples.py
```

Runtime path:

```text
input
→ SafetyGateCompatibilityView
→ Phase 1 / AST v2 parity guard
→ mismatch: fail before semantic validation
→ match: AST v2 scope/registry/entry extraction
→ existing Safety Gate semantic validation
```

Retained:

```text
registry/ID/state validity
required fields
satisfied evidence/authority
blocked and na rules
dev-prompt baseline
composition rules
protected wording
aggregate state
inheritance and graph semantics
```

Permanent guard:

```text
record lines without entries: field
→ legacy/typed divergence
→ parity guard failure
```

Module-level helper API remains for inheritance, graph, optional R1C, and semantic modules. Phase 6C-6 does not claim their separate structural migration.

## 8. Verification

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
R1C parity: 10 / failed 0
CompactPrompt parity: 12 / failed 0
CompactPrompt checker migration: 4 / failed 0
Safety Gate parity: 8 / failed 0
Safety Gate checker migration: 4 / failed 0
unified runners: 14
unified expectations: 307 / failed 0
workflow run: 29231502084 / #305
KDSL Validation: success
Packet Semantic Property: success
```

## 9. Unified runner policy

```text
successful child runner: compact total/failed summary
failed or malformed child runner: full stdout/stderr
missing summary: failure
non-zero child exit: failure
```

Output compaction changes observability only and does not weaken the suite.

## 10. Current limitations

```text
not a complete YAML or JSON5 parser
not a natural-language semantic parser
selected structural parity != meaning-preservation proof
R1C full semantic equivalence not proven
Full R1 compatibility view not implemented
Packet compatibility view/migration pending
Packet Normalization compatibility view/migration pending
helper APIs remain for inheritance/graph and optional consumers
legacy adapter retirement proof incomplete
same-marker multiple-envelope semantics not generally defined
no alias inference
no unknown schema inference
no implicit defaults
```

## 11. Next migration order

```text
Packet compatibility view/parity pilot
Packet checker migration after parity evidence
Packet Normalization compatibility view/migration
Full R1 compatibility view/migration
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

## 12. Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser parity or semantic failure
```
