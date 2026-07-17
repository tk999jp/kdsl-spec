# KDSL Packet→P1L/P1 Normalization Lint v0.1 Draft

status: v2-draft adopted target-specific lint
applies_to:
  - kdsl-packet-p1-normalization@0.1-draft
canonical_sources:
  - spec/packet/kdsl-packet-p1-normalization-contract.md
  - spec/adps/kdsl-p1l-contract-schema.md
  - spec/adps/kdsl-p1-compact-contract-schema.md

## 1. Boundary

```text
lint/property pass != Packet normalized
lint/property pass != executable
lint/property pass != semantic equivalence
lint/property pass != complete safety proof
lint/property pass != runtime binding
lint/property pass != execution authority
lint/property pass != RT:v
```

## 2. Applicability

Fail when:

```text
BASE.id != BASE-ADPS-P1
NORMALIZE.target not in P1|P1L
source Packet semantic checker fails
source Packet STATUS != non-executable
source Packet NORMALIZE.state != not_normalized
```

## 3. TARGET / OUTPUT

P1L required:

```text
TARGET.schema: kdsl-p1l@0.1-draft
TARGET.resolution: resolved
TARGET.executable: false
OUTPUT.marker: P1L_PREVIEW
OUTPUT.executable: false
```

P1 required:

```text
TARGET.schema: kdsl-p1@0.1-draft
TARGET.resolution: resolved
TARGET.executable: false
OUTPUT.marker: P1_PREVIEW
OUTPUT.executable: false
```

Fail when canonical-looking execution marker is exposed:

```text
P1L:
P1|
KDSL_PROMPT:
```

```text
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
```

## 4. MAP

Every Packet field must be accounted for exactly once:

```text
SCHEMA/STATUS/BASE/TASK/SRC/READ/TGT/OBS/GOAL/NON/SG/STOP/FLOW/VERIFY/OUT/AUTHORITY/NORMALIZE
```

Fail when:

```text
source missing/duplicated/unknown
mapping target differs from target-specific contract
mapping mode differs from exact/structured/expanded policy
MAP evidence empty
AUTHORITY expansion evidence omits explicit forbid safety floor
blocked MAP entry with resolved target
```

## 5. Observation / task projection

Fail when:

```text
observed/inferred/unverified classification changes
unlabelled OBS promoted to observed
TASK registry mapping differs from contract
TASK mapping treated as authority/completion
```

## 6. Preservation

Required exact comparison:

```text
PRESERVE.exact_strings
PRESERVE.protected_wording
PRESERVE.ordered_fields
```

Fail on repo/path/file/branch/tag/commit/URL/command/package/class/method/property/API or Windows path changes.

Fail when applicable protected wording is missing or weakened:

```text
TGT外変更禁止
未確認を確認済扱い禁止
未実行verifyをpass扱禁止
build/diff/lint/test/CI pass != RT:v
NEXT実行許可扱禁止
COMMIT自動commit許可扱禁止
KDSL-DP直接実行禁止
P1/P1L正規化必須
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
execution_authority:none
```

## 7. Authority

Source rails copied exactly:

```text
read/edit/stage/commit/push/release
```

Additional canonical rails fixed:

```text
public_repo: forbid
destructive_ops: forbid
```

Fail when:

```text
any source rail missing/widened
public_repo/destructive_ops != forbid
MAP evidence hides the additional rails
normalization AUTHORITY.source_rails_preserved != true
normalization AUTHORITY.execution_authority != none
```

## 8. Runtime / Binding

Required target projection:

```text
RUNTIME.disposition: pending
BINDING.runtime_control: unresolved
BINDING.state: unbound
BINDING.executable: false
```

Fail when:

```text
RT:v/fail/blk result claim appears
Binding becomes bound/executable
property pass is used as runtime-control evidence
```

## 9. Unresolved / Loss / Round-trip

Resolved target requires:

```text
UNRESOLVED: []
LOSS: []
ROUND_TRIP.state: structural_pass
ROUND_TRIP.structural_equivalence: pass
ROUND_TRIP.semantic_equivalence: not_proven
```

Fail when:

```text
blocked unresolved item exists
critical/render loss exists without target blocking
semantic equivalence proven claim
structural_pass does not reconstruct canonical P1L projection
P1 target does not reconstruct P1L exactly
```

## 10. Preview payload

P1L:

```text
PROJECTION_JSON parses
P1L schema validator first slice passes
projection equals mapper-derived expected model
```

P1:

```text
SERIALIZATION_JSON decodes to string
canonical P1 parser passes
P1 reconstructs mapper-derived P1L model
```

Fail when preview payload differs from expected model, even if the outer normalization structure remains valid.

## 11. Validator boundary

```text
validator未実行→pass扱禁止
validator pass != canonical semantic conformance proof
validator pass != safety proof
validator pass != runtime binding
validator pass != authority
validator pass != Packet normalized
validator pass != RT:v
validator pass != release readiness
```
