# Packet Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / checker-migration-pending
compatibility_view: tools/validator/kdsl_parser_v2_packet_compat.py
parity_checker: tools/validator/kdsl_parser_v2_packet_parity.py
parity_runner: tools/validator/run_parser_v2_packet_parity_samples.py
implementation_pull_request: 71
implementation_squash_commit: 5b158c667a266ee1e10e2337eee9f0260f6b02ba
workflow: 29232149425 / 309 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Packet structural view that matches the complete Phase 1 helper surface consumed by `kdsl_packet.py` before changing the active checker.

```text
parser parity != Packet semantic equivalence
parser parity != normalization completion
parser parity != execution authority
parser parity != Packet executability
```

## Current active checker path

```text
tools/validator/kdsl_packet.py
→ tools/validator/kdsl_parser_adapter.py
→ install_packet(globals())
→ Phase 1 structural helpers
→ existing semantic/property checks
```

The active checker has not switched to the v2 view.

## Compatibility view path

```text
input
→ independent legacy-compatible PACKET_DRAFT scope selection
→ exact original scope retained
→ DocumentNodeV2 raw-envelope parse
→ typed top-level Packet blocks
→ legacy helper output reconstruction
→ Phase 1/AST v2 parity comparison
```

## Compared helper contract

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
top-level entries and relative lines
duplicate top-level fields
raw block maps
nested scalar maps and duplicates
SG.id lists
FLOW.op lists
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

`PacketBlockNodeV2` retains:

```text
name
inline value
body lines
raw text
source span
relative line
```

It exposes bounded compatibility helpers:

```text
nested_scalars()
list_field()
sequence_items()
legacy_block
```

## Fenced example boundary

The repository Packet example is inside a Markdown fence.

```text
AST v2 active-document→fenced Packet inactive
Phase 1 Packet parser→first marker selected
PacketCompatibilityView→same legacy-compatible scope selected
selected scope→raw-envelope parse
```

General parser fence behavior remains unchanged.

## Semantic rules intentionally excluded

```text
SCHEMA/STATUS validity
required Packet field/order rules
BASE/TASK registry and ID validity
TASK/FLOW composition
SG registry/ID/composition
trigger-required gates
AUTHORITY rails
OUT result schema
NORMALIZE required/target/state
GOAL placeholders
warnings for empty lists
Packet semantic properties
```

These remain in the active Packet checker and property modules.

## Critical Packet boundary

```text
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
normalization_required: yes
execution_authority: none
PKT:v1: prohibited
```

No CompatibilityView result may be interpreted as normalization completion or execution permission.

## Verification

```text
Packet structural parity: 8 / failed 0
unified runners: 15
unified expectations: 315 / failed 0
workflow run: 29232149425 / #309
KDSL Validation: success
Packet Semantic Property: success
```

## Exit codes

```text
0: structural parity pass
2: structural parity or usage failure
```

## Current boundary

```text
CompatibilityView: integrated
parity corpus: integrated
checker switch: pending
Phase 1 adapter: active for Packet
Packet Normalization adapter: active
legacy adapter removal: prohibited
```

## Next step

```text
Packet checker structural extraction→PacketCompatibilityView
in-process Phase 1/AST v2 parity guard required
Packet semantic/property boundaries unchanged
non-executable/not_normalized/authority rails保持
```
