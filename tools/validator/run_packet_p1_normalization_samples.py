from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE = REPO_ROOT / 'examples/packet/packet-p1l-normalization.example.md'


def run(name: str, script: str, args: list[str], expected: int, contains: tuple[str, ...] = ()) -> bool:
    proc = subprocess.run(
        [sys.executable, str(ROOT / script), *args],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    ok = proc.returncode == expected and all(marker in proc.stdout for marker in contains)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    print('  expected: ' + str(expected))
    print('  actual: ' + str(proc.returncode))
    if not ok:
        print('  stdout:')
        print('\n'.join('    ' + line for line in proc.stdout.splitlines()))
        if proc.stderr:
            print('  stderr:')
            print('\n'.join('    ' + line for line in proc.stderr.splitlines()))
    return ok


def generate(source_path: Path) -> str:
    proc = subprocess.run(
        [sys.executable, str(ROOT / 'kdsl_packet_normalize_p1.py'), str(source_path)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return proc.stdout


def run_property_text(name: str, source_text: str, normalization_text: str, expected: int, contains=()) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        source_path = Path(tmp) / 'source.md'
        normalization_path = Path(tmp) / 'normalization.md'
        source_path.write_text(source_text, encoding='utf-8')
        normalization_path.write_text(normalization_text, encoding='utf-8')
        return run(
            name,
            'kdsl_packet_p1_property.py',
            [str(source_path), str(normalization_path)],
            expected,
            tuple(contains),
        )


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise AssertionError('mutation anchor not found: ' + old)
    return text.replace(old, new, 1)


def mutate_projection(normalization: str, mutator) -> str:
    match = re.search(r'^(\s*PROJECTION_JSON: )(\{.*\})$', normalization, re.MULTILINE)
    if match is None:
        raise AssertionError('P1L projection JSON not found')
    model = json.loads(match.group(2))
    mutator(model)
    rendered = json.dumps(model, ensure_ascii=False, separators=(',', ':'))
    return normalization[:match.start(2)] + rendered + normalization[match.end(2):]


def main() -> int:
    source_text = SOURCE.read_text(encoding='utf-8')
    normalization_p1l = generate(SOURCE)
    results: list[bool] = []

    results.append(run('P1L source semantic pass', 'kdsl_packet_semantic.py', [str(SOURCE)], 0, ('STATUS: pass',)))
    results.append(
        run(
            'P1L mapper pass',
            'kdsl_packet_normalize_p1.py',
            [str(SOURCE)],
            0,
            ('TARGET:', 'schema: kdsl-p1l@0.1-draft', 'marker: P1L_PREVIEW', 'execution_authority: none'),
        )
    )
    results.append(
        run(
            'generated P1L property pass',
            'kdsl_packet_p1_property.py',
            [str(SOURCE)],
            0,
            ('STATUS: property_pass', 'public_repo/destructive_ops explicitly narrowed to forbid'),
        )
    )
    results.append(run_property_text('supplied P1L property pass', source_text, normalization_p1l, 0, ('STATUS: property_pass',)))

    p1_source_text = replace_once(source_text, '  target: P1L', '  target: P1')
    with tempfile.TemporaryDirectory() as tmp:
        p1_source = Path(tmp) / 'p1-source.md'
        p1_source.write_text(p1_source_text, encoding='utf-8')
        normalization_p1 = generate(p1_source)
        results.append(
            run(
                'P1 mapper pass',
                'kdsl_packet_normalize_p1.py',
                [str(p1_source)],
                0,
                ('schema: kdsl-p1@0.1-draft', 'marker: P1_PREVIEW', 'SERIALIZATION_JSON:'),
            )
        )
        results.append(
            run(
                'generated P1 property pass',
                'kdsl_packet_p1_property.py',
                [str(p1_source)],
                0,
                ('STATUS: property_pass', 'P1 preview serialization reconstructs canonical P1L projection'),
            )
        )
        results.append(run_property_text('supplied P1 property pass', p1_source_text, normalization_p1, 0, ('STATUS: property_pass',)))

    results.append(
        run_property_text(
            'TARGET executable widening detected',
            source_text,
            replace_once(normalization_p1l, '  executable: false', '  executable: true'),
            2,
            ('TARGET.executable mismatch',),
        )
    )
    results.append(
        run_property_text(
            'preview marker execution-like mutation detected',
            source_text,
            replace_once(normalization_p1l, '    P1L_PREVIEW:', '    P1L:'),
            2,
            ('canonical P1L/P1 executable-looking marker exposed in preview',),
        )
    )

    widened = mutate_projection(normalization_p1l, lambda model: model['AUTHORITY'].__setitem__('edit', 'allow'))
    results.append(
        run_property_text(
            'source authority widening detected',
            source_text,
            widened,
            2,
            ('required field changed: AUTHORITY',),
        )
    )

    public_widened = mutate_projection(normalization_p1l, lambda model: model['AUTHORITY'].__setitem__('public_repo', 'allow'))
    results.append(
        run_property_text(
            'public_repo safety floor widening detected',
            source_text,
            public_widened,
            2,
            ('required field changed: AUTHORITY',),
        )
    )

    destructive_removed = mutate_projection(normalization_p1l, lambda model: model['AUTHORITY'].pop('destructive_ops'))
    results.append(
        run_property_text(
            'destructive_ops rail removal detected',
            source_text,
            destructive_removed,
            2,
            ('AUTHORITY key order mismatch',),
        )
    )

    binding_widened = mutate_projection(
        normalization_p1l,
        lambda model: model['BINDING'].update({'state': 'bound', 'executable': True}),
    )
    results.append(
        run_property_text(
            'runtime binding widening detected',
            source_text,
            binding_widened,
            2,
            ('BINDING.executable must be false',),
        )
    )

    results.append(
        run_property_text(
            'semantic equivalence claim detected',
            source_text,
            replace_once(normalization_p1l, 'semantic_equivalence: not_proven', 'semantic_equivalence: proven'),
            2,
            ('ROUND_TRIP boundary mismatch',),
        )
    )

    missing_map = re.sub(
        r'    - source: NORMALIZE\n      target: .*?\n      mode: .*?\n      evidence: .*?\n',
        '',
        normalization_p1l,
        count=1,
    )
    results.append(
        run_property_text(
            'missing Packet field mapping detected',
            source_text,
            missing_map,
            2,
            ('MAP sources missing: NORMALIZE',),
        )
    )

    blocked_source = replace_once(source_text, '  state: not_normalized', '  state: normalized')
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'blocked-source.md'
        path.write_text(blocked_source, encoding='utf-8')
        results.append(
            run(
                'normalized Packet self-claim rejected before mapping',
                'kdsl_packet_normalize_p1.py',
                [str(path)],
                2,
                (),
            )
        )

    wrong_base = replace_once(source_text, '  id: BASE-ADPS-P1', '  id: BASE-KDSL-DEV')
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'wrong-base.md'
        path.write_text(wrong_base, encoding='utf-8')
        results.append(
            run(
                'wrong BASE rejected by P1 mapper',
                'kdsl_packet_normalize_p1.py',
                [str(path)],
                2,
                (),
            )
        )

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
