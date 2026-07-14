# Phase 6D-5B — Packet Normalize Consumer Migration

status: completed / integrated
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 96
implementation_source_head: fe98668da6b6dc23db6abfd28c9f3203a138d35b
implementation_squash_commit: 6f0b4d6c1ea1e7d6c1013f3cde23b57e6799f696
workflow_run_id: 29329029353
workflow_run_number: 363
workflow_conclusion: success

## 1. Goal

Migrate `kdsl_packet_normalize.collect_data()` from structural helper imports in `kdsl_packet` to `PacketCompatibilityView` while preserving its established return contract and downstream normalization/property behavior.

```text
contract corpus first: complete
consumer migration second: complete
install_packet removal: not performed
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_packet_normalize.py
tools/validator/run_all_samples.py
```

Added:

```text
tools/validator/run_packet_normalize_migration_samples.py
```

Unchanged:

```text
tools/validator/kdsl_packet_semantic.py
tools/validator/kdsl_packet.py installer boundary
tools/validator/kdsl_parser_adapter.py
spec/packet/*
spec/registry/*
```

## 3. Runtime path

Before:

```text
collect_data
→ extract_packet_scope
→ parse_top_level
→ blocks_from_entries
→ parse_nested_scalars / parse_sequence_items
```

After:

```text
collect_data
→ PacketCompatibilityView.from_text
→ view.values
→ view.nested_scalars
→ view.sequence_items
→ view.legacy_blocks for local SG/FLOW record parsing
```

Imports retained from `kdsl_packet`:

```text
load_text
unquote
```

Legacy structural imports removed:

```text
extract_packet_scope
parse_top_level
blocks_from_entries
parse_nested_scalars
parse_sequence_items
parse_list_field
```

## 4. Preserved return contract

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

Behavior retained:

```text
first PACKET_DRAFT selection
fenced repository example handling
nested duplicate last-wins
sequence and record order
unsafe value extraction without semantic repair
missing envelope exact ValueError
```

## 5. Verification

```text
implementation PR: 96
source head: fe98668da6b6dc23db6abfd28c9f3203a138d35b
squash commit: 6f0b4d6c1ea1e7d6c1013f3cde23b57e6799f696
workflow run: 29329029353 / #363
KDSL Validation: success
Packet Semantic Property: success
Packet normalize contract: 10 / failed 0
Packet normalize migration: 4 / failed 0
unified runners: 27
unified expectations: 393 / failed 0
```

Migration cases:

```text
legacy structural imports removed
PacketCompatibilityView import present
valid returned contract retained
missing-envelope error retained
```

## 6. Packet and authority boundary

```text
Packet STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
execution_authority: none
PKT:v1 prohibited
```

No Packet execution, normalization completion, edit authority, P1/P1L execution, commit, push, tag, release, or Release Asset was produced.

## 7. Current dependency state

```text
Packet normalize consumer migration: satisfied
Packet semantic consumer migration: pending
install_packet: retained
Packet installer removal proof: pending
adapter file retirement: blocked
```

## 8. Trust boundary

```text
contract/migration pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
validator pass != adapter retirement proof
CI pass != release readiness
```

## 9. Next safe step

Phase 6D-6A:

```text
freeze kdsl_packet_semantic.py consumer contract before import migration
cover scope, top-level, nested fields, SG/FLOW records, sequence order, and invalid-boundary observation
keep semantic decisions and exits unchanged
```

Then:

```text
Phase 6D-6B semantic consumer migration
→ Packet installer removal trial
→ adapter retirement decision last
```

## 10. Closeout decision

```text
Phase 6D-5B Packet normalize consumer migration: integrated
install_packet removal: not authorized
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
