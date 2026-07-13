from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

PASS_MARKERS = (
    'STATUS: pass',
    'block order/content and duplicates match',
    'BOUNDARY: structural parity only; CP-Lift/restricted-alias/authority semantics unchanged',
)

CASES = (
    SuiteCase(
        'CompactPrompt standard sample parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/sample_cp_standard_ok.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt kanji sample parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/sample_cp_kanji_ok.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt missing-block sample structural parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/sample_cp_missing_block.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt restricted-alias sample structural parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/sample_cp_restricted_alias.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt CP-Lift sample structural parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/sample_cp_lift_required.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt repository standard example parity',
        ('kdsl_parser_v2_compact_parity.py', 'examples/compact-prompt/blog_meta.kdsl-cp.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt repository kanji example parity',
        ('kdsl_parser_v2_compact_parity.py', 'examples/compact-prompt/blog_meta.kdsl-cp-kanji.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt repository novel review parity',
        ('kdsl_parser_v2_compact_parity.py', 'examples/compact-prompt/novel_review.kdsl-cp-kanji.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt profile-only form parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/parser-v2/compact_profile_only.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt duplicate block parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/parser-v2/compact_duplicate_block.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt mixed structural keys parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/parser-v2/compact_mixed_keys.md'),
        0,
        PASS_MARKERS,
    ),
    SuiteCase(
        'CompactPrompt fenced scope parity',
        ('kdsl_parser_v2_compact_parity.py', 'samples/parser-v2/compact_fenced_scope.md'),
        0,
        PASS_MARKERS,
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser-v2-compact-parity').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
