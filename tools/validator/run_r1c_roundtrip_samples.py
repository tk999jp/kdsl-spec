import copy
import subprocess
import sys
import tempfile
from pathlib import Path

from kdsl_r1c_roundtrip import compare_models, parse_model, project_to_full_r1, reconstruct_r1c

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SUCCESS = REPO_ROOT / 'examples/r1c/r1c-success.example.md'
BLOCKED = REPO_ROOT / 'examples/r1c/r1c-blocked.example.md'
NEEDS_USER = REPO_ROOT / 'examples/r1c/r1c-needs-user.example.md'
INVALID = ROOT / 'samples/sample_r1c_invalid_rt.md'


def run_cli(name, path, expected, contains=()):
    result = subprocess.run(
        [sys.executable, str(ROOT / 'kdsl_r1c_roundtrip.py'), str(path)],
        capture_output=True,
        text=True,
    )
    ok = result.returncode == expected and all(marker in result.stdout for marker in contains)
    label = 'PASS' if ok else 'FAIL'
    print(f'{label}: {name}')
    print(f'  expected: {expected}')
    print(f'  actual: {result.returncode}')
    if not ok:
        print('  stdout:')
        print('\n'.join('    ' + line for line in result.stdout.splitlines()))
        if result.stderr:
            print('  stderr:')
            print('\n'.join('    ' + line for line in result.stderr.splitlines()))
    return ok


def success_model():
    return parse_model(SUCCESS.read_text(encoding='utf-8'))


def find_field(projection, key):
    for index, (field, value) in enumerate(projection['fields']):
        if field == key:
            return index, value
    raise KeyError(key)


def property_case(name, mutate, expected_marker):
    source = success_model()
    projection = project_to_full_r1(source)
    mutate(projection)
    reconstructed = reconstruct_r1c(projection)
    mismatches = compare_models(source, reconstructed)
    ok = any(expected_marker in item for item in mismatches)
    label = 'PASS' if ok else 'FAIL'
    print(f'{label}: {name}')
    if not ok:
        print('  mismatches: ' + repr(mismatches))
    return ok


def optional_doc():
    text = SUCCESS.read_text(encoding='utf-8')
    needle = 'COMMIT:{"actual":"05773b4 Validator: add Safety Gate Registry first heuristic lint","proposed":null,"permission_basis":"U承認"}'
    replacement = needle + '\n' + (
        'EVIDENCE:{"observed":["CI success"],"inferred":[],"not_observed":[],"unverified":["local rerun"]}\n'
        'AUTHORITY:{"read":"allow","edit":"target_only","stage":"not_requested","commit":"propose_only","push":"forbid","release":"forbid"}'
    )
    return text.replace(needle, replacement)


def safety_gate_doc():
    text = SUCCESS.read_text(encoding='utf-8')
    needle = 'COMMIT:{"actual":"05773b4 Validator: add Safety Gate Registry first heuristic lint","proposed":null,"permission_basis":"U承認"}'
    replacement = needle + '\n' + (
        'SAFETY_GATES:\n'
        '  registry: kdsl-sg@0.1-draft\n'
        '  entries:\n'
        '    - id: SG-EVIDENCE\n'
        '      state: hold\n'
        '      scope: round-trip proof\n'
        '      reason: semantic equivalence not proven\n'
    )
    return text.replace(needle, replacement)


def main():
    results = []
    results.append(run_cli('success example structural pass', SUCCESS, 0, ('STATUS: structural_pass', 'SEMANTIC_EQUIVALENCE: not_proven')))
    results.append(run_cli('blocked result structural pass', BLOCKED, 0, ('STATUS: structural_pass', 'RT state/basis preserved')))
    results.append(run_cli('needs-user result structural pass', NEEDS_USER, 0, ('STATUS: structural_pass', 'NEXT proposal_only boundary preserved')))
    results.append(run_cli('invalid R1C rejected', INVALID, 2, ('STATUS: fail', 'source R1C failed validator')))

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        optional_path = tmp_path / 'optional.md'
        optional_path.write_text(optional_doc(), encoding='utf-8')
        results.append(run_cli('optional evidence and authority structural pass', optional_path, 0, ('optional JSON blocks preserved',)))

        safety_path = tmp_path / 'safety.md'
        safety_path.write_text(safety_gate_doc(), encoding='utf-8')
        results.append(run_cli('optional Safety Gates safely blocked', safety_path, 1, ('STATUS: blocked', 'does not claim safe SAFETY_GATES round-trip')))

    def mutate_files_order(projection):
        index, value = find_field(projection, 'FILES')
        projection['fields'][index] = ('FILES', list(reversed(value)))

    def mutate_cmd(projection):
        index, value = find_field(projection, 'CMD')
        projection['fields'][index] = ('CMD', value + ['python invented.py'])

    def mutate_verify(projection):
        index, value = find_field(projection, 'VERIFY')
        changed = copy.deepcopy(value)
        item = changed['not_run'].pop()
        changed['pass'].append(item)
        projection['fields'][index] = ('VERIFY', changed)

    def mutate_rt(projection):
        index, value = find_field(projection, 'RT')
        changed = copy.deepcopy(value)
        changed['state'] = 'v'
        projection['fields'][index] = ('RT', changed)

    def mutate_next(projection):
        index, value = find_field(projection, 'NEXT')
        changed = copy.deepcopy(value)
        changed['authority'] = 'allow_once'
        projection['fields'][index] = ('NEXT', changed)

    def mutate_commit(projection):
        index, value = find_field(projection, 'COMMIT')
        changed = copy.deepcopy(value)
        changed['actual'] = None
        changed['proposed'] = value['actual']
        projection['fields'][index] = ('COMMIT', changed)

    def mutate_required_order(projection):
        projection['field_order'][0], projection['field_order'][1] = projection['field_order'][1], projection['field_order'][0]

    results.append(property_case('FILES order mutation detected', mutate_files_order, 'required field changed: FILES'))
    results.append(property_case('CMD exact-string mutation detected', mutate_cmd, 'required field changed: CMD'))
    results.append(property_case('VERIFY class mutation detected', mutate_verify, 'required field changed: VERIFY'))
    results.append(property_case('RT mutation detected', mutate_rt, 'required field changed: RT'))
    results.append(property_case('NEXT authority mutation detected', mutate_next, 'required field changed: NEXT'))
    results.append(property_case('COMMIT actual/proposed mutation detected', mutate_commit, 'required field changed: COMMIT'))
    results.append(property_case('required field order mutation detected', mutate_required_order, 'required field order changed'))

    optional_source = parse_model(optional_doc())
    optional_projection = project_to_full_r1(optional_source)
    optional_projection['optional'][0][1]['observed'].append('invented observation')
    optional_mismatches = compare_models(optional_source, reconstruct_r1c(optional_projection))
    optional_ok = any('optional field changed: EVIDENCE' in item for item in optional_mismatches)
    print(('PASS' if optional_ok else 'FAIL') + ': optional EVIDENCE mutation detected')
    results.append(optional_ok)

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print(f'  total: {len(results)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
