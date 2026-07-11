from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


replace_once(
    'docs/project-status.md',
    '''### PR #18 — Packet normalization ownership work branch

```yaml
pull_request: 18
merge_status: work_branch_pending_close
source_branch: agent/kdsl-packet-normalization-ownership-work
superseded_by: 19
execution_effect: none
stable_effect: none
```''',
    '''### PR #18 — Packet normalization ownership work branch

```yaml
pull_request: 18
merge_status: closed_unmerged
source_branch: agent/kdsl-packet-normalization-ownership-work
source_head: 817762bfcdf3abb803d192eec4d12f2f366a7f07
superseded_by: 19
workflow_run_id: 29150276507
workflow_run_number: 135
sample_job_id: 86538556667
sample_conclusion: success
alignment_job_id: 86538556696
alignment_conclusion: success
execution_effect: none
stable_effect: none
```''',
)
replace_once(
    'docs/project-status.md',
    '''### PR #19 — Packet normalization v2-draft ownership alignment

```yaml
pull_request: 19
merge_status: pending
source_branch: agent/kdsl-packet-normalization-ownership
schema_id: kdsl-packet-normalization@0.1-draft
target_status: v2_draft_adopted_non_executable
validator_mapper: not_implemented
execution_effect: none
stable_effect: none
```''',
    '''### PR #19 — Packet normalization v2-draft ownership alignment

```yaml
pull_request: 19
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-packet-normalization-ownership
source_head: 7e938b603fe0edbe79306485804a1e09f98ed76d
squash_commit: 070b651a8d1088dd9698d0d9bd613fec3be84ef6
closeout_pull_request: 21
schema_id: kdsl-packet-normalization@0.1-draft
target_status: v2_draft_adopted_non_executable
validator_mapper: not_implemented
workflow_run_id: 29150351160
workflow_run_number: 137
sample_job_id: 86538743508
workflow_conclusion: success
sample_total: 69
sample_failed: 0
execution_effect: none
normalization_effect: none
stable_effect: none
```''',
)
replace_once(
    'docs/project-status.md',
    '''### Packet normalization design regression

```yaml
pull_request: 17''',
    '''### Packet normalization ownership

```yaml
work_pull_request: 18
pull_request: 19
source_head: 7e938b603fe0edbe79306485804a1e09f98ed76d
squash_commit: 070b651a8d1088dd9698d0d9bd613fec3be84ef6
work_run_id: 29150276507
work_run_number: 135
clean_run_id: 29150351160
clean_run_number: 137
conclusion: success
sample_total: 69
failed: 0
meaning: ownership/status alignment evidence; not normalization validator/mapper proof
```

### Packet normalization design regression

```yaml
pull_request: 17''',
)
replace_once(
    'docs/project-status.md',
    '''tools/validator/verification/kdsl_packet_verify.md
docs/reviews/kdsl-packet-validator-first-slice.md
docs/reviews/kdsl-r1c-design-integration.md''',
    '''tools/validator/verification/kdsl_packet_verify.md
docs/reviews/kdsl-packet-validator-first-slice.md
docs/reviews/kdsl-packet-normalization-design.md
docs/reviews/kdsl-packet-normalization-ownership.md
docs/reviews/kdsl-r1c-design-integration.md''',
)
replace_once(
    'docs/project-status.md',
    '''P0: PR #19 CI確認 / squash merge / normalization ownership closeout
P1: normalization validator/structural mapper first slice
P2: normalization round-trip/property tests
P3: Safety Gate protected wording/inheritance validator拡張
P4: R1C round-trip/property-based validator検討
P5: public-facing v2 overview / CI required check検討''',
    '''P0: normalization validator/structural mapper first slice
P1: normalization round-trip/property tests
P2: Safety Gate protected wording/inheritance validator拡張
P3: R1C round-trip/property-based validator検討
P4: public-facing v2 overview / CI required check検討''',
)

replace_once(
    'docs/reviews/kdsl-packet-normalization-ownership.md',
    '''status: merge-pending
review_date: 2026-07-11
work_pull_request: 18
pull_request: 19
target: main''',
    '''status: completed / merged
review_date: 2026-07-11
work_pull_request: 18
pull_request: 19
source_head: 7e938b603fe0edbe79306485804a1e09f98ed76d
squash_commit: 070b651a8d1088dd9698d0d9bd613fec3be84ef6
closeout_pull_request: 21
target: main''',
)
replace_once(
    'docs/reviews/kdsl-packet-normalization-ownership.md',
    '''## Evidence

```text
PR #17 design source: b11eac3b55853b240e850af5bc2f43bf5c7048b2
PR #17 squash: e27f130f64f0f0e9c3c6ac005adffc9476860f6f
Validator CI run #127: success / 69 expectations / failed 0
normalization source digests fixed
P1/P1L blocked examples reviewed
```''',
    '''## Evidence

```text
PR #17 design source: b11eac3b55853b240e850af5bc2f43bf5c7048b2
PR #17 squash: e27f130f64f0f0e9c3c6ac005adffc9476860f6f
Validator CI run #127: success / 69 expectations / failed 0
PR #18 work head: 817762bfcdf3abb803d192eec4d12f2f366a7f07
PR #18 run #135: alignment success / sample 69 / failed 0
PR #19 source: 7e938b603fe0edbe79306485804a1e09f98ed76d
PR #19 squash: 070b651a8d1088dd9698d0d9bd613fec3be84ef6
PR #19 run #137: success / sample 69 / failed 0
normalization source digests fixed
P1/P1L blocked examples reviewed
```''',
)

replace_once(
    'README.md',
    '''P0:
  PR #19 CI確認 / squash merge / normalization ownership closeout

P1:
  normalization validator/structural mapper first slice

P2:
  normalization round-trip/property tests

P3:
  Safety Gate protected wording/inheritance validator拡張

P4:
  R1C round-trip/property-based validator検討

P5:
  public-facing v2 overview
  CI required check / branch protection検討''',
    '''P0:
  normalization validator/structural mapper first slice

P1:
  normalization round-trip/property tests

P2:
  Safety Gate protected wording/inheritance validator拡張

P3:
  R1C round-trip/property-based validator検討

P4:
  public-facing v2 overview
  CI required check / branch protection検討''',
)

replace_once(
    'CHANGELOG.md',
    '''- Kept P1/P1L targets blocked while canonical target field schemas are absent.
- Kept `semantic_equivalence:not_proven` and `execution_authority:none` mandatory.

#### Packet normalization contract design candidate''',
    '''- Kept P1/P1L targets blocked while canonical target field schemas are absent.
- Kept `semantic_equivalence:not_proven` and `execution_authority:none` mandatory.

Verification:

```text
work_pull_request: 18
work_head: 817762bfcdf3abb803d192eec4d12f2f366a7f07
work_run: 29150276507 / #135 / alignment success / sample 69 / failed 0
pull_request: 19
source_head: 7e938b603fe0edbe79306485804a1e09f98ed76d
squash_commit: 070b651a8d1088dd9698d0d9bd613fec3be84ef6
clean_run: 29150351160 / #137 / success / sample 69 / failed 0
```

#### Packet normalization contract design candidate''',
)

Path('.github/scripts/apply_packet_normalization_closeout.py').unlink()
