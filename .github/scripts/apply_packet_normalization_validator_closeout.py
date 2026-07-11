from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


Path('tools/validator/verification/kdsl_packet_normalization_verify.md').write_text(
    '''# KDSL Packet Normalization Validator Verification

status: integrated / verified
verification_date: 2026-07-11
work_pull_request: 22
pull_request: 23
source_branch: agent/kdsl-packet-normalization-validator-clean
source_head: 40598b400d5a59d42b25ef05d8d280ae09182045
squash_commit: b3b95ee21f6a7829477185bcb5f4cd8fc0abe7a3
workflow: Validator CI
workflow_run_id: 29151175762
workflow_run_number: 150
job_id: 86540808942
workflow_status: completed
workflow_conclusion: success
sample_total: 93
sample_failed: 0

## Verified scope

```text
repository Full KDSL/P1/critical-loss normalization examples: pass
schema/status/source/target/authority/loss invalid samples: expected fail
wrapper normalization valid/invalid: expected exits
wrapper all valid normalization: pass
mapper Full KDSL: required preview markers / no executable KDSL_PROMPT:
mapper P1: blocked / marker:none / no P1: or KDSL_PROMPT:
invalid Packet mapper input: exit 2 / no normalization output
```

## Boundary

```text
mapper output != executable target
Packet normalize_state remains not_normalized
semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
validator/mapper pass != semantic equivalence
validator/mapper pass != safety proof
validator/mapper pass != round-trip proof
validator/mapper pass != RT:v
validator/mapper pass != execution authority
validator/mapper pass != release readiness
```
''',
    encoding='utf-8',
)

replace_once(
    'tools/validator/kdsl-packet-normalization-implementation-notes.md',
    'status: integration-candidate',
    'status: first-slice integrated',
)
replace_once(
    'tools/validator/kdsl-packet-normalization-implementation-notes.md',
    '## Boundaries\n',
    '''## Integration evidence

```text
work_pull_request: 22
pull_request: 23
source_head: 40598b400d5a59d42b25ef05d8d280ae09182045
squash_commit: b3b95ee21f6a7829477185bcb5f4cd8fc0abe7a3
workflow_run_id: 29151175762
run_number: 150
sample_total: 93
failed: 0
```

## Boundaries
''',
)
replace_once(
    'tools/validator/samples/normalization_expected_results.md',
    'status: first-slice candidate\nexpected_total_suite: 93',
    'status: first-slice verified\nverified_total_suite: 93\nfailed: 0',
)
replace_once(
    'tools/validator/samples/normalization_expected_results.md',
    'mapper invalid Packet: no normalization output / exit 2\n```',
    '''mapper invalid Packet: no normalization output / exit 2
```

Verification:

```text
pull_request: 23
workflow_run_id: 29151175762
run_number: 150
sample_total: 93
failed: 0
```''',
)

replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'validator: first-slice integration pending',
    'validator: first-slice integrated',
)
replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    '''normalization validator: first-slice integration pending
normalization mapper: first-slice integration pending
round-trip property tests: not implemented''',
    '''normalization validator: first-slice integrated
normalization mapper: first-slice integrated / non-executable preview only
round-trip property tests: not implemented''',
)
replace_once(
    'spec/packet/README.md',
    'validator/mapper: first-slice integration pending',
    'validator/mapper: first-slice integrated / non-executable preview only',
)

replace_once(
    'tools/validator/README.md',
    '''Packet normalization first slice candidate:
  expected total: 93 / branch validation pending''',
    '''Packet normalization first slice integrated:
  total: 93 / failed: 0
  pull_request: 23
  workflow_run: 150 / success''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Packet normalization first slice candidate:
  expected total: 93 / branch validation pending''',
    '''Packet normalization first slice integrated:
  total: 93 / failed: 0
  pull_request: 23
  workflow_run: 150 / success''',
)

