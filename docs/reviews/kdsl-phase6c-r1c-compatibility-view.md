# Phase 6C-1 — R1C Parser Compatibility View

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 59
implementation_source_head: 0f974b0d91c0188761f779de16c4dc43d07a2551
implementation_squash_commit: e20ebde511ce860faf9224f0b5902c08309a0a6f
final_workflow_run_id: 29223392311
final_workflow_run_number: 263
final_workflow_conclusion: success

## 1. Goal

Create the first explicit AST v2 compatibility view and prove bounded structural parity with the Phase 1 R1C extraction contract before switching the existing R1C checker.

```text
parity evidence > checker switch
raw-source preservation > normalized-value convenience
bounded pilot > legacy adapter removal
```

## 2. Integrated files

```text
tools/validator/kdsl_parser_v2_compat.py
tools/validator/kdsl_parser_v2_r1c_parity.py
tools/validator/run_parser_v2_r1c_parity_samples.py
tools/validator/samples/parser-v2/r1c_quoted_scalar.md
```

Updated:

```text
tools/validator/run_all_samples.py
```

## 3. Compatibility contract

The compatibility view compares:

```text
KDSL_RESULT envelope presence
selected scope lines
field order
legacy-compatible raw field values
relative field line numbers
duplicate field order
```

Values are reconstructed from AST v2 raw source, not from normalized semantic nodes.

Retained source properties:

```text
quotes
multiline JSON text
protected Japanese wording
block-scalar style behavior
field order
relative line positions
duplicate order
```

## 4. Corrective history

### Initial failure

```text
workflow run #261:
  KDSL Validation: failure
  Packet Semantic Property: success

workflow run #262:
  KDSL Validation: failure
  Packet Semantic Property: success
  compact failure logging: enabled
```

Root cause:

```text
repository R1C examples place KDSL_RESULT inside Markdown fences
Phase 1 legacy parser selects the fenced KDSL_RESULT scope
AST v2 active-document intentionally excludes fenced envelopes
compatibility view therefore reported envelope-presence mismatch
```

### Corrective implementation

```text
R1CCompatibilityView selects the first legacy-compatible KDSL_RESULT scope
selected scope is parsed by AST v2 in raw-envelope context
AST v2 active-document fence-isolation policy remains unchanged
existing kdsl_r1c.py remains unchanged
existing kdsl_parser_adapter.py remains unchanged
```

The correction is limited to the compatibility surface. It does not redefine active-document semantics.

## 5. Final verification

```text
source head: 0f974b0d91c0188761f779de16c4dc43d07a2551
workflow run: 29223392311 / #263
KDSL Validation: success
Packet Semantic Property: success
```

Corpus:

```text
R1C legacy-v2 parity: 8 / failed 0
previous unified expectations: 269 / failed 0
current unified expectations: 277 / failed 0
unified runners: 10
```

Parity cases:

```text
multiline JSON
duplicate fields
invalid JSON raw extraction
no KDSL_RESULT envelope
quoted scalar and protected wording
repository success example
repository blocked example
repository needs-user example
```

## 6. Unified runner observability corrective

`run_all_samples.py` now:

```text
prints compact summaries for successful child runners
prints full stdout/stderr only for failed or malformed child runners
retains missing-summary and non-zero-exit failure behavior
```

This changes log verbosity only. It does not weaken any test or acceptance condition.

## 7. Migration boundary retained

```text
R1CCompatibilityView: integrated
R1C parity corpus: integrated
existing R1C checker switch: not performed
legacy adapter: retained
legacy adapter removal: prohibited
```

The view is not yet the production extraction path for `kdsl_r1c.py`.

## 8. Safety and authority boundaries

```text
parity pass != semantic equivalence
parity pass != complete safety proof
parity pass != U approval
parity pass != RT:v
parity pass != execution authority
parity pass != release readiness
```

Retained:

```text
RT:v条件変更なし
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
parity scope is bounded to first R1C compatibility contract
same-marker duplicate envelope parity not proven
R1C semantic checker still uses Phase 1 adapter
Full R1/CompactPrompt/Safety Gate/Packet compatibility views not implemented
legacy adapter retirement proof absent
not a semantic-equivalence proof
```

## 10. Next safe step

Phase 6C-2 candidate:

```text
switch kdsl_r1c.py structural extraction to explicit R1CCompatibilityView
retain a legacy-v2 dual-run/parity guard during migration
require all existing R1C expected exits to remain unchanged
retain legacy adapter for Packet/Normalization/Safety Gate
```

Stop when:

```text
R1C expected exits change
RT/NEXT/COMMIT inputs differ
fenced/unfenced scope behavior changes unexpectedly
unknown schema/default inference would be required
```

## 11. Closeout decision

```text
Phase 6C-1 compatibility view: integrated
Phase 6C-2 checker switch: pending
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
Packet executable: no
public_ready: no
stable_release: no
```
