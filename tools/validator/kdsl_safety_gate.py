import re
import sys
from pathlib import Path

REGISTRY = 'kdsl-sg@0.1-draft'
KNOWN_IDS = {
    'SG-DESIGN',
    'SG-SCOPE',
    'SG-EVIDENCE',
    'SG-RUNTIME',
    'SG-AUTHORITY',
    'SG-ROLLBACK',
    'SG-PUBLIC',
    'SG-DATA',
    'SG-KDSL-DP',
    'SG-STOP',
}
KNOWN_STATES = {'hold', 'satisfied', 'blocked', 'na'}
REQUIRED_FIELDS = ('id', 'state', 'scope', 'reason')
BASELINE_IDS = {'SG-SCOPE', 'SG-EVIDENCE', 'SG-AUTHORITY', 'SG-STOP'}

COMPOSITION_RULES = (
    (
        'rollback/revert/discard',
        re.compile(r'\brollback\b|\brevert\b|未push破棄|git\s+restore|git\s+clean', re.IGNORECASE),
        {'SG-DESIGN', 'SG-ROLLBACK', 'SG-SCOPE', 'SG-EVIDENCE', 'SG-AUTHORITY', 'SG-STOP'},
    ),
    (
        'data migration/schema/save format',
        re.compile(r'data migration|データ移行|data schema|保存形式|不可逆変換', re.IGNORECASE),
        {'SG-DESIGN', 'SG-DATA', 'SG-SCOPE', 'SG-EVIDENCE', 'SG-AUTHORITY', 'SG-STOP'},
    ),
    (
        'public/tag/release/assets',
        re.compile(
            r'public履歴|public history|公開済tag|Release Assets|GitHub Release|stable/public-ready',
            re.IGNORECASE,
        ),
        {'SG-PUBLIC', 'SG-EVIDENCE', 'SG-AUTHORITY', 'SG-STOP'},
    ),
    (
        'runtime/RT:v',
        re.compile(r'RT:v|実機確認|runtime verification|対象環境runtime確認', re.IGNORECASE),
        {'SG-EVIDENCE', 'SG-RUNTIME'},
    ),
    (
        'KDSL-DP',
        re.compile(r'KDSL-DP|ADPS Authoring|\bKDP\b', re.IGNORECASE),
        {'SG-KDSL-DP', 'SG-EVIDENCE', 'SG-AUTHORITY', 'SG-STOP'},
    ),
)

PROTECTED_WORDING_RULES = {
    'SG-SCOPE': (
        (
            re.compile(r'原因未確.*広域修正禁止', re.IGNORECASE),
            re.compile(r'target/non-target', re.IGNORECASE),
            re.compile(r'exact target and non-target', re.IGNORECASE),
            re.compile(r'対象/非対象', re.IGNORECASE),
            re.compile(r'TGT外変更禁止', re.IGNORECASE),
        ),
    ),
    'SG-EVIDENCE': (
        (
            re.compile(r'未確認.*確認済扱禁止', re.IGNORECASE),
            re.compile(r'未実行.*実行済扱禁止', re.IGNORECASE),
            re.compile(r'observed/inferred/unverified', re.IGNORECASE),
            re.compile(r'executed evidence separated from inference', re.IGNORECASE),
            re.compile(r'観測/推論', re.IGNORECASE),
        ),
    ),
    'SG-STOP': (
        (
            re.compile(r'停止条件', re.IGNORECASE),
            re.compile(r'stop condition', re.IGNORECASE),
            re.compile(r'preflight stop', re.IGNORECASE),
            re.compile(r'no mismatch observed', re.IGNORECASE),
            re.compile(r'preflight mismatch', re.IGNORECASE),
        ),
    ),
    'SG-DESIGN': (
        (
            re.compile(r'D禁止', re.IGNORECASE),
            re.compile(r'未承認.*実装指示禁止', re.IGNORECASE),
            re.compile(r'未承認.*方針', re.IGNORECASE),
            re.compile(r'設計変更.*承認', re.IGNORECASE),
            re.compile(r'design change.*approval', re.IGNORECASE),
        ),
    ),
    'SG-RUNTIME': (
        (re.compile(r'RT:v', re.IGNORECASE),),
        (
            re.compile(r'build/diff/lint/test/CI pass != RT:v', re.IGNORECASE),
            re.compile(r'Runtime未確認', re.IGNORECASE),
            re.compile(r'runtime verification has not', re.IGNORECASE),
            re.compile(r'実機確認未', re.IGNORECASE),
            re.compile(r'RT:p|RT:u', re.IGNORECASE),
        ),
    ),
    'SG-ROLLBACK': (
        (re.compile(r'\brollback\b|\brevert\b|未push破棄', re.IGNORECASE),),
        (
            re.compile(r'status/diff/退避', re.IGNORECASE),
            re.compile(r'rollback前', re.IGNORECASE),
            re.compile(r'全体破棄', re.IGNORECASE),
            re.compile(r'git status', re.IGNORECASE),
            re.compile(r'patch/status/stat', re.IGNORECASE),
        ),
    ),
    'SG-PUBLIC': (
        (re.compile(r'public履歴|public history|公開済tag|Release Assets|GitHub Release', re.IGNORECASE),),
        (re.compile(r'承認|approval|改竄|上書|non-rewrite|non-overwrite', re.IGNORECASE),),
    ),
    'SG-DATA': (
        (re.compile(r'data保護|backup|rollback|復旧', re.IGNORECASE),),
    ),
    'SG-KDSL-DP': (
        (
            re.compile(r'KDSL-DP直接実行禁止', re.IGNORECASE),
            re.compile(r'KDSL-DP.*直接.*禁止', re.IGNORECASE),
        ),
        (
            re.compile(r'P1/P1L正規化必須', re.IGNORECASE),
            re.compile(r'P1/P1L.*正規化', re.IGNORECASE),
        ),
    ),
}

