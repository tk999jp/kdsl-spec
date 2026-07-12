import re
import sys
from pathlib import Path

SCHEMA_ID = 'kdsl-packet@0.1-draft'
BASE_REGISTRY = 'kdsl-packet-base@0.1-draft'
TASK_REGISTRY = 'kdsl-packet-task@0.1-draft'
FLOW_REGISTRY = 'kdsl-packet-flow@0.1-draft'
SG_REGISTRY = 'kdsl-sg@0.1-draft'
R1C_SCHEMA = 'kdsl-r1c@0.1-draft'

REQUIRED_KEYS = (
    'SCHEMA',
    'STATUS',
    'BASE',
    'TASK',
    'SRC',
    'READ',
    'TGT',
    'OBS',
    'GOAL',
    'NON',
    'SG',
    'STOP',
    'FLOW',
    'VERIFY',
    'OUT',
    'AUTHORITY',
    'NORMALIZE',
)
KNOWN_TOP_LEVEL = set(REQUIRED_KEYS)

KNOWN_BASE_IDS = {
    'BASE-DESIGN-ONLY',
    'BASE-KDSL-DEV',
    'BASE-ADPS-P1',
}
BASE_TARGETS = {
    'BASE-DESIGN-ONLY': {'design-only'},
    'BASE-KDSL-DEV': {'full-kdsl-dev-prompt'},
    'BASE-ADPS-P1': {'P1', 'P1L'},
}

KNOWN_TASK_IDS = {
    'TASK-INSPECT',
    'TASK-PLAN',
    'TASK-CHANGE',
    'TASK-VERIFY',
    'TASK-CLOSEOUT',
    'TASK-PUBLIC',
    'TASK-DATA',
}
TASK_REQUIRED_FLOWS = {
    'TASK-INSPECT': {'FLOW-READ', 'FLOW-ANALYZE', 'FLOW-REPORT'},
    'TASK-PLAN': {'FLOW-READ', 'FLOW-ANALYZE', 'FLOW-GATE', 'FLOW-DECIDE', 'FLOW-REPORT'},
    'TASK-CHANGE': {'FLOW-READ', 'FLOW-ANALYZE', 'FLOW-GATE', 'FLOW-CHANGE', 'FLOW-VERIFY', 'FLOW-REPORT'},
    'TASK-VERIFY': {'FLOW-READ', 'FLOW-GATE', 'FLOW-VERIFY', 'FLOW-REPORT'},
    'TASK-CLOSEOUT': {'FLOW-READ', 'FLOW-GATE', 'FLOW-VERIFY', 'FLOW-REPORT'},
    'TASK-PUBLIC': {'FLOW-READ', 'FLOW-ANALYZE', 'FLOW-GATE', 'FLOW-DECIDE', 'FLOW-CHANGE', 'FLOW-VERIFY', 'FLOW-REPORT'},
    'TASK-DATA': {'FLOW-READ', 'FLOW-ANALYZE', 'FLOW-GATE', 'FLOW-DECIDE', 'FLOW-CHANGE', 'FLOW-VERIFY', 'FLOW-REPORT'},
}
TASK_REQUIRED_GATES = {
    'TASK-INSPECT': {'SG-SCOPE', 'SG-EVIDENCE', 'SG-STOP'},
    'TASK-PLAN': {'SG-SCOPE', 'SG-EVIDENCE', 'SG-STOP'},
    'TASK-CHANGE': {'SG-SCOPE', 'SG-EVIDENCE', 'SG-AUTHORITY', 'SG-STOP'},
    'TASK-VERIFY': {'SG-EVIDENCE', 'SG-STOP'},
    'TASK-CLOSEOUT': {'SG-EVIDENCE', 'SG-AUTHORITY', 'SG-STOP'},
    'TASK-PUBLIC': {'SG-PUBLIC', 'SG-AUTHORITY', 'SG-EVIDENCE', 'SG-SCOPE', 'SG-STOP'},
    'TASK-DATA': {'SG-DATA', 'SG-ROLLBACK', 'SG-AUTHORITY', 'SG-EVIDENCE', 'SG-SCOPE', 'SG-STOP'},
}

