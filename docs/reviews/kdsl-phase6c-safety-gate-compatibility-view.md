# Phase 6C-5 — Safety Gate Compatibility View Pilot

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 67
implementation_source_head: ce0f45852a2d2baf81e09371e8534ea2026051e0
implementation_squash_commit: 604e4e1f8f8c601f7054b15b38e3c5db40d88056
workflow_run_id: 29230830767
workflow_run_number: 301
workflow_conclusion: success

## 1. Goal

Add a bounded AST v2 structural view for Safety Gate documents and prove parity with the Phase 1 parser before changing the active checker.

```text
structural parity first
checker switch deferred
Safety Gate semantic/safety policy unchanged
```

## 2. Integrated files

```text
tools/validator/kdsl_parser_v2_safety_gate_compat.py
tools/validator/kdsl_parser_v2_safety_gate_parity.py
tools/validator/run_parser_v2_safety_gate_parity_samples.py
```

Updated:

```text
tools/validator/run_all_samples.py
```

Unchanged:

```text
tools/validator/kdsl_safety_gate.py
tools/validator/kdsl_parser_adapter.py
spec/registry/kdsl-safety-gate-registry.md
```

## 3. Compatibility surface

The view records and compares:

```text
SAFETY_GATES presence
exact Phase 1 selected scope
registry value
entry order
entry field order
entry field values
fenced repository example selection
out-of-scope absence
```

Typed view records:

```text
DocumentNodeV2
scope-local DocumentNodeV2
EnvelopeNodeV2
SafetyGateEntryNodeV2
SourceSpanV2
```

## 4. Scope and indentation handling

The repository example places its active Safety Gate block inside a Markdown fence. AST v2 `active-document` intentionally excludes fenced examples, while Phase 1 selects the first `SAFETY_GATES:` marker.

Compatibility behavior:

```text
first legacy-compatible SAFETY_GATES scope selected independently
exact original scope retained for parity
scope-local copy dedented for AST v2 raw-envelope parsing
AST v2 general indentation behavior unchanged
AST v2 active-document fence behavior unchanged
```

The dedent is view-local and does not mutate source text or canonical parser rules.

## 5. Semantic boundary retained

The view does not decide:

```text
registry validity
known Safety Gate ID validity
state validity
required fields
satisfied/blocked/na rules
dev-prompt baseline gates
composition requirements
protected wording
operation-specific authority wording
inheritance transitions
graph semantics
aggregate safety meaning
```

These remain in the existing checker and related modules.

```text
CompatibilityView != Safety Gate semantic checker
parity pass != safety proof
```

## 6. Verification

```text
source head: ce0f45852a2d2baf81e09371e8534ea2026051e0
workflow run: 29230830767 / #301
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
Safety Gate parity: 8 / failed 0
previous unified expectations: 295 / failed 0
current unified expectations: 303 / failed 0
unified runners: 13
```

Cases:

```text
valid Safety Gate sample
fenced repository example
unknown registry sample
unknown ID/state sample
missing required field sample
satisfied missing basis sample
na missing reason sample
out-of-scope R1 document
```

Semantically invalid samples are expected to pass structural parity because the pilot compares extraction, not validity.

## 7. Current migration state

```text
Safety Gate compatibility view: integrated
Safety Gate structural parity corpus: integrated
Safety Gate checker switch: not performed
Phase 1 adapter: retained
```

Remaining active extraction path:

```text
kdsl_safety_gate.py
→ install_safety_gate(globals())
→ Phase 1 extract_gate_block_legacy / parse_registry_legacy
→ existing semantic validation
```

## 8. Safety and authority boundaries

```text
parity pass != semantic equivalence
parity pass != complete safety proof
parity pass != U approval
parity pass != RT:v
parity pass != execution authority
validator/CI pass != release readiness
```

Retained:

```text
hold/blocked gate削除禁止
state:satisfied requires evidence and authority basis
public/tag/release/assets gate protection
KDSL-DP direct execution prohibition
Packet executable:no
Packet state:not_normalized
stable/public-ready/tag/release/Release Assets操作なし
```

## 9. Known limitations

```text
checker has not switched to CompatibilityView
entry duplicate semantics are not expanded beyond legacy output parity
complete Markdown/context semantics not proven
full natural-language protected-wording reasoning not implemented
cross-document graph proof remains bounded
structural parity != meaning-preservation proof
Packet/Normalization compatibility views pending
```

## 10. Next safe step

Candidate Phase 6C-6:

```text
migrate Safety Gate structural extraction to CompatibilityView
retain in-process Phase 1/AST v2 parity guard
keep registry/state/composition/protected-wording/inheritance semantics unchanged
add active-checker guard cases before merge
```

Stop when:

```text
existing checker exits change
hold/blocked semantics weaken
required evidence/authority conditions change
protected wording or composition requirements change
```

## 11. Closeout decision

```text
Phase 6C-5 Safety Gate compatibility pilot: integrated
Safety Gate checker migration: pending
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
Packet executable: no
public_ready: no
stable_release: none
Release Assets: none
```
