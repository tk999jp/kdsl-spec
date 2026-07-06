import sys
from pathlib import Path

TEMPLATE_GROUPS = {
    'base': [
        'templates/base/kdsl_base_dev.md',
    ],
    'result': [
        'templates/result/r1_result_spec.md',
    ],
    'task': [
        'templates/tasks/task_docs_state_closeout.md',
        'templates/tasks/task_corrective_impl.md',
        'templates/tasks/task_investigation_only.md',
    ],
}

REQUIRED_SECTIONS = {
    'base': [
        'format:',
        'profile:',
        'mode:',
        'safety:',
        '目的',
        'AUTHORITY',
        '禁止',
        '停止条件',
        '検証',
        'KDSL_RESULT',
    ],
    'result': [
        'KDSL_RESULT',
        'STATUS:',
        'PHASE:',
        'S:',
        'FILES:',
        'WHY:',
        'CMD:',
        'VERIFY:',
        'RT:',
        'RISK:',
        'NEXT:',
        'COMMIT:',
    ],
    'task': [
        'PHASE',
        'REPO_OR_MATERIAL',
        'TARGET_SCOPE',
        'NON_TARGET',
        'STOP_CONDITIONS',
        'VERIFY',
        'AUTHORITY',
    ],
}

EVIDENCE_MARKERS = [
    'expanded_from:',
    'inherits:',
    'template_read:',
    'source_template:',
]


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def known_paths():
    items = []
    for group, paths in TEMPLATE_GROUPS.items():
        for path in paths:
            items.append((group, path))
    return items


def detect_refs(text):
    lower = text.lower()
    refs = []
    for group, path in known_paths():
        if path.lower() in lower:
            refs.append((group, path))
    return refs


def has_evidence(text, path):
    lower = text.lower()
    p = path.lower()
    for marker in EVIDENCE_MARKERS:
        if (marker + p) in lower:
            return marker + path
    return ''


def section_coverage(text, group):
    missing = []
    for token in REQUIRED_SECTIONS[group]:
        if token not in text:
            missing.append(token)
    return missing


def detect_unknown_template(text):
    lower = text.lower()
    if 'templates/' not in lower:
        return False
    for _, path in known_paths():
        lower = lower.replace(path.lower(), '')
    return 'templates/' in lower


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    refs = detect_refs(text)
    errors = []
    warnings = []
    info = []

    if detect_unknown_template(text):
        errors.append('unknown template path detected')

    if not refs:
        info.append('no known template reference detected')
    else:
        for group, template_path in refs:
            evidence = has_evidence(text, template_path)
            if not evidence:
                errors.append('template reference has no expansion/inheritance evidence: ' + template_path)
            else:
                info.append('template expansion evidence: ' + evidence)

            missing = section_coverage(text, group)
            if len(missing) == len(REQUIRED_SECTIONS[group]):
                errors.append('required section group absent for template: ' + template_path)
            elif missing:
                warnings.append('required section group partial for template: ' + template_path + ' missing=' + ', '.join(missing))
            else:
                info.append('required section group present for template: ' + template_path)

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
