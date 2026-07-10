# KDSL CompactPrompt Examples

status: v2-draft examples
scope: KDSL-CP / kanji-v1 / CP-Lift
canonical: no

These examples demonstrate general LLM and Project file use of KDSL-CP.

They are understanding aids, not Core/Profile/Lexicon canonical specifications.

## Files

```text
blog_meta.kdsl-cp.md:
  Standard lexicon example for blog metadata generation.

blog_meta.kdsl-cp-kanji.md:
  `profile:compact-prompt + mode:dense + lexicon:kanji-v1` version.

novel_review.kdsl-cp-kanji.md:
  kanji-v1 structural-key example for fiction review.

prompt_improver.kdsl-cp.md:
  General prompt improvement example.

cp_lift_example.md:
  Boundary example showing when KDSL-CP must lift to Full KDSL.
  Future Packet is shown only as draft-non-executable.
```

## Architecture

```text
KDSL-CP:=profile:compact-prompt
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1
CP-Lift current target:=Full KDSL profile:dev-prompt
KDSL-Packet current status:=draft-non-executable
```

## Kanji lexicon rule

```text
構造alias:
  役/目/材/出/則/守/調/確
  → KEY位置のみ使用

safety-critical free text:
  完全語を使用
  禁止/不明/事実/未確認/未実行/承認/承認待/断定禁止を一字化しない
```

## Non-goals

```text
AI coding tool implementation contract
R1/KDSL_RESULT replacement
RT:v condition relaxation
KDSL-DP/P1/P1L boundary change
Core canonical replacement
undeclared Packet execution
```

## Review checklist

```text
Goal/Input/Output/Guard/Check保持
kanji-v1時は目/材/出/守/確保持
Guard保持
Check保持
入力外事実追加禁止保持
不明→断定禁止保持
推測→推測明記保持
指定形式外出力禁止保持
restricted一字aliasなし
CP-Lift条件確認
未定義Packet直接実行なし
```
