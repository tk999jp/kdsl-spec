from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


# Verification record becomes the authoritative branch/CI evidence note.
Path('tools/validator/verification/kdsl_packet_verify.md').write_text(
    '''# KDSL Packet Validator Verification

status: integrated / verified
verification_date: 2026-07-11
pull_request: 14
source_branch: agent/kdsl-packet-validator-clean
source_head: 9cde7e5a13861a9f7c6f1c05b20d23d023f66025
squash_commit: f1bba2206d28f0ce3cbc1643738d306c940537f6
workflow: Validator CI
workflow_run_id: 29148894965
workflow_run_number: 116
job_id: 86535040415
workflow_status: completed
workflow_conclusion: success
sample_total: 69
sample_failed: 0

## Verified scope

```text
Packet repository example: pass
baseline valid Packet: pass
invalid/warn/out-of-scope direct cases: expected exits
wrapper --target packet valid/invalid: expected exits
wrapper --target all valid Packet: pass
legacy R1 negative samples: preserved
```

## Integration history

```text
PR #13:=closed without merge / temporary workflow history
PR #14:=clean integration / squash merged
Packet scope correction:=protective wording outside PACKET_DRAFT excluded from actual-use checks
R1 checker envelope separation:=KDSL_RESULT未検出→pass/info
```

## Boundary

```text
validator未実行→pass扱禁止
Packet validator pass != semantic equivalence
Packet validator pass != safety proof
Packet validator pass != normalization proof
Packet validator pass != RT:v
Packet validator pass != authority
Packet validator pass != executable readiness
Packet validator pass != release readiness
```
''',
    encoding='utf-8',
)

# Implementation notes and expected-results record.
replace_once(
    'tools/validator/kdsl-packet-implementation-notes.md',
    'status: implementation-candidate',
    'status: first-slice integrated',
)
replace_once(
    'tools/validator/kdsl-packet-implementation-notes.md',
    '## Boundaries\n',
    '''## Integration evidence

```text
pull_request: 14
source_head: 9cde7e5a13861a9f7c6f1c05b20d23d023f66025
squash_commit: f1bba2206d28f0ce3cbc1643738d306c940537f6
workflow_run_id: 29148894965
run_number: 116
sample_total: 69
failed: 0
```

## Boundaries
''',
)
replace_once(
    'tools/validator/samples/packet_expected_results.md',
    'status: first-slice candidate',
    'status: first-slice verified',
)
replace_once(
    'tools/validator/samples/packet_expected_results.md',
    'wrapper all valid Packet: pass\n```',
    '''wrapper all valid Packet: pass
```

Verification:

```text
pull_request: 14
workflow_run_id: 29148894965
run_number: 116
sample_total: 69
failed: 0
```''',
)

# Validator documentation.
replace_once(
    'tools/validator/README.md',
    '''Packet first slice candidate:
  expected total: 69 / branch validation pending''',
    '''Packet first slice integrated:
  total: 69 / failed: 0
  pull_request: 14
  workflow_run: 116 / success''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Packet first slice candidate:
  expected total: 69 / branch validation pending''',
    '''Packet first slice integrated:
  total: 69 / failed: 0
  pull_request: 14
  workflow_run: 116 / success''',
)

# Root README current state/evidence/next phase.
replace_once(
    'README.md',
    '''Packet validator: first heuristic slice integration pending
validator sample suite: 69 expectations candidate''',
    '''Packet validator: first heuristic slice integrated
validator sample suite: 69 expectations / failed 0''',
)
replace_once(
    'README.md',
    '''sample expectations: 49
failed: 0
workflow: .github/workflows/validator.yml
latest R1C PR run: #50 / success''',
    '''sample expectations: 69
failed: 0
workflow: .github/workflows/validator.yml
latest Packet PR: #14
latest Packet run: #116 / success''',
)
replace_once(
    'README.md',
    'Packet validator first slice:=integration pending',
    'Packet validator first slice:=main integrated / 69 expectations verified',
)
replace_once(
    'README.md',
    '''P0:
  PR #13 CI確認 / squash merge / Packet validator closeout''',
    '''P0:
  PR #16 CI確認 / squash merge / Packet validator closeout''',
)

# Changelog integration evidence and current boundary.
replace_once(
    'CHANGELOG.md',
    '''- Packet execution/normalization readiness remains explicitly out of scope.

#### Packet v2-draft ownership alignment''',
    '''- Packet execution/normalization readiness remains explicitly out of scope.

Verification:

```text
pull_request: 14
source_head: 9cde7e5a13861a9f7c6f1c05b20d23d023f66025
squash_commit: f1bba2206d28f0ce3cbc1643738d306c940537f6
workflow_run_id: 29148894965
run_number: 116
sample_total: 69
failed: 0
```

Integration note:

```text
PR #13:=closed without merge / superseded by clean PR #14
Packet scope correction:=integrated
R1 checker envelope separation:=integrated
```

#### Packet v2-draft ownership alignment''',
)
replace_once(
    'CHANGELOG.md',
    '''Packet lint:=v2-draft adopted / validator first slice integration pending
Packet sample suite:=69 expectations candidate''',
    '''Packet lint:=v2-draft adopted / validator first slice integrated
Packet sample suite:=69 expectations / failed 0''',
)

