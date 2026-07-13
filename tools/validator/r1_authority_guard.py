import re
import sys
from pathlib import Path

from kdsl_parser_v2_full_r1_compat import (
    FullR1CompatibilityView,
    compare_full_r1_legacy_v2,
)

NEXT_MARKERS = [
    'none',
    'proposed:',
    'proposal:',
    'proposed only',
    'proposal only',
    'proposal-only',
    '提案:',
    '提案のみ',
    '次候補:',
]

COMMIT_MARKERS = [
    'actual:',
    'proposed:',
    'none',
]

FIELD_HEADER = re.compile(r'^[A-Z_]+:')


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def has_result_envelope(text):
    return any(line.strip().startswith('KDSL_RESULT:') for line in text.splitlines())


def find_field(text, name):
    marker = name + ':'
    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith(marker):
            continue

        value = stripped[len(marker):].strip()
        block_lines = []
        for following in lines[index + 1:]:
            if not following.strip():
                if block_lines:
                    break
                continue
            if FIELD_HEADER.match(following.strip()) and not following.startswith((' ', '\t')):
                break
            if following.startswith((' ', '\t', '-', '*')):
                block_lines.append(following.strip())
                continue
            break

        if block_lines:
            return (value + '\n' + '\n'.join(block_lines)).strip()
        return value
    return ''


def has_next_marker(value):
    lower = value.lower()
    return any(marker.lower() in lower for marker in NEXT_MARKERS)


def has_commit_shape(value):
    lower = value.lower()
    if lower == 'none':
        return True
    return 'actual:' in lower and 'proposed:' in lower


def emit(errors, warnings, info):
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


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    view = FullR1CompatibilityView.from_text(text)
    parity_errors, _ = compare_full_r1_legacy_v2(text)

    if parity_errors:
        return emit(
            ['Full R1 parser parity guard: ' + item for item in parity_errors],
            [],
            [],
        )

    if not view.has_result_envelope:
        return emit(
            [],
            [],
            [
                'Full R1 parser parity guard: pass',
                'no KDSL_RESULT envelope detected; R1 authority target not applicable',
            ],
        )

    next_value = view.continued_value('NEXT')
    commit_value = view.continued_value('COMMIT')

    errors = []
    warnings = []
    info = [
        'Full R1 parser parity guard: pass',
        'Full R1 structural extraction: AST v2 compatibility view',
    ]

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

    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
