# KDSL v2 Draft Glossary

status: v2-draft
canonical: no
source_alignment: docs/design/kdsl-v2-direction.md

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
BASE/TASK/FLOW/SG registry未定義
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

### SG

```text
SG:=safety gate registry/state schema候補
```

Current status:

```text
not canonical
```

## Release strategy

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft:=優先設計線
```

This status does not authorize tag, release, or Release Assets operations.
