# KDSL Packet Normalization Contract Design Review

status: design-candidate
review_date: 2026-07-11
branch: agent/kdsl-packet-normalization-design
target: main
canonical_effect: none
execution_effect: none

## 1. Scope

```text
spec/packet/kdsl-packet-normalization-contract.md
spec/lint/kdsl-packet-normalization-lint.md
spec/packet/README.md
examples/packet/normalization-source.example.md
examples/packet/normalization-p1-source.example.md
examples/packet/normalization-full-kdsl.example.md
examples/packet/normalization-p1-blocked.example.md
examples/packet/normalization-lossy-blocked.example.md
examples/packet/README.md
```

## 2. Selected model

```text
schema: kdsl-packet-normalization@0.1-draft
top-level: NORMALIZATION_DRAFT
status: design-candidate / non-executable
source: kdsl-packet@0.1-draft
target preview: design-only|full-kdsl-dev-prompt
P1/P1L: blocked until canonical target schema exists
semantic_equivalence: not_proven
execution_authority: none
```

## 3. Why a separate normalization artifact

Rejected direct transformation:

```text
PACKET_DRAFT→KDSL_PROMPT direct output
```

Reason:

```text
Packet valid != normalized
normalization mapping/loss/evidence would be hidden
KDSL_PROMPT top-level is an executable contract surface
Safety Gate/Authority loss could be overlooked
```

Selected sequence:

```text
PACKET_DRAFT
→ NORMALIZATION_DRAFT mapping/loss/round-trip evidence
→ separate future approval/tooling phase
→ executable target only after explicit promotion
```

## 4. Full KDSL target decision

Full KDSL mapping is structurally designable because the target profile exists:

```text
spec/profiles/kdsl-profile-dev-prompt.md
```

The candidate permits only:

```text
KDSL_PROMPT_PREVIEW
OUTPUT.executable:false
```

It does not produce `KDSL_PROMPT:`.

## 5. P1/P1L decision

Current repository evidence:

```text
spec/bridge/kdsl-adps-bridge.md defines KDSL-DP→P1/P1L boundary
canonical P1/P1L field schema is absent
```

Decision:

```text
P1/P1L target resolution:=blocked
schema inference:=prohibited
preview generation:=prohibited
source authority rails remain evidence only
```

This is stricter than treating Bridge labels as a complete target schema.

## 6. Round-trip definition

Selected proof class:

```text
structural round-trip only
semantic equivalence remains not_proven
```

Structural comparison covers:

```text
required Packet fields
scope/read/target values
observation/inference distinction
goal/non-goals
Safety Gate wording and state
STOP/FLOW/VERIFY order
AUTHORITY rails
OUT schema
exact strings
```

A structural pass is not execution permission or a safety proof.

## 7. Loss policy

```text
critical loss→target blocked
unresolved authority/safety/scope/stop/verify/output→blocked
render-only loss→structural equivalence not proven until reconstruction test
```

Critical loss cannot be downgraded to warning merely to produce a preview.

## 8. Source identity

Dedicated exact UTF-8 sources:

```text
examples/packet/normalization-source.example.md
sha256:b464944da1a3e080b08166e0b0eaa13327c4daa8974c3c56f6a22428dd81daed

examples/packet/normalization-p1-source.example.md
sha256:b37951d0a8c30afef865a64f0e29566136b6c2dace51810c9ef328a6615df9f1
```

Digest identity does not prove semantics.

## 9. Self-consistency corrections

During review:

```text
P1 example gained an exact source/digest
P1 source authority rails changed to preserved:true
critical-loss example linked to the actual Full KDSL source digest
AUTHORITY loss is explicitly critical and unresolved
```

These corrections keep examples compliant with the candidate lint rules.

## 10. Rejected alternatives

### `KDSL_PROMPT:` inside normalization output

Rejected because it creates a copyable executable surface before approval.

### P1/P1L schema inferred from names

Rejected because unknown schema/preset inference is prohibited.

### `semantic_equivalence: pass`

Rejected because the current repository has no semantic proof system.

### Registry-only safety preservation

Rejected because SG ID-only compression is prohibited.

### Authority inherited as target permission

Rejected because a normalizer is not an executor or approver.

## 11. Compatibility classification

```text
new normalization contract candidate: compatible experimental addition
canonical Packet/Bridge/R1 meaning change: none
Packet execution change: none
normalization state change: none
stable/public-ready change: none
```

## 12. Split-phase plan

```text
P1: design candidate integration
P2: manifest/Bridge/glossary ownership adoption review
P3: normalization validator + structural mapper first slice
P4: round-trip/property tests
P5: executable target promotion review only after explicit approval
```

The transformer and adoption are separated so a design document cannot self-authorize execution.

## 13. Merge gate

```text
existing Validator CI regression: total 69 / failed 0
source digests independently fixed
P1/P1L blocked boundary reviewed
example self-consistency reviewed
no workflow changes
no validator/tool implementation
squash merge
post-merge design closeout
```

## 14. Non-actions

```text
KDSL_PROMPT executable生成なし
P1/P1L生成なし
Packet normalized化なし
semantic equivalence claimなし
authority付与なし
tag/release/Release Assets操作なし
stable/public-ready化なし
source branch削除なし
```
