import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

SAMPLES = [
    {
        'name': 'r1 required blocks ok',
        'command': ['r1_required_blocks.py', 'samples/sample_r1_ok.md'],
        'expected': 0,
    },
    {
        'name': 'r1 required blocks missing block',
        'command': ['r1_required_blocks.py', 'samples/sample_r1_missing_block.md'],
        'expected': 2,
    },
    {
        'name': 'rt v valid field-scoped basis',
        'command': ['r1_rt_basis.py', 'samples/sample_rt_v_valid.md'],
        'expected': 0,
    },
    {
        'name': 'rt v invalid basis',
        'command': ['r1_rt_basis.py', 'samples/sample_rt_v_invalid_basis.md'],
        'expected': 2,
    },
    {
        'name': 'rt v no basis',
        'command': ['r1_rt_basis.py', 'samples/sample_rt_v_no_basis.md'],
        'expected': 2,
    },
    {
        'name': 'authority ok',
        'command': ['r1_authority_guard.py', 'samples/sample_authority_ok.md'],
        'expected': 0,
    },
    {
        'name': 'authority warn',
        'command': ['r1_authority_guard.py', 'samples/sample_authority_warn.md'],
        'expected': 1,
    },
    {
        'name': 'authority fail',
        'command': ['r1_authority_guard.py', 'samples/sample_authority_fail.md'],
        'expected': 2,
    },
    {
        'name': 'template refs ok',
        'command': ['kdsl_template_refs.py', 'samples/sample_template_ref_ok.md'],
        'expected': 0,
    },
    {
        'name': 'template refs missing gate',
        'command': ['kdsl_template_refs.py', 'samples/sample_template_ref_missing_gate.md'],
        'expected': 2,
    },
    {
        'name': 'template expansion evidence ok',
        'command': ['kdsl_template_expansion.py', 'samples/sample_template_expansion_ok.md'],
        'expected': 0,
    },
    {
        'name': 'template expansion evidence warn',
        'command': ['kdsl_template_expansion.py', 'samples/sample_template_expansion_warn.md'],
        'expected': 1,
    },
    {
        'name': 'template expansion evidence fail',
        'command': ['kdsl_template_expansion.py', 'samples/sample_template_expansion_fail.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target r1 valid',
        'command': ['kdsl_validate.py', '--target', 'r1', 'samples/sample_rt_v_valid.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target prompt expansion ok',
        'command': ['kdsl_validate.py', '--target', 'prompt', 'samples/sample_template_expansion_ok.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target prompt ref only fails expansion evidence',
        'command': ['kdsl_validate.py', '--target', 'prompt', 'samples/sample_template_ref_ok.md'],
        'expected': 2,
    },
]


def resolve_command(command):
    script = ROOT / command[0]
    args = []
    for item in command[1:]:
        if item.startswith('samples/'):
            args.append(str(ROOT / item))
        else:
            args.append(item)
    return [sys.executable, str(script), *args]


def run_sample(sample):
    proc = subprocess.run(
        resolve_command(sample['command']),
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    ok = proc.returncode == sample['expected']
    status = 'PASS' if ok else 'FAIL'
    command_text = 'python tools/validator/' + ' '.join(sample['command'])
    print(f"{status}: {sample['name']}")
    print(f"  cmd: {command_text}")
    print(f"  expected: {sample['expected']}")
    print(f"  actual: {proc.returncode}")
    if not ok:
        if proc.stdout:
            print('  stdout:')
            print(indent(proc.stdout.rstrip()))
        if proc.stderr:
            print('  stderr:')
            print(indent(proc.stderr.rstrip()))
    return ok


def indent(text):
    return '\n'.join('    ' + line for line in text.splitlines())


def main():
    failed = 0
    for sample in SAMPLES:
        if not run_sample(sample):
            failed += 1
    print('SUMMARY:')
    print(f'  total: {len(SAMPLES)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
