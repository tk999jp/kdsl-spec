from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, got {count}: {old!r}')
    target.write_text(text.replace(old, new), encoding='utf-8')


# Root README current status/navigation/validation/gaps/next phases.
replace_once(
    'README.md',
    '''Packet normalization structural round-trip: first-slice integrated / selected structural properties only
validator sample suite: 108 expectations / failed 0
validator_authority: non_authoritative''',
    '''Packet normalization structural round-trip: first-slice integrated / selected structural properties only
Common parser/AST: Phase 1 integrated / source-spanned first slice
major parser adapters: R1C / Packet / Packet Normalization / Safety Gate
KDSL Validation unified suite: 147 expectations / failed 0
required check activation: pending / issue #39
validator_authority: non_authoritative''',
)
replace_once(
    'README.md',
    '''  tools/validator/kdsl_packet_roundtrip.py
  tools/validator/run_samples.py
  tools/validator/samples/*''',
    '''  tools/validator/kdsl_packet_roundtrip.py
  tools/validator/kdsl_parser.py
  tools/validator/kdsl_parse.py
  tools/validator/kdsl_parser_adapter.py
  tools/validator/run_all_samples.py
  tools/validator/run_parser_samples.py
  tools/validator/run_samples.py
  tools/validator/samples/*''',
)
replace_once(
    'README.md',
    '''python tools/validator/kdsl_packet_roundtrip.py <packet-file> [normalization-file]
python tools/validator/kdsl_validate.py --target all <file>''',
    '''python tools/validator/kdsl_packet_roundtrip.py <packet-file> [normalization-file]
python tools/validator/kdsl_parse.py --envelope <MARKER> [--json] <file>
python tools/validator/kdsl_validate.py --target all <file>''',
)
replace_once(
    'README.md',
    '''Current sample runner:

```text
python tools/validator/run_samples.py
```

Latest CI evidence:

```text
sample expectations: 69
failed: 0
workflow: .github/workflows/validator.yml
latest Packet PR: #14
latest Packet run: #116 / success
```''',
    '''Current unified runner:

```text
python tools/validator/run_all_samples.py

component runners:
  run_samples.py: 108
  run_safety_gate_samples.py: 14
  run_r1c_roundtrip_samples.py: 14
  run_parser_samples.py: 11
```

Latest CI evidence:

```text
pull_request: 38
source_head: 9fe8912b39e5df1b31b85e3302dfda35351f25c0
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
workflow/check: KDSL Validation
workflow_run: #192 / success
unified expectations: 147
failed: 0
required-check repository setting: pending / issue #39
```''',
)
replace_once(
    'README.md',
    '''full YAML/JSON/KDSL parserなし
full natural-language semantic parserなし
full negation parserなし
protected wording semantic equivalence lintなし
Safety Gate parent-child inheritance lintなし
Safety Gate aggregate state lintなし
R1C multi-line JSON lintなし
R1C round-trip semantic proofなし
Packet validator first slice:=main integrated / 69 expectations verified
Packet full YAML/semantic parserなし
Packet normalization validator/mapper first slice:=main integrated / 93 expectations verified
Packet normalization structural round-trip first slice:=main integrated / 108 expectations verified
Packet normalization semantic/property proofなし
Packet Safety Gate completeness/inheritance proofなし
KDSL-Packet:=v2-draft adopted / non-executable''',
    '''common source-spanned parser/AST first slice:=main integrated
full YAML/KDSL semantic parserなし
full natural-language semantic parserなし
full negation parserなし
protected wording semantic equivalence lintなし
Safety Gate pairwise inheritance/aggregate:=integrated; multi-generation/deep scope未実装
R1C multiline JSON input:=common parser adapter integrated
R1C round-trip semantic proofなし
Packet validator first slice:=main integrated / 69 expectations verified
Packet full semantic parserなし
Packet normalization validator/mapper first slice:=main integrated / 93 expectations verified
Packet normalization structural round-trip first slice:=main integrated / 108 expectations verified
Packet normalization semantic/property proofなし
Packet Safety Gate completeness/inheritance proofなし
required KDSL Validation check:=workflow ready / repository setting pending issue #39
KDSL-Packet:=v2-draft adopted / non-executable''',
)
replace_once(
    'README.md',
    '''P0:
  Safety Gate protected wording/inheritance validator拡張

P1:
  R1C round-trip/property-based validator検討

P2:
  public-facing v2 overview
  CI required check / branch protection検討

Hold:
  v1.1.0 stable release
  tag/release/Release Assets操作''',
    '''P0:
  required KDSL Validation check activation / issue #39

P1:
  Phase 2 Safety Semantics / multi-generation inheritance / bounded protected-language model

P2:
  Phase 3 R1C deep optional-block round-trip / Evidence / Authority

P3:
  Phase 4 Packet / Normalization semantic-property proof

P4:
  Phase 5 public-facing v2 hardening / release-readiness review

Hold:
  v1.1.0 stable release
  tag/release/Release Assets操作''',
)

