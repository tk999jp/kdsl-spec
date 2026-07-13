# Phase 6D-3A — Packet Normalization Consumer Contract Corpus

status: design-draft / additive evidence slice
repository: tk999jp/kdsl-spec
tracking_issue: 55
review_date: 2026-07-14

## 1. Purpose

Freeze the current structural contract consumed by `kdsl_packet_roundtrip.parse_normalization()` before replacing its imports from `kdsl_packet_normalization` with `NormalizationCompatibilityView`.

```text
contract corpus first
consumer import migration second
installer removal later
```

## 2. Consumer graph

Direct structural consumer:

```text
kdsl_packet_roundtrip.py
  parse_normalization()
```

Current imported helpers:

```text
extract_scope
parse_top_level
blocks_from_entries
parse_nested_scalars
parse_list_records
parse_nested_lists
extract_multiline
```

Indirect consumer:

```text
kdsl_packet_property.py
  imports parse_normalization from kdsl_packet_roundtrip.py
```

## 3. Returned contract

`parse_normalization(text)` returns:

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

The contract includes order and raw-value behavior, not only presence.

## 4. Corpus properties

The additive corpus must detect:

```text
valid top-level and nested scalar extraction
MAP record order drift
PRESERVE list order drift
OUTPUT.preview block-scalar drift
fenced repository example scope drift
blocked P1 artifact drift
missing NORMALIZATION_DRAFT handling drift
duplicate nested scalar resolution drift
nested-list mutation drift
non-executable/equivalence/authority value coercion
```

## 5. Expected legacy behavior

```text
first NORMALIZATION_DRAFT marker selected
fenced repository examples remain parseable
nested scalar duplicates resolve last value in returned mapping
record/list order preserved
preview text preserved after block dedent
missing envelope raises ValueError
values are extracted, not normalized into safer replacements
```

The last rule is essential: downstream semantic/property checks must see unsafe mutated values and reject them. Parser extraction must not silently repair them.

## 6. Migration boundary

Phase 6D-3A must not:

```text
change kdsl_packet_roundtrip imports
change parse_normalization implementation
remove install_normalization
change normalization semantic rules
claim semantic equivalence
claim adapter-retirement readiness
```

## 7. Critical invariants

```text
STATUS: non-executable
TARGET.executable:false
ROUND_TRIP.semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
Packet executable:no
Packet state:not_normalized
```

The contract corpus may inject violating values to prove extraction fidelity, but those mutations are test artifacts and do not alter canonical rules.

## 8. Verification target

```text
new consumer contract cases: 10
previous unified runners: 22
previous unified expectations: 362
expected unified runners: 23
expected unified expectations: 372
```

## 9. Next step

After this corpus succeeds:

```text
Phase 6D-3B:
  migrate parse_normalization() to NormalizationCompatibilityView
  keep returned dictionary shape identical
  keep dedicated contract corpus unchanged
  re-run inventory/matrix/full suite
```

## 10. Trust boundary

```text
contract pass != consumer migration
contract pass != semantic equivalence
contract pass != complete safety proof
contract pass != adapter retirement proof
contract pass != U approval
contract pass != RT:v
contract pass != execution authority
CI pass != release readiness
```
