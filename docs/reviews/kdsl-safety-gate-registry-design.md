# KDSL Safety Gate Registry Design Review

status: approved / integrated-on-branch
review_date: 2026-07-11
approval_date: 2026-07-11
branch: agent/kdsl-safety-gate-registry
target: main
pull_request: 4

## 1. Problem

KDSL Core, dev-prompt, R1, Lint, and Bridge already define safety concepts, but future R1C and Packet designs need stable references without duplicating or weakening their meaning.

Initial gap:

```text
SG:=not canonical
Packet SG registry:=undefined
unknown SG推測禁止
```

Approved response:

```text
kdsl-sg@0.1-draft:=v2-draft Registry
Core/R1/Bridge safety meaning remains authoritative
KDSL-Packet remains draft-non-executable
```

## 2. Design goal

```text
existing safety meaningを保持
stable candidate IDを付与
state/inheritance/conflict rulesを定義
R1C/Packetが後続で参照可能な形にする
IDだけでprotected wordingを削除させない
```

## 3. Approved registry

```text
registry: kdsl-sg
version: 0.1-draft
states: hold|satisfied|blocked|na
```

Approved IDs:

```text
SG-DESIGN
SG-SCOPE
SG-EVIDENCE
SG-RUNTIME
SG-AUTHORITY
SG-ROLLBACK
SG-PUBLIC
SG-DATA
SG-KDSL-DP
SG-STOP
```

## 4. Key decisions

### 4.1 Semantic IDs over numeric IDs

Adopted:

```text
SG-RUNTIME
SG-AUTHORITY
```

Rejected alternative:

```text
SG01
SG02
```

Reason:

```text
human reviewability
misreference risk reduction
future Packet debug visibility
```

### 4.2 Four states

Adopted:

```text
hold
satisfied
blocked
na
```

Rejected:

```text
waived
ignored
disabled
```

Reason:

```text
waived/ignored/disabledはsafety bypassへ誤用されやすい
approvalとfactual verificationを混同しやすい
```

### 4.3 IDs do not replace wording in current Full KDSL

Adopted:

```text
ID + full critical wording
```

Rejected:

```text
ID only
```

Reason:

```text
current LLM direct-input reliability
registry resolution failure時の意味消失防止
protected words保持
```

### 4.4 Typed non-substitution

Adopted:

```text
U承認 != RT:v evidence
RT:v != commit/push/release authority
CI/validator pass != semantic equivalence
NEXT/COMMIT proposal != authority
```

Reason:

```text
single pass/approval signalによる複数gate解除を防ぐ
```

### 4.5 Additive composition

Adopted:

```text
specialized gate != broader gate解除
single gate satisfied != composite safety satisfied
```

Representative composition:

```text
rollback/revert/未push破棄
→ SG-DESIGN/SG-ROLLBACK/SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP
```

### 4.6 Packet remains non-executable

Adopted:

```text
SG registry adoption alone does not enable Packet
```

Remaining undefined:

```text
Packet schema
BASE registry
TASK registry
FLOW registry
R1C schema
Packet lint
```

## 5. Compatibility

Classification:

```text
candidate change: compatible v2-draft addition
existing Core/R1/Bridge semantics: unchanged
existing KDSL_PROMPT syntax: unchanged
existing KDSL_RESULT syntax: unchanged
```

Potential breaking conditions prohibited:

```text
IDで保護語を置換
state:satisfiedをauthority扱
existing D禁止/RT:v/NEXT/COMMIT意味変更
Packet executable化
```

## 6. Source alignment

```text
SG-DESIGN    → Core D禁止 / dev-prompt D禁止
SG-SCOPE     → dev-prompt minimal Slice / preflight / lint
SG-EVIDENCE  → R1 Evidence separation
SG-RUNTIME   → R1 RT
SG-AUTHORITY → R1 Authority separation
SG-ROLLBACK  → dev-prompt Rollback
SG-PUBLIC    → Core protected terms / glossary public history
SG-DATA      → Modes high-risk / Core D禁止
SG-KDSL-DP   → Core/ADPS bridge
SG-STOP      → Core unknown handling / Lint / CP-Packet bridge
```

## 7. Registry files

```text
spec/registry/README.md
spec/registry/kdsl-safety-gate-registry.md
spec/registry/kdsl-safety-gate-composition.md
spec/lint/kdsl-safety-gate-registry-lint.md
examples/safety-gates/dev-prompt-safety-gates.example.md
docs/reviews/kdsl-safety-gate-registry-design.md
docs/reviews/kdsl-safety-gate-registry-integration.md
```

## 8. Alignment applied after approval

```text
spec/manifest.md
spec/bridge/kdsl-cp-packet-bridge.md
spec/glossary-v2-draft.md
spec/registry/README.md
README.md
CHANGELOG.md
docs/project-status.md
```

Approval basis:

```text
U: OKです。進めてください
```

Packet boundary retained:

```text
KDSL-Packet:=draft-non-executable
PKT:v1使用禁止
unknown BASE/TASK/FLOW/R1C推測禁止
```

## 9. Validation plan and result

Existing sample CI:

```text
GitHub Actions sample runner
expected: total 23 / failed 0
```

Previous candidate runs:

```text
run 5: success
run 6: success
```

Final aligned head requires a fresh successful CI run before merge.

No Safety Gate validator implementation is included in this Phase.

## 10. Non-actions

```text
Core meaning changeなし
R1 meaning changeなし
KDSL-DP/P1/P1L boundary changeなし
Packet schema adoptionなし
R1C schema adoptionなし
tag/release/Release Assets操作なし
stable/public-ready化なし
```

## 11. Merge gate

```text
ID/state/composition review: approved
manifest/bridge/glossary alignment: complete
README/CHANGELOG/status alignment: complete
protected wording replacement: prohibited
Packet non-executable boundary: retained
latest Validator CI: success required
merge method: squash
post-merge status closeout: required
```
