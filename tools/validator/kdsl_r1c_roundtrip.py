import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from kdsl_r1c import OPTIONAL_KEYS, REQUIRED_KEYS, SCHEMA_ID, extract_result_scope, parse_top_level

ROOT = Path(__file__).resolve().parent
STRUCTURED_KEYS = {'FILES', 'CMD', 'VERIFY', 'RT', 'RISK', 'NEXT', 'COMMIT'}
JSON_OPTIONAL_KEYS = {'EVIDENCE', 'AUTHORITY', 'ANNUNCIATOR'}
UNSUPPORTED_OPTIONAL_KEYS = {'SAFETY_GATES'}


def load_text(path):
    return Path(path).read_text(encoding='utf-8')


def source_digest(text):
    scope = extract_result_scope(text)
    if scope is None:
        return None
    normalized = '\n'.join(scope).rstrip() + '\n'
    return 'sha256:' + hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def parse_model(text):
    scope = extract_result_scope(text)
    if scope is None:
        raise ValueError('no KDSL_RESULT block detected')
    entries, duplicates = parse_top_level(scope)
    if duplicates:
        raise ValueError('duplicate fields: ' + ', '.join(duplicates))

    values = {key: value for key, value, _ in entries}
    if values.get('SCHEMA') != SCHEMA_ID:
        raise ValueError('source is not kdsl-r1c@0.1-draft')

    required_order = [key for key, _, _ in entries if key in REQUIRED_KEYS]
    optional_order = [key for key, _, _ in entries if key in OPTIONAL_KEYS]
    model = {
        'schema': values['SCHEMA'],
        'required_order': required_order,
        'optional_order': optional_order,
        'required': {},
        'optional': {},
    }

    for key in REQUIRED_KEYS[1:]:
        value = values[key]
        if key in STRUCTURED_KEYS:
            model['required'][key] = json.loads(value)
        else:
            model['required'][key] = value

    for key in optional_order:
        if key in UNSUPPORTED_OPTIONAL_KEYS:
            model['optional'][key] = {'_unsupported_raw': values.get(key, '')}
        elif key in JSON_OPTIONAL_KEYS:
            model['optional'][key] = json.loads(values[key])
        else:
            model['optional'][key] = values[key]
    return model


def project_to_full_r1(model):
    return {
        'source_schema': model['schema'],
        'field_order': list(REQUIRED_KEYS[1:]),
        'fields': [(key, copy.deepcopy(model['required'][key])) for key in REQUIRED_KEYS[1:]],
        'optional_order': list(model['optional_order']),
        'optional': [(key, copy.deepcopy(model['optional'][key])) for key in model['optional_order']],
        'semantic_equivalence': 'not_proven',
        'execution_authority': 'none',
    }


def reconstruct_r1c(projection):
    required = {key: copy.deepcopy(value) for key, value in projection['fields']}
    optional = {key: copy.deepcopy(value) for key, value in projection['optional']}
    return {
        'schema': projection['source_schema'],
        'required_order': ['SCHEMA'] + list(projection['field_order']),
        'optional_order': list(projection['optional_order']),
        'required': required,
        'optional': optional,
    }


def compare_models(source, reconstructed):
    mismatches = []
    if reconstructed.get('schema') != source.get('schema'):
        mismatches.append('schema changed')

    expected_order = list(REQUIRED_KEYS)
    if reconstructed.get('required_order') != expected_order:
        mismatches.append('required field order changed')
    if source.get('required_order') != expected_order:
        mismatches.append('source required field order is not canonical')

    for key in REQUIRED_KEYS[1:]:
        if key not in reconstructed.get('required', {}):
            mismatches.append('required field missing after reconstruction: ' + key)
        elif reconstructed['required'][key] != source['required'][key]:
            mismatches.append('required field changed: ' + key)

    if reconstructed.get('optional_order') != source.get('optional_order'):
        mismatches.append('optional field order changed')

    source_optional = source.get('optional', {})
    reconstructed_optional = reconstructed.get('optional', {})
    if set(source_optional) != set(reconstructed_optional):
        mismatches.append('optional field set changed')
    for key in source_optional:
        if reconstructed_optional.get(key) != source_optional[key]:
            mismatches.append('optional field changed: ' + key)

    return mismatches


def validate_source(path):
    result = subprocess.run(
        [sys.executable, str(ROOT / 'kdsl_r1c.py'), str(path)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def emit(status, digest, checks, errors=None, warnings=None):
    errors = errors or []
    warnings = warnings or []
    print('R1C_STRUCTURAL_ROUND_TRIP_RESULT:')
    print('STATUS: ' + status)
    print('SOURCE_SCHEMA: ' + SCHEMA_ID)
    print('SOURCE_DIGEST: ' + str(digest))
    print('EXECUTABLE: no')
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    print('CHECKS:')
    for check in checks or ['none']:
        print('  - ' + check)
    print('ERRORS:')
    for item in errors or ['none']:
        print('  - ' + item)
    print('WARNINGS:')
    for item in warnings or ['none']:
        print('  - ' + item)
    if status == 'structural_pass':
        return 0
    if status == 'blocked':
        return 1
    return 2


def main(argv):
    if len(argv) != 2:
        print('usage: python kdsl_r1c_roundtrip.py <r1c-file>')
        return 2

    path = Path(argv[1])
    validator_code, validator_stdout, validator_stderr = validate_source(path)
    if validator_code == 2:
        return emit(
            'fail',
            None,
            ['source validator failed'],
            errors=['source R1C failed validator', validator_stdout.strip() or validator_stderr.strip()],
        )

    text = load_text(path)
    digest = source_digest(text)
    try:
        model = parse_model(text)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        return emit('fail', digest, ['source parse failed'], errors=[str(exc)])

    if any(key in model['optional'] for key in UNSUPPORTED_OPTIONAL_KEYS):
        return emit(
            'blocked',
            digest,
            ['required field model parsed', 'optional SAFETY_GATES requires dedicated expansion'],
            warnings=['first slice does not claim safe SAFETY_GATES round-trip'],
        )

    projection = project_to_full_r1(model)
    reconstructed = reconstruct_r1c(projection)
    mismatches = compare_models(model, reconstructed)
    if mismatches:
        return emit('fail', digest, ['projection generated', 'reconstruction compared'], errors=mismatches)

    warnings = []
    if validator_code == 1:
        warnings.append('source validator returned warning')
    return emit(
        'structural_pass',
        digest,
        [
            'canonical required field order preserved',
            'scalar fields preserved exactly',
            'FILES/CMD/RISK order preserved',
            'VERIFY classes preserved',
            'RT state/basis preserved',
            'NEXT proposal_only boundary preserved',
            'COMMIT actual/proposed/permission_basis preserved',
            'optional JSON blocks preserved',
        ],
        warnings=warnings,
    )


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
