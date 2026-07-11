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
base = (samples / 'sample_normalization_valid.md').read_text(encoding='utf-8')

variants = {
    'sample_normalization_unknown_schema.md': base.replace(
        'SCHEMA: kdsl-packet-normalization@0.1-draft',
        'SCHEMA: kdsl-packet-normalization@9',
        1,
    ),
    'sample_normalization_executable_status.md': base.replace(
        'STATUS: non-executable',
        'STATUS: executable',
        1,
    ),
    'sample_normalization_target_executable.md': base.replace(
        '  executable: false',
        '  executable: true',
        1,
    ),
    'sample_normalization_semantic_claim.md': base.replace(
        '  semantic_equivalence: not_proven',
        '  semantic_equivalence: pass',
        1,
    ),
    'sample_normalization_authority.md': base.replace(
        '  execution_authority: none',
        '  execution_authority: allow',
        1,
    ),
    'sample_normalization_p1_resolved.md': base.replace(
        '''  kind: full-kdsl-dev-prompt
  schema: "format:KDSL/profile:dev-prompt"
  resolution: resolved''',
        '''  kind: P1
  schema: unresolved
  resolution: resolved''',
        1,
    ),
    'sample_normalization_executable_marker.md': base.replace(
        '    KDSL_PROMPT_PREVIEW:',
        '    KDSL_PROMPT:',
        1,
    ),
    'sample_normalization_source_normalized.md': base.replace(
        '  normalize_state: not_normalized',
        '  normalize_state: normalized',
        1,
    ),
    'sample_normalization_missing_digest.md': base.replace(
        '  digest: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n',
        '',
        1,
    ),
    'sample_normalization_critical_resolved.md': base.replace(
        'LOSS: []',
        '''LOSS:
  - class: critical
    source: SG
    detail: "protected wording lost"''',
        1,
    ),
    'sample_normalization_rails_false.md': base.replace(
        '  source_rails_preserved: true',
        '  source_rails_preserved: false',
        1,
    ),
    'sample_normalization_bad_digest.md': base.replace(
        'sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'sha256:ABC',
        1,
    ),
    'sample_normalization_blocked_preview.md': base.replace(
        '  resolution: resolved',
        '  resolution: blocked',
        1,
    ).replace(
        '  marker: KDSL_PROMPT_PREVIEW',
        '  marker: none',
        1,
    ),
    'sample_normalization_out_of_scope.md': '# Ordinary document\n\nNo normalization envelope is present.\n',
}
for name, content in variants.items():
    (samples / name).write_text(content, encoding='utf-8')

# Combined wrapper integration.
replace_once(
    'tools/validator/kdsl_validate.py',
    """    'packet': [
        'kdsl_packet.py',
    ],
    'all': [""",
    """    'packet': [
        'kdsl_packet.py',
    ],
    'normalization': [
        'kdsl_packet_normalization.py',
    ],
    'all': [""",
)
replace_once(
    'tools/validator/kdsl_validate.py',
    """        'kdsl_r1c.py',
        'kdsl_packet.py',
    ],""",
    """        'kdsl_r1c.py',
        'kdsl_packet.py',
        'kdsl_packet_normalization.py',
    ],""",
)
replace_once(
    'tools/validator/kdsl_validate.py',
    "TARGETS = 'r1, prompt, compact, safety-gate, r1c, packet, all'",
    "TARGETS = 'r1, prompt, compact, safety-gate, r1c, packet, normalization, all'",
)
replace_once(
    'tools/validator/kdsl_validate.py',
    "usage: python kdsl_validate.py [--target r1|prompt|compact|safety-gate|r1c|packet|all] <file>",
    "usage: python kdsl_validate.py [--target r1|prompt|compact|safety-gate|r1c|packet|normalization|all] <file>",
)

