from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from kdsl_packet_normalize import PACKET_FIELDS, collect_data, load_text, unique
from kdsl_packet_normalize_semantic import exact_strings, ordered_fields, protected_wording
from kdsl_packet_roundtrip import (
    AUTHORITY_RAILS,
    FORBIDDEN_EXECUTABLE_MARKERS,
    ordered_in_text,
    parse_normalization,
)
from kdsl_safety_semantics import check_semantics

MODEL_ID = 'kdsl-packet-property@0.1-draft'
EXPECTED_RESOLVED_MODES = {
    'SCHEMA': 'exact',
    'STATUS': 'exact',
    'BASE': 'structured',
    'TASK': 'structured',
    'SRC': 'exact',
    'READ': 'exact',
    'TGT': 'exact',
    'OBS': 'exact',
    'GOAL': 'exact',
    'NON': 'exact',
    'SG': 'expanded',
    'STOP': 'exact',
    'FLOW': 'expanded',
    'VERIFY': 'exact',
    'OUT': 'structured',
    'AUTHORITY': 'exact',
    'NORMALIZE': 'exact',
}


def emit(status: str, checks: list[str], errors: list[str], warnings: list[str], info: list[str]) -> int:
    print('PACKET_PROPERTY_RESULT:')
    print('STATUS: ' + status)
    print('MODEL: ' + MODEL_ID)
    print('EXECUTABLE: no')
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('FULL_SAFETY_PROOF: not_proven')
    print('EXECUTION_AUTHORITY: none')
    print('CHECKS:')
    for item in checks or ['none']:
        print('  - ' + item)
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('WARNINGS:')
    for item in warnings or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    if errors:
        return 2
    return 1 if status == 'blocked' or warnings else 0


def run_script(script: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(Path(__file__).with_name(script)), *args],
        text=True,
        capture_output=True,
    )


def run_normalization_checker(text: str) -> subprocess.CompletedProcess[str]:
    temp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.md', delete=False) as handle:
            handle.write(text)
            temp_path = handle.name
        return run_script('kdsl_packet_normalization.py', [temp_path])
    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)


def map_index(records: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], list[str]]:
    result: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for record in records:
        source = record.get('source', '')
        if source in result:
            duplicates.append(source)
        result[source] = record
    return result, duplicates


def check_map(normalized: dict, resolution: str) -> tuple[list[str], list[str]]:
    checks: list[str] = []
    errors: list[str] = []
    indexed, duplicates = map_index(normalized['map_records'])
    if duplicates:
        errors.append('duplicate MAP source entries: ' + ', '.join(sorted(set(duplicates))))
    missing = [field for field in PACKET_FIELDS if field not in indexed]
    unknown = sorted(set(indexed) - set(PACKET_FIELDS))
    if missing:
        errors.append('MAP missing Packet fields: ' + ', '.join(missing))
    if unknown:
        errors.append('MAP contains unknown Packet fields: ' + ', '.join(unknown))
    if not missing and not unknown and not duplicates:
        checks.append('all 17 Packet fields mapped exactly once')

    if resolution == 'resolved':
        for field, expected_mode in EXPECTED_RESOLVED_MODES.items():
            actual = indexed.get(field, {}).get('mode')
            if actual != expected_mode:
                errors.append(f'MAP mode mismatch: {field} expected {expected_mode} actual {actual}')
        if not any(error.startswith('MAP mode mismatch') for error in errors):
            checks.append('resolved MAP modes match adopted reconstruction policy')
    else:
        for field in PACKET_FIELDS:
            actual = indexed.get(field, {}).get('mode')
            if actual != 'blocked':
                errors.append(f'blocked target MAP mode must be blocked: {field}')
        if not any(error.startswith('blocked target MAP mode') for error in errors):
            checks.append('blocked target MAP remains blocked for all fields')
    return checks, errors


def gate_line(record: dict[str, str]) -> str:
    return '- ' + ' / '.join(
        [
            'id=' + record.get('id', 'unknown'),
            'state=' + record.get('state', 'unknown'),
            'scope=' + record.get('scope', 'unknown'),
            'reason=' + record.get('reason', 'unknown'),
            'evidence=' + record.get('evidence', 'none'),
            'authority=' + record.get('authority', 'none'),
        ]
    )


