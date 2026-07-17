# KDSL P1/P1L Lint v0.1 Draft

status: v2-draft adopted
applies_to:
  - kdsl-p1l@0.1-draft
  - kdsl-p1@0.1-draft
canonical_sources:
  - spec/adps/kdsl-p1l-contract-schema.md
  - spec/adps/kdsl-p1-compact-contract-schema.md

## 1. Boundary

```text
lint pass != executable
lint pass != semantic equivalence
lint pass != complete safety proof
lint pass != runtime binding
lint pass != execution authority
lint pass != U approval
lint pass != RT:v
```

Unknown schema/profile/alias/preset meaning must not be inferred.

## 2. P1L envelope

Fail when:

```text
opening marker != P1L:
SCHEMA != kdsl-p1l@0.1-draft
STATUS != contract-candidate
required field missing/repeated/out of order
implicit default used
undeclared top-level field used
```

Required order:

```text
META/SOURCE/PROFILE/TASK/SCOPE/CONTEXT/GOAL/PLAN/GUARD/STOP/VERIFY/RUNTIME/OUTPUT/AUTHORITY/NORMALIZATION/BINDING
```

## 3. Source and profile identity

Fail when:

```text
SOURCE.digest missing or malformed
source identity is invented
PROFILE.completion:profile_completed without exact id/revision/digest
PROFILE.completed_fields missing for completed values
completed value remains hidden instead of expanded
PROFILE.completion:explicit with required hidden defaults
unknown profile/alias/preset completed by similarity/memory/convention
```

Warn when the source identity exists but the underlying referenced content is unavailable for independent verification.

## 4. Task, scope, and context

Fail when:

```text
unknown task alias silently mapped
read scope treated as edit scope
edit/stage/commit authority with empty SCOPE.target
operation exceeds SCOPE.target
non_target is weakened/deleted
repo/path/file/branch/tag/commit/URL/command/package/class/method/property/API exact string changes
observed/inferred/unverified classes are merged
inferred promoted to observed
unverified treated as absent/confirmed
```

## 5. Guard and Stop

Fail when applicable protected wording is omitted or weakened:

```text
禁止/必須/未確認/未実行/承認/承認待
rollback/revert/data protection
public履歴/公開済tag/Release Assets
D禁止/停止条件
KDSL-DP直接実行禁止/P1/P1L正規化必須
RT:v/NEXT/COMMIT authority boundaries
```

Fail when:

```text
Safety Gate ID/preset replaces complete protected wording
hold/blocked gate is removed
Stop activation is ignored
plan/flow is treated as permission
```

## 6. Verify and Runtime

Fail when:

```text
VERIFY requirement is reported as executed evidence
not_run/unavailable/user_required reported as pass
build/diff/lint/test/CI pass treated as RT:v
RUNTIME.disposition outside pending|user_required|not_applicable
pre-execution contract claims RT:v|RT:fail|RT:blk|verified|success
```

`RT:v` remains valid only in R1/R1C after target-environment runtime evidence.

## 7. Output

Fail when:

```text
result schema request treated as result success
NEXT treated as next-task authority
COMMIT treated as commit authority
a required R1/R1C boundary is weakened
```

## 8. Authority

All required rails:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

Fail when:

```text
any rail missing/implicit
not_requested interpreted as allow
propose_only interpreted as operation authority
read allow implies edit
edit allow implies stage/commit
commit allow implies push
push allow implies release
public_repo allow implies history rewrite
allow_once lacks exact target/scope where required
destructive_ops enabled without exact approved scope
```

## 9. Normalization and Binding

Fail when:

```text
NORMALIZATION.state outside explicit|profile_completed|lossy|blocked
critical unresolved/loss with state other than blocked
lossy contract BINDING.state=bound
semantic_equivalence != not_proven
round_trip state inconsistent with loss/unresolved
BINDING.executable != false
schema/lint/round-trip pass changes BINDING state
unresolved K1/PF1 is invented
```

## 10. P1 serialization

Required segment order:

```text
SCHEMA/STATUS/M/SRC/PF/T/S/C/G/P/GD/X/V/RT/O/A/N/BD
```

Fail when:

```text
opening marker != P1
SCHEMA != kdsl-p1@0.1-draft
STATUS != contract-candidate
segment missing/repeated/out of order
unknown segment key
value is not canonical compact JSON
JSON object key order differs from P1L canonical order
implicit field omission/default
pipe inside JSON string is split as a segment
exact Unicode value changes after parse/render
P1 cannot reconstruct every P1L required field/subfield
```

## 11. P1↔P1L round-trip

Compare:

```text
field presence/order
source/profile identity
scope/non-target
observed/inferred/unverified classification
goal/questions
plan order
Guard/protected wording
Stop/Verify/Runtime/Output
all Authority rails
Normalization/Binding
exact strings
```

Fail when any critical class differs.

```text
structural_pass != semantic equivalence
structural_pass != complete safety proof
structural_pass != execution authority
structural_pass != runtime binding
```

## 12. Legacy operational P1

Legacy colon forms are not canonical P1.

Fail canonical promotion when:

```text
loss=L meaning required
AP/H meaning required
profile revision/digest absent
alias/preset definition absent
Authority rails absent without exact permission contract
legacy form self-declares kdsl-p1@0.1-draft without reconstruction
```

`loss=P` may map to `profile_completed` only with exact compatibility evidence and expanded completed fields.

## 13. Mandatory blocked cases

```text
unknown schema/profile/alias/preset
critical source/scope/guard/stop/verify/runtime/output/authority uncertainty
missing exact profile evidence
missing Authority rail
edit authority with empty target
critical exact-string loss
runtime result claim in P1/P1L
BINDING.executable:true
KDSL-DP direct execution
```

## 14. Validator boundary

```text
validator未実行→pass扱禁止
validator pass != canonical semantic conformance proof
validator pass != authority
validator pass != RT:v
validator pass != release readiness
```
