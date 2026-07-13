import sys
from pathlib import Path

from kdsl_parser_v2_compact_compat import compare_compact_legacy_v2


def load_text(path: str) -> str:
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def emit(errors: list[str], info: list[str]) -> int:
    print('COMPACT_PARSER_PARITY_RESULT:')
    print('STATUS: ' + ('fail' if errors else 'pass'))
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    print('BOUNDARY: structural parity only; CP-Lift/restricted-alias/authority semantics unchanged')
    return 2 if errors else 0


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) > 1 else '-'
    errors, info = compare_compact_legacy_v2(load_text(path))
    return emit(errors, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
