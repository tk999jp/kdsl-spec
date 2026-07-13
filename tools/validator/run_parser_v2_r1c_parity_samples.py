from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

PASS_MARKERS = (
    'STATUS: pass',
    'BOUNDARY: structural parity only; no semantic/authority/RT proof',
)

CASES = (
    SuiteCase(
        'R1C parity multiline JSON',
        ('kdsl_parser_v2_r1c_parity.py', 'samples/parser/r1c_multiline_json.md'),
        0,
        (*PASS_MARKERS, 'field order/value/relative-line entries match'),
    ),
    SuiteCase(
        'R1C parity duplicate field list',
        ('kdsl_parser_v2_r1c_parity.py', 'samples/parser/duplicate_field.md'),
        0,
        (*PASS_MARKERS, 'duplicate field list matches'),
    ),
    SuiteCase(
        'R1C parity invalid JSON raw extraction',
        ('kdsl_parser_v2_r1c_parity.py', 'samples/parser/invalid_json.md'),
        0,
        (*PASS_MARKERS, 'raw-source compatibility retained'),
    ),
    SuiteCase(
        'R1C parity no envelope',
        ('kdsl_parser_v2_r1c_parity.py', 'samples/parser/no_envelope.md'),
        0,
        (*PASS_MARKERS, 'KDSL_RESULT absent in both parsers'),
    ),
    SuiteCase(
        'R1C parity quoted scalar and protected wording',
        ('kdsl_parser_v2_r1c_parity.py', 'samples/parser-v2/r1c_quoted_scalar.md'),
        0,
        (*PASS_MARKERS, 'raw-source compatibility retained'),
    ),
    SuiteCase(
        'R1C parity repository success example',
        ('kdsl_parser_v2_r1c_parity.py', 'examples/r1c/r1c-success.example.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'R1C parity repository blocked example',
        ('kdsl_parser_v2_r1c_parity.py', 'examples/r1c/r1c-blocked.example.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'R1C parity repository needs-user example',
        ('kdsl_parser_v2_r1c_parity.py', 'examples/r1c/r1c-needs-user.example.md'),
        0,
        PASS_MARKERS,
    ),
)


def main():
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser-v2-r1c-parity').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