def check_preview(data: dict, normalized: dict) -> tuple[list[str], list[str], list[str]]:
    checks: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []
    preview = normalized['preview']

    if normalized['output'].get('marker') != 'KDSL_PROMPT_PREVIEW' or not preview.strip():
        errors.append('resolved Full KDSL target requires non-empty KDSL_PROMPT_PREVIEW')
        return checks, errors, warnings
    if FORBIDDEN_EXECUTABLE_MARKERS.search(preview):
        errors.append('preview contains executable KDSL_PROMPT/P1/P1L marker')
    else:
        checks.append('preview marker remains non-executable')

    missing_exact = [value for value in exact_strings(data) if value not in preview]
    if missing_exact:
        errors.append('exact source strings missing from preview: ' + ' | '.join(missing_exact))
    else:
        checks.append('all selected exact source strings represented in preview')

    for record in data['sg_records']:
        expected = gate_line(record)
        if expected not in preview:
            errors.append('Safety Gate record not exactly represented in preview: ' + record.get('id', 'unknown'))
    if not any(error.startswith('Safety Gate record') for error in errors):
        checks.append('Safety Gate state/scope/reason/evidence/authority preserved')

    flow_values: list[str] = []
    for record in data['flow_records']:
        flow_values.extend([record.get('op', ''), record.get('detail', '')])
    if flow_values and not ordered_in_text([value for value in flow_values if value], preview):
        errors.append('FLOW opcode/detail order changed in preview')
    elif flow_values:
        checks.append('FLOW opcode/detail order preserved')

    if data['stop'] and not ordered_in_text(data['stop'], preview):
        errors.append('STOP order changed in preview')
    elif data['stop']:
        checks.append('STOP order preserved')
    if data['verify'] and not ordered_in_text(data['verify'], preview):
        errors.append('VERIFY order changed in preview')
    elif data['verify']:
        checks.append('VERIFY requirement order preserved')

    for rail in AUTHORITY_RAILS:
        expected = '- ' + rail + ': ' + data['authority'].get(rail, 'unknown')
        if expected not in preview:
            errors.append('authority rail missing or widened in preview: ' + rail)
    if not any(error.startswith('authority rail') for error in errors):
        checks.append('all six authority rails preserved')

    gate_ids = [record.get('id', '') for record in data['sg_records'] if record.get('id')]
    semantic_errors, semantic_warnings, _, _ = check_semantics(preview, gate_ids)
    errors.extend('preview ' + item for item in semantic_errors)
    warnings.extend('preview ' + item for item in semantic_warnings)
    if not semantic_errors:
        checks.append('bounded protected-language concepts preserved in preview')

    for line in preview.splitlines():
        lowered = line.lower()
        if any(marker in line for marker in ('禁止', '未確認', '未実行', '!=')):
            continue
        if re.search(r'\b(?:success|completed|executed|verified)\b|成功|実行済|確認済|完了', lowered, re.IGNORECASE):
            if line.strip() not in load_text.__doc__ if False else False:
                pass
            source_candidates = exact_strings(data)
            if not any(candidate and candidate in line for candidate in source_candidates):
                errors.append('preview appears to invent completion/verification claim: ' + line.strip())
    if not any(error.startswith('preview appears to invent') for error in errors):
        checks.append('no invented completion/verification claim detected')

    if data['result_schema'] not in preview:
        errors.append('result schema missing from preview')
    else:
        checks.append('result schema request preserved')
    return checks, errors, warnings


