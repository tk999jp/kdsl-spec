from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


# Generate Packet sample matrix from the validated baseline sample.
sample_dir = Path('tools/validator/samples')
base = (sample_dir / 'sample_packet_valid.md').read_text(encoding='utf-8')

variants = {
    'sample_packet_unknown_schema.md': base.replace(
        'SCHEMA: kdsl-packet@0.1-draft',
        'SCHEMA: kdsl-packet@9',
    ),
    'sample_packet_executable_status.md': base.replace(
        'STATUS: non-executable',
        'STATUS: executable',
    ),
    'sample_packet_missing_read.md': base.replace(
        'READ:\n  - "src/Example.cs"\n',
        '',
    ),
    'sample_packet_unknown_base.md': base.replace(
        'id: BASE-KDSL-DEV',
        'id: BASE-UNKNOWN',
    ),
    'sample_packet_target_mismatch.md': base.replace(
        'target: full-kdsl-dev-prompt',
        'target: design-only',
    ),
    'sample_packet_unknown_task.md': base.replace(
        'id: TASK-CHANGE',
        'id: TASK-UNKNOWN',
    ),
    'sample_packet_unknown_sg_registry.md': base.replace(
        'registry: kdsl-sg@0.1-draft',
        'registry: kdsl-sg@9',
    ),
    'sample_packet_missing_gate.md': base.replace(
        '    - id: SG-AUTHORITY\n      state: hold\n      scope: edit\n      reason: pending\n',
        '',
    ),
    'sample_packet_unknown_flow.md': base.replace(
        '    - op: FLOW-ANALYZE',
        '    - op: FLOW-RUN',
    ),
    'sample_packet_flow_order.md': base.replace(
        '    - op: FLOW-GATE\n      detail: "Gate"\n    - op: FLOW-CHANGE\n      detail: "Change after normalization"',
        '    - op: FLOW-CHANGE\n      detail: "Change before gate"\n    - op: FLOW-GATE\n      detail: "Gate"',
    ),
    'sample_packet_missing_authority.md': base.replace(
        '  release: forbid\n',
        '',
    ),
    'sample_packet_normalized.md': base.replace(
        'state: not_normalized',
        'state: normalized',
    ),
    'sample_packet_pkt_v1.md': base + '\nPKT:v1\n',
    'sample_packet_authority_warn.md': base.replace(
        '  push: forbid',
        '  push: allow_once',
    ),
    'sample_packet_out_of_scope.md': '# Ordinary document\n\nNo Packet authoring block is present.\n',
}

for name, text in variants.items():
    (sample_dir / name).write_text(text, encoding='utf-8')

# Wrapper integration.
replace_once(
    'tools/validator/kdsl_validate.py',
    """    'r1c': [
        'kdsl_r1c.py',
    ],
    'all': [""",
    """    'r1c': [
        'kdsl_r1c.py',
    ],
    'packet': [
        'kdsl_packet.py',
    ],
    'all': [""",
)
replace_once(
    'tools/validator/kdsl_validate.py',
    """        'kdsl_safety_gate.py',
        'kdsl_r1c.py',
    ],""",
    """        'kdsl_safety_gate.py',
        'kdsl_r1c.py',
        'kdsl_packet.py',
    ],""",
)
replace_once(
    'tools/validator/kdsl_validate.py',
    "TARGETS = 'r1, prompt, compact, safety-gate, r1c, all'",
    "TARGETS = 'r1, prompt, compact, safety-gate, r1c, packet, all'",
)
replace_once(
    'tools/validator/kdsl_validate.py',
    "usage: python kdsl_validate.py [--target r1|prompt|compact|safety-gate|r1c|all] <file>",
    "usage: python kdsl_validate.py [--target r1|prompt|compact|safety-gate|r1c|packet|all] <file>",
)

