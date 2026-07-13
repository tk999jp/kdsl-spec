import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
RUNNERS = (
    ('core-r1c-success-diagnostic', 'run_r1c_migration_diagnostic.py'),
)


def parse_summary(stdout):
    total = None
    failed = None
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith('total:'):
            total = int(stripped.split(':', 1)[1].strip())
        elif stripped.startswith('failed:'):
            failed = int(stripped.split(':', 1)[1].strip())
    return total, failed


def print_failure_output(proc):
    if proc.stdout:
        print('STDOUT:')
        print(proc.stdout.rstrip())
    if proc.stderr:
        print('STDERR:')
        print(proc.stderr.rstrip())


def main():
    grand_total = 0
    grand_failed = 0
    runner_failures = 0
    for name, script_name in RUNNERS:
        proc = subprocess.run(
            [sys.executable, str(ROOT / script_name)],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
        )
        total, failed = parse_summary(proc.stdout)
        summary_missing = total is None or failed is None
        runner_failed = proc.returncode != 0 or summary_missing or bool(failed)

        print(f'RUNNER: {name}')
        if summary_missing:
            runner_failures += 1
            print('RUNNER_SUMMARY_ERROR')
        else:
            grand_total += total
            grand_failed += failed
            print(f'  total: {total}')
            print(f'  failed: {failed}')

        if proc.returncode != 0:
            runner_failures += 1
            print(f'  exit: {proc.returncode}')

        if runner_failed:
            print_failure_output(proc)

    print('UNIFIED_SUMMARY:')
    print('  runners: ' + str(len(RUNNERS)))
    print('  total: ' + str(grand_total))
    print('  failed: ' + str(grand_failed))
    print('  runner_failures: ' + str(runner_failures))
    return 1 if grand_failed or runner_failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
