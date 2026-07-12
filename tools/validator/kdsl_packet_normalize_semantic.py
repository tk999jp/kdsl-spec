from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from kdsl_packet_normalize import FULL_TARGETS, PACKET_FIELDS, collect_data, load_text, unique

NORMALIZATION_SCHEMA = 'kdsl-packet-normalization@0.1-draft'
PACKET_SCHEMA = 'kdsl-packet@0.1-draft'
FULL_KDSL_SCHEMA = 'format:KDSL/profile:dev-prompt'


def q(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def run_semantic_checker(path: str) -> tuple[int, str]:
    checker = Path(__file__).with_name('kdsl_packet_semantic.py')
    proc = subprocess.run(
        [sys.executable, str(checker), path],
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout.strip() or proc.stderr.strip()


def yaml_list(lines: list[str], indent: int, values: list[str]) -> None:
    prefix = ' ' * indent
    if not values:
        lines.append(prefix + '[]')
        return
    for value in values:
        lines.append(prefix + '- ' + q(value))


def append_map(lines: list[str], source: str, target: str, mode: str, evidence: str) -> None:
    lines.append('    - source: ' + source)
    lines.append('      target: ' + q(target))
    lines.append('      mode: ' + mode)
    lines.append('      evidence: ' + q(evidence))


def record_values(records: list[dict[str, str]], keys: tuple[str, ...]) -> list[str]:
    values: list[str] = []
    for record in records:
        for key in keys:
            value = record.get(key, '').strip()
            if value:
                values.append(value)
    return values


def exact_strings(data: dict) -> list[str]:
    return unique(
        data['src']
        + data['read']
        + data['tgt']
        + data['obs']
        + [data['goal']]
        + data['non']
        + data['stop']
        + data['verify']
        + record_values(data['sg_records'], ('id', 'state', 'scope', 'reason', 'evidence', 'authority'))
        + record_values(data['flow_records'], ('op', 'detail'))
        + [data['result_schema']]
        + [data['authority'].get(rail, '') for rail in ('read', 'edit', 'stage', 'commit', 'push', 'release')]
    )


def protected_wording(data: dict) -> list[str]:
    return unique(
        data['non']
        + data['stop']
        + [record.get('reason', '') for record in data['sg_records']]
        + [
            'TGT外変更禁止',
            '未確認を確認済扱い禁止',
            '未実行verifyをpass扱禁止',
            'build/diff/lint/test/CI pass != RT:v',
            'NEXT実行許可扱禁止',
            'COMMIT自動commit許可扱禁止',
            'KDSL_PROMPT_PREVIEW != KDSL_PROMPT',
            'execution_authority:none',
        ]
    )


def ordered_fields(data: dict) -> list[str]:
    flow = '>'.join(record.get('op', '') for record in data['flow_records'] if record.get('op'))
    values: list[str] = []
    if flow:
        values.append(flow)
    if data['stop']:
        values.append('STOP: ' + ' > '.join(data['stop']))
    if data['verify']:
        values.append('VERIFY: ' + ' > '.join(data['verify']))
    return unique(values)


def build_full_preview(data: dict) -> list[str]:
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
    lines.append('観測/推論/未確認:')
    for value in data['obs']:
        lines.append('- ' + value)
    lines.append('- 未確認を確認済扱い禁止')
    lines.append('対象Slice:')
    for value in data['tgt'] or ['none']:
        lines.append('- ' + value)
    lines.append('非対象/禁止:')
    for value in data['non']:
        lines.append('- ' + value)
    if 'TGT外変更禁止' not in data['non']:
        lines.append('- TGT外変更禁止')

    lines.append('Safety Gates:')
    for record in data['sg_records']:
        fields = [
            'id=' + record.get('id', 'unknown'),
            'state=' + record.get('state', 'unknown'),
            'scope=' + record.get('scope', 'unknown'),
            'reason=' + record.get('reason', 'unknown'),
            'evidence=' + record.get('evidence', 'none'),
            'authority=' + record.get('authority', 'none'),
        ]
        lines.append('- ' + ' / '.join(fields))

    lines.append('停止条件:')
    for value in data['stop']:
        lines.append('- ' + value)

    lines.append('作業手順:')
    for record in data['flow_records']:
        lines.append('- ' + record.get('op', 'FLOW-UNKNOWN') + ': ' + record.get('detail', 'detail unavailable'))

    lines.append('検証要求:')
    for value in data['verify']:
        lines.append('- ' + value)
    lines.append('- 未実行verifyをpass扱禁止')
    lines.append('- build/diff/lint/test/CI pass != RT:v')

    lines.append('報告形式:')
    lines.append('- ' + data['result_schema'])
    lines.append('Authority:')
    for rail in ('read', 'edit', 'stage', 'commit', 'push', 'release'):
        lines.append('- ' + rail + ': ' + data['authority'].get(rail, 'unknown'))

    lines.append('Boundary:')
    lines.append('- KDSL_PROMPT_PREVIEW != KDSL_PROMPT')
    lines.append('- NEXT実行許可扱禁止')
    lines.append('- COMMIT自動commit許可扱禁止')
    lines.append('- execution_authority:none')
    return lines


def build_design_preview(data: dict) -> list[str]:
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


def emit_normalization(text: str, data: dict) -> int:
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
        '  schema: ' + (q(target_schema) if ':' in target_schema else target_schema),
        '  resolution: ' + resolution,
        '  executable: false',
        'MAP:',
        '  entries:',
    ]

    for source in PACKET_FIELDS:
        if blocked:
            append_map(
                lines,
                source,
                target_kind + ' target schema',
                'blocked',
                'canonical ' + target_kind + ' field schema is unresolved',
            )
        else:
            mode = 'exact'
            if source in {'BASE', 'TASK', 'OUT'}:
                mode = 'structured'
            elif source in {'SG', 'FLOW'}:
                mode = 'expanded'
            append_map(
                lines,
                source,
                FULL_TARGETS[source],
                mode,
                'Phase 4 strict mapper preserves source field and reconstruction property',
            )

    lines.extend(['PRESERVE:', '  exact_strings:'])
    yaml_list(lines, 4, exact_strings(data))
    lines.append('  protected_wording:')
    yaml_list(lines, 4, protected_wording(data))
    lines.append('  ordered_fields:')
    yaml_list(lines, 4, ordered_fields(data))

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
        lines.extend('    ' + line for line in preview)
    else:
        lines.append('  preview: ""')

    print('\n'.join(lines))
    return 1 if blocked else 0


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('usage: python kdsl_packet_normalize_semantic.py <packet-file>', file=sys.stderr)
        return 2
    path = argv[1]
    code, output = run_semantic_checker(path)
    if code >= 2:
        print(output, file=sys.stderr)
        return 2
    if code == 1 and output:
        print(output, file=sys.stderr)
    try:
        text = load_text(path)
        data = collect_data(text)
        return emit_normalization(text, data)
    except (OSError, ValueError) as exc:
        print('NORMALIZATION_ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