# Sample runner: 49 -> 69 expectations.
packet_samples = """    {
        'name': 'packet repository design example valid',
        'command': ['kdsl_packet.py', 'examples/packet/packet-design.example.md'],
        'expected': 0,
    },
    {
        'name': 'packet baseline valid',
        'command': ['kdsl_packet.py', 'samples/sample_packet_valid.md'],
        'expected': 0,
    },
    {
        'name': 'packet unknown schema',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_schema.md'],
        'expected': 2,
    },
    {
        'name': 'packet executable status rejected',
        'command': ['kdsl_packet.py', 'samples/sample_packet_executable_status.md'],
        'expected': 2,
    },
    {
        'name': 'packet missing required READ field',
        'command': ['kdsl_packet.py', 'samples/sample_packet_missing_read.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown BASE ID',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_base.md'],
        'expected': 2,
    },
    {
        'name': 'packet BASE target mismatch',
        'command': ['kdsl_packet.py', 'samples/sample_packet_target_mismatch.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown TASK ID',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_task.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown SG registry',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_sg_registry.md'],
        'expected': 2,
    },
    {
        'name': 'packet TASK minimum gate missing',
        'command': ['kdsl_packet.py', 'samples/sample_packet_missing_gate.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown FLOW opcode',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_flow.md'],
        'expected': 2,
    },
    {
        'name': 'packet FLOW-CHANGE before FLOW-GATE',
        'command': ['kdsl_packet.py', 'samples/sample_packet_flow_order.md'],
        'expected': 2,
    },
    {
        'name': 'packet missing authority rail',
        'command': ['kdsl_packet.py', 'samples/sample_packet_missing_authority.md'],
        'expected': 2,
    },
    {
        'name': 'packet normalized state rejected',
        'command': ['kdsl_packet.py', 'samples/sample_packet_normalized.md'],
        'expected': 2,
    },
    {
        'name': 'packet PKT v1 rejected',
        'command': ['kdsl_packet.py', 'samples/sample_packet_pkt_v1.md'],
        'expected': 2,
    },
    {
        'name': 'packet broad push authority warning',
        'command': ['kdsl_packet.py', 'samples/sample_packet_authority_warn.md'],
        'expected': 1,
    },
    {
        'name': 'packet out of scope document',
        'command': ['kdsl_packet.py', 'samples/sample_packet_out_of_scope.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target packet valid',
        'command': ['kdsl_validate.py', '--target', 'packet', 'samples/sample_packet_valid.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target packet invalid',
        'command': ['kdsl_validate.py', '--target', 'packet', 'samples/sample_packet_normalized.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target all Packet valid',
        'command': ['kdsl_validate.py', '--target', 'all', 'samples/sample_packet_valid.md'],
        'expected': 0,
    },
"""
replace_once(
    'tools/validator/run_samples.py',
    '\n]\n\n\ndef resolve_command',
    '\n' + packet_samples + ']\n\n\ndef resolve_command',
)

# CompactPrompt Packet boundary now references the adopted schema.
replace_once(
    'tools/validator/kdsl_compact_prompt.py',
    "errors.append('PKT:v1 is prohibited while Packet schema/registries are undefined')",
    "errors.append('PKT:v1 is prohibited')",
)
replace_once(
    'tools/validator/kdsl_compact_prompt.py',
    """    if 'PACKET_DRAFT:' in scope:
        if 'status: non-executable' not in scope or 'schema: undefined' not in scope:
            errors.append('PACKET_DRAFT requires status: non-executable and schema: undefined')
        else:
            info.append('non-executable Packet draft marker detected')""",
    """    if 'PACKET_DRAFT:' in scope:
        required_packet_markers = (
            'SCHEMA: kdsl-packet@0.1-draft',
            'STATUS: non-executable',
            'required: true',
            'state: not_normalized',
        )
        missing = [marker for marker in required_packet_markers if marker not in scope]
        if missing:
            errors.append('PACKET_DRAFT non-executable markers missing: ' + ', '.join(missing))
        else:
            info.append('adopted non-executable Packet marker detected')""",
)

