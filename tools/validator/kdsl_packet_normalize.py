import hashlib
import json
import subprocess
import sys
from pathlib import Path

from kdsl_packet import (
    blocks_from_entries,
    extract_packet_scope,
    load_text,
    parse_list_field,
    parse_nested_scalars,
    parse_sequence_items,
    parse_top_level,
    unquote,
)

NORMALIZATION_SCHEMA = 'kdsl-packet-normalization@0.1-draft'
PACKET_SCHEMA = 'kdsl-packet@0.1-draft'
FULL_KDSL_SCHEMA = 'format:KDSL/profile:dev-prompt'
PACKET_FIELDS = (
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
FULL_TARGETS = {
    'SCHEMA': 'normalization provenance',
    'STATUS': 'normalization provenance',
    'BASE': 'header/profile basis',
    'TASK': 'Phase/task metadata',
    'SRC': '前提/正本',
    'READ': '前提/読取対象',
    'TGT': '対象Slice/変更対象',
    'OBS': '前提/観測',
    'GOAL': '目的',
    'NON': '非対象/禁止',
    'SG': 'Safety Gates/禁止',
    'STOP': '停止条件',
    'FLOW': '作業手順',
    'VERIFY': '検証',
    'OUT': '報告形式',
    'AUTHORITY': 'Authority/禁止',
    'NORMALIZE': 'normalization provenance',
}


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def unique(values):
    seen = set()
    result = []
    for value in values:
        value = str(value)
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def parse_records(block):
    records = []
    current = None
    for raw_line in block.get('lines', []):
        stripped = raw_line.strip()
        if stripped.startswith('- '):
            if current is not None:
                records.append(current)
            current = {}
            payload = stripped[2:]
            if ':' in payload:
                key, value = payload.split(':', 1)
                current[key.strip().lower()] = unquote(value.strip())
            continue
        if current is not None and ':' in stripped:
            key, value = stripped.split(':', 1)
            current[key.strip().lower()] = unquote(value.strip())
    if current is not None:
        records.append(current)
    return records


def validate_source(path):
    checker = Path(__file__).with_name('kdsl_packet.py')
    proc = subprocess.run(
        [sys.executable, str(checker), path],
        text=True,
        capture_output=True,
    )
    if proc.returncode >= 2:
        if proc.stdout:
            print(proc.stdout.rstrip(), file=sys.stderr)
        if proc.stderr:
            print(proc.stderr.rstrip(), file=sys.stderr)
        return False, proc.returncode
    if proc.returncode == 1 and proc.stdout:
        print(proc.stdout.rstrip(), file=sys.stderr)
    return True, proc.returncode


def yaml_list(lines, indent, values):
    prefix = ' ' * indent
    if not values:
        lines.append(prefix + '[]')
        return
    for value in values:
        lines.append(prefix + '- ' + q(value))


def append_map(lines, source, target, mode, evidence):
    lines.append('    - source: ' + source)
    lines.append('      target: ' + q(target))
    lines.append('      mode: ' + mode)
    lines.append('      evidence: ' + q(evidence))


def build_full_preview(data):
    lines = [
        'KDSL_PROMPT_PREVIEW:',
        'format: KDSL',
        'profile: dev-prompt',
        'mode: min',
        'safety: lock-critical',
        'execution: prohibited',
        'Phase: ' + data['task_id'],
        '目的: ' + data['goal'],
        '前提:',
    ]
    for value in data['src']:
        lines.append('- SRC: ' + value)
    for value in data['read']:
        lines.append('- READ: ' + value)
    for value in data['obs']:
        lines.append('- OBS: ' + value)
    lines.append('- 未確認を確認済扱い禁止')
    lines.append('対象Slice:')
    for value in data['tgt'] or ['none']:
        lines.append('- ' + value)
    lines.append('非対象/禁止:')
    for value in data['non'] or ['TGT外変更禁止']:
        lines.append('- ' + value)
    if 'TGT外変更禁止' not in data['non']:
        lines.append('- TGT外変更禁止')
    lines.append('Safety Gates:')
    for record in data['sg_records']:
        gate_id = record.get('id', 'unknown')
        state = record.get('state', 'unknown')
        reason = record.get('reason', 'reason unavailable')
        lines.append(f'- {gate_id} / {state} / {reason}')
    lines.append('停止条件:')
    for value in data['stop'] or ['required stop conditions unavailable']:
        lines.append('- ' + value)
    lines.append('作業手順:')
    for record in data['flow_records']:
        op = record.get('op', 'FLOW-UNKNOWN')
        detail = record.get('detail', 'detail unavailable')
        lines.append(f'- {op}: {detail}')
    lines.append('検証:')
    for value in data['verify']:
        lines.append('- ' + value)
    lines.append('- 未実行verifyをpass扱禁止')
    lines.append('- build/diff/lint/test/CI pass != RT:v')
    lines.append('報告形式:')
    lines.append('- ' + data['result_schema'])
    lines.append('Authority:')
    for rail in ('read', 'edit', 'stage', 'commit', 'push', 'release'):
        lines.append(f'- {rail}: {data["authority"].get(rail, "unknown")}')
    lines.append('Boundary:')
    lines.append('- KDSL_PROMPT_PREVIEW != KDSL_PROMPT')
    lines.append('- NEXT/COMMIT提案 != 実行authority')
    return lines


def build_design_preview(data):
    lines = [
        'DESIGN_PREVIEW:',
        'STATUS: non-executable',
        'TASK: ' + data['task_id'],
        'GOAL: ' + data['goal'],
        'TARGETS:',
    ]
    for value in data['tgt'] or ['none']:
        lines.append('- ' + value)
    lines.append('NON-GOALS:')
    for value in data['non'] or ['none']:
        lines.append('- ' + value)
    lines.append('BOUNDARY: review only / execution prohibited')
    return lines


def collect_data(text):
    scope = extract_packet_scope(text)
    if scope is None:
        raise ValueError('PACKET_DRAFT block not found')
    entries, _ = parse_top_level(scope)
    values = {key: value for key, value, _ in entries}
    blocks = blocks_from_entries(scope, entries)

    base, _ = parse_nested_scalars(blocks.get('BASE', {}))
    task, _ = parse_nested_scalars(blocks.get('TASK', {}))
    authority, _ = parse_nested_scalars(blocks.get('AUTHORITY', {}))
    normalize, _ = parse_nested_scalars(blocks.get('NORMALIZE', {}))
    out, _ = parse_nested_scalars(blocks.get('OUT', {}))

    return {
        'values': values,
        'base_id': base.get('id', ''),
        'task_id': task.get('id', ''),
        'src': parse_sequence_items(blocks.get('SRC', {})),
        'read': parse_sequence_items(blocks.get('READ', {})),
        'tgt': parse_sequence_items(blocks.get('TGT', {})),
        'obs': parse_sequence_items(blocks.get('OBS', {})),
        'goal': unquote(values.get('GOAL', '')),
        'non': parse_sequence_items(blocks.get('NON', {})),
        'stop': parse_sequence_items(blocks.get('STOP', {})),
        'verify': parse_sequence_items(blocks.get('VERIFY', {})),
        'sg_records': parse_records(blocks.get('SG', {})),
        'flow_records': parse_records(blocks.get('FLOW', {})),
        'authority': authority,
        'normalize_target': normalize.get('target', ''),
        'result_schema': out.get('result_schema', 'canonical-r1'),
    }


def emit_normalization(text, data):
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    base_id = data['base_id']
    blocked = False

    if base_id == 'BASE-KDSL-DEV':
        target_kind = 'full-kdsl-dev-prompt'
        target_schema = FULL_KDSL_SCHEMA
        resolution = 'resolved'
        output_marker = 'KDSL_PROMPT_PREVIEW'
        preview = build_full_preview(data)
    elif base_id == 'BASE-DESIGN-ONLY':
        target_kind = 'design-only'
        target_schema = 'design-review'
        resolution = 'resolved'
        output_marker = 'DESIGN_PREVIEW'
        preview = build_design_preview(data)
    elif base_id == 'BASE-ADPS-P1':
        target_kind = data['normalize_target'] if data['normalize_target'] in {'P1', 'P1L'} else 'P1'
        target_schema = 'unresolved'
        resolution = 'blocked'
        output_marker = 'none'
        preview = []
        blocked = True
    else:
        raise ValueError('unsupported BASE ID: ' + base_id)

    exact_strings = unique(
        data['src'] + data['read'] + data['tgt'] + data['verify'] + [data['result_schema']]
    )
    protected_wording = unique(
        data['non']
        + data['stop']
        + [record.get('reason', '') for record in data['sg_records']]
        + ['KDSL_PROMPT_PREVIEW != KDSL_PROMPT', 'execution_authority:none']
    )
    flow_order = '>'.join(record.get('op', '') for record in data['flow_records'] if record.get('op'))
    ordered_fields = unique(
        [flow_order]
        + (['STOP: ' + ' > '.join(data['stop'])] if data['stop'] else [])
        + (['VERIFY: ' + ' > '.join(data['verify'])] if data['verify'] else [])
    )

    lines = [
        'NORMALIZATION_DRAFT:',
        'SCHEMA: ' + NORMALIZATION_SCHEMA,
        'STATUS: non-executable',
        'SOURCE:',
        '  schema: ' + PACKET_SCHEMA,
        '  digest: ' + q('sha256:' + digest),
        '  packet_status: non-executable',
        '  normalize_state: not_normalized',
        'TARGET:',
        '  kind: ' + target_kind,
        '  schema: ' + q(target_schema) if ':' in target_schema else '  schema: ' + target_schema,
        '  resolution: ' + resolution,
        '  executable: false',
        'MAP:',
        '  entries:',
    ]

    if blocked:
        for source in PACKET_FIELDS:
            append_map(
                lines,
                source,
                target_kind + ' target schema',
                'blocked',
                'canonical ' + target_kind + ' field schema is unresolved',
            )
    else:
        for source in PACKET_FIELDS:
            mode = 'exact'
            if source in {'BASE', 'TASK', 'OUT'}:
                mode = 'structured'
            elif source in {'SG', 'FLOW'}:
                mode = 'expanded'
            append_map(lines, source, FULL_TARGETS[source], mode, 'source field retained by first-slice mapper')

    lines.extend(['PRESERVE:', '  exact_strings:'])
    yaml_list(lines, 4, exact_strings)
    lines.append('  protected_wording:')
    yaml_list(lines, 4, protected_wording)
    lines.append('  ordered_fields:')
    yaml_list(lines, 4, ordered_fields)

    if blocked:
        lines.extend(
            [
                'UNRESOLVED:',
                '  - source: ' + q(target_kind + ' target field schema'),
                '    reason: ' + q('canonical target schema not present in repository'),
                '    impact: blocked',
            ]
        )
    else:
        lines.append('UNRESOLVED: []')

    lines.extend(
        [
            'LOSS: []',
            'ROUND_TRIP:',
            '  state: ' + ('blocked' if blocked else 'not_tested'),
            '  structural_equivalence: not_proven',
            '  semantic_equivalence: not_proven',
            'AUTHORITY:',
            '  source_rails_preserved: true',
            '  execution_authority: none',
            'OUTPUT:',
            '  marker: ' + output_marker,
            '  executable: false',
        ]
    )

    if preview:
        lines.append('  preview: |')
        for line in preview:
            lines.append('    ' + line)
    else:
        lines.append('  preview: ""')

    print('\n'.join(lines))
    return 1 if blocked else 0


def main(argv):
    if len(argv) != 2:
        print('usage: python kdsl_packet_normalize.py <packet-file>', file=sys.stderr)
        return 2
    path = argv[1]
    valid, code = validate_source(path)
    if not valid:
        return 2
    try:
        text = load_text(path)
        data = collect_data(text)
        return emit_normalization(text, data)
    except (OSError, ValueError) as exc:
        print('NORMALIZATION_ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
