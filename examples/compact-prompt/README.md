# KDSL CompactPrompt Examples

status: v2-draft examples
scope: KDSL-CP / KDSL-CP漢 / CP-Lift examples
canonical: no

These examples demonstrate how KDSL-CP can be used for general LLM prompts and Project files.

They are understanding aids, not Core specification.

## Files

```text
blog_meta.kdsl-cp.md:
  Standard KDSL-CP example for blog metadata generation.

blog_meta.kdsl-cp-kanji.md:
  Dense Japanese alias version of the same blog metadata prompt.

novel_review.kdsl-cp-kanji.md:
  KDSL-CP漢 example for fiction review.

prompt_improver.kdsl-cp.md:
  General prompt improvement example.

cp_lift_example.md:
  Boundary example showing when KDSL-CP must be lifted to KDSL-Packet / Full KDSL.
```

## Principles

```text
KDSL-CP:
  general LLM / Project files / single prompt use

KDSL-CP漢:
  dense-ja alias form for Japanese prompts

CP-Lift:
  implementation/repo/runtime/public operations → KDSL-Packet or Full KDSL
```

## Non-goals

```text
AI coding tool implementation contract
R1/KDSL_RESULT replacement
RT:v condition relaxation
KDSL-DP/P1/P1L boundary change
Core canonical replacement
```

## Review checklist

```text
Guard保持
Check保持
src外事実追加禁止保持
unk→断定禁止保持
est→推測明記保持
fmt外出力禁止保持
CP-Lift条件に該当しないこと
```
