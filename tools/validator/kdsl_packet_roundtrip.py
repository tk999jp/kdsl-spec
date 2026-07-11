import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from kdsl_packet_normalization import (
    blocks_from_entries as normalization_blocks,
    extract_multiline,
    extract_scope as extract_normalization_scope,
    parse_list_records,
    parse_nested_lists,
    parse_nested_scalars as parse_normalization_scalars,
    parse_top_level as parse_normalization_top_level,
)
from kdsl_packet_normalize import PACKET_FIELDS, collect_data, load_text, unique


ROUND_TRIP_MARKER = 'STRUCTURAL_ROUND_TRIP_RESULT:'
FORBIDDEN_EXECUTABLE_MARKERS = re.compile(r'^\s*(?:KDSL_PROMPT|P1|P1L)\s*:', re.MULTILINE)
AUTHORITY_RAILS = ('read', 'edit', 'stage', 'commit', 'push', 'release')


def emit(status, checks, errors, info):
    print(ROUND_TRIP_MARKER)
    print('STATUS: ' + status)
    print('EXECUTABLE: no')
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    print('CHECKS:')
    for item in checks or ['none']:
        print('  - ' + item)
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in info or ['none']:
        print('  - ' + item)
    if errors:
        return 2
    return 1 if status == 'blocked' else 0


def run_mapper(source_path):
    mapper = Path(__file__).with_name('kdsl_packet_normalize.py')
    return subprocess.run(
        [sys.executable, str(mapper), source_path],
        text=True,
        capture_output=True,
    )


def run_normalization_checker(text):
    checker = Path(__file__).with_name('kdsl_packet_normalization.py')
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            suffix='.md',
            delete=False,
        ) as handle:
            handle.write(text)
            temp_path = handle.name
        return subprocess.run(
            [sys.executable, str(checker), temp_path],
            text=True,
            capture_output=True,
        )
    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)


def parse_normalization(text):
    scope = extract_normalization_scope(text)
    if scope is None:
        raise ValueError('NORMALIZATION_DRAFT block not found')
    entries, _ = parse_normalization_top_level(scope)
    values = {key: value for key, value, _ in entries}
    blocks = normalization_blocks(scope, entries)
    source, _ = parse_normalization_scalars(blocks.get('SOURCE', {}))
    target, _ = parse_normalization_scalars(blocks.get('TARGET', {}))
    round_trip, _ = parse_normalization_scalars(blocks.get('ROUND_TRIP', {}))
    authority, _ = parse_normalization_scalars(blocks.get('AUTHORITY', {}))
    output, _ = parse_normalization_scalars(blocks.get('OUTPUT', {}))
    return {
        'values': values,
        'source': source,
        'target': target,
        'map_records': parse_list_records(blocks.get('MAP', {})),
        'preserve': parse_nested_lists(blocks.get('PRESERVE', {})),
        'unresolved': parse_list_records(blocks.get('UNRESOLVED', {})),
        'loss': parse_list_records(blocks.get('LOSS', {})),
        'round_trip': round_trip,
        'authority': authority,
        'output': output,
        'preview': extract_multiline(blocks.get('OUTPUT', {}), 'preview'),
    }


def ordered_in_text(values, text):
    position = -1
    for value in values:
        found = text.find(value, position + 1)
        if found < 0:
            return False
        position = found
    return True


def expected_properties(data):
    exact_strings = unique(
        data['src'] + data['read'] + data['tgt'] + data['verify'] + [data['result_schema']]
    )
    source_protected = unique(
        data['non'] + data['stop'] + [record.get('reason', '') for record in data['sg_records']]
    )
    protected_wording = unique(
        source_protected + ['KDSL_PROMPT_PREVIEW != KDSL_PROMPT', 'execution_authority:none']
    )
    flow_ops = [record.get('op', '') for record in data['flow_records'] if record.get('op')]
    flow_order = '>'.join(flow_ops)
    ordered_fields = unique(
        [flow_order]
        + (['STOP: ' + ' > '.join(data['stop'])] if data['stop'] else [])
        + (['VERIFY: ' + ' > '.join(data['verify'])] if data['verify'] else [])
    )
    return {
        'exact_strings': exact_strings,
        'source_protected': source_protected,
        'protected_wording': protected_wording,
        'flow_ops': flow_ops,
        'ordered_fields': ordered_fields,
    }


