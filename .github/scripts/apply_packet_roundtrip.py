import subprocess
import sys
from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


root = Path('tools/validator')
samples = root / 'samples'
source_path = Path('examples/packet/normalization-source.example.md')
mapper = root / 'kdsl_packet_normalize.py'
mapper_run = subprocess.run(
    [sys.executable, str(mapper), str(source_path)],
    text=True,
    capture_output=True,
)
if mapper_run.returncode != 0:
    raise SystemExit('baseline mapper failed: ' + (mapper_run.stderr or mapper_run.stdout))
normalization = mapper_run.stdout
(samples / 'sample_roundtrip_normalization_valid.md').write_text(normalization, encoding='utf-8')

source_text = source_path.read_text(encoding='utf-8')
(samples / 'sample_roundtrip_source_mutated.md').write_text(
    source_text.replace(
        'GOAL: "Confirm the cause and apply the smallest safe correction"',
        'GOAL: "Confirm the cause and apply a different correction"',
        1,
    ),
    encoding='utf-8',
)

variants = {
    'sample_roundtrip_bad_digest.md': normalization.replace(
        'sha256:',
        'sha256:0',
        1,
    ),
    'sample_roundtrip_missing_exact.md': normalization.replace(
        '    - "repository: tk999jp/example"\n',
        '',
        1,
    ),
    'sample_roundtrip_missing_protected.md': normalization.replace(
        '    - "Broad refactor prohibited"\n',
        '',
        1,
    ),
    'sample_roundtrip_order_changed.md': normalization.replace(
        'FLOW-READ>FLOW-ANALYZE>FLOW-GATE>FLOW-CHANGE>FLOW-VERIFY>FLOW-REPORT',
        'FLOW-ANALYZE>FLOW-READ>FLOW-GATE>FLOW-CHANGE>FLOW-VERIFY>FLOW-REPORT',
        1,
    ),
    'sample_roundtrip_preview_order_changed.md': normalization.replace(
        '''    - FLOW-READ: Inspect exact READ references
    - FLOW-ANALYZE: Separate observation from inference''',
        '''    - FLOW-ANALYZE: Separate observation from inference
    - FLOW-READ: Inspect exact READ references''',
        1,
    ),
    'sample_roundtrip_authority_widened.md': normalization.replace(
        '    - push: forbid',
        '    - push: allow',
        1,
    ),
    'sample_roundtrip_map_omission.md': normalization.replace(
        '''    - source: SCHEMA
      target: "normalization provenance"
      mode: exact
      evidence: "source field retained by first-slice mapper"
''',
        '',
        1,
    ),
    'sample_roundtrip_result_schema_lost.md': normalization.replace(
        '    - kdsl-r1c@0.1-draft',
        '    - canonical-r1',
        1,
    ),
    'sample_roundtrip_semantic_claim.md': normalization.replace(
        '  semantic_equivalence: not_proven',
        '  semantic_equivalence: pass',
        1,
    ),
    'sample_roundtrip_executable_marker.md': normalization.replace(
        '    KDSL_PROMPT_PREVIEW:',
        '    KDSL_PROMPT:',
        1,
    ),
}
for name, content in variants.items():
    (samples / name).write_text(content, encoding='utf-8')

roundtrip_cases = """    {
        'name': 'round-trip generated Full KDSL structural pass',
        'command': ['kdsl_packet_roundtrip.py', 'examples/packet/normalization-source.example.md'],
        'expected': 0,
        'stdout_contains': [
            'STRUCTURAL_ROUND_TRIP_RESULT:',
            'STATUS: structural_pass',
            'EXECUTABLE: no',
            'SEMANTIC_EQUIVALENCE: not_proven',
            'EXECUTION_AUTHORITY: none',
        ],
        'stdout_not_contains': ['\\nKDSL_PROMPT:', '\\nP1:', '\\nP1L:'],
    },
    {
        'name': 'round-trip generated P1 blocked',
        'command': ['kdsl_packet_roundtrip.py', 'examples/packet/normalization-p1-source.example.md'],
        'expected': 1,
        'stdout_contains': [
            'STATUS: blocked',
            'EXECUTABLE: no',
            'SEMANTIC_EQUIVALENCE: not_proven',
            'P1/P1L unresolved target remains blocked',
        ],
        'stdout_not_contains': ['\\nKDSL_PROMPT:', '\\nP1:'],
    },
    {
        'name': 'round-trip invalid Packet rejected',
        'command': ['kdsl_packet_roundtrip.py', 'tools/validator/samples/sample_packet_normalized.md'],
        'expected': 2,
        'stdout_contains': ['STATUS: fail'],
        'stdout_not_contains': ['STATUS: structural_pass'],
    },
    {
        'name': 'round-trip provided normalization structural pass',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_normalization_valid.md',
        ],
        'expected': 0,
        'stdout_contains': ['STATUS: structural_pass', 'all Packet fields accounted in MAP'],
    },
    {
        'name': 'round-trip source mutation detects digest mismatch',
        'command': [
            'kdsl_packet_roundtrip.py',
            'samples/sample_roundtrip_source_mutated.md',
            'samples/sample_roundtrip_normalization_valid.md',
        ],
        'expected': 2,
        'stdout_contains': ['source digest mismatch'],
    },
    {
        'name': 'round-trip malformed digest rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_bad_digest.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
    },
    {
        'name': 'round-trip exact string loss detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_missing_exact.md',
        ],
        'expected': 2,
        'stdout_contains': ['exact strings missing from PRESERVE'],
    },
    {
        'name': 'round-trip protected wording loss detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_missing_protected.md',
        ],
        'expected': 2,
        'stdout_contains': ['protected wording missing from PRESERVE'],
    },
    {
        'name': 'round-trip preserved order mutation detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_order_changed.md',
        ],
        'expected': 2,
        'stdout_contains': ['ordered fields missing or changed'],
    },
    {
        'name': 'round-trip preview FLOW order mutation detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_preview_order_changed.md',
        ],
        'expected': 2,
        'stdout_contains': ['FLOW order changed in preview'],
    },
    {
        'name': 'round-trip authority widening detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_authority_widened.md',
        ],
        'expected': 2,
        'stdout_contains': ['authority rail missing or widened in preview: push'],
    },
    {
        'name': 'round-trip MAP omission rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_map_omission.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
    },
    {
        'name': 'round-trip result schema loss detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_result_schema_lost.md',
        ],
        'expected': 2,
        'stdout_contains': ['result schema missing from preview'],
    },
    {
        'name': 'round-trip semantic equivalence claim rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_semantic_claim.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
    },
    {
        'name': 'round-trip executable marker rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_executable_marker.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
        'stdout_not_contains': ['STATUS: structural_pass'],
    },
"""
replace_once(
    'tools/validator/run_samples.py',
    '\n]\n\n\ndef resolve_command',
    '\n' + roundtrip_cases + ']\n\n\ndef resolve_command',
)

