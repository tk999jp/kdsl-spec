# Phase 6D-3 — Packet Normalization Consumer Contract and Migration

status: completed / integrated
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
contract_pull_request: 89
contract_source_head: 91db0dfac8787c20d6abe9fe8bfa2872971e5bc6
contract_squash_commit: 0ec72d29698679b1e09bd3258eaf3c16d8bd80af
contract_workflow: 29288968298 / 349 / success
migration_pull_request: 90
migration_source_head: 5a0cecc1130f9fe022a5cb574bda8c36f274dbee
migration_squash_commit: a031eb3b2b71d19a0f549d4f69c9cbcd73f984df
migration_workflow: 29289185279 / 351 / success
validator_authority: non-authoritative

## 1. Goal

Migrate the Packet Normalization round-trip consumer from structural helper imports re-exported by `kdsl_packet_normalization.py` to `NormalizationCompatibilityView`, after freezing its current returned contract with mutation/property evidence.

```text
contract corpus first
consumer migration second
installer removal deferred
```

## 2. Consumer graph

Before migration:

```text
kdsl_packet_roundtrip.py
  parse_normalization()
  imports:
    extract_scope
    parse_top_level
    blocks_from_entries
    parse_nested_scalars
    parse_list_records
    parse_nested_lists
    extract_multiline
  from kdsl_packet_normalization.py

kdsl_packet_property.py
  imports parse_normalization from kdsl_packet_roundtrip.py
```

After migration:

```text
kdsl_packet_roundtrip.py
  parse_normalization()
  consumes NormalizationCompatibilityView

kdsl_packet_property.py
  indirect consumer unchanged
```

## 3. Contract corpus

Added:

```text
tools/validator/run_normalization_consumer_contract_samples.py
```

Ten cases freeze:

```text
valid nested scalar contract
MAP record order
PRESERVE and preview content
fenced repository example scope
blocked P1 artifact
missing envelope error
nested scalar duplicate last-wins behavior
nested list order
preview block text
unsafe boundary value extraction without coercion
```

Returned dictionary shape:

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

## 4. Migration

Modified:

```text
tools/validator/kdsl_packet_roundtrip.py
```

Removed:

```text
structural imports from kdsl_packet_normalization
```

Added:

```text
NormalizationCompatibilityView
```

The returned dictionary is reconstructed through:

```text
view.values
view.nested_scalars(...)
view.list_records(...)
view.nested_lists(...)
view.multiline(...)
```

## 5. Migration verification

Added:

```text
tools/validator/run_normalization_consumer_migration_samples.py
```

Three cases verify:

```text
legacy Normalization structural import is absent
AST v2 CompatibilityView import is present
valid artifact contract remains
blocked P1 artifact contract remains
```

The static import check and runtime checks are grouped into three cases.

## 6. Final verification

```text
consumer contract: 10 / failed 0
consumer migration: 3 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 24
unified expectations: 375 / failed 0
workflow run: 29289185279 / #351
KDSL Validation: success
Packet Semantic Property: success
```

## 7. Critical boundaries retained

```text
STATUS: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
OUTPUT.executable: false
Packet executable: no
Packet state: not_normalized
```

Unsafe mutated values are extracted unchanged so downstream validation can reject them. No parser-side safety repair or default inference was added.

## 8. Dependency impact

Cleared blocking consumer:

```text
kdsl_packet_roundtrip.py -> kdsl_packet_normalization structural helpers
```

Still retained:

```text
kdsl_packet_normalization.py -> install_normalization
```

Therefore:

```text
Normalization structural consumer migration: complete
Normalization direct-installer removal proof: pending
adapter retirement: blocked
```

## 9. Trust boundary

```text
contract/migration pass != semantic equivalence
contract/migration pass != complete safety proof
contract/migration pass != adapter retirement proof
contract/migration pass != U approval
contract/migration pass != RT:v
contract/migration pass != execution authority
CI pass != release readiness
```

No tag, release, stable/public-ready state, executable target, or Release Asset was created.

## 10. Next safe step

Phase 6D-4 candidate:

```text
Normalization installer removal trial
remove install_normalization only
retain local helper definitions temporarily
update direct-installer inventory to Packet-only
run consumer contract/migration/checker/property/full suites
```

Stop when:

```text
unknown Normalization helper consumer appears
checker or round-trip exit changes
non-executable/not_proven/none boundary changes
property suite changes
```

## 11. Closeout decision

```text
Phase 6D-3A consumer contract: integrated
Phase 6D-3B consumer migration: integrated
Normalization installer removal: pending
adapter retirement: blocked
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v: not granted
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
