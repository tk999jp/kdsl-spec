import subprocess
import sys
import tempfile
from pathlib import Path

from run_r1c_roundtrip_samples import ROOT, REPO_ROOT, safety_gate_doc


def main():
    with tempfile.TemporaryDirectory() as tmp:
        safety_path = Path(tmp) / 'safety.md'
        safety_path.write_text(safety_gate_doc(), encoding='utf-8')
        result = subprocess.run(
            [sys.executable, str(ROOT / 'kdsl_validate.py'), '--target', 'r1c', str(safety_path)],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
        )

    ok = result.returncode == 0
    print(('PASS' if ok else 'FAIL') + ': Safety Gates R1C validator stage')
    print('  expected: 0')
    print(f'  actual: {result.returncode}')
    if not ok:
        print('  stdout:')
        print('\n'.join('    ' + line for line in result.stdout.splitlines()))
        if result.stderr:
            print('  stderr:')
            print('\n'.join('    ' + line for line in result.stderr.splitlines()))

    print('SUMMARY:')
    print('  total: 1')
    print('  failed: ' + ('0' if ok else '1'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