# Sample runner output assertions.
replace_once(
    'tools/validator/run_samples.py',
    """    ok = proc.returncode == sample['expected']
    status = 'PASS' if ok else 'FAIL'""",
    """    expected_code = proc.returncode == sample['expected']
    contains = sample.get('stdout_contains', [])
    excludes = sample.get('stdout_not_contains', [])
    contains_ok = all(value in proc.stdout for value in contains)
    excludes_ok = all(value not in proc.stdout for value in excludes)
    ok = expected_code and contains_ok and excludes_ok
    status = 'PASS' if ok else 'FAIL'""",
)
replace_once(
    'tools/validator/run_samples.py',
    """    print(f"  actual: {proc.returncode}")
    if not ok:
        if proc.stdout:""",
    """    print(f"  actual: {proc.returncode}")
    if contains:
        print(f"  stdout_contains: {contains}")
    if excludes:
        print(f"  stdout_not_contains: {excludes}")
    if not ok:
        missing = [value for value in contains if value not in proc.stdout]
        present = [value for value in excludes if value in proc.stdout]
        if missing:
            print(f"  missing stdout values: {missing}")
        if present:
            print(f"  prohibited stdout values: {present}")
        if proc.stdout:""",
)

normalization_cases = """    {
        'name': 'normalization repository Full KDSL preview valid',
        'command': ['kdsl_packet_normalization.py', 'examples/packet/normalization-full-kdsl.example.md'],
        'expected': 0,
    },
    {
        'name': 'normalization repository P1 blocked valid',
        'command': ['kdsl_packet_normalization.py', 'examples/packet/normalization-p1-blocked.example.md'],
        'expected': 0,
    },
    {
        'name': 'normalization repository critical-loss blocked valid',
        'command': ['kdsl_packet_normalization.py', 'examples/packet/normalization-lossy-blocked.example.md'],
        'expected': 0,
    },
    {
        'name': 'normalization baseline valid',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_valid.md'],
        'expected': 0,
    },
    {
        'name': 'normalization unknown schema',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_unknown_schema.md'],
        'expected': 2,
    },
    {
        'name': 'normalization executable status rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_executable_status.md'],
        'expected': 2,
    },
    {
        'name': 'normalization target executable rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_target_executable.md'],
        'expected': 2,
    },
    {
        'name': 'normalization semantic equivalence claim rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_semantic_claim.md'],
        'expected': 2,
    },
    {
        'name': 'normalization execution authority rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_authority.md'],
        'expected': 2,
    },
    {
        'name': 'normalization P1 resolved rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_p1_resolved.md'],
        'expected': 2,
    },
    {
        'name': 'normalization executable KDSL prompt marker rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_executable_marker.md'],
        'expected': 2,
    },
    {
        'name': 'normalization source normalized state rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_source_normalized.md'],
        'expected': 2,
    },
    {
        'name': 'normalization missing digest rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_missing_digest.md'],
        'expected': 2,
    },
    {
        'name': 'normalization critical loss with resolved target rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_critical_resolved.md'],
        'expected': 2,
    },
    {
        'name': 'normalization authority rails false without blocked critical loss rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_rails_false.md'],
        'expected': 2,
    },
    {
        'name': 'normalization malformed digest rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_bad_digest.md'],
        'expected': 2,
    },
    {
        'name': 'normalization blocked target with preview rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_blocked_preview.md'],
        'expected': 2,
    },
    {
        'name': 'normalization out of scope document',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_out_of_scope.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target normalization valid',
        'command': ['kdsl_validate.py', '--target', 'normalization', 'samples/sample_normalization_valid.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target normalization invalid',
        'command': ['kdsl_validate.py', '--target', 'normalization', 'samples/sample_normalization_semantic_claim.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target all normalization valid',
        'command': ['kdsl_validate.py', '--target', 'all', 'samples/sample_normalization_valid.md'],
        'expected': 0,
    },
    {
        'name': 'normalization mapper Full KDSL preview',
        'command': ['kdsl_packet_normalize.py', 'examples/packet/normalization-source.example.md'],
        'expected': 0,
        'stdout_contains': [
            'NORMALIZATION_DRAFT:',
            'SCHEMA: kdsl-packet-normalization@0.1-draft',
            'KDSL_PROMPT_PREVIEW:',
            'semantic_equivalence: not_proven',
            'execution_authority: none',
            'TARGET:',
            '  executable: false',
        ],
        'stdout_not_contains': ['\\nKDSL_PROMPT:', '\\nSTATUS: executable'],
    },
    {
        'name': 'normalization mapper P1 blocked',
        'command': ['kdsl_packet_normalize.py', 'examples/packet/normalization-p1-source.example.md'],
        'expected': 1,
        'stdout_contains': [
            'NORMALIZATION_DRAFT:',
            '  kind: P1',
            '  resolution: blocked',
            '  marker: none',
            'execution_authority: none',
        ],
        'stdout_not_contains': ['\\nP1:', '\\nKDSL_PROMPT:'],
    },
    {
        'name': 'normalization mapper invalid Packet rejected',
        'command': ['kdsl_packet_normalize.py', 'samples/sample_packet_normalized.md'],
        'expected': 2,
        'stdout_not_contains': ['NORMALIZATION_DRAFT:', 'KDSL_PROMPT_PREVIEW:'],
    },
"""
replace_once(
    'tools/validator/run_samples.py',
    '\n]\n\n\ndef resolve_command',
    '\n' + normalization_cases + ']\n\n\ndef resolve_command',
)

