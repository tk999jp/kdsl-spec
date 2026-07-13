from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

PARITY_MARKER = 'Normalization parser parity guard: pass'
AST_MARKER = 'Normalization structural extraction: AST v2 compatibility view'

CASES = (
    SuiteCase(
        'Normalization valid sample remains valid',
        ('kdsl_packet_normalization.py', 'samples/sample_normalization_valid.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'execution authority boundary checked'),
    ),
    SuiteCase(
        'Normalization Full KDSL example remains valid',
        ('kdsl_packet_normalization.py', 'examples/packet/normalization-full-kdsl.example.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'target checked: full-kdsl-dev-prompt/resolved'),
    ),
    SuiteCase(
        'Normalization P1 blocked example remains valid',
        ('kdsl_packet_normalization.py', 'examples/packet/normalization-p1-blocked.example.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'target checked: P1/blocked'),
    ),
    SuiteCase(
        'Normalization unknown schema remains failure',
        ('kdsl_packet_normalization.py', 'samples/sample_normalization_unknown_schema.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'unknown normalization schema'),
    ),
    SuiteCase(
        'Normalization executable status remains failure',
        ('kdsl_packet_normalization.py', 'samples/sample_normalization_executable_status.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'normalization STATUS must be non-executable'),
    ),
    SuiteCase(
        'Normalization semantic claim remains failure',
        ('kdsl_packet_normalization.py', 'samples/sample_normalization_semantic_claim.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'ROUND_TRIP.semantic_equivalence must remain not_proven'),
    ),
    SuiteCase(
        'Normalization out-of-scope document remains pass',
        ('kdsl_packet_normalization.py', 'samples/sample_normalization_out_of_scope.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, 'no NORMALIZATION_DRAFT block detected'),
        (AST_MARKER,),
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'normalization-checker-migration').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
