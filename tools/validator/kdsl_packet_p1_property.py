from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from kdsl_p1_bootstrap import ContractParseResult, compare_models, parse_p1_line, validate_model
from kdsl_packet_normalize import collect_data, load_text
from kdsl_packet_normalize_p1 import (
    NORMALIZATION_SCHEMA,
    PACKET_SCHEMA,
    P1L_SCHEMA_ID,
    P1L_TARGETS,
    P1_SCHEMA_ID,
    build_model,
    exact_strings,
    ordered_fields,
    protected_wording,
)
from kdsl_parser_v2_normalization_compat import (
    NormalizationCompatibilityView,
    compare_normalization_legacy_v2,
)

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
PACKET_SOURCE_FIELDS = frozenset(
    {
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
)
MAP_MODES = {
    source: (
        'structured'
        if source in {'BASE', 'TASK', 'OUT', 'AUTHORITY', 'NORMALIZE'}
        else ('expanded' if source in {'OBS', 'SG', 'FLOW'} else 'exact')
    )
    for source in PACKET_SOURCE_FIELDS
}


def emit(status: str, errors: list[str], info: list[str]) -> int:
    print('PACKET_P1_PROPERTY_RESULT:')
    print('STATUS: ' + status)
    print('EXECUTABLE: no')
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    return 0 if status == 'property_pass' else 2


def run_source_checker(path: str) -> tuple[int, str]:
    checker = Path(__file__).with_name('kdsl_packet_semantic.py')
    proc = subprocess.run(
        [sys.executable, str(checker), path],
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout.strip() or proc.stderr.strip()


def generate_normalization(path: str) -> tuple[int, str]:
    mapper = Path(__file__).with_name('kdsl_packet_normalize_p1.py')
    proc = subprocess.run(
        [sys.executable, str(mapper), path],
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout.strip() or proc.stderr.strip()


def validate_preview(
    kind: str,
    marker: str,
    preview: str,
    expected_model: dict[str, Any],
    errors: list[str],
    info: list[str],
) -> None:
    lines = preview.splitlines()
    if re.search(r'^\s*(?:P1L\s*:|P1\|)', preview, re.MULTILINE):
        errors.append('canonical P1L/P1 executable-looking marker exposed in preview')

    if kind == 'P1L':
        if marker != 'P1L_PREVIEW':
            errors.append('P1L target requires OUTPUT.marker:P1L_PREVIEW')
        if 'P1L_PREVIEW:' not in lines:
            errors.append('P1L_PREVIEW marker missing from preview')
        projection_line = next((line for line in lines if line.startswith('PROJECTION_JSON: ')), None)
        if projection_line is None:
            errors.append('P1L preview projection JSON missing')
            return
        try:
            model = json.loads(projection_line.split(': ', 1)[1])
        except json.JSONDecodeError as exc:
            errors.append('P1L preview projection JSON invalid: ' + exc.msg)
            return
        validation = ContractParseResult(kind='P1L', model=model)
        validate_model(model, validation)
        errors.extend('P1L preview model: ' + item for item in validation.errors)
        mismatches = compare_models(expected_model, model)
        errors.extend(mismatches)
        if not validation.errors and not mismatches:
            info.append('P1L preview canonical projection preserved')
        return

    if marker != 'P1_PREVIEW':
        errors.append('P1 target requires OUTPUT.marker:P1_PREVIEW')
    if 'P1_PREVIEW:' not in lines:
        errors.append('P1_PREVIEW marker missing from preview')
    serialization_line = next((line for line in lines if line.startswith('SERIALIZATION_JSON: ')), None)
    if serialization_line is None:
        errors.append('P1 preview serialization JSON missing')
        return
    try:
        p1_line = json.loads(serialization_line.split(': ', 1)[1])
    except json.JSONDecodeError as exc:
        errors.append('P1 preview serialization JSON invalid: ' + exc.msg)
        return
    if not isinstance(p1_line, str):
        errors.append('P1 preview serialization must decode to a string')
        return
    parsed = parse_p1_line(p1_line)
    errors.extend('P1 preview contract: ' + item for item in parsed.errors)
    mismatches = compare_models(expected_model, parsed.model) if parsed.model is not None else []
    errors.extend(mismatches)
    if not parsed.errors and parsed.model is not None and not mismatches:
        info.append('P1 preview serialization reconstructs canonical P1L projection')


def validate_property(source_text: str, normalization_text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    info: list[str] = []

    data = collect_data(source_text)
    if data['base_id'] != 'BASE-ADPS-P1':
        errors.append('source BASE must be BASE-ADPS-P1')
    if data['normalize_target'] not in {'P1', 'P1L'}:
        errors.append('source NORMALIZE.target must be P1 or P1L')
    try:
        expected_model = build_model(source_text, data)
    except (ValueError, KeyError, TypeError) as exc:
        errors.append('expected P1L projection could not be built: ' + str(exc))
        return errors, info

    view = NormalizationCompatibilityView.from_text(normalization_text)
    parity_errors, _ = compare_normalization_legacy_v2(normalization_text)
    errors.extend('normalization parser parity: ' + item for item in parity_errors)
    if not view.present:
        errors.append('NORMALIZATION_DRAFT block not found')
        return errors, info

    values = view.values
    key_order = [key for key, _, _ in view.entries]
    if tuple(key_order) != REQUIRED_KEYS:
        errors.append('normalization required field order mismatch')
    if values.get('SCHEMA') != NORMALIZATION_SCHEMA:
        errors.append('normalization schema mismatch')
    if values.get('STATUS') != 'non-executable':
        errors.append('normalization status must be non-executable')

    source, source_duplicates = view.nested_scalars('SOURCE')
    if source_duplicates:
        errors.append('duplicate SOURCE fields: ' + ', '.join(source_duplicates))
    expected_digest = 'sha256:' + hashlib.sha256(source_text.encode('utf-8')).hexdigest()
    expected_source = {
        'schema': PACKET_SCHEMA,
        'digest': expected_digest,
        'packet_status': 'non-executable',
        'normalize_state': 'not_normalized',
    }
    for key, expected in expected_source.items():
        if source.get(key) != expected:
            errors.append(f'SOURCE.{key} mismatch')

    target, target_duplicates = view.nested_scalars('TARGET')
    if target_duplicates:
        errors.append('duplicate TARGET fields: ' + ', '.join(target_duplicates))
    kind = data['normalize_target']
    expected_target = {
        'kind': kind,
        'schema': P1L_SCHEMA_ID if kind == 'P1L' else P1_SCHEMA_ID,
        'resolution': 'resolved',
        'executable': 'false',
    }
    for key, expected in expected_target.items():
        if target.get(key) != expected:
            errors.append(f'TARGET.{key} mismatch')

    map_records = view.list_records('MAP')
    map_by_source: dict[str, dict[str, str]] = {}
    for record in map_records:
        source_name = record.get('source', '')
        if source_name in map_by_source:
            errors.append('duplicate MAP source: ' + source_name)
        map_by_source[source_name] = record
    missing_map = sorted(PACKET_SOURCE_FIELDS - set(map_by_source))
    extra_map = sorted(set(map_by_source) - PACKET_SOURCE_FIELDS)
    if missing_map:
        errors.append('MAP sources missing: ' + ', '.join(missing_map))
    if extra_map:
        errors.append('MAP sources unknown: ' + ', '.join(extra_map))
    for source_name in sorted(PACKET_SOURCE_FIELDS & set(map_by_source)):
        record = map_by_source[source_name]
        if record.get('target') != P1L_TARGETS[source_name]:
            errors.append('MAP target mismatch: ' + source_name)
        if record.get('mode') != MAP_MODES[source_name]:
            errors.append('MAP mode mismatch: ' + source_name)
        if not record.get('evidence', '').strip():
            errors.append('MAP evidence missing: ' + source_name)
    authority_evidence = map_by_source.get('AUTHORITY', {}).get('evidence', '')
    if 'public_repo/destructive_ops explicitly narrowed to forbid' not in authority_evidence:
        errors.append('AUTHORITY safety-floor mapping evidence missing')

    preserve = view.nested_lists('PRESERVE')
    expected_preserve = {
        'exact_strings': exact_strings(data),
        'protected_wording': protected_wording(expected_model),
        'ordered_fields': ordered_fields(data),
    }
    for key, expected in expected_preserve.items():
        actual = preserve.get(key, [])
        if actual != expected:
            errors.append('PRESERVE.' + key + ' missing or changed')

    unresolved = [] if values.get('UNRESOLVED') == '[]' else view.list_records('UNRESOLVED')
    loss = [] if values.get('LOSS') == '[]' else view.list_records('LOSS')
    if unresolved:
        errors.append('resolved P1L/P1 normalization must have UNRESOLVED:[]')
    if loss:
        errors.append('resolved P1L/P1 normalization must have LOSS:[]')

    round_trip, _ = view.nested_scalars('ROUND_TRIP')
    if round_trip != {
        'state': 'structural_pass',
        'structural_equivalence': 'pass',
        'semantic_equivalence': 'not_proven',
    }:
        errors.append('ROUND_TRIP boundary mismatch')

    authority, _ = view.nested_scalars('AUTHORITY')
    if authority != {'source_rails_preserved': 'true', 'execution_authority': 'none'}:
        errors.append('normalization AUTHORITY boundary mismatch')

    output, _ = view.nested_scalars('OUTPUT')
    if output.get('executable') != 'false':
        errors.append('OUTPUT.executable must be false')
    preview = view.multiline('OUTPUT', 'preview')
    if not preview:
        errors.append('resolved P1L/P1 normalization requires preview')
    else:
        validate_preview(kind, output.get('marker', ''), preview, expected_model, errors, info)

    model_authority = expected_model['AUTHORITY']
    for rail in ('read', 'edit', 'stage', 'commit', 'push', 'release'):
        if model_authority.get(rail) != data['authority'].get(rail):
            errors.append('source authority rail missing or widened: ' + rail)
    if model_authority.get('public_repo') != 'forbid':
        errors.append('public_repo safety floor must be forbid')
    if model_authority.get('destructive_ops') != 'forbid':
        errors.append('destructive_ops safety floor must be forbid')
    if expected_model['BINDING'] != {
        'runtime_control': 'unresolved',
        'state': 'unbound',
        'executable': False,
    }:
        errors.append('P1L binding boundary widened')

    if not errors:
        info.extend(
            [
                'all Packet fields accounted for',
                'six source authority rails preserved exactly',
                'public_repo/destructive_ops explicitly narrowed to forbid',
                'P1L/P1 preview remains non-executable',
                'Packet source remains not_normalized',
                'semantic equivalence remains not_proven',
                'NormalizationCompatibilityView structural path used',
            ]
        )
    return errors, info


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print('usage: python kdsl_packet_p1_property.py <packet-file> [normalization-file]')
        return 2
    source_path = argv[1]
    source_code, source_output = run_source_checker(source_path)
    if source_code >= 2:
        return emit('fail', ['source Packet semantic checker failed', source_output], [])

    source_text = load_text(source_path)
    if len(argv) == 3:
        normalization_text = load_text(argv[2])
    else:
        mapper_code, mapper_output = generate_normalization(source_path)
        if mapper_code != 0:
            return emit('fail', ['P1L/P1 mapper failed', mapper_output], [])
        normalization_text = mapper_output

    try:
        errors, info = validate_property(source_text, normalization_text)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return emit('fail', ['property evaluation failed: ' + str(exc)], [])
    return emit('property_pass' if not errors else 'fail', errors, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