# Implementation and expectation records.
Path('tools/validator/kdsl-packet-implementation-notes.md').write_text(
    """# KDSL Packet Validator First Slice\n\nstatus: implementation-candidate\nschema: kdsl-packet@0.1-draft\nchecker: tools/validator/kdsl_packet.py\nvalidator_authority: non-authoritative\n\n## Implemented checks\n\n```text\nPACKET_DRAFT detection / out-of-scope pass\nrequired top-level field presence/order\nSCHEMA/STATUS exact values\nBASE/TASK/FLOW/SG registry and known ID checks\nTASK minimum FLOW and Safety Gate matrices\nFLOW-CHANGE ordering around FLOW-GATE/FLOW-STOP\nAUTHORITY required rails and allowed values\nNORMALIZE.required/target/state and BASE target compatibility\nOUT.result_schema representative values\nPKT:v1 rejection\nrepresentative rollback/runtime/public/data/KDSL-DP trigger gates\n```\n\n## Boundaries\n\n```text\nline-based heuristic parser\nfirst PACKET_DRAFT block only\nfull YAML parserなし\nfull natural-language trigger parserなし\nSafety Gate entry state/evidence deep lintなし\nprotected wording semantic equivalence proofなし\nnormalization transformer/round-trip proofなし\nPacket validator pass != executable/normalized/authority/safety proof\n```\n\n## Exit codes\n\n```text\n0: pass/out-of-scope\n1: warning\n2: fail\n```\n""",
    encoding='utf-8',
)
Path('tools/validator/samples/packet_expected_results.md').write_text(
    """# Packet Validator Expected Results\n\nstatus: first-slice candidate\n\n```text\nrepository example: pass\nbaseline sample: pass\nunknown schema: fail\nexecutable status: fail\nmissing required field: fail\nunknown BASE/TASK/SG/FLOW: fail\nBASE/NORMALIZE mismatch: fail\nminimum gate missing: fail\nFLOW order violation: fail\nmissing authority rail: fail\nnormalized state: fail\nPKT:v1: fail\nbroad push/release authority: warn\nout-of-scope document: pass/info\nwrapper packet valid/invalid: expected exit preserved\nwrapper all valid Packet: pass\n```\n""",
    encoding='utf-8',
)
Path('tools/validator/verification/kdsl_packet_verify.md').write_text(
    """# KDSL Packet Validator Verification\n\nstatus: branch-validation-pending\ndate: 2026-07-11\nbranch: agent/kdsl-packet-validator\nexpected_sample_total: 69\n\n```text\nvalidator未実行→pass扱禁止\nCI pending\nPacket validator pass != semantic equivalence/safety proof/normalization proof/RT:v/authority/release readiness\n```\n""",
    encoding='utf-8',
)

