# Packet Normalization Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / checker-migration-pending
compatibility_view: tools/validator/kdsl_parser_v2_normalization_compat.py
parity_checker: tools/validator/kdsl_parser_v2_normalization_parity.py
parity_runner: tools/validator/run_parser_v2_normalization_parity_samples.py
implementation_pull_request: 75
implementation_squash_commit: ceb8269c2f1b3fe84342bd0fcff6d36871385510
workflow: 29233236734 / 317 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned structural view matching the complete Phase 1 helper surface consumed by `kdsl_packet_normalization.py` before changing the active checker.

```text
parser parity != semantic equivalence
parser parity != normalization completion
parser parity != execution authority
parser parity != executable target
```

## Current active checker path

```text
tools/validator/kdsl_packet_normalization.py
→ tools/validator/kdsl_parser_adapter.py
→ install_normalization(globals())
→ Phase 1 structural helpers
→ existing normalization semantic validation
```

The active checker has not switched to the v2 view.

## Compatibility view path

```text
input
→ legacy-compatible NORMALIZATION_DRAFT scope selection
→ exact original scope retained
→ DocumentNodeV2 raw-envelope parse
→ NormalizationBlockNodeV2 records
→ legacy helper output reconstruction
→ Phase 1/AST v2 parity comparison
```

## Compared helper contract

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
top-level entries/relative lines/duplicates
raw block maps
nested scalar maps and duplicates
MAP/UNRESOLVED/LOSS records
PRESERVE nested lists
OUTPUT.preview block scalar
```

## AST v2 data used

```text
DocumentNodeV2
EnvelopeNodeV2
FieldNodeV2
SourceSpanV2
NormalizationBlockNodeV2
NormalizationCompatibilityView
```

`NormalizationBlockNodeV2` exposes:

```text
nested_scalars()
list_records()
nested_lists()
multiline()
legacy_block
```

## Fenced example boundary

```text
AST v2 active-document→fenced normalization inactive
Phase 1 parser→first NORMALIZATION_DRAFT marker selected
NormalizationCompatibilityView→same scope selected
selected scope→raw-envelope parse
```

General AST v2 fence behavior remains unchanged.

## Semantic rules intentionally excluded

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
unified runners: 17
unified expectations: 329 / failed 0
workflow run: 29233236734 / #317
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
Phase 1 adapter: active for normalization checker
legacy adapter removal: prohibited
```

## Next step

```text
normalization checker structural extraction→NormalizationCompatibilityView
in-process Phase 1/AST v2 parity guard required
semantic/equivalence/authority rules unchanged
non-executable/not_proven/none boundaries保持
```
