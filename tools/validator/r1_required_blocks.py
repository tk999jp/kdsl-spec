import sys
from pathlib import Path

from kdsl_parser_v2_full_r1_compat import (
    FullR1CompatibilityView,
    compare_full_r1_legacy_v2,
)

REQUIRED = [
    'KDSL_RESULT',
    'STATUS',
    'PHASE',
    'S',
    'FILES',
    'WHY',
    'CMD',
    'VERIFY',
    'RT',
    'RISK',
    'NEXT',
    'COMMIT',
]


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def present(text, name):
    marker = name + ':'
    return any(line.strip().startswith(marker) for line in text.splitlines())


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    view = FullR1CompatibilityView.from_text(text)
    parity_errors, _ = compare_full_r1_legacy_v2(text)

    if parity_errors:
        print('VALIDATION_RESULT:')
        print('STATUS: fail')
        print('ERRORS:')
        for item in parity_errors:
            print('  - Full R1 parser parity guard: ' + item)
        print('WARNINGS:')
        print('  - none')
        print('INFO:')
        print('  - none')
        return 2

    if not view.has_result_envelope:
        print('VALIDATION_RESULT:')
        print('STATUS: pass')
        print('ERRORS:')
        print('  - none')
        print('WARNINGS:')
        print('  - none')
        print('INFO:')
        print('  - Full R1 parser parity guard: pass')
        print('  - no KDSL_RESULT envelope detected; R1 required-block target not applicable')
        return 0

    missing = [name for name in REQUIRED if not view.present(name)]

    print('VALIDATION_RESULT:')
    print('STATUS: ' + ('fail' if missing else 'pass'))
    print('ERRORS:')
    if missing:
        for name in missing:
            print('  - missing required field: ' + name)
    else:
        print('  - none')
    print('WARNINGS:')
    print('  - none')
    print('INFO:')
    print('  - Full R1 parser parity guard: pass')
    print('  - Full R1 structural extraction: AST v2 compatibility view')
    if missing:
        print('  - required block check failed')
    else:
        print('  - required block check passed')
    return 2 if missing else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
