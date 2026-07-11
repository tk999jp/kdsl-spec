# KDSL CompactPrompt Validator First Slice

status: experimental-first-slice
script: tools/validator/kdsl_compact_prompt.py
source_specs:

```text
spec/profiles/kdsl-profile-compact-prompt.md
spec/lexicons/kdsl-lexicon-kanji-v1.md
spec/lint/kdsl-compact-prompt-lint.md
spec/bridge/kdsl-cp-packet-bridge.md
```

## Purpose

Provide a lightweight heuristic lint for KDSL-CP and KDSL-CP漢 without claiming full parsing or semantic equivalence.

## Implemented checks

```text
CompactPrompt detection:
  profile:compact-prompt
  KDSL-CP:
  KDSL-CP漢:

axis validation:
  mode:=readable|min|dense|lock
  safety:=normal|lock-critical|lock-all
  lexicon:=standard|kanji-v1
  mode:dense-ja→fail

required blocks:
  standard:=Goal/Input/Output/Guard/Check
  kanji-v1:=目/材/出/守/確

structure:
  empty required block→fail
  mixed standard/kanji keys→warn
  duplicate block→warn

kanji-v1:
  restricted free-text alias shape→fail
  structural key at key position→allowed

CP-Lift:
  implementation/repository/runtime/release/data/source-of-truth/AI coding trigger→fail
  explicit prohibition clause such as safety gate削除禁止→trigger除外

Packet boundary:
  PKT:v1→fail
  incomplete PACKET_DRAFT markers→fail
```

## Exit codes

```text
0:=pass
1:=warn
2:=fail
```

## Scope extraction

When `KDSL-CP:` or `KDSL-CP漢:` appears inside a Markdown code block, the checker evaluates from the shorthand marker to the closing code fence. Notes after the prompt are not interpreted as prompt instructions.

## Non-goals

```text
semantic equivalence proof
full Markdown parser
full natural-language parser
complete negation analysis
runtime verification
U approval
release readiness
Packet schema validation
```

## Known limitations

```text
string/regex heuristic中心
CP-Liftは代表triggerのみ
未知の自然言語表現を完全検出しない
validator pass != safety proof
validator pass != RT:v
validator pass != U承認
```
