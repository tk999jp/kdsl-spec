# KDSL Packet Normalization Contract v0.1 Draft Candidate

status: design-candidate
canonical: no
schema_id: kdsl-packet-normalization@0.1-draft
source_schema: kdsl-packet@0.1-draft
executable: no
semantic_equivalence: not_proven

## 1. Purpose

This candidate defines the evidence contract for expanding an adopted non-executable Packet into a reviewable target preview without granting execution authority.

```text
Packet normalization:=source Packet→mapping evidence+non-executable target preview
Packet normalization != direct execution
Packet normalization != authority grant
Packet normalization != semantic equivalence proof
Packet normalization != RT:v
```

Priority:

```text
meaning/safety/evidence/authority preservation > reversibility > preview completeness > compactness
```

## 2. Current boundary

```text
schema: kdsl-packet-normalization@0.1-draft
status: design-candidate
NORMALIZATION_DRAFT:=non-executable evidence artifact
KDSL_PROMPT direct generation:=out of scope
P1/P1L generation:=blocked until target schema exists
PKT:v1使用禁止
```

The normalization artifact may be inspected, linted, or used as input to a later approved transformer. It must not be passed to an AI coding tool as an implementation contract.

## 3. Ownership relation

```text
Core/Profile/R1/Bridge canonical meaning
> adopted Packet schema/registries/lint
> normalization contract candidate
> normalization lint candidate
> examples/tools
```

Conflict handling:

```text
normalization candidate×canonical source→canonical source優先
unknown target schema/profile/field→blocked
meaning/safety/authority loss→blocked
```

## 4. Required envelope

Required opening:

```text
NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
STATUS: non-executable
```

Required field order:

```text
NORMALIZATION_DRAFT
SCHEMA
STATUS
SOURCE
TARGET
MAP
PRESERVE
UNRESOLVED
LOSS
ROUND_TRIP
AUTHORITY
OUTPUT
```

No implicit defaults are defined.

## 5. Candidate record shape

```yaml
NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
STATUS: non-executable
SOURCE:
  schema: kdsl-packet@0.1-draft
  digest: "sha256:<hex>"
  packet_status: non-executable
  normalize_state: not_normalized
TARGET:
  kind: full-kdsl-dev-prompt
  schema: "format:KDSL/profile:dev-prompt"
  resolution: resolved
  executable: false
MAP:
  entries: []
PRESERVE:
  exact_strings: []
  protected_wording: []
  ordered_fields: []
UNRESOLVED: []
LOSS: []
ROUND_TRIP:
  state: not_tested
  structural_equivalence: not_proven
  semantic_equivalence: not_proven
AUTHORITY:
  source_rails_preserved: false
  execution_authority: none
OUTPUT:
  marker: KDSL_PROMPT_PREVIEW
  executable: false
  preview: ""
```

The example shape is illustrative. Candidate lint/tool implementation is a separate phase.

## 6. SOURCE

`SOURCE` binds the normalization evidence to one exact Packet source.

Required:

```text
schema:=kdsl-packet@0.1-draft
packet_status:=non-executable
normalize_state:=not_normalized
digest:=sha256 of exact source text or declared canonical projection
```

Rules:

```text
source digest missing→blocked
source Packet invalid→blocked
source Packet normalized自己申告→blocked
multiple Packet sources混在→blocked
```

The digest proves source identity only. It does not prove meaning, safety, or authority.

## 7. TARGET

Allowed candidate kinds:

```text
design-only
full-kdsl-dev-prompt
P1
P1L
```

Required fields:

```text
kind
schema
resolution
executable:false
```

Resolution values:

```text
resolved
blocked
```

Rules:

```text
TARGET.executable:=false固定
unknown target→blocked
resolved requires canonical target structure in repository
blocked target→OUTPUT preview禁止
```

### 7.1 design-only

```text
BASE required: BASE-DESIGN-ONLY
schema: design-review
resolution: resolved
OUTPUT.marker: DESIGN_PREVIEW
```

### 7.2 full-kdsl-dev-prompt

```text
BASE required: BASE-KDSL-DEV
schema: format:KDSL/profile:dev-prompt
canonical target: spec/profiles/kdsl-profile-dev-prompt.md
resolution: resolved
OUTPUT.marker: KDSL_PROMPT_PREVIEW
```

`KDSL_PROMPT_PREVIEW` is deliberately not `KDSL_PROMPT:` and is not executable.

### 7.3 P1 / P1L

Current repository state:

```text
BASE required: BASE-ADPS-P1
target schema: unresolved
resolution: blocked
OUTPUT preview: prohibited
```

Reason:

```text
spec/bridge/kdsl-adps-bridge.md defines the normalization boundary
canonical P1/P1L field schema is not present in this repository
unknown target schema推測禁止
```

P1/P1L normalization must remain blocked until a canonical target schema is explicitly supplied and adopted.

## 8. MAP

Each mapping entry records one source-to-target transformation.

Candidate entry:

```yaml
- source: GOAL
  target: 目的
  mode: exact|structured|expanded|blocked
  evidence: "rule/reference"
```

Rules:

```text
all Packet required fields accounted for
mapping omission→LOSS or UNRESOLVEDへ明示
mode exact→text/sequence identity保持
mode structured/expanded→reconstruction rule必須
mode blocked→target preview生成禁止
```

### 8.1 Full KDSL structural mapping