# Validator README.
replace_once(
    'tools/validator/README.md',
    '''## 現在の実装範囲

```text
r1_required_blocks.py:''',
    '''## 現在の実装範囲

```text
kdsl_parser.py / kdsl_parse.py:
  source-spanned Document/Envelope/Field AST
  field order/duplicate/tab diagnostics
  multiline JSON-compatible field capture
  block scalar/mapping/sequence/record adapters
  exact raw text retention

kdsl_parser_adapter.py:
  R1C/Packet/Normalization/Safety Gate input adapters
  semantic rules remain in each checker

r1_required_blocks.py:''',
)
replace_once(
    'tools/validator/README.md',
    '''kdsl_validate.py:
  target wrapper: r1 / prompt / compact / safety-gate / r1c / packet / normalization / all

run_samples.py:
  sample expectation runner''',
    '''kdsl_validate.py:
  common parser preflight
  target wrapper: r1 / prompt / compact / safety-gate / r1c / packet / normalization / all

run_all_samples.py:
  unified core/Safety Gate/R1C round-trip/parser runner
  missing summary or child-runner failure detection

run_parser_samples.py:
  parser/AST and adapter integration property runner

run_samples.py:
  core/Packet/Normalization expectation runner''',
)
replace_once(
    'tools/validator/README.md',
    '''R1C structural round-trip first slice integrated:
  existing suite: 108 / failed: 0
  Safety Gate suite: 14 / failed: 0
  R1C round-trip suite: 14 / failed: 0
  pull_request: 34
  workflow_run: 179 / success
```''',
    '''R1C structural round-trip first slice integrated:
  existing suite: 108 / failed: 0
  Safety Gate suite: 14 / failed: 0
  R1C round-trip suite: 14 / failed: 0
  pull_request: 34
  workflow_run: 179 / success

Common parser / unified validation Phase 1 integrated:
  core suite: 108 / failed: 0
  Safety Gate suite: 14 / failed: 0
  R1C round-trip suite: 14 / failed: 0
  parser/adapter suite: 11 / failed: 0
  unified total: 147 / failed: 0
  pull_request: 38
  workflow_run: 192 / success
  required-check activation: pending / issue #39
```''',
)
replace_once(
    'tools/validator/README.md',
    '''tools/validator/verification/kdsl_packet_roundtrip_verify.md
```''',
    '''tools/validator/verification/kdsl_packet_roundtrip_verify.md
tools/validator/verification/kdsl_common_parser_verify.md
```''',
)
replace_once(
    'tools/validator/README.md',
    '''Non-executable structural preview生成
EVIDENCEの観測/推論/未観測/未確認分離検査設計''',
    '''Non-executable structural preview生成
共通source-spanned parser/ASTによる入力解釈統一
multiline JSON-compatible R1C field処理
EVIDENCEの観測/推論/未観測/未確認分離検査設計''',
)
replace_once(
    'tools/validator/README.md',
    '''full parserとして扱わない
full YAML/JSON parserとして扱わない''',
    '''common parser first sliceをfull semantic parserとして扱わない
full YAML/KDSL semantic parserとして扱わない''',
)
replace_once(
    'tools/validator/README.md',
    '''  kdsl_validate.py
  kdsl_validate_usage.md
  run_samples.py''',
    '''  kdsl_parser.py
  kdsl_parse.py
  kdsl_parser_adapter.py
  kdsl_suite.py
  kdsl_validate.py
  kdsl_validate_usage.md
  run_all_samples.py
  run_parser_samples.py
  run_samples.py''',
)
replace_once(
    'tools/validator/README.md',
    '''inline JSON-compatible valueのみ
multi-line structured value未実装
Full R1 semantic validationの代替ではない''',
    '''inline/multiline JSON-compatible valueをcommon parserで結合
multiline JSON adapter検証済み
Full R1 semantic validationの代替ではない''',
)