# Operational status: PR history, current state, latest CI, evidence, next phase.
replace_once(
    'docs/project-status.md',
    '''### PR #13 — Packet validator first slice

```yaml
pull_request: 13
merge_status: pending
source_branch: agent/kdsl-packet-validator
checker: tools/validator/kdsl_packet.py
wrapper_target: packet
expected_sample_total: 69
validator_authority: non_authoritative
packet_execution_effect: none
stable_effect: none
```''',
    '''### PR #13 — Packet validator integration work branch

```yaml
pull_request: 13
merge_status: closed_unmerged
source_branch: agent/kdsl-packet-validator
superseded_by: 14
reason: temporary workflow integration history / clean replacement
checker: tools/validator/kdsl_packet.py
packet_execution_effect: none
stable_effect: none
```

### PR #14 — Packet validator first slice

```yaml
pull_request: 14
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-packet-validator-clean
source_head: 9cde7e5a13861a9f7c6f1c05b20d23d023f66025
squash_commit: f1bba2206d28f0ce3cbc1643738d306c940537f6
closeout_pull_request: 16
checker: tools/validator/kdsl_packet.py
wrapper_target: packet
workflow_run_id: 29148894965
workflow_run_number: 116
job_id: 86535040415
workflow_conclusion: success
sample_total: 69
sample_failed: 0
validator_authority: non_authoritative
packet_execution_effect: none
normalization_effect: none
stable_effect: none
```''',
)
replace_once(
    'docs/project-status.md',
    'Packet validator first slice:=integration pending',
    'Packet validator first slice:=main統合済み / 69 expectations verified',
)
replace_once(
    'docs/project-status.md',
    '  validator: first_slice_integration_pending',
    '  validator: first_slice_integrated',
)
replace_once(
    'docs/project-status.md',
    '''    latest_pr_validation:
      pull_request: 7
      run_id: 29144196401
      run_number: 50
      conclusion: success''',
    '''    latest_pr_validation:
      pull_request: 14
      run_id: 29148894965
      run_number: 116
      conclusion: success
      sample_total: 69
      sample_failed: 0''',
)
replace_once(
    'docs/project-status.md',
    '''### Packet validator candidate

```yaml
pull_request: 13
branch: agent/kdsl-packet-validator
expected_sample_total: 69
status: branch_validation_pending
meaning: Packet first-slice heuristic candidate; not Packet execution/normalization proof
```''',
    '''### Packet validator first slice

```yaml
pull_request: 14
source_branch: agent/kdsl-packet-validator-clean
source_head: 9cde7e5a13861a9f7c6f1c05b20d23d023f66025
squash_commit: f1bba2206d28f0ce3cbc1643738d306c940537f6
workflow_run_id: 29148894965
run_number: 116
job_id: 86535040415
conclusion: success
sample_total: 69
failed: 0
repository_example: pass
wrapper_packet_valid_invalid: expected exits
wrapper_all_valid_packet: pass
meaning: first-slice heuristic evidence; not Packet execution/normalization proof
```''',
)
replace_once(
    'docs/project-status.md',
    '''tools/validator/verification/kdsl_r1c_verify.md
docs/reviews/kdsl-r1c-design-integration.md''',
    '''tools/validator/verification/kdsl_r1c_verify.md
tools/validator/verification/kdsl_packet_verify.md
docs/reviews/kdsl-packet-validator-first-slice.md
docs/reviews/kdsl-r1c-design-integration.md''',
)
replace_once(
    'docs/project-status.md',
    'Packet validator first slice:=integration pending\n',
    '',
)
replace_once(
    'docs/project-status.md',
    'P0: PR #13 CI確認 / squash merge / Packet validator closeout',
    'P0: PR #16 CI確認 / squash merge / Packet validator closeout',
)

# Completed integration review.
Path('docs/reviews/kdsl-packet-validator-first-slice.md').write_text(
    '''# KDSL Packet Validator First Slice

status: completed / merged
review_date: 2026-07-11
pull_request: 14
source_branch: agent/kdsl-packet-validator-clean
source_head: 9cde7e5a13861a9f7c6f1c05b20d23d023f66025
squash_commit: f1bba2206d28f0ce3cbc1643738d306c940537f6
closeout_pull_request: 16

## Scope

```text
tools/validator/kdsl_packet.py
--target packet
--target all Packet integration
69-case expectation suite
CompactPrompt Packet-boundary synchronization
R1 checker KDSL_RESULT envelope separation
```

## Verification

```text
workflow: Validator CI
workflow_run_id: 29148894965
run_number: 116
job_id: 86535040415
conclusion: success
sample_total: 69
failed: 0
Packet repository example: pass
wrapper packet valid/invalid: expected exits
wrapper all valid Packet: pass
```

## Integration history

```text
PR #13:=closed without merge
reason:=temporary workflow integration history
PR #14:=clean replacement / squash merged
Packet scope correction:=protective wording outside PACKET_DRAFT excluded
R1 envelope separation:=KDSL_RESULT未検出→pass/info
```

## Validation boundary

```text
line-based heuristic parser
first PACKET_DRAFT block only
full YAML/semantic parserなし
Safety Gate state/evidence deep lintなし
normalization transformer/round-trip proofなし
validator pass != semantic equivalence
validator pass != safety proof
validator pass != normalization proof
validator pass != RT:v
validator pass != authority/executable readiness/release readiness
```

## Non-actions

```text
Packet executable化なし
NORMALIZE.state変更なし
PKT:v1有効化なし
canonical/stable昇格なし
tag/release/Release Assets操作なし
source branch削除なし
```
''',
    encoding='utf-8',
)

Path('.github/scripts/apply_packet_validator_closeout.py').unlink()
