# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated / phase6c-r1c-migrated / phase6c-compact-migrated / phase6c-safety-gate-migrated / phase6c-packet-base-migrated / phase6c-normalization-compat-integrated
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
phase6c_normalization_compat_pull_request: 75
phase6c_normalization_compat_squash_commit: ceb8269c2f1b3fe84342bd0fcff6d36871385510
latest_workflow: 29233236734 / 317 / success
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

Active checker-level adapter consumer:

```text
kdsl_packet_normalization.py
```

Retained helper-export compatibility:

```text
kdsl_packet.py helper exports for semantic/property/normalization modules
Safety Gate helper exports for inheritance/graph/optional modules
```

Migrated base/checker paths:

```text
kdsl_r1c.py
kdsl_compact_prompt.py
kdsl_safety_gate.py
kdsl_packet.py base checker
```

Normalization has an integrated CompatibilityView/parity corpus, but its active checker still uses the Phase 1 adapter. Adapter removal remains prohibited.

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
input→AST v2 R1C extraction→schema fallback/parity guard→existing R1C semantics
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
input→CompatibilityView→parity guard→AST v2 structure→existing CompactPrompt semantics
```

Retained:

```text
mode/safety/lexicon
KDSL-CP漢 conflicts
required/empty/mixed/duplicate policy
restricted aliases
CP-Lift triggers and prohibition exception
PKT:v1 and Packet boundaries
```

## 6. Safety Gate path

```text
compatibility view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
active checker: tools/validator/kdsl_safety_gate.py
migration runner: tools/validator/run_safety_gate_migration_samples.py
```

```text
input→CompatibilityView→parity guard→AST v2 registry/entries→existing Safety Gate semantics
```

Retained:

```text
registry/ID/state
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

```text
input→PacketCompatibilityView→parity guard→AST v2 scope/entries/blocks→existing Packet semantics
```

Retained helper boundary:

```text
install_packet(globals()): retained
helper consumers' separate migration: not claimed
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

## 8. Packet Normalization compatibility pilot

```text
compatibility view: tools/validator/kdsl_parser_v2_normalization_compat.py
parity checker: tools/validator/kdsl_parser_v2_normalization_parity.py
parity runner: tools/validator/run_parser_v2_normalization_parity_samples.py
active checker: tools/validator/kdsl_packet_normalization.py / Phase 1 adapter
```

Compatibility path:

```text
input
→ legacy-compatible NORMALIZATION_DRAFT scope
→ raw-envelope AST v2 parse
→ NormalizationBlockNodeV2
→ Phase 1 helper output reconstruction
→ structural parity comparison
```

Compared helper surface:

```text
extract_scope_lines
parse_top_level_legacy
blocks_from_entries_legacy
parse_nested_scalars_legacy
parse_list_records_legacy
parse_nested_lists_legacy
extract_multiline_legacy
```

Compared outputs:

```text
envelope presence/exact scope
top-level order/value/relative lines/duplicates
raw blocks
nested scalar maps/duplicates
MAP/UNRESOLVED/LOSS records
PRESERVE nested lists
OUTPUT.preview block scalar
```

Checker switch is not performed in Phase 6C-9.

Critical normalization boundary:

```text
STATUS: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
executable target markers prohibited
PKT:v1 prohibited
normalization completion: not_proven
```

## 9. Verification

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
R1C parity: 10 / failed 0
CompactPrompt parity: 12 / failed 0
CompactPrompt migration: 4 / failed 0
Safety Gate parity: 8 / failed 0
Safety Gate migration: 4 / failed 0
Packet parity: 8 / failed 0
Packet migration: 6 / failed 0
Normalization parity: 8 / failed 0
unified runners: 17
unified expectations: 329 / failed 0
workflow run: 29233236734 / #317
KDSL Validation: success
Packet Semantic Property: success
```

## 10. Current limitations

```text
not a complete YAML/JSON5/natural-language parser
selected structural parity != meaning-preservation proof
R1C semantic equivalence not proven
Full R1 view pending
Normalization checker migration pending
Packet/Safety helper-consumer migration decisions pending
legacy adapter retirement proof incomplete
same-marker multiple-envelope semantics not generally defined
no alias/default/unknown-schema inference
```

## 11. Next migration order

```text
Packet Normalization checker migration under parity guard
Full R1 compatibility view/migration
helper-consumer migration decision
Phase 6D mutation/property/repository corpus
legacy adapter retirement decision
```

Stop migration when:

```text
expected checker exits change
normalization non-executable boundary weakens
TARGET.executable:false weakens
semantic_equivalence:not_proven weakens
execution_authority:none weakens
Packet/Safety/CP-Lift/RT/NEXT/COMMIT meaning changes
unknown schema/default inference is required
```

## 12. Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser parity or semantic failure
```
