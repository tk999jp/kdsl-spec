from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

PARITY_MARKER = 'CompactPrompt parser parity guard: pass'
AST_MARKER = 'CompactPrompt structural extraction: AST v2 compatibility view'

CASES = (
    SuiteCase(
        'CompactPrompt profile-only form remains valid',
        ('kdsl_compact_prompt.py', 'samples/parser-v2/compact_profile_only.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'CompactPrompt form: standard'),
    ),
    SuiteCase(
        'CompactPrompt duplicate block remains warning',
        ('kdsl_compact_prompt.py', 'samples/parser-v2/compact_duplicate_block.md'),
        1,
        ('STATUS: warn', PARITY_MARKER, 'duplicate CompactPrompt blocks: Goal'),
    ),
    SuiteCase(
        'CompactPrompt mixed structural keys remain warning',
        ('kdsl_compact_prompt.py', 'samples/parser-v2/compact_mixed_keys.md'),
        1,
        ('STATUS: warn', PARITY_MARKER, 'mixed standard/kanji structural keys: 目'),
    ),
    SuiteCase(
        'CompactPrompt fenced scope excludes following notes',
        ('kdsl_compact_prompt.py', 'samples/parser-v2/compact_fenced_scope.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER),
        ('CP-Lift required',),
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'compact-checker-migration').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