def compare(source_text, data, normalization_text, normalized):
    checks = []
    errors = []
    info = []

    digest = 'sha256:' + hashlib.sha256(source_text.encode('utf-8')).hexdigest()
    if normalized['source'].get('digest') == digest:
        checks.append('source digest matches')
    else:
        errors.append('source digest mismatch')

    if normalized['source'].get('normalize_state') == 'not_normalized':
        checks.append('source normalize_state remains not_normalized')
    else:
        errors.append('source normalize_state changed')

    if normalized['authority'].get('execution_authority') == 'none':
        checks.append('execution authority remains none')
    else:
        errors.append('execution authority widened')

    if normalized['round_trip'].get('semantic_equivalence') == 'not_proven':
        checks.append('semantic equivalence remains not_proven')
    else:
        errors.append('semantic equivalence claim is prohibited')

    if normalized['target'].get('executable') == 'false' and normalized['output'].get('executable') == 'false':
        checks.append('target and output remain non-executable')
    else:
        errors.append('target/output executable boundary violated')

    if FORBIDDEN_EXECUTABLE_MARKERS.search(normalization_text):
        errors.append('executable KDSL_PROMPT/P1/P1L marker detected')
    else:
        checks.append('no executable target marker')

    expected = expected_properties(data)
    mapped = {record.get('source', '') for record in normalized['map_records']}
    missing_map = sorted(set(PACKET_FIELDS) - mapped)
    if missing_map:
        errors.append('Packet fields missing from MAP: ' + ', '.join(missing_map))
    else:
        checks.append('all Packet fields accounted in MAP')

    exact_values = normalized['preserve'].get('exact_strings', [])
    missing_exact = [value for value in expected['exact_strings'] if value not in exact_values]
    if missing_exact:
        errors.append('exact strings missing from PRESERVE: ' + ' | '.join(missing_exact))
    else:
        checks.append('exact strings preserved')

    protected_values = normalized['preserve'].get('protected_wording', [])
    missing_protected = [value for value in expected['protected_wording'] if value not in protected_values]
    if missing_protected:
        errors.append('protected wording missing from PRESERVE: ' + ' | '.join(missing_protected))
    else:
        checks.append('protected wording preserved')

    ordered_values = normalized['preserve'].get('ordered_fields', [])
    missing_order = [value for value in expected['ordered_fields'] if value not in ordered_values]
    if missing_order:
        errors.append('ordered fields missing or changed: ' + ' | '.join(missing_order))
    else:
        checks.append('FLOW/STOP/VERIFY order preserved')

    resolution = normalized['target'].get('resolution')
    kind = normalized['target'].get('kind')
    marker = normalized['output'].get('marker')
    preview = normalized['preview']

    if resolution == 'blocked':
        if kind not in {'P1', 'P1L'}:
            errors.append('blocked target kind is not P1/P1L')
        if normalized['target'].get('schema') != 'unresolved':
            errors.append('blocked P1/P1L target schema must remain unresolved')
        if marker != 'none' or preview.strip():
            errors.append('blocked target must not contain preview output')
        if not normalized['unresolved']:
            errors.append('blocked target requires unresolved evidence')
        if not errors:
            checks.append('P1/P1L unresolved target remains blocked')
            info.append('structural comparison stopped at unresolved target schema')
            return 'blocked', checks, errors, info
        return 'fail', checks, errors, info

    if kind != 'full-kdsl-dev-prompt':
        errors.append('first-slice structural pass supports full-kdsl-dev-prompt only')
        return 'fail', checks, errors, info

    if marker != 'KDSL_PROMPT_PREVIEW' or not preview.strip():
        errors.append('resolved Full KDSL target requires KDSL_PROMPT_PREVIEW')
    else:
        checks.append('Full KDSL preview marker preserved')

    missing_preview_exact = [value for value in expected['exact_strings'] if value not in preview]
    if missing_preview_exact:
        errors.append('exact strings missing from Full KDSL preview: ' + ' | '.join(missing_preview_exact))
    else:
        checks.append('exact strings represented in Full KDSL preview')

    missing_preview_protected = [value for value in expected['source_protected'] if value not in preview]
    if missing_preview_protected:
        errors.append('source protected wording missing from preview: ' + ' | '.join(missing_preview_protected))
    else:
        checks.append('source protected wording represented in preview')

    if expected['flow_ops'] and ordered_in_text(expected['flow_ops'], preview):
        checks.append('FLOW order represented in preview')
    elif expected['flow_ops']:
        errors.append('FLOW order changed in preview')

    for rail in AUTHORITY_RAILS:
        expected_line = f'- {rail}: {data["authority"].get(rail, "unknown")}'
        if expected_line not in preview:
            errors.append('authority rail missing or widened in preview: ' + rail)
    if not any(error.startswith('authority rail') for error in errors):
        checks.append('authority rails preserved in preview')

    if data['result_schema'] in preview:
        checks.append('result schema preserved in preview')
    else:
        errors.append('result schema missing from preview')

    return ('fail' if errors else 'structural_pass'), checks, errors, info


def main(argv):
    if len(argv) not in {2, 3}:
        print('usage: python kdsl_packet_roundtrip.py <packet-file> [normalization-file]', file=sys.stderr)
        return 2

    source_path = argv[1]
    try:
        source_text = load_text(source_path)
        data = collect_data(source_text)
    except (OSError, ValueError) as exc:
        return emit('fail', [], ['source Packet parse failed: ' + str(exc)], [])

    if len(argv) == 3:
        try:
            normalization_text = load_text(argv[2])
        except OSError as exc:
            return emit('fail', [], ['normalization artifact read failed: ' + str(exc)], [])
        mapper_code = None
    else:
        mapper = run_mapper(source_path)
        mapper_code = mapper.returncode
        if mapper.returncode >= 2:
            details = mapper.stderr.strip() or mapper.stdout.strip() or 'mapper failed'
            return emit('fail', [], ['mapper rejected source Packet: ' + details], [])
        normalization_text = mapper.stdout

    checker = run_normalization_checker(normalization_text)
    if checker.returncode != 0:
        details = checker.stdout.strip() or checker.stderr.strip() or 'normalization checker failed'
        return emit('fail', [], ['normalization artifact failed checker: ' + details], [])

    try:
        normalized = parse_normalization(normalization_text)
    except ValueError as exc:
        return emit('fail', [], ['normalization parse failed: ' + str(exc)], [])

    status, checks, errors, info = compare(source_text, data, normalization_text, normalized)
    if mapper_code == 1 and status != 'blocked':
        errors.append('mapper returned blocked exit without blocked round-trip state')
        status = 'fail'
    elif mapper_code == 0 and status == 'blocked':
        errors.append('mapper returned success for blocked round-trip state')
        status = 'fail'

    return emit(status, checks, errors, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
