import subprocess
import sys
from pathlib import Path

CHECKERS = [
    'r1_required_blocks.py',
    'r1_rt_basis.py',
    'kdsl_template_refs.py',
]


def main(argv):
    if len(argv) < 2:
        print('usage: python kdsl_validate.py <file>')
        return 2

    target = argv[1]
    root = Path(__file__).resolve().parent
    final_code = 0

    for checker in CHECKERS:
        script = root / checker
        print('CHECK: ' + checker)
        proc = subprocess.run(
            [sys.executable, str(script), target],
            text=True,
            capture_output=True,
        )
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.stderr:
            print('STDERR:')
            print(proc.stderr.rstrip())
        if proc.returncode > final_code:
            final_code = proc.returncode

    return final_code


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
