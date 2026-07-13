# KDSL CompactPrompt Validator

status: experimental-first-slice / phase6c-compatibility-view-integrated
script: tools/validator/kdsl_compact_prompt.py
compatibility_view: tools/validator/kdsl_parser_v2_compact_compat.py
parity_checker: tools/validator/kdsl_parser_v2_compact_parity.py
phase6c_pull_request: 63
phase6c_squash_commit: 2df06525265b7fdf56b449447967f5e681534615
phase6c_workflow: 29224978552 / 293 / success
source_specs:

```text
spec/profiles/kdsl-profile-compact-prompt.md
spec/lexicons/kdsl-lexicon-kanji-v1.md
spec/lint/kdsl-compact-prompt-lint.md
spec/bridge/kdsl-cp-packet-bridge.md
```

## Purpose

Provide a lightweight heuristic lint for KDSL-CP and KDSL-CP漢 without claiming full parsing or semantic equivalence.

```text
CompatibilityView != CompactPrompt semantic checker
parity pass != semantic equivalence/safety proof/RT:v/U approval
```

## Implemented semantic checks

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

## Phase 6C compatibility view

Integrated structural view:

```text
tools/validator/kdsl_parser_v2_compact_compat.py
```

Recorded structure:

```text
DocumentNodeV2
CompactPrompt detection
KDSL-CP / KDSL-CP漢 shorthand
legacy-compatible scope
profile/mode/safety/lexicon headers
CompactBlockNodeV2 records
block order/content/source span
duplicate block order
```

Compared legacy functions:

```text
detect_profile
detect_shorthand
extract_scope
header_value
parse_blocks
```

The view intentionally does not decide:

```text
CP-Lift
restricted free-text aliases
mode/safety/lexicon validity
required/empty block validity
mixed-key warning policy
Packet execution/authority boundaries
```

These remain in `kdsl_compact_prompt.py`.

## Verification

```text
CompactPrompt parity corpus: 8 / failed 0
unified runners: 11
unified expectations: 287 / failed 0
workflow: KDSL Validation
workflow run: 29224978552 / #293 / success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

Corpus includes valid and semantically invalid samples because structural parity is independent from semantic exit classification.

## Exit codes

```text
0:=pass
1:=warn
2:=fail
```

## Scope extraction

When `KDSL-CP:` or `KDSL-CP漢:` appears inside a Markdown code block, the checker evaluates from the shorthand marker to the closing code fence. Notes after the prompt are not interpreted as prompt instructions.

The compatibility view preserves this current scope-selection behavior.

## Current migration boundary

```text
CompatibilityView: integrated
parity corpus: integrated
checker switch: not performed
legacy semantic policy: active
```

A checker switch requires a separate phase with an in-process parity guard and unchanged CP-Lift/restricted-alias policies.

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
profile-only/no-shorthand corpusは限定的
checkerはCompatibilityView未使用
validator pass != safety proof
validator pass != RT:v
validator pass != U承認
```

## Next safe step

```text
CompactPrompt checker structural extraction→CompatibilityView
legacy-v2 parity guard保持
CP-Lift/restricted alias/Packet boundary意味変更禁止
profile-only/duplicate/mixed/fenced guard case追加
```
