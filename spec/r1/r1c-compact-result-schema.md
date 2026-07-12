# R1C Compact Result Schema v0.1 Draft

status: v2-draft adopted
canonical: v2-draft subordinate
schema_id: kdsl-r1c@0.1-draft
base_canonical: spec/r1/r1-result-spec.md

## 1. Purpose

R1C is a compact serialization profile for canonical R1 / `KDSL_RESULT`.

```text
R1C:=canonical R1 meaningを保持したcompact serialization profile
R1C != 新しい結果意味
R1C != 新しいexecution authority
R1C != Packet execution contract
```

The first candidate keeps the canonical `KDSL_RESULT:` envelope and all required R1 field names. It compresses structured values with JSON-compatible arrays/objects and removes repetitive prose without removing required state.

Priority:

```text
意味保持 > Evidence保持 > RT条件保持 > Authority分離 > 可逆性 > 圧縮率
```

## 2. Source-of-truth relation

```text
canonical R1:
  spec/r1/r1-result-spec.md

v2-draft serialization:
  spec/r1/r1c-compact-result-schema.md

Phase 3 subordinate optional-block contract:
  spec/r1/r1c-optional-block-contract.md
```

Conflict rule:

```text
canonical R1 > R1C v2-draft serialization profile
```

R1C must not redefine `STATUS`, `RT`, `NEXT`, `COMMIT`, Evidence, or Authority semantics.

## 3. Envelope

R1C does not introduce an `R1C:` top-level envelope.

Required opening:

```text
KDSL_RESULT:
SCHEMA: kdsl-r1c@0.1-draft
```

Required field order:

```text
KDSL_RESULT:
SCHEMA:
STATUS:
PHASE:
S:
FILES:
WHY:
CMD:
VERIFY:
RT:
RISK:
NEXT:
COMMIT:
```

Rules:

```text
KDSL_RESULT先頭固定
SCHEMA:=kdsl-r1c@0.1-draft固定
11 canonical required fields保持
required field省略禁止
unknown R1C schema推測禁止
invalid R1C→Full R1へfallback
```

Optional canonical blocks may follow `COMMIT`:

```text
EVIDENCE
AUTHORITY
ANNUNCIATOR
SAFETY_GATES
```

Optional blocks retain their canonical names. No alias is defined in this candidate.

Phase 3 deep optional validation and round-trip rules are defined in `spec/r1/r1c-optional-block-contract.md`.

## 4. No-alias rule

The first candidate intentionally does not define short field aliases.

```text
STATUS→ST 禁止
PHASE→PH 禁止
FILES→F 禁止
WHY→W 禁止
CMD→C 禁止
VERIFY→V 禁止
RISK→RK 禁止
NEXT短縮禁止
COMMIT短縮禁止
```

Reason:

```text
field identityの明示
既存R1 lintとの対応
誤展開防止
NEXT/COMMIT authority境界保持
```

Short aliases may be reconsidered only as a separate version with independent lint and migration rules.

## 5. Value encoding

### 5.1 Scalar fields

The following remain scalar KDSL values:

```text
STATUS
PHASE
S
WHY
```

`STATUS` values remain canonical:

```text
success|partial|blocked|noop|failed|needs_user
```

Empty or unknown scalar values are prohibited.

### 5.2 Structured fields

The following use JSON-compatible values:

```text
FILES: JSON array<string>
CMD: JSON array<string>
VERIFY: JSON object
RT: JSON object
RISK: JSON array<string>
NEXT: JSON object
COMMIT: JSON object
```

JSON-compatible means:

```text
double-quoted strings
[] arrays
{} objects
null explicit absence
standard JSON escaping
```

Commands, paths, hashes, API names, and file names must be preserved exactly inside strings.

## 6. Field schema

### 6.1 FILES

```text
FILES:["path/a","path/b"]
```

Rules:

```text
changed files only
no changed files→[]
inspected-only files混入禁止
path短縮/変換禁止
```

Inspected files may be recorded in optional Evidence or a later schema extension. They are not mixed into `FILES`.

### 6.2 CMD

```text
CMD:["python tools/validator/run_samples.py"]
```

Rules:

```text
実行したcommandのみ
未実行cmd記載禁止
no command executed→[]
command文字列変換禁止
```

### 6.3 VERIFY

Required shape:

```json
{"pass":[],"fail":[],"not_run":[]}
```

Example:

```text
VERIFY:{"pass":["git diff --check","sample runner total 34 / failed 0"],"fail":[],"not_run":["target runtime"]}
```

Rules:

```text
pass/fail/not_run全key必須
未実行verify→pass混入禁止
not_runをpass扱禁止
empty class→[]
```

### 6.4 RT

Required shape:

```json
{"state":"p|u|v|na|fail|blk","basis":"non-empty string"}
```

Examples:

```text
RT:{"state":"v","basis":"U実機観測: target Windows UI confirmed"}
RT:{"state":"na","basis":"docs/spec design only; runtime対象なし"}
RT:{"state":"p","basis":"runtime未実行"}
```

Rules:

```text
state/basis必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI passだけをbasisにすること禁止
RT:p|u→RISKにruntime_unverified相当保持
RT:na→非該当理由必須
```

### 6.5 RISK

```text
RISK:["runtime_unverified","full parserなし"]
```

Rules:

