import sys
from pathlib import Path

NEXT_MARKERS = [
    'none',
    'proposed:',
    'proposal:',
    '提案:',
    '次候補:',
]

COMMIT_MARKERS = [
    'actual:',
    'proposed:',
    'none',
]


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def find_field(text, name):
    marker = name + ':'
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(marker):
            return stripped[len(marker):].strip()
    return ''


def has_next_marker(value):
    lower = value.lower()
    return any(marker.lower() in lower for marker in NEXT_MARKERS)


def has_commit_shape(value):
    lower = value.lower()
    if lower == 'none':
        return True
    return 'actual:' in lower and 'proposed:' in lower


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    next_value = find_field(text, 'NEXT')
    commit_value = find_field(text, 'COMMIT')

    errors = []
    warnings = []
    info = []

    if not next_value:
        errors.append('NEXT field missing')
    elif not has_next_marker(next_value):
        warnings.append('NEXT field is not clearly proposal-only')
    else:
        info.append('NEXT proposal-only shape detected')

    if not commit_value:
        errors.append('COMMIT field missing')
    elif not has_commit_shape(commit_value):
        warnings.append('COMMIT field is not clearly actual/proposed separated')
    else:
        info.append('COMMIT actual/proposed/none shape detected')

    status = 'fail' if errors else ('warn' if warnings else 'pass')
    print('VALIDATION_RESULT:')
    print('STATUS: ' + status)
    print('ERRORS:')
    if errors:
        for item in errors:
            print('  - ' + item)
    else:
        print('  - none')
    print('WARNINGS:')
    if warnings:
        for item in warnings:
            print('  - ' + item)
    else:
        print('  - none')
    print('INFO:')
    if info:
        for item in info:
            print('  - ' + item)
    else:
        print('  - none')
    return 2 if errors else (1 if warnings else 0)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
