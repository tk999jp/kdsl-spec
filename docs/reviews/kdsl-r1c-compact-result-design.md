# KDSL R1C Compact Result Schema Design Review

status: design-candidate / approval-wait
review_date: 2026-07-11
branch: agent/kdsl-r1c-design
target: main

## 1. Problem

Canonical R1 is safe but can become verbose when AI coding work repeatedly reports files, commands, verification, runtime state, risks, next proposals, and commit state.

The compression problem is not only character count.

```text
圧縮後も検収可能
未実行/未確認を成功扱いしない
RT:v条件維持
NEXT/COMMIT authority分離維持
path/command exactness維持
Full R1へ可逆展開可能
```

## 2. Constraints from canonical R1

The candidate must preserve:

```text
KDSL_RESULT先頭固定
STATUS/PHASE/S/FILES/WHY/CMD/VERIFY/RT/RISK/NEXT/COMMIT
未実行cmd→CMD記載禁止
未実行verify→pass扱禁止
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=actual/proposed, 自動commit許可扱禁止
Evidence separation
Authority separation
```

Source:

```text
spec/r1/r1-result-spec.md
```

## 3. Options considered

### Option A — Full field names + JSON-compatible structured values

Example:

```text
FILES:["a","b"]
VERIFY:{"pass":["lint"],"fail":[],"not_run":["runtime"]}
RT:{"state":"p","basis":"runtime未実行"}
NEXT:{"proposal":"U確認","authority":"proposal_only"}
```

Advantages:

```text
canonical field identity維持
JSON parser利用可能
path/command quoting明確
Full R1へ可逆展開しやすい
既存R1 lintとの対応明確
```

Costs:

```text
key自体の圧縮率は低い
JSON escaping必要
human-only入力では記述負荷あり
```

Decision: selected for v0.1 candidate.

### Option B — Short field aliases

Example:

```text
ST/PH/F/W/C/V/RK/NX/CM
```

Advantages:

```text
文字数削減
```

Risks:

```text
canonical fieldとの対応誤認
NEXT/COMMIT authority境界弱化
alias衝突
validator/migration負荷
R1 report contractとの不一致
```

Decision: rejected for v0.1.

### Option C — New `R1C:` top-level envelope

Advantages:

```text
形式識別が簡単
```

Risks:

```text
KDSL_RESULT先頭固定との衝突
AI coding report contract分岐
Full R1 fallbackが不明瞭
```

Decision: rejected.

### Option D — Required field omission + implicit defaults

Examples:

```text
CMD省略→none
RISK省略→none
NEXT省略→none
```

Advantages:

```text
最大圧縮
```

Risks:

```text
未実行/未確認/なしの混同
missingとnoneの区別消失
round-tripで推測が必要
```

Decision: prohibited.

### Option E — Custom delimiter mini-language

Examples:

```text
RT:v@basis
VERIFY:pass=a|not_run=b
```

Advantages:

```text
短い
```

Risks:

```text
command/path内delimiter衝突
escaping仕様増加
独自parser必須
```

Decision: rejected in favor of JSON-compatible values.

## 4. Selected model

```text
schema_id: kdsl-r1c@0.1-draft
envelope: KDSL_RESULT
field names: canonical R1 names
structured values: JSON-compatible
required fields: all retained
implicit defaults: none
fallback: Full R1
```

R1C is a serialization profile, not a new result semantic layer.

## 5. Compression source

The candidate gains compactness from:

```text
single-line arrays/objects
empty state as [] or null
repeated prose elimination
typed VERIFY/RT/NEXT/COMMIT structure
optional Evidence/Authority only when needed
```

It does not gain compactness by deleting safety-critical fields.

## 6. Required value shapes