AUTHORITY_TRIGGER = re.compile(
    r'\bcommit\b|\bpush\b|\brelease\b|NEXT|COMMIT|public|destructive|破壊操作',
    re.IGNORECASE,
)
AUTHORITY_WORDING = (
    re.compile(r'実行許可扱禁止', re.IGNORECASE),
    re.compile(r'自動commit許可扱禁止', re.IGNORECASE),
    re.compile(r'commit/push/release authority', re.IGNORECASE),
    re.compile(r'propose_only', re.IGNORECASE),
    re.compile(r'\bforbid\b', re.IGNORECASE),
    re.compile(r'別操作の許可', re.IGNORECASE),
)


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def extract_gate_block(text):
    lines = text.splitlines()
    start = None
    base_indent = 0
    for index, line in enumerate(lines):
        match = re.match(r'^(\s*)SAFETY_GATES\s*:\s*$', line)
        if match:
            start = index
            base_indent = len(match.group(1))
            break
    if start is None:
        return None

    scoped = [lines[start]]
    for line in lines[start + 1:]:
        if not line.strip():
            scoped.append(line)
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= base_indent and re.match(r'^\s*[A-Za-z][A-Za-z0-9_-]*\s*:', line):
            break
        scoped.append(line)
    return '\n'.join(scoped)


def parse_registry(block):
    registry_match = re.search(r'^\s*registry\s*:\s*(\S+)\s*$', block, re.MULTILINE)
    registry = registry_match.group(1) if registry_match else None

    entries = []
    current = None
    for raw_line in block.splitlines():
        item_match = re.match(r'^\s*-\s*id\s*:\s*(.*?)\s*$', raw_line)
        if item_match:
            if current is not None:
                entries.append(current)
            current = {'id': item_match.group(1)}
            continue

        field_match = re.match(r'^\s+([a-z][a-z0-9_-]*)\s*:\s*(.*?)\s*$', raw_line, re.IGNORECASE)
        if field_match and current is not None:
            current[field_match.group(1).lower()] = field_match.group(2)

    if current is not None:
        entries.append(current)
    return registry, entries


def is_blank(value):
    return value is None or not str(value).strip()


def authority_is_unverified(value):
    if is_blank(value):
        return True
    return str(value).strip().lower() in {'none', 'unknown', 'unverified', 'pending', '未確認'}


def dev_prompt_context(text):
    return bool(
        re.search(r'^\s*profile\s*:\s*dev-prompt\s*$', text, re.IGNORECASE | re.MULTILINE)
        or re.search(r'^\s*KDSL_PROMPT\s*:', text, re.MULTILINE)
    )


def aggregate_state(entries):
    states = [entry.get('state', '').strip().lower() for entry in entries]
    states = [state for state in states if state in KNOWN_STATES]
    applicable = [state for state in states if state != 'na']
    if 'blocked' in applicable:
        return 'blocked'
    if 'hold' in applicable:
        return 'hold'
    if applicable and all(state == 'satisfied' for state in applicable):
        return 'satisfied'
    if states and all(state == 'na' for state in states):
        return 'na'
    return 'unknown'


def wording_group_present(text, patterns):
    return any(pattern.search(text) for pattern in patterns)


