from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

BOUNDARY = 'BOUNDARY: structural parity only; normalization semantic/equivalence/execution/authority rules unchanged'
PRESENT_MARKERS = (
    'STATUS: pass',
    'NORMALIZATION_DRAFT presence and exact scope match',
    'top-level field order/value/relative-line and duplicates match',
    'nested scalar/record/list/block-scalar helper outputs match',
    BOUNDARY,
)
ABSENT_MARKERS = (
    'STATUS: pass',
    'NORMALIZATION_DRAFT absent in both parsers',
    BOUNDARY,
)

CASES = (
    SuiteCase(
        'Normalization valid sample structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'samples/sample_normalization_valid.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Normalization Full KDSL repository example structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'examples/packet/normalization-full-kdsl.example.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Normalization P1 blocked repository example structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'examples/packet/normalization-p1-blocked.example.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Normalization lossy blocked repository example structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'examples/packet/normalization-lossy-blocked.example.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Normalization unknown schema structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'samples/sample_normalization_unknown_schema.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Normalization executable status structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'samples/sample_normalization_executable_status.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Normalization semantic claim structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'samples/sample_normalization_semantic_claim.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Normalization out-of-scope document structural parity',
        ('kdsl_parser_v2_normalization_parity.py', 'samples/sample_normalization_out_of_scope.md'),
        0,
        ABSENT_MARKERS,
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser-v2-normalization-parity').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
