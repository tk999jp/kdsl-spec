from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

BOUNDARY = 'BOUNDARY: structural parity only; RT/NEXT/COMMIT semantic/evidence/authority rules unchanged'
PRESENT_MARKERS = (
    'STATUS: pass',
    'KDSL_RESULT and required-field presence match',
    'RT/VERIFY/S first-field values and basis scope match',
    'NEXT/COMMIT continuation values match',
    'whole-document legacy scan compatibility retained',
    BOUNDARY,
)
ABSENT_MARKERS = (
    'STATUS: pass',
    'KDSL_RESULT and required-field presence match',
    'Full R1 structural compatibility retained',
    BOUNDARY,
)

CASES = (
    SuiteCase(
        'Full R1 valid sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_r1_ok.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Full R1 missing-block sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_r1_missing_block.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Full R1 RT v valid sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_rt_v_valid.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Full R1 RT invalid-basis sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_rt_v_invalid_basis.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Full R1 authority valid sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_authority_ok.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Full R1 authority warning sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_authority_warn.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Full R1 authority failure sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_authority_fail.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Full R1 out-of-scope Packet sample structural parity',
        ('kdsl_parser_v2_full_r1_parity.py', 'samples/sample_packet_valid.md'),
        0,
        ABSENT_MARKERS,
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser-v2-full-r1-parity').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
