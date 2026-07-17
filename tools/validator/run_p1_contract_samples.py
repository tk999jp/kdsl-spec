import copy
import subprocess
import sys
import tempfile
from pathlib import Path

from kdsl_p1_bootstrap import (
    compare_models,
    parse_contract,
    parse_p1_line,
    render_p1,
    split_p1_segments,
)

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
P1L_EXPLICIT = REPO_ROOT / 'examples/adps/p1l-investigate.example.md'
P1_PROFILE = REPO_ROOT / 'examples/adps/p1-profile-completed.example.md'
P1_UNKNOWN_PROFILE = REPO_ROOT / 'examples/adps/p1-unknown-profile-blocked.example.md'
P1L_AUTHORITY_MISSING = REPO_ROOT / 'examples/adps/p1-authority-missing-blocked.example.md'


def run_cli(name, script, path, expected, contains=()):
    result = subprocess.run(
        [sys.executable, str(ROOT / script), str(path)],
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


def explicit_model():
    result = parse_contract(P1L_EXPLICIT.read_text(encoding='utf-8'), expected='P1L')
    if result.errors or result.model is None:
        raise AssertionError('explicit P1L example did not parse: ' + repr(result.errors))
    return result.model


def check(name, condition, detail=''):
    ok = bool(condition)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    if not ok and detail:
        print('  ' + detail)
    return ok


def main():
    results = []
    results.append(
        run_cli(
            'explicit P1L accepted',
            'kdsl_p1l.py',
            P1L_EXPLICIT,
            0,
            ('STATUS: pass', 'KIND: P1L', 'EXECUTABLE: no'),
        )
    )
    results.append(
        run_cli(
            'profile-completed P1 accepted',
            'kdsl_p1.py',
            P1_PROFILE,
            0,
            ('STATUS: pass', 'KIND: P1', 'EXECUTION_AUTHORITY: none'),
        )
    )
    results.append(
        run_cli(
            'unknown profile P1 rejected',
            'kdsl_p1.py',
            P1_UNKNOWN_PROFILE,
            2,
            ('STATUS: fail', 'PROFILE.revision requires exact profile evidence'),
        )
    )
    results.append(
        run_cli(
            'missing authority rails P1L rejected',
            'kdsl_p1l.py',
            P1L_AUTHORITY_MISSING,
            2,
            ('STATUS: fail', 'missing AUTHORITY rail: push'),
        )
    )
    results.append(
        run_cli(
            'P1L structural round trip passes',
            'kdsl_p1_roundtrip.py',
            P1L_EXPLICIT,
            0,
            ('STATUS: structural_pass', 'all eight authority rails preserved'),
        )
    )
    results.append(
        run_cli(
            'P1 structural round trip passes',
            'kdsl_p1_roundtrip.py',
            P1_PROFILE,
            0,
            ('STATUS: structural_pass', 'SOURCE_KIND: P1'),
        )
    )

    model = explicit_model()

    pipe_model = copy.deepcopy(model)
    pipe_model['GOAL']['questions'] = ['left|right']
    pipe_line = render_p1(pipe_model)
    pipe_result = parse_p1_line(pipe_line)
    pipe_ok = not pipe_result.errors and pipe_result.model is not None and not compare_models(pipe_model, pipe_result.model)
    results.append(check('pipe inside JSON string is not split', pipe_ok, repr(pipe_result.errors)))

    exact_model = copy.deepcopy(model)
    exact_value = r'G:\source\repos\MidFD\MainForm.cs'
    exact_model['SCOPE']['target'] = [exact_value]
    exact_model['AUTHORITY']['edit'] = 'target_only'
    exact_line = render_p1(exact_model)
    exact_result = parse_p1_line(exact_line)
    exact_ok = (
        not exact_result.errors
        and exact_result.model is not None
        and exact_result.model['SCOPE']['target'] == [exact_value]
    )
    results.append(check('Windows path exact string survives P1 JSON round trip', exact_ok, repr(exact_result.errors)))

    runtime_model = copy.deepcopy(model)
    runtime_model['RUNTIME']['disposition'] = 'v'
    runtime_result = parse_p1_line(render_p1(runtime_model))
    results.append(
        check(
            'pre-execution RT:v claim rejected',
            any('result-only RT claim prohibited' in item for item in runtime_result.errors),
            repr(runtime_result.errors),
        )
    )

    authority_model = copy.deepcopy(model)
    authority_model['AUTHORITY'].pop('push')
    authority_result = parse_p1_line(render_p1(authority_model))
    results.append(
        check(
            'authority rail removal detected',
            any('AUTHORITY key order mismatch' in item or 'missing AUTHORITY rail: push' in item for item in authority_result.errors),
            repr(authority_result.errors),
        )
    )

    canonical_line = render_p1(model)
    segments = split_p1_segments(canonical_line)
    segments[2], segments[3] = segments[3], segments[2]
    wrong_order = 'P1|' + '|'.join(key + '=' + value for key, value in segments)
    order_result = parse_p1_line(wrong_order)
    results.append(
        check(
            'P1 segment order mutation detected',
            any('P1 segment order mismatch' in item for item in order_result.errors),
            repr(order_result.errors),
        )
    )

    legacy = 'P1|M:contract_rev=0.1,loss=L|T:I|S:scope|G:ro|V:none|X:missing|O:std'
    legacy_result = parse_contract(legacy, expected='P1')
    results.append(
        check(
            'legacy colon P1 cannot self-promote',
            any('legacy operational P1 colon syntax' in item for item in legacy_result.errors),
            repr(legacy_result.errors),
        )
    )

    blocked_model = copy.deepcopy(model)
    blocked_model['NORMALIZATION']['state'] = 'blocked'
    blocked_model['NORMALIZATION']['unresolved'] = ['unknown profile alias']
    blocked_result = parse_p1_line(render_p1(blocked_model))
    results.append(
        check(
            'explicit blocked normalization remains unusable',
            any('NORMALIZATION.state is blocked' in item for item in blocked_result.errors),
            repr(blocked_result.errors),
        )
    )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        mixed = tmp_path / 'mixed.md'
        mixed.write_text(P1L_EXPLICIT.read_text(encoding='utf-8') + '\n' + canonical_line + '\n', encoding='utf-8')
        results.append(
            run_cli(
                'mixed P1L and P1 source rejected',
                'kdsl_p1_auto.py',
                mixed,
                2,
                ('mixed P1L and P1 contract sources are not allowed',),
            )
        )

    failed = sum(not item for item in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
