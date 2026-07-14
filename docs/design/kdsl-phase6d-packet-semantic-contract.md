# Phase 6D-6A — Packet Semantic Consumer Contract Corpus

status: design-draft / additive evidence slice
repository: tk999jp/kdsl-spec
tracking_issue: 55
review_date: 2026-07-14

## 1. Purpose

Freeze the structural contract consumed by `kdsl_packet_semantic.parse_packet()` before replacing its structural imports from `kdsl_packet` with `PacketCompatibilityView`.

```text
contract corpus first
semantic consumer migration second
install_packet removal later
```

## 2. Direct consumer

```text
tools/validator/kdsl_packet_semantic.py
  parse_packet(text)
```

Current structural imports:

```text
extract_packet_scope
parse_top_level
blocks_from_entries
parse_nested_scalars
parse_sequence_items
```

Current nonstructural imports:

```text
AUTHORITY_RAILS
KNOWN_SG_IDS
SG_REGISTRY
load_text
unquote
```

## 3. Returned surface

`parse_packet(text)` returns:

```text
scope
duplicates
values
blocks
authority
normalize
obs
stop
verify
sg_records
flow_records
```

The contract includes first-scope selection, top-level duplicate reporting, last-value resolution, nested scalar resolution, sequence order, and record order.

## 4. Corpus properties

The additive corpus must detect:

```text
return-key drift
PACKET_DRAFT scope boundary drift
top-level value drift
OBS/STOP/VERIFY order drift
SG record order/field drift
FLOW record order/detail drift
AUTHORITY/NORMALIZE drift
top-level duplicate reporting/last-wins drift
nested duplicate last-wins drift
unsafe value coercion
missing-envelope error drift
```

## 5. Migration boundary

Phase 6D-6A must not:

```text
change kdsl_packet_semantic imports
change parse_packet implementation
change semantic decisions or exit codes
remove install_packet
change Packet checker/property/normalization behavior
claim semantic equivalence
claim adapter retirement readiness
```

## 6. Critical invariants

```text
Packet STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
execution_authority: none
PKT:v1 prohibited
```

Mutation cases may inject violating values to prove extraction fidelity. Such fixtures do not alter canonical rules and must remain rejected by downstream semantic validation.

## 7. Verification target

```text
new Packet semantic consumer contract cases: 10
previous unified runners: 27
previous unified expectations: 393
expected unified runners: 28
expected unified expectations: 403
```

## 8. Next step

After the contract corpus succeeds:

```text
Phase 6D-6B:
  migrate parse_packet() to PacketCompatibilityView
  retain return dictionary shape
  retain all 10 contract cases unchanged
  retain existing semantic/property exits
```

## 9. Trust boundary

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
