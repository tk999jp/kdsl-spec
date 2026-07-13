# Packet Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / base-checker-migrated-under-parity-guard
compatibility_view: tools/validator/kdsl_parser_v2_packet_compat.py
parity_checker: tools/validator/kdsl_parser_v2_packet_parity.py
parity_runner: tools/validator/run_parser_v2_packet_parity_samples.py
active_checker: tools/validator/kdsl_packet.py
migration_runner: tools/validator/run_packet_migration_samples.py
compatibility_pull_request: 71
compatibility_squash_commit: 5b158c667a266ee1e10e2337eee9f0260f6b02ba
migration_pull_request: 73
migration_squash_commit: 52675d02969123f7329727fdddfcf5e0813a377e
latest_workflow: 29232739675 / 313 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Packet structural view and use it as the active base checker's scope/entry/block input without changing Packet semantics, normalization state, authority, or executability.

```text
parser parity != Packet semantic equivalence
parser parity != normalization completion
parser parity != execution authority
parser parity != Packet executability
```

## Active base checker path

```text
input
→ PacketCompatibilityView
→ compare_packet_legacy_v2
→ mismatch: fail before semantic validation
→ match: AST v2 scope/entries/duplicates/blocks
→ existing Packet validation
```

Consumed view channels:

```text
view.scope_lines
view.entries
view.duplicates
view.values
view.legacy_blocks
```

Output markers:

```text
Packet parser parity guard: pass
Packet structural extraction: AST v2 compatibility view
```

## Retained helper API

Dependent modules import structural helper functions from `kdsl_packet.py`:

```text
kdsl_packet_semantic.py
kdsl_packet_property.py
kdsl_packet_normalize.py
kdsl_packet_roundtrip.py
related normalization semantic helpers
```

Therefore:

```text
install_packet(globals()): retained
helper exports: Phase 1-compatible
active base checker scope/entry/block extraction: AST v2
helper consumer migration: not claimed
```

The retained adapter export does not mean the base checker's primary structural input remains Phase 1.

## Compatibility view path

```text
legacy-compatible PACKET_DRAFT scope selection
→ exact original scope retained
→ DocumentNodeV2 raw-envelope parse
→ PacketBlockNodeV2 records
→ legacy helper output reconstruction
→ Phase 1/AST v2 parity comparison
```

Compared helpers:

```text
extract_scope_lines
parse_top_level_legacy
blocks_from_entries_legacy
parse_nested_scalars_legacy
parse_list_field_legacy
parse_sequence_items_legacy
```

Compared outputs:

```text
envelope presence
exact scope lines
top-level field order/value/relative line
duplicate top-level fields
raw block boundaries
nested scalar maps and duplicate order
SG.id list
FLOW.op list
sequence items
```

## AST v2 data used

```text
DocumentNodeV2
EnvelopeNodeV2
FieldNodeV2
SourceSpanV2
PacketBlockNodeV2
PacketCompatibilityView
```

## Fenced example boundary

```text
AST v2 active-document→fenced Packet inactive
Phase 1 parser→first PACKET_DRAFT marker selected
PacketCompatibilityView→same legacy-compatible scope selected
selected scope→raw-envelope parse
```

General parser fence behavior remains unchanged.

## Semantic rules retained

```text
SCHEMA/STATUS validity
required field/order rules
BASE/TASK registry and ID validity
TASK/FLOW composition
SG registry/ID/composition
trigger-required gates
AUTHORITY rails
OUT result schema
NORMALIZE required/target/state
GOAL placeholder handling
list warnings
PKT:v1 prohibition
Packet semantic properties
```

Critical Packet boundary:

```text
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
normalization_required: yes
normalization_completion: not_proven
execution_authority: none
```

No parser result grants edit, stage, commit, push, release, or execution permission.

## Verification

```text
Packet structural parity: 8 / failed 0
Packet checker migration: 6 / failed 0
unified runners: 16
unified expectations: 321 / failed 0
workflow run: 29232739675 / #313
KDSL Validation: success
Packet Semantic Property: success
```

## Exit codes

```text
0: pass
1: semantic warning
2: parser parity or semantic failure
```

## Current boundary

```text
CompatibilityView: integrated
active base checker switch: integrated
Phase 1/AST v2 parity guard: active
helper exports for dependent modules: retained
Packet Normalization checker migration: pending
legacy adapter removal: prohibited
```

## Next step

```text
Packet Normalization compatibility view/parity pilot
normalization draft remains non-executable
semantic_equivalence:not_proven保持
execution_authority:none保持
checker switchはparity成立後
```
