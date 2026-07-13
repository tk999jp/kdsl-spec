# KDSL CompactPrompt Validator

status: experimental-first-slice / phase6c-checker-migrated
script: tools/validator/kdsl_compact_prompt.py
compatibility_view: tools/validator/kdsl_parser_v2_compact_compat.py
parity_checker: tools/validator/kdsl_parser_v2_compact_parity.py
compatibility_pull_request: 63
compatibility_squash_commit: 2df06525265b7fdf56b449447967f5e681534615
migration_pull_request: 65
migration_squash_commit: 4d4a5f7b6580ecec44636f8e09e163540fb17770
latest_workflow: 29230246858 / 297 / success
source_specs:

```text
spec/profiles/kdsl-profile-compact-prompt.md
spec/lexicons/kdsl-lexicon-kanji-v1.md
spec/lint/kdsl-compact-prompt-lint.md
spec/bridge/kdsl-cp-packet-bridge.md
```

## Purpose

Provide a lightweight heuristic lint for KDSL-CP and KDSL-CP漢 without claiming full semantic equivalence or complete natural-language safety analysis.

```text
CompatibilityView != semantic equivalence proof
validator pass != safety proof/RT:v/U approval/authority/release readiness
```

## Active structural path

```text
input
→ CompactPromptCompatibilityView
→ legacy-v2 structural parity guard
→ mismatch: fail before semantic validation
→ match: AST v2 scope/header/block/duplicate extraction
→ existing semantic and safety checks
```

The active checker now reads these structural values from the compatibility view:

```text
CompactPrompt detection
KDSL-CP / KDSL-CP漢 shorthand
scope
profile/mode/safety/lexicon headers
standard/kanji-v1 block values
same-key duplicates
```

Legacy helper functions remain only for in-process parity comparison.

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

structure policy:
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

These semantic decisions were not changed by the AST v2 migration.

## Compatibility and parity surface

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

Parity mismatch behavior:

```text
CompactPrompt parser parity guard: <mismatch>
→ exit 2 before semantic validation
```

## Verification

```text
CompactPrompt parity corpus: 12 / failed 0
CompactPrompt checker migration corpus: 4 / failed 0
unified runners: 12
unified expectations: 295 / failed 0
workflow: KDSL Validation
workflow run: 29230246858 / #297 / success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

Permanent migration cases:

```text
profile-only/no-shorthand form
same-key duplicate warning
mixed standard/kanji warning
fenced scope excluding following notes
```

The fenced case retains the contract that content after the closing Markdown fence is not interpreted as CompactPrompt instruction text.

## Exit codes

```text
0:=pass
1:=warn
2:=fail
```

## Current boundaries

```text
CP-Lift semantics: unchanged
restricted alias semantics: unchanged
mode/safety/lexicon semantics: unchanged
Packet boundary semantics: unchanged
legacy helper removal: prohibited while parity guard is required
```

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
string/regex semantic checks remain
CP-Lift covers representative triggers only
unknown natural-language expressions are not completely detected
structural parity != meaning-preservation proof
same-marker/general context semantics remain incomplete
validator pass != safety proof
validator pass != RT:v
validator pass != U approval
```

## Next safe step

```text
Safety Gate compatibility view/parity pilot
→ Safety Gate checker migration only after parity evidence
→ Packet compatibility view/migration
→ Packet Normalization compatibility view/migration
```
