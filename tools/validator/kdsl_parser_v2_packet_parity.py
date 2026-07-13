import sys
from pathlib import Path

from kdsl_parser_v2_packet_compat import compare_packet_legacy_v2


def load_text(path: str) -> str:
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('usage: python kdsl_parser_v2_packet_parity.py <file>')
        return 2

    text = load_text(argv[1])
    errors, info = compare_packet_legacy_v2(text)
    print('PACKET_PARSER_PARITY_RESULT:')
    print('STATUS: ' + ('fail' if errors else 'pass'))
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    print('BOUNDARY: structural parity only; Packet semantic/execution/normalization/authority rules unchanged')
    return 2 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
