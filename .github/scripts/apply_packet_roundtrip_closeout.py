from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


Path('tools/validator/verification/kdsl_packet_roundtrip_verify.md').write_text(
    '''# KDSL Packet Normalization Round-Trip Verification

status: integrated / verified
verification_date: 2026-07-11
work_pull_request: 26
pull_request: 27
source_branch: agent/kdsl-packet-normalization-roundtrip-clean
source_head: 478157b5059aac0304a8bdde1be6cae192c367c0
squash_commit: 82397678cf939df80df35d5e075be9556dae0fc3
workflow: Validator CI
workflow_run_id: 29151860435
workflow_run_number: 163
job_id: 86542493448
workflow_status: completed
workflow_conclusion: success
sample_total: 108
sample_failed: 0

## Verified scope

```text
Full KDSL generated round-trip: structural_pass / exit 0
P1 generated round-trip: blocked / exit 1
invalid Packet: fail / exit 2
source/digest mismatch: fail
exact-string/protected-wording loss: fail
preserved/preview order mutation: fail
authority widening: fail
MAP omission: fail
result-schema loss: fail
semantic-equivalence claim: fail
executable target marker: fail
```

## Boundary

```text
structural_pass != semantic equivalence
structural_pass != complete safety proof
structural_pass != normalization completion
structural_pass != RT:v
structural_pass != execution authority
structural_pass != release readiness
```
''',
    encoding='utf-8',
)

replace_once(
    'tools/validator/kdsl-packet-roundtrip-implementation-notes.md',
    'status: integration-candidate',
    'status: first-slice integrated',
)
replace_once(
    'tools/validator/kdsl-packet-roundtrip-implementation-notes.md',
    '## Boundaries\n',
    '''## Integration evidence

```text
work_pull_request: 26
pull_request: 27
source_head: 478157b5059aac0304a8bdde1be6cae192c367c0
squash_commit: 82397678cf939df80df35d5e075be9556dae0fc3
workflow_run_id: 29151860435
run_number: 163
sample_total: 108
failed: 0
```

## Boundaries
''',
)
replace_once(
    'tools/validator/samples/roundtrip_expected_results.md',
    'status: first-slice candidate\nexpected_total_suite: 108',
    'status: first-slice verified\nverified_total_suite: 108\nfailed: 0',
)
replace_once(
    'tools/validator/samples/roundtrip_expected_results.md',
    'semantic claim/executable marker: fail\n```',
    '''semantic claim/executable marker: fail
```

Verification:

```text
pull_request: 27
workflow_run_id: 29151860435
run_number: 163
sample_total: 108
failed: 0
```''',
)

replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'round-trip property tests: first-slice integration pending',
    'round-trip property tests: first-slice integrated / selected structural properties only',
)
replace_once(
    'tools/validator/README.md',
    '''Packet normalization round-trip first slice candidate:
  expected total: 108 / branch validation pending''',
    '''Packet normalization round-trip first slice integrated:
  total: 108 / failed: 0
  pull_request: 27
  workflow_run: 163 / success''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Packet normalization round-trip first slice candidate:
  expected total: 108 / branch validation pending''',
    '''Packet normalization round-trip first slice integrated:
  total: 108 / failed: 0
  pull_request: 27
  workflow_run: 163 / success''',
)

replace_once(
    'README.md',
    '''Packet normalization structural round-trip: first-slice integration pending
validator sample suite: 108 expectations candidate''',
    '''Packet normalization structural round-trip: first-slice integrated / selected structural properties only
validator sample suite: 108 expectations / failed 0''',
)
replace_once(
    'README.md',
    'Packet normalization structural round-trip first slice:=integration pending\nPacket normalization semantic/property proofなし',
    'Packet normalization structural round-trip first slice:=main integrated / 108 expectations verified\nPacket normalization semantic/property proofなし',
)
replace_once(
    'README.md',
    '''P0:
  PR #27 CI確認 / squash merge / round-trip closeout

P1:
  Safety Gate protected wording/inheritance validator拡張

P2:
  R1C round-trip/property-based validator検討

P3:
  public-facing v2 overview
  CI required check / branch protection検討''',
    '''P0:
  Safety Gate protected wording/inheritance validator拡張

P1:
  R1C round-trip/property-based validator検討

P2:
  public-facing v2 overview
  CI required check / branch protection検討''',
)

replace_once(
    'CHANGELOG.md',
    '''- Expanded the candidate suite from 93 to 108 expectations.
- Kept `semantic_equivalence:not_proven`, `execution_authority:none`, and non-executable output fixed.

#### Packet normalization validator / mapper first slice''',
    '''- Expanded the candidate suite from 93 to 108 expectations.
- Kept `semantic_equivalence:not_proven`, `execution_authority:none`, and non-executable output fixed.

Verification:

```text
work_pull_request: 26
work_head: edbfa65c5672f90e2c084c83289c2aeffc95ed1d
pull_request: 27
source_head: 478157b5059aac0304a8bdde1be6cae192c367c0
squash_commit: 82397678cf939df80df35d5e075be9556dae0fc3
workflow_run_id: 29151860435
run_number: 163
sample_total: 108
failed: 0
```

#### Packet normalization validator / mapper first slice''',
)

