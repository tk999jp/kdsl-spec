from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from kdsl_parser_v2_safety_gate_compat import SafetyGateCompatibilityView
from kdsl_r1c import SCHEMA_ID, extract_result_scope, parse_top_level
from kdsl_safety_gate import (
    KNOWN_IDS,
    KNOWN_STATES,
    REGISTRY,
    REQUIRED_FIELDS,
    authority_is_unverified,
    is_blank,
)

EVIDENCE_KEYS = ('observed', 'inferred', 'not_observed', 'unverified')
AUTHORITY_KEYS = ('read', 'edit', 'stage', 'commit', 'push', 'release')
AUTHORITY_VALUES = {
    'allow',
    'forbid',
    'target_only',
    'allow_once',
    'propose_only',
    'not_requested',
    'not_applicable',
}
ANNUNCIATOR_KEYS = {'STATUS', 'PHASE', 'AUTHORITY', 'RT', 'PUBLIC_OPS', 'DESTRUCTIVE_OPS'}
SAFETY_ENTRY_FIELDS = {'id', 'state', 'scope', 'reason', 'evidence', 'authority'}

_STAGE_RE = re.compile(r'(^|\s)git\s+add(?:\s|$)', re.IGNORECASE)
_COMMIT_RE = re.compile(r'(^|\s)git\s+commit(?:\s|$)', re.IGNORECASE)
_PUSH_RE = re.compile(r'(^|\s)git\s+push(?:\s|$)', re.IGNORECASE)
_RELEASE_RE = re.compile(
    r'(^|\s)git\s+tag(?:\s|$)|(^|\s)gh\s+release(?:\s|$)|Release Assets|GitHub Release',
    re.IGNORECASE,
)


def load_text(path: str) -> str:
    if path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def emit(errors: list[str], warnings: list[str], info: list[str]) -> int:
    status = 'fail' if errors else ('warn' if warnings else 'pass')
    print('R1C_OPTIONAL_VALIDATION_RESULT:')
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
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    return 2 if errors else (1 if warnings else 0)


