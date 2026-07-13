# Phase 6C-2 — R1C Checker Migration to AST v2

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 61
implementation_source_head: 627fde4a718a40a762b6285884f756a9ccd60dc5
implementation_squash_commit: a81bb8cae5aefd4020c0df004c616d5e4f834cee
final_workflow_run_id: 29224617949
final_workflow_run_number: 289
final_workflow_conclusion: success

## 1. Goal

Migrate only the R1C checker structural extraction path from the Phase 1 namespace adapter to the explicit AST v2 `R1CCompatibilityView`, while retaining an in-process legacy-v2 parity guard before R1C semantic validation.

```text
bounded checker migration > broad adapter removal
parity guard > silent reinterpretation
Full R1 fallback preservation > universal KDSL_RESULT capture
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_parser_v2_compat.py
tools/validator/kdsl_parser_v2_r1c_parity.py
tools/validator/kdsl_r1c.py
tools/validator/run_parser_v2_r1c_parity_samples.py
```

Added permanent corpus:

```text
tools/validator/samples/parser-v2/r1c_safety_gates_optional.md
tools/validator/samples/parser-v2/r1c_same_marker_duplicate.md
```

Not changed:

```text
R1C semantic rules
canonical R1/R1C specifications
RT/NEXT/COMMIT meanings
Packet checker extraction
Packet Normalization checker extraction
Safety Gate checker extraction
legacy adapter file for remaining consumers
```

## 3. Final R1C runtime path

```text
input
→ AST v2 R1C compatibility scope/extraction
→ no R1C schema: Full R1 fallback/out-of-scope
→ R1C schema present: legacy extraction + AST v2 extraction
→ parity mismatch: fail before semantic validation
→ parity match: existing R1C semantic validation
```

`kdsl_r1c.py` no longer installs its own Phase 1 namespace adapter. The Phase 1 adapter remains available for other checkers.

## 4. Corrective history

### 4.1 Full R1 fallback ordering

Initial migration applied the parity guard before schema classification.

Risk:

```text
non-R1C KDSL_RESULT / Full R1 could be rejected by an R1C-only migration guard
```

Correction:

```text
extract selected scope
→ inspect SCHEMA
→ no R1C schema: Full R1 fallback/out-of-scope
→ only R1C schema documents enter parity guard
```

### 4.2 Optional SAFETY_GATES ambiguity

`SAFETY_GATES:` has two structural roles:

```text
standalone KDSL-family envelope marker
R1C optional field
```

The general AST v2 parser correctly treated it as a standalone envelope marker. Within an already selected R1C scope, however, this prematurely ended the R1C envelope and broke optional-block round-trip validation.

Bounded correction:

```text
R1CCompatibilityView scope only:
  temporarily remove SAFETY_GATES from general envelope markers
  parse selected R1C raw-envelope scope
  restore marker registry in finally
```

Retained boundary:

```text
AST v2 active-document behavior: unchanged
general standalone SAFETY_GATES behavior: unchanged
R1C optional SAFETY_GATES field: preserved
```

### 4.3 Diagnostic isolation

Temporary diagnostic runners and temporary reduced unified-runner configurations were used to isolate failures through:

```text
core R1C cases
standalone parity corpus
R1C round-trip
R1C optional blocks
SAFETY_GATES validator stage
```

All temporary diagnostic files were deleted and the complete unified runner was restored before the final verification run.

## 5. Final verification

```text
final source head: 627fde4a718a40a762b6285884f756a9ccd60dc5
workflow: KDSL Validation
workflow run: 29224617949 / #289
KDSL Validation: success
Packet Semantic Property: success
```

Validated aggregate:

```text
unified runners: 10
unified expectations: 279
failed: 0
R1C legacy-v2 parity cases: 10 / failed 0
```

The 279 expectations are the previously integrated 277 plus:

```text
R1C optional SAFETY_GATES parity pass
same-marker divergence rejected by parity guard
```

## 6. Permanent guard cases

### Optional SAFETY_GATES

Confirms that:

```text
R1C optional field remains in selected R1C scope
legacy and AST v2 raw values match
round-trip and optional-block consumers remain compatible
```

### Same-marker duplicate divergence

Confirms that unsupported extraction divergence does not continue into semantic validation.

```text
parity mismatch→R1C validation fail
silent first/second envelope reinterpretation→prohibited
```

## 7. Current migration state

```text
R1C compatibility view: integrated
R1C checker extraction: AST v2 compatibility path
R1C legacy-v2 parity guard: active
R1C semantic checker policy: unchanged
```

Remaining Phase 1 adapter consumers:

```text
Packet
Packet Normalization
Safety Gate
```

The adapter itself must not be removed until those consumers have explicit compatibility views and parity evidence.

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
RT:v=対象環境runtime確認済のみ
NEXT:=提案, 実行許可扱禁止
COMMIT自動commit許可扱禁止
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
Packet executable:no
Packet state:not_normalized
PKT:v1使用禁止
stable/public-ready/tag/release/Release Assets操作なし
```

## 9. Known limitations

```text
R1C full semantic equivalence: not_proven
complete safety proof: not_proven
same-marker multiple-envelope semantics: not generally defined
parity guard proves selected structural contract only
Full R1 compatibility view: not implemented
CompactPrompt compatibility view: not implemented
Safety Gate/Packet/Normalization compatibility views: not implemented
legacy adapter retirement proof: absent
```

## 10. Next safe step

Recommended Phase 6C-3:

```text
Full R1 / CompactPrompt structural compatibility inventory
select one bounded migration target
add explicit view + parity corpus before checker switch
```

Preferred order:

```text
CompactPrompt header/structural extraction
→ Safety Gate records
→ Packet
→ Packet Normalization
```

Reason:

```text
CompactPrompt establishes header/profile/lexicon structure
Safety Gate has protected-language and state sensitivity
Packet/Normalization retain the broadest execution/authority boundaries
```

## 11. Closeout decision

```text
Phase 6C-2 R1C checker migration: integrated
Issue #55: remain open
legacy adapter removal: prohibited
semantic equivalence: not_proven
complete safety proof: not_proven
Packet executable: no
public_ready: no
stable_release: no
```