# Evidence and implementation notes.
Path('tools/validator/kdsl-packet-normalization-implementation-notes.md').write_text(
    '''# KDSL Packet Normalization Validator / Mapper First Slice

status: integration-candidate
schema: kdsl-packet-normalization@0.1-draft
checker: tools/validator/kdsl_packet_normalization.py
mapper: tools/validator/kdsl_packet_normalize.py
validator_authority: non-authoritative

## Checker scope

```text
NORMALIZATION_DRAFT detection/out-of-scope separation
required field presence/order
SOURCE digest/status/not_normalized
TARGET kind/schema/resolution/executable
MAP accounting/mode/evidence
PRESERVE classes
UNRESOLVED/LOSS consistency
ROUND_TRIP state/semantic boundary
AUTHORITY.execution_authority:none
OUTPUT marker/executable/preview boundary
P1/P1L blocked target enforcement
KDSL_PROMPT/P1/P1L/PKT:v1 marker rejection
```

## Mapper scope

```text
source Packet validated first
BASE-KDSL-DEV→KDSL_PROMPT_PREVIEW
BASE-DESIGN-ONLY→DESIGN_PREVIEW
BASE-ADPS-P1→blocked/no preview
source SHA-256 recorded
ROUND_TRIP:not_tested|blocked
semantic_equivalence:not_proven
execution_authority:none
```

## Boundaries

```text
line-based heuristic parser
first NORMALIZATION_DRAFT/PACKET_DRAFT block only
full YAML parserなし
semantic equivalence proofなし
round-trip proofなし
Safety Gate completeness proofなし
mapper output != executable target
KDSL_PROMPT:生成なし
P1/P1L生成なし
Packet state normalized化なし
```
''',
    encoding='utf-8',
)
Path('tools/validator/samples/normalization_expected_results.md').write_text(
    '''# Packet Normalization Expected Results

status: first-slice candidate
expected_total_suite: 93

```text
repository Full KDSL preview: pass
repository P1 blocked: pass
repository critical-loss blocked: pass
baseline normalization: pass
schema/status/source/target/authority violations: fail
P1 resolved: fail
executable target marker: fail
critical loss + resolved target: fail
blocked target + preview: fail
out-of-scope: pass/info
wrapper normalization valid/invalid: expected exits
wrapper all valid normalization: pass
mapper Full KDSL: non-executable preview / exit 0
mapper P1: blocked / no preview / exit 1
mapper invalid Packet: no normalization output / exit 2
```
''',
    encoding='utf-8',
)
Path('tools/validator/verification/kdsl_packet_normalization_verify.md').write_text(
    '''# KDSL Packet Normalization Validator Verification

status: branch-validation-pending
date: 2026-07-11
branch: agent/kdsl-packet-normalization-validator
expected_sample_total: 93

```text
validator/mapper未実行→pass扱禁止
CI pending
mapper output != executable target
validator/mapper pass != semantic equivalence/safety proof/round-trip proof/RT:v/authority/release readiness
```
''',
    encoding='utf-8',
)

