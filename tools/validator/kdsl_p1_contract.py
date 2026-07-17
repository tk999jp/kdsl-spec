from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kdsl_parser_v2 import (
    BlockScalarNode,
    DocumentNodeV2,
    EmptyNode,
    InvalidNode,
    JsonNode,
    MappingNode,
    RecordSequenceNode,
    ScalarNode,
    SequenceNode,
)

P1L_SCHEMA_ID = 'kdsl-p1l@0.1-draft'
P1_SCHEMA_ID = 'kdsl-p1@0.1-draft'
STATUS = 'contract-candidate'

P1L_FIELD_ORDER = (
    'SCHEMA',
    'STATUS',
    'META',
    'SOURCE',
    'PROFILE',
    'TASK',
    'SCOPE',
    'CONTEXT',
    'GOAL',
    'PLAN',
    'GUARD',
    'STOP',
    'VERIFY',
    'RUNTIME',
    'OUTPUT',
    'AUTHORITY',
    'NORMALIZATION',
    'BINDING',
)

P1_SEGMENT_ORDER = (
    'SCHEMA',
    'STATUS',
    'M',
    'SRC',
    'PF',
    'T',
    'S',
    'C',
    'G',
    'P',
    'GD',
    'X',
    'V',
    'RT',
    'O',
    'A',
    'N',
    'BD',
)

P1_TO_P1L = {
    'M': 'META',
    'SRC': 'SOURCE',
    'PF': 'PROFILE',
    'T': 'TASK',
    'S': 'SCOPE',
    'C': 'CONTEXT',
    'G': 'GOAL',
    'P': 'PLAN',
    'GD': 'GUARD',
    'X': 'STOP',
    'V': 'VERIFY',
    'RT': 'RUNTIME',
    'O': 'OUTPUT',
    'A': 'AUTHORITY',
    'N': 'NORMALIZATION',
    'BD': 'BINDING',
}

SUBFIELD_ORDER = {
    'META': ('contract_rev', 'contract_id', 'parent_id'),
    'SOURCE': ('kind', 'digest', 'references'),
    'PROFILE': ('id', 'revision', 'digest', 'completion', 'completed_fields'),
    'TASK': ('kind', 'declared'),
    'SCOPE': ('source', 'read', 'target', 'non_target'),
    'CONTEXT': ('background', 'observed', 'inferred', 'unverified'),
    'GOAL': ('expected', 'questions'),
    'PLAN': ('strategy', 'steps'),
    'GUARD': ('constraints', 'safety_gates', 'protected_wording'),
    'VERIFY': ('requirements', 'unavailable_policy'),
    'RUNTIME': ('disposition', 'required_evidence'),
    'OUTPUT': ('result_schema', 'report_requirements'),
    'AUTHORITY': (
        'read',
        'edit',
        'stage',
        'commit',
        'push',
        'release',
        'public_repo',
        'destructive_ops',
    ),
    'NORMALIZATION': ('state', 'unresolved', 'loss', 'round_trip', 'semantic_equivalence'),
    'BINDING': ('runtime_control', 'state', 'executable'),
}

LIST_FIELDS = {
    ('SOURCE', 'references'),
    ('PROFILE', 'completed_fields'),
    ('SCOPE', 'source'),
    ('SCOPE', 'read'),
    ('SCOPE', 'target'),
    ('SCOPE', 'non_target'),
    ('CONTEXT', 'background'),
    ('CONTEXT', 'observed'),
    ('CONTEXT', 'inferred'),
    ('CONTEXT', 'unverified'),
    ('GOAL', 'expected'),
    ('GOAL', 'questions'),
    ('PLAN', 'strategy'),
    ('PLAN', 'steps'),
    ('GUARD', 'constraints'),
    ('GUARD', 'safety_gates'),
    ('GUARD', 'protected_wording'),
    ('VERIFY', 'requirements'),
    ('RUNTIME', 'required_evidence'),
    ('OUTPUT', 'report_requirements'),
    ('NORMALIZATION', 'unresolved'),
    ('NORMALIZATION', 'loss'),
}