replace_once(
    'docs/project-status.md',
    '''### PR #26 — Packet normalization structural round-trip work branch

```yaml
pull_request: 26
merge_status: pending
source_branch: agent/kdsl-packet-normalization-roundtrip
tool: tools/validator/kdsl_packet_roundtrip.py
expected_sample_total: 108
status_model: structural_pass|blocked|fail
semantic_equivalence: not_proven
execution_authority: none
stable_effect: none
```''',
    '''### PR #26 — Packet normalization structural round-trip work branch

```yaml
pull_request: 26
merge_status: closed_unmerged
source_branch: agent/kdsl-packet-normalization-roundtrip
source_head: edbfa65c5672f90e2c084c83289c2aeffc95ed1d
superseded_by: 27
tool: tools/validator/kdsl_packet_roundtrip.py
status_model: structural_pass|blocked|fail
semantic_equivalence: not_proven
execution_authority: none
stable_effect: none
```

### PR #27 — Packet normalization structural round-trip first slice

```yaml
pull_request: 27
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-packet-normalization-roundtrip-clean
source_head: 478157b5059aac0304a8bdde1be6cae192c367c0
squash_commit: 82397678cf939df80df35d5e075be9556dae0fc3
closeout_pull_request: 29
tool: tools/validator/kdsl_packet_roundtrip.py
workflow_run_id: 29151860435
workflow_run_number: 163
job_id: 86542493448
workflow_conclusion: success
sample_total: 108
sample_failed: 0
status_model: structural_pass|blocked|fail
semantic_equivalence: not_proven
execution_authority: none
normalization_effect: none
stable_effect: none
```''',
)
replace_once(
    'docs/project-status.md',
    'Packet normalization structural round-trip first slice:=integration pending',
    'Packet normalization structural round-trip first slice:=main統合済み / 108 expectations verified',
)
replace_once(
    'docs/project-status.md',
    '''      pull_request: 23
      run_id: 29151175762
      run_number: 150
      conclusion: success
      sample_total: 93
      sample_failed: 0''',
    '''      pull_request: 27
      run_id: 29151860435
      run_number: 163
      conclusion: success
      sample_total: 108
      sample_failed: 0''',
)
replace_once(
    'docs/project-status.md',
    '''Packet Safety Gate state/evidence deep lint
Normalization structural round-trip first slice:=integration pending
Normalization semantic/property proofなし
Packet Safety Gate completeness/inheritance proof''',
    '''Packet Safety Gate state/evidence deep lint
Normalization semantic/property proofなし
Packet Safety Gate completeness/inheritance proof''',
)
replace_once(
    'docs/project-status.md',
    '''### Packet normalization structural round-trip candidate

```yaml
pull_request: 26
branch: agent/kdsl-packet-normalization-roundtrip
expected_sample_total: 108
status: branch_validation_pending
meaning: selected structural properties only; not semantic-equivalence/safety/normalization proof
```''',
    '''### Packet normalization structural round-trip first slice

```yaml
work_pull_request: 26
pull_request: 27
source_branch: agent/kdsl-packet-normalization-roundtrip-clean
source_head: 478157b5059aac0304a8bdde1be6cae192c367c0
squash_commit: 82397678cf939df80df35d5e075be9556dae0fc3
workflow_run_id: 29151860435
run_number: 163
job_id: 86542493448
conclusion: success
sample_total: 108
failed: 0
full_kdsl: structural_pass
p1_p1l: blocked
meaning: selected structural properties only; not semantic-equivalence/safety/normalization proof
```''',
)
replace_once(
    'docs/project-status.md',
    '''tools/validator/verification/kdsl_packet_normalization_verify.md
docs/reviews/kdsl-packet-validator-first-slice.md''',
    '''tools/validator/verification/kdsl_packet_normalization_verify.md
tools/validator/verification/kdsl_packet_roundtrip_verify.md
docs/reviews/kdsl-packet-validator-first-slice.md
docs/reviews/kdsl-packet-roundtrip-first-slice.md''',
)
replace_once(
    'docs/project-status.md',
    '''Packet full YAML/semantic parserなし
Normalization structural round-trip first slice:=integration pending
Normalization semantic/property proofなし''',
    '''Packet full YAML/semantic parserなし
Normalization semantic/property proofなし''',
)
replace_once(
    'docs/project-status.md',
    '''P0: PR #27 CI確認 / squash merge / round-trip closeout
P1: Safety Gate protected wording/inheritance validator拡張
P2: R1C round-trip/property-based validator検討
P3: public-facing v2 overview / CI required check検討''',
    '''P0: Safety Gate protected wording/inheritance validator拡張
P1: R1C round-trip/property-based validator検討
P2: public-facing v2 overview / CI required check検討''',
)

Path('docs/reviews/kdsl-packet-roundtrip-first-slice.md').write_text(
    '''# KDSL Packet Normalization Structural Round-Trip First Slice

status: completed / merged
review_date: 2026-07-11
work_pull_request: 26
pull_request: 27
source_branch: agent/kdsl-packet-normalization-roundtrip-clean
source_head: 478157b5059aac0304a8bdde1be6cae192c367c0
squash_commit: 82397678cf939df80df35d5e075be9556dae0fc3
closeout_pull_request: 29

## Scope

```text
tools/validator/kdsl_packet_roundtrip.py
108-case expectation suite
source digest/MAP/exact strings/protected wording/order/authority/result schema
Full KDSL structural_pass
P1/P1L blocked
```

## Verification

```text
workflow_run_id: 29151860435
run_number: 163
job_id: 86542493448
conclusion: success
sample_total: 108
failed: 0
```

## Boundary

```text
structural_pass != semantic equivalence
structural_pass != complete safety proof
structural_pass != normalization completion
structural_pass != RT:v
structural_pass != execution authority
structural_pass != release readiness
```

## Non-actions

```text
executable KDSL_PROMPT/P1/P1L生成なし
Packet normalized化なし
semantic equivalence claimなし
tag/release/Release Assets操作なし
stable/public-ready化なし
source branch削除なし
```
''',
    encoding='utf-8',
)

Path('.github/scripts/apply_packet_roundtrip_closeout.py').unlink()
