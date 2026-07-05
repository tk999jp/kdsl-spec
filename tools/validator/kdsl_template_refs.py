import sys
from pathlib import Path

KNOWN_TEMPLATES = [
    'templates/base/kdsl_base_dev.md',
    'templates/result/r1_result_spec.md',
    'templates/tasks/task_docs_state_closeout.md',
    'templates/tasks/task_corrective_impl.md',
    'templates/tasks/task_investigation_only.md',
]

REQUIRED_GATES = [
    'template_unreadable',
    'unknown template',
    '読了扱禁止',
]


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def contains_any(text, words):
    lower = text.lower()
    return [word for word in words if word.lower() in lower]


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    lower = text.lower()

    refs = [item for item in KNOWN_TEMPLATES if item.lower() in lower]
    has_template_word = 'template' in lower or 'テンプレート' in text
    gates = contains_any(text, REQUIRED_GATES)

    errors = []
    warnings = []
    info = []

    if refs:
        info.append('template references: ' + ', '.join(refs))
        if not gates:
            errors.append('template reference exists but required template safety gates are missing')
    elif has_template_word:
        warnings.append('template wording exists but known template path was not found')

    if gates:
        info.append('template safety gates: ' + ', '.join(gates))

    if not refs and not has_template_word:
        info.append('no template reference detected')

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