AUTHORITY_VALUES = {
    'allow',
    'forbid',
    'target_only',
    'allow_once',
    'propose_only',
    'not_requested',
    'not_applicable',
}
OPERATIONAL_AUTHORITY_VALUES = {'allow', 'target_only', 'allow_once'}
TASK_KINDS = {
    'investigate',
    'plan',
    'implement',
    'fix',
    'add',
    'refactor',
    'closeout',
    'docs',
    'state',
    'review',
    'other',
}
PROFILE_COMPLETIONS = {'explicit', 'profile_completed', 'blocked'}
SOURCE_KINDS = {'kdsl-dp', 'packet', 'manual'}
RUNTIME_DISPOSITIONS = {'pending', 'user_required', 'not_applicable'}
RESULT_SCHEMAS = {'kdsl-r1c@0.1-draft', 'full-r1'}
NORMALIZATION_STATES = {'explicit', 'profile_completed', 'lossy', 'blocked'}
ROUND_TRIP_STATES = {'not_tested', 'structural_pass', 'loss_detected', 'blocked'}
BINDING_STATES = {'unbound', 'bound', 'blocked'}
SHA256_RE = re.compile(r'^sha256:[0-9a-f]{64}$')


@dataclass
class ContractParseResult:
    kind: str | None = None
    model: dict[str, Any] | None = None
    source_scope: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 2 if self.errors else (1 if self.warnings else 0)


class ContractValueError(ValueError):
    pass


