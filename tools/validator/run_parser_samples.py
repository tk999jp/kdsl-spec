from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

CASES = (
    SuiteCase(
        'parser Packet envelope with spans',
        ('kdsl_parse.py', '--envelope', 'PACKET_DRAFT', 'samples/parser/packet_valid.md'),
        0,
        ('ENVELOPE: PACKET_DRAFT', 'FIELD_COUNT: 4', 'PARSER_AST_READY'),
    ),
    SuiteCase(
        'parser R1C multiline JSON',
        ('kdsl_parse.py', '--json', '--envelope', 'KDSL_RESULT', 'samples/parser/r1c_multiline_json.md'),
        0,
        ('FILES', 'src/A.cs', 'PARSER_AST_READY'),
    ),
    SuiteCase(
        'R1C checker accepts parser multiline JSON',
        ('kdsl_r1c.py', 'samples/parser/r1c_multiline_json.md'),
        0,
        ('R1C schema checked', 'structured JSON fields checked'),
    ),
    SuiteCase(
        'wrapper accepts parser multiline R1C',
        ('kdsl_validate.py', '--target', 'r1c', 'samples/parser/r1c_multiline_json.md'),
        0,
        ('PARSER_PREFLIGHT:', 'CHECK: kdsl_r1c.py'),
    ),
    SuiteCase(
        'parser normalization block scalar',
        ('kdsl_parse.py', '--json', '--envelope', 'NORMALIZATION_DRAFT', 'samples/parser/normalization_block_scalar.md'),
        0,
        ('KDSL_PROMPT_PREVIEW:', '"field_count": 3'),
    ),
    SuiteCase(
        'parser duplicate field rejected',
        ('kdsl_parse.py', '--envelope', 'KDSL_RESULT', 'samples/parser/duplicate_field.md'),
        2,
        ('PARSER_DUPLICATE_FIELD',),
    ),
    SuiteCase(
        'parser tab indentation rejected',
        ('kdsl_parse.py', '--envelope', 'PACKET_DRAFT', 'samples/parser/tab_indent.md'),
        2,
        ('PARSER_TAB_INDENT',),
    ),
    SuiteCase(
        'parser missing envelope rejected',
        ('kdsl_parse.py', '--envelope', 'PACKET_DRAFT', 'samples/parser/no_envelope.md'),
        2,
        ('PARSER_ENVELOPE_MISSING',),
    ),
    SuiteCase(
        'parser exact string preserved',
        ('kdsl_parse.py', '--json', '--envelope', 'PACKET_DRAFT', 'samples/parser/exact_string.md'),
        0,
        ('MidFD', 'git diff --check'),
    ),
    SuiteCase(
        'parser invalid multiline JSON rejected',
        ('kdsl_parse.py', '--envelope', 'KDSL_RESULT', 'samples/parser/invalid_json.md'),
        2,
        ('PARSER_INVALID_JSON',),
    ),
    SuiteCase(
        'parser nested Safety Gate scope',
        ('kdsl_parse.py', '--envelope', 'SAFETY_GATES', 'samples/parser/safety_gates.md'),
        0,
        ('ENVELOPE: SAFETY_GATES', 'registry', 'entries'),
    ),
)


def main():
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
