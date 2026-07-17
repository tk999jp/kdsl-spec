# KDSL Packet to P1L/P1 Normalization Contract v0.1 Draft

status: v2-draft adopted target-specific first slice
canonical: subordinate to Packet normalization contract
schema_id: kdsl-packet-p1-normalization@0.1-draft
source_schema: kdsl-packet@0.1-draft
target_schemas:
  - kdsl-p1l@0.1-draft
  - kdsl-p1@0.1-draft
executable: no
semantic_equivalence: not_proven

## 1. Purpose

This target-specific contract resolves the canonical P1L/P1 target structure for `BASE-ADPS-P1` while preserving the Packet normalization artifact as non-executable evidence.

```text
Packet source
→ dedicated Packet→P1L model mapping
→ P1L structural validation
→ optional P1 serialization and P1L reconstruction
→ P1L_PREVIEW or P1_PREVIEW
```

```text
preview != executable contract
TARGET.resolution:resolved != Packet normalized
structural_pass != semantic equivalence/safety proof/runtime binding/authority
```

## 2. Ownership and applicability

```text
Core/Profile/R1/Bridge meaning
> P1L/P1 canonical schema
> generic Packet normalization contract
> this target-specific P1L/P1 mapping contract
> target-specific lint/property checker
> example/tool
```

This contract applies only when:

```text
BASE.id: BASE-ADPS-P1
NORMALIZE.target: P1|P1L
Packet semantic checker: pass
mapper: tools/validator/kdsl_packet_normalize_p1.py
property checker: tools/validator/kdsl_packet_p1_property.py
```

For this exact path, this contract supersedes the earlier generic `P1/P1L target schema unresolved` statement. It does not alter design-only or Full KDSL targets.

Without the dedicated mapper/property evidence, P1/P1L normalization remains blocked.

## 3. Required target record

P1L:

```yaml
TARGET:
  kind: P1L
  schema: kdsl-p1l@0.1-draft
  resolution: resolved
  executable: false
OUTPUT:
  marker: P1L_PREVIEW
  executable: false
```

P1:

```yaml
TARGET:
  kind: P1
  schema: kdsl-p1@0.1-draft
  resolution: resolved
  executable: false
OUTPUT:
  marker: P1_PREVIEW
  executable: false
```

Mandatory boundary:

```text
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
preview content must not expose an executable-looking canonical top-level marker
```

## 4. Mapping

All Packet source fields remain accounted for:

```text
SCHEMA/STATUS→SOURCE provenance
BASE→SOURCE.kind/PROFILE/BINDING boundary
TASK→TASK.kind/TASK.declared
SRC→SOURCE.references/SCOPE.source
READ→SCOPE.read
TGT→SCOPE.target
OBS→CONTEXT.observed/inferred/unverified
GOAL→GOAL.expected
NON→SCOPE.non_target/GUARD constraints/protected wording
SG→GUARD.safety_gates/protected wording
STOP→STOP/protected wording
FLOW→PLAN.steps
VERIFY→VERIFY.requirements/RUNTIME.required_evidence
OUT→OUTPUT result schema/report requirements
AUTHORITY→P1L AUTHORITY
NORMALIZE→NORMALIZATION/BINDING provenance
```

Mapping modes:

```text
exact: SCHEMA/STATUS/SRC/READ/TGT/GOAL/NON/STOP/VERIFY
structured: BASE/TASK/OUT/AUTHORITY/NORMALIZE
expanded: OBS/SG/FLOW
```

Any missing source accounting, blocked mapping entry, critical unresolved item, or critical loss blocks resolution.

## 5. Observation classification

```text
observed:<value>→CONTEXT.observed
inferred:<value>→CONTEXT.inferred
unverified:<value>→CONTEXT.unverified
unlabelled value→CONTEXT.unverified
```

Unlabelled or inferred values must never be promoted to observed facts.

## 6. Task mapping

```text
TASK-INSPECT→investigate
TASK-PLAN→plan
TASK-CHANGE→implement
TASK-VERIFY→review
TASK-CLOSEOUT→closeout
TASK-PUBLIC→other
TASK-DATA→other
```

This mapping is work classification only. It does not grant authority or mark work complete.

## 7. Authority mapping

Packet v0.1 source rails:

```text
read/edit/stage/commit/push/release
```

These six rails must be copied exactly.

Canonical P1L additional rails:

```text
public_repo: forbid
destructive_ops: forbid
```

This is an explicit non-widening safety floor, not implicit permission or profile inference. The MAP evidence must record the expansion.

```text
source rail widening→fail
public_repo/destructive_ops != forbid→fail
AUTHORITY.execution_authority:none固定
```

## 8. Runtime and binding

```text
RUNTIME.disposition: pending
BINDING.runtime_control: unresolved
BINDING.state: unbound
BINDING.executable: false
```

Packet VERIFY entries mentioning runtime/RT:v/実機/target environment may be copied to `RUNTIME.required_evidence`.

```text
pending != RT:v
Packet/P1L/P1 property pass != runtime binding
runtime binding is out of scope
```

## 9. Normalization evidence

Resolved first-slice output requires:

```text
UNRESOLVED: []
LOSS: []
ROUND_TRIP.state: structural_pass
ROUND_TRIP.structural_equivalence: pass
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.source_rails_preserved: true
AUTHORITY.execution_authority: none
OUTPUT.executable: false
```

The Packet source remains:

```text
SOURCE.packet_status: non-executable
SOURCE.normalize_state: not_normalized
```

`structural_pass` means only that the target projection can be validated and reconstructed without first-slice structural loss.

## 10. Preview payload

P1L preview:

```text
P1L_PREVIEW:
SCHEMA: kdsl-p1l@0.1-draft
STATUS: non-executable-preview
PROJECTION_JSON: <canonical P1L JSON projection>
```

P1 preview:

```text
P1_PREVIEW:
SCHEMA: kdsl-p1@0.1-draft
STATUS: non-executable-preview
SERIALIZATION_JSON: <JSON string containing canonical P1 serialization>
```

The JSON wrapper prevents the preview from appearing as an executable top-level P1 contract.

## 11. Property requirements

The dedicated property checker must verify:

```text
source Packet semantic pass
source digest identity
all Packet fields mapped exactly once
mapping mode/target policy
exact strings/protected wording/order
P1L model schema validity
P1 serialization reconstruction when requested
six source authority rails exact
additional authority rails explicitly forbid
Binding non-executable
preview marker separation
semantic equivalence remains not_proven
```

## 12. Invalid conditions

```text
wrong BASE or NORMALIZE target
TARGET.executable:true
canonical P1L:/P1| marker exposed as preview top level
source authority widening
public_repo/destructive_ops permission
missing Authority rail
BINDING bound/executable
semantic_equivalence proven claim
Packet source normalized self-claim
missing source field mapping
critical loss/unresolved item with resolved target
```

Any invalid condition blocks target-specific normalization use.

## 13. Non-goals

```text
Packet normalized state promotion
P1L/P1 runtime binding
K1/PF1 adoption
executable transformer
AI coding tool direct execution
complete semantic equivalence proof
complete safety proof
stable/public-ready/tag/release/Release Assets operation
```
