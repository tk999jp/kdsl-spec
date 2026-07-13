# Phase 6C-7 — Packet Compatibility View Pilot

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 71
implementation_source_head: 4cd323da5908b4023c8c6c1bf1deb53703e69a37
implementation_squash_commit: 5b158c667a266ee1e10e2337eee9f0260f6b02ba
workflow_run_id: 29232149425
workflow_run_number: 309
workflow_conclusion: success

## 1. Goal

Add a bounded AST v2 structural view for `PACKET_DRAFT` and prove parity with every Phase 1 structural helper consumed by the active Packet checker before any checker switch.

```text
structural parity first
checker switch deferred
Packet non-executable/not_normalized boundaries unchanged
```

## 2. Integrated files

Added:

```text
tools/validator/kdsl_parser_v2_packet_compat.py
tools/validator/kdsl_parser_v2_packet_parity.py
tools/validator/run_parser_v2_packet_parity_samples.py
```

Updated:

```text
tools/validator/run_all_samples.py
```

Unchanged:

```text
tools/validator/kdsl_packet.py
tools/validator/kdsl_parser_adapter.py
spec/packet/*
spec/registry/*
```

## 3. Compatibility surface

The view records and compares:

```text
PACKET_DRAFT presence
exact Phase 1 selected scope
top-level field order
inline top-level values
relative field line numbers
duplicate top-level field order
raw block boundaries
nested scalar values and duplicate order
SG.id list order
FLOW.op list order
SRC/READ/TGT/OBS/NON/STOP/VERIFY sequence items
```

Typed records:

```text
DocumentNodeV2
EnvelopeNodeV2
FieldNodeV2
SourceSpanV2
PacketBlockNodeV2
PacketCompatibilityView
```

## 4. Phase 1 contract compared

The parity comparison directly executes:

```text
extract_scope_lines(..., PACKET_DRAFT)
parse_top_level_legacy
blocks_from_entries_legacy
parse_nested_scalars_legacy
parse_list_field_legacy
parse_sequence_items_legacy
```

The AST v2 view reconstructs the same structural outputs from source-spanned fields and raw block text.

```text
parity target:=checker-consumed structural contract
semantic validity:=not evaluated by parity checker
```

## 5. Fenced example boundary

The repository Packet example is inside a Markdown fence.

```text
AST v2 active-document: fenced example inactive
Phase 1 Packet parser: first PACKET_DRAFT marker selected
PacketCompatibilityView: independently selects the same legacy-compatible scope
selected scope→raw-envelope parse
```

General AST v2 fenced-example isolation is unchanged.

## 6. Semantic and authority boundary retained

The view does not decide:

```text
Packet schema validity
STATUS validity
BASE/TASK/FLOW/SG registry or ID validity
required top-level fields/order policy
TASK-required FLOW composition
TASK-required Safety Gate composition
trigger-required Safety Gates
GOAL placeholder policy
AUTHORITY rail validity
OUT result schema validity
NORMALIZE target/state validity
Packet executability
normalization completion
execution authority
```

These remain in `kdsl_packet.py` and related Packet property modules.

Critical invariants:

```text
Packet STATUS:=non-executable
NORMALIZE.required:=true
NORMALIZE.state:=not_normalized
Packet executable:no
execution_authority:none
PKT:v1使用禁止
normalization preview != executable target
```

## 7. Verification

```text
source head: 4cd323da5908b4023c8c6c1bf1deb53703e69a37
workflow run: 29232149425 / #309
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
Packet parity: 8 / failed 0
previous unified runners: 14
current unified runners: 15
previous unified expectations: 307
current unified expectations: 315 / failed 0
```

Cases:

```text
valid Packet sample
fenced repository Packet example
unknown schema
executable STATUS
missing READ
FLOW order violation
authority warning
out-of-scope document
```

Semantically invalid Packet samples are expected to pass structural parity because this pilot compares extraction equality, not Packet validity.

## 8. Current migration state

```text
Packet compatibility view: integrated
Packet structural parity corpus: integrated
Packet checker switch: not performed
Phase 1 adapter: retained
Packet semantic/property checker: unchanged
```

Current active Packet path:

```text
kdsl_packet.py
→ install_packet(globals())
→ Phase 1 structural helpers
→ existing Packet semantic validation
```

## 9. Safety and trust boundary

```text
parity pass != semantic equivalence
parity pass != complete safety proof
parity pass != U approval
parity pass != RT:v
parity pass != execution authority
validator/CI pass != release readiness
```

No operation was performed on:

```text
published tag
stable release
public-ready state
Release Assets
Packet normalization output
executable prompt or P1/P1L target
```

## 10. Known limitations

```text
checker has not switched to PacketCompatibilityView
complete nested language semantics not proven
selected parity corpus is bounded
Packet semantic equivalence not proven
normalization completion not proven
Packet Normalization compatibility view pending
Full R1 compatibility view pending
legacy adapter retirement proof incomplete
```

## 11. Next safe step

Candidate Phase 6C-8:

```text
migrate kdsl_packet.py structural extraction to PacketCompatibilityView
retain in-process Phase 1/AST v2 parity guard
keep all Packet semantic/property rules unchanged
add active-checker divergence guard before merge
```

Stop when:

```text
existing Packet checker exits change
Packet STATUS non-executable weakens
NORMALIZE.required true weakens
NORMALIZE.state not_normalized weakens
authority rails or PKT:v1 policy changes
unknown schema/default inference is required
```

## 12. Closeout decision

```text
Phase 6C-7 Packet compatibility pilot: integrated
Packet checker migration: pending
Issue #55: remain open
semantic equivalence: not_proven
normalization completion: not_proven
Packet executable: no
Packet state: not_normalized
public_ready: no
stable_release: none
Release Assets: none
```