replace_once(
    'README.md',
    '''Packet normalization validator/mapper: first-slice integration pending
validator sample suite: 93 expectations candidate''',
    '''Packet normalization validator/mapper: first-slice integrated / non-executable preview only
validator sample suite: 93 expectations / failed 0''',
)
replace_once(
    'README.md',
    'Packet normalization validator/mapper first slice:=integration pending\nPacket normalization round-trip/property proofなし',
    'Packet normalization validator/mapper first slice:=main integrated / 93 expectations verified\nPacket normalization round-trip/property proofなし',
)
replace_once(
    'README.md',
    '''P0:
  PR #23 CI確認 / squash merge / normalization validator closeout

P1:
  normalization round-trip/property tests

P2:
  Safety Gate protected wording/inheritance validator拡張

P3:
  R1C round-trip/property-based validator検討

P4:
  public-facing v2 overview
  CI required check / branch protection検討''',
    '''P0:
  normalization round-trip/property tests

P1:
  Safety Gate protected wording/inheritance validator拡張

P2:
  R1C round-trip/property-based validator検討

P3:
  public-facing v2 overview
  CI required check / branch protection検討''',
)

replace_once(
    'CHANGELOG.md',
    '''- Kept executable `KDSL_PROMPT:`, P1, and P1L generation prohibited.
- Kept Packet state `not_normalized`, `semantic_equivalence:not_proven`, and `execution_authority:none`.

#### Packet normalization v2-draft ownership alignment''',
    '''- Kept executable `KDSL_PROMPT:`, P1, and P1L generation prohibited.
- Kept Packet state `not_normalized`, `semantic_equivalence:not_proven`, and `execution_authority:none`.

Verification:

```text
work_pull_request: 22
work_head: bd74e883f01b3ae5888c4327f29765521dfcd2fb
pull_request: 23
source_head: 40598b400d5a59d42b25ef05d8d280ae09182045
squash_commit: b3b95ee21f6a7829477185bcb5f4cd8fc0abe7a3
workflow_run_id: 29151175762
run_number: 150
sample_total: 93
failed: 0
```

#### Packet normalization v2-draft ownership alignment''',
)

