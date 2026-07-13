from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

PARITY_MARKER = 'Packet parser parity guard: pass'
AST_MARKER = 'Packet structural extraction: AST v2 compatibility view'

CASES = (
    SuiteCase(
        'Packet valid sample remains valid',
        ('kdsl_packet.py', 'samples/sample_packet_valid.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'non-executable normalization boundary checked'),
    ),
    SuiteCase(
        'Packet fenced repository example remains valid',
        ('kdsl_packet.py', 'examples/packet/packet-design.example.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, AST_MARKER, 'Packet schema checked: kdsl-packet@0.1-draft'),
    ),
    SuiteCase(
        'Packet unknown schema remains failure',
        ('kdsl_packet.py', 'samples/sample_packet_unknown_schema.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'unknown Packet schema'),
    ),
    SuiteCase(
        'Packet executable status remains failure',
        ('kdsl_packet.py', 'samples/sample_packet_executable_status.md'),
        2,
        ('STATUS: fail', PARITY_MARKER, AST_MARKER, 'Packet STATUS must be non-executable'),
    ),
    SuiteCase(
        'Packet authority warning remains warning',
        ('kdsl_packet.py', 'samples/sample_packet_authority_warn.md'),
        1,
        ('STATUS: warn', PARITY_MARKER, AST_MARKER, 'remains non-executable'),
    ),
    SuiteCase(
        'Packet out-of-scope document remains pass',
        ('kdsl_packet.py', 'samples/sample_packet_out_of_scope.md'),
        0,
        ('STATUS: pass', PARITY_MARKER, 'no PACKET_DRAFT block detected'),
        (AST_MARKER,),
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'packet-checker-migration').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