# Wrapper usage.
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Run validator checks by target type so unrelated checks do not run against the wrong document class unless explicitly requested.''',
    '''Run a common parser preflight and then validator checks by target type so unrelated semantic checks do not run against the wrong document class unless explicitly requested.''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''## Default

```text
python tools/validator/kdsl_validate.py <file>
```''',
    '''## Parser preflight

For structured targets, the wrapper first parses known envelopes and reports duplicate fields, tab indentation, malformed JSON-compatible values, and source spans before semantic checkers run.

```text
python tools/validator/kdsl_parse.py --envelope KDSL_RESULT --json <file>
python tools/validator/kdsl_parse.py --envelope PACKET_DRAFT <file>
```

Parser success is not semantic validation or authority.

## Default

```text
python tools/validator/kdsl_validate.py <file>
```''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''full YAML parsing
full natural-language trigger parsing
full negation parsing
protected wording semantic equivalence
parent-child inheritance across documents
execution authority judgment''',
    '''full YAML/KDSL semantic parsing
full natural-language trigger parsing
full negation parsing
protected wording semantic equivalence
multi-generation inheritance graph/deep scope semantics
execution authority judgment''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''full JSON/YAML/KDSL parser
multi-line JSON objects
semantic equivalence proof''',
    '''full JSON/YAML/KDSL semantic parser
multiline JSON-compatible fields are parsed, but semantic equivalence is not proven
semantic equivalence proof''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Packet normalization round-trip first slice integrated:
  total: 108 / failed: 0
  pull_request: 27
  workflow_run: 163 / success
```''',
    '''Packet normalization round-trip first slice integrated:
  total: 108 / failed: 0
  pull_request: 27
  workflow_run: 163 / success

Common parser / unified validation Phase 1 integrated:
  component totals: 108 + 14 + 14 + 11
  unified total: 147 / failed: 0
  pull_request: 38
  workflow_run: 192 / success
```''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''tools/validator/verification/kdsl_packet_normalization_verify.md
```''',
    '''tools/validator/verification/kdsl_packet_normalization_verify.md
tools/validator/verification/kdsl_common_parser_verify.md
```''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''validator pass != RT:v''',
    '''parser preflight pass != semantic validation
validator pass != RT:v''',
)

# Changelog.
replace_once(
    'CHANGELOG.md',
    '''### Added

#### Packet normalization structural round-trip first slice''',
    '''### Added

#### Phase 1 common parser / unified validation foundation

- Added a source-spanned `DocumentNode` / `EnvelopeNode` / `FieldNode` AST.
- Added duplicate, tab-indentation, malformed multiline JSON, field-order, exact-text, and block-scalar handling.
- Migrated R1C, Packet, Packet Normalization, and Safety Gate input parsing through common adapters.
- Added `kdsl_parse.py`, parser/property samples, and `run_all_samples.py`.
- Replaced fragmented CI entrypoints with the stable read-only `KDSL Validation` check.
- Verified multiline R1C through parser CLI, semantic checker, and wrapper.

Verification:

```text
work_pull_request: 37 / closed unmerged
pull_request: 38
source_head: 9fe8912b39e5df1b31b85e3302dfda35351f25c0
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
workflow_run_id: 29177082691
run_number: 192
unified_total: 147
failed: 0
required_check_activation: pending / issue #39
```

#### Packet normalization structural round-trip first slice''',
)

