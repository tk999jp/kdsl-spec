# Packet Normalization Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / checker-migrated-under-parity-guard
compatibility_view: tools/validator/kdsl_parser_v2_normalization_compat.py
parity_checker: tools/validator/kdsl_parser_v2_normalization_parity.py
parity_runner: tools/validator/run_parser_v2_normalization_parity_samples.py
active_checker: tools/validator/kdsl_packet_normalization.py
migration_runner: tools/validator/run_normalization_migration_samples.py
compatibility_pull_request: 75
compatibility_squash_commit: ceb8269c2f1b3fe84342bd0fcff6d36871385510
migration_pull_request: 77
migration_squash_commit: 01f7c7c29aae98b1dfbb95ae416446c9e5b5f823
latest_workflow: 29233820287 / 321 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned structural view and use it as the active Packet Normalization checker's scope/entry/block input without changing normalization semantics, equivalence, authority, or executability.

```text
parser parity != semantic equivalence
parser parity != normalization completion
parser parity != execution authority
parser parity != executable target
```

## Active checker path

```text
input
→ NormalizationCompatibilityView
→ compare_normalization_legacy_v2
→ mismatch: fail before semantic validation
→ match: AST v2 scope/entries/duplicates/blocks
→ existing normalization semantic validation
```

Consumed channels:

```text
view.scope_lines
view.entries
view.duplicates
view.values
view.legacy_blocks
```

Output markers:

```text
Normalization parser parity guard: pass
Normalization structural extraction: AST v2 compatibility view
```

## Retained helper API

Round-trip and property modules import normalization helper functions from `kdsl_packet_normalization.py`.

```text
install_normalization(globals()): retained
helper exports: Phase 1-compatible
active checker scope/entry/block extraction: AST v2
helper consumer migration: not claimed
```

The retained adapter export does not mean the active checker remains on the Phase 1 structural path.

## Compatibility view contract

```text
NORMALIZATION_DRAFT presence/exact scope
top-level entries/relative lines/duplicates
raw block boundaries
SOURCE/TARGET/ROUND_TRIP/AUTHORITY/OUTPUT nested scalars
MAP/UNRESOLVED/LOSS records
PRESERVE nested lists
OUTPUT.preview block scalar
```

Phase 1 helpers compared:

```text
extract_scope_lines
parse_top_level_legacy
blocks_from_entries_legacy
parse_nested_scalars_legacy
parse_list_records_legacy
parse_nested_lists_legacy
extract_multiline_legacy
```

AST v2 data:

```text
DocumentNodeV2
EnvelopeNodeV2
FieldNodeV2
SourceSpanV2
NormalizationBlockNodeV2
NormalizationCompatibilityView
```

## Fenced example boundary

```text
AST v2 active-document→fenced normalization inactive
Phase 1 parser→first NORMALIZATION_DRAFT marker selected
NormalizationCompatibilityView→same legacy-compatible scope selected
selected scope→raw-envelope parse
```

General AST v2 fence behavior remains unchanged.

## Semantic rules retained

```text
SCHEMA/STATUS validity
SOURCE schema/digest/status/state
TARGET kind/schema/resolution/executable
MAP accounting/mode/evidence
UNRESOLVED impact/reason
LOSS class/detail/criticality
PRESERVE completeness
ROUND_TRIP rules
AUTHORITY rules
OUTPUT marker/executable/preview rules
blocked/resolved consistency
executable marker prohibition
PKT:v1 prohibition
```

Critical boundaries:

```text
STATUS: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
executable KDSL_PROMPT/P1/P1L markers prohibited
PKT:v1 prohibited
normalization completion: not_proven
```

## Verification

```text
Normalization structural parity: 8 / failed 0
Normalization checker migration: 7 / failed 0
unified runners: 18
unified expectations: 336 / failed 0
workflow run: 29233820287 / #321
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
active checker switch: integrated
Phase 1/AST v2 parity guard: active
helper exports for dependent modules: retained
normalization semantic/equivalence/authority policy: unchanged
legacy adapter removal: prohibited
```

## Next step

```text
Full R1 compatibility inventory/view/parity pilot
preserve RT/NEXT/COMMIT evidence and authority rules
helper-consumer migration decision after broader evidence
```
