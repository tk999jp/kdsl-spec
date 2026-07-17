from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
FIXTURES = ROOT / 'samples' / 'adapter-inventory'


def run_case(name: str, target: Path, expected: int, markers: tuple[str, ...]) -> bool:
    proc = subprocess.run(
        [sys.executable, str(ROOT / 'kdsl_parser_adapter_matrix.py'), str(target)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    ok = proc.returncode == expected and all(marker in proc.stdout for marker in markers)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    print('  expected: ' + str(expected))
    print('  actual: ' + str(proc.returncode))
    if not ok:
        missing = [marker for marker in markers if marker not in proc.stdout]
        if missing:
            print('  missing markers: ' + repr(missing))
        if proc.stdout:
            print('  stdout:')
            print('\n'.join('    ' + line for line in proc.stdout.splitlines()))
        if proc.stderr:
            print('  stderr:')
            print('\n'.join('    ' + line for line in proc.stderr.splitlines()))
    return ok


def repository_snapshot(tmp: Path) -> Path:
    target = tmp / 'validator-root'
    target.mkdir()
    for source in ROOT.glob('*.py'):
        shutil.copy2(source, target / source.name)
    return target


def main() -> int:
    results: list[bool] = []
    boundary = (
        'BOUNDARY: matrix pass != consumer migration/semantic equivalence/'
        'adapter retirement proof/U approval/RT:v/authority/release readiness'
    )

    with tempfile.TemporaryDirectory() as raw_tmp:
        snapshot = repository_snapshot(Path(raw_tmp))
        results.append(
            run_case(
                'repository dependency matrix has semantic API decisions only',
                snapshot,
                0,
                (
                    'STATUS: pass',
                    'MODE: repository',
                    '=> retain-semantic-api',
                    'migrate-or-replace: 0',
                    'retain-temporarily: 0',
                    'state: candidate',
                    'blocking_records: 0',
                    boundary,
                ),
            )
        )

    results.append(
        run_case(
            'legacy helper consumer requires migration or replacement',
            FIXTURES / 'helper_consumer.py',
            0,
            (
                'STATUS: pass',
                'helper_consumer.py <- kdsl_packet: parse_top_level => migrate-or-replace',
                'state: blocked',
                boundary,
            ),
        )
    )
    results.append(
        run_case(
            'parity-named structural consumer is retained for parity only',
            FIXTURES / 'parity_consumer.py',
            0,
            (
                'STATUS: pass',
                'parity_consumer.py <- kdsl_packet: parse_top_level => retain-parity-only',
                'state: candidate',
                boundary,
            ),
        )
    )
    results.append(
        run_case(
            'nonstructural module consumer is retained as semantic API',
            FIXTURES / 'semantic_consumer.py',
            0,
            (
                'STATUS: pass',
                'semantic_consumer.py <- kdsl_packet: SCHEMA_ID => retain-semantic-api',
                'state: candidate',
                boundary,
            ),
        )
    )
    results.append(
        run_case(
            'retired Packet installer recurrence is rejected',
            FIXTURES / 'allowed' / 'kdsl_packet.py',
            2,
            (
                'STATUS: fail',
                'unauthorized direct adapter import: install_packet',
                'state: blocked',
                boundary,
            ),
        )
    )

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