# Project status.
replace_once('docs/project-status.md', 'last_updated: 2026-07-11', 'last_updated: 2026-07-12')
replace_once(
    'docs/project-status.md',
    '''## 3. Current architecture direction''',
    '''### PR #37 — Phase 1 common parser work branch

```yaml
pull_request: 37
merge_status: closed_unmerged
source_branch: agent/kdsl-common-parser-phase1-work
source_head: 58154edb350e61db5a4b39c9cc91f081f2caa439
superseded_by: 38
work_run_id: 29176973744
work_run_number: 189
baseline_conclusion: success
adapter_conclusion: success
reason: clean replacement after temporary write-enabled workflow
```

### PR #38 — Phase 1 common parser / unified validation foundation

```yaml
pull_request: 38
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-common-parser-phase1
source_head: 9fe8912b39e5df1b31b85e3302dfda35351f25c0
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
closeout_pull_request: 41
workflow: KDSL Validation
workflow_run_id: 29177082691
workflow_run_number: 192
job_id: 86608033032
workflow_conclusion: success
core_total: 108
safety_gate_total: 14
r1c_round_trip_total: 14
parser_adapter_total: 11
unified_total: 147
failed: 0
required_check_issue: 39
required_check_activation: pending
validator_authority: non_authoritative
stable_effect: none
```

## 3. Current architecture direction''',
)
replace_once(
    'docs/project-status.md',
    '''Validator CI baseline:=main統合済み
Safety Gate Registry:=v2-draft integrated''',
    '''Validator CI baseline:=main統合済み
Common parser/AST Phase 1:=main統合済み / 147 expectations verified
KDSL Validation unified check:=main統合済み / repository required setting pending issue #39
Safety Gate Registry:=v2-draft integrated''',
)
replace_once(
    'docs/project-status.md',
    'structured_values: JSON-compatible inline arrays/objects',
    'structured_values: JSON-compatible inline/multiline arrays/objects via common parser adapter',
)
replace_once(
    'docs/project-status.md',
    '''  implementation: partial
  authority: non_authoritative
  wrapper_targets:''',
    '''  implementation: partial
  authority: non_authoritative
  common_parser_ast: first_slice_integrated
  parser_adapters:
    - r1c
    - packet
    - normalization
    - safety-gate
  wrapper_targets:''',
)
replace_once(
    'docs/project-status.md',
    '''    - KDSL_RESULT required block presence lint''',
    '''    - source-spanned envelope/field AST and common parser diagnostics
    - multiline JSON-compatible value capture
    - common parser preflight / exact raw text retention
    - KDSL_RESULT required block presence lint''',
)
replace_once(
    'docs/project-status.md',
    '''  ci:
    workflow: .github/workflows/validator.yml
    command: python tools/validator/run_samples.py
    extension_command: python tools/validator/run_safety_gate_samples.py
    r1c_round_trip_command: python tools/validator/run_r1c_roundtrip_samples.py
    expected_sample_total: 108
    expected_safety_gate_extension_total: 14
    expected_r1c_round_trip_total: 14
    latest_pr_validation:
      pull_request: 34
      run_id: 29154476912
      run_number: 179
      conclusion: success
      sample_total: 108
      sample_failed: 0
      safety_gate_extension_total: 14
      safety_gate_extension_failed: 0
      r1c_round_trip_total: 14
      r1c_round_trip_failed: 0''',
    '''  ci:
    workflow: .github/workflows/validator.yml
    workflow_name: KDSL Validation
    required_check_name: KDSL Validation
    command: python tools/validator/run_all_samples.py
    component_commands:
      - python tools/validator/run_samples.py
      - python tools/validator/run_safety_gate_samples.py
      - python tools/validator/run_r1c_roundtrip_samples.py
      - python tools/validator/run_parser_samples.py
    expected_unified_total: 147
    required_check_activation: pending
    required_check_issue: 39
    latest_pr_validation:
      pull_request: 38
      run_id: 29177082691
      run_number: 192
      conclusion: success
      unified_total: 147
      failed: 0''',
)
replace_once(
    'docs/project-status.md',
    '''full natural-language trigger context parser
R1C multi-line JSON parsing
R1C full semantic equivalence proof''',
    '''full natural-language trigger context parser
common parser first slice integrated; full YAML/KDSL semantic parser未実装
R1C multiline JSON adapter integrated
R1C full semantic equivalence proof''',
)
replace_once(
    'docs/project-status.md',
    '''## 7. Safety and authority boundaries''',
    '''### Phase 1 common parser / unified validation

```yaml
pull_request: 38
source_head: 9fe8912b39e5df1b31b85e3302dfda35351f25c0
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
workflow: KDSL Validation
workflow_run_id: 29177082691
run_number: 192
job_id: 86608033032
conclusion: success
core_total: 108
safety_gate_total: 14
r1c_round_trip_total: 14
parser_adapter_total: 11
unified_total: 147
failed: 0
required_check_activation: pending
required_check_issue: 39
meaning: parser/structural regression evidence; not semantic-equivalence/safety/authority proof
```

## 7. Safety and authority boundaries''',
)
replace_once(
    'docs/project-status.md',
    '''tools/validator/verification/kdsl_packet_roundtrip_verify.md
''',
    '''tools/validator/verification/kdsl_packet_roundtrip_verify.md
tools/validator/verification/kdsl_common_parser_verify.md
''',
)
replace_once(
    'docs/project-status.md',
    '''full YAML/JSON/KDSL parserなし
full natural-language semantic parserなし''',
    '''common source-spanned parser/AST first slice統合済み
full YAML/KDSL semantic parserなし
full natural-language semantic parserなし''',
)
replace_once(
    'docs/project-status.md',
    'CI required check/branch protection未設定',
    'KDSL Validation workflow/check実装済み / required repository setting未設定 issue #39',
)
replace_once(
    'docs/project-status.md',
    '''P0: public-facing v2 overview / CI required check検討
P1: Safety Gate multi-generation inheritance/property tests検討
P2: R1C optional SAFETY_GATES dedicated round-trip検討
Hold: v1.1.0 stable / tag / release / Release Assets''',
    '''P0: required KDSL Validation check activation / issue #39
P1: Phase 2 Safety Semantics / multi-generation inheritance / bounded protected-language model
P2: Phase 3 R1C deep optional-block round-trip / Evidence / Authority
P3: Phase 4 Packet / Normalization semantic-property proof
P4: Phase 5 public-facing v2 hardening / release-readiness review
Hold: v1.1.0 stable / tag / release / Release Assets''',
)