```text
no known risk→[]
未確認risk削除禁止
runtime未確認→対応risk保持
```

An empty array means no risk was recorded. It does not prove that no risk exists.

### 6.6 NEXT

Required shape:

```json
{"proposal":null,"authority":"proposal_only"}
```

or:

```text
NEXT:{"proposal":"R1C validator first slice","authority":"proposal_only"}
```

Rules:

```text
proposal/authority必須
authority:=proposal_only固定
proposal may be null
NEXT:=提案
NEXT実行許可扱禁止
```

R1C does not encode permission to execute the next task.

### 6.7 COMMIT

Required shape:

```json
{"actual":null,"proposed":null,"permission_basis":"none"}
```

Example:

```text
COMMIT:{"actual":"05773b4 Validator: add Safety Gate Registry first heuristic lint","proposed":null,"permission_basis":"U承認"}
```

Rules:

```text
actual/proposed/permission_basis全key必須
actual:=実行済commitのみ
proposed:=推奨messageのみ
proposed != commit authority
COMMIT != 自動commit許可
permission_basis未確認→none
```

## 7. Optional Evidence encoding

Optional `EVIDENCE` may use this JSON-compatible shape:

```json
{
  "observed":[],
  "inferred":[],
  "not_observed":[],
  "unverified":[]
}
```

Rules remain canonical:

```text
observed != inferred
not_observed != confirmed
unverified != RT:v basis
inferred→observed扱禁止
```

For high-risk or disputed claims, omission of `EVIDENCE` is not recommended.

## 8. Optional Authority encoding

Optional `AUTHORITY` may use this JSON-compatible shape:

```json
{
  "read":"allow",
  "edit":"target_only",
  "stage":"not_requested",
  "commit":"propose_only",
  "push":"forbid",
  "release":"forbid"
}
```

Allowed values remain canonical:

```text
allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
```

R1C serialization does not grant authority.

## 9. Safety Gate relation

If `SAFETY_GATES` is included, it uses the adopted registry structure.

```text
registry: kdsl-sg@0.1-draft
```

Rules:

```text
SG ID-only compression禁止
hold/blocked gate削除禁止
state:satisfied != unrelated authority
validator pass != safety proof
```

R1C must not compress complete critical safety wording into an SG ID alone.

## 10. Round-trip invariant

A valid R1C result must expand to canonical Full R1 without inventing or losing required meaning.

Required preservation:

```text
STATUS exact
PHASE exact
S meaning
FILES exact strings/order
WHY meaning
CMD exact strings/order
VERIFY class and evidence
RT state and basis
RISK entries
NEXT proposal + proposal_only boundary
COMMIT actual/proposed/permission_basis
optional Evidence separation
optional Authority separation
```

Invalid conditions:

```text
required field omitted
unknown schema
unknown field alias
structured JSON invalid
unknown required subkey
implicit default needed for expansion
RT:v basis insufficient
NEXT authority != proposal_only
COMMIT permission inferred
command/path altered
```

When round-trip cannot be guaranteed:

```text
R1C使用禁止
Full R1出力
```

## 11. Compact example

```text
KDSL_RESULT:
SCHEMA:kdsl-r1c@0.1-draft
STATUS:success
PHASE:Safety Gate validator first slice
S:validator/CI/docs closeout complete
FILES:["tools/validator/kdsl_safety_gate.py","docs/project-status.md"]
WHY:known SG ID/state/field/composition欠落をheuristic検出するため
CMD:[]
VERIFY:{"pass":["Validator CI total 34 / failed 0"],"fail":[],"not_run":["local Windows rerun"]}
RT:{"state":"na","basis":"validator/spec/docs変更; target application runtime対象なし"}
RISK:["heuristic parser","semantic equivalence proofなし"]
NEXT:{"proposal":"R1C compact schema design","authority":"proposal_only"}
COMMIT:{"actual":"05773b4 Validator: add Safety Gate Registry first heuristic lint","proposed":null,"permission_basis":"U承認"}
```

## 12. Full R1 fallback example

Use Full R1 instead of R1C when:

```text
複雑なEvidenceをcompact valueで安全に表現できない
複数Phaseの結果を1blockへ無理に圧縮する
path/command quotingが曖昧
RT basisが長く分岐する
Authority railが複雑
human reviewでcompact representationが不明瞭
```

## 13. Packet boundary

```text
R1C candidate存在 != Packet schema完成
R1C candidate存在 != Packet executable
R1C candidate存在 != BASE/TASK/FLOW registry完成
R1C candidate存在 != Packet lint完成
KDSL-Packet:=draft-non-executable
PKT:v1使用禁止
```

A future Packet may reference an adopted R1C schema only after Packet dependencies and lint are separately defined.

## 14. Current status

```text
schema: kdsl-r1c@0.1-draft
status: v2-draft adopted
canonical: v2-draft subordinate to spec/r1/r1-result-spec.md
validator: first heuristic slice integrated
deep_optional_validator: Phase 3 first slice integrated
structural_round_trip: Phase 3 optional-block first slice integrated
optional_evidence_authority_round_trip: structural_pass first slice
optional_safety_gates_round_trip: structural_pass first slice
annunciator_round_trip: structural-only first slice
semantic_equivalence: not_proven
main integration: yes
stable/public-ready effect: none
```

No tag, release, Release Assets, or stable/public-ready operation is authorized by this candidate.
