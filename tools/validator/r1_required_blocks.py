import sys
from pathlib import Path

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

    if not present(text, 'KDSL_RESULT'):
        print('VALIDATION_RESULT:')
        print('STATUS: pass')
        print('ERRORS:')
        print('  - none')
        print('WARNINGS:')
        print('  - none')
        print('INFO:')
        print('  - no KDSL_RESULT envelope detected; R1 required-block target not applicable')
        return 0

    missing = [name for name in REQUIRED if not present(text, name)]

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
    if missing:
        print('  - required block check failed')
    else:
        print('  - required block check passed')
    return 2 if missing else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