# Validator README.
replace_once(
    'tools/validator/README.md',
    'KDSL / R1 / R1C / Template / CompactPrompt / Safety Gate Registry をPython等で機械検査',
    'KDSL / R1 / R1C / Packet / Template / CompactPrompt / Safety Gate Registry をPython等で機械検査',
)
replace_once(
    'tools/validator/README.md',
    'spec/lint/kdsl-r1c-lint.md\nspec/r1/r1-result-spec.md',
    'spec/lint/kdsl-r1c-lint.md\nspec/lint/kdsl-packet-lint.md\nspec/packet/kdsl-packet-schema.md\nspec/r1/r1-result-spec.md',
)
replace_once(
    'tools/validator/README.md',
    'spec/registry/kdsl-safety-gate-composition.md\ntemplates/README.md',
    'spec/registry/kdsl-safety-gate-composition.md\nspec/registry/kdsl-packet-base-registry.md\nspec/registry/kdsl-packet-task-registry.md\nspec/registry/kdsl-packet-flow-registry.md\ntemplates/README.md',
)
replace_once(
    'tools/validator/README.md',
    """kdsl_r1c.py:
  KDSL_RESULT + kdsl-r1c@0.1-draft detection
  Full R1 fallback/out-of-scope separation
  canonical required field presence/order
  short alias rejection
  JSON-compatible structured field lint
  VERIFY class separation
  RT state/basis heuristic lint
  NEXT proposal_only lint
  COMMIT actual/proposed/permission basis lint

kdsl_validate.py:
  target wrapper: r1 / prompt / compact / safety-gate / r1c / all""",
    """kdsl_r1c.py:
  KDSL_RESULT + kdsl-r1c@0.1-draft detection
  Full R1 fallback/out-of-scope separation
  canonical required field presence/order
  short alias rejection
  JSON-compatible structured field lint
  VERIFY class separation
  RT state/basis heuristic lint
  NEXT proposal_only lint
  COMMIT actual/proposed/permission basis lint

kdsl_packet.py:
  PACKET_DRAFT + kdsl-packet@0.1-draft detection
  required field presence/order
  BASE/TASK/FLOW/SG registry and known ID checks
  TASK minimum gate/flow checks
  AUTHORITY/NORMALIZE/OUT boundary checks
  PKT:v1 and representative trigger checks

kdsl_validate.py:
  target wrapper: r1 / prompt / compact / safety-gate / r1c / packet / all""",
)
replace_once(
    'tools/validator/README.md',
    """R1C first slice candidate:
  total: 49 / failed: 0
```""",
    """R1C first slice candidate:
  total: 49 / failed: 0

Packet first slice candidate:
  expected total: 69 / branch validation pending
```""",
)
replace_once(
    'tools/validator/README.md',
    'examples/r1c/r1c-needs-user.example.md\n```',
    'examples/r1c/r1c-needs-user.example.md\nexamples/packet/packet-design.example.md\n```',
)
replace_once(
    'tools/validator/README.md',
    'tools/validator/verification/kdsl_r1c_verify.md\n```',
    'tools/validator/verification/kdsl_r1c_verify.md\ntools/validator/verification/kdsl_packet_verify.md\n```',
)
replace_once(
    'tools/validator/README.md',
    'R1C Full R1 fallback分離\nEVIDENCEの観測/推論/未観測/未確認分離検査設計',
    'R1C Full R1 fallback分離\nPacket envelope/registry/gate/flow/authority/normalization境界検出\nEVIDENCEの観測/推論/未観測/未確認分離検査設計',
)
replace_once(
    'tools/validator/README.md',
    'R1C canonical/stable promotionを判定しない\nPacket readinessを判定しない',
    'R1C canonical/stable promotionを判定しない\nPacket execution/normalization readinessを判定しない',
)
replace_once(
    'tools/validator/README.md',
    '  kdsl_r1c.py\n  kdsl-r1c-implementation-notes.md\n  kdsl_validate.py',
    '  kdsl_r1c.py\n  kdsl-r1c-implementation-notes.md\n  kdsl_packet.py\n  kdsl-packet-implementation-notes.md\n  kdsl_validate.py',
)
replace_once(
    'tools/validator/README.md',
    '## 設計方針',
    """## Packet first-slice checks

```text
schema:=kdsl-packet@0.1-draft
envelope:=PACKET_DRAFT
status:=non-executable
required fields/order:=SCHEMA..NORMALIZE
registries:=BASE/TASK/FLOW/SG
TASK minimum flow/gate matrix
AUTHORITY rails:=read/edit/stage/commit/push/release
NORMALIZE:=required true / state not_normalized / BASE target match
PKT:v1:=error
out-of-scope document:=pass/info
```

Boundary:

```text
first PACKET_DRAFT block only
line-based YAML-like parsing
full Safety Gate state/evidence validationなし
normalization transformer/round-trip proofなし
Packet validator pass != executable/normalized/authority/safety proof
```

## 設計方針""",
)
replace_once(
    'tools/validator/README.md',
    'single SAFETY_GATES blockのみ解析\nfirst KDSL_RESULT blockのみ解析',
    'single SAFETY_GATES blockのみ解析\nfirst KDSL_RESULT blockのみ解析\nfirst PACKET_DRAFT blockのみ解析',
)
replace_once(
    'tools/validator/README.md',
    'R1C round-trip semantic proofなし\nruntime実行なし',
    'R1C round-trip semantic proofなし\nPacket full YAML/semantic parserなし\nPacket normalization round-trip proofなし\nruntime実行なし',
)
replace_once(
    'tools/validator/README.md',
    'R1C validator pass != Packet readiness\nvalidator failure時',
    'R1C validator pass != Packet readiness\nPacket validator pass != Packet executable/normalized/authority\nvalidator failure時',
)

