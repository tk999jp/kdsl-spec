from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from kdsl_packet import (
    AUTHORITY_RAILS,
    KNOWN_SG_IDS,
    SG_REGISTRY,
    blocks_from_entries,
    extract_packet_scope,
    load_text,
    parse_nested_scalars,
    parse_sequence_items,
    parse_top_level,
    unquote,
)
from kdsl_safety_semantics import check_semantics

MODEL_ID = 'kdsl-packet-semantic@0.1-draft'
ALLOWED_SG_STATES = {'hold', 'satisfied', 'blocked', 'na'}
ALLOWED_SG_FIELDS = {'id', 'state', 'scope', 'reason', 'evidence', 'authority'}
REQUIRED_SG_FIELDS = {'id', 'state', 'scope', 'reason'}
OBS_CLASSES = {'observed', 'inferred', 'not_observed', 'unverified'}
ALLOW_RAIL_VALUES = {'allow', 'allow_once', 'target_only'}
EMPTY_MARKERS = {'', 'none', 'null', 'unknown', 'unverified', 'not_established', 'not established'}


def emit(errors: list[str], warnings: list[str], info: list[str]) -> int:
    status = 'fail' if errors else ('warn' if warnings else 'pass')
    print('PACKET_SEMANTIC_RESULT:')
    print('STATUS: ' + status)
    print('MODEL: ' + MODEL_ID)
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('WARNINGS:')
    for item in warnings or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    print('FULL_SEMANTIC_EQUIVALENCE: not_proven')
    print('FULL_SAFETY_PROOF: not_proven')
    print('EXECUTION_AUTHORITY: none')
    return 2 if errors else (1 if warnings else 0)


def parse_records(block: dict) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
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


