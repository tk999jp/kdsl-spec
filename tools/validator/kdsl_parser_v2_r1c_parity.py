import sys

from kdsl_parser import load_text
from kdsl_parser_v2_compat import compare_r1c_legacy_v2


def emit(errors, info):
    print('R1C_PARSER_PARITY_RESULT:')
    print('STATUS: ' + ('fail' if errors else 'pass'))
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    print('BOUNDARY: structural parity only; no semantic/authority/RT proof')
    return 2 if errors else 0


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    errors, info = compare_r1c_legacy_v2(load_text(path))
    return emit(errors, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