# Spec status on implementation branch.
replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'validator: not implemented',
    'validator: first-slice integration pending',
)
replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    '''normalization validator: not implemented
normalization transformer: not implemented
round-trip property tests: not implemented''',
    '''normalization validator: first-slice integration pending
normalization mapper: first-slice integration pending
round-trip property tests: not implemented''',
)
replace_once(
    'spec/packet/README.md',
    'validator/mapper: not implemented',
    'validator/mapper: first-slice integration pending',
)

# Validator README.
replace_once(
    'tools/validator/README.md',
    'KDSL / R1 / R1C / Packet / Template / CompactPrompt / Safety Gate Registry',
    'KDSL / R1 / R1C / Packet / Packet Normalization / Template / CompactPrompt / Safety Gate Registry',
)
replace_once(
    'tools/validator/README.md',
    'spec/lint/kdsl-packet-lint.md\nspec/packet/kdsl-packet-schema.md',
    'spec/lint/kdsl-packet-lint.md\nspec/lint/kdsl-packet-normalization-lint.md\nspec/packet/kdsl-packet-schema.md\nspec/packet/kdsl-packet-normalization-contract.md',
)
replace_once(
    'tools/validator/README.md',
    """kdsl_packet.py:
  PACKET_DRAFT + kdsl-packet@0.1-draft detection
  required field presence/order
  BASE/TASK/FLOW/SG registry and known ID checks
  TASK minimum gate/flow checks
  AUTHORITY/NORMALIZE/OUT boundary checks
  PKT:v1 and representative trigger checks

kdsl_validate.py:
  target wrapper: r1 / prompt / compact / safety-gate / r1c / packet / all""",
    """kdsl_packet.py:
  PACKET_DRAFT + kdsl-packet@0.1-draft detection
  required field presence/order
  BASE/TASK/FLOW/SG registry and known ID checks
  TASK minimum gate/flow checks
  AUTHORITY/NORMALIZE/OUT boundary checks
  PKT:v1 and representative trigger checks

kdsl_packet_normalization.py:
  NORMALIZATION_DRAFT schema/field/order checks
  source/target/map/preserve/loss/round-trip checks
  authority/output/non-execution checks
  P1/P1L blocked target enforcement

kdsl_packet_normalize.py:
  source Packet pre-validation
  non-executable Full KDSL/design preview generation
  P1/P1L blocked evidence generation
  no executable KDSL_PROMPT/P1/P1L generation

kdsl_validate.py:
  target wrapper: r1 / prompt / compact / safety-gate / r1c / packet / normalization / all""",
)
replace_once(
    'tools/validator/README.md',
    '''Packet first slice integrated:
  total: 69 / failed: 0
  pull_request: 14
  workflow_run: 116 / success''',
    '''Packet first slice integrated:
  total: 69 / failed: 0
  pull_request: 14
  workflow_run: 116 / success

Packet normalization first slice candidate:
  expected total: 93 / branch validation pending''',
)
replace_once(
    'tools/validator/README.md',
    'examples/packet/packet-design.example.md\n```',
    '''examples/packet/packet-design.example.md
examples/packet/normalization-full-kdsl.example.md
examples/packet/normalization-p1-blocked.example.md
examples/packet/normalization-lossy-blocked.example.md
```''',
)
replace_once(
    'tools/validator/README.md',
    'tools/validator/verification/kdsl_packet_verify.md\n```',
    'tools/validator/verification/kdsl_packet_verify.md\ntools/validator/verification/kdsl_packet_normalization_verify.md\n```',
)
replace_once(
    'tools/validator/README.md',
    'Packet envelope/registry/gate/flow/authority/normalization境界検出\nEVIDENCE',
    'Packet envelope/registry/gate/flow/authority/normalization境界検出\nNormalization mapping/loss/authority/output境界検出\nNon-executable structural preview生成\nEVIDENCE',
)
replace_once(
    'tools/validator/README.md',
    '  kdsl-packet-implementation-notes.md\n  kdsl_validate.py',
    '  kdsl-packet-implementation-notes.md\n  kdsl_packet_normalization.py\n  kdsl_packet_normalize.py\n  kdsl-packet-normalization-implementation-notes.md\n  kdsl_validate.py',
)
replace_once(
    'tools/validator/README.md',
    'Packet full YAML/semantic parserなし\nPacket normalization round-trip proofなし',
    'Packet full YAML/semantic parserなし\nNormalization full YAML/semantic parserなし\nNormalization round-trip proofなし',
)
replace_once(
    'tools/validator/README.md',
    'Packet validator pass != Packet executable/normalized/authority\nvalidator failure時',
    'Packet validator pass != Packet executable/normalized/authority\nNormalization validator/mapper pass != executable target/semantic equivalence/round-trip proof\nvalidator failure時',
)

