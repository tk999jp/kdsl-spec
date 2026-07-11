# KDSL R1C Lint v0.1 Draft Candidate

status: review-candidate
canonical: no
schema: kdsl-r1c@0.1-draft
source_candidate: spec/r1/r1c-compact-result-schema.md
base_canonical: spec/r1/r1-result-spec.md

## 1. Purpose

Validate that an R1C compact serialization remains a reversible view of canonical R1.

```text
R1C lint:=構造/型/必須field/RT/NEXT/COMMIT境界検査
R1C lint != semantic equivalence proof
R1C lint != safety proof
R1C lint != U承認
R1C lint != RT:v
R1C lint != execution authority
```

## 2. Detection

R1C is detected only when both markers exist:

```text
KDSL_RESULT:
SCHEMA:kdsl-r1c@0.1-draft
```

Rules:

```text
KDSL_RESULTなし→R1C扱禁止
SCHEMAなし→R1C扱禁止
unknown SCHEMA→fail
R1C推測禁止
```

A normal Full R1 result without `SCHEMA` is outside this lint target.

## 3. Required top-level order

Required order:

```text
KDSL_RESULT
SCHEMA
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

Fail:

```text
required key欠落
required key重複
required key順序違反
KDSL_RESULT前自然文
unknown compact alias使用
```

Unknown aliases include:

```text
ST
PH
F
W
C
V
RK
NX
CM
```

This list is representative. No R1C field alias is defined in v0.1 candidate.

## 4. Scalar lint

### STATUS

Allowed:

```text
success|partial|blocked|noop|failed|needs_user
```

Fail:

```text
unknown STATUS
empty STATUS
STATUSの独自短縮値
```

### PHASE / S / WHY

Fail:

```text
empty value
null
meaning required but placeholder only
```

Placeholder-only examples:

```text
TBD
unknown
-
```

`unknown` may be valid inside an explanatory sentence, but not as the complete value.

## 5. JSON-compatible structured lint

The following values must parse as JSON-compatible arrays/objects:

```text
FILES: array<string>
CMD: array<string>
VERIFY: object
RT: object
RISK: array<string>
NEXT: object
COMMIT: object
```

Fail:

```text
invalid JSON
wrong top-level type
non-string array member
implicit unquoted path/command
unknown required subkey
```

Commands, paths, tags, hashes, URLs, API names, and file names must remain exact strings.

## 6. FILES lint

```text
FILES must be array<string>
[] allowed
```

Fail:

```text
null
scalar path
empty-string member
duplicate path without reason
inspected-only file represented as changed file
```

The last condition may require human review and can be WARN in heuristic tooling.

## 7. CMD lint

```text
CMD must be array<string>
[] means no command executed
```

Fail:

```text
null
recommendation/proposed command混入
未実行cmdをexecuted commandとして記載
empty-string member
```

Heuristic indicators for proposed commands:

```text
should run
run next
recommended
推奨
次に実行
```

A heuristic hit is WARN unless execution evidence is clearly absent and the command is asserted as executed.

## 8. VERIFY lint

Required exact subkeys:

```text
pass
fail
not_run
```

Each value:

```text
array<string>
```

Fail:

```text
subkey欠落
unknown subkey
same verification in pass and not_run
same verification in pass and fail
未実行verifyをpassへ記載
```

WARN:

```text
pass itemが結果/根拠を含まない
fail itemがfailure内容を含まない
not_run itemが対象を特定しない
```

## 9. RT lint

Required exact subkeys:

```text
state
basis
```

Allowed state:

```text
p|u|v|na|fail|blk
```

Fail:

```text
state欠落
basis欠落/空
unknown state
RT:v basisがbuild/diff/lint/test/CIのみ
RT:na理由なし
RT:p|uなのにruntime未確認riskがRISKにない
```

Representative invalid `RT:v` basis:

```text
build pass
CI success
lint pass
diff clean
unit tests pass
```

Representative valid `RT:v` basis requires target-environment runtime evidence, U observation, shared runtime log, or explicit runtime verification result.

## 10. RISK lint

```text
RISK must be array<string>
[] allowed
```

Rules:

```text
RT:p|u→runtime_unverified相当必須
VERIFY.not_runにcritical verifyあり→対応risk推奨
blocked/partial/failed→empty RISKはWARN
```

An empty array does not prove absence of risk.

## 11. NEXT lint

Required exact subkeys:

```text
proposal
authority
```

Allowed:

```text
proposal: string|null
authority: proposal_only
```

Fail:

```text
authority != proposal_only
NEXTをexecution permissionとして表現
proposal field欠落
unknown subkey
```

Protected boundary:

```text
NEXT:=提案
NEXT実行許可扱禁止
```

## 12. COMMIT lint

Required exact subkeys:

```text
actual
proposed
permission_basis
```

Allowed:

```text
actual: string|null
proposed: string|null
permission_basis: string
```

Fail:

```text
required subkey欠落
permission_basis空
actual/proposed両方が同一値
proposedを実行済扱い
COMMITをautomatic commit permissionとして表現
```

WARN:

```text
actualあり + commit hash/message不明瞭
actualあり + permission_basis=none
proposedあり + permission_basisをcommit許可として読める表現
```

Protected boundary:

```text
COMMIT:=実行済commitまたは推奨message
COMMIT自動commit許可扱禁止
```

## 13. Optional EVIDENCE lint

When present, required exact subkeys:

```text
observed
inferred
not_observed
unverified
```

Each value:

```text
array<string>
```

Fail:

```text
observed/inferred混同
not_observedをconfirmed扱い
unverifiedをRT:v basis扱い
same item in observed and unverified
```

## 14. Optional AUTHORITY lint

When present, allowed keys:

```text
read
edit
stage
commit
push
release
```

Allowed values:

```text
allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
```

Fail:

```text
unknown authority key/value
AUTHORITY.commit=propose_only + actual commit asserted without separate basis
AUTHORITY.push=forbid + push asserted
AUTHORITY.release=forbid + tag/release/assets asserted
```

## 15. Optional SAFETY_GATES lint

When present, delegate to the adopted Safety Gate validator/lint.

```text
registry: kdsl-sg@0.1-draft
```

Fail:

```text
unknown SG ID/state
hold/blocked削除
SG ID-only compression
state:satisfiedによるunrelated authority推定
```

## 16. Round-trip lint

The R1C view must expand to Full R1 without implicit defaults.

Fail:

```text
required information reconstructed only by guess
empty array meaning ambiguous
null meaning ambiguous
unknown subkey ignored
path/command normalization required
STATUS/RT/NEXT/COMMIT meaning changed
```

Fallback rule:

```text
round-trip不成立→R1C fail→Full R1使用
```

## 17. Packet boundary lint

```text
R1C lint pass != Packet executable
R1C schema candidate != Packet schema
R1C schema candidate != BASE/TASK/FLOW registry
R1C schema candidate != Packet lint
PKT:v1使用禁止
```

Any claim that this candidate completes Packet dependencies is fail.

## 18. Severity

```text
ERROR:
  required field/type/schema failure
  RT:v basis violation
  NEXT/COMMIT authority violation
  round-trip loss
  Packet execution claim

WARN:
  weak evidence wording
  duplicate/ambiguous entries
  high-risk optional Evidence omission
  partial/blocked/failed with empty RISK

INFO:
  Full R1 document outside R1C target
  optional readability improvements
```

## 19. Validator status

```text
R1C lint specification: review-candidate
R1C validator implementation: not implemented
validator未実装→pass扱禁止
existing CI pass != R1C lint pass
```

## 20. Required adoption checks

Before v2-draft adoption:

```text
U design approval
manifest/bridge/glossary/status alignment
success/blocked/needs_user examples
R1C validator first slice
sample runner integration
Full R1 fallback verification
Packet non-executable boundary confirmation
```
