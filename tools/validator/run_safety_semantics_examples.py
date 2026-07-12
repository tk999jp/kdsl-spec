import contextlib
import io
from pathlib import Path

import kdsl_safety_gate_graph
import kdsl_safety_semantics

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent


def run_main(fn, argv):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = fn(argv)
    return code, output.getvalue()


def main():
    cases = [
        (
            'bounded semantics repository example',
            kdsl_safety_semantics.main,
            [
                'kdsl_safety_semantics.py',
                str(REPO_ROOT / 'examples/safety-gates/bounded-semantics.example.md'),
            ],
            0,
            'semantic concept preserved',
        ),
        (
            'multi-generation graph repository example',
            kdsl_safety_gate_graph.main,
            [
                'kdsl_safety_gate_graph.py',
                str(REPO_ROOT / 'examples/safety-gates/multigeneration/graph.json'),
            ],
            0,
            'topological order: phase0>phase1>phase2',
        ),
    ]
    failed = 0
    for name, fn, argv, expected, marker in cases:
        code, output = run_main(fn, argv)
        ok = code == expected and marker in output
        print(('PASS' if ok else 'FAIL') + ': ' + name)
        if not ok:
            failed += 1
            print('  expected: ' + str(expected))
            print('  actual: ' + str(code))
            print(output)
    print('SUMMARY:')
    print('  total: ' + str(len(cases)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
