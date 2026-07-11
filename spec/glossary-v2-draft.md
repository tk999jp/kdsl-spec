# KDSL v2 Draft Glossary

status: v2-draft
canonical: no
source_alignment: docs/design/kdsl-v2-direction.md / spec/manifest.md

This file supplements `spec/glossary.md` for v2-draft terms. It does not replace the v1.1 glossary.

## Architecture axes

### profile

```text
profile:=用途別運用仕様
```

Examples:

```text
compact-prompt
dev-prompt
converter
lint
```

### mode

```text
mode:=圧縮強度
```

Canonical values remain:

```text
readable|min|dense|lock
```

### safety

```text
safety:=安全保持強度
```

Canonical values remain:

```text
normal|lock-critical|lock-all
```

### lexicon

```text
lexicon:=profile内で使用する宣言済み語彙/alias集合
```

Constraints:

```text
lexicon != mode
lexicon != profile
unknown lexicon推測禁止
lexiconで保護語上書禁止
```

### envelope

```text
envelope:=prompt/resultを包む入出力契約形式
```

Draft values:

```text
plain
packet-draft
result
```

## CompactPrompt terms

### KDSL-CP

```text
KDSL-CP:=profile:compact-promptの短縮名
```

Use:

```text
一般LLM
Project files
単体prompt
```

Non-use:

```text
AI coding tool実装契約
repo操作
runtime verification
release/tag/Release Assets操作
```

### KDSL-CP漢

```text
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1 の宣言済み短縮構成
```

It is not a new mode.

### kanji-v1

```text
kanji-v1:=KDSL-CP向け漢字構造alias lexicon
```

Structural keys:

```text
役/目/材/出/則/守/調/確
```

Constraints:

```text
構造aliasはKEY位置のみ
free-text一字aliasは原則禁止
禁/不/実/要は標準free-text aliasではない
```

### Guard

```text
Guard:=禁止/未確認扱い/safety gateを記述するblock
```

### Check

```text
Check:=出力直前のself-lint block
```

Check is not a chain-of-thought disclosure request.

### CP-Lift

```text
CP-Lift:=KDSL-CPの適用範囲を超えたpromptをFull KDSL dev-promptへ昇格する境界処理
```

Triggers include implementation, repository operations, runtime verification, rollback/revert, public history, tags, Release Assets, data migration, and source-of-truth changes.

## Safety Gate Registry terms

### Registry

```text
Registry:=既存正本意味を参照するID/state/composition集合
```

Constraints:

```text
Registry != 新しい実行権限
Registry ID != permission
Registry state != execution authority
Registry reference != protected wording削除許可
unknown registry/ID推測禁止
```

### kdsl-sg@0.1-draft

```text
kdsl-sg@0.1-draft:=KDSL v2-draft Safety Gate Registry
```

Source:

```text
spec/registry/kdsl-safety-gate-registry.md
```

Status:

```text
v2-draft adopted
stable/public-ready: no
Safety Gate validator: not implemented
```

Priority:

```text
Core/R1/Bridge safety meaning > Registry mapping > Profile usage > Example/Tool
```

### SG

```text
SG:=Safety Gate Registry entry/reference
```

Current IDs:

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

No one-character SG aliases are defined.

### SG state

Allowed states:

```text
hold
satisfied
blocked
na
```

Definitions:

```text
hold:=gate適用中, 前提/evidence/承認未充足, 関連操作禁止
satisfied:=必要根拠と必要authorityがexact scope内で充足
blocked:=違反/衝突/停止条件発火, 作業停止
na:=非該当を理由付きで確認済み
```

Constraints:

```text
state省略→hold
unknown state→blocked
unknown SG ID→blocked
required gate欠落→blocked
satisfied根拠不足→blocked
na理由なし→blocked
state:satisfied != unrelated authority
```

### Safety Gate inheritance

```text
parent hold/blocked→child Phase/Sliceへ継承必須
scope拡大→satisfied再評価
summary/view→hold/blocked保持
parent na→child自動na禁止
```

### Safety Gate composition

```text
Safety Gate composition:=複数gateを加算的に適用する規則
```

Source:

```text
spec/registry/kdsl-safety-gate-composition.md
```

Rules:

```text
specialized gate != broader gate解除
single gate satisfied != composite safety satisfied
any blocked→operation blocked
no blocked + any hold→operation hold
all applicable satisfied→gate prerequisites satisfied
gate prerequisites satisfied != automatic execution permission
```

Representative composition:

```text
rollback/revert/未push破棄
→ SG-DESIGN/SG-ROLLBACK/SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP

runtime claim/RT:v
→ SG-EVIDENCE/SG-RUNTIME
```

### Typed non-substitution

```text
U承認 != runtime evidence
runtime evidence != commit/push/release authority
CI/validator pass != semantic equivalence
CI/validator pass != U承認
NEXT != execution authority
COMMIT.proposed != commit authority
satisfied gate != unrelated gate satisfaction
```

### SG ID-only compression

```text
SG ID-only compression:=SG IDだけでcritical natural-language safety wordingを置換すること
```

Current rule:

```text
禁止
current Full KDSL:=SG ID + complete protected wording
```

## Packet terms

### KDSL-Packet

```text
KDSL-Packet:=AI coding work-contract用packet envelope候補
```

Current status:

```text
draft-non-executable
```

Reason:

```text
Packet schema未定義
BASE/TASK/FLOW registry未定義
SG registryはv2-draftのみでstable/canonical Packet dependency未充足
R1C schema未定義
Packet lint未定義
```

### PACKET_DRAFT

```text
PACKET_DRAFT:=未定義Packetを設計検討するための非実行表記
```

Required marker:

```text
status: non-executable
schema: undefined
```

Constraints:

```text
AI coding tool直接投入禁止
valid-looking != executable
PKT:v1使用禁止
unknown registry推測禁止
```

## Result candidates

### R1C

```text
R1C:=R1/KDSL_RESULTのcompact schema候補
```

Current status:

```text
not canonical
not executable contract
```

## Release strategy

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft:=優先設計線
```

This status does not authorize tag, release, or Release Assets operations.