replace_once(
    'docs/project-status.md',
    '''### PR #22 — Packet normalization validator / mapper work branch

```yaml
pull_request: 22
merge_status: pending
source_branch: agent/kdsl-packet-normalization-validator
checker: tools/validator/kdsl_packet_normalization.py
mapper: tools/validator/kdsl_packet_normalize.py
wrapper_target: normalization
expected_sample_total: 93
validator_authority: non_authoritative
executable_output: no
normalization_effect: none
stable_effect: none
```''',
    '''### PR #22 — Packet normalization validator / mapper work branch

```yaml
pull_request: 22
merge_status: closed_unmerged
source_branch: agent/kdsl-packet-normalization-validator
source_head: bd74e883f01b3ae5888c4327f29765521dfcd2fb
superseded_by: 23
checker: tools/validator/kdsl_packet_normalization.py
mapper: tools/validator/kdsl_packet_normalize.py
wrapper_target: normalization
validator_authority: non_authoritative
executable_output: no
normalization_effect: none
stable_effect: none
```

### PR #23 — Packet normalization validator / mapper first slice

```yaml
pull_request: 23
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-packet-normalization-validator-clean
source_head: 40598b400d5a59d42b25ef05d8d280ae09182045
squash_commit: b3b95ee21f6a7829477185bcb5f4cd8fc0abe7a3
closeout_pull_request: 25
checker: tools/validator/kdsl_packet_normalization.py
mapper: tools/validator/kdsl_packet_normalize.py
wrapper_target: normalization
workflow_run_id: 29151175762
workflow_run_number: 150
job_id: 86540808942
workflow_conclusion: success
sample_total: 93
sample_failed: 0
validator_authority: non_authoritative
executable_output: no
normalization_effect: none
semantic_equivalence: not_proven
stable_effect: none
```''',
)
replace_once(
    'docs/project-status.md',
    'Packet normalization validator/mapper first slice:=integration pending',
    'Packet normalization validator/mapper first slice:=main統合済み / 93 expectations verified',
)
replace_once(
    'docs/project-status.md',
    '  normalization_validator_mapper: first_slice_integration_pending',
    '  normalization_validator_mapper: first_slice_integrated_non_executable',
)
replace_once(
    'docs/project-status.md',
    '''      pull_request: 14
      run_id: 29148894965
      run_number: 116
      conclusion: success
      sample_total: 69
      sample_failed: 0''',
    '''      pull_request: 23
      run_id: 29151175762
      run_number: 150
      conclusion: success
      sample_total: 93
      sample_failed: 0''',
)
replace_once(
    'docs/project-status.md',
    '''Packet Safety Gate state/evidence deep lint
Normalization validator/mapper first slice:=integration pending
Normalization round-trip/property proofなし
Packet Safety Gate completeness/inheritance proof''',
    '''Packet Safety Gate state/evidence deep lint
Normalization round-trip/property proofなし
Packet Safety Gate completeness/inheritance proof''',
)
replace_once(
    'docs/project-status.md',
    '''### Packet normalization validator / mapper candidate

```yaml
pull_request: 22
branch: agent/kdsl-packet-normalization-validator
expected_sample_total: 93
status: branch_validation_pending
meaning: first-slice heuristic/preview candidate; not semantic-equivalence/round-trip/execution proof
```''',
    '''### Packet normalization validator / mapper first slice

```yaml
work_pull_request: 22
pull_request: 23
source_branch: agent/kdsl-packet-normalization-validator-clean
source_head: 40598b400d5a59d42b25ef05d8d280ae09182045
squash_commit: b3b95ee21f6a7829477185bcb5f4cd8fc0abe7a3
workflow_run_id: 29151175762
run_number: 150
job_id: 86540808942
conclusion: success
sample_total: 93
failed: 0
mapper_full_kdsl: non_executable_preview
mapper_p1: blocked_no_preview
meaning: first-slice heuristic/preview evidence; not semantic-equivalence/round-trip/execution proof
```''',
)
replace_once(
    'docs/project-status.md',
    '''tools/validator/verification/kdsl_packet_verify.md
docs/reviews/kdsl-packet-validator-first-slice.md''',
    '''tools/validator/verification/kdsl_packet_verify.md
tools/validator/verification/kdsl_packet_normalization_verify.md
docs/reviews/kdsl-packet-validator-first-slice.md
docs/reviews/kdsl-packet-normalization-validator-first-slice.md''',
)
replace_once(
    'docs/project-status.md',
    '''Packet full YAML/semantic parserなし
Normalization validator/mapper first slice:=integration pending
Normalization round-trip/property proofなし''',
    '''Packet full YAML/semantic parserなし
Normalization round-trip/property proofなし''',
)
replace_once(
    'docs/project-status.md',
    '''P0: PR #23 CI確認 / squash merge / normalization validator closeout
P1: normalization round-trip/property tests
P2: Safety Gate protected wording/inheritance validator拡張
P3: R1C round-trip/property-based validator検討
P4: public-facing v2 overview / CI required check検討''',
    '''P0: normalization round-trip/property tests
P1: Safety Gate protected wording/inheritance validator拡張
P2: R1C round-trip/property-based validator検討
P3: public-facing v2 overview / CI required check検討''',
)

Path('docs/reviews/kdsl-packet-normalization-validator-first-slice.md').write_text(
    '''# KDSL Packet Normalization Validator / Mapper First Slice

status: completed / merged
review_date: 2026-07-11
work_pull_request: 22
pull_request: 23
source_branch: agent/kdsl-packet-normalization-validator-clean
source_head: 40598b400d5a59d42b25ef05d8d280ae09182045
squash_commit: b3b95ee21f6a7829477185bcb5f4cd8fc0abe7a3
closeout_pull_request: 25

## Scope

```text
tools/validator/kdsl_packet_normalization.py
tools/validator/kdsl_packet_normalize.py
--target normalization
--target all normalization integration
93-case expectation suite
```

## Verification

```text
workflow_run_id: 29151175762
run_number: 150
job_id: 86540808942
conclusion: success
sample_total: 93
failed: 0
mapper Full KDSL:=KDSL_PROMPT_PREVIEW / exit 0
mapper P1:=blocked / marker:none / exit 1
invalid Packet:=no normalization output / exit 2
```

## Boundary

```text
mapper output != executable target
KDSL_PROMPT:生成なし
P1/P1L生成なし
Packet state normalized化なし
semantic_equivalence:not_proven
execution_authority:none
validator/mapper pass != semantic equivalence/safety proof/round-trip proof/RT:v/authority/release readiness
```

## Non-actions

```text
Packet executable化なし
normalization completion claimなし
tag/release/Release Assets操作なし
stable/public-ready化なし
source branch削除なし
```
''',
    encoding='utf-8',
)

Path('.github/scripts/apply_packet_normalization_validator_closeout.py').unlink()