```text
FILES: array<string>
CMD: array<string>
VERIFY: {pass:array<string>,fail:array<string>,not_run:array<string>}
RT: {state:p|u|v|na|fail|blk,basis:string}
RISK: array<string>
NEXT: {proposal:string|null,authority:proposal_only}
COMMIT: {actual:string|null,proposed:string|null,permission_basis:string}
```

## 7. Reversibility decision

Round-trip is mandatory.

```text
R1C→Full R1展開時に推測不要
required meaning欠落なし
path/command exact string保持
RT state/basis保持
NEXT proposal_only保持
COMMIT actual/proposed/basis保持
```

If the content cannot satisfy this invariant:

```text
R1C使用禁止
Full R1使用
```

## 8. Status and authority separation

R1C keeps canonical status values.

```text
success|partial|blocked|noop|failed|needs_user
```

Authority boundaries:

```text
NEXT.authority:=proposal_only固定
COMMIT.proposed != commit authority
COMMIT.actual:=実行済のみ
validator pass != execution authority
```

No compact token is allowed to imply commit, push, release, or next-task permission.

## 9. RT decision

`RT` is represented as an object because state-only serialization loses evidence basis.

```text
RT:{"state":"v","basis":"target runtime evidence"}
```

Required:

```text
state + basis
RT:v basis must be runtime evidence
RT:p|u→runtime_unverified risk保持
RT:na→理由保持
```

## 10. Evidence and Authority

`EVIDENCE` and `AUTHORITY` remain optional canonical extensions.

R1C JSON-compatible shapes are defined, but omission is not recommended for high-risk or disputed claims.

```text
optional != removable when required by context
```

## 11. Safety Gate relation

Safety Gate references remain optional extensions.

```text
SG ID-only compression禁止
hold/blocked gate削除禁止
state:satisfied != unrelated authority
```

R1C does not merge the Safety Gate state model into `STATUS` or `RT`.

## 12. Packet boundary

The design intentionally does not satisfy Packet dependencies.

```text
R1C candidate存在 != Packet schema完成
R1C candidate存在 != Packet executable
BASE/TASK/FLOW registry未定義
Packet lint未定義
PKT:v1使用禁止
```

A future Packet may refer to an adopted R1C schema only after separate Packet design and lint.

## 13. Compatibility

```text
classification: compatible v2-draft candidate
canonical R1 change: none
Core change: none
Bridge meaning change: none
KDSL-DP/P1/P1L change: none
existing R1 output validity: unchanged
```

R1C becomes available only when explicitly declared with its exact schema ID after adoption.

## 14. Files in candidate slice

```text
spec/r1/r1c-compact-result-schema.md
spec/lint/kdsl-r1c-lint.md
examples/r1c/README.md
examples/r1c/r1c-success.example.md
examples/r1c/r1c-blocked.example.md
examples/r1c/r1c-needs-user.example.md
docs/reviews/kdsl-r1c-compact-result-design.md
```

No manifest, glossary, Bridge, README, CHANGELOG, or project-status alignment is performed before design approval.

## 15. Validation status

```text
R1C lint specification: candidate
R1C validator: not implemented
existing Validator CI: regression only
existing sample pass != R1C lint pass
```

## 16. Adoption gate

Required after U design approval:

```text
manifestにR1C candidate ownership追加
CP-Packet BridgeへR1C status/boundary同期
glossary-v2-draft同期
README/CHANGELOG/project-status同期
R1C validator first slice
sample runner/CI integration
Full R1 fallback sample
```

The design may be adopted to v2-draft without making it canonical/stable.

## 17. Recommended decision

Adopt the selected model as `kdsl-r1c@0.1-draft`:

```text
KDSL_RESULT envelope retained
canonical field names retained
JSON-compatible structured values
no implicit defaults
no short aliases
round-trip required
Full R1 fallback required
```

## 18. Non-actions

```text
canonical R1変更なし
Packet executable化なし
R1C validator実装なし
tag操作なし
release操作なし
Release Assets操作なし
stable/public-ready化なし
branch deletionなし
```
