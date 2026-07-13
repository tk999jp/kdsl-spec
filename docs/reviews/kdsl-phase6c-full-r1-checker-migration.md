# Phase 6C-12 — Full R1 Checker Structural Migration

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 81
implementation_source_head: 6720fbef02fac201c8e1016f76e546bd119bebaf
implementation_squash_commit: 7a78231eebb8a49b2a49d2d201a1a9e6deabf618
workflow_run_id: 29234998011
workflow_run_number: 329
workflow_conclusion: success

## 1. Goal

Move the structural inputs of the three Full R1 checkers to `FullR1CompatibilityView` without changing required-field, RT evidence, NEXT proposal-only, or COMMIT authority policy.

```text
r1_required_blocks.py
r1_rt_basis.py
r1_authority_guard.py
```

## 2. Integrated changes

Modified:

```text
tools/validator/r1_required_blocks.py
tools/validator/r1_rt_basis.py
tools/validator/r1_authority_guard.py
tools/validator/run_all_samples.py
```

Added:

```text
tools/validator/run_full_r1_migration_samples.py
```

Unchanged:

```text
spec/r1/r1-result-spec.md
tools/validator/kdsl_parser_v2_full_r1_compat.py
tools/validator/kdsl_parser_v2_full_r1_parity.py
```

## 3. Active checker paths

Required blocks:

```text
input
→ FullR1CompatibilityView
→ compare_full_r1_legacy_v2
→ view.present(name)
→ existing required-field decision
```

RT basis:

```text
input
→ FullR1CompatibilityView
→ parity guard
→ view.simple_value(RT/VERIFY/S)
→ view.basis_scope_text
→ existing RT basis rules
```

Authority:

```text
input
→ FullR1CompatibilityView
→ parity guard
→ view.continued_value(NEXT/COMMIT)
→ existing authority-shape rules
```

On parity mismatch, each checker fails before checker-specific semantic validation.

## 4. Whole-document compatibility retained

The previous Full R1 checkers scanned the whole document. Phase 6C-12 preserves that contract.

```text
whole-document field presence: retained
first-field selection: retained
NEXT/COMMIT continuation behavior: retained
bounded-envelope tightening: not introduced
```

This is compatibility preservation, not a canonical declaration that whole-document scanning is the final ideal grammar.

## 5. Semantic and authority rules retained

Required blocks:

```text
KDSL_RESULT
STATUS
PHASE
S
FILES
WHY
CMD
VERIFY
RT
RISK
NEXT
COMMIT
```

RT:

```text
RT:v detection unchanged
accepted runtime basis vocabulary unchanged
invalid basis vocabulary unchanged
mixed accepted/invalid basis warning unchanged
build/diff/lint/test/CI pass != RT:v
```

Authority:

```text
NEXT proposal-only markers unchanged
COMMIT actual/proposed/none shape unchanged
NEXT does not grant execution authority
COMMIT does not grant automatic commit authority
```

Evidence:

```text
未確認→確認済扱禁止
未実行→実行済扱禁止
U観測>AI推測
```

## 6. Verification

```text
implementation PR: 81
source head: 6720fbef02fac201c8e1016f76e546bd119bebaf
squash commit: 7a78231eebb8a49b2a49d2d201a1a9e6deabf618
workflow run: 29234998011 / #329
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
Full R1 structural parity: 8 / failed 0
Full R1 checker migration: 9 / failed 0
unified runners: 20
unified expectations: 353 / failed 0
```

Migration cases:

```text
required fields pass/fail/out-of-scope
RT accepted basis/invalid basis/no basis
NEXT/COMMIT pass/warn/fail
```

## 7. Current migration state

```text
R1C checker: AST v2 + parity guard
Full R1 required/RT/authority checkers: AST v2 + parity guard
CompactPrompt checker: AST v2 + parity guard
Safety Gate checker: AST v2 + parity guard
Packet base checker: AST v2 + parity guard
Packet Normalization checker: AST v2 + parity guard
```

No active checker remains solely on the Phase 1 structural path.

Retained helper exports remain for dependent modules and must not be removed without separate evidence.

## 8. Trust boundary

```text
parity pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
CI pass != release readiness
```

No runtime claim, NEXT execution, commit, tag, stable release, public-ready change, or Release Asset was produced.

## 9. Known limitations

```text
whole-document compatibility remains
helper-consumer migration decision pending
legacy adapter retirement proof incomplete
selected corpus != complete grammar proof
same-marker multi-envelope semantics not generally defined
complete semantic equivalence not proven
```

## 10. Next safe step

Phase 6D candidate:

```text
inventory remaining Phase 1 adapter/helper consumers
separate active checker dependencies from compatibility-only imports
add mutation/property/repository corpus for migrated paths
prove or reject adapter retirement per helper family
```

Recommended order:

```text
consumer inventory
→ direct helper migration candidates
→ mutation/property coverage
→ adapter retirement decision
```

## 11. Closeout decision

```text
Phase 6C-12 Full R1 checker migration: integrated
Phase 6C active checker migrations: complete
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v proof: not granted by parser/CI
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