# Wrapper usage document.
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    """--target r1c
  runs:
    kdsl_r1c.py

--target all""",
    """--target r1c
  runs:
    kdsl_r1c.py

--target packet
  runs:
    kdsl_packet.py

--target all""",
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '    kdsl_safety_gate.py\n    kdsl_r1c.py\n```',
    '    kdsl_safety_gate.py\n    kdsl_r1c.py\n    kdsl_packet.py\n```',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    """R1C checker:
  KDSL_RESULTなし→pass/info
  KDSL_RESULTあり + SCHEMAなし→Full R1 fallback / pass/info
  unknown SCHEMA→fail
```""",
    """R1C checker:
  KDSL_RESULTなし→pass/info
  KDSL_RESULTあり + SCHEMAなし→Full R1 fallback / pass/info
  unknown SCHEMA→fail

Packet checker:
  PACKET_DRAFTなし→pass/info
  Packet SCHEMAのみ + PACKET_DRAFTなし→fail
  unknown SCHEMA/registry/ID/opcode→fail
```""",
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'python tools/validator/kdsl_validate.py --target r1c examples/r1c/r1c-success.example.md\npython tools/validator/kdsl_validate.py --target all',
    'python tools/validator/kdsl_validate.py --target r1c examples/r1c/r1c-success.example.md\npython tools/validator/kdsl_validate.py --target packet examples/packet/packet-design.example.md\npython tools/validator/kdsl_validate.py --target all',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '## Sample verification',
    """## Packet first-slice scope

```text
schema/envelope/status exact checks
required field presence/order
BASE/TASK/FLOW/SG known registry/ID checks
TASK minimum gate/flow matrix
FLOW-CHANGE ordering
AUTHORITY rails/values
NORMALIZE required/target/state
OUT.result_schema representative values
PKT:v1 and representative trigger checks
out-of-scope separation
```

Not covered:

```text
full YAML parser
full natural-language trigger parser
Safety Gate state/evidence deep lint
protected wording semantic equivalence
normalization transformer/round-trip proof
execution authority/readiness
```

## Sample verification""",
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    """R1C first slice candidate:
  total: 49 / failed: 0
```""",
    """R1C first slice candidate:
  total: 49 / failed: 0

Packet first slice candidate:
  expected total: 69 / branch validation pending
```""",
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'examples/r1c/r1c-needs-user.example.md\n```',
    'examples/r1c/r1c-needs-user.example.md\nexamples/packet/packet-design.example.md\n```',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'tools/validator/verification/kdsl_r1c_verify.md\n```',
    'tools/validator/verification/kdsl_r1c_verify.md\ntools/validator/verification/kdsl_packet_verify.md\n```',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    '--target r1c does not validate Full R1 Evidence/Authority semantics beyond first-slice shape\n--target all',
    '--target r1c does not validate Full R1 Evidence/Authority semantics beyond first-slice shape\n--target packet does not prove Packet normalization/execution/authority semantics\n--target all',
)
replace_once(
    'tools/validator/kdsl_validate_usage.md',
    'R1C validator implementation != Packet readiness\n```',
    'R1C validator implementation != Packet readiness\nPacket validator implementation != Packet executable/normalized/readiness\n```',
)

# Root README.
replace_once(
    'README.md',
    'Packet validator: not implemented\nvalidator sample suite: 49 expectations',
    'Packet validator: first heuristic slice integration pending\nvalidator sample suite: 69 expectations candidate',
)
replace_once(
    'README.md',
    '  tools/validator/kdsl_r1c.py\n  tools/validator/run_samples.py',
    '  tools/validator/kdsl_r1c.py\n  tools/validator/kdsl_packet.py\n  tools/validator/run_samples.py',
)
replace_once(
    'README.md',
    """python tools/validator/kdsl_validate.py --target r1c <file>
python tools/validator/kdsl_validate.py --target all <file>""",
    """python tools/validator/kdsl_validate.py --target r1c <file>
python tools/validator/kdsl_validate.py --target packet <file>
python tools/validator/kdsl_validate.py --target all <file>""",
)
replace_once(
    'README.md',
    'examples/r1c/r1c-needs-user.example.md\n```',
    'examples/r1c/r1c-needs-user.example.md\nexamples/packet/packet-design.example.md\n```',
)
replace_once(
    'README.md',
    'Packet validator/sample matrix未実装\nPacket normalization transformer/round-trip proofなし',
    'Packet validator first slice:=integration pending\nPacket full YAML/semantic parserなし\nPacket normalization transformer/round-trip proofなし',
)
replace_once(
    'README.md',
    """P1:
  Packet validator first slice
  Packet positive/negative sample matrix""",
    """P0:
  PR #13 CI確認 / squash merge / Packet validator closeout

P1:
  Packet normalization round-trip tooling/tests""",
)
replace_once(
    'README.md',
    """P2:
  Packet normalization round-trip tooling/tests

P3:
  Safety Gate protected wording/inheritance validator拡張

P4:
  R1C round-trip/property-based validator検討

P5:""",
    """P2:
  Safety Gate protected wording/inheritance validator拡張

P3:
  R1C round-trip/property-based validator検討

P4:""",
)