def compare(source_text: str, data: dict, normalization_text: str, normalized: dict) -> tuple[str, list[str], list[str], list[str], list[str]]:
    checks: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    digest = 'sha256:' + hashlib.sha256(source_text.encode('utf-8')).hexdigest()
    if normalized['source'].get('digest') != digest:
        errors.append('source digest mismatch')
    else:
        checks.append('source digest matches exact Packet text')

    if normalized['source'].get('normalize_state') != 'not_normalized':
        errors.append('source normalize_state must remain not_normalized')
    if normalized['authority'].get('execution_authority') != 'none':
        errors.append('normalization execution authority widened')
    if normalized['round_trip'].get('semantic_equivalence') != 'not_proven':
        errors.append('semantic equivalence claim is prohibited')
    if normalized['target'].get('executable') != 'false' or normalized['output'].get('executable') != 'false':
        errors.append('target/output executable boundary violated')
    if not any('authority' in error or 'executable' in error or 'semantic equivalence' in error for error in errors):
        checks.append('non-executable/non-authority/non-equivalence boundary preserved')

    resolution = normalized['target'].get('resolution', '')
    map_checks, map_errors = check_map(normalized, resolution)
    checks.extend(map_checks)
    errors.extend(map_errors)

    preserve = normalized['preserve']
    expected_exact = exact_strings(data)
    missing_exact = [value for value in expected_exact if value not in preserve.get('exact_strings', [])]
    if missing_exact:
        errors.append('PRESERVE.exact_strings missing: ' + ' | '.join(missing_exact))
    else:
        checks.append('PRESERVE exact strings complete')

    expected_protected = protected_wording(data)
    missing_protected = [value for value in expected_protected if value not in preserve.get('protected_wording', [])]
    if missing_protected:
        errors.append('PRESERVE.protected_wording missing: ' + ' | '.join(missing_protected))
    else:
        checks.append('PRESERVE protected wording complete')

    expected_order = ordered_fields(data)
    missing_order = [value for value in expected_order if value not in preserve.get('ordered_fields', [])]
    if missing_order:
        errors.append('PRESERVE.ordered_fields missing or changed: ' + ' | '.join(missing_order))
    else:
        checks.append('PRESERVE ordered fields complete')

    critical_loss = any(record.get('class') == 'critical' for record in normalized['loss'])
    blocked_unresolved = any(record.get('impact') == 'blocked' for record in normalized['unresolved'])
    if resolution == 'resolved':
        if critical_loss:
            errors.append('resolved target contains critical LOSS')
        if blocked_unresolved:
            errors.append('resolved target contains blocked UNRESOLVED item')
        preview_checks, preview_errors, preview_warnings = check_preview(data, normalized)
        checks.extend(preview_checks)
        errors.extend(preview_errors)
        warnings.extend(preview_warnings)
    else:
        if normalized['target'].get('kind') not in {'P1', 'P1L'}:
            errors.append('blocked target kind must be P1/P1L')
        if normalized['target'].get('schema') != 'unresolved':
            errors.append('blocked P1/P1L target schema must remain unresolved')
        if normalized['output'].get('marker') != 'none' or normalized['preview'].strip():
            errors.append('blocked target must not emit preview')
        if not blocked_unresolved:
            errors.append('blocked target requires blocked UNRESOLVED evidence')
        if not errors:
            checks.append('P1/P1L remains blocked without canonical target schema')
            info.append('property comparison stopped at unresolved target schema')
            return 'blocked', checks, errors, warnings, info

    return ('fail' if errors else 'property_pass'), checks, errors, warnings, info


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print('usage: python kdsl_packet_property.py <packet-file> [normalization-file]', file=sys.stderr)
        return 2
    source_path = argv[1]
    source_semantic = run_script('kdsl_packet_semantic.py', [source_path])
    if source_semantic.returncode >= 2:
        details = source_semantic.stdout.strip() or source_semantic.stderr.strip()
        return emit('fail', [], ['source Packet failed semantic checker: ' + details], [], [])

    try:
        source_text = load_text(source_path)
        data = collect_data(source_text)
    except (OSError, ValueError) as exc:
        return emit('fail', [], ['source Packet parse failed: ' + str(exc)], [], [])

    if len(argv) == 3:
        try:
            normalization_text = load_text(argv[2])
        except OSError as exc:
            return emit('fail', [], ['normalization artifact read failed: ' + str(exc)], [], [])
        mapper_code = None
    else:
        mapper = run_script('kdsl_packet_normalize_semantic.py', [source_path])
        mapper_code = mapper.returncode
        if mapper.returncode >= 2:
            details = mapper.stderr.strip() or mapper.stdout.strip()
            return emit('fail', [], ['strict mapper rejected source Packet: ' + details], [], [])
        normalization_text = mapper.stdout

    checker = run_normalization_checker(normalization_text)
    if checker.returncode != 0:
        details = checker.stdout.strip() or checker.stderr.strip()
        return emit('fail', [], ['normalization artifact failed base checker: ' + details], [], [])

    try:
        normalized = parse_normalization(normalization_text)
    except ValueError as exc:
        return emit('fail', [], ['normalization parse failed: ' + str(exc)], [], [])

    status, checks, errors, warnings, info = compare(source_text, data, normalization_text, normalized)
    if source_semantic.returncode == 1:
        warnings.append('source semantic checker returned warning')
    if mapper_code == 1 and status != 'blocked':
        errors.append('strict mapper returned blocked exit without blocked property state')
        status = 'fail'
    elif mapper_code == 0 and status == 'blocked':
        errors.append('strict mapper returned success for blocked property state')
        status = 'fail'
    return emit(status, checks, errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
