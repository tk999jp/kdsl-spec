import subprocess
import sys
from pathlib import Path

CHECKER_SETS = {
    'r1': [
        'r1_required_blocks.py',
        'r1_rt_basis.py',
    ],
    'prompt': [
        'kdsl_template_refs.py',
    ],
    'all': [
        'r1_required_blocks.py',
        'r1_rt_basis.py',
        'kdsl_template_refs.py',
    ],
}


def parse_args(argv):
    target_mode = 'all'
    path = None
    index = 1
    while index < len(argv):
        arg = argv[index]
        if arg == '--target':
            if index + 1 >= len(argv):
                raise ValueError('--target requires one of: r1, prompt, all')
            target_mode = argv[index + 1]
            index += 2
            continue
        if path is None:
            path = arg
            index += 1
            continue
        raise ValueError('unexpected argument: ' + arg)
    if path is None:
        raise ValueError('usage: python kdsl_validate.py [--target r1|prompt|all] <file>')
    if target_mode not in CHECKER_SETS:
        raise ValueError('unknown target: ' + target_mode)
    return target_mode, path


def run_checker(root, checker, target):
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
    return proc.returncode


def main(argv):
    try:
        target_mode, target = parse_args(argv)
    except ValueError as exc:
        print(str(exc))
        return 2

    root = Path(__file__).resolve().parent
    final_code = 0

    print('TARGET: ' + target_mode)
    for checker in CHECKER_SETS[target_mode]:
        code = run_checker(root, checker, target)
        if code > final_code:
            final_code = code

    return final_code


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