```text
BASE        → header/profile/normalization basis evidence
TASK        → Phase/task classification metadata
SRC         → 前提/正本/共有材
READ        → 前提/作業前確認/読取対象
TGT         → 対象Slice/変更対象
OBS         → 前提/観測
GOAL        → 目的
NON         → 非対象/禁止
SG          → safety gate references + complete protected wording
STOP        → 停止条件
FLOW        → 作業手順
VERIFY      → 検証
OUT         → 報告形式/KDSL_RESULT要求
AUTHORITY   → operation-specific authority/禁止
NORMALIZE   → normalization provenance only; target prompt permissionには変換禁止
```

`SCHEMA` and `STATUS` remain provenance in the normalization artifact and are not silently discarded.

## 9. PRESERVE

Required preservation classes:

```text
exact_strings
protected_wording
ordered_fields
```

### 9.1 exact_strings

Must preserve exactly:

```text
repo/path/file/branch/tag/commit hash
command/URL/package/class/method/property/API
Windows path/file name/extension
```

Any alteration is critical loss.

### 9.2 protected_wording

Must preserve complete applicable wording for:

```text
禁止/必須/未確認/未実行/承認/承認待
rollback/revert/data/public history/tag/Release Assets
D禁止/停止条件/RT:v/NEXT/COMMIT
KDSL-DP直接実行禁止/P1/P1L正規化必須
```

Registry IDs may supplement but never replace this wording.

### 9.3 ordered_fields

Must preserve order for:

```text
FLOW steps
STOP conditions when order is meaningful
VERIFY sequence when prerequisite order exists
```

## 10. UNRESOLVED

`UNRESOLVED` contains source material that cannot yet be mapped without invention.

Candidate entry:

```yaml
- source: "field/path"
  reason: "missing target rule/evidence"
  impact: warning|blocked
```

Rules:

```text
unknown meaning→推測禁止
critical field unresolved→blocked
non-critical render choice unresolved→warning可
unresolved authority/safety/scope/stop/verify/output→blocked
```

## 11. LOSS

Loss classes:

```text
none
render_only
critical
```

Candidate entry:

```yaml
- class: critical
  source: SG
  detail: "protected wording missing"
```

Rules:

```text
critical loss any→STATUS remains non-executable / target resolution blocked
render_only loss→round-trip structural_equivalence not_proven
loss none自己申告→evidence required
```

Critical loss includes:

```text
source/read/target scope
observed/inferred separation
goal/non-goals
Safety Gates/protected wording
STOP/FLOW order
VERIFY requirements
AUTHORITY rails
OUT result schema
exact strings
```

## 12. ROUND_TRIP

Allowed states:

```text
not_tested
structural_pass
loss_detected
blocked
```

Required fields:

```text
state
structural_equivalence
semantic_equivalence:not_proven
```

Structural round-trip model:

```text
Packet source
→ normalization mapping
→ target preview canonical projection
→ reconstructed Packet projection
→ compare required field values/order/exact strings
```

Rules:

```text
structural_pass != semantic equivalence
structural_pass != safety proof
structural_pass != normalization completion
structural_pass != execution authority
semantic_equivalence:not_proven固定 in v0.1 candidate
critical loss/unresolved→state blocked|loss_detected
```

## 13. AUTHORITY

Required:

```text
source_rails_preserved:true|false
execution_authority:none
```

Rules:

```text
execution_authority:none固定
source read/edit/stage/commit/push/release railsを個別保持
allow rail保持 != normalization artifact実行許可
NEXT/COMMIT.proposed != authority
normalizer tool != approver
```

Any missing or widened authority rail is critical loss.

## 14. OUTPUT

Allowed markers:

```text
DESIGN_PREVIEW
KDSL_PROMPT_PREVIEW
none
```

Rules:

```text
OUTPUT.executable:false固定
KDSL_PROMPT: top-level出力禁止
P1:/P1L: top-level出力禁止 while schema unresolved
blocked target→marker:none / preview empty
previewに実行済/確認済/successを発明禁止
```

A later executable transformer must be specified, reviewed, and approved separately.

## 15. Validity conditions

A normalization draft is structurally valid only when:

```text
source Packet identity/validity recorded
TARGET resolution consistent with BASE
all required Packet fields mapped or explicitly unresolved/lost
critical loss absent for resolved target
all exact strings/protected wording/order preserved
all authority rails preserved
ROUND_TRIP state/evidence consistent
OUTPUT remains non-executable
```

Structural validity still does not authorize execution.

## 16. Invalid conditions

```text
STATUS executable相当
TARGET.executable:true
OUTPUT marker KDSL_PROMPT/P1/P1L
P1/P1L resolved without canonical schema
source digest missing
mapping field omission without UNRESOLVED/LOSS
critical loss with resolved target
semantic_equivalence proven/satisfied claim
execution_authority != none
exact string alteration
protected wording/hold/blocked gate deletion
NORMALIZE source state changed to normalized
PKT:v1使用
```

Any invalid condition blocks use of the normalization artifact.

## 17. Promotion gate

Before adopted/tooling/executable promotion:

```text
manifest/Bridge/glossary ownership review
normalization lint implementation
positive/negative sample matrix
Full KDSL structural mapper tests
Packet reconstruction/round-trip tests
exact-string/protected-wording property tests
Authority non-substitution tests
P1/P1L target schema adoption before related mapping
U明示承認
```

## 18. Non-goals

```text
KDSL_PROMPT executable生成
P1/P1L生成
Packet state normalized化
semantic equivalence proof
Safety Gate satisfaction proof
authority付与
runtime/RT:v判定
stable/public-ready化
tag/release/Release Assets操作
```
