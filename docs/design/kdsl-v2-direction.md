# KDSL v2 Direction Draft

status: v2-draft-planning
scope: KDSL architecture / CompactPrompt / Lexicon / Packet / R1 compact candidates
base_state: v1.1.0-rc1 experimental preview
stable_release: none
public_ready: no
Release Assets: none
license: MIT

## 1. Purpose

This document records the approved direction for the KDSL v2 draft line.

The goal is to preserve KDSL meaning and safety gates while reducing prompt length and separating general LLM prompts from AI coding work contracts without turning them into unrelated languages.

```text
priority: 意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 出力安定 > 圧縮率 > 人間可読性
```

## 2. Current baseline

```text
v1.1.0-rc1:
  status: experimental preview
  public: yes
  public_ready: no
  stable_release: none
  Release Assets: none
  license: MIT
```

Policy:

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft設計を優先
既存tag移動禁止
Release Assets操作禁止
stable/public-ready化→別途U明示承認必須
```

## 3. Orthogonal architecture

KDSL v2 is organized by orthogonal axes rather than treating every variation as a separate language.

```text
format:
  KDSL

profile:
  compact-prompt
  dev-prompt
  converter
  lint

mode:
  readable
  min
  dense
  lock

safety:
  normal
  lock-critical
  lock-all

lexicon:
  standard
  kanji-v1

envelope:
  plain
  packet-draft
  result
```

Meaning:

```text
profile:=用途
mode:=圧縮強度
safety:=安全保持強度
lexicon:=使用語彙/alias集合
envelope:=入出力を包む契約形式
```

## 4. Named compositions

The following names are compositions of the axes above.

```text
KDSL-Core:
  format/operator/保護語/変換禁止/mode/safetyの正本

KDSL-CP:
  profile:compact-prompt
  general LLM / Project files / single prompt use

KDSL-CP漢:
  profile:compact-prompt
  mode:dense
  lexicon:kanji-v1

KDSL-Packet:
  envelope:packet
  AI coding work-contract candidate
  registry未整備のため現時点ではdraft-non-executable

KDSL-R1:
  envelope:result
  KDSL_RESULT / Evidence / RT / Authority

KDSL-R1C:
  compact result schema candidate

KDSL-SG:
  safety gate registry / state schema candidate
```

`KDSL-P` is not used because it can be confused with P1/P1L.

## 5. CompactPrompt first

KDSL-CP is the first v2 draft target.

```text
対象:
  general LLM prompts
  Project files
  single prompt instructions
  text generation / review / summary / research / comparison

非対象:
  AI coding implementation contract
  repository operation
  rollback/revert
  runtime verification
  release/tag/Release Assets operation
```

KDSL-CP must remain standalone and low-registry, while using an official minimal vocabulary and lint rules.

## 6. Lexicon policy

Kanji aliases belong to the `lexicon` axis, not to `mode` or `profile`.

```text
standard block keys:
  Role / Goal / Input / Output / Rules / Guard / Style / Check

kanji-v1 structural keys:
  役 / 目 / 材 / 出 / 則 / 守 / 調 / 確
```

Rules:

```text
構造alias:=KEY位置のみ使用
free-text一字alias:=原則禁止
保護語弱化禁止
unknown lexicon/alias推測禁止
```

The following must remain explicit in free text:

```text
禁止
必須
不明
事実
未確認
未実行
承認
承認待
断定禁止
確認済扱禁止
実行済扱禁止
成功扱禁止
```

## 7. CP-Lift

KDSL-CP must not be used as a lightweight shortcut for implementation work.

```text
CP-Lift triggers:
  実装/改修/削除
  repo/path/branch/commit操作
  file/API/command変更
  rollback/revert
  未push破棄
  RT:v/実機確認
  public履歴/tag/Release Assets
  data migration
  正本変更
  AI coding toolへ渡す場合
```

Current lift target:

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min|dense|lock
safety: lock-critical|lock-all
```

Future Packet target:

```text
KDSL-Packet registry未定義→実行禁止
packet draft valid-looking != executable
unknown BASE/TASK/FLOW/SG/R1C推測禁止
```

## 8. v2-draft files

```text
docs/design/kdsl-v2-direction.md
spec/profiles/kdsl-profile-compact-prompt.md
spec/lexicons/kdsl-lexicon-kanji-v1.md
spec/lint/kdsl-compact-prompt-lint.md
spec/bridge/kdsl-cp-packet-bridge.md
spec/glossary-v2-draft.md
examples/compact-prompt/*
```

These files do not replace the v1.1 Core/R1/Lint/ADPS Bridge canonical files.

## 9. Later candidates

```text
spec/r1/r1-compact-schema.md
spec/safety/safety-gate-registry.md
spec/packet/kdsl-packet-registry.md
templates/packet/human_render_min.md
examples/packet/*
```

## 10. Non-goals

```text
Core正本の即置換
v1.1.0 stable化
既存tag移動
Release Assets操作
validatorを承認者扱い
RT:v条件緩和
保護語弱化
未定義Packet直接実行
```

## 11. Promotion policy

A v2 draft item can be promoted only after the following are recorded.

```text
採用理由
不採用代替案
影響範囲
互換性: breaking/compatible/patch
必要lint
必要example
Core/R1/Bridgeとの整合
保護語弱化なし
U明示承認
```
