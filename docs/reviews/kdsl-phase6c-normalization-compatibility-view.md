# Phase 6C-9 — Packet Normalization Compatibility View Pilot

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 75
implementation_source_head: c99a774ba7d58dcc7eac5e733cdc1d12a4b9e310
implementation_squash_commit: ceb8269c2f1b3fe84342bd0fcff6d36871385510
workflow_run_id: 29233236734
workflow_run_number: 317
workflow_conclusion: success

## 1. Goal

Add a bounded AST v2 structural view for `NORMALIZATION_DRAFT` and prove parity with every Phase 1 structural helper consumed by the active normalization checker before any checker switch.

```text
structural parity first
checker switch deferred
normalization remains draft/non-executable
semantic equivalence remains not_proven
execution authority remains none
```

## 2. Integrated files

Added:

```text
tools/validator/kdsl_parser_v2_normalization_compat.py
tools/validator/kdsl_parser_v2_normalization_parity.py
tools/validator/run_parser_v2_normalization_parity_samples.py
```

Updated:

```text
tools/validator/run_all_samples.py
```

Unchanged:

```text
tools/validator/kdsl_packet_normalization.py
tools/validator/kdsl_parser_adapter.py
spec/packet/*
spec/registry/*
```

## 3. Compatibility surface

Compared:

```text
NORMALIZATION_DRAFT presence
exact Phase 1 selected scope
top-level field order/value/relative line
duplicate top-level fields
raw block boundaries
SOURCE/TARGET/ROUND_TRIP/AUTHORITY/OUTPUT nested scalars
MAP/UNRESOLVED/LOSS list records
PRESERVE nested lists
OUTPUT.preview block scalar
```

Typed data:

```text
DocumentNodeV2
EnvelopeNodeV2
FieldNodeV2
SourceSpanV2
NormalizationBlockNodeV2
NormalizationCompatibilityView
```

## 4. Phase 1 contract compared

The parity comparison executes:

```text
extract_scope_lines(..., NORMALIZATION_DRAFT)
parse_top_level_legacy
blocks_from_entries_legacy
parse_nested_scalars_legacy
parse_list_records_legacy
parse_nested_lists_legacy
extract_multiline_legacy
```

```text
parity target:=checker-consumed structural contract
normalization semantic validity:=not evaluated by parity checker
```

## 5. Fenced example boundary

Repository normalization examples are inside Markdown fences.

```text
AST v2 active-document: fenced example inactive
Phase 1 normalization parser: first NORMALIZATION_DRAFT marker selected
NormalizationCompatibilityView: independently selects same legacy-compatible scope
selected scope→raw-envelope parse
```

General AST v2 fence behavior remains unchanged.

## 6. Semantic and authority boundary retained

The view does not decide:

```text
SCHEMA/STATUS validity
required field/order policy
SOURCE schema/digest/status/state
TARGET kind/schema/resolution/executable
MAP mode/evidence/accounting
UNRESOLVED impact/reason
LOSS class/detail/criticality
PRESERVE completeness
ROUND_TRIP state/structural/semantic equivalence
AUTHORITY source rails/execution authority
OUTPUT marker/executable/preview
blocked/resolved consistency
```

Critical invariants:

```text
normalization STATUS: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
executable KDSL_PROMPT/P1/P1L marker prohibited
PKT:v1 prohibited
normalization completion: not_proven
```

## 7. Verification

```text
source head: c99a774ba7d58dcc7eac5e733cdc1d12a4b9e310
workflow run: 29233236734 / #317
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
Normalization parity: 8 / failed 0
previous unified runners: 16
current unified runners: 17
previous unified expectations: 321
current unified expectations: 329 / failed 0
```

Cases:

```text
valid normalization sample
Full KDSL repository example
P1 blocked repository example
lossy blocked repository example
unknown schema
executable STATUS
semantic equivalence claim
out-of-scope document
```

Semantically invalid artifacts pass structural parity when extraction is equal; parity is not semantic acceptance.

## 8. Current migration state

```text
Normalization CompatibilityView: integrated
Normalization parity corpus: integrated
normalization checker switch: not performed
Phase 1 adapter: retained
```

Active normalization path:

```text
kdsl_packet_normalization.py
→ install_normalization(globals())
→ Phase 1 structural helpers
→ existing normalization semantic validation
```

## 9. Trust boundary

```text
parity pass != semantic equivalence
parity pass != normalization completion
parity pass != complete safety proof
parity pass != U approval
parity pass != RT:v
parity pass != execution authority
CI pass != release readiness
```

No executable target, P1/P1L, tag, stable release, public-ready change, or Release Asset was produced.

## 10. Known limitations

```text
checker has not switched to CompatibilityView
bounded corpus != complete language proof
normalization completion not proven
Packet helper consumers remain compatibility-bound
Full R1 view pending
legacy adapter retirement evidence incomplete
```

## 11. Next safe step

Candidate Phase 6C-10:

```text
migrate kdsl_packet_normalization.py structural extraction to NormalizationCompatibilityView
retain in-process Phase 1/AST v2 parity guard
keep all normalization semantic/authority/equivalence rules unchanged
add active-checker migration corpus
```

Stop when:

```text
existing normalization checker exits change
STATUS non-executable weakens
TARGET.executable:false weakens
ROUND_TRIP.semantic_equivalence:not_proven weakens
AUTHORITY.execution_authority:none weakens
executable marker prohibition weakens
unknown schema/default inference is required
```

## 12. Closeout decision

```text
Phase 6C-9 Normalization compatibility pilot: integrated
normalization checker migration: pending
Issue #55: remain open
semantic equivalence: not_proven
normalization completion: not_proven
execution authority: none
Packet executable: no
public_ready: no
stable_release: none
Release Assets: none
```
