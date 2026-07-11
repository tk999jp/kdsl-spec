# KDSL Packet BASE Registry v0.1 Draft Candidate

status: design-candidate
canonical: no
registry: kdsl-packet-base
version: 0.1-draft
executable_effect: none

## 1. Purpose

This candidate defines normalization baselines for a future KDSL-Packet.

```text
BASE:=normalization/source-contract classification
BASE != execution permission
BASE != authority
BASE != runtime environment confirmation
```

Priority:

```text
Core/Profile/Bridge canonical meaning > BASE mapping > Packet/example/tool
```

## 2. Current boundary

```text
registry: kdsl-packet-base@0.1-draft
status: design-candidate
adopted: no
stable/public-ready: no
Packet executable effect: none
unknown BASE ID推測禁止
```

## 3. Record model

Each entry defines:

```text
id
purpose
normalization_target
required_sources
required_boundaries
forbidden_inference
```

No entry may grant edit, commit, push, release, destructive-operation, or runtime authority.

## 4. Candidate entries

### BASE-DESIGN-ONLY

Purpose:

```text
Packet schema/registry/lint/example review only
```

Normalization target:

```text
design-only
```

Required sources:

```text
spec/packet/kdsl-packet-schema.md
spec/lint/kdsl-packet-lint.md
relevant registry candidates
```

Required boundaries:

```text
STATUS:non-executable
NORMALIZE.target:design-only
NORMALIZE.state:not_normalized
AI coding tool直接投入禁止
```

Forbidden inference:

```text
design valid-looking→executable扱禁止
review approval→implementation authority扱禁止
```

### BASE-KDSL-DEV

Purpose:

```text
Full KDSL profile:dev-promptへの可逆normalization候補
```

Normalization target:

```text
full-kdsl-dev-prompt
```

Required sources:

```text
spec/core/kdsl-spec.md
spec/core/kdsl-core.md
spec/core/kdsl-modes.md
spec/profiles/kdsl-profile-dev-prompt.md
spec/lint/kdsl-lint-checklist.md
spec/bridge/kdsl-cp-packet-bridge.md
```

Required boundaries:

```text
KDSL_PROMPT先頭固定
D禁止時KDSL_PROMPT出力禁止
complete protected wording保持
KDSL_RESULT報告要求保持
Safety Gate/Authority/STOP保持
```

Forbidden inference:

```text
BASE-KDSL-DEV選択→edit/commit/push許可扱禁止
Packet valid→Full KDSL normalized扱禁止
```

### BASE-ADPS-P1

Purpose:

```text
ADPS authoringからP1/P1Lへ正規化する候補baseline
```

Normalization target:

```text
P1|P1L
```

Required sources:

```text
spec/bridge/kdsl-adps-bridge.md
canonical ADPS/P1/P1L references declared by that bridge
```

Required boundaries:

```text
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
Packet→P1/P1L変換結果の別artifact/evidence必須
```

Forbidden inference:

```text
BASE-ADPS-P1選択→P1/P1L生成済扱禁止
KDSL本体直投入前提の自動継承禁止
```

## 5. Selection rules

```text
BASE exactly one
unknown ID→blocked
multiple BASE IDs→blocked
normalization_target不一致→blocked
required source未取得→未確認/hold
```

BASE selection does not select task class or flow sequence.

## 6. Compatibility

```text
new BASE ID追加→compatible candidate
existing BASE ID意味変更→breaking candidate or new ID required
normalization target変更→breaking
permission意味追加→禁止
```

## 7. Promotion gate

```text
manifest adoption review
Bridge ownership alignment
Packet lint implementation
normalization round-trip tests
unknown-ID tests
Safety Gate/Authority preservation tests
U明示承認
```

## 8. Non-goals

```text
runtime profile選択
OS/toolchain存在保証
repo access保証
execution authority付与
stable preset定義
PKT:v1有効化
```
