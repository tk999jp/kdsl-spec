import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
RUNNERS = (
    ('core', 'run_samples.py'),
    ('safety-gate', 'run_safety_gate_samples.py'),
    ('r1c-roundtrip', 'run_r1c_roundtrip_samples.py'),
    ('parser', 'run_parser_samples.py'),
    ('safety-semantics', 'run_safety_semantics_samples.py'),
    ('safety-semantics-examples', 'run_safety_semantics_examples.py'),
    ('r1c-optional', 'run_r1c_optional_samples.py'),
    ('packet-semantic-property', 'run_packet_semantic_property_samples.py'),
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
        print(f'RUNNER: {name}')
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.stderr:
            print('STDERR:')
            print(proc.stderr.rstrip())
        total, failed = parse_summary(proc.stdout)
        if total is None or failed is None:
            runner_failures += 1
            print(f'RUNNER_SUMMARY_ERROR: {name}')
        else:
            grand_total += total
            grand_failed += failed
        if proc.returncode != 0:
            runner_failures += 1

    print('UNIFIED_SUMMARY:')
    print('  runners: ' + str(len(RUNNERS)))
    print('  total: ' + str(grand_total))
    print('  failed: ' + str(grand_failed))
    print('  runner_failures: ' + str(runner_failures))
    return 1 if grand_failed or runner_failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
