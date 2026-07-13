# Full R1 Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / checker-migration-pending
compatibility_view: tools/validator/kdsl_parser_v2_full_r1_compat.py
parity_checker: tools/validator/kdsl_parser_v2_full_r1_parity.py
parity_runner: tools/validator/run_parser_v2_full_r1_parity_samples.py
implementation_pull_request: 79
implementation_squash_commit: 191e7315482934fc474022f3a21d02f2457793be
workflow: 29234411316 / 325 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned view matching the current structural inputs of:

```text
r1_required_blocks.py
r1_rt_basis.py
r1_authority_guard.py
```

```text
parser parity != Full R1 semantic equivalence
parser parity != RT:v evidence
parser parity != NEXT execution authority
parser parity != COMMIT authority
```

## Current checker behavior

The three Full R1 checkers scan the whole document independently. They do not share a bounded `KDSL_RESULT` envelope parser.

The CompatibilityView intentionally preserves:

```text
whole-document KDSL_RESULT presence
whole-document required-field presence
first RT/VERIFY/S values
RT basis-scope construction
first NEXT/COMMIT values
NEXT/COMMIT continuation lines
```

No envelope-scope tightening is introduced by the parity pilot.

## View model

```text
DocumentNodeV2
FullR1FieldNodeV2
FullR1CompatibilityView
SourceSpanV2
```

`FullR1FieldNodeV2` records:

```text
name
simple_value
continued_value
raw_line
span
```

View channels:

```text
has_result_envelope
present(name)
simple_value(name)
continued_value(name)
required_presence
basis_scope_text
authority_values
```

## Compared legacy functions

```text
r1_required_blocks.present
r1_rt_basis.has_result_envelope
r1_rt_basis.find_field
r1_rt_basis.field_scope_text
r1_authority_guard.has_result_envelope
r1_authority_guard.find_field
```

## Semantic rules intentionally excluded

```text
required block validity decision
RT:v detection
accepted runtime basis vocabulary
invalid basis vocabulary
mixed basis warning
NEXT proposal-only marker policy
COMMIT actual/proposed/none policy
execution authority
```

Critical boundaries:

```text
build/diff/lint/test/CI pass != RT:v
RT:v requires target runtime evidence
NEXT:=proposal, not execution authority
COMMIT:=actual or proposed message, not auto-commit authority
未確認/未実行→確認済/実行済扱禁止
```

## Verification

```text
Full R1 structural parity: 8 / failed 0
unified runners: 19
unified expectations: 344 / failed 0
workflow run: 29234411316 / #325
KDSL Validation: success
Packet Semantic Property: success
```

## Current boundary

```text
CompatibilityView: integrated
parity corpus: integrated
three checker switches: pending
whole-document compatibility: retained
semantic/evidence/authority rules: unchanged
```

## Next step

```text
migrate r1_required_blocks.py, r1_rt_basis.py, r1_authority_guard.py
retain compare_full_r1_legacy_v2 guard
preserve RT/NEXT/COMMIT semantics and exits
```
