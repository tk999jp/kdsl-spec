# KDSL Packet Normalization Lint v0.1 Draft Candidate

status: design-candidate
canonical: no
validator: not implemented
scope: kdsl-packet-normalization@0.1-draft

## 1. Purpose

This candidate defines structural and safety checks for non-executable Packet normalization evidence.

```text
lint pass != semantic equivalence
lint pass != normalization completion
lint pass != executable target
lint pass != authority
lint pass != safety proof
lint pass != RT:v
```

## 2. Detection

In scope when:

```text
NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
```

Out of scope:

```text
PACKET_DRAFT
KDSL_PROMPT
KDSL-DP
P1/P1L
KDSL_RESULT/R1C
```

Mixed top-level envelopes are errors unless a canonical bridge explicitly permits them.

## 3. Required envelope checks

Errors:

```text
NORMALIZATION_DRAFT not first significant line
SCHEMA missing/unknown
STATUS missing or != non-executable
KDSL_PROMPT/P1/P1L top-level marker present
TARGET.executable != false
AUTHORITY.execution_authority != none
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

Missing, duplicate, or reordered fields are errors in v0.1 candidate.

## 4. SOURCE checks

Required:

```text
schema: kdsl-packet@0.1-draft
digest: sha256:<64 hex>
packet_status: non-executable
normalize_state: not_normalized
```

Errors:

```text
unknown source schema
missing/malformed digest
packet_status executable-like
normalize_state normalized-like
multiple source identities
```

The checker must not treat digest presence as semantic proof.

## 5. TARGET checks

Known kinds:

```text
design-only
full-kdsl-dev-prompt
P1
P1L
```

Known resolution:

```text
resolved
blocked
```

Required mapping:

```text
design-only + BASE-DESIGN-ONLY → resolved / design-review
full-kdsl-dev-prompt + BASE-KDSL-DEV → resolved / format:KDSL/profile:dev-prompt
P1|P1L + BASE-ADPS-P1 → blocked / target schema unresolved
```

Errors:

```text
TARGET.executable:true
P1/P1L resolution:resolved
P1/P1L preview present
unknown target kind/schema/resolution
BASE/target mismatch
```

## 6. MAP checks

Every Packet required field must be accounted for:

```text
SCHEMA
STATUS
BASE
TASK
SRC
READ
TGT
OBS
GOAL
NON
SG
STOP
FLOW
VERIFY
OUT
AUTHORITY
NORMALIZE
```

Known mapping modes:

```text
exact
structured
expanded
blocked
```

Errors:

```text
required source field absent from MAP/UNRESOLVED/LOSS accounting
unknown mapping mode
exact mode without identity evidence
structured/expanded mode without reconstruction rule/evidence
blocked mode with TARGET.resolution:resolved
mapping to permission/execution state
```

## 7. Full KDSL mapping checks

For target `full-kdsl-dev-prompt`, minimum targets:

```text
GOAL→目的
TGT→対象Slice/変更対象
NON→非対象/禁止
SG→safety gate/protected wording
STOP→停止条件
FLOW→作業手順
VERIFY→検証
OUT→報告形式
AUTHORITY→authority/禁止
```

Errors:

```text
required minimum mapping absent
SG mapping uses ID-only substitution
AUTHORITY mapping widens any rail
NORMALIZE mapped to execution permission
KDSL_PROMPT top-level generated
```

Warnings:

```text
TASK mapping lacks Phase/task metadata
SRC/READ/OBS mapping merged without observed/inferred distinction
```

## 8. PRESERVE checks

Required blocks:

```text
exact_strings
protected_wording
ordered_fields
```

Errors:

```text
missing preservation class
known path/command/API/hash absent after mapping
protected wording represented only by Registry ID
FLOW order changed
STOP/VERIFY prerequisite order changed
```

Exact-string comparison must be byte/text exact after declared newline normalization only.

## 9. UNRESOLVED checks

Each entry requires:

```text
source
reason
impact: warning|blocked
```

Errors:

```text
unknown source omitted rather than listed
critical source marked warning
authority/safety/scope/stop/verify/output unresolved but target resolved
reason empty
```

## 10. LOSS checks

Known classes:

```text
none
render_only
critical
```

Errors:

```text
critical loss + TARGET.resolution:resolved
loss none without evidence
loss entry missing source/detail
exact string/protected wording/authority loss classified render_only
```

Warnings:

```text
render_only loss + structural_equivalence claimed pass without basis
```

## 11. ROUND_TRIP checks

Known state:

```text
not_tested
structural_pass
loss_detected
blocked
```

Required:

```text
structural_equivalence: not_proven|pass|failed
semantic_equivalence: not_proven
```

Errors:

```text
semantic_equivalence != not_proven
structural_pass with critical loss/unresolved blocked item
structural_pass without source/target projection evidence
loss_detected with LOSS empty
blocked with TARGET resolved and no blocking reason
```

Rules:

```text
structural_pass != semantic equivalence
structural_pass != safety proof
structural_pass != execution authority
```

## 12. AUTHORITY checks

Required:

```text
source_rails_preserved:true|false
execution_authority:none
```

Errors:

```text
execution_authority != none
source rail absent/widened
read→edit expansion
edit→stage/commit/push expansion
commit→push/release expansion
NEXT/COMMIT.proposed treated as permission
```

`source_rails_preserved:false` requires critical LOSS and blocked target.

## 13. OUTPUT checks

Known marker:

```text
DESIGN_PREVIEW
KDSL_PROMPT_PREVIEW
none
```

Required:

```text
executable:false
```

Errors:

```text
marker KDSL_PROMPT/P1/P1L
executable true
blocked target with non-empty preview
P1/P1L target with preview
preview claims executed/verified/success without source evidence
```

## 14. Protected boundary checks

Errors:

```text
D禁止削除/弱化
rollback/revert/data/public-history protection loss
未確認/未実行→確認済/実行済変換
build/diff/lint/test/CI pass→RT:v変換
NEXT→execution authority
COMMIT.proposed→commit authority
KDSL-DP直接実行
P1/P1L schema推測
PKT:v1使用
```

## 15. Validator boundary

Current state:

```text
normalization validator: not implemented
normalization transformer: not implemented
round-trip property tests: not implemented
lint pass claim: prohibited until implementation/execution evidence
```

Future validator success will still not prove:

```text
semantic equivalence
complete protected wording preservation
Safety Gate completeness
normalization completion
execution authority
RT:v
release readiness
```

## 16. Promotion checks

Before adoption/tooling/executable generation:

```text
manifest/Bridge/glossary ownership review
positive/negative normalization sample matrix
source digest tests
Full KDSL mapping tests
reconstruction/round-trip tests
exact-string/protected-wording property tests
Authority non-substitution tests
P1/P1L target schema adoption before mapping
U明示承認
```
