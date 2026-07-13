# Phase 6C-3 — CompactPrompt Compatibility View Pilot

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 63
implementation_source_head: 34ec6ef9895ecb21b2e32e8c6db36da0a14ab003
implementation_squash_commit: 2df06525265b7fdf56b449447967f5e681534615
workflow_run_id: 29224978552
workflow_run_number: 293
workflow_conclusion: success

## 1. Goal

Add a bounded AST v2 compatibility view for CompactPrompt structural extraction and prove parity with the current checker before any checker switch.

```text
structural parity first
CP-Lift/restricted-alias semantics remain in current checker
checker switch deferred
```

## 2. Integrated files

```text
tools/validator/kdsl_parser_v2_compact_compat.py
tools/validator/kdsl_parser_v2_compact_parity.py
tools/validator/run_parser_v2_compact_parity_samples.py
```

Updated:

```text
tools/validator/run_all_samples.py
```

Unchanged:

```text
tools/validator/kdsl_compact_prompt.py
spec/profiles/kdsl-profile-compact-prompt.md
spec/lexicons/kdsl-lexicon-kanji-v1.md
spec/lint/kdsl-compact-prompt-lint.md
```

## 3. Compatibility surface

The view records:

```text
AST v2 DocumentNodeV2
CompactPrompt detection
KDSL-CP / KDSL-CP漢 shorthand
legacy-compatible scope
profile/mode/safety/lexicon headers
typed CompactBlockNodeV2 records
block order/content/source span
duplicate block order
```

Compared legacy contract:

```text
detect_profile
detect_shorthand
extract_scope
header_value
parse_blocks
```

## 4. Structural forms covered

Standard form:

```text
Goal
Input
Output
Guard
Check
optional Role/Rules/Style
```

kanji-v1 form:

```text
目
材
出
守
確
optional 役/則/調
```

The view preserves the current raw block cleaning and scope termination behavior. It does not reinterpret free text.

## 5. Semantic boundary retained

The following remain exclusively in the current checker:

```text
mode/safety/lexicon validity decisions
KDSL-CP漢 mode/lexicon conflict decisions
required/empty block validity
mixed-key warning policy
restricted free-text alias detection
CP-Lift trigger detection and negation guard
PKT:v1 prohibition
PACKET_DRAFT non-executable marker checks
```

```text
CompatibilityView != CompactPrompt semantic checker
parity pass != CP-Lift safety proof
```

## 6. Verification

```text
source head: 34ec6ef9895ecb21b2e32e8c6db36da0a14ab003
workflow run: 29224978552 / #293
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
CompactPrompt parity: 8 / failed 0
previous unified expectations: 279 / failed 0
current unified expectations: 287 / failed 0
unified runners: 11
```

Cases:

```text
standard valid sample
kanji-v1 valid sample
missing-block sample
restricted-alias sample
CP-Lift-required sample
repository standard example
repository kanji-v1 example
repository novel-review example
```

Invalid semantic samples are expected to pass structural parity because parity checks extraction equality, not semantic validity.

## 7. Current migration state

```text
CompactPrompt compatibility view: integrated
CompactPrompt structural parity corpus: integrated
CompactPrompt checker switch: not performed
CP-Lift semantics: unchanged
restricted alias semantics: unchanged
```

The current checker remains the active semantic validator.

## 8. Safety and authority boundaries

```text
parity pass != semantic equivalence
parity pass != complete safety proof
parity pass != U approval
parity pass != RT:v
parity pass != execution authority
validator/CI pass != release readiness
```

Retained:

```text
implementation/repo/runtime/public/data/source-of-truth/AI coding triggers→CP-Lift
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
Packet executable:no
Packet state:not_normalized
PKT:v1使用禁止
stable/public-ready/tag/release/Release Assets操作なし
```

## 9. Known limitations

```text
checker has not switched to CompatibilityView
profile-only/no-shorthand corpus remains limited
complete Markdown/fence semantics not proven
full natural-language CP-Lift/negation reasoning not implemented
structural parity != meaning preservation proof
Safety Gate/Packet/Normalization compatibility views pending
```

## 10. Next safe step

Candidate Phase 6C-4:

```text
migrate CompactPrompt structural extraction to CompatibilityView
retain legacy-v2 parity guard during migration
keep all semantic and safety regex/policies unchanged
add profile-only, duplicate, mixed-key and fenced-scope guard cases
```

Alternative next bounded target:

```text
Safety Gate compatibility view pilot before CompactPrompt checker switch
```

Recommended order:

```text
CompactPrompt checker switch
→ Safety Gate view/migration
→ Packet view/migration
→ Packet Normalization view/migration
```

## 11. Closeout decision

```text
Phase 6C-3 CompactPrompt compatibility pilot: integrated
CompactPrompt checker migration: pending
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
Packet executable: no
public_ready: no
stable_release: no
```
