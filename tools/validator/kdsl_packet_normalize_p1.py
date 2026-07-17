from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from kdsl_p1_contract import (
    P1L_SCHEMA_ID,
    P1_SCHEMA_ID,
    ContractParseResult,
    canonical_json,
    compare_models,
    parse_p1_line,
    render_p1,
    validate_model,
)
from kdsl_packet_normalize import PACKET_FIELDS, collect_data, load_text, unique

NORMALIZATION_SCHEMA = 'kdsl-packet-normalization@0.1-draft'
PACKET_SCHEMA = 'kdsl-packet@0.1-draft'

TASK_MAP = {
    'TASK-INSPECT': 'investigate',
    'TASK-PLAN': 'plan',
    'TASK-CHANGE': 'implement',
    'TASK-VERIFY': 'review',
    'TASK-CLOSEOUT': 'closeout',
    'TASK-PUBLIC': 'other',
    'TASK-DATA': 'other',
}

P1L_TARGETS = {
    'SCHEMA': 'SOURCE.schema / normalization provenance',
    'STATUS': 'SOURCE.packet_status / normalization provenance',
    'BASE': 'SOURCE.kind / PROFILE / BINDING boundary',
    'TASK': 'TASK.kind / TASK.declared',
    'SRC': 'SOURCE.references / SCOPE.source',
    'READ': 'SCOPE.read',
    'TGT': 'SCOPE.target',
    'OBS': 'CONTEXT.observed/inferred/unverified',
    'GOAL': 'GOAL.expected',
    'NON': 'SCOPE.non_target / GUARD.constraints / GUARD.protected_wording',
    'SG': 'GUARD.safety_gates / GUARD.protected_wording',
    'STOP': 'STOP / GUARD.protected_wording',
    'FLOW': 'PLAN.steps',
    'VERIFY': 'VERIFY.requirements / RUNTIME.required_evidence',
    'OUT': 'OUTPUT.result_schema / OUTPUT.report_requirements',
    'AUTHORITY': 'AUTHORITY source rails + explicit safety-floor rails',
    'NORMALIZE': 'NORMALIZATION / BINDING provenance',
}

PROTECTED_BOUNDARIES = [
    'TGT外変更禁止',
    '未確認を確認済扱い禁止',
    '未実行verifyをpass扱禁止',
    'build/diff/lint/test/CI pass != RT:v',
    'NEXT実行許可扱禁止',
    'COMMIT自動commit許可扱禁止',
    'KDSL-DP直接実行禁止',
    'P1/P1L正規化必須',
    'P1L_PREVIEW != P1L:',
    'P1_PREVIEW != P1|',
    'execution_authority:none',
]


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


def append_map(lines: list[str], source: str, target: str, mode: str, evidence: str) -> None:
    lines.append('    - source: ' + source)
    lines.append('      target: ' + q(target))
    lines.append('      mode: ' + mode)
    lines.append('      evidence: ' + q(evidence))


def yaml_list(lines: list[str], indent: int, values: list[str]) -> None:
    prefix = ' ' * indent
    if not values:
        lines.append(prefix + '[]')
        return
    for value in values:
        lines.append(prefix + '- ' + q(value))


def record_values(records: list[dict[str, str]], keys: tuple[str, ...]) -> list[str]:
    values: list[str] = []
    for record in records:
        for key in keys:
            value = record.get(key, '').strip()
            if value:
                values.append(value)
    return values


def classify_observations(values: list[str]) -> dict[str, list[str]]:
    classified = {'observed': [], 'inferred': [], 'unverified': []}
    for raw in values:
        value = str(raw)
        prefix, separator, payload = value.partition(':')
        key = prefix.strip().lower()
        if separator and key in classified:
            classified[key].append(payload.strip())
        else:
            # Unlabelled Packet observations are never promoted to observed facts.
            classified['unverified'].append(value)
    return classified


def runtime_evidence(values: list[str]) -> list[str]:
    return [
        value
        for value in values
        if any(token in value.lower() for token in ('runtime', 'rt:v', '実機', 'target environment'))
    ]


