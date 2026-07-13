from pathlib import Path

from kdsl_suite import SuiteCase, SuiteRunner

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

BOUNDARY = 'BOUNDARY: structural parity only; Packet semantic/execution/normalization/authority rules unchanged'
PRESENT_MARKERS = (
    'STATUS: pass',
    'PACKET_DRAFT presence and exact scope match',
    'top-level field order/value/relative-line and duplicates match',
    'nested scalar/list/sequence helper outputs match',
    BOUNDARY,
)
ABSENT_MARKERS = (
    'STATUS: pass',
    'PACKET_DRAFT absent in both parsers',
    BOUNDARY,
)

CASES = (
    SuiteCase(
        'Packet valid sample structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'samples/sample_packet_valid.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Packet fenced repository example structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'examples/packet/packet-design.example.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Packet unknown schema structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'samples/sample_packet_unknown_schema.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Packet executable status structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'samples/sample_packet_executable_status.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Packet missing READ structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'samples/sample_packet_missing_read.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Packet FLOW order structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'samples/sample_packet_flow_order.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Packet authority warning structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'samples/sample_packet_authority_warn.md'),
        0,
        PRESENT_MARKERS,
    ),
    SuiteCase(
        'Packet out-of-scope document structural parity',
        ('kdsl_parser_v2_packet_parity.py', 'samples/sample_packet_out_of_scope.md'),
        0,
        ABSENT_MARKERS,
    ),
)


def main() -> int:
    result = SuiteRunner(ROOT, REPO_ROOT, 'parser-v2-packet-parity').run(CASES)
    return 1 if not result.ok else 0


if __name__ == '__main__':
    raise SystemExit(main())
