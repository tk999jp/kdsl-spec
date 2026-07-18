import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from kdsl_parser_v2 import DocumentNodeV2
from kdsl_runtime_control import (
    AUTHORITY_RAILS,
    C14N_ID,
    CONTRACT_SCHEMAS,
    K1_SCHEMA_ID,
    K1_STATUS,
    PF1_SCHEMA_ID,
    PF1_STATUS,
    RESULT_SCHEMAS,
    compute_digest,
    parse_definition,
    resolve_runtime_control,
)

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
K1_SAMPLE = REPO_ROOT / 'examples/runtime/k1-canonical.example.md'


def check(name, condition, detail=''):
    ok = bool(condition)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    if not ok and detail:
        print('  ' + detail)
    return ok


def run_cli(name, script, paths, expected, contains=()):
    result = subprocess.run(
        [sys.executable, str(ROOT / script), *(str(path) for path in paths)],
        capture_output=True,
        text=True,
    )
    ok = result.returncode == expected and all(marker in result.stdout for marker in contains)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    print('  expected: ' + str(expected))
    print('  actual: ' + str(result.returncode))
    if not ok:
        print('  stdout:')
        print('\n'.join('    ' + line for line in result.stdout.splitlines()))
        if result.stderr:
            print('  stderr:')
            print('\n'.join('    ' + line for line in result.stderr.splitlines()))
    return ok


def build_pf1_model(k1_model):
    ceiling = {
        rail: {
            'mode': 'allow_max' if rail == 'read' else 'forbid',
            'scope': 'any',
            'cardinality': 'any',
        }
        for rail in AUTHORITY_RAILS
    }
    model = {
        'SCHEMA': PF1_SCHEMA_ID,
        'STATUS': PF1_STATUS,
        'IDENTITY': {
            'id': 'kdsl.reference.profile',
            'revision': '0.1.0',
            'canonicalization': C14N_ID,
            'digest': 'sha256:' + ('0' * 64),
            'source_ref': 'generated:runtime-control-corpus/pf1',
        },
        'KERNEL_REF': {
            'id': k1_model['IDENTITY']['id'],
            'revision': k1_model['IDENTITY']['revision'],
            'digest': k1_model['IDENTITY']['digest'],
        },
        'PROJECT': {
            'id': 'kdsl-spec',
            'repository': 'tk999jp/kdsl-spec',
            'root_ref': 'repository:tk999jp/kdsl-spec',
        },
        'APPLIES_TO': {
            'contract_schemas': list(CONTRACT_SCHEMAS),
            'task_kinds': ['docs', 'review'],
            'excluded_task_kinds': ['implement', 'fix'],
        },
        'DEFAULTS': {
            'guard': 'none',
            'verify': 'none',
            'stop': 'none',
            'output': 'none',
            'runtime_disposition': 'not_applicable',
            'result_schema': RESULT_SCHEMAS[0],
        },
        'PRESETS': {
            'guard': [],
            'verify': [],
            'stop': [],
            'output': [],
            'runtime': [],
        },
        'ALIASES': [],
        'RESTRICTIONS': [],
        'AUTHORITY_CEILING': ceiling,
        'CAPABILITY_REQUIREMENTS': [],
        'ROUTING': [],
        'RUNTIME_POLICY': {
            'code_change_default': 'user_required',
            'docs_only_default': 'not_applicable',
            'state_only_default': 'not_applicable',
        },
        'RESULT_POLICY': {
            'result_schema': RESULT_SCHEMAS[0],
            'report_requirements': [
                'KDSL_RESULT',
                'RT_boundary',
                'NEXT_proposal_only',
                'COMMIT_non_authoritative',
            ],
        },
        'COMPATIBILITY': {
            'legacy_profile_ids': [],
            'legacy_aliases': [],
            'migration_notes': [],
        },
    }
    model['IDENTITY']['digest'] = compute_digest('PF1', model)
    return model


