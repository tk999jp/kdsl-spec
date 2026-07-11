import json
import re
import sys
from pathlib import Path

SCHEMA_ID = 'kdsl-r1c@0.1-draft'
REQUIRED_KEYS = (
    'SCHEMA',
    'STATUS',
    'PHASE',
    'S',
    'FILES',
    'WHY',
    'CMD',
    'VERIFY',
    'RT',
    'RISK',
    'NEXT',
    'COMMIT',
)
OPTIONAL_KEYS = ('EVIDENCE', 'AUTHORITY', 'ANNUNCIATOR', 'SAFETY_GATES')
STATUS_VALUES = {'success', 'partial', 'blocked', 'noop', 'failed', 'needs_user'}
RT_VALUES = {'p', 'u', 'v', 'na', 'fail', 'blk'}
ALIASES = {'ST', 'PH', 'F', 'W', 'C', 'V', 'RK', 'NX', 'CM'}
PLACEHOLDER_VALUES = {'', '-', 'tbd', 'unknown', 'null'}


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


def extract_result_scope(text):
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == 'KDSL_RESULT:':
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
    pattern = re.compile(r'^\s*([A-Z][A-Z0-9_-]*)\s*:\s*(.*)$')
    for line_number, raw_line in enumerate(scope, start=1):
        match = pattern.match(raw_line)
        if not match:
            continue
        key = match.group(1)
        value = match.group(2).strip()
        if key == 'KDSL_RESULT':
            continue
        if key in seen:
            duplicates.append(key)
        seen.add(key)
        entries.append((key, value, line_number))
    return entries, duplicates


def parse_json_value(key, value, errors):
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        errors.append(f'{key} must be valid JSON-compatible value: {exc.msg}')
        return None


def require_string_array(key, value, errors):
    parsed = parse_json_value(key, value, errors)
    if parsed is None:
        return None
    if not isinstance(parsed, list):
        errors.append(f'{key} must be a JSON array')
        return None
    for index, item in enumerate(parsed):
        if not isinstance(item, str) or not item.strip():
            errors.append(f'{key}[{index}] must be a non-empty string')
    return parsed


def require_exact_object(key, value, required_subkeys, errors):
    parsed = parse_json_value(key, value, errors)
    if parsed is None:
        return None
    if not isinstance(parsed, dict):
        errors.append(f'{key} must be a JSON object')
        return None
    actual = set(parsed)
    required = set(required_subkeys)
    missing = sorted(required - actual)
    unknown = sorted(actual - required)
    for subkey in missing:
        errors.append(f'{key} required subkey missing: {subkey}')
    for subkey in unknown:
        errors.append(f'{key} unknown subkey: {subkey}')
    return parsed


def contains_runtime_risk(risks):
    return any(
        re.search(r'runtime[_ -]?unverified|runtime未確認|実機未確認|runtime確認未完了', item, re.IGNORECASE)
        for item in risks
    )


def validate_verify(value, errors, warnings):
    parsed = require_exact_object('VERIFY', value, ('pass', 'fail', 'not_run'), errors)
    if not isinstance(parsed, dict):
        return None
    classes = {}
    for key in ('pass', 'fail', 'not_run'):
        items = parsed.get(key)
        if not isinstance(items, list):
            errors.append(f'VERIFY.{key} must be a JSON array')
            classes[key] = []
            continue
        checked = []
        for index, item in enumerate(items):
            if not isinstance(item, str) or not item.strip():
                errors.append(f'VERIFY.{key}[{index}] must be a non-empty string')
            else:
                checked.append(item)
        classes[key] = checked

    normalized = {key: {item.strip().lower() for item in items} for key, items in classes.items()}
    for left, right in (('pass', 'fail'), ('pass', 'not_run'), ('fail', 'not_run')):
        overlap = sorted(normalized[left] & normalized[right])
        if overlap:
            errors.append(f'VERIFY contradiction between {left} and {right}: ' + ', '.join(overlap))

    for item in classes.get('pass', []):
        if re.search(r'not[_ -]?run|未実行|未確認', item, re.IGNORECASE):
            warnings.append('VERIFY.pass may contain unexecuted wording: ' + item)
    return classes


def validate_rt(value, risks, errors):
    parsed = require_exact_object('RT', value, ('state', 'basis'), errors)
    if not isinstance(parsed, dict):
        return None
    state = parsed.get('state')
    basis = parsed.get('basis')
    if state not in RT_VALUES:
        errors.append('RT.state unknown: ' + str(state))
    if not isinstance(basis, str) or not basis.strip():
        errors.append('RT.basis must be a non-empty string')
        basis = ''

    if state == 'v':
        runtime_marker = re.search(
            r'runtime|実機|target environment|target Windows|smoke|U観測|U実機|runtime log',
            basis,
            re.IGNORECASE,
        )
        static_only = re.search(r'build|diff|lint|unit test|tests? pass|CI|静的', basis, re.IGNORECASE)
        if not runtime_marker or (static_only and not runtime_marker):
            errors.append('RT:v basis lacks target runtime evidence')
    if state in {'p', 'u'} and not contains_runtime_risk(risks):
        errors.append('RT:p|u requires runtime_unverified-equivalent RISK entry')
    return parsed


