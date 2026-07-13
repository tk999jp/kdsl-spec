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
        [sys.executable, str(ROOT / 'kdsl_parser_adapter_inventory.py'), str(target)],
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
        'BOUNDARY: inventory pass != semantic equivalence/safety proof/'
        'adapter retirement proof/U approval/RT:v/authority/release readiness'
    )

    with tempfile.TemporaryDirectory() as raw_tmp:
        snapshot = repository_snapshot(Path(raw_tmp))
        results.append(
            run_case(
                'repository adapter/helper inventory is known and retirement remains blocked',
                snapshot,
                0,
                (
                    'STATUS: pass',
                    'MODE: repository',
                    'kdsl_packet.py <- kdsl_parser_adapter: install_packet',
                    'kdsl_packet_normalization.py <- kdsl_parser_adapter: install_normalization',
                    'kdsl_safety_gate.py <- kdsl_parser_adapter: install_safety_gate',
                    'LEGACY_STRUCTURAL_HELPER_CONSUMERS:',
                    'state: blocked',
                    boundary,
                ),
            )
        )

    results.append(
        run_case(
            'unauthorized direct adapter importer is rejected',
            FIXTURES / 'unauthorized_direct.py',
            2,
            (
                'STATUS: fail',
                'unauthorized direct adapter import: install_packet',
                'state: blocked',
                boundary,
            ),
        )
    )
    results.append(
        run_case(
            'install_r1c recurrence is rejected',
            FIXTURES / 'prohibited_r1c.py',
            2,
            (
                'STATUS: fail',
                'prohibited adapter installer import: install_r1c',
                'state: blocked',
                boundary,
            ),
        )
    )
    results.append(
        run_case(
            'legacy structural helper consumer is classified without direct-import error',
            FIXTURES / 'helper_consumer.py',
            0,
            (
                'STATUS: pass',
                'helper_consumer.py <- kdsl_packet: parse_top_level',
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
