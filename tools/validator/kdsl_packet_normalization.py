import re
import sys
from pathlib import Path

SCHEMA_ID = 'kdsl-packet-normalization@0.1-draft'
SOURCE_SCHEMA = 'kdsl-packet@0.1-draft'
FULL_KDSL_SCHEMA = 'format:KDSL/profile:dev-prompt'

REQUIRED_KEYS = (
    'SCHEMA',
    'STATUS',
    'SOURCE',
    'TARGET',
    'MAP',
    'PRESERVE',
    'UNRESOLVED',
    'LOSS',
    'ROUND_TRIP',
    'AUTHORITY',
    'OUTPUT',
)
KNOWN_TOP_LEVEL = set(REQUIRED_KEYS)
PACKET_SOURCE_FIELDS = {
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
}
TARGET_KINDS = {'design-only', 'full-kdsl-dev-prompt', 'P1', 'P1L'}
TARGET_RESOLUTIONS = {'resolved', 'blocked'}
MAP_MODES = {'exact', 'structured', 'expanded', 'blocked'}
LOSS_CLASSES = {'none', 'render_only', 'critical'}
ROUND_TRIP_STATES = {'not_tested', 'structural_pass', 'loss_detected', 'blocked'}
STRUCTURAL_EQ = {'not_proven', 'pass', 'failed'}
OUTPUT_MARKERS = {'DESIGN_PREVIEW', 'KDSL_PROMPT_PREVIEW', 'none'}
PRESERVE_KEYS = {'exact_strings', 'protected_wording', 'ordered_fields'}
DIGEST_RE = re.compile(r'^sha256:[0-9a-f]{64}$')


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


def extract_scope(text):
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == 'NORMALIZATION_DRAFT:':
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
        if key == 'NORMALIZATION_DRAFT':
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
    pattern = re.compile(r'^  ([a-z][a-z0-9_-]*)\s*:\s*(.*?)\s*$', re.IGNORECASE)
    for raw_line in block.get('lines', []):
        match = pattern.match(raw_line)
        if not match:
            continue
        key = match.group(1).lower()
        value = unquote(match.group(2))
        if key in values:
            duplicates.append(key)
        values[key] = value
    return values, duplicates


def parse_list_records(block):
    records = []
    current = None
    item_pattern = re.compile(r'^\s*-\s+([a-z][a-z0-9_-]*)\s*:\s*(.*?)\s*$', re.IGNORECASE)
    field_pattern = re.compile(r'^\s{4,}([a-z][a-z0-9_-]*)\s*:\s*(.*?)\s*$', re.IGNORECASE)
    for raw_line in block.get('lines', []):
        item = item_pattern.match(raw_line)
        if item:
            if current is not None:
                records.append(current)
            current = {item.group(1).lower(): unquote(item.group(2))}
            continue
        field = field_pattern.match(raw_line)
        if field and current is not None:
            current[field.group(1).lower()] = unquote(field.group(2))
    if current is not None:
        records.append(current)
    return records


def parse_nested_lists(block):
    result = {}
    current = None
    key_pattern = re.compile(r'^  ([a-z][a-z0-9_-]*)\s*:\s*(.*?)\s*$', re.IGNORECASE)
    item_pattern = re.compile(r'^\s{4,}-\s*(.*?)\s*$')
    for raw_line in block.get('lines', []):
        key_match = key_pattern.match(raw_line)
        if key_match:
            current = key_match.group(1).lower()
            result.setdefault(current, [])
            inline = key_match.group(2).strip()
            if inline == '[]':
                continue
            if inline:
                result[current].append(unquote(inline))
            continue
        item_match = item_pattern.match(raw_line)
        if item_match and current is not None:
            result[current].append(unquote(item_match.group(1)))
    return result


