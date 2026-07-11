# KDSL Safety Gate Registry Design Review

status: design-review-candidate
review_date: 2026-07-11
branch: agent/kdsl-safety-gate-registry
target: main

## 1. Problem

KDSL Core, dev-prompt, R1, Lint, and Bridge already define safety concepts, but future R1C and Packet designs need stable references without duplicating or weakening their meaning.

Current gap:

```text
SG:=not canonical
Packet SG registry:=undefined
unknown SG推測禁止
```

## 2. Design goal

```text
existing safety meaningを保持
stable candidate IDを付与
state/inheritance/conflict rulesを定義
R1C/Packetが後続で参照可能な形にする
IDだけでprotected wordingを削除させない
```

## 3. Proposed registry

```text
registry: kdsl-sg
version: 0.1-draft
states: hold|satisfied|blocked|na
```

Candidate IDs:

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

Adopt candidate:

```text
SG-RUNTIME
SG-AUTHORITY
```

Rejected initial alternative:

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

Adopt:

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

Adopt:

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

Adopt:

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

### 4.5 Packet remains non-executable

Adopt:

```text
SG registry candidate alone does not enable Packet
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
candidate change: compatible draft addition
existing Core/R1/Bridge semantics: unchanged
existing KDSL_PROMPT syntax: unchanged
existing KDSL_RESULT syntax: unchanged
```

Potential breaking conditions to avoid:

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

## 7. Files in this candidate slice

```text
spec/registry/README.md
spec/registry/kdsl-safety-gate-registry.md
spec/lint/kdsl-safety-gate-registry-lint.md
examples/safety-gates/dev-prompt-safety-gates.example.md
docs/reviews/kdsl-safety-gate-registry-design.md
```

## 8. Deliberately deferred alignment

The following files are not changed in the first candidate slice:

```text
spec/manifest.md
spec/bridge/kdsl-cp-packet-bridge.md
spec/glossary-v2-draft.md
README.md
CHANGELOG.md
docs/project-status.md
```

Reason:

```text
first review ID/state model independently
avoid declaring registry canonical before U review
avoid temporarily implying Packet executability
```

After design approval, alignment must be applied in one integration slice.

## 9. Required integration slice after approval

```text
manifestにRegistry layer/ownership追加
CP-Packet bridgeのSG未定義表記をdraft-definedへ更新
v2 glossaryのSG status更新
README navigation/status更新
CHANGELOG記録
project-statusにworkstream/merge evidence記録
```

Packet boundary must remain:

```text
KDSL-Packet:=draft-non-executable
PKT:v1使用禁止
unknown BASE/TASK/FLOW/R1C推測禁止
```

## 10. Validation plan

```text
GitHub Actions sample runner: total 23 / failed 0
manual cross-file review
known ID/state lint review
protected wording review
Packet non-executable boundary review
```

No validator implementation is included in this Phase.

## 11. Non-actions

```text
Core meaning changeなし
R1 meaning changeなし
KDSL-DP/P1/P1L boundary changeなし
Packet schema adoptionなし
R1C schema adoptionなし
tag/release/Release Assets操作なし
stable/public-ready化なし
```

## 12. Review gate

Before moving from candidate to adopted v2-draft registry:

```text
ID set review
state model review
inheritance/conflict review
non-substitution review
manifest/bridge/glossary alignment review
U明示承認
```
