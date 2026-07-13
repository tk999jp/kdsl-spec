from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

PARITY_MARKER = 'Safety Gate parser parity guard: pass'
AST_MARKER = 'Safety Gate structural extraction: AST v2 compatibility view'

CASES = (
    SuiteCase(
        'Safety Gate repository example remains valid',
        ('kdsl_safety_gate.py', 'examples/safety-gates/dev-prompt-safety-gates.example.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'aggregate state: hold'),
    ),
    SuiteCase(
        'Safety Gate unknown registry remains failure',
        ('kdsl_safety_gate.py', 'samples/sample_sg_unknown_registry.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, 'unknown Safety Gate registry'),
    ),
    SuiteCase(
        'Safety Gate absent document remains out of scope',
        ('kdsl_safety_gate.py', 'samples/sample_r1_ok.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, 'no SAFETY_GATES block detected'),
    ),
    SuiteCase(
        'Safety Gate unsupported no-entries shape is blocked by parity guard',
        ('kdsl_safety_gate.py', 'samples/parser-v2/safety_gate_no_entries_field.md'),
        2,
        ('STATUS: fail', 'Safety Gate parser parity guard: entry mismatch'),
        (AST_MARKER,),
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'safety-gate-checker-migration').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
