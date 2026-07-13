# Packet Normalization Parser v2 Compatibility Notes

status: checker-migrated / round-trip-consumer-migrated / installer-removal-pending
compatibility_view: tools/validator/kdsl_parser_v2_normalization_compat.py
parity_checker: tools/validator/kdsl_parser_v2_normalization_parity.py
active_checker: tools/validator/kdsl_packet_normalization.py
round_trip_consumer: tools/validator/kdsl_packet_roundtrip.py
tracking_issue: 55
validator_authority: non-authoritative

## Integrated history

```text
compatibility PR: 75
compatibility squash: ceb8269c2f1b3fe84342bd0fcff6d36871385510
checker migration PR: 77
checker migration squash: 01f7c7c29aae98b1dfbb95ae416446c9e5b5f823
consumer contract PR: 89
consumer contract squash: 0ec72d29698679b1e09bd3258eaf3c16d8bd80af
consumer migration PR: 90
consumer migration squash: a031eb3b2b71d19a0f549d4f69c9cbcd73f984df
latest workflow: 29289185279 / 351 / success
```

## 1. Purpose

Provide a source-spanned Normalization structural view used by both the active checker and the round-trip consumer without changing semantic, equivalence, authority, or executability rules.

```text
parser/consumer migration != semantic equivalence
parser/consumer migration != normalization completion
parser/consumer migration != execution authority
```

## 2. Active checker path

```text
input
→ NormalizationCompatibilityView
→ compare_normalization_legacy_v2
→ mismatch: fail before semantic validation
→ match: AST v2 scope/entries/duplicates/blocks
→ existing normalization semantic validation
```

Active checker channels:

```text
view.scope_lines
view.entries
view.duplicates
view.values
view.legacy_blocks
```

## 3. Round-trip consumer path

Before Phase 6D-3B:

```text
kdsl_packet_roundtrip.parse_normalization
→ structural helpers imported from kdsl_packet_normalization
```

Current path:

```text
kdsl_packet_roundtrip.parse_normalization
→ NormalizationCompatibilityView
→ values/nested scalars/records/lists/multiline
→ unchanged returned dictionary
```

Returned contract:

```text
values
source
target
map_records
preserve
unresolved
loss
round_trip
authority
output
preview
```

`kdsl_packet_property.py` remains an indirect consumer of `parse_normalization`.

## 4. Contract and mutation evidence

```text
consumer contract: 10 / failed 0
consumer migration: 3 / failed 0
```

Covered behavior:

```text
nested scalars
record/list order
fenced scope
blocked P1 artifact
missing envelope
last-wins duplicate scalar behavior
preview block text
unsafe value extraction without coercion
static import migration
valid/blocked runtime contracts
```

## 5. Compatibility view contract

```text
NORMALIZATION_DRAFT presence/exact scope
top-level entries/relative lines/duplicates
raw block boundaries
SOURCE/TARGET/ROUND_TRIP/AUTHORITY/OUTPUT nested scalars
MAP/UNRESOLVED/LOSS records
PRESERVE nested lists
OUTPUT.preview block scalar
```

## 6. Semantic rules retained

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

## 7. Final verification

```text
Normalization structural parity: 8 / failed 0
Normalization checker migration: 7 / failed 0
Normalization consumer contract: 10 / failed 0
Normalization consumer migration: 3 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 24
unified expectations: 375 / failed 0
workflow run: 29289185279 / #351
KDSL Validation: success
Packet Semantic Property: success
```

## 8. Current dependency boundary

```text
active checker: AST v2 CompatibilityView
round-trip consumer: AST v2 CompatibilityView
property consumer: indirect parse_normalization API
install_normalization(globals()): retained temporarily
local legacy helper definitions: retained temporarily
Normalization installer removal proof: pending
```

The retained installer does not mean the active checker or round-trip consumer remains on the Phase 1 structural path.

## 9. Exit codes

```text
0: pass
1: semantic warning or blocked round-trip
2: parser parity or semantic failure
```

## 10. Next step

```text
Phase 6D-4 Normalization installer removal trial
remove install_normalization only
retain local helper definitions during trial
update direct-installer inventory to Packet-only
run contract/migration/checker/property/full suites
```

## 11. Trust boundary

```text
validator/contract/migration pass != semantic equivalence
validator/contract/migration pass != complete safety proof
validator/contract/migration pass != adapter retirement proof
validator/contract/migration pass != RT:v
validator/contract/migration pass != execution authority
CI pass != release readiness
```
