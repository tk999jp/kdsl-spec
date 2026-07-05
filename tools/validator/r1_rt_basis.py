import sys
from pathlib import Path

VALID_BASIS = [
    'runtime確認済',
    '実機確認済',
    '対象環境runtime確認',
    'U実機観測',
    'U共有runtime log',
    'actual runtime observed',
    'local runtime verified',
]

INVALID_BASIS = [
    'build pass',
    'build成功',
    'diff pass',
    'diff確認',
    'lint pass',
    'unit test pass',
    'test pass',
    'validator pass',
    '静的確認',
    '推測',
    '未確認',
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


def is_rt_v(value):
    compact = value.replace(' ', '').lower()
    return compact == 'v' or compact.startswith('v/') or 'rt:v' in compact


def hits(text, words):
    lower = text.lower()
    return [word for word in words if word.lower() in lower]


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    rt_value = find_field(text, 'RT')
    rt_v = is_rt_v(rt_value)
    valid = hits(text, VALID_BASIS)
    invalid = hits(text, INVALID_BASIS)

    errors = []
    warnings = []
    info = []

    if not rt_value:
        warnings.append('RT field not found')
    elif not rt_v:
        info.append('RT is not v; basis check skipped')
    else:
        if not valid:
            errors.append('RT:v has no accepted runtime basis')
        if invalid and not valid:
            errors.append('RT:v appears based only on invalid evidence: ' + ', '.join(invalid))
        elif invalid and valid:
            warnings.append('RT:v includes both accepted and invalid basis wording: ' + ', '.join(invalid))
        if valid:
            info.append('accepted runtime basis: ' + ', '.join(valid))

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
