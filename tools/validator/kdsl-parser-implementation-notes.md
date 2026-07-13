# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated / phase6c-r1c-migrated / phase6c-compact-migrated / phase6c-safety-gate-migrated / phase6c-packet-base-migrated
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
phase6c_packet_pull_requests: 71 / 73
phase6c_packet_squashes: 5b158c667a266ee1e10e2337eee9f0260f6b02ba / 52675d02969123f7329727fdddfcf5e0813a377e
latest_workflow: 29232739675 / 313 / success
phase6_tracking_issue: 55
validator_authority: non-authoritative

## 1. Purpose

Provide source-spanned parser foundations and migrate validator structural extraction checker by checker without changing canonical safety, authority, runtime, Packet, normalization, or release meanings.

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

Active checker-level namespace-adapter consumer:

```text
kdsl_packet_normalization.py
```

Retained exported helper compatibility:

```text
kdsl_packet.py installs Phase 1 helper functions for importing semantic/property/normalization modules
active Packet base checker scope/entries/blocks are AST v2
```

Migrated base/checker paths:

```text
kdsl_r1c.py
kdsl_compact_prompt.py
kdsl_safety_gate.py
kdsl_packet.py base checker
```

The adapter file must not be removed before Packet Normalization and helper-consumer migration evidence is complete.

## 3. Phase 6A/6B foundation

Design:

```text
docs/design/kdsl-semantic-parser-v2.md
docs/reviews/kdsl-phase6a-semantic-parser-foundation.md
```

Typed AST:

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
invalid JSON/unclosed fence diagnostics
active-document fenced-example isolation
CRLF normalization
UTF-8/Japanese exact wording preservation
unknown header values retained without inference
```

## 4. R1C path

```text
compatibility view: tools/validator/kdsl_parser_v2_compat.py
parity checker: tools/validator/kdsl_parser_v2_r1c_parity.py
active checker: tools/validator/kdsl_r1c.py
```

```text
input
→ AST v2 R1C compatibility extraction
→ Full R1 fallback when schema absent
→ legacy-v2 parity guard when R1C schema present
→ existing R1C semantic validation
```

Retained:

```text
required fields/order and JSON
RT state/basis
NEXT proposal_only
COMMIT actual/proposed/permission
optional-block validation
PKT:v1 prohibition
```

## 5. CompactPrompt path

```text
compatibility view: tools/validator/kdsl_parser_v2_compact_compat.py
parity checker: tools/validator/kdsl_parser_v2_compact_parity.py
active checker: tools/validator/kdsl_compact_prompt.py
migration runner: tools/validator/run_compact_migration_samples.py
```

```text
input
→ CompactPromptCompatibilityView
→ legacy-v2 parity guard
→ AST v2 scope/header/block extraction
→ existing CompactPrompt semantic/safety validation
```

Retained:

```text
mode/safety/lexicon validity
KDSL-CP漢 conflicts
required/empty/mixed/duplicate policy
restricted aliases
CP-Lift triggers and prohibition exception
PKT:v1 and Packet non-executable checks
```

## 6. Safety Gate path

```text
compatibility view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
active checker: tools/validator/kdsl_safety_gate.py
migration runner: tools/validator/run_safety_gate_migration_samples.py
```

```text
input
→ SafetyGateCompatibilityView
→ Phase 1/AST v2 parity guard
→ AST v2 scope/registry/entries
→ existing Safety Gate semantic validation
```

Retained:

```text
registry/ID/state validity
required fields
satisfied evidence/authority
blocked/na rules
baseline/composition/protected wording
aggregate state
inheritance and graph semantics
```

## 7. Packet path

```text
compatibility view: tools/validator/kdsl_parser_v2_packet_compat.py
parity checker: tools/validator/kdsl_parser_v2_packet_parity.py
active base checker: tools/validator/kdsl_packet.py
migration runner: tools/validator/run_packet_migration_samples.py
```

Runtime path:

```text
input
→ PacketCompatibilityView
→ compare_packet_legacy_v2
→ mismatch: fail before semantic validation
→ match: AST v2 scope/entries/duplicates/blocks
→ existing Packet validation
```

Migrated input channels:

```text
view.scope_lines
view.entries
view.duplicates
view.values
view.legacy_blocks
```

Compared structural contract:

```text
PACKET_DRAFT presence/exact scope
top-level order/value/relative line/duplicates
raw block boundaries
nested scalar maps and duplicates
SG.id and FLOW.op lists
sequence items
```

Retained helper boundary:

```text
install_packet(globals()): retained
helper exports consumed by Packet semantic/property/normalization modules
helper consumer migration: not claimed
```

Retained Packet policy:

```text
SCHEMA/STATUS validity
required field/order
BASE/TASK/FLOW/SG registries and IDs
FLOW and Safety Gate composition
AUTHORITY rails
OUT result schema
NORMALIZE required/target/state
PKT:v1 prohibition
```

Critical invariants:

```text
STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
normalization completion: not_proven
execution authority: none
```

## 8. Verification

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
R1C parity: 10 / failed 0
CompactPrompt parity: 12 / failed 0
CompactPrompt checker migration: 4 / failed 0
Safety Gate parity: 8 / failed 0
Safety Gate checker migration: 4 / failed 0
Packet parity: 8 / failed 0
Packet checker migration: 6 / failed 0
unified runners: 16
unified expectations: 321 / failed 0
workflow run: 29232739675 / #313
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

## 10. Current limitations

```text
not a complete YAML or JSON5 parser
not a natural-language semantic parser
selected structural parity != meaning-preservation proof
R1C full semantic equivalence not proven
Full R1 compatibility view not implemented
Packet helper-consumer migration pending
Packet Normalization compatibility view/migration pending
inheritance/graph helper migration decision pending
legacy adapter retirement proof incomplete
same-marker multiple-envelope semantics not generally defined
no alias inference
no unknown schema inference
no implicit defaults
```

## 11. Next migration order

```text
Packet Normalization compatibility view/parity pilot
Packet Normalization checker migration
Full R1 compatibility view/migration
Packet/Safety helper-consumer migration decision
Phase 6D mutation/property/repository corpus
legacy adapter retirement decision
```

Stop migration when:

```text
expected checker exits change without specification approval
Packet STATUS non-executable weakens
NORMALIZE.required true weakens
NORMALIZE.state not_normalized weakens
normalization semantic_equivalence:not_proven weakens
execution_authority:none weakens
Packet authority/PKT:v1 policy changes
Safety Gate or CP-Lift meaning changes
RT/NEXT/COMMIT meaning changes
unknown schema/default inference is required
```

## 12. Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser parity or semantic failure
```
