# Full R1 Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / checkers-migrated-under-parity-guard
compatibility_view: tools/validator/kdsl_parser_v2_full_r1_compat.py
parity_checker: tools/validator/kdsl_parser_v2_full_r1_parity.py
parity_runner: tools/validator/run_parser_v2_full_r1_parity_samples.py
active_checkers:
  - tools/validator/r1_required_blocks.py
  - tools/validator/r1_rt_basis.py
  - tools/validator/r1_authority_guard.py
migration_runner: tools/validator/run_full_r1_migration_samples.py
compatibility_pull_request: 79
compatibility_squash_commit: 191e7315482934fc474022f3a21d02f2457793be
migration_pull_request: 81
migration_squash_commit: 7a78231eebb8a49b2a49d2d201a1a9e6deabf618
migration_workflow: 29234998011 / 329 / success
closeout_pull_request: 82
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Full R1 structural view and use it in the required-block, RT-basis, and authority checkers without changing evidence or authority semantics.

```text
parser parity != Full R1 semantic equivalence
parser parity != RT:v evidence
parser parity != NEXT execution authority
parser parity != COMMIT authority
```

## Active checker pattern

```text
input
→ FullR1CompatibilityView
→ compare_full_r1_legacy_v2
→ mismatch: fail before checker-specific semantic validation
→ match: existing required/RT/authority validation
```

Output markers:

```text
Full R1 parser parity guard: pass
Full R1 structural extraction: AST v2 compatibility view
```

## Whole-document compatibility

The pre-migration Full R1 checkers scan the entire document rather than a bounded `KDSL_RESULT` envelope. Phase 6C preserves:

```text
whole-document KDSL_RESULT presence
whole-document required-field presence
first RT/VERIFY/S values
RT basis-scope construction
first NEXT/COMMIT values
NEXT/COMMIT continuation behavior
```

No silent scope tightening was introduced.

## View model

```text
DocumentNodeV2
FullR1FieldNodeV2
FullR1CompatibilityView
SourceSpanV2
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

## Checker-specific usage

```text
required blocks: view.has_result_envelope / view.present(name)
RT basis: view.simple_value('RT') / view.basis_scope_text
authority: view.continued_value('NEXT') / view.continued_value('COMMIT')
```

Legacy helper functions remain in the checker modules so the parity checker can compare the old contract directly.

## Semantic rules retained

```text
required Full R1 field list
RT:v detection
accepted runtime basis vocabulary
invalid basis vocabulary
mixed-basis warning
NEXT proposal-only marker policy
COMMIT actual/proposed/none policy
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
Full R1 checker migration: 9 / failed 0
unified runners at migration: 20
unified expectations at migration: 353 / failed 0
workflow run: 29234998011 / #329
KDSL Validation: success
Packet Semantic Property: success
```

## Current boundary

```text
CompatibilityView: integrated
three checker switches: integrated
legacy parity guard: active
whole-document compatibility: retained
RT/NEXT/COMMIT semantic/evidence/authority rules: unchanged
```

## Next step

```text
Phase 6D remaining helper-consumer inventory and decision matrix
consumer-specific mutation/property corpus
legacy adapter retirement decision per helper family
```
