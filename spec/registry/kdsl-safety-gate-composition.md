# KDSL Safety Gate Composition Rules v0.1-draft

status: review-candidate
registry: kdsl-sg@0.1-draft
source: spec/registry/kdsl-safety-gate-registry.md

## 1. Purpose

Safety gates are additive controls. A specialized gate does not replace a broader design, evidence, authority, or stop gate.

```text
specialized gate != broader gate解除
single gate satisfied != composite safety satisfied
```

## 2. Baseline composition

AI coding / dev-prompt work baseline:

```text
SG-SCOPE
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
```

Conditional gates are added to this baseline; they do not replace it.

## 3. Required compositions

### rollback / revert / restore / clean / 未push破棄

```text
SG-DESIGN
SG-ROLLBACK
SG-SCOPE
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
```

Reason:

```text
rollback/revertはD禁止trigger
rollback固有の退避/限定Slice/verifyも必要
```

### data migration / data schema / 保存形式 / 不可逆変換

```text
SG-DESIGN
SG-DATA
SG-SCOPE
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
必要時SG-RUNTIME
```

Reason:

```text
schema/保存形式変更は設計変更とdata保護の双方
```

### public history / tag / release / Release Assets

```text
SG-PUBLIC
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
変更方針を含む場合SG-DESIGN
```

Reason:

```text
公開操作保護と操作authorityは別gate
```

### runtime claim / RT:v

```text
SG-EVIDENCE
SG-RUNTIME
```

Operation claimを伴う場合:

```text
+ SG-AUTHORITY
```

### KDSL-DP / ADPS authoring input

```text
SG-KDSL-DP
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
```

Execution contractへ正規化する場合:

```text
P1/P1L正規化必須
```

### unknown source / registry / ID / preflight mismatch

```text
SG-SCOPE
SG-EVIDENCE
SG-STOP
```

Source-of-truth変更を提案する場合:

```text
+ SG-DESIGN
```

### UI contract / public API / implementation policy change

```text
SG-DESIGN
SG-SCOPE
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
必要時SG-RUNTIME
```

## 4. No substitution

```text
SG-ROLLBACK satisfied != SG-DESIGN satisfied
SG-DATA satisfied != SG-DESIGN satisfied
SG-PUBLIC satisfied != SG-AUTHORITY satisfied
SG-RUNTIME satisfied != SG-EVIDENCE全般 satisfied
SG-AUTHORITY satisfied != SG-PUBLIC satisfied
SG-KDSL-DP satisfied扱禁止 != P1/P1L executable
```

## 5. Aggregate state

For a composite operation:

```text
any blocked→operation blocked
no blocked + any hold→operation hold
all applicable satisfied→gate prerequisites satisfied
```

Even when all gate prerequisites are satisfied:

```text
gate prerequisites satisfied != automatic execution permission
```

The exact operation authority and current contract still apply.

`na` handling:

```text
required composition memberをnaにする場合→非該当理由/evidence必須
trigger存在時na禁止
```

## 6. Full KDSL representation

```text
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-DESIGN
      state: hold
      ...
    - id: SG-ROLLBACK
      state: hold
      ...
    - id: SG-AUTHORITY
      state: hold
      ...

Guard:
- rollback/revert/未push破棄含→未承認実装指示禁止
- rollback前→status/diff/退避確認必須
- authority未確認→実行禁止
```

Current rule:

```text
ID + complete protected wording
ID-only compression禁止
```

## 7. Lint minimum

```text
conditional trigger→required composition確認
specialized gateだけでbroader gate欠落→不合格
composite aggregate state計算確認
blocked/hold member欠落→不合格
na bypass→不合格
```

## 8. Packet boundary

```text
composition rules defined != Packet executable
Packet schema/BASE/TASK/FLOW/R1C/lint未定義→直接実行禁止
PKT:v1使用禁止
```