# Review and activation runbook.
replace_once(
    'docs/reviews/kdsl-phase1-common-parser.md',
    '''status: branch-validation-pending
review_date: 2026-07-12
repository: tk999jp/kdsl-spec
base: main@ca258df765a93ac7e1fed64a2d845897c78fa7cd''',
    '''status: completed / merged
review_date: 2026-07-12
repository: tk999jp/kdsl-spec
base: main@ca258df765a93ac7e1fed64a2d845897c78fa7cd
work_pull_request: 37
pull_request: 38
source_head: 9fe8912b39e5df1b31b85e3302dfda35351f25c0
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
workflow_run_id: 29177082691
workflow_run_number: 192
job_id: 86608033032
workflow_conclusion: success
unified_total: 147
failed: 0
required_check_issue: 39
required_check_activation: pending''',
)
replace_once(
    'docs/reviews/kdsl-phase1-common-parser.md',
    '''## Non-actions''',
    '''## Integration result

```text
work PR #37:=closed without merge
clean PR #38:=squash merged
common parser adapters:=R1C/Packet/Normalization/Safety Gate
multiline R1C:=parser CLI + checker + wrapper pass
workflow/check:=KDSL Validation / contents:read
required-check repository setting:=pending issue #39
```

## Non-actions''',
)
replace_once(
    'docs/operations/ci-required-check.md',
    '''status: activation-pending
repository: tk999jp/kdsl-spec''',
    '''status: activation-pending
tracking_issue: 39
repository: tk999jp/kdsl-spec''',
)
replace_once(
    'docs/operations/ci-required-check.md',
    '''## Prerequisite

The workflow must have completed at least once on a pull request with this exact check name:''',
    '''## Prerequisite

Completed evidence:

```text
pull_request: 38
workflow_run: #192 / success
unified_total: 147 / failed 0
```

The workflow has completed with this exact check name:''',
)

# Verification record.
Path('tools/validator/verification/kdsl_common_parser_verify.md').write_text(
    '''# KDSL Common Parser / Unified Validation Verification

status: integrated / verified
verification_date: 2026-07-12
work_pull_request: 37
pull_request: 38
source_branch: agent/kdsl-common-parser-phase1
source_head: 9fe8912b39e5df1b31b85e3302dfda35351f25c0
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
workflow: KDSL Validation
workflow_run_id: 29177082691
workflow_run_number: 192
job_id: 86608033032
workflow_status: completed
workflow_conclusion: success

## Suite result

```text
core/Packet/Normalization: 108 / failed 0
Safety Gate extension: 14 / failed 0
R1C round-trip/property: 14 / failed 0
parser/AST + adapter integration: 11 / failed 0
unified total: 147 / failed 0
```

## Verified parser properties

```text
source line/column spans
field order and duplicate detection
tab-indentation rejection
multiline JSON-compatible value capture
block scalar capture
exact string retention
nested Safety Gate envelope parsing
R1C multiline JSON through CLI/checker/wrapper
major checker adapter regression preservation
```

## Required-check state

```text
workflow/check name: KDSL Validation
workflow permissions: contents read
repository required-check activation: pending
tracking issue: #39
```

## Boundary

```text
parser pass != semantic equivalence
parser pass != safety proof
parser pass != RT:v
parser pass != authority
parser pass != release readiness
workflow success != required-check repository setting
```
''',
    encoding='utf-8',
)

Path('.github/scripts/apply_phase1_closeout.py').unlink()
