# KDSL Common Parser / AST

status: phase1-integrated / phase6a-design-integrated / phase6b-core-integrated / phase6c-active-checkers-migrated
phase1_pull_request: 38
phase1_squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
phase6a_pull_request: 56
phase6a_squash_commit: bedd63937a9ef746962836833d24ad77ff3f09d0
phase6b_pull_request: 57
phase6b_squash_commit: 54c214587cedfc4af634edba9d3df7cdea30d524
phase6c_r1c_pull_requests: 59 / 61
phase6c_compact_pull_requests: 63 / 65
phase6c_safety_gate_pull_requests: 67 / 69
phase6c_packet_pull_requests: 71 / 73
phase6c_normalization_pull_requests: 75 / 77
latest_workflow: 29233820287 / 321 / success
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

## 2. Phase 1 compatibility layer

```text
tools/validator/kdsl_parser.py
tools/validator/kdsl_parser_adapter.py
```

No active base checker remains solely on the Phase 1 structural path.

Retained helper-export compatibility:

```text
Packet helper exports→semantic/property/normalization modules
Normalization helper exports→round-trip/property modules
Safety Gate helper exports→inheritance/graph/R1C optional/semantic modules
```

```text
helper exports retained != active checker Phase 1 path
adapter removal prohibited until helper-consumer and Full R1 evidence
```

## 3. Typed AST v2 foundation

```text
tools/validator/kdsl_parser_v2.py
tools/validator/kdsl_parse_v2.py
```

Core surface:

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
raw + normalized channels
nested typed values and source spans
duplicate envelope/field/mapping-key diagnostics
invalid JSON and unclosed fence diagnostics
active-document fenced-example isolation
raw-envelope compatibility contexts
CRLF normalization
UTF-8/Japanese exact wording preservation
unknown header values retained without inference
```

## 4. Common migration pattern

```text
input
→ checker-specific AST v2 CompatibilityView
→ Phase 1/AST v2 structural parity guard
→ mismatch: semantic validation前にfail
→ match: existing semantic validation
```

Compatibility pass proves only the selected structural contract.

## 5. R1C path

```text
view: tools/validator/kdsl_parser_v2_compat.py
parity: tools/validator/kdsl_parser_v2_r1c_parity.py
checker: tools/validator/kdsl_r1c.py
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

## 6. CompactPrompt path

```text
view: tools/validator/kdsl_parser_v2_compact_compat.py
parity: tools/validator/kdsl_parser_v2_compact_parity.py
checker: tools/validator/kdsl_compact_prompt.py
```

Retained:

```text
mode/safety/lexicon validity
KDSL-CP漢 conflicts
required/empty/mixed/duplicate rules
restricted aliases
CP-Lift triggers and prohibition exception
Packet boundary checks
```

## 7. Safety Gate path

```text
view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity: tools/validator/kdsl_parser_v2_safety_gate_parity.py
checker: tools/validator/kdsl_safety_gate.py
```

Retained:

```text
registry/ID/state validity
required fields
satisfied evidence/authority
blocked/na handling
baseline/composition/protected wording
aggregate state
inheritance and graph meanings
```

## 8. Packet path

```text
view: tools/validator/kdsl_parser_v2_packet_compat.py
parity: tools/validator/kdsl_parser_v2_packet_parity.py
checker: tools/validator/kdsl_packet.py
```

Retained:

```text
SCHEMA/STATUS rules
required field/order
BASE/TASK/FLOW/SG registries and IDs
FLOW/Safety Gate composition
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

## 9. Packet Normalization path

```text
view: tools/validator/kdsl_parser_v2_normalization_compat.py
parity: tools/validator/kdsl_parser_v2_normalization_parity.py
checker: tools/validator/kdsl_packet_normalization.py
```

Retained:

```text
SCHEMA/STATUS
SOURCE/TARGET
MAP/PRESERVE/UNRESOLVED/LOSS
ROUND_TRIP
AUTHORITY
OUTPUT
executable marker prohibition
PKT:v1 prohibition
```

Critical invariants:

```text
STATUS: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
normalization completion: not_proven
```

## 10. Verification

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
Normalization parity: 8 / failed 0
Normalization checker migration: 7 / failed 0
unified runners: 18
unified expectations: 336 / failed 0
workflow run: 29233820287 / #321
KDSL Validation: success
Packet Semantic Property: success
```

## 11. Current limitations

```text
not a complete YAML/JSON5/natural-language parser
selected structural parity != meaning-preservation proof
Full R1 CompatibilityView pending
helper-consumer migration decision pending
legacy adapter retirement proof incomplete
same-marker multiple-envelope semantics not generally defined
no alias/default/unknown-schema inference
```

## 12. Next order

```text
Full R1 compatibility inventory/view/parity pilot
Full R1 checker migration
helper-consumer migration decision
Phase 6D mutation/property/repository corpus
legacy adapter retirement decision
```

Stop when:

```text
existing checker exits change
RT/NEXT/COMMIT meaning changes
Packet non-executable/not_normalized boundary weakens
normalization non-executable/not_proven/none boundary weakens
Safety Gate/CP-Lift meaning changes
unknown schema/default inference is required
```

## 13. Exit codes

```text
0: pass / applicable parse succeeded
1: warning
2: parser parity or semantic failure
```