def load_text(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8')


def parse_contract(text: str, expected: str | None = None, require: bool = True) -> ContractParseResult:
    p1l_scopes = _extract_p1l_scopes(text)
    p1_lines = _extract_p1_lines(text)
    result = ContractParseResult()

    if len(p1l_scopes) > 1:
        result.errors.append('duplicate P1L envelopes detected')
    if len(p1_lines) > 1:
        result.errors.append('duplicate P1 compact contracts detected')
    if p1l_scopes and p1_lines:
        result.errors.append('mixed P1L and P1 contract sources are not allowed')
    if result.errors:
        return result

    expected_upper = expected.upper() if expected else None
    if p1l_scopes:
        if expected_upper == 'P1':
            result.errors.append('P1 source required but P1L was supplied')
            return result
        return parse_p1l_scope(p1l_scopes[0])
    if p1_lines:
        if expected_upper == 'P1L':
            result.errors.append('P1L source required but P1 was supplied')
            return result
        return parse_p1_line(p1_lines[0])

    if require:
        result.errors.append('no P1L or P1 contract detected')
    else:
        result.info.append('no P1L or P1 contract detected')
    return result


def parse_p1l_scope(scope: str) -> ContractParseResult:
    result = ContractParseResult(kind='P1L', source_scope=scope)
    document = DocumentNodeV2.parse(scope, context='raw-envelope')
    for issue in document.errors:
        result.errors.append(issue.format())
    for issue in document.warnings:
        result.warnings.append(issue.format())

    envelopes = document.envelopes('P1L')
    if len(envelopes) != 1:
        result.errors.append(f'expected one P1L envelope, found {len(envelopes)}')
        return result

    envelope = envelopes[0]
    names = [field_node.name for field_node in envelope.fields]
    if tuple(names) != P1L_FIELD_ORDER:
        result.errors.append(
            'P1L field order mismatch: expected '
            + '/'.join(P1L_FIELD_ORDER)
            + ' actual '
            + '/'.join(names)
        )

    model: dict[str, Any] = {}
    for field_node in envelope.fields:
        try:
            model[field_node.name] = value_to_python(field_node.value)
        except ContractValueError as exc:
            result.errors.append(f'{field_node.name}: {exc}')
    result.model = model
    validate_model(model, result)
    if not result.errors:
        result.info.append('P1L required fields and canonical order preserved')
        result.info.append('P1L remains non-executable and unbound unless separately bound')
    return result


def parse_p1_line(line: str) -> ContractParseResult:
    result = ContractParseResult(kind='P1', source_scope=line)
    try:
        segments = split_p1_segments(line)
    except ValueError as exc:
        result.errors.append(str(exc))
        return result

    keys = [key for key, _ in segments]
    if tuple(keys) != P1_SEGMENT_ORDER:
        result.errors.append(
            'P1 segment order mismatch: expected '
            + '/'.join(P1_SEGMENT_ORDER)
            + ' actual '
            + '/'.join(keys)
        )

    values: dict[str, Any] = {}
    for key, raw_value in segments:
        if key in {'SCHEMA', 'STATUS'}:
            if not raw_value:
                result.errors.append(f'{key}: empty value')
            values[key] = raw_value
            continue
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError as exc:
            result.errors.append(f'{key}: invalid JSON: {exc.msg}')
            continue
        canonical = canonical_json(value)
        if canonical != raw_value:
            result.errors.append(f'{key}: JSON is not canonical compact serialization')
        values[key] = value

    model: dict[str, Any] = {
        'SCHEMA': values.get('SCHEMA'),
        'STATUS': values.get('STATUS'),
    }
    for compact_key, long_key in P1_TO_P1L.items():
        if compact_key in values:
            model[long_key] = values[compact_key]
    result.model = model
    validate_model(model, result, expected_schema=P1_SCHEMA_ID)
    if not result.errors:
        result.info.append('P1 ordered JSON segments parsed')
        result.info.append('P1 canonical projection can be reconstructed as P1L data')
    return result


def split_p1_segments(line: str) -> list[tuple[str, str]]:
    stripped = line.strip()
    if stripped.startswith('P1|') and '|SCHEMA=' not in stripped:
        if re.search(r'(?:^|\|)[A-Z][A-Z0-9]*:', stripped[3:]):
            raise ValueError('legacy operational P1 colon syntax is not kdsl-p1@0.1-draft')
    if not stripped.startswith('P1|'):
        raise ValueError('P1 compact contract must start with P1|')

    parts: list[str] = []
    start = 3
    depth = 0
    in_string = False
    escaped = False
    for index in range(3, len(stripped)):
        char = stripped[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char in '[{':
            depth += 1
        elif char in ']}':
            depth -= 1
            if depth < 0:
                raise ValueError('P1 contains an unmatched JSON closing delimiter')
        elif char == '|' and depth == 0:
            parts.append(stripped[start:index])
            start = index + 1
    if in_string:
        raise ValueError('P1 contains an unterminated JSON string')
    if depth != 0:
        raise ValueError('P1 contains unbalanced JSON delimiters')
    parts.append(stripped[start:])

    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for part in parts:
        if '=' not in part:
            raise ValueError('P1 segment must use key=value: ' + part)
        key, value = part.split('=', 1)
        if not key:
            raise ValueError('P1 segment key is empty')
        if key in seen:
            raise ValueError('duplicate P1 segment: ' + key)
        seen.add(key)
        entries.append((key, value))
    return entries


def render_p1(model: dict[str, Any]) -> str:
    values: list[str] = [
        'P1',
        'SCHEMA=' + P1_SCHEMA_ID,
        'STATUS=' + STATUS,
    ]
    for compact_key in P1_SEGMENT_ORDER[2:]:
        long_key = P1_TO_P1L[compact_key]
        if long_key not in model:
            raise KeyError('missing P1L field for rendering: ' + long_key)
        values.append(compact_key + '=' + canonical_json(model[long_key]))
    return '|'.join(values)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=False)


def source_digest(result: ContractParseResult) -> str | None:
    if result.source_scope is None:
        return None
    normalized = result.source_scope.replace('\r\n', '\n').replace('\r', '\n').rstrip() + '\n'
    return 'sha256:' + hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def compare_models(source: dict[str, Any], reconstructed: dict[str, Any]) -> list[str]:
    mismatches: list[str] = []
    for key in P1L_FIELD_ORDER[2:]:
        if key not in reconstructed:
            mismatches.append('required field missing after reconstruction: ' + key)
        elif reconstructed[key] != source.get(key):
            mismatches.append('required field changed: ' + key)
    extra = [key for key in reconstructed if key not in P1L_FIELD_ORDER]
    if extra:
        mismatches.append('unexpected reconstructed fields: ' + ','.join(extra))
    return mismatches


def validate_model(
    model: dict[str, Any],
    result: ContractParseResult,
    expected_schema: str = P1L_SCHEMA_ID,
) -> None:
    expected_top = set(P1L_FIELD_ORDER)
    missing = [key for key in P1L_FIELD_ORDER if key not in model]
    extra = [key for key in model if key not in expected_top]
    if missing:
        result.errors.append('missing required fields: ' + ', '.join(missing))
    if extra:
        result.errors.append('unknown top-level fields: ' + ', '.join(extra))

    if model.get('SCHEMA') != expected_schema:
        result.errors.append(f'SCHEMA must be {expected_schema}')
    if model.get('STATUS') != STATUS:
        result.errors.append(f'STATUS must be {STATUS}')

    for field_name, required_keys in SUBFIELD_ORDER.items():
        value = model.get(field_name)
        if not isinstance(value, dict):
            result.errors.append(f'{field_name} must be a mapping/object')
            continue
        actual_keys = tuple(value.keys())
        if actual_keys != required_keys:
            result.errors.append(
                f'{field_name} key order mismatch: expected '
                + '/'.join(required_keys)
                + ' actual '
                + '/'.join(actual_keys)
            )

    stop = model.get('STOP')
    if not isinstance(stop, list):
        result.errors.append('STOP must be a sequence/array')

    for field_name, subfield in LIST_FIELDS:
        parent = model.get(field_name)
        if isinstance(parent, dict) and not isinstance(parent.get(subfield), list):
            result.errors.append(f'{field_name}.{subfield} must be an array')

    _validate_source(model, result)
    _validate_profile(model, result)
    _validate_task_scope_context(model, result)
    _validate_runtime_output(model, result)
    _validate_authority(model, result)
    _validate_normalization_binding(model, result)


def _validate_source(model: dict[str, Any], result: ContractParseResult) -> None:
    source = model.get('SOURCE')
    if not isinstance(source, dict):
        return
    if source.get('kind') not in SOURCE_KINDS:
        result.errors.append('SOURCE.kind is unknown')
    digest = source.get('digest')
    if not isinstance(digest, str) or not SHA256_RE.match(digest):
        result.errors.append('SOURCE.digest must be sha256:<64 lowercase hex>')


def _validate_profile(model: dict[str, Any], result: ContractParseResult) -> None:
    profile = model.get('PROFILE')
    if not isinstance(profile, dict):
        return
    completion = profile.get('completion')
    if completion not in PROFILE_COMPLETIONS:
        result.errors.append('PROFILE.completion is unknown')
        return
    if completion == 'blocked':
        result.errors.append('PROFILE.completion is blocked')
    if completion == 'profile_completed':
        for key in ('id', 'revision', 'digest'):
            value = profile.get(key)
            if not isinstance(value, str) or value in {'', 'none', 'unknown'}:
                result.errors.append(f'PROFILE.{key} requires exact profile evidence')
        digest = profile.get('digest')
        if isinstance(digest, str) and not SHA256_RE.match(digest):
            result.errors.append('PROFILE.digest must be sha256:<64 lowercase hex>')
        completed_fields = profile.get('completed_fields')
        if not isinstance(completed_fields, list) or not completed_fields:
            result.errors.append('PROFILE.completed_fields required for profile_completed')
    elif completion == 'explicit':
        completed_fields = profile.get('completed_fields')
        if completed_fields not in ([], None):
            result.errors.append('PROFILE.completed_fields must be empty for explicit completion')


def _validate_task_scope_context(model: dict[str, Any], result: ContractParseResult) -> None:
    task = model.get('TASK')
    if isinstance(task, dict) and task.get('kind') not in TASK_KINDS:
        result.errors.append('TASK.kind is unknown')

    context = model.get('CONTEXT')
    if isinstance(context, dict):
        observed = set(_hashable_values(context.get('observed')))
        inferred = set(_hashable_values(context.get('inferred')))
        unverified = set(_hashable_values(context.get('unverified')))
        if observed & inferred:
            result.errors.append('CONTEXT observed/inferred classifications overlap')
        if observed & unverified:
            result.errors.append('CONTEXT observed/unverified classifications overlap')


def _validate_runtime_output(model: dict[str, Any], result: ContractParseResult) -> None:
    verify = model.get('VERIFY')
    if isinstance(verify, dict) and verify.get('unavailable_policy') != 'report_not_run':
        result.errors.append('VERIFY.unavailable_policy must be report_not_run')

    runtime = model.get('RUNTIME')
    if isinstance(runtime, dict):
        disposition = runtime.get('disposition')
        if disposition not in RUNTIME_DISPOSITIONS:
            result.errors.append(
                'RUNTIME.disposition must be pending|user_required|not_applicable; result-only RT claim prohibited'
            )

    output = model.get('OUTPUT')
    if isinstance(output, dict) and output.get('result_schema') not in RESULT_SCHEMAS:
        result.errors.append('OUTPUT.result_schema is unknown')


def _validate_authority(model: dict[str, Any], result: ContractParseResult) -> None:
    authority = model.get('AUTHORITY')
    if not isinstance(authority, dict):
        return
    required_rails = SUBFIELD_ORDER['AUTHORITY']
    for rail in required_rails:
        if rail not in authority:
            result.errors.append('missing AUTHORITY rail: ' + rail)
            continue
        if authority[rail] not in AUTHORITY_VALUES:
            result.errors.append(f'AUTHORITY.{rail} has unknown value')

    scope = model.get('SCOPE')
    targets = scope.get('target') if isinstance(scope, dict) else None
    if not targets:
        for rail in ('edit', 'stage', 'commit'):
            if authority.get(rail) in OPERATIONAL_AUTHORITY_VALUES:
                result.errors.append(f'AUTHORITY.{rail} requires non-empty SCOPE.target')


def _validate_normalization_binding(model: dict[str, Any], result: ContractParseResult) -> None:
    normalization = model.get('NORMALIZATION')
    binding = model.get('BINDING')
    if isinstance(normalization, dict):
        state = normalization.get('state')
        if state not in NORMALIZATION_STATES:
            result.errors.append('NORMALIZATION.state is unknown')
        round_trip = normalization.get('round_trip')
        if round_trip not in ROUND_TRIP_STATES:
            result.errors.append('NORMALIZATION.round_trip is unknown')
        if normalization.get('semantic_equivalence') != 'not_proven':
            result.errors.append('NORMALIZATION.semantic_equivalence must remain not_proven')
        unresolved = normalization.get('unresolved')
        loss = normalization.get('loss')
        if (unresolved or loss) and state != 'blocked':
            result.errors.append('NORMALIZATION with unresolved/loss must be blocked')
        if state == 'blocked':
            result.errors.append('NORMALIZATION.state is blocked')

    if isinstance(binding, dict):
        if binding.get('state') not in BINDING_STATES:
            result.errors.append('BINDING.state is unknown')
        if binding.get('executable') is not False:
            result.errors.append('BINDING.executable must be false')
        if (
            isinstance(normalization, dict)
            and normalization.get('state') == 'lossy'
            and binding.get('state') == 'bound'
        ):
            result.errors.append('lossy contract cannot be runtime-bound')


def value_to_python(node: Any) -> Any:
    if isinstance(node, JsonNode):
        return node.value
    if isinstance(node, ScalarNode):
        if node.quote is None:
            if node.value == 'true':
                return True
            if node.value == 'false':
                return False
            if node.value == 'null':
                return None
        return node.value
    if isinstance(node, BlockScalarNode):
        return node.value
    if isinstance(node, EmptyNode):
        return None
    if isinstance(node, InvalidNode):
        raise ContractValueError(node.reason)
    if isinstance(node, MappingNode):
        return {entry.key: value_to_python(entry.value) for entry in node.entries}
    if isinstance(node, (SequenceNode, RecordSequenceNode)):
        return [value_to_python(item.value) for item in node.items]
    raise ContractValueError('unsupported value node: ' + type(node).__name__)


def _extract_p1l_scopes(text: str) -> list[str]:
    normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = normalized.split('\n')
    starts = [index for index, line in enumerate(lines) if line.strip() == 'P1L:']
    scopes: list[str] = []
    for start in starts:
        end = len(lines)
        for index in range(start + 1, len(lines)):
            stripped = lines[index].strip()
            if stripped == '```':
                end = index
                break
            if lines[index].startswith('#'):
                end = index
                break
            if index != start and stripped == 'P1L:':
                end = index
                break
        scopes.append('\n'.join(lines[start:end]).rstrip())
    return scopes


def _extract_p1_lines(text: str) -> list[str]:
    normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    return [line.strip() for line in normalized.split('\n') if line.strip().startswith('P1|')]


def _hashable_values(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [canonical_json(item) if not isinstance(item, str) else item for item in value]


def emit_result(result: ContractParseResult) -> int:
    status = 'fail' if result.errors else ('warn' if result.warnings else 'pass')
    schema = None
    if result.model:
        schema = result.model.get('SCHEMA')
    print('P1_CONTRACT_RESULT:')
    print('STATUS: ' + status)
    print('KIND: ' + str(result.kind or 'none'))
    print('SCHEMA: ' + str(schema or 'none'))
    print('SOURCE_DIGEST: ' + str(source_digest(result)))
    print('EXECUTABLE: no')
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    print('ERRORS:')
    for item in result.errors or ['none']:
        print('  - ' + item)
    print('WARNINGS:')
    for item in result.warnings or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in result.info or ['none']:
        print('  - ' + item)
    return result.exit_code


def cli_main(argv: list[str], expected: str | None = None, require: bool = True) -> int:
    if len(argv) != 2:
        print('usage: python kdsl_p1_contract.py <p1l-or-p1-file>')
        return 2
    text = load_text(argv[1])
    return emit_result(parse_contract(text, expected=expected, require=require))


def main(argv: list[str]) -> int:
    return cli_main(argv)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
