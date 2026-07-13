# Phase 6C-10 — Packet Normalization Checker Structural Migration

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 77
implementation_source_head: cd70e15f8df7d1d17f7c5ee1f8348719cba327a0
implementation_squash_commit: 01f7c7c29aae98b1dfbb95ae416446c9e5b5f823
workflow_run_id: 29233820287
workflow_run_number: 321
workflow_conclusion: success

## 1. Goal

Move the active Packet Normalization checker's structural input to `NormalizationCompatibilityView` without changing normalization semantics, equivalence status, authority, or executability.

```text
active checker structural migration
Phase 1/AST v2 parity guard retained
helper API compatibility retained
normalization remains non-executable
semantic equivalence remains not_proven
execution authority remains none
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_packet_normalization.py
tools/validator/run_all_samples.py
```

Added:

```text
tools/validator/run_normalization_migration_samples.py
```

Unchanged:

```text
spec/packet/*
spec/registry/*
tools/validator/kdsl_packet_roundtrip.py
tools/validator/kdsl_packet_property.py
tools/validator/kdsl_packet_normalize.py
```

## 3. Active checker path

```text
input
→ NormalizationCompatibilityView
→ compare_normalization_legacy_v2
→ mismatch: fail before semantic validation
→ match: AST v2 scope/entries/duplicates/blocks
→ existing normalization semantic validation
```

The active checker consumes:

```text
view.scope_lines
view.entries
view.duplicates
view.values
view.legacy_blocks
```

Output markers:

```text
Normalization parser parity guard: pass
Normalization structural extraction: AST v2 compatibility view
```

## 4. Retained helper API boundary

Round-trip and property modules import normalization helper functions from `kdsl_packet_normalization.py`.

Therefore:

```text
install_normalization(globals()): retained
adapter-installed helper exports: retained
active checker scope/entry/block source: AST v2
helper consumers' separate migration: not claimed
```

This is intentional bounded compatibility. It does not weaken the active checker's AST v2 migration.

## 5. Structural parity guard

Before semantic validation:

```text
compare_normalization_legacy_v2(text)
```

Compared:

```text
NORMALIZATION_DRAFT presence/exact scope
top-level order/value/relative line/duplicates
raw block boundaries
nested scalar maps and duplicates
MAP/UNRESOLVED/LOSS records
PRESERVE nested lists
OUTPUT.preview block scalar
```

On mismatch:

```text
STATUS: fail
Normalization parser parity guard: <difference>
semantic validation: not entered
```

## 6. Semantic and authority policy retained

Unchanged:

```text
SCHEMA/STATUS validity
required top-level fields and order
SOURCE schema/digest/packet_status/normalize_state
TARGET kind/schema/resolution/executable
MAP mode/evidence/accounting
UNRESOLVED reason/impact
LOSS class/detail/criticality
PRESERVE classes
ROUND_TRIP state/structural_equivalence/semantic_equivalence
AUTHORITY source_rails_preserved/execution_authority
OUTPUT marker/executable/preview
blocked/resolved consistency
executable target marker prohibition
PKT:v1 prohibition
```

Critical invariants:

```text
STATUS: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
normalization_completion: not_proven
Packet executable: no
```

## 7. Verification

```text
implementation PR: 77
source head: cd70e15f8df7d1d17f7c5ee1f8348719cba327a0
squash commit: 01f7c7c29aae98b1dfbb95ae416446c9e5b5f823
workflow run: 29233820287 / #321
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
Normalization structural parity: 8 / failed 0
Normalization checker migration: 7 / failed 0
unified runners: 18
unified expectations: 336 / failed 0
```

Migration cases:

```text
valid artifact remains pass
Full KDSL example remains pass
P1 blocked example remains pass
unknown schema remains fail
executable STATUS remains fail
semantic equivalence claim remains fail
out-of-scope input remains pass
```

## 8. Current migration state

```text
R1C checker: AST v2 + parity guard
CompactPrompt checker: AST v2 + parity guard
Safety Gate checker: AST v2 + parity guard
Packet base checker: AST v2 + parity guard
Packet Normalization checker: AST v2 + parity guard
helper exports: Phase 1-compatible for dependent modules
```

No active base checker remains solely on the Phase 1 namespace-adapter path. Legacy adapter removal is still prohibited because helper consumers and Full R1 migration evidence remain incomplete.

## 9. Trust boundary

```text
parity pass != semantic equivalence
validator pass != normalization completion
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
CI pass != release readiness
```

No executable target, P1/P1L execution, tag, stable release, public-ready change, or Release Asset was produced.

## 10. Known limitations

```text
round-trip/property helper imports remain Phase 1-compatible
Full R1 CompatibilityView pending
helper-consumer migration decision pending
selected parity corpus != complete language proof
normalization completion not proven
legacy adapter retirement evidence incomplete
```

## 11. Next safe step

Candidate Phase 6C-11:

```text
Full R1 structural compatibility inventory and bounded view/parity pilot
retain canonical R1 semantic checker behavior
preserve RT/NEXT/COMMIT evidence and authority boundaries
```

Then:

```text
Full R1 checker migration
→ helper-consumer migration decision
→ Phase 6D mutation/property/repository corpus
→ legacy adapter retirement decision
```

## 12. Closeout decision

```text
Phase 6C-10 Normalization checker migration: integrated
Issue #55: remain open
semantic equivalence: not_proven
normalization completion: not_proven
execution authority: none
Packet executable: no
public_ready: no
stable_release: none
Release Assets: none
```
