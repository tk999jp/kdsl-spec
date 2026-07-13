# Phase 6D-5A — Packet Normalize Consumer Contract Corpus

status: completed / integrated
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 94
implementation_source_head: 6f9653b165664e471c48369e2b07fe676e6961f6
implementation_squash_commit: dc5a6689d69ad1580ece058f736ea23fd028ae81
workflow_run_id: 29290606329
workflow_run_number: 359
workflow_conclusion: success
validator_authority: non-authoritative

## 1. Goal

Freeze the structural contract returned by `kdsl_packet_normalize.collect_data()` before replacing its imports from `kdsl_packet` with `PacketCompatibilityView`.

```text
contract corpus first
consumer migration second
install_packet removal later
```

## 2. Consumer graph

Direct consumer:

```text
kdsl_packet_normalize.py
  collect_data()
```

Current structural imports:

```text
extract_packet_scope
parse_top_level
blocks_from_entries
parse_nested_scalars
parse_list_field
parse_sequence_items
```

Indirect consumers:

```text
kdsl_packet_roundtrip.py
kdsl_packet_property.py
kdsl_packet_normalize_semantic.py
```

## 3. Returned contract

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

## 4. Contract corpus

Ten cases verify:

```text
valid Packet scalar contract
Packet sequence order
Safety Gate record order
FLOW record order
Packet authority mapping
fenced repository Packet scope
missing Packet envelope error
duplicate nested scalar last-wins behavior
sequence mutation order
unsafe Packet value extraction without coercion
```

The parser-side consumer must expose unsafe mutations to downstream semantic/property validation rather than silently repairing them.

## 5. Verification

```text
workflow run: 29290606329 / #359
KDSL Validation: success
Packet Semantic Property: success
Packet normalize contract: 10 / failed 0
Normalization installer-removal: 4 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 26
unified expectations: 389 / failed 0
```

## 6. Migration boundary

```text
kdsl_packet_normalize.py structural imports: unchanged
collect_data implementation: unchanged
Packet direct installer: retained
Packet consumer migration: not performed
```

This phase proves the current consumer contract only.

## 7. Critical boundaries retained

```text
Packet STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
execution authority: none
PKT:v1 prohibited
```

## 8. Current dependency impact

Satisfied:

```text
collect_data consumer contract and mutation evidence
```

Pending:

```text
collect_data migration to PacketCompatibilityView
Packet semantic consumer contract/migration
Packet direct-installer removal
adapter file retirement
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

## 10. Next safe step

Phase 6D-5B:

```text
migrate collect_data() to PacketCompatibilityView
preserve returned dictionary contract
keep 10-case corpus unchanged
add static import and valid/property/round-trip migration cases
```

Stop when:

```text
returned contract changes
record/list order changes
unsafe values are coerced
Packet non-executable/not_normalized/authority boundaries weaken
```

## 11. Closeout decision

```text
Phase 6D-5A Packet normalize consumer contract: integrated
collect_data migration: pending
Packet installer removal: pending
adapter file retirement: blocked
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v: not granted
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