# Changelog and operational status.
replace_once(
    'CHANGELOG.md',
    '### Added\n\n#### Packet v2-draft ownership alignment',
    """### Added

#### Packet validator first slice

- Added `tools/validator/kdsl_packet.py`.
- Added Packet envelope/required-field/order checks.
- Added BASE/TASK/FLOW/SG registry and known ID checks.
- Added TASK minimum Safety Gate/FLOW matrix checks.
- Added AUTHORITY/NORMALIZE/OUT boundary checks.
- Added PKT:v1 and representative trigger checks.
- Added `--target packet` and Packet checking to `--target all`.
- Expanded the candidate sample suite from 49 to 69 expectations.
- Added actual `examples/packet/packet-design.example.md` coverage.
- Packet execution/normalization readiness remains explicitly out of scope.

#### Packet v2-draft ownership alignment""",
)
replace_once(
    'CHANGELOG.md',
    'Packet lint:=v2-draft adopted / validator not implemented\nnormalization transformer/round-trip proof:=not implemented',
    'Packet lint:=v2-draft adopted / validator first slice integration pending\nPacket sample suite:=69 expectations candidate\nnormalization transformer/round-trip proof:=not implemented',
)

replace_once(
    'docs/project-status.md',
    '## 3. Current architecture direction',
    """### PR #13 — Packet validator first slice

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
```

## 3. Current architecture direction""",
)
replace_once(
    'docs/project-status.md',
    'Packet ownership:=v2-draft adopted authoring schema/registries/lint\nKDSL-Packet:=non-executable / normalization required',
    'Packet ownership:=v2-draft adopted authoring schema/registries/lint\nPacket validator first slice:=integration pending\nKDSL-Packet:=non-executable / normalization required',
)
replace_once(
    'docs/project-status.md',
    '  validator: not_implemented',
    '  validator: first_slice_integration_pending',
)
replace_once(
    'docs/project-status.md',
    """    - r1c
    - all
  current_main_scope:""",
    """    - r1c
    - packet
    - all
  current_main_scope:""",
)
replace_once(
    'docs/project-status.md',
    '    - Full R1 fallback/out-of-scope separation\n  ci:',
    '    - Full R1 fallback/out-of-scope separation\n    - Packet envelope/field/order lint\n    - Packet registry/ID/gate/flow/authority/normalization lint\n    - Packet out-of-scope separation\n  ci:',
)
replace_once(
    'docs/project-status.md',
    '    expected_sample_total: 49\n    latest_pr_validation:',
    '    expected_sample_total: 69\n    latest_pr_validation:',
)
replace_once(
    'docs/project-status.md',
    'Packet validator/sample matrix\nPacket normalization transformer/round-trip proof',
    'Packet full YAML/semantic parser\nPacket Safety Gate state/evidence deep lint\nPacket normalization transformer/round-trip proof',
)
replace_once(
    'docs/project-status.md',
    '### R1C validator\n',
    """### Packet validator candidate

```yaml
pull_request: 13
branch: agent/kdsl-packet-validator
expected_sample_total: 69
status: branch_validation_pending
meaning: Packet first-slice heuristic candidate; not Packet execution/normalization proof
```

### R1C validator
""",
)
replace_once(
    'docs/project-status.md',
    'Packet validator/sample matrix未実装\nPacket normalization transformer/round-trip proofなし',
    'Packet validator first slice:=integration pending\nPacket full YAML/semantic parserなし\nPacket normalization transformer/round-trip proofなし',
)
replace_once(
    'docs/project-status.md',
    'P0: PR #12 CI確認 / squash merge / Packet ownership closeout\nP1: Packet validator first slice / sample matrix\nP2: Packet normalization round-trip tooling/tests\nP3: Safety Gate protected wording/inheritance validator拡張\nP4: R1C round-trip/property-based validator検討\nP5: public-facing v2 overview / CI required check検討',
    'P0: PR #13 CI確認 / squash merge / Packet validator closeout\nP1: Packet normalization round-trip tooling/tests\nP2: Safety Gate protected wording/inheritance validator拡張\nP3: R1C round-trip/property-based validator検討\nP4: public-facing v2 overview / CI required check検討',
)

Path('.github/scripts/apply_packet_validator.py').unlink()