def run_base_checker(path: str) -> tuple[int, str]:
    checker = Path(__file__).with_name('kdsl_packet.py')
    proc = subprocess.run(
        [sys.executable, str(checker), path],
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout.strip() or proc.stderr.strip()


def parse_packet(text: str) -> dict:
    scope = extract_packet_scope(text)
    if scope is None:
        raise ValueError('PACKET_DRAFT block not found')
    entries, duplicates = parse_top_level(scope)
    values = {key: value for key, value, _ in entries}
    blocks = blocks_from_entries(scope, entries)
    authority, _ = parse_nested_scalars(blocks.get('AUTHORITY', {}))
    normalize, _ = parse_nested_scalars(blocks.get('NORMALIZE', {}))
    return {
        'scope': scope,
        'duplicates': duplicates,
        'values': values,
        'blocks': blocks,
        'authority': authority,
        'normalize': normalize,
        'obs': parse_sequence_items(blocks.get('OBS', {})),
        'stop': parse_sequence_items(blocks.get('STOP', {})),
        'verify': parse_sequence_items(blocks.get('VERIFY', {})),
        'sg_records': parse_records(blocks.get('SG', {})),
        'flow_records': parse_records(blocks.get('FLOW', {})),
    }


def classify_observation(item: str) -> tuple[str | None, str]:
    match = re.match(r'^\s*(observed|inferred|not_observed|unverified)\s*:\s*(.+?)\s*$', item, re.IGNORECASE)
    if not match:
        return None, item.strip()
    return match.group(1).lower(), match.group(2).strip()


def is_empty_marker(value: str | None) -> bool:
    return str(value or '').strip().lower() in EMPTY_MARKERS


def check_safety_gates(text: str, records: list[dict[str, str]]) -> tuple[list[str], list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    gate_ids: list[str] = []
    seen: set[str] = set()

    if not records:
        errors.append('Packet semantic surface requires SG entries')
        return errors, warnings, info, gate_ids

    for index, record in enumerate(records, start=1):
        unknown = sorted(set(record) - ALLOWED_SG_FIELDS)
        if unknown:
            errors.append(f'SG entry {index} unknown fields: ' + ', '.join(unknown))
        missing = sorted(REQUIRED_SG_FIELDS - set(record))
        if missing:
            errors.append(f'SG entry {index} missing fields: ' + ', '.join(missing))

        gate_id = record.get('id', '').strip()
        state = record.get('state', '').strip()
        scope = record.get('scope', '').strip()
        reason = record.get('reason', '').strip()
        evidence = record.get('evidence', '').strip()
        authority = record.get('authority', '').strip()

        if gate_id:
            gate_ids.append(gate_id)
            if gate_id in seen:
                errors.append('duplicate Packet Safety Gate ID: ' + gate_id)
            seen.add(gate_id)
            if gate_id not in KNOWN_SG_IDS:
                errors.append('unknown Packet Safety Gate ID: ' + gate_id)
        if state not in ALLOWED_SG_STATES:
            errors.append(f'SG entry {index} unknown state: {state}')
        if not scope or is_empty_marker(scope):
            errors.append(f'SG entry {index} scope must be explicit')
        if not reason or is_empty_marker(reason):
            errors.append(f'SG entry {index} reason must be explicit')

        if state == 'satisfied':
            if is_empty_marker(evidence):
                errors.append(f'SG entry {index} satisfied requires evidence')
            if gate_id in {'SG-DESIGN', 'SG-AUTHORITY', 'SG-PUBLIC', 'SG-DATA'} and is_empty_marker(authority):
                errors.append(f'SG entry {index} satisfied requires authority reference')
        elif state == 'blocked':
            if is_empty_marker(evidence):
                errors.append(f'SG entry {index} blocked requires observed evidence')
        elif state == 'na':
            if is_empty_marker(reason):
                errors.append(f'SG entry {index} na requires explicit reason')
        elif state == 'hold':
            if authority.lower() in {'allow', 'allow_once', 'approved', 'granted'}:
                errors.append(f'SG entry {index} hold conflicts with granting authority wording')

    semantic_errors, semantic_warnings, semantic_info, _ = check_semantics(text, gate_ids)
    errors.extend(semantic_errors)
    warnings.extend(semantic_warnings)
    info.extend(semantic_info)
    return errors, warnings, info, gate_ids


def check_observations(items: list[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    info: list[str] = []
    seen: dict[str, str] = {}
    for index, item in enumerate(items, start=1):
        category, payload = classify_observation(item)
        if category not in OBS_CLASSES:
            errors.append(f'OBS entry {index} must use observed|inferred|not_observed|unverified prefix')
            continue
        normalized = payload.casefold()
        previous = seen.get(normalized)
        if previous is not None and previous != category:
            errors.append(f'OBS classification conflict: {previous} vs {category}: {payload}')
        else:
            seen[normalized] = category
        info.append(f'OBS.{category}: {payload}')
    return errors, info


def check_flow_and_authority(data: dict) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    flow_records = data['flow_records']
    authority = data['authority']
    sg_records = data['sg_records']
    stop = data['stop']

    blocked = [record for record in sg_records if record.get('state') == 'blocked']
    held_ids = {record.get('id') for record in sg_records if record.get('state') == 'hold'}
    ops = [record.get('op', '') for record in flow_records]

    if blocked and 'FLOW-CHANGE' in ops:
        errors.append('blocked Safety Gate conflicts with FLOW-CHANGE')
    if (blocked or held_ids) and not stop:
        errors.append('hold/blocked Safety Gate requires explicit STOP entries')

    for index, record in enumerate(flow_records, start=1):
        unknown = sorted(set(record) - {'op', 'detail'})
        if unknown:
            errors.append(f'FLOW entry {index} unknown fields: ' + ', '.join(unknown))
        op = record.get('op', '').strip()
        detail = record.get('detail', '').strip()
        if not op or not detail:
            errors.append(f'FLOW entry {index} requires op and detail')
            continue
        if op == 'FLOW-READ' and authority.get('read') not in ALLOW_RAIL_VALUES:
            errors.append('FLOW-READ requires explicit read authority rail')
        if op == 'FLOW-CHANGE' and authority.get('edit') not in ALLOW_RAIL_VALUES:
            conditional = re.search(r'after|only after|承認後|authority|権限|gate|正規化後', detail, re.IGNORECASE)
            if not conditional or 'SG-AUTHORITY' not in held_ids:
                errors.append('FLOW-CHANGE without edit authority must remain explicitly conditional on SG-AUTHORITY')
        if op == 'FLOW-VERIFY' and not data['verify']:
            errors.append('FLOW-VERIFY requires VERIFY requirements')

    if authority.get('push') in {'forbid', 'not_requested', 'not_applicable'}:
        for record in flow_records:
            if re.search(r'\bgit\s+push\b|\bpush\b', record.get('detail', ''), re.IGNORECASE):
                errors.append('FLOW detail conflicts with push authority rail')
    if authority.get('release') in {'forbid', 'not_requested', 'not_applicable'}:
        for record in flow_records:
            if re.search(r'git\s+tag|GitHub Release|Release Assets|publish release', record.get('detail', ''), re.IGNORECASE):
                errors.append('FLOW detail conflicts with release authority rail')

    for item in data['verify']:
        if re.search(r'\bpass(?:ed)?\b|\bsuccess\b|実行済|確認済|成功', item, re.IGNORECASE) and not re.search(
            r'未実行|扱禁止|requirement|要求', item, re.IGNORECASE
        ):
            errors.append('Packet VERIFY must describe a requirement, not completed evidence: ' + item)

    info.append('FLOW semantic records checked: ' + str(len(flow_records)))
    info.append('Authority rails checked: ' + str(len(AUTHORITY_RAILS)))
    return errors, warnings, info


def validate_packet_semantics(text: str) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    data = parse_packet(text)

    sg_block = data['blocks'].get('SG', {})
    registry, _ = parse_nested_scalars(sg_block)
    if registry.get('registry') != SG_REGISTRY:
        errors.append('SG.registry must be ' + SG_REGISTRY)

    sg_errors, sg_warnings, sg_info, gate_ids = check_safety_gates(text, data['sg_records'])
    errors.extend(sg_errors)
    warnings.extend(sg_warnings)
    info.extend(sg_info)

    obs_errors, obs_info = check_observations(data['obs'])
    errors.extend(obs_errors)
    info.extend(obs_info)

    flow_errors, flow_warnings, flow_info = check_flow_and_authority(data)
    errors.extend(flow_errors)
    warnings.extend(flow_warnings)
    info.extend(flow_info)

    if data['normalize'].get('state') != 'not_normalized':
        errors.append('Packet semantic surface requires NORMALIZE.state:not_normalized')
    if re.search(r'^\s*(?:KDSL_PROMPT|P1|P1L)\s*:', text, re.MULTILINE):
        errors.append('Packet contains executable target marker')

    info.append('Safety Gate records checked: ' + str(len(data['sg_records'])))
    info.append('Safety Gate IDs: ' + ', '.join(gate_ids))
    info.append('Packet remains non-executable and not_normalized')
    return errors, warnings, info


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) > 1 else '-'
    base_code, base_output = run_base_checker(path)
    if base_code >= 2:
        return emit(['base Packet checker failed', base_output], [], [])
    try:
        text = load_text(path)
        errors, warnings, info = validate_packet_semantics(text)
    except (OSError, ValueError) as exc:
        return emit(['Packet semantic parse failed: ' + str(exc)], [], [])
    if base_code == 1:
        warnings.append('base Packet checker returned warning')
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