Path('tools/validator/kdsl-packet-roundtrip-implementation-notes.md').write_text(
    '''# KDSL Packet Normalization Structural Round-Trip First Slice

status: integration-candidate
tool: tools/validator/kdsl_packet_roundtrip.py
output: STRUCTURAL_ROUND_TRIP_RESULT
validator_authority: non-authoritative

## Scope

```text
source digest identity
all Packet field MAP accounting
exact-string preservation
protected-wording preservation
FLOW/STOP/VERIFY order preservation
authority rail preservation
OUT result schema preservation
non-executable target/output boundary
P1/P1L blocked target evidence
```

## Status model

```text
structural_pass: selected structural properties match
blocked: canonical P1/P1L target schema unresolved
fail: loss/mismatch/checker failure
```

## Boundaries

```text
structural_pass != semantic equivalence
structural_pass != complete safety proof
structural_pass != normalization completion
structural_pass != execution authority
structural_pass != RT:v
first slice supports Full KDSL pass and P1/P1L blocked state
```
''',
    encoding='utf-8',
)
Path('tools/validator/samples/roundtrip_expected_results.md').write_text(
    '''# Packet Normalization Round-Trip Expected Results

status: first-slice candidate
expected_total_suite: 108

```text
generated Full KDSL: structural_pass / exit 0
generated P1: blocked / exit 1
invalid Packet: fail / exit 2
provided baseline artifact: structural_pass
source/digest mutation: fail
exact string/protected wording/order loss: fail
authority widening: fail
MAP omission: fail
result schema loss: fail
semantic claim/executable marker: fail
```
''',
    encoding='utf-8',
)
Path('tools/validator/verification/kdsl_packet_roundtrip_verify.md').write_text(
    '''# KDSL Packet Normalization Round-Trip Verification

status: branch-validation-pending
date: 2026-07-11
branch: agent/kdsl-packet-normalization-roundtrip
expected_sample_total: 108

```text
round-trip helper未実行→pass扱禁止
CI pending
structural_pass != semantic equivalence/safety proof/normalization completion/RT:v/authority/release readiness
```
''',
    encoding='utf-8',
)

replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'round-trip property tests: not implemented',
    'round-trip property tests: first-slice integration pending',
)
replace_once(
    'tools/validator/README.md',
    '  kdsl_packet_normalize.py\n  kdsl-packet-normalization-implementation-notes.md',
    '  kdsl_packet_normalize.py\n  kdsl_packet_roundtrip.py\n  kdsl-packet-normalization-implementation-notes.md\n  kdsl-packet-roundtrip-implementation-notes.md',
)
replace_once(
    'tools/validator/README.md',
    '''Packet normalization first slice integrated:
  total: 93 / failed: 0
  pull_request: 23
  workflow_run: 150 / success''',
    '''Packet normalization first slice integrated:
  total: 93 / failed: 0
  pull_request: 23
  workflow_run: 150 / success

Packet normalization round-trip first slice candidate:
  expected total: 108 / branch validation pending''',
)
replace_once(
    'tools/validator/README.md',
    'tools/validator/verification/kdsl_packet_normalization_verify.md\n```',
    'tools/validator/verification/kdsl_packet_normalization_verify.md\ntools/validator/verification/kdsl_packet_roundtrip_verify.md\n```',
)
replace_once(
    'tools/validator/README.md',
    'Normalization round-trip proofなし\nruntime実行なし',
    'Normalization semantic round-trip proofなし\nStructural round-trip first slice:=integration pending\nruntime実行なし',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '## Sample verification',
    '''## Structural round-trip helper

```text
python tools/validator/kdsl_packet_roundtrip.py <packet-file>
python tools/validator/kdsl_packet_roundtrip.py <packet-file> <normalization-file>
```

Output:

```text
STRUCTURAL_ROUND_TRIP_RESULT
STATUS: structural_pass|blocked|fail
EXECUTABLE:no
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

This helper is outside the combined validator target set. It does not create executable targets or prove semantic equivalence.

## Sample verification''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Packet normalization first slice integrated:
  total: 93 / failed: 0
  pull_request: 23
  workflow_run: 150 / success''',
    '''Packet normalization first slice integrated:
  total: 93 / failed: 0
  pull_request: 23
  workflow_run: 150 / success

Packet normalization round-trip first slice candidate:
  expected total: 108 / branch validation pending''',
)
replace_once(
    'README.md',
    'Packet normalization validator/mapper: first-slice integrated / non-executable preview only\nvalidator sample suite: 93 expectations / failed 0',
    'Packet normalization validator/mapper: first-slice integrated / non-executable preview only\nPacket normalization structural round-trip: first-slice integration pending\nvalidator sample suite: 108 expectations candidate',
)
replace_once(
    'README.md',
    '  tools/validator/kdsl_packet_normalize.py\n  tools/validator/run_samples.py',
    '  tools/validator/kdsl_packet_normalize.py\n  tools/validator/kdsl_packet_roundtrip.py\n  tools/validator/run_samples.py',
)
replace_once(
    'README.md',
    'python tools/validator/kdsl_packet_normalize.py <packet-file>\npython tools/validator/kdsl_validate.py --target all <file>',
    'python tools/validator/kdsl_packet_normalize.py <packet-file>\npython tools/validator/kdsl_packet_roundtrip.py <packet-file> [normalization-file]\npython tools/validator/kdsl_validate.py --target all <file>',
)
replace_once(
    'README.md',
    'Packet normalization round-trip/property proofなし',
    'Packet normalization structural round-trip first slice:=integration pending\nPacket normalization semantic/property proofなし',
)
replace_once(
    'README.md',
    '''P0:
  normalization round-trip/property tests

P1:
  Safety Gate protected wording/inheritance validator拡張''',
    '''P0:
  PR #27 CI確認 / squash merge / round-trip closeout

P1:
  Safety Gate protected wording/inheritance validator拡張''',
)
replace_once(
    'CHANGELOG.md',
    '### Added\n\n#### Packet normalization validator / mapper first slice',
    '''### Added

#### Packet normalization structural round-trip first slice

- Added `tools/validator/kdsl_packet_roundtrip.py`.
- Added source digest, MAP accounting, exact-string, protected-wording, ordering, authority, and result-schema comparisons.
- Added Full KDSL structural-pass and P1/P1L blocked status handling.
- Added mutation tests for loss, widening, order changes, semantic claims, and executable markers.
- Expanded the candidate suite from 93 to 108 expectations.
- Kept `semantic_equivalence:not_proven`, `execution_authority:none`, and non-executable output fixed.

#### Packet normalization validator / mapper first slice''',
)
replace_once(
    'docs/project-status.md',
    '## 3. Current architecture direction',
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
```

## 3. Current architecture direction''',
)
replace_once(
    'docs/project-status.md',
    'Packet normalization validator/mapper first slice:=main統合済み / 93 expectations verified\nKDSL-Packet:=non-executable / normalization required',
    'Packet normalization validator/mapper first slice:=main統合済み / 93 expectations verified\nPacket normalization structural round-trip first slice:=integration pending\nKDSL-Packet:=non-executable / normalization required',
)
replace_once(
    'docs/project-status.md',
    '    expected_sample_total: 93',
    '    expected_sample_total: 108',
)
replace_once(
    'docs/project-status.md',
    'Normalization round-trip/property proofなし',
    'Normalization structural round-trip first slice:=integration pending\nNormalization semantic/property proofなし',
)
replace_once(
    'docs/project-status.md',
    '### Packet normalization validator / mapper first slice\n',
    '''### Packet normalization structural round-trip candidate

```yaml
pull_request: 26
branch: agent/kdsl-packet-normalization-roundtrip
expected_sample_total: 108
status: branch_validation_pending
meaning: selected structural properties only; not semantic-equivalence/safety/normalization proof
```

### Packet normalization validator / mapper first slice
''',
)
replace_once(
    'docs/project-status.md',
    '''P0: normalization round-trip/property tests
P1: Safety Gate protected wording/inheritance validator拡張''',
    '''P0: PR #27 CI確認 / squash merge / round-trip closeout
P1: Safety Gate protected wording/inheritance validator拡張''',
)

Path('.github/scripts/apply_packet_roundtrip.py').unlink()
