# KDSL v2 Direction Draft

status: v2-draft-planning
scope: KDSL family restructuring / CompactPrompt / Packet / R1 compact candidates
base_state: v1.1.0-rc1 experimental preview
stable_release: none
public_ready: no
release_assets: none

## 1. Purpose

This document records the approved direction for a KDSL v2 draft line.

The goal is to keep the safety-gate-preserving value of KDSL while reducing prompt length and separating lightweight general LLM prompts from heavier AI coding tool work contracts.

```text
priority: safety gate保持 > 意味保持 > 判断分岐保持 > 誤実装防止 > 圧縮率 > 可読性
```

## 2. Current baseline

```text
v1.1.0-rc1:
  status: experimental preview
  public: yes
  public_ready: no
  stable_release: none
  Release Assets: none
```

This v2 draft does not promote v1.1.0-rc1 to stable, does not move existing tags, and does not create or modify Release Assets.

## 3. Family split

```text
KDSL-Core:
  KDSL本体仕様。operator / abbrev / 保護語 / 変換禁止 / mode / safety の正本。

KDSL-CP:
  CompactPrompt。一般LLM / Project files / 単体prompt向け軽量サブセット。

KDSL-Packet:
  GPT↔Codex / AI coding tool向け作業契約packet。
  BASE / TASK / SG / FLOW / R1C / human render を扱う重装備サブセット。

KDSL-R1:
  KDSL_RESULT / Evidence / RT / Authority の結果証跡仕様。

KDSL-R1C:
  KDSL_RESULT compact candidate。通常報告の冗長な定型を圧縮する候補。

KDSL-SG:
  Safety gate registry / bitmask candidate。安全gate状態をschema化して圧縮報告する候補。
```

Notes:

```text
KDSL-P という略称は非推奨。
理由: P1/P1L と衝突しやすい。
推奨表記: KDSL-Packet
```

## 4. Design direction

### 4.1 KDSL-CP first

KDSL-CP is the first v2 draft target because it is useful for general LLM prompts and Project files without requiring the heavier Packet/R1C/SG machinery.

```text
KDSL-CP target:
  high-compression general prompts
  Project files
  single prompt instructions
  low learning cost
  safety gate保持
```

### 4.2 Kanji aliases

KDSL v2 may add dense Japanese aliases for CompactPrompt.

```text
KDSL-CP:min:
  Role / Goal / Input / Output / Rules / Guard / Style / Check

KDSL-CP:dense-ja:
  役 / 目 / 材 / 出 / 則 / 守 / 調 / 確
```

Kanji aliases are compression aliases, not permission to weaken protected words.

### 4.3 Protected words remain protected

The following words and meanings must not be shortened away in safety-critical contexts.

```text
禁止
必須
未確認
未実行
承認
承認待
断定禁止
確認済扱禁止
実行済扱禁止
成功扱禁止
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v
KDSL_RESULT NEXT
KDSL_RESULT COMMIT
public履歴
公開済tag
Release Assets
rollback
revert
```

### 4.4 CP-Lift

KDSL-CP must not be used as a lightweight shortcut for dangerous implementation work. If a prompt crosses into implementation or repository operations, it must be lifted to KDSL-Packet or Full KDSL.

```text
CP-Lift triggers:
  実装/改修/削除
  repo/path/branch/commit操作
  rollback/revert
  RT:v/実機確認
  public履歴/tag/Release Assets
  data migration
  AI coding toolへ渡す場合
```

## 5. Initial v2-draft files

```text
docs/design/kdsl-v2-direction.md
spec/profiles/kdsl-profile-compact-prompt.md
spec/profiles/kdsl-compact-kanji-aliases.md
spec/bridge/kdsl-cp-packet-bridge.md
```

These files are v2-draft additions. They do not replace the v1.1 Core/R1/Lint/Bridge canonical files.

## 6. Later candidates

```text
spec/r1/r1-compact-schema.md
spec/safety/safety-gate-registry.md
spec/packet/kdsl-packet-registry.md
templates/packet/human_render_min.md
examples/compact-prompt/*
examples/packet/*
```

## 7. Non-goals

```text
Core正本の即置換
v1.1.0-rc1のstable化
既存tag移動
Release Assets操作
validatorを承認者扱い
RT:v条件緩和
保護語弱化
```

## 8. Promotion policy

A v2 draft item can be promoted only after the following are recorded.

```text
採用理由
不採用代替案
影響範囲
互換性: breaking/compatible/patch
必要lint
必要example
U明示承認
```
