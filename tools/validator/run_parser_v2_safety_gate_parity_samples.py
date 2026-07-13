from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

BOUNDARY = 'BOUNDARY: structural parity only; Safety Gate semantic/composition/authority rules unchanged'
PRESENT_MARKERS = (
    'STATUS: pass',
    'SAFETY_GATES presence and exact scope match',
    'entry order/field order/value match',
    BOUNDARY,
)
ABSENT_MARKERS = (
    'STATUS: pass',
    'SAFETY_GATES absent in both parsers',
    BOUNDARY,
)

CASES = (
    SuiteCase(
        'Safety Gate valid sample parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'samples/sample_sg_valid.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Safety Gate fenced repository example parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'examples/safety-gates/dev-prompt-safety-gates.example.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Safety Gate unknown registry structural parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'samples/sample_sg_unknown_registry.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Safety Gate unknown ID and state structural parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'samples/sample_sg_unknown_id_state.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Safety Gate missing field structural parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'samples/sample_sg_missing_field.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Safety Gate satisfied missing basis structural parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'samples/sample_sg_satisfied_missing_basis.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Safety Gate na missing reason structural parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'samples/sample_sg_na_missing_reason.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Safety Gate absent document parity',
        ('kdsl_parser_v2_safety_gate_parity.py', 'samples/sample_r1_ok.md'),
        0,
        ABSENT_MARKERS,
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser-v2-safety-gate-parity').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
