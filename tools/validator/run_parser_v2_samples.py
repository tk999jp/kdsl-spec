from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

CASES = (
    SuiteCase(
        'parser v2 exposes formal headers and envelope',
        ('kdsl_parse_v2.py', 'samples/parser-v2/full_headers.md'),
        0,
        (
            'HEADER_COUNT: 6',
            'HEADERS: format,profile,mode,safety,lexicon,envelope',
            'ENVELOPE_COUNT: 1',
            'ENVELOPES: KDSL_PROMPT',
            'PARSER_V2_AST_READY',
        ),
    ),
    SuiteCase(
        'parser v2 builds typed nested values',
        ('kdsl_parse_v2.py', '--json', 'samples/parser-v2/nested_values.md'),
        0,
        (
            '"kind": "mapping"',
            '"kind": "record-sequence"',
            '"key": "flags"',
            '"state"',
        ),
    ),
    SuiteCase(
        'parser v2 preserves block scalar styles',
        ('kdsl_parse_v2.py', '--json', 'samples/parser-v2/block_scalars.md'),
        0,
        (
            '"kind": "block-scalar"',
            '"style": "|"',
            '"style": ">"',
            'KDSL_PROMPT:',
        ),
    ),
    SuiteCase(
        'parser v2 rejects duplicate envelopes',
        ('kdsl_parse_v2.py', 'samples/parser-v2/duplicate_envelope.md'),
        2,
        ('PARSER_DUPLICATE_ENVELOPE',),
    ),
    SuiteCase(
        'parser v2 rejects duplicate fields',
        ('kdsl_parse_v2.py', 'samples/parser-v2/duplicate_field.md'),
        2,
        ('PARSER_DUPLICATE_FIELD',),
    ),
    SuiteCase(
        'parser v2 rejects duplicate mapping keys',
        ('kdsl_parse_v2.py', 'samples/parser-v2/duplicate_mapping.md'),
        2,
        ('PARSER_DUPLICATE_MAPPING_KEY',),
    ),
    SuiteCase(
        'parser v2 rejects invalid multiline JSON',
        ('kdsl_parse_v2.py', 'samples/parser-v2/invalid_json.md'),
        2,
        ('PARSER_INVALID_JSON',),
    ),
    SuiteCase(
        'parser v2 rejects unclosed markdown fence',
        ('kdsl_parse_v2.py', 'samples/parser-v2/unclosed_fence.md'),
        2,
        ('PARSER_UNCLOSED_FENCE',),
    ),
    SuiteCase(
        'parser v2 ignores fenced envelope in active context',
        ('kdsl_parse_v2.py', 'samples/parser-v2/fenced_example.md'),
        0,
        (
            'ENVELOPE_COUNT: 1',
            'ENVELOPES: PACKET_DRAFT',
            'PARSER_V2_AST_READY',
        ),
    ),
    SuiteCase(
        'parser v2 retains unknown header values without inference',
        ('kdsl_parse_v2.py', '--json', 'samples/parser-v2/unknown_header_value.md'),
        0,
        (
            '"key": "profile"',
            '"normalized_value": "future-profile"',
            '"normalized_value": "future-mode"',
        ),
    ),
    SuiteCase(
        'parser v2 preserves exact Japanese protected wording',
        ('kdsl_parse_v2.py', '--json', 'samples/parser-v2/exact_japanese.md'),
        0,
        (
            '承認待 / 未確認 / 未実行 / rollback / KDSL-DP直接実行禁止',
            'build/diff/lint/test/CI pass != RT:v',
            '"raw_text"',
        ),
    ),
    SuiteCase(
        'parser v2 normalizes CRLF input',
        ('kdsl_parse_v2.py', 'samples/parser-v2/crlf_headers.md'),
        0,
        (
            'HEADER_COUNT: 4',
            'ENVELOPE_COUNT: 1',
            'ENVELOPES: KDSL_PROMPT',
            'PARSER_V2_AST_READY',
        ),
    ),
)


def main():
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser-v2').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
