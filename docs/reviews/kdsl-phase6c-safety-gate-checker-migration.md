# Phase 6C-6 — Safety Gate Checker Migration

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 69
implementation_source_head: fda782f69eb020f50a6670d7529c8a830c116d4e
implementation_squash_commit: bfc034c44473232cee5107c53483a0b080e25a46
workflow_run_id: 29231502084
workflow_run_number: 305
workflow_conclusion: success

## 1. Goal

Move the active Safety Gate checker structural input from the Phase 1 namespace adapter to the AST v2 `SafetyGateCompatibilityView` without changing Safety Gate semantic, composition, authority, inheritance, or graph policy.

```text
structural migration only
legacy-v2 parity guard retained
semantic/safety rules unchanged
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_safety_gate.py
tools/validator/run_all_samples.py
```

Added:

```text
tools/validator/run_safety_gate_migration_samples.py
tools/validator/samples/parser-v2/safety_gate_no_entries_field.md
```

Unchanged:

```text
spec/registry/kdsl-safety-gate-registry.md
tools/validator/kdsl_safety_gate_inheritance.py
tools/validator/kdsl_safety_gate_graph.py
tools/validator/kdsl_safety_semantics.py
```

## 3. Active checker path

```text
input
→ SafetyGateCompatibilityView
→ Phase 1 / AST v2 structural parity guard
→ mismatch: fail before semantic validation
→ match: existing Safety Gate semantic validation
```

The active checker no longer calls:

```text
install_safety_gate(globals())
```

Module-level `extract_gate_block` and `parse_registry` helpers remain for existing imports by inheritance, graph, optional R1C, and semantic helper modules. Their safety meanings were not changed.

## 4. Migrated structural surface

```text
SAFETY_GATES presence
legacy-compatible selected scope
registry value
entry order
entry field order
entry values
fenced repository example selection
out-of-scope absence
```

The checker consumes:

```text
view.block_text
view.registry
view.entry_dicts
```

## 5. Parity guard

Before semantic validation, the checker executes:

```text
compare_safety_gate_legacy_v2(text)
```

On mismatch:

```text
STATUS: fail
Safety Gate parser parity guard: <difference>
semantic validation: not entered
```

On match:

```text
Safety Gate parser parity guard: pass
Safety Gate structural extraction: AST v2 compatibility view
```

## 6. Unsupported shape guard

The migration adds a malformed legacy-tolerated structure where records appear without the required `entries:` field.

```text
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  - id: SG-SCOPE
```

Phase 1 scanning can observe a record while the typed AST v2 structure cannot represent it as a valid `entries` record sequence. The parity guard rejects this divergence before semantic validation.

```text
unsupported structural divergence→fail closed
unknown structure→推測/補正禁止
```

## 7. Semantic and safety rules retained

Unchanged:

```text
registry identifier validation
known Safety Gate ID validation
required fields
state:hold/satisfied/blocked/na handling
state:satisfied evidence requirement
state:satisfied authority basis requirement
state:blocked evidence warning
state:na reason requirement
dev-prompt baseline gates
operation-triggered composition rules
protected wording groups
operation-specific authority wording
aggregate state calculation
inheritance transitions
graph/semantic relations
```

Critical protections remain:

```text
hold/blocked gate削除禁止
未確認→確認済扱禁止
未実行→実行済扱禁止
build/diff/lint/test/CI pass != RT:v
NEXT実行許可扱禁止
COMMIT自動commit許可扱禁止
public履歴/公開済tag/Release Assets保護
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
```

## 8. Verification

```text
implementation PR: 69
source head: fda782f69eb020f50a6670d7529c8a830c116d4e
squash commit: bfc034c44473232cee5107c53483a0b080e25a46
workflow run: 29231502084 / #305
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
Safety Gate structural parity: 8 / failed 0
Safety Gate active-checker migration: 4 / failed 0
unified runners: 14
unified expectations: 307 / failed 0
```

Migration cases:

```text
repository example remains valid
unknown registry remains semantic failure
absent Safety Gate remains out-of-scope pass
unsupported no-entries shape is blocked by parity guard
```

## 9. Authority boundary

```text
parser parity pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
CI pass != release readiness
```

No operation was performed on:

```text
tag
stable release
public-ready state
Release Assets
published release history
```

## 10. Current migration state

```text
R1C checker: AST v2 compatibility extraction + parity guard
CompactPrompt checker: AST v2 compatibility extraction + parity guard
Safety Gate checker: AST v2 compatibility extraction + parity guard
remaining Phase 1 namespace-adapter consumers:
  Packet
  Packet Normalization
legacy adapter removal: prohibited
```

Inheritance and graph modules still consume the retained helper API; this phase does not claim their structural migration.

## 11. Known limitations

```text
not a complete YAML parser
not a natural-language safety proof
selected structural parity only
helper API remains for inheritance/graph/optional consumers
Packet and Packet Normalization views pending
Full R1 view pending
legacy adapter retirement proof incomplete
```

## 12. Next safe step

Candidate Phase 6C-7:

```text
Packet compatibility view/parity pilot
preserve Packet non-executable and not_normalized boundaries
checker switch deferred until parity evidence
```

Then:

```text
Packet checker migration
→ Packet Normalization view/migration
→ Full R1 view/migration
→ Phase 6D mutation/property/repository corpus
→ legacy adapter retirement decision
```

## 13. Closeout decision

```text
Phase 6C-6 Safety Gate checker migration: integrated
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
Packet executable: no
Packet state: not_normalized
public_ready: no
stable_release: none
Release Assets: none
```
