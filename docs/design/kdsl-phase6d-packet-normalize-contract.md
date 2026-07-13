# Phase 6D-5A — Packet Normalize Consumer Contract Corpus

status: design-draft / additive evidence slice
repository: tk999jp/kdsl-spec
tracking_issue: 55
review_date: 2026-07-14

## 1. Purpose

Freeze the current structural contract returned by `kdsl_packet_normalize.collect_data()` before replacing its structural imports from `kdsl_packet` with `PacketCompatibilityView`.

```text
contract corpus first
collect_data migration second
install_packet removal later
```

## 2. Consumer graph

Direct structural consumer:

```text
kdsl_packet_normalize.py
  collect_data()
```

Current imported structural helpers:

```text
extract_packet_scope
parse_top_level
blocks_from_entries
parse_nested_scalars
parse_list_field
parse_sequence_items
```

Current imported nonstructural helpers:

```text
load_text
unquote
```

Indirect consumers:

```text
kdsl_packet_roundtrip.py
kdsl_packet_property.py
kdsl_packet_normalize_semantic.py
```

## 3. Returned contract

`collect_data(text)` returns:

```text
values
base_id
task_id
src
read
tgt
obs
goal
non
stop
verify
sg_records
flow_records
authority
normalize_target
result_schema
```

The contract includes list and record order, first-scope behavior, quoting behavior, and last-value duplicate behavior.

## 4. Corpus properties

The additive corpus must detect:

```text
valid scalar and nested-scalar extraction
sequence order drift
Safety Gate record order drift
FLOW record order drift
AUTHORITY/NORMALIZE/OUT extraction drift
fenced repository example scope drift
missing PACKET_DRAFT handling drift
duplicate nested scalar resolution drift
sequence mutation order drift
unsafe Packet boundary value coercion
```

## 5. Expected legacy behavior

```text
first PACKET_DRAFT marker selected
fenced repository examples remain parseable
top-level values returned without semantic repair
nested scalar duplicates resolve last value
sequence and record order preserved
missing envelope raises ValueError
unsafe STATUS/NORMALIZE/AUTHORITY values remain observable for downstream rejection
```

## 6. Migration boundary

Phase 6D-5A must not:

```text
change kdsl_packet_normalize imports
change collect_data implementation
remove install_packet
change Packet semantic/property rules
claim semantic equivalence
claim adapter retirement readiness
```

## 7. Critical invariants

```text
Packet STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
execution_authority: none
PKT:v1 prohibited
```

The contract corpus may inject violating values to prove extraction fidelity, but those mutations are test artifacts and do not alter canonical rules.

## 8. Verification target

```text
new collect_data contract cases: 10
previous unified runners: 25
previous unified expectations: 379
expected unified runners: 26
expected unified expectations: 389
```

## 9. Next step

After this corpus succeeds:

```text
Phase 6D-5B:
  migrate collect_data() to PacketCompatibilityView
  keep returned dictionary shape identical
  keep the 10-case corpus unchanged
  re-run property/round-trip/inventory/matrix/full suites
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
