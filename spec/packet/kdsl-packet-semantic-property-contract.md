# KDSL Packet Semantic Property Contract v0.1 Draft

status: v2-draft adopted subordinate
model_id: kdsl-packet-property@0.1-draft
packet_schema: kdsl-packet@0.1-draft
normalization_schema: kdsl-packet-normalization@0.1-draft
canonical: v2-draft subordinate
executable: no
semantic_equivalence: not_proven
execution_authority: none

## 1. Purpose

This contract defines a strict, non-authoritative property surface for checking whether one non-executable Packet and its non-executable Normalization preview retain selected safety, evidence, scope, ordering, exact-string, result, and authority properties.

```text
Packet semantic/property check:=bounded source/preview property evidence
Packet semantic/property check != full semantic equivalence proof
Packet semantic/property check != complete safety proof
Packet semantic/property check != execution authority
Packet semantic/property check != normalization completion
Packet semantic/property check != RT:v
```

Priority:

```text
canonical Core/Profile/R1/Bridge meaning
> Packet/Normalization adopted v2-draft contracts
> this subordinate property contract
> tool/example
```

## 2. Surfaces

```text
packet-semantic:
  source Packet strict bounded semantic checks

strict normalization mapper:
  source Packet→non-executable Normalization artifact

packet-property:
  source Packet×Normalization artifact selected property comparison
```

The existing Packet and Normalization first-slice validators remain valid compatibility surfaces. The strict surface is explicitly selected and does not silently change prior first-slice behavior.

## 3. Packet semantic source requirements

### 3.1 Observation classification

Each `OBS` item uses one explicit prefix:

```text
observed:
inferred:
not_observed:
unverified:
```

Rules:

```text
same payload across different classes→fail
unprefixed OBS→fail in strict surface
inferred→observed扱禁止
unverified→confirmed扱禁止
not_observed→absent/confirmed扱禁止
```

### 3.2 Safety Gate records

Strict Packet records retain:

```text
id
state
scope
reason
evidence
authority
```

Required fields remain the adopted registry minimum:

```text
id/state/scope/reason
```

Strict conditional requirements:

```text
satisfied→evidence必須
SG-DESIGN/SG-AUTHORITY/SG-PUBLIC/SG-DATA satisfied→authority reference必須
blocked→observed evidence必須
na→explicit reason必須
hold×granting authority wording→fail
unknown field/ID/state→fail
```

Registry IDs supplement but do not replace protected wording.

### 3.3 Bounded protected language

The strict source invokes:

```text
model: kdsl-safety-language@0.1-draft
```

Applicable declared concepts must retain strong wording for:

```text
D禁止/design approval
scope/TGT外変更禁止
evidence separation
RT:v non-substitution
NEXT/COMMIT authority separation
rollback preflight
public history/tag/Release Assets protection
data recovery
KDSL-DP直接実行禁止
P1/P1L正規化必須
停止条件
```

```text
bounded semantic pass != full natural-language equivalence
```

### 3.4 FLOW and authority

```text
FLOW opcode/detail != permission
FLOW-READ→read rail必要
FLOW-CHANGE without edit rail→SG-AUTHORITY hold + explicit conditional wording必須
blocked gate×FLOW-CHANGE→fail
FLOW-VERIFY→VERIFY requirements必須
push/release flow×forbid/not_requested rail→fail
```

### 3.5 VERIFY

Packet `VERIFY` remains requirements, not executed evidence.

```text
pass/success/executed/verified claim→fail unless explicitly marked not_run/prohibition/requirement
validator/CI pass != RT:v
```

## 4. Strict normalization mapper

The mapper may produce only:

```text
NORMALIZATION_DRAFT:
STATUS: non-executable
TARGET.executable:false
OUTPUT.executable:false
execution_authority:none
semantic_equivalence:not_proven
```

Allowed preview markers:

```text
KDSL_PROMPT_PREVIEW
a DESIGN_PREVIEW
none
```

Forbidden:

```text
KDSL_PROMPT:
P1:
P1L:
STATUS: executable
```

### 4.1 Exact property selection

The strict mapper records selected exact strings from:

```text
SRC/READ/TGT
OBS
GOAL/NON/STOP/VERIFY
SG id/state/scope/reason/evidence/authority
FLOW op/detail
OUT result schema
AUTHORITY rail values
```

### 4.2 Protected wording

`PRESERVE.protected_wording` retains source prohibitions, stop conditions, Safety Gate reasons, and these fixed boundaries:

```text
TGT外変更禁止
未確認を確認済扱い禁止
未実行verifyをpass扱禁止
build/diff/lint/test/CI pass != RT:v
NEXT実行許可扱禁止
COMMIT自動commit許可扱禁止
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
execution_authority:none
```

### 4.3 Ordered property selection

```text
FLOW opcode order
STOP order
VERIFY requirement order
```

## 5. MAP completeness and mode policy

All 17 Packet fields are accounted exactly once.

Resolved Full KDSL mode policy:

```text
SCHEMA/STATUS/SRC/READ/TGT/OBS/GOAL/NON/STOP/VERIFY/AUTHORITY/NORMALIZE:=exact
BASE/TASK/OUT:=structured
SG/FLOW:=expanded
```

Blocked P1/P1L target:

```text
all MAP modes:=blocked
TARGET.schema:=unresolved
TARGET.resolution:=blocked
OUTPUT.marker:=none
preview:=empty
UNRESOLVED impact:=blocked
```

Canonical P1/P1L schema remains unresolved. No schema is inferred.

## 6. Preview reconstruction properties

For resolved Full KDSL preview, the checker requires:

```text
selected exact source strings represented
SG id/state/scope/reason/evidence/authority represented exactly
FLOW op/detail order represented
STOP order represented
VERIFY requirement order represented
all six authority rails represented exactly
result schema represented
bounded protected concepts preserved
no invented completion/verification claim
```

## 7. Loss and unresolved consistency

```text
resolved target×critical LOSS→fail
resolved target×blocked UNRESOLVED→fail
missing exact/protected/order property→fail
missing/widened authority rail→critical fail
missing Safety Gate state/evidence/wording→critical fail
```

The property checker does not accept a `LOSS:none` self-claim as proof. It independently compares the selected properties.

## 8. Result model

```text
PACKET_PROPERTY_RESULT:
STATUS: property_pass|blocked|fail
MODEL: kdsl-packet-property@0.1-draft
EXECUTABLE: no
SEMANTIC_EQUIVALENCE: not_proven
FULL_SAFETY_PROOF: not_proven
EXECUTION_AUTHORITY: none
```

Meaning:

```text
property_pass:=selected properties matched
blocked:=canonical target schema unresolved and preview prohibited
fail:=source/normalization/property inconsistency detected
```

## 9. Non-proofs

```text
property_pass != full semantic equivalence
property_pass != complete safety proof
property_pass != U承認
property_pass != RT:v
property_pass != execution authority
property_pass != normalization completion
property_pass != release readiness
```

## 10. Packet and execution boundary

```text
KDSL-Packet直接実行禁止
Packet state:not_normalized
PKT:v1使用禁止
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
P1/P1L unresolved→blocked
NEXT実行許可扱禁止
COMMIT自動commit許可扱禁止
```

No result from this contract authorizes direct use by an AI coding tool.

## 11. Current status

```text
contract: v2-draft adopted subordinate
validator: Phase 4 strict first slice integrated
property suite: 42 expectations / failed 0
unified suite: 257 expectations / failed 0
implementation PR: 48 / squash 47b15f9af3496dc36e14673cf0a681e3c333b098
workflow run: 29191890776 / #224 / success
stable/public-ready effect: none
```