def render_scalar(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def render_mapping(mapping, indent):
    lines = []
    prefix = ' ' * indent
    for key, value in mapping.items():
        if isinstance(value, dict):
            lines.append(prefix + key + ':')
            lines.extend(render_mapping(value, indent + 2))
        else:
            lines.append(prefix + key + ': ' + render_scalar(value))
    return lines


def render_envelope(kind, model):
    lines = [kind + ':']
    for key, value in model.items():
        if isinstance(value, dict):
            lines.append(key + ':')
            lines.extend(render_mapping(value, 2))
        else:
            lines.append(key + ': ' + render_scalar(value))
    return '\n'.join(lines) + '\n'


def main():
    results = []
    k1_text = K1_SAMPLE.read_text(encoding='utf-8')
    k1 = parse_definition(k1_text, 'K1')
    results.append(check('canonical K1 parses', not k1.errors, repr(k1.errors)))
    if k1.model is None:
        print('SUMMARY:')
        print('  total: ' + str(len(results)))
        print('  failed: 1')
        return 1

    pf1_model = build_pf1_model(k1.model)
    pf1_text = render_envelope('PF1', pf1_model)
    pf1 = parse_definition(pf1_text, 'PF1')
    results.append(check('generated canonical PF1 parses', not pf1.errors, repr(pf1.errors)))

    k1_ast = DocumentNodeV2.parse(k1_text, context='raw-envelope')
    pf1_ast = DocumentNodeV2.parse(pf1_text, context='raw-envelope')
    results.append(check('shared AST recognizes K1', len(k1_ast.envelopes('K1')) == 1, repr(k1_ast.errors)))
    results.append(check('shared AST recognizes PF1', len(pf1_ast.envelopes('PF1')) == 1, repr(pf1_ast.errors)))

    compatibility = resolve_runtime_control(k1, pf1)
    results.append(
        check(
            'K1 PF1 exact compatibility resolves',
            not compatibility.errors
            and compatibility.runtime_control_state == 'valid'
            and compatibility.executable is False
            and compatibility.execution_authority == 'none',
            repr(compatibility.errors),
        )
    )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pf1_path = tmp_path / 'pf1.md'
        pf1_path.write_text(pf1_text, encoding='utf-8')
        results.append(
            run_cli(
                'K1 CLI accepts canonical sample',
                'kdsl_k1.py',
                [K1_SAMPLE],
                0,
                ('STATUS: pass', 'KIND: K1', 'EXECUTABLE: no', 'EXECUTION_AUTHORITY: none'),
            )
        )
        results.append(
            run_cli(
                'PF1 CLI accepts generated sample',
                'kdsl_pf1.py',
                [pf1_path],
                0,
                ('STATUS: pass', 'KIND: PF1', 'EXECUTABLE: no', 'EXECUTION_AUTHORITY: none'),
            )
        )
        results.append(
            run_cli(
                'compatibility CLI remains non-executable',
                'kdsl_runtime_control_compatibility.py',
                [K1_SAMPLE, pf1_path],
                0,
                ('STATUS: valid', 'RUNTIME_CONTROL_STATE: valid', 'EXECUTABLE: false', 'EXECUTION_AUTHORITY: none'),
            )
        )

    digest_mutation = copy.deepcopy(pf1_model)
    digest_mutation['IDENTITY']['digest'] = 'sha256:' + ('f' * 64)
    digest_result = parse_definition(render_envelope('PF1', digest_mutation), 'PF1')
    results.append(
        check(
            'PF1 self-digest mismatch rejected',
            any('IDENTITY.digest mismatch' in item for item in digest_result.errors),
            repr(digest_result.errors),
        )
    )

    ref_mutation = copy.deepcopy(pf1_model)
    ref_mutation['KERNEL_REF']['digest'] = 'sha256:' + ('9' * 64)
    ref_mutation['IDENTITY']['digest'] = compute_digest('PF1', ref_mutation)
    ref_result = parse_definition(render_envelope('PF1', ref_mutation), 'PF1')
    ref_compatibility = resolve_runtime_control(k1, ref_result)
    results.append(
        check(
            'PF1 KERNEL_REF mismatch blocked',
            any('PF1 KERNEL_REF mismatch' in item for item in ref_compatibility.errors),
            repr(ref_compatibility.errors),
        )
    )

    ceiling_mutation = copy.deepcopy(pf1_model)
    ceiling_mutation['AUTHORITY_CEILING']['read']['mode'] = 'grant'
    ceiling_mutation['IDENTITY']['digest'] = compute_digest('PF1', ceiling_mutation)
    ceiling_result = parse_definition(render_envelope('PF1', ceiling_mutation), 'PF1')
    results.append(
        check(
            'unknown PF1 authority ceiling mode rejected',
            any('AUTHORITY_CEILING.read.mode is unknown' in item for item in ceiling_result.errors),
            repr(ceiling_result.errors),
        )
    )

    capability_mutation = copy.deepcopy(k1.model)
    capability_mutation['CAPABILITY_POLICY']['capability_is_permission'] = True
    capability_mutation['IDENTITY']['digest'] = compute_digest('K1', capability_mutation)
    capability_result = parse_definition(render_envelope('K1', capability_mutation), 'K1')
    results.append(
        check(
            'capability cannot become permission',
            any('CAPABILITY_POLICY.capability_is_permission' in item for item in capability_result.errors),
            repr(capability_result.errors),
        )
    )

    duplicate_result = parse_definition(k1_text + '\n' + k1_text, 'K1')
    results.append(
        check(
            'duplicate K1 envelope rejected',
            any('duplicate K1 envelopes detected' in item for item in duplicate_result.errors),
            repr(duplicate_result.errors),
        )
    )

    failed = sum(not item for item in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
