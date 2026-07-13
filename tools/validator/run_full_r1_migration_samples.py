from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

PARITY_MARKER = 'Full R1 parser parity guard: pass'
AST_MARKER = 'Full R1 structural extraction: AST v2 compatibility view'

CASES = (
    SuiteCase(
        'Full R1 required blocks valid remains pass',
        ('r1_required_blocks.py', 'samples/sample_r1_ok.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'required block check passed'),
    ),
    SuiteCase(
        'Full R1 required block missing remains failure',
        ('r1_required_blocks.py', 'samples/sample_r1_missing_block.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'missing required field'),
    ),
    SuiteCase(
        'Full R1 required target out of scope remains pass',
        ('r1_required_blocks.py', 'samples/sample_packet_valid.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, 'target not applicable'),
        (AST_MARKER,),
    ),
    SuiteCase(
        'Full R1 RT valid basis remains pass',
        ('r1_rt_basis.py', 'samples/sample_rt_v_valid.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'accepted runtime basis'),
    ),
    SuiteCase(
        'Full R1 RT invalid basis remains failure',
        ('r1_rt_basis.py', 'samples/sample_rt_v_invalid_basis.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'RT:v has no accepted runtime basis'),
    ),
    SuiteCase(
        'Full R1 RT no basis remains failure',
        ('r1_rt_basis.py', 'samples/sample_rt_v_no_basis.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'RT:v has no accepted runtime basis'),
    ),
    SuiteCase(
        'Full R1 authority valid remains pass',
        ('r1_authority_guard.py', 'samples/sample_authority_ok.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'NEXT proposal-only shape detected'),
    ),
    SuiteCase(
        'Full R1 authority ambiguous remains warning',
        ('r1_authority_guard.py', 'samples/sample_authority_warn.md'),
        1,
        ('STATUS: warn', PARITY_MARKER, AST_MARKER, 'not clearly'),
    ),
    SuiteCase(
        'Full R1 authority missing remains failure',
        ('r1_authority_guard.py', 'samples/sample_authority_fail.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'field missing'),
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'full-r1-checker-migration').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