# Usage documentation.
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    """--target packet
  runs:
    kdsl_packet.py

--target all""",
    """--target packet
  runs:
    kdsl_packet.py

--target normalization
  runs:
    kdsl_packet_normalization.py

--target all""",
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '    kdsl_r1c.py\n    kdsl_packet.py\n```',
    '    kdsl_r1c.py\n    kdsl_packet.py\n    kdsl_packet_normalization.py\n```',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Packet checker:
  PACKET_DRAFTなし→pass/info
  Packet SCHEMAのみ + PACKET_DRAFTなし→fail
  unknown SCHEMA/registry/ID/opcode→fail''',
    '''Packet checker:
  PACKET_DRAFTなし→pass/info
  Packet SCHEMAのみ + PACKET_DRAFTなし→fail
  unknown SCHEMA/registry/ID/opcode→fail

Normalization checker:
  NORMALIZATION_DRAFTなし→pass/info
  normalization SCHEMAのみ + envelopeなし→fail
  executable target/P1/P1L marker→fail''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'python tools/validator/kdsl_validate.py --target packet examples/packet/packet-design.example.md\npython tools/validator/kdsl_validate.py --target all',
    'python tools/validator/kdsl_validate.py --target packet examples/packet/packet-design.example.md\npython tools/validator/kdsl_validate.py --target normalization examples/packet/normalization-full-kdsl.example.md\npython tools/validator/kdsl_validate.py --target all',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '## Sample verification',
    '''## Packet normalization first-slice scope

```text
NORMALIZATION_DRAFT/schema/status/order
SOURCE digest/non-executable/not_normalized
TARGET kind/schema/resolution/executable
MAP accounting/mode/evidence
PRESERVE/UNRESOLVED/LOSS
ROUND_TRIP semantic boundary
AUTHORITY.execution_authority:none
OUTPUT marker/preview/non-execution
P1/P1L blocked enforcement
non-executable structural mapper
```

Not covered:

```text
full YAML parser
semantic equivalence proof
round-trip reconstruction/property proof
Safety Gate completeness proof
executable KDSL_PROMPT/P1/P1L generation
Packet state normalized transition
```

## Sample verification''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '''Packet first slice integrated:
  total: 69 / failed: 0
  pull_request: 14
  workflow_run: 116 / success''',
    '''Packet first slice integrated:
  total: 69 / failed: 0
  pull_request: 14
  workflow_run: 116 / success

Packet normalization first slice candidate:
  expected total: 93 / branch validation pending''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'examples/packet/packet-design.example.md\n```',
    '''examples/packet/packet-design.example.md
examples/packet/normalization-full-kdsl.example.md
examples/packet/normalization-p1-blocked.example.md
examples/packet/normalization-lossy-blocked.example.md
```''',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'tools/validator/verification/kdsl_packet_verify.md\n```',
    'tools/validator/verification/kdsl_packet_verify.md\ntools/validator/verification/kdsl_packet_normalization_verify.md\n```',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '--target packet does not prove Packet normalization/execution/authority semantics\n--target all',
    '--target packet does not prove Packet normalization/execution/authority semantics\n--target normalization does not prove semantic equivalence/round-trip/execution readiness\n--target all',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'Packet validator implementation != Packet executable/normalized/readiness\n```',
    'Packet validator implementation != Packet executable/normalized/readiness\nNormalization validator/mapper implementation != executable target/normalized state\n```',
)

