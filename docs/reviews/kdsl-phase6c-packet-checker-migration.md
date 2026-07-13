# Phase 6C-8 — Packet Checker Structural Migration

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 73
implementation_source_head: e764b8efa41fdb0f2512985a0750302d6d57aabb
implementation_squash_commit: 52675d02969123f7329727fdddfcf5e0813a377e
workflow_run_id: 29232739675
workflow_run_number: 313
workflow_conclusion: success

## 1. Goal

Move the active Packet base checker's structural input to `PacketCompatibilityView` without changing Packet schema, semantic/property, normalization, authority, or executability policy.

```text
active base checker structural migration
Phase 1/AST v2 parity guard retained
helper API compatibility retained
Packet remains non-executable and not_normalized
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_packet.py
tools/validator/run_all_samples.py
```

Added:

```text
tools/validator/run_packet_migration_samples.py
```

Unchanged:

```text
spec/packet/*
spec/registry/*
tools/validator/kdsl_packet_semantic.py
tools/validator/kdsl_packet_property.py
tools/validator/kdsl_packet_normalization.py
tools/validator/kdsl_packet_normalize.py
tools/validator/kdsl_packet_roundtrip.py
```

## 3. Active base checker path

```text
input
→ PacketCompatibilityView
→ compare_packet_legacy_v2
→ mismatch: fail before semantic validation
→ match: AST v2 scope/entries/duplicates/blocks
→ existing Packet semantic validation
```

The active base checker now consumes:

```text
view.scope_lines
view.entries
view.duplicates
view.values
view.legacy_blocks
```

Output markers:

```text
Packet parser parity guard: pass
Packet structural extraction: AST v2 compatibility view
```

## 4. Retained helper API boundary

`kdsl_packet_semantic.py`, normalization, property and round-trip modules import helper functions from `kdsl_packet.py`.

Therefore:

```text
install_packet(globals()): retained
adapter-installed helper exports: retained
active base checker scope/entry/block source: AST v2
helper consumers' separate migration: not claimed
```

This is intentional bounded compatibility, not incomplete execution of the active base checker migration.

## 5. Structural parity guard

Before Packet semantic validation:

```text
compare_packet_legacy_v2(text)
```

Compared:

```text
PACKET_DRAFT presence/exact scope
top-level order/value/relative line/duplicates
raw block boundaries
nested scalar maps and duplicates
SG.id lists
FLOW.op lists
sequence fields
```

On mismatch:

```text
STATUS: fail
Packet parser parity guard: <difference>
semantic validation: not entered
```

## 6. Semantic and authority policy retained

Unchanged:

```text
SCHEMA: kdsl-packet@0.1-draft
STATUS must be non-executable
required top-level fields and order
BASE/TASK registries and IDs
TASK-required FLOW opcodes
FLOW-GATE/FLOW-CHANGE/FLOW-STOP order
SG registry and Safety Gate IDs
TASK-required and trigger-required Safety Gates
GOAL placeholder rejection
OUT result schema
AUTHORITY rails and allowed values
NORMALIZE required/target/state
PKT:v1 prohibition
list-empty warnings
```

Critical invariants:

```text
STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
normalization_required: yes
normalization_completion: not_proven
execution_authority: none
FLOW-CHANGE != edit authority
```

## 7. Verification

```text
implementation PR: 73
source head: e764b8efa41fdb0f2512985a0750302d6d57aabb
squash commit: 52675d02969123f7329727fdddfcf5e0813a377e
workflow run: 29232739675 / #313
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
Packet structural parity: 8 / failed 0
Packet checker migration: 6 / failed 0
unified runners: 16
unified expectations: 321 / failed 0
```

Migration cases:

```text
valid Packet remains pass
fenced repository example remains pass
unknown schema remains fail
executable STATUS remains fail
authority widening remains warning and non-executable
out-of-scope input remains pass
```

## 8. Current migration state

```text
R1C base checker: AST v2 + parity guard
CompactPrompt checker: AST v2 + parity guard
Safety Gate checker: AST v2 + parity guard
Packet base checker: AST v2 + parity guard
Packet helper API consumers: Phase 1-compatible exports retained
Packet Normalization checker: Phase 1 adapter path
```

Legacy adapter removal remains prohibited.

## 9. Trust boundary

```text
parity pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
CI pass != release readiness
```

No operation was performed on:

```text
Packet normalization output
executable prompt
P1/P1L target
tag
stable release
public-ready state
Release Assets
```

## 10. Known limitations

```text
Packet semantic/property helper imports remain Phase 1-compatible
Packet Normalization CompatibilityView pending
Full R1 CompatibilityView pending
selected parity corpus != full semantic proof
normalization completion not proven
legacy adapter retirement evidence incomplete
```

## 11. Next safe step

Candidate Phase 6C-9:

```text
Packet Normalization compatibility view/parity pilot
checker switch deferred until parity evidence
preserve draft/non-executable/semantic_equivalence:not_proven boundaries
```

Then:

```text
Packet Normalization checker migration
→ Full R1 compatibility view/migration
→ helper consumer migration decision
→ Phase 6D mutation/property/repository corpus
→ legacy adapter retirement decision
```

## 12. Closeout decision

```text
Phase 6C-8 Packet checker migration: integrated
Issue #55: remain open
Packet semantic equivalence: not_proven
normalization completion: not_proven
Packet executable: no
Packet state: not_normalized
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