def validate_next(value, errors):
    parsed = require_exact_object('NEXT', value, ('proposal', 'authority'), errors)
    if not isinstance(parsed, dict):
        return None
    proposal = parsed.get('proposal')
    authority = parsed.get('authority')
    if proposal is not None and (not isinstance(proposal, str) or not proposal.strip()):
        errors.append('NEXT.proposal must be a non-empty string or null')
    if authority != 'proposal_only':
        errors.append('NEXT.authority must be proposal_only')
    return parsed


def validate_commit(value, errors, warnings):
    parsed = require_exact_object('COMMIT', value, ('actual', 'proposed', 'permission_basis'), errors)
    if not isinstance(parsed, dict):
        return None
    actual = parsed.get('actual')
    proposed = parsed.get('proposed')
    permission_basis = parsed.get('permission_basis')
    for subkey, item in (('actual', actual), ('proposed', proposed)):
        if item is not None and (not isinstance(item, str) or not item.strip()):
            errors.append(f'COMMIT.{subkey} must be a non-empty string or null')
    if not isinstance(permission_basis, str) or not permission_basis.strip():
        errors.append('COMMIT.permission_basis must be a non-empty string')
    if actual is not None and proposed is not None and actual == proposed:
        errors.append('COMMIT.actual and COMMIT.proposed must not be identical')
    if actual is not None and permission_basis == 'none':
        warnings.append('COMMIT.actual is present while permission_basis is none')
    if isinstance(permission_basis, str) and re.search(r'automatic|auto[_ -]?commit|自動', permission_basis, re.IGNORECASE):
        errors.append('COMMIT.permission_basis must not imply automatic commit authority')
    return parsed


def validate_optional_json(key, value, errors):
    parsed = parse_json_value(key, value, errors)
    if parsed is not None and not isinstance(parsed, dict):
        errors.append(f'{key} must be a JSON object when present')


def main(argv):
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    scope = extract_result_scope(text)

    errors = []
    warnings = []
    info = []

    if scope is None:
        info.append('no KDSL_RESULT block detected; R1C target not applicable')
        return emit(errors, warnings, info)

    entries, duplicates = parse_top_level(scope)
    values = {key: value for key, value, _ in entries}

    schema = values.get('SCHEMA')
    if schema is None:
        info.append('KDSL_RESULT has no R1C SCHEMA marker; Full R1 fallback/out-of-scope')
        return emit(errors, warnings, info)
    if schema != SCHEMA_ID:
        errors.append('unknown R1C schema: ' + schema)
        return emit(errors, warnings, info)

    if re.search(r'^\s*R1C\s*:', text, re.MULTILINE):
        errors.append('R1C top-level envelope is prohibited; use KDSL_RESULT')

    for key in duplicates:
        errors.append('duplicate R1C field: ' + key)

    key_order = [key for key, _, _ in entries if key in REQUIRED_KEYS or key in OPTIONAL_KEYS or key in ALIASES]
    for alias in sorted(ALIASES & set(key_order)):
        errors.append('R1C short field alias is not defined: ' + alias)

    required_present = [key for key in key_order if key in REQUIRED_KEYS]
    for key in REQUIRED_KEYS:
        if key not in values:
            errors.append('required R1C field missing: ' + key)

    if required_present and required_present != list(REQUIRED_KEYS[: len(required_present)]):
        errors.append('R1C required field order mismatch')
    elif all(key in values for key in REQUIRED_KEYS):
        exact_positions = [key_order.index(key) for key in REQUIRED_KEYS]
        if exact_positions != sorted(exact_positions):
            errors.append('R1C required field order mismatch')

    for key in ('STATUS', 'PHASE', 'S', 'WHY'):
        value = values.get(key)
        if value is not None and value.strip().lower() in PLACEHOLDER_VALUES:
            errors.append(f'{key} must be a non-placeholder scalar')

    status = values.get('STATUS')
    if status is not None and status not in STATUS_VALUES:
        errors.append('unknown R1C STATUS: ' + status)

    files = require_string_array('FILES', values['FILES'], errors) if 'FILES' in values else []
    commands = require_string_array('CMD', values['CMD'], errors) if 'CMD' in values else []
    risks = require_string_array('RISK', values['RISK'], errors) if 'RISK' in values else []
    verify = validate_verify(values['VERIFY'], errors, warnings) if 'VERIFY' in values else None
    rt = validate_rt(values['RT'], risks or [], errors) if 'RT' in values else None
    next_value = validate_next(values['NEXT'], errors) if 'NEXT' in values else None
    commit = validate_commit(values['COMMIT'], errors, warnings) if 'COMMIT' in values else None

    for key in OPTIONAL_KEYS:
        if key in values and key != 'SAFETY_GATES':
            validate_optional_json(key, values[key], errors)

    if 'PKT:v1' in text:
        errors.append('PKT:v1 is prohibited while Packet schema/registries are undefined')

    if status in {'partial', 'blocked', 'failed', 'needs_user'} and risks == []:
        warnings.append('non-success STATUS has empty RISK array')

    info.append('R1C schema checked: ' + SCHEMA_ID)
    info.append('required fields checked: ' + ', '.join(REQUIRED_KEYS[1:]))
    info.append('structured JSON fields checked')
    if files is not None:
        info.append('FILES entries: ' + str(len(files)))
    if commands is not None:
        info.append('CMD entries: ' + str(len(commands)))
    if verify is not None:
        info.append('VERIFY classes checked')
    if rt is not None:
        info.append('RT state checked: ' + str(rt.get('state')))
    if next_value is not None:
        info.append('NEXT proposal_only boundary checked')
    if commit is not None:
        info.append('COMMIT actual/proposed boundary checked')

    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