# Root README and changelog.
replace_once(
    'README.md',
    'Packet normalization validator/mapper: not implemented\nvalidator sample suite: 69 expectations / failed 0',
    'Packet normalization validator/mapper: first-slice integration pending\nvalidator sample suite: 93 expectations candidate',
)
replace_once(
    'README.md',
    '  tools/validator/kdsl_packet.py\n  tools/validator/run_samples.py',
    '  tools/validator/kdsl_packet.py\n  tools/validator/kdsl_packet_normalization.py\n  tools/validator/kdsl_packet_normalize.py\n  tools/validator/run_samples.py',
)
replace_once(
    'README.md',
    'python tools/validator/kdsl_validate.py --target packet <file>\npython tools/validator/kdsl_validate.py --target all <file>',
    'python tools/validator/kdsl_validate.py --target packet <file>\npython tools/validator/kdsl_validate.py --target normalization <file>\npython tools/validator/kdsl_packet_normalize.py <packet-file>\npython tools/validator/kdsl_validate.py --target all <file>',
)
replace_once(
    'README.md',
    'Normalization validator/mapper未実装\nNormalization round-trip/property proofなし',
    'Normalization validator/mapper first slice:=integration pending\nNormalization round-trip/property proofなし',
)
replace_once(
    'README.md',
    '''P0:
  normalization validator/structural mapper first slice

P1:
  normalization round-trip/property tests''',
    '''P0:
  PR #23 CI確認 / squash merge / normalization validator closeout

P1:
  normalization round-trip/property tests''',
)

replace_once(
    'CHANGELOG.md',
    '### Added\n\n#### Packet normalization v2-draft ownership alignment',
    '''### Added

#### Packet normalization validator / mapper first slice

- Added `tools/validator/kdsl_packet_normalization.py`.
- Added non-executable `tools/validator/kdsl_packet_normalize.py`.
- Added normalization schema/field/order/source/target/map/loss/round-trip/authority/output checks.
- Added Full KDSL/design preview generation and P1/P1L blocked evidence generation.
- Added `--target normalization` and normalization checking to `--target all`.
- Expanded the candidate suite from 69 to 93 expectations.
- Kept executable `KDSL_PROMPT:`, P1, and P1L generation prohibited.
- Kept Packet state `not_normalized`, `semantic_equivalence:not_proven`, and `execution_authority:none`.

#### Packet normalization v2-draft ownership alignment''',
)

# Project status pending integration record.
replace_once(
    'docs/project-status.md',
    '## 3. Current architecture direction',
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
```

## 3. Current architecture direction''',
)
replace_once(
    'docs/project-status.md',
    'Packet normalization validator/mapper:=未実装',
    'Packet normalization validator/mapper first slice:=integration pending',
)
replace_once(
    'docs/project-status.md',
    '  normalization_validator_mapper: not_implemented',
    '  normalization_validator_mapper: first_slice_integration_pending',
)
replace_once(
    'docs/project-status.md',
    '    - packet\n    - all',
    '    - packet\n    - normalization\n    - all',
)
replace_once(
    'docs/project-status.md',
    '    - Packet out-of-scope separation\n  ci:',
    '    - Packet out-of-scope separation\n    - Normalization envelope/source/target/map/loss/authority/output lint\n    - Non-executable structural mapper\n  ci:',
)
replace_once(
    'docs/project-status.md',
    '    expected_sample_total: 69',
    '    expected_sample_total: 93',
)
replace_once(
    'docs/project-status.md',
    'Normalization validator/mapper未実装\nNormalization round-trip/property proofなし',
    'Normalization validator/mapper first slice:=integration pending\nNormalization round-trip/property proofなし',
)
replace_once(
    'docs/project-status.md',
    '### Packet normalization ownership\n',
    '''### Packet normalization validator / mapper candidate

```yaml
pull_request: 22
branch: agent/kdsl-packet-normalization-validator
expected_sample_total: 93
status: branch_validation_pending
meaning: first-slice heuristic/preview candidate; not semantic-equivalence/round-trip/execution proof
```

### Packet normalization ownership
''',
)
replace_once(
    'docs/project-status.md',
    '''P0: normalization validator/structural mapper first slice
P1: normalization round-trip/property tests''',
    '''P0: PR #23 CI確認 / squash merge / normalization validator closeout
P1: normalization round-trip/property tests''',
)

Path('.github/scripts/apply_packet_normalization_validator.py').unlink()