KNOWN_FLOW_OPS = {
    'FLOW-READ',
    'FLOW-ANALYZE',
    'FLOW-GATE',
    'FLOW-DECIDE',
    'FLOW-CHANGE',
    'FLOW-VERIFY',
    'FLOW-REPORT',
    'FLOW-STOP',
    'FLOW-ASK',
}
KNOWN_SG_IDS = {
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
AUTHORITY_RAILS = ('read', 'edit', 'stage', 'commit', 'push', 'release')
AUTHORITY_VALUES = {
    'allow',
    'forbid',
    'target_only',
    'allow_once',
    'propose_only',
    'not_requested',
    'not_applicable',
}
NORMALIZE_TARGETS = {'design-only', 'full-kdsl-dev-prompt', 'P1', 'P1L'}
PLACEHOLDERS = {'', '-', 'tbd', 'unknown', 'null', 'none'}

TRIGGER_GATES = (
    (
        'rollback/revert/discard',
        re.compile(r'\brollback\b|\brevert\b|未push破棄|git\s+restore|git\s+clean', re.IGNORECASE),
        {'SG-ROLLBACK'},
    ),
    (
        'runtime/RT:v',
        re.compile(r'RT:v|実機確認|runtime verification|対象環境runtime確認', re.IGNORECASE),
        {'SG-RUNTIME'},
    ),
    (
        'public/tag/release assets',
        re.compile(r'public履歴|public history|公開済tag|Release Assets|GitHub Release', re.IGNORECASE),
        {'SG-PUBLIC'},
    ),
    (
        'data migration/schema',
        re.compile(r'data migration|データ移行|data schema|保存形式|不可逆変換|data deletion', re.IGNORECASE),
        {'SG-DATA', 'SG-ROLLBACK'},
    ),
    (
        'KDSL-DP/ADPS',
        re.compile(r'KDSL-DP|ADPS Authoring|\bBASE-ADPS-P1\b', re.IGNORECASE),
        {'SG-KDSL-DP'},
    ),
)


def load_text(path):
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


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


def extract_packet_scope(text):
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == 'PACKET_DRAFT:':
            start = index
            break
    if start is None:
        return None

    scope = []
    for index in range(start, len(lines)):
        line = lines[index]
        stripped = line.strip()
        if index > start and stripped == '```':
            break
        if index > start and line.startswith('#'):
            break
        scope.append(line)
    return scope


def parse_top_level(scope):
    entries = []
    duplicates = []
    seen = set()
    pattern = re.compile(r'^([A-Z][A-Z0-9_-]*)\s*:\s*(.*)$')
    for index, raw_line in enumerate(scope):
        match = pattern.match(raw_line)
        if not match:
            continue
        key = match.group(1)
        value = match.group(2).strip()
        if key == 'PACKET_DRAFT':
            continue
        if key in seen:
            duplicates.append(key)
        seen.add(key)
        entries.append((key, value, index))
    return entries, duplicates


def blocks_from_entries(scope, entries):
    blocks = {}
    for position, (key, value, line_index) in enumerate(entries):
        next_index = entries[position + 1][2] if position + 1 < len(entries) else len(scope)
        blocks[key] = {'value': value, 'lines': scope[line_index + 1:next_index]}
    return blocks


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_nested_scalars(block):
    values = {}
    duplicates = []
    pattern = re.compile(r'^\s+([a-z][a-z0-9_-]*)\s*:\s*(.*?)\s*$', re.IGNORECASE)
    for raw_line in block.get('lines', []):
        if re.match(r'^\s*-\s*', raw_line):
            continue
        match = pattern.match(raw_line)
        if not match:
            continue
        key = match.group(1).lower()
        if key in values:
            duplicates.append(key)
        values[key] = unquote(match.group(2))
    return values, duplicates


def parse_list_field(block, field):
    values = []
    pattern = re.compile(r'^\s*-\s*' + re.escape(field) + r'\s*:\s*(.*?)\s*$', re.IGNORECASE)
    for raw_line in block.get('lines', []):
        match = pattern.match(raw_line)
        if match:
            values.append(unquote(match.group(1)))
    return values


def parse_sequence_items(block):
    value = block.get('value', '').strip()
    if value == '[]':
        return []
    items = []
    for raw_line in block.get('lines', []):
        match = re.match(r'^\s*-\s*(?![a-z][a-z0-9_-]*\s*:)(.*?)\s*$', raw_line, re.IGNORECASE)
        if match and match.group(1).strip():
            items.append(unquote(match.group(1)))
    if value and value != '[]':
        items.append(unquote(value))
    return items


def require_registry_and_id(label, block, expected_registry, known_ids, errors):
    values, duplicates = parse_nested_scalars(block)
    for key in duplicates:
        errors.append(f'{label} duplicate field: {key}')
    registry = values.get('registry')
    item_id = values.get('id')
    if registry is None:
        errors.append(f'{label}.registry is missing')
    elif registry != expected_registry:
        errors.append(f'unknown {label} registry: {registry}')
    if item_id is None:
        errors.append(f'{label}.id is missing')
    elif item_id not in known_ids:
        errors.append(f'unknown {label} ID: {item_id}')
    return item_id


def validate_authority(block, errors):
    values, duplicates = parse_nested_scalars(block)
    for key in duplicates:
        errors.append('AUTHORITY duplicate rail: ' + key)
    for rail in AUTHORITY_RAILS:
        value = values.get(rail)
        if value is None:
            errors.append('AUTHORITY required rail missing: ' + rail)
        elif value not in AUTHORITY_VALUES:
            errors.append(f'AUTHORITY.{rail} unknown value: {value}')
    for rail in sorted(set(values) - set(AUTHORITY_RAILS)):
        errors.append('AUTHORITY unknown rail: ' + rail)
    return values


def validate_normalize(block, base_id, errors):
    values, duplicates = parse_nested_scalars(block)
    for key in duplicates:
        errors.append('NORMALIZE duplicate field: ' + key)
    required = values.get('required', '').lower()
    target = values.get('target')
    state = values.get('state')
    if required != 'true':
        errors.append('NORMALIZE.required must be true')
    if target not in NORMALIZE_TARGETS:
        errors.append('NORMALIZE.target unknown or missing: ' + str(target))
    if state != 'not_normalized':
        errors.append('NORMALIZE.state must be not_normalized')
    if base_id in BASE_TARGETS and target is not None and target not in BASE_TARGETS[base_id]:
        errors.append(f'BASE/NORMALIZE target mismatch: {base_id} -> {target}')
    for key in sorted(set(values) - {'required', 'target', 'state'}):
        errors.append('NORMALIZE unknown field: ' + key)
    return values


def validate_flow(block, task_id, errors, warnings):
    values, duplicates = parse_nested_scalars(block)
    for key in duplicates:
        if key == 'registry':
            errors.append('FLOW duplicate registry field')
    registry = values.get('registry')
    if registry is None:
        errors.append('FLOW.registry is missing')
    elif registry != FLOW_REGISTRY:
        errors.append('unknown FLOW registry: ' + registry)

    ops = parse_list_field(block, 'op')
    if not ops:
        errors.append('FLOW.steps/op entries are missing')
        return []

    for op in ops:
        if op not in KNOWN_FLOW_OPS:
            errors.append('unknown FLOW opcode: ' + op)

    if task_id in TASK_REQUIRED_FLOWS:
        missing = sorted(TASK_REQUIRED_FLOWS[task_id] - set(ops))
        if missing:
            errors.append(task_id + ' required FLOW opcodes missing: ' + ', '.join(missing))

    if 'FLOW-CHANGE' in ops:
        first_change = ops.index('FLOW-CHANGE')
        if 'FLOW-GATE' not in ops[:first_change]:
            errors.append('FLOW-CHANGE must occur after FLOW-GATE')
        if 'FLOW-STOP' in ops[:first_change]:
            errors.append('FLOW-CHANGE must not occur after FLOW-STOP')
    if 'FLOW-STOP' in ops:
        stop_index = ops.index('FLOW-STOP')
        if 'FLOW-CHANGE' in ops[stop_index + 1:]:
            errors.append('FLOW-CHANGE must not occur after FLOW-STOP')

    if ops[-1] not in {'FLOW-REPORT', 'FLOW-STOP', 'FLOW-ASK'}:
        warnings.append('FLOW should end with FLOW-REPORT, FLOW-STOP, or FLOW-ASK')
    return ops


def validate_sg(block, task_id, text, errors):
    registry_match = None
    for raw_line in block.get('lines', []):
        match = re.match(r'^\s+registry\s*:\s*(\S+)\s*$', raw_line, re.IGNORECASE)
        if match:
            registry_match = match.group(1)
            break
    if registry_match is None:
        errors.append('SG.registry is missing')
    elif registry_match != SG_REGISTRY:
        errors.append('unknown SG registry: ' + registry_match)

    gate_ids = parse_list_field(block, 'id')
    if not gate_ids:
        errors.append('SG.entries/id entries are missing')
    valid_ids = set()
    seen = set()
    for gate_id in gate_ids:
        if gate_id not in KNOWN_SG_IDS:
            errors.append('unknown Safety Gate ID in Packet: ' + gate_id)
        else:
            valid_ids.add(gate_id)
        if gate_id in seen:
            errors.append('duplicate Packet Safety Gate ID: ' + gate_id)
        seen.add(gate_id)

    if task_id in TASK_REQUIRED_GATES:
        missing = sorted(TASK_REQUIRED_GATES[task_id] - valid_ids)
        if missing:
            errors.append(task_id + ' minimum Safety Gates missing: ' + ', '.join(missing))

    for trigger_name, pattern, required in TRIGGER_GATES:
        if pattern.search(text):
            missing = sorted(required - valid_ids)
            if missing:
                errors.append(trigger_name + ' trigger gates missing: ' + ', '.join(missing))
    return valid_ids



# Phase 1 common parser adapter. Semantic validation remains in this module.
from kdsl_parser_adapter import install_packet
install_packet(globals())

def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    errors = []
    warnings = []
    info = []

    scope = extract_packet_scope(text)
    schema_marker = re.search(r'^\s*SCHEMA\s*:\s*(\S+)\s*$', text, re.MULTILINE)
    if scope is None:
        if schema_marker and schema_marker.group(1) == SCHEMA_ID:
            errors.append('Packet SCHEMA marker requires PACKET_DRAFT top-level envelope')
        elif re.search(r'^\s*PKT\s*:\s*v1\s*$', text, re.IGNORECASE | re.MULTILINE):
            errors.append('PKT:v1 is prohibited')
        else:
            info.append('no PACKET_DRAFT block detected; Packet target not applicable')
        return emit(errors, warnings, info)

    packet_text = '\n'.join(scope)
    entries, duplicates = parse_top_level(scope)
    values = {key: value for key, value, _ in entries}
    blocks = blocks_from_entries(scope, entries)

    for key in duplicates:
        errors.append('duplicate Packet field: ' + key)

    key_order = [key for key, _, _ in entries]
    for key in key_order:
        if key not in KNOWN_TOP_LEVEL:
            errors.append('unknown Packet top-level field: ' + key)
    for key in REQUIRED_KEYS:
        if key not in values:
            errors.append('required Packet field missing: ' + key)

    required_present = [key for key in key_order if key in KNOWN_TOP_LEVEL]
    if required_present and required_present != list(REQUIRED_KEYS[: len(required_present)]):
        errors.append('Packet required field order mismatch')
    elif all(key in values for key in REQUIRED_KEYS):
        positions = [key_order.index(key) for key in REQUIRED_KEYS]
        if positions != sorted(positions):
            errors.append('Packet required field order mismatch')

    schema = values.get('SCHEMA')
    if schema != SCHEMA_ID:
        errors.append('unknown Packet schema: ' + str(schema))
    status = values.get('STATUS')
    if status != 'non-executable':
        errors.append('Packet STATUS must be non-executable')
    if re.search(r'^\s*PKT\s*:\s*v1\s*$', packet_text, re.IGNORECASE | re.MULTILINE):
        errors.append('PKT:v1 is prohibited')

    goal = unquote(values.get('GOAL', '')).strip().lower()
    if goal in PLACEHOLDERS:
        errors.append('GOAL must be a non-placeholder scalar')

    base_id = require_registry_and_id('BASE', blocks.get('BASE', {}), BASE_REGISTRY, KNOWN_BASE_IDS, errors)
    task_id = require_registry_and_id('TASK', blocks.get('TASK', {}), TASK_REGISTRY, KNOWN_TASK_IDS, errors)
    gate_ids = validate_sg(blocks.get('SG', {}), task_id, packet_text, errors)
    ops = validate_flow(blocks.get('FLOW', {}), task_id, errors, warnings)
    authority = validate_authority(blocks.get('AUTHORITY', {}), errors)
    normalize = validate_normalize(blocks.get('NORMALIZE', {}), base_id, errors)

    out_values, out_duplicates = parse_nested_scalars(blocks.get('OUT', {}))
    for key in out_duplicates:
        errors.append('OUT duplicate field: ' + key)
    result_schema = out_values.get('result_schema')
    if result_schema not in {R1C_SCHEMA, 'full-r1', 'canonical-r1'}:
        errors.append('OUT.result_schema unknown or missing: ' + str(result_schema))
    for key in sorted(set(out_values) - {'result_schema'}):
        errors.append('OUT unknown field: ' + key)

    for key in ('SRC', 'READ', 'TGT', 'OBS', 'NON', 'STOP', 'VERIFY'):
        if key in blocks:
            items = parse_sequence_items(blocks[key])
            if key in {'READ', 'TGT', 'NON', 'STOP', 'VERIFY'} and task_id in {'TASK-CHANGE', 'TASK-PUBLIC', 'TASK-DATA'} and not items:
                warnings.append(f'{task_id} should not leave {key} empty')
            if key == 'READ' and task_id == 'TASK-VERIFY' and not items:
                warnings.append('TASK-VERIFY should not leave READ empty')

    if authority.get('push') in {'allow', 'allow_once'} or authority.get('release') in {'allow', 'allow_once'}:
        warnings.append('Packet records push/release authority but remains non-executable')

    if normalize.get('state') == 'not_normalized':
        info.append('non-executable normalization boundary checked')
    info.append('Packet schema checked: ' + str(schema))
    info.append('BASE checked: ' + str(base_id))
    info.append('TASK checked: ' + str(task_id))
    info.append('Safety Gate IDs checked: ' + str(len(gate_ids)))
    info.append('FLOW opcodes checked: ' + str(len(ops)))
    info.append('Authority rails checked: ' + str(len(AUTHORITY_RAILS)))

    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