def extract_multiline(block, field):
    lines = block.get('lines', [])
    pattern = re.compile(r'^  ' + re.escape(field) + r'\s*:\s*\|\s*$', re.IGNORECASE)
    start = None
    for index, raw_line in enumerate(lines):
        if pattern.match(raw_line):
            start = index + 1
            break
    if start is None:
        return ''
    collected = []
    for raw_line in lines[start:]:
        if raw_line.startswith('    '):
            collected.append(raw_line[4:])
        elif not raw_line.strip():
            collected.append('')
        else:
            break
    return '\n'.join(collected).rstrip()


def validate_records(label, records, required_fields, errors):
    for index, record in enumerate(records, start=1):
        missing = sorted(required_fields - set(record))
        if missing:
            errors.append(f'{label} entry {index} missing fields: ' + ', '.join(missing))


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    errors = []
    warnings = []
    info = []

    scope = extract_scope(text)
    schema_marker = re.search(r'^\s*SCHEMA\s*:\s*(\S+)\s*$', text, re.MULTILINE)
    if scope is None:
        if schema_marker and schema_marker.group(1) == SCHEMA_ID:
            errors.append('normalization SCHEMA marker requires NORMALIZATION_DRAFT envelope')
        else:
            info.append('no NORMALIZATION_DRAFT block detected; normalization target not applicable')
        return emit(errors, warnings, info)

    normalization_text = '\n'.join(scope)
    entries, duplicates = parse_top_level(scope)
    values = {key: value for key, value, _ in entries}
    blocks = blocks_from_entries(scope, entries)
    key_order = [key for key, _, _ in entries]

    for key in duplicates:
        errors.append('duplicate normalization field: ' + key)
    for key in key_order:
        if key not in KNOWN_TOP_LEVEL:
            errors.append('unknown normalization top-level field: ' + key)
    for key in REQUIRED_KEYS:
        if key not in values:
            errors.append('required normalization field missing: ' + key)

    present_required = [key for key in key_order if key in KNOWN_TOP_LEVEL]
    if present_required and present_required != list(REQUIRED_KEYS[: len(present_required)]):
        errors.append('normalization required field order mismatch')
    elif all(key in values for key in REQUIRED_KEYS):
        positions = [key_order.index(key) for key in REQUIRED_KEYS]
        if positions != sorted(positions):
            errors.append('normalization required field order mismatch')

    if values.get('SCHEMA') != SCHEMA_ID:
        errors.append('unknown normalization schema: ' + str(values.get('SCHEMA')))
    if values.get('STATUS') != 'non-executable':
        errors.append('normalization STATUS must be non-executable')

    if re.search(r'^\s*(?:KDSL_PROMPT|P1|P1L)\s*:', normalization_text, re.MULTILINE):
        errors.append('executable target marker is prohibited in NORMALIZATION_DRAFT')
    if re.search(r'^\s*PKT\s*:\s*v1\s*$', normalization_text, re.IGNORECASE | re.MULTILINE):
        errors.append('PKT:v1 is prohibited')

    source, source_duplicates = parse_nested_scalars(blocks.get('SOURCE', {}))
    for key in source_duplicates:
        errors.append('SOURCE duplicate field: ' + key)
    required_source = {'schema', 'digest', 'packet_status', 'normalize_state'}
    missing_source = sorted(required_source - set(source))
    if missing_source:
        errors.append('SOURCE fields missing: ' + ', '.join(missing_source))
    if source.get('schema') != SOURCE_SCHEMA:
        errors.append('SOURCE.schema must be ' + SOURCE_SCHEMA)
    if not DIGEST_RE.fullmatch(source.get('digest', '')):
        errors.append('SOURCE.digest must be sha256:<64 lowercase hex>')
    if source.get('packet_status') != 'non-executable':
        errors.append('SOURCE.packet_status must be non-executable')
    if source.get('normalize_state') != 'not_normalized':
        errors.append('SOURCE.normalize_state must be not_normalized')

    target, target_duplicates = parse_nested_scalars(blocks.get('TARGET', {}))
    for key in target_duplicates:
        errors.append('TARGET duplicate field: ' + key)
    required_target = {'kind', 'schema', 'resolution', 'executable'}
    missing_target = sorted(required_target - set(target))
    if missing_target:
        errors.append('TARGET fields missing: ' + ', '.join(missing_target))
    kind = target.get('kind')
    resolution = target.get('resolution')
    if kind not in TARGET_KINDS:
        errors.append('unknown TARGET.kind: ' + str(kind))
    if resolution not in TARGET_RESOLUTIONS:
        errors.append('unknown TARGET.resolution: ' + str(resolution))
    if target.get('executable', '').lower() != 'false':
        errors.append('TARGET.executable must be false')
    if kind == 'full-kdsl-dev-prompt':
        if target.get('schema') != FULL_KDSL_SCHEMA:
            errors.append('full-kdsl-dev-prompt TARGET.schema mismatch')
        if resolution != 'resolved':
            errors.append('full-kdsl-dev-prompt target must be resolved or explicitly changed to a blocked target')
    elif kind == 'design-only':
        if target.get('schema') != 'design-review' or resolution != 'resolved':
            errors.append('design-only target must use design-review/resolved')
    elif kind in {'P1', 'P1L'}:
        if target.get('schema') != 'unresolved':
            errors.append(kind + ' TARGET.schema must remain unresolved')
        if resolution != 'blocked':
            errors.append(kind + ' target must remain blocked until canonical schema exists')

    map_records = parse_list_records(blocks.get('MAP', {}))
    validate_records('MAP', map_records, {'source', 'target', 'mode', 'evidence'}, errors)
    mapped_sources = set()
    for index, record in enumerate(map_records, start=1):
        source_name = record.get('source', '')
        if source_name:
            mapped_sources.add(source_name)
        mode = record.get('mode')
        if mode not in MAP_MODES:
            errors.append(f'MAP entry {index} unknown mode: {mode}')
        if mode == 'blocked' and resolution == 'resolved':
            errors.append(f'MAP entry {index} blocked mode conflicts with resolved target')
        if not record.get('evidence', '').strip():
            errors.append(f'MAP entry {index} evidence is empty')

    unresolved_records = parse_list_records(blocks.get('UNRESOLVED', {}))
    loss_records = parse_list_records(blocks.get('LOSS', {}))
    if blocks.get('UNRESOLVED', {}).get('value') == '[]':
        unresolved_records = []
    if blocks.get('LOSS', {}).get('value') == '[]':
        loss_records = []
    validate_records('UNRESOLVED', unresolved_records, {'source', 'reason', 'impact'}, errors)
    validate_records('LOSS', loss_records, {'class', 'source', 'detail'}, errors)

    accounted = mapped_sources | {record.get('source', '') for record in unresolved_records} | {
        record.get('source', '') for record in loss_records
    }
    if resolution == 'resolved':
        missing_accounting = sorted(PACKET_SOURCE_FIELDS - accounted)
        if missing_accounting:
            errors.append('resolved target missing Packet field accounting: ' + ', '.join(missing_accounting))

    for index, record in enumerate(unresolved_records, start=1):
        impact = record.get('impact')
        if impact not in {'warning', 'blocked'}:
            errors.append(f'UNRESOLVED entry {index} unknown impact: {impact}')
        if impact == 'blocked' and resolution == 'resolved':
            errors.append(f'UNRESOLVED entry {index} blocked impact conflicts with resolved target')
        if not record.get('reason', '').strip():
            errors.append(f'UNRESOLVED entry {index} reason is empty')

    critical_loss = False
    for index, record in enumerate(loss_records, start=1):
        loss_class = record.get('class')
        if loss_class not in LOSS_CLASSES:
            errors.append(f'LOSS entry {index} unknown class: {loss_class}')
        if loss_class == 'critical':
            critical_loss = True
        if not record.get('detail', '').strip():
            errors.append(f'LOSS entry {index} detail is empty')
    if critical_loss and resolution == 'resolved':
        errors.append('critical LOSS requires blocked target')

    preserve = parse_nested_lists(blocks.get('PRESERVE', {}))
    missing_preserve = sorted(PRESERVE_KEYS - set(preserve))
    if missing_preserve:
        errors.append('PRESERVE classes missing: ' + ', '.join(missing_preserve))
    if resolution == 'resolved':
        for key in sorted(PRESERVE_KEYS):
            if not preserve.get(key):
                warnings.append('resolved target PRESERVE.' + key + ' is empty')

    round_trip, round_duplicates = parse_nested_scalars(blocks.get('ROUND_TRIP', {}))
    for key in round_duplicates:
        errors.append('ROUND_TRIP duplicate field: ' + key)
    required_round = {'state', 'structural_equivalence', 'semantic_equivalence'}
    missing_round = sorted(required_round - set(round_trip))
    if missing_round:
        errors.append('ROUND_TRIP fields missing: ' + ', '.join(missing_round))
    if round_trip.get('state') not in ROUND_TRIP_STATES:
        errors.append('unknown ROUND_TRIP.state: ' + str(round_trip.get('state')))
    if round_trip.get('structural_equivalence') not in STRUCTURAL_EQ:
        errors.append('unknown ROUND_TRIP.structural_equivalence: ' + str(round_trip.get('structural_equivalence')))
    if round_trip.get('semantic_equivalence') != 'not_proven':
        errors.append('ROUND_TRIP.semantic_equivalence must remain not_proven')
    if round_trip.get('state') == 'structural_pass':
        if critical_loss or any(record.get('impact') == 'blocked' for record in unresolved_records):
            errors.append('structural_pass conflicts with critical loss or blocked unresolved item')
        if round_trip.get('structural_equivalence') != 'pass':
            errors.append('structural_pass requires structural_equivalence: pass')
    if round_trip.get('state') == 'loss_detected' and not loss_records:
        errors.append('loss_detected requires LOSS entries')

    authority, authority_duplicates = parse_nested_scalars(blocks.get('AUTHORITY', {}))
    for key in authority_duplicates:
        errors.append('AUTHORITY duplicate field: ' + key)
    if authority.get('source_rails_preserved') not in {'true', 'false'}:
        errors.append('AUTHORITY.source_rails_preserved must be true or false')
    if authority.get('execution_authority') != 'none':
        errors.append('AUTHORITY.execution_authority must be none')
    if authority.get('source_rails_preserved') == 'false' and not (critical_loss and resolution == 'blocked'):
        errors.append('source_rails_preserved:false requires critical loss and blocked target')

    output, output_duplicates = parse_nested_scalars(blocks.get('OUTPUT', {}))
    for key in output_duplicates:
        errors.append('OUTPUT duplicate field: ' + key)
    marker = output.get('marker')
    if marker not in OUTPUT_MARKERS:
        errors.append('unknown OUTPUT.marker: ' + str(marker))
    if output.get('executable', '').lower() != 'false':
        errors.append('OUTPUT.executable must be false')
    preview = extract_multiline(blocks.get('OUTPUT', {}), 'preview')
    inline_preview = output.get('preview', '')
    preview_present = bool(preview.strip()) or inline_preview not in {'', '""', "''"}

    if resolution == 'blocked':
        if marker != 'none':
            errors.append('blocked target requires OUTPUT.marker:none')
        if preview_present:
            errors.append('blocked target requires empty OUTPUT.preview')
    elif kind == 'full-kdsl-dev-prompt':
        if marker != 'KDSL_PROMPT_PREVIEW':
            errors.append('full-kdsl-dev-prompt requires KDSL_PROMPT_PREVIEW marker')
        if not preview_present:
            errors.append('resolved Full KDSL target requires non-empty preview')
    elif kind == 'design-only':
        if marker != 'DESIGN_PREVIEW':
            errors.append('design-only target requires DESIGN_PREVIEW marker')

    info.append('normalization schema checked: ' + str(values.get('SCHEMA')))
    info.append('target checked: ' + str(kind) + '/' + str(resolution))
    info.append('MAP entries checked: ' + str(len(map_records)))
    info.append('LOSS entries checked: ' + str(len(loss_records)))
    info.append('execution authority boundary checked')
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