def parse_json_object(key: str, value: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        errors.append(f'{key} must be valid JSON-compatible object: {exc.msg}')
        return None
    if not isinstance(parsed, dict):
        errors.append(f'{key} must be a JSON object')
        return None
    return parsed


def require_exact_keys(key: str, parsed: dict[str, Any], required: tuple[str, ...], errors: list[str]) -> None:
    actual = set(parsed)
    expected = set(required)
    for subkey in sorted(expected - actual):
        errors.append(f'{key} required subkey missing: {subkey}')
    for subkey in sorted(actual - expected):
        errors.append(f'{key} unknown subkey: {subkey}')


def normalize_item(value: str) -> str:
    return re.sub(r'\s+', ' ', value.strip()).casefold()


def validate_string_array_map(
    key: str,
    parsed: dict[str, Any],
    subkeys: tuple[str, ...],
    errors: list[str],
) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for subkey in subkeys:
        raw = parsed.get(subkey)
        if not isinstance(raw, list):
            errors.append(f'{key}.{subkey} must be a JSON array')
            result[subkey] = []
            continue
        checked: list[str] = []
        seen: set[str] = set()
        for index, item in enumerate(raw):
            if not isinstance(item, str) or not item.strip():
                errors.append(f'{key}.{subkey}[{index}] must be a non-empty string')
                continue
            normalized = normalize_item(item)
            if normalized in seen:
                errors.append(f'{key}.{subkey} duplicate item: {item}')
            seen.add(normalized)
            checked.append(item)
        result[subkey] = checked
    return result


def validate_evidence(
    value: str,
    verify: dict[str, list[str]] | None,
    rt: dict[str, Any] | None,
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any] | None:
    parsed = parse_json_object('EVIDENCE', value, errors)
    if parsed is None:
        return None
    require_exact_keys('EVIDENCE', parsed, EVIDENCE_KEYS, errors)
    classes = validate_string_array_map('EVIDENCE', parsed, EVIDENCE_KEYS, errors)

    normalized = {
        key: {normalize_item(item): item for item in classes.get(key, [])}
        for key in EVIDENCE_KEYS
    }
    for index, left in enumerate(EVIDENCE_KEYS):
        for right in EVIDENCE_KEYS[index + 1:]:
            overlap = sorted(set(normalized[left]) & set(normalized[right]))
            for item in overlap:
                errors.append(
                    f'EVIDENCE classification overlap between {left} and {right}: '
                    + normalized[left][item]
                )

    if verify:
        pass_items = {normalize_item(item) for item in verify.get('pass', [])}
        for evidence_class in ('not_observed', 'unverified'):
            overlap = sorted(pass_items & set(normalized[evidence_class]))
            for item in overlap:
                errors.append(
                    f'VERIFY.pass conflicts with EVIDENCE.{evidence_class}: '
                    + normalized[evidence_class][item]
                )

    if isinstance(rt, dict) and rt.get('state') == 'v':
        basis = normalize_item(str(rt.get('basis', '')))
        for evidence_class in ('not_observed', 'unverified'):
            for normalized_item, original in normalized[evidence_class].items():
                if len(normalized_item) >= 4 and normalized_item in basis:
                    errors.append(f'RT:v basis conflicts with EVIDENCE.{evidence_class}: {original}')

    if not any(classes.values()):
        warnings.append('EVIDENCE is present but all evidence classes are empty')
    return parsed


def operation_allowed(value: Any) -> bool:
    return value in {'allow', 'allow_once'}


def command_matches(commands: list[str], pattern: re.Pattern[str]) -> list[str]:
    return [command for command in commands if pattern.search(command)]


def validate_authority(
    value: str,
    files: list[str],
    commands: list[str],
    commit: dict[str, Any] | None,
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any] | None:
    parsed = parse_json_object('AUTHORITY', value, errors)
    if parsed is None:
        return None
    require_exact_keys('AUTHORITY', parsed, AUTHORITY_KEYS, errors)
    for key in AUTHORITY_KEYS:
        rail = parsed.get(key)
        if rail not in AUTHORITY_VALUES:
            errors.append(f'AUTHORITY.{key} unknown value: {rail}')

    edit = parsed.get('edit')
    if files and edit not in {'allow', 'allow_once', 'target_only'}:
        errors.append(f'AUTHORITY.edit={edit} conflicts with non-empty FILES')

    operation_checks = (
        ('stage', _STAGE_RE),
        ('commit', _COMMIT_RE),
        ('push', _PUSH_RE),
        ('release', _RELEASE_RE),
    )
    for rail_name, pattern in operation_checks:
        matching = command_matches(commands, pattern)
        if matching and not operation_allowed(parsed.get(rail_name)):
            errors.append(
                f'AUTHORITY.{rail_name}={parsed.get(rail_name)} conflicts with executed command: {matching[0]}'
            )

    if isinstance(commit, dict) and commit.get('actual') is not None:
        commit_rail = parsed.get('commit')
        permission_basis = str(commit.get('permission_basis', '')).strip()
        if commit_rail in {'forbid', 'not_requested', 'not_applicable'}:
            errors.append(f'AUTHORITY.commit={commit_rail} conflicts with COMMIT.actual')
        elif commit_rail == 'propose_only':
            if not permission_basis or permission_basis == 'none':
                errors.append('AUTHORITY.commit=propose_only with COMMIT.actual requires separate permission_basis')
            else:
                warnings.append('COMMIT.actual uses separate permission_basis while AUTHORITY.commit=propose_only')

    return parsed


def validate_annunciator(value: str, errors: list[str]) -> dict[str, Any] | None:
    parsed = parse_json_object('ANNUNCIATOR', value, errors)
    if parsed is None:
        return None
    for key in sorted(set(parsed) - ANNUNCIATOR_KEYS):
        errors.append('ANNUNCIATOR unknown subkey: ' + key)
    return parsed


def safety_gate_standalone(value: str) -> str:
    body = value.splitlines()
    return 'SAFETY_GATES:\n' + '\n'.join('  ' + line for line in body)


def parse_safety_gates_model(value: str) -> dict[str, Any]:
    view = SafetyGateCompatibilityView.from_text(safety_gate_standalone(value))
    return {
        'registry': view.registry,
        'entries': [dict(entry) for entry in view.entry_dicts],
        'entry_field_order': [list(order) for order in view.entry_field_orders],
    }


def validate_safety_gates(
    value: str,
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    model = parse_safety_gates_model(value)
    registry = model['registry']
    entries = model['entries']
    if registry != REGISTRY:
        errors.append('SAFETY_GATES unknown or missing registry: ' + str(registry))
    if not entries:
        errors.append('SAFETY_GATES entries are missing')
        return model

    seen: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        label = str(entry.get('id') or f'entry#{index}')
        for field in REQUIRED_FIELDS:
            if is_blank(entry.get(field)):
                errors.append(f'SAFETY_GATES {label}: required field missing or empty: {field}')
        for field in sorted(set(entry) - SAFETY_ENTRY_FIELDS):
            errors.append(f'SAFETY_GATES {label}: unknown field: {field}')

        gate_id = str(entry.get('id', '')).strip()
        if gate_id in seen:
            errors.append('SAFETY_GATES duplicate Safety Gate ID: ' + gate_id)
        seen.add(gate_id)
        if gate_id and gate_id not in KNOWN_IDS:
            errors.append('SAFETY_GATES unknown Safety Gate ID: ' + gate_id)

        state = str(entry.get('state', '')).strip().lower()
        if state and state not in KNOWN_STATES:
            errors.append(f'SAFETY_GATES {label}: unknown Safety Gate state: {state}')
        elif state == 'satisfied':
            if is_blank(entry.get('evidence')):
                errors.append(f'SAFETY_GATES {label}: state:satisfied requires evidence')
            if authority_is_unverified(entry.get('authority')):
                errors.append(
                    f'SAFETY_GATES {label}: state:satisfied requires verified authority or not_required'
                )
        elif state == 'blocked' and is_blank(entry.get('evidence')):
            warnings.append(f'SAFETY_GATES {label}: state:blocked should include observed evidence')
        elif state == 'na' and is_blank(entry.get('reason')):
            errors.append(f'SAFETY_GATES {label}: state:na requires reason')
    return model


def validate_optional_values(
    values: dict[str, str],
    *,
    files: list[str],
    commands: list[str],
    verify: dict[str, list[str]] | None,
    rt: dict[str, Any] | None,
    commit: dict[str, Any] | None,
    errors: list[str],
    warnings: list[str],
    info: list[str],
) -> dict[str, Any]:
    models: dict[str, Any] = {}
    if 'EVIDENCE' in values:
        models['EVIDENCE'] = validate_evidence(values['EVIDENCE'], verify, rt, errors, warnings)
        info.append('optional EVIDENCE deep lint checked')
    if 'AUTHORITY' in values:
        models['AUTHORITY'] = validate_authority(
            values['AUTHORITY'], files, commands, commit, errors, warnings
        )
        info.append('optional AUTHORITY rail lint checked')
    if 'ANNUNCIATOR' in values:
        models['ANNUNCIATOR'] = validate_annunciator(values['ANNUNCIATOR'], errors)
        info.append('optional ANNUNCIATOR structural lint checked')
    if 'SAFETY_GATES' in values:
        models['SAFETY_GATES'] = validate_safety_gates(values['SAFETY_GATES'], errors, warnings)
        info.append('optional SAFETY_GATES deep lint checked')
    return models


def parse_base_structures(values: dict[str, str], errors: list[str]) -> tuple[list[str], list[str], dict[str, list[str]] | None, dict[str, Any] | None, dict[str, Any] | None]:
    def array_value(key: str) -> list[str]:
        try:
            parsed = json.loads(values.get(key, '[]'))
        except json.JSONDecodeError as exc:
            errors.append(f'{key} must be valid JSON-compatible value: {exc.msg}')
            return []
        if not isinstance(parsed, list):
            errors.append(f'{key} must be a JSON array')
            return []
        return [item for item in parsed if isinstance(item, str)]

    def object_value(key: str) -> dict[str, Any] | None:
        try:
            parsed = json.loads(values.get(key, '{}'))
        except json.JSONDecodeError as exc:
            errors.append(f'{key} must be valid JSON-compatible value: {exc.msg}')
            return None
        if not isinstance(parsed, dict):
            errors.append(f'{key} must be a JSON object')
            return None
        return parsed

    files = array_value('FILES')
    commands = array_value('CMD')
    verify = object_value('VERIFY')
    rt = object_value('RT')
    commit = object_value('COMMIT')
    return files, commands, verify, rt, commit


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) > 1 else '-'
    text = load_text(path)
    scope = extract_result_scope(text)
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if scope is None:
        info.append('no KDSL_RESULT block detected; R1C optional target not applicable')
        return emit(errors, warnings, info)

    entries, _ = parse_top_level(scope)
    values = {key: value for key, value, _ in entries}
    schema = values.get('SCHEMA')
    if schema is None:
        info.append('KDSL_RESULT has no R1C SCHEMA marker; Full R1 fallback/out-of-scope')
        return emit(errors, warnings, info)
    if schema != SCHEMA_ID:
        errors.append('unknown R1C schema: ' + str(schema))
        return emit(errors, warnings, info)

    files, commands, verify, rt, commit = parse_base_structures(values, errors)
    models = validate_optional_values(
        values,
        files=files,
        commands=commands,
        verify=verify,
        rt=rt,
        commit=commit,
        errors=errors,
        warnings=warnings,
        info=info,
    )
    if not models:
        info.append('no optional R1C blocks present')
    info.append('R1C optional-block contract checked')
    return emit(errors, warnings, info)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
