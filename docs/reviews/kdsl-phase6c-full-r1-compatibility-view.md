# Phase 6C-11 — Full R1 Compatibility View Pilot

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 79
implementation_source_head: 1b2cd34bf6623c660f062207fb06ebaa96d2c2b8
implementation_squash_commit: 191e7315482934fc474022f3a21d02f2457793be
workflow_run_id: 29234411316
workflow_run_number: 325
workflow_conclusion: success

## 1. Goal

Add a source-spanned compatibility view matching the structural inputs consumed by the three current Full R1 checkers before any checker switch.

```text
r1_required_blocks.py
r1_rt_basis.py
r1_authority_guard.py
```

```text
structural parity first
whole-document scan compatibility retained
RT/NEXT/COMMIT semantics unchanged
```

## 2. Integrated files

Added:

```text
tools/validator/kdsl_parser_v2_full_r1_compat.py
tools/validator/kdsl_parser_v2_full_r1_parity.py
tools/validator/run_parser_v2_full_r1_parity_samples.py
```

Updated:

```text
tools/validator/run_all_samples.py
```

Unchanged:

```text
tools/validator/r1_required_blocks.py
tools/validator/r1_rt_basis.py
tools/validator/r1_authority_guard.py
spec/r1/r1-result-spec.md
```

## 3. Current Full R1 structural contract

The existing Full R1 checkers do not use a shared bounded-envelope parser. They scan the entire document for first matching fields.

The CompatibilityView intentionally reproduces:

```text
KDSL_RESULT presence anywhere in the document
required field presence anywhere in the document
first RT/VERIFY/S scalar values
RT basis-scope concatenation
first NEXT/COMMIT values
NEXT/COMMIT continuation-line behavior
```

It does not silently narrow the scan to the first `KDSL_RESULT` envelope.

## 4. Source-spanned view

```text
DocumentNodeV2
FullR1FieldNodeV2
SourceSpanV2
FullR1CompatibilityView
```

Each first field records:

```text
name
simple value
continued value
raw line
source span
```

The view exposes:

```text
has_result_envelope
present(name)
simple_value(name)
continued_value(name)
required_presence
basis_scope_text
authority_values
```

## 5. Compared checker inputs

Required blocks:

```text
r1_required_blocks.present(text, name)
```

RT basis:

```text
r1_rt_basis.has_result_envelope
r1_rt_basis.find_field for RT/VERIFY/S
r1_rt_basis.field_scope_text
```

Authority:

```text
r1_authority_guard.has_result_envelope
r1_authority_guard.find_field for NEXT/COMMIT
```

## 6. Semantic and authority boundary retained

The view does not decide:

```text
whether required fields are semantically valid
whether RT is v
whether runtime basis is accepted
whether invalid basis wording conflicts
whether NEXT is proposal-only
whether COMMIT is actual/proposed separated
execution authority
RT:v status
```

Critical invariants:

```text
build/diff/lint/test/CI pass != RT:v
RT:v requires target runtime evidence
NEXT:=proposal, not execution authority
COMMIT:=actual commit or proposed message, not auto-commit permission
未確認/未実行→確認済/実行済扱禁止
```

## 7. Verification

```text
source head: 1b2cd34bf6623c660f062207fb06ebaa96d2c2b8
workflow run: 29234411316 / #325
KDSL Validation: success
Packet Semantic Property: success
Full R1 structural parity: 8 / failed 0
unified runners: 19
unified expectations: 344 / failed 0
```

Cases:

```text
valid Full R1
missing required block
RT:v accepted basis
RT:v invalid basis
NEXT/COMMIT valid shape
NEXT warning shape
COMMIT failure shape
out-of-scope Packet input
```

Semantically invalid samples pass structural parity when extraction is equal. This is not semantic acceptance.

## 8. Current migration state

```text
Full R1 CompatibilityView: integrated
Full R1 parity corpus: integrated
three Full R1 checker switches: not performed
```

Current checker path:

```text
raw text
→ checker-local line scanning
→ checker-specific semantic validation
```

## 9. Trust boundary

```text
parity pass != semantic equivalence
parity pass != complete safety proof
parity pass != U approval
parity pass != RT:v
parity pass != execution authority
CI pass != release readiness
```

No runtime claim, NEXT execution, commit, tag, release, public-ready change, or Release Asset was produced.

## 10. Known limitations

```text
whole-document scan remains intentionally compatible
bounded-envelope Full R1 semantics not introduced
checker switches pending
selected corpus != complete language proof
helper-consumer migration decision pending
legacy adapter retirement evidence incomplete
```

## 11. Next safe step

Candidate Phase 6C-12:

```text
migrate the three Full R1 checker structural inputs to FullR1CompatibilityView
retain compare_full_r1_legacy_v2 guard in each checker
keep required/RT/NEXT/COMMIT semantic rules unchanged
add active-checker migration corpus
```

Stop when:

```text
existing checker exits change
whole-document compatibility changes without specification approval
RT accepted/invalid basis rules change
NEXT proposal-only boundary changes
COMMIT authority boundary changes
unknown default/schema inference is required
```

## 12. Closeout decision

```text
Phase 6C-11 Full R1 compatibility pilot: integrated
Full R1 checker migration: pending
Issue #55: remain open
semantic equivalence: not_proven
RT:v proof: not_proven by parser parity
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