def check_protected_wording(text, entry_by_id, errors):
    if not dev_prompt_context(text):
        return
    for gate_id, groups in PROTECTED_WORDING_RULES.items():
        if gate_id not in entry_by_id:
            continue
        for group_index, group in enumerate(groups, start=1):
            if not wording_group_present(text, group):
                errors.append(f'{gate_id}: protected wording group missing: {group_index}')
    if 'SG-AUTHORITY' in entry_by_id and AUTHORITY_TRIGGER.search(text):
        if not wording_group_present(text, AUTHORITY_WORDING):
            errors.append('SG-AUTHORITY: operation-specific protected authority wording missing')


def emit(errors, warnings, info):
    status = 'fail' if errors else ('warn' if warnings else 'pass')
    print('VALIDATION_RESULT:')
    print('STATUS: ' + status)
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('WARNINGS:')
    for item in warnings or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    return 2 if errors else (1 if warnings else 0)



# Phase 1 common parser adapter. Semantic validation remains in this module.
from kdsl_parser_adapter import install_safety_gate
install_safety_gate(globals())

def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    block = extract_gate_block(text)

    errors = []
    warnings = []
    info = []

    if block is None:
        info.append('no SAFETY_GATES block detected')
        return emit(errors, warnings, info)

    registry, entries = parse_registry(block)
    if registry is None:
        errors.append('SAFETY_GATES registry is missing')
    elif registry != REGISTRY:
        errors.append('unknown Safety Gate registry: ' + registry)

    if not entries:
        errors.append('SAFETY_GATES entries are missing')

    seen = set()
    valid_ids = set()
    entry_by_id = {}
    for index, entry in enumerate(entries, start=1):
        label = entry.get('id') or f'entry#{index}'
        for field in REQUIRED_FIELDS:
            if is_blank(entry.get(field)):
                errors.append(f'{label}: required field missing or empty: {field}')

        gate_id = entry.get('id', '').strip()
        if gate_id:
            if not re.fullmatch(r'SG-[A-Z0-9-]+', gate_id):
                errors.append(gate_id + ': invalid Safety Gate ID format')
            elif gate_id not in KNOWN_IDS:
                errors.append('unknown Safety Gate ID: ' + gate_id)
            else:
                valid_ids.add(gate_id)
                entry_by_id[gate_id] = entry
            if gate_id in seen:
                errors.append('duplicate Safety Gate ID: ' + gate_id)
            seen.add(gate_id)

        state = entry.get('state', '').strip().lower()
        if state and state not in KNOWN_STATES:
            errors.append(f'{label}: unknown Safety Gate state: {state}')
            continue

        if state == 'satisfied':
            if is_blank(entry.get('evidence')):
                errors.append(f'{label}: state:satisfied requires evidence')
            if authority_is_unverified(entry.get('authority')):
                errors.append(f'{label}: state:satisfied requires verified authority or not_required')
        elif state == 'blocked':
            if is_blank(entry.get('evidence')):
                warnings.append(f'{label}: state:blocked should record observed conflict/stop evidence')
        elif state == 'na':
            if is_blank(entry.get('reason')):
                errors.append(f'{label}: state:na requires a non-applicability reason')

    is_dev_prompt = dev_prompt_context(text)
    if is_dev_prompt:
        missing = sorted(BASELINE_IDS - valid_ids)
        if missing:
            errors.append('dev-prompt baseline Safety Gates missing: ' + ', '.join(missing))
        for gate_id in sorted(BASELINE_IDS & valid_ids):
            if entry_by_id[gate_id].get('state', '').strip().lower() == 'na':
                errors.append(f'{gate_id}: dev-prompt baseline gate cannot use state:na')

    for rule_name, pattern, required_ids in COMPOSITION_RULES:
        if pattern.search(text):
            missing = sorted(required_ids - valid_ids)
            if missing:
                errors.append(rule_name + ' composition missing: ' + ', '.join(missing))
            for gate_id in sorted(required_ids & valid_ids):
                if entry_by_id[gate_id].get('state', '').strip().lower() == 'na':
                    errors.append(f'{rule_name}: trigger-present gate cannot use state:na: {gate_id}')

    check_protected_wording(text, entry_by_id, errors)

    info.append('Safety Gate registry checked: ' + (registry or 'missing'))
    info.append('entries checked: ' + str(len(entries)))
    info.append('aggregate state: ' + aggregate_state(entries))
    if is_dev_prompt:
        info.append('dev-prompt baseline checked')
        info.append('protected wording checked')
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
