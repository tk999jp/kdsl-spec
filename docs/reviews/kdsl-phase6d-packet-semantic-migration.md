# Phase 6D-6B — Packet Semantic Consumer Migration

status: completed / integrated
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 100
implementation_source_head: 41dea6754eade558ea226e38c9078244c73165cb
implementation_squash_commit: 047380b1b7f2a7c47b8ed7f74e7a73f016e08b9e
workflow_run_id: 29330823674
workflow_run_number: 371
workflow_conclusion: success

## 1. Goal

Migrate `kdsl_packet_semantic.parse_packet()` from structural helper imports in `kdsl_packet` to `PacketCompatibilityView` while preserving its frozen return contract and all semantic/property decisions.

```text
contract corpus first: complete
semantic consumer migration: complete
install_packet removal: not performed
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_packet_semantic.py
tools/validator/run_all_samples.py
```

Added:

```text
tools/validator/run_packet_semantic_migration_samples.py
```

Unchanged:

```text
tools/validator/kdsl_packet.py installer boundary
tools/validator/kdsl_parser_adapter.py
spec/packet/*
spec/registry/*
```

## 3. Runtime path

Before:

```text
parse_packet
→ extract_packet_scope
→ parse_top_level
→ blocks_from_entries
→ parse_nested_scalars / parse_sequence_items
```

After:

```text
parse_packet
→ PacketCompatibilityView.from_text
→ view.scope_lines / duplicates / values / legacy_blocks
→ view.nested_scalars / sequence_items
→ existing local SG/FLOW record parsing
```

SG registry extraction also uses `PacketCompatibilityView`.

Imports retained from `kdsl_packet`:

```text
AUTHORITY_RAILS
KNOWN_SG_IDS
SG_REGISTRY
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
```

## 4. Preserved return contract

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

## 5. Semantic behavior retained

```text
OBS classification and conflict rules
Safety Gate fields/state/evidence/authority rules
protected wording checks
FLOW/Authority consistency rules
VERIFY requirement-vs-completed-evidence rules
NORMALIZE.state:not_normalized requirement
executable marker prohibition
output status and exit codes
```

## 6. Verification

```text
implementation PR: 100
source head: 41dea6754eade558ea226e38c9078244c73165cb
squash commit: 047380b1b7f2a7c47b8ed7f74e7a73f016e08b9e
workflow run: 29330823674 / #371
KDSL Validation: success
Packet Semantic Property: success
Packet semantic contract: 10 / failed 0
Packet semantic migration: 4 / failed 0
unified runners: 29
unified expectations: 407 / failed 0
```

Migration cases:

```text
legacy structural imports removed
PacketCompatibilityView import present
return contract retained
valid semantic result and NORMALIZE-state rejection retained
```

## 7. Packet and authority boundary

```text
Packet STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
execution_authority: none
PKT:v1 prohibited
```

No Packet execution, edit authority, P1/P1L execution, commit, push, tag, release, or Release Asset was produced.

## 8. Current dependency state

```text
Packet normalize consumer migration: satisfied
Packet semantic consumer migration: satisfied
install_packet: retained
Packet installer removal proof: pending
adapter file retirement: blocked
```

## 9. Trust boundary

```text
contract/migration pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
validator pass != adapter retirement proof
CI pass != release readiness
```

## 10. Next safe step

Phase 6D-7:

```text
re-run exact Packet helper-consumer inventory
separate parity-only and semantic-constant consumers
attempt Packet installer removal only when no runtime structural consumer remains
add installer-removal corpus before changing adapter file
```

## 11. Closeout decision

```text
Phase 6D-6B Packet semantic consumer migration: integrated
install_packet removal: not authorized until inventory proof
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