def build_model(text: str, data: dict[str, Any]) -> dict[str, Any]:
    digest_hex = hashlib.sha256(text.encode('utf-8')).hexdigest()
    source_digest = 'sha256:' + digest_hex
    task_kind = TASK_MAP.get(data['task_id'])
    if task_kind is None:
        raise ValueError('unsupported Packet TASK for P1L mapping: ' + data['task_id'])

    context = classify_observations(data['obs'])
    flow_steps = [
        record.get('op', 'FLOW-UNKNOWN') + ': ' + record.get('detail', 'detail unavailable')
        for record in data['flow_records']
    ]
    safety_gates = [
        {
            key: record.get(key, '')
            for key in ('id', 'state', 'scope', 'reason', 'evidence', 'authority')
        }
        for record in data['sg_records']
    ]
    protected = unique(
        data['non']
        + data['stop']
        + [record.get('reason', '') for record in data['sg_records']]
        + PROTECTED_BOUNDARIES
    )

    source_authority = data['authority']
    authority = {
        rail: source_authority.get(rail, '')
        for rail in ('read', 'edit', 'stage', 'commit', 'push', 'release')
    }
    # Packet v0.1 has six rails. Canonical P1L has eight. The mapper adds an
    # explicit non-widening safety floor rather than inferring permission.
    authority['public_repo'] = 'forbid'
    authority['destructive_ops'] = 'forbid'

    model: dict[str, Any] = {
        'SCHEMA': P1L_SCHEMA_ID,
        'STATUS': 'contract-candidate',
        'META': {
            'contract_rev': '0.1',
            'contract_id': 'packet-' + digest_hex[:16],
            'parent_id': 'none',
        },
        'SOURCE': {
            'kind': 'packet',
            'digest': source_digest,
            'references': list(data['src']),
        },
        'PROFILE': {
            'id': 'none',
            'revision': 'none',
            'digest': 'none',
            'completion': 'explicit',
            'completed_fields': [],
        },
        'TASK': {
            'kind': task_kind,
            'declared': data['task_id'],
        },
        'SCOPE': {
            'source': list(data['src']),
            'read': list(data['read']),
            'target': list(data['tgt']),
            'non_target': list(data['non']),
        },
        'CONTEXT': {
            'background': [],
            'observed': context['observed'],
            'inferred': context['inferred'],
            'unverified': context['unverified'],
        },
        'GOAL': {
            'expected': [data['goal']],
            'questions': [],
        },
        'PLAN': {
            'strategy': [],
            'steps': flow_steps,
        },
        'GUARD': {
            'constraints': list(data['non']),
            'safety_gates': safety_gates,
            'protected_wording': protected,
        },
        'STOP': list(data['stop']),
        'VERIFY': {
            'requirements': list(data['verify']),
            'unavailable_policy': 'report_not_run',
        },
        'RUNTIME': {
            'disposition': 'pending',
            'required_evidence': runtime_evidence(data['verify']),
        },
        'OUTPUT': {
            'result_schema': data['result_schema'],
            'report_requirements': [
                'NEXT remains proposal only',
                'COMMIT remains non-authoritative unless actually executed',
            ],
        },
        'AUTHORITY': authority,
        'NORMALIZATION': {
            'state': 'explicit',
            'unresolved': [],
            'loss': [],
            'round_trip': 'structural_pass',
            'semantic_equivalence': 'not_proven',
        },
        'BINDING': {
            'runtime_control': 'unresolved',
            'state': 'unbound',
            'executable': False,
        },
    }

    validation = ContractParseResult(kind='P1L', model=model)
    validate_model(model, validation)
    if validation.errors:
        raise ValueError('generated P1L model failed validation: ' + '; '.join(validation.errors))

    rendered = render_p1(model)
    reconstructed = parse_p1_line(rendered)
    if reconstructed.errors or reconstructed.model is None:
        raise ValueError('generated P1 failed validation: ' + '; '.join(reconstructed.errors))
    mismatches = compare_models(model, reconstructed.model)
    if mismatches:
        raise ValueError('generated P1 round-trip mismatch: ' + '; '.join(mismatches))
    return model


def exact_strings(data: dict[str, Any]) -> list[str]:
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


def protected_wording(model: dict[str, Any]) -> list[str]:
    return list(model['GUARD']['protected_wording'])


