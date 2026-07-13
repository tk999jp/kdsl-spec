# Packet Normalization Parser v2 Compatibility Notes

status: checker-migrated / round-trip-consumer-migrated / direct-installer-removed
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
installer removal PR: 92
installer removal squash: 1e488c6fedb792cd1a40a003b68c374af93b7dae
latest workflow: 29290086908 / 355 / success
```

## 1. Purpose

Provide a source-spanned Normalization structural view used by both the active checker and the round-trip consumer without changing semantic, equivalence, authority, or executability rules.

```text
parser/consumer migration != semantic equivalence
parser/consumer migration != normalization completion
installer removal != adapter file retirement proof
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

## 4. Direct installer state

Removed in PR #92:

```text
from kdsl_parser_adapter import install_normalization
install_normalization(globals())
```

Retained locally in `kdsl_packet_normalization.py`:

```text
extract_scope
parse_top_level
blocks_from_entries
parse_nested_scalars
parse_list_records
parse_nested_lists
extract_multiline
```

These helpers remain for parity comparison and bounded compatibility evidence. They are not installed through `kdsl_parser_adapter`.

## 5. Contract and migration evidence

```text
Normalization structural parity: 8 / failed 0
Normalization checker migration: 7 / failed 0
Normalization consumer contract: 10 / failed 0
Normalization consumer migration: 3 / failed 0
Normalization installer removal: 4 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 25
unified expectations: 379 / failed 0
workflow run: 29290086908 / #355
KDSL Validation: success
Packet Semantic Property: success
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
static consumer migration
valid/blocked runtime contracts
direct installer absence
property path without installer
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

## 7. Current dependency boundary

```text
active checker: AST v2 CompatibilityView
round-trip consumer: AST v2 CompatibilityView
property consumer: indirect parse_normalization API
Normalization direct adapter installer: absent
local parity helpers: retained
Packet direct adapter installer: retained elsewhere
adapter file retirement: blocked
```

## 8. Exit codes

```text
0: pass
1: semantic warning or blocked round-trip
2: parser parity or semantic failure
```

## 9. Next step

```text
Phase 6D-5 Packet helper-consumer contract inventory
consumer-specific mutation/property corpus
Packet consumer migration before install_packet removal
```

## 10. Trust boundary

```text
validator/contract/migration/installer-removal pass != semantic equivalence
validator/contract/migration/installer-removal pass != complete safety proof
validator/contract/migration/installer-removal pass != adapter file retirement proof
validator/contract/migration/installer-removal pass != RT:v
validator/contract/migration/installer-removal pass != execution authority
CI pass != release readiness
```