def ordered_fields(data: dict[str, Any]) -> list[str]:
    values: list[str] = []
    flow = '>'.join(record.get('op', '') for record in data['flow_records'] if record.get('op'))
    if flow:
        values.append(flow)
    if data['stop']:
        values.append('STOP: ' + ' > '.join(data['stop']))
    if data['verify']:
        values.append('VERIFY: ' + ' > '.join(data['verify']))
    return unique(values)


def preview_lines(target_kind: str, model: dict[str, Any]) -> tuple[str, list[str]]:
    if target_kind == 'P1L':
        return (
            'P1L_PREVIEW',
            [
                'P1L_PREVIEW:',
                'SCHEMA: ' + P1L_SCHEMA_ID,
                'STATUS: non-executable-preview',
                'PROJECTION_JSON: ' + canonical_json(model),
                'BOUNDARY: P1L_PREVIEW != P1L: / execution prohibited',
            ],
        )
    rendered = render_p1(model)
    return (
        'P1_PREVIEW',
        [
            'P1_PREVIEW:',
            'SCHEMA: ' + P1_SCHEMA_ID,
            'STATUS: non-executable-preview',
            'SERIALIZATION_JSON: ' + json.dumps(rendered, ensure_ascii=False),
            'BOUNDARY: P1_PREVIEW != P1| / execution prohibited',
        ],
    )


def emit_normalization(text: str, data: dict[str, Any]) -> int:
    if data['base_id'] != 'BASE-ADPS-P1':
        raise ValueError('P1 mapper requires BASE-ADPS-P1')
    target_kind = data['normalize_target']
    if target_kind not in {'P1', 'P1L'}:
        raise ValueError('P1 mapper requires NORMALIZE.target P1 or P1L')

    model = build_model(text, data)
    target_schema = P1L_SCHEMA_ID if target_kind == 'P1L' else P1_SCHEMA_ID
    output_marker, preview = preview_lines(target_kind, model)
    digest_hex = hashlib.sha256(text.encode('utf-8')).hexdigest()

    lines = [
        'NORMALIZATION_DRAFT:',
        'SCHEMA: ' + NORMALIZATION_SCHEMA,
        'STATUS: non-executable',
        'SOURCE:',
        '  schema: ' + PACKET_SCHEMA,
        '  digest: ' + q('sha256:' + digest_hex),
        '  packet_status: non-executable',
        '  normalize_state: not_normalized',
        'TARGET:',
        '  kind: ' + target_kind,
        '  schema: ' + target_schema,
        '  resolution: resolved',
        '  executable: false',
        'MAP:',
        '  entries:',
    ]

    for source in PACKET_FIELDS:
        mode = 'exact'
        if source in {'BASE', 'TASK', 'OUT', 'AUTHORITY', 'NORMALIZE'}:
            mode = 'structured'
        elif source in {'OBS', 'SG', 'FLOW'}:
            mode = 'expanded'
        evidence = 'Phase 7D Packet→P1L mapping rule'
        if source == 'AUTHORITY':
            evidence += '; six source rails preserved; public_repo/destructive_ops explicitly narrowed to forbid'
        append_map(lines, source, P1L_TARGETS[source], mode, evidence)

    lines.extend(['PRESERVE:', '  exact_strings:'])
    yaml_list(lines, 4, exact_strings(data))
    lines.append('  protected_wording:')
    yaml_list(lines, 4, protected_wording(model))
    lines.append('  ordered_fields:')
    yaml_list(lines, 4, ordered_fields(data))
    lines.extend(
        [
            'UNRESOLVED: []',
            'LOSS: []',
            'ROUND_TRIP:',
            '  state: structural_pass',
            '  structural_equivalence: pass',
            '  semantic_equivalence: not_proven',
            'AUTHORITY:',
            '  source_rails_preserved: true',
            '  execution_authority: none',
            'OUTPUT:',
            '  marker: ' + output_marker,
            '  executable: false',
            '  preview: |',
        ]
    )
    lines.extend('    ' + line for line in preview)
    print('\n'.join(lines))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('usage: python kdsl_packet_normalize_p1.py <packet-file>', file=sys.stderr)
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
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('P1_NORMALIZATION_ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
