from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kdsl_p1_contract import ContractValueError, value_to_python
from kdsl_parser_v2 import DocumentNodeV2

K1_SCHEMA_ID = 'kdsl-k1@0.1-draft'
PF1_SCHEMA_ID = 'kdsl-pf1@0.1-draft'
C14N_ID = 'kdsl-runtime-control-c14n@0.1-draft'
K1_STATUS = 'runtime-control-definition'
PF1_STATUS = 'project-runtime-control-profile'
SELF_DIGEST = 'sha256:SELF'
SHA256_RE = re.compile(r'^sha256:[0-9a-f]{64}$')

CONTRACT_SCHEMAS = ['kdsl-p1l@0.1-draft', 'kdsl-p1@0.1-draft']
AUTHORITY_RAILS = [
    'read',
    'edit',
    'stage',
    'commit',
    'push',
    'release',
    'public_repo',
    'destructive_ops',
]
P1L_AUTHORITY_VALUES = [
    'allow',
    'forbid',
    'target_only',
    'allow_once',
    'propose_only',
    'not_requested',
    'not_applicable',
]
REQUIRED_STATES = [
    'authoring_valid',
    'contract_valid',
    'profile_resolved',
    'runtime_control_valid',
    'binding_valid',
    'authority_sufficient',
    'capability_sufficient',
    'stop_clear',
    'executable',
    'executed',
    'verified',
    'runtime_verified',
]
PRE_EXECUTION_VALUES = ['pending', 'user_required', 'not_applicable']
R1_RUNTIME_VALUES = ['v', 'fail', 'blk']
RESULT_SCHEMAS = ['kdsl-r1c@0.1-draft', 'full-r1']
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

K1_FIELD_ORDER = (
    'SCHEMA',
    'STATUS',
    'IDENTITY',
    'APPLIES_TO',
    'STATE_MODEL',
    'COMPLETION_POLICY',
    'AUTHORITY_POLICY',
    'CAPABILITY_POLICY',
    'STOP_POLICY',
    'VERIFY_POLICY',
    'RUNTIME_POLICY',
    'RESULT_POLICY',
    'CONFLICT_POLICY',
    'BINDING_REQUIREMENTS',
)
PF1_FIELD_ORDER = (
    'SCHEMA',
    'STATUS',
    'IDENTITY',
    'KERNEL_REF',
    'PROJECT',
    'APPLIES_TO',
    'DEFAULTS',
    'PRESETS',
    'ALIASES',
    'RESTRICTIONS',
    'AUTHORITY_CEILING',
    'CAPABILITY_REQUIREMENTS',
    'ROUTING',
    'RUNTIME_POLICY',
    'RESULT_POLICY',
    'COMPATIBILITY',
)

IDENTITY_ORDER = ('id', 'revision', 'canonicalization', 'digest', 'source_ref')
K1_MAPPING_ORDER = {
    'IDENTITY': IDENTITY_ORDER,
    'APPLIES_TO': ('contract_schemas', 'project_scope', 'no_profile_task_kinds'),
    'STATE_MODEL': ('required_states', 'executable_under_current_contract'),
    'COMPLETION_POLICY': (
        'exact_identity_required',
        'inference_prohibited',
        'provenance_required',
        'cyclic_expansion',
        'ambiguous_expansion',
    ),
    'AUTHORITY_POLICY': (
        'rails',
        'p1l_values',
        'non_widening',
        'missing_rail',
        'approval_reference_required_when_declared',
    ),
    'CAPABILITY_POLICY': (
        'sufficient_claim',
        'inferred_claim',
        'unverified_claim',
        'stale_claim',
        'capability_is_permission',
    ),
    'STOP_POLICY': ('continuation_is_authority', 'active_for_requested_operation', 'unknown_state'),
    'VERIFY_POLICY': ('requirement_is_result', 'unavailable_is_pass', 'not_run_is_pass'),
    'RUNTIME_POLICY': ('pre_execution_values', 'result_values_reserved_for_r1', 'build_test_ci_is_rt_v'),
    'RESULT_POLICY': ('next_is_authority', 'commit_field_is_commit_authority', 'required_result_schema'),
    'CONFLICT_POLICY': (
        'unknown_definition',
        'identity_mismatch',
        'category_mismatch',
        'protected_wording_weakening',
        'critical_exact_string_change',
    ),
    'BINDING_REQUIREMENTS': (
        'evidence_representation',
        'evidence_schema',
        'reference_from_p1l_binding',
        'executable',
        'semantic_equivalence',
        'execution_authority',
    ),
}
PF1_MAPPING_ORDER = {
    'IDENTITY': IDENTITY_ORDER,
    'KERNEL_REF': ('id', 'revision', 'digest'),
    'PROJECT': ('id', 'repository', 'root_ref'),
    'APPLIES_TO': ('contract_schemas', 'task_kinds', 'excluded_task_kinds'),
    'DEFAULTS': ('guard', 'verify', 'stop', 'output', 'runtime_disposition', 'result_schema'),
    'PRESETS': ('guard', 'verify', 'stop', 'output', 'runtime'),
    'AUTHORITY_CEILING': tuple(AUTHORITY_RAILS),
    'RUNTIME_POLICY': ('code_change_default', 'docs_only_default', 'state_only_default'),
    'RESULT_POLICY': ('result_schema', 'report_requirements'),
    'COMPATIBILITY': ('legacy_profile_ids', 'legacy_aliases', 'migration_notes'),
}

CEILING_MODES = {'allow_max', 'propose_only_max', 'forbid', 'approval_required', 'not_applicable_only'}
CEILING_SCOPES = {'any', 'target_only'}
CEILING_CARDINALITIES = {'any', 'once'}
ALIAS_CATEGORIES = {'task', 'strategy', 'guard', 'verify', 'stop', 'output', 'runtime', 'route'}
RESTRICTION_EFFECTS = {'forbid', 'approval_required', 'stop'}
ROUTE_KINDS = {'skill', 'tool', 'workflow'}
INVALIDATION_VALUES = {
    'time_expired',
    'scope_changed',
    'environment_digest_changed',
    'credential_rotated',
    'repository_state_changed',
    'explicit_revocation',
}


@dataclass
class RuntimeControlParseResult:
    kind: str | None = None
    model: dict[str, Any] | None = None
    source_scope: str | None = None
    computed_digest: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 2 if self.errors else (1 if self.warnings else 0)


@dataclass
class RuntimeControlResolution:
    identity_state: str = 'blocked'
    kernel_ref_state: str = 'blocked'
    project_scope_state: str = 'blocked'
    runtime_control_state: str = 'blocked'
    executable: bool = False
    semantic_equivalence: str = 'not_proven'
    execution_authority: str = 'none'
    errors: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 2 if self.errors else 0


def load_text(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8')


def parse_definition(text: str, expected: str, require: bool = True) -> RuntimeControlParseResult:
    kind = expected.upper()
    if kind not in {'K1', 'PF1'}:
        raise ValueError('expected must be K1 or PF1')
    scopes = _extract_scopes(text, kind)
    result = RuntimeControlParseResult(kind=kind)
    if len(scopes) > 1:
        result.errors.append(f'duplicate {kind} envelopes detected')
        return result
    if not scopes:
        if require:
            result.errors.append(f'no {kind} definition detected')
        else:
            result.info.append(f'no {kind} definition detected')
        return result
    return parse_scope(scopes[0], kind)


def parse_scope(scope: str, kind: str) -> RuntimeControlParseResult:
    kind = kind.upper()
    result = RuntimeControlParseResult(kind=kind, source_scope=scope)
    document = DocumentNodeV2.parse(scope, context='raw-envelope')
    for issue in document.errors:
        result.errors.append(issue.format())
    for issue in document.warnings:
        result.warnings.append(issue.format())

    envelopes = document.envelopes(kind)
    if len(envelopes) != 1:
        result.errors.append(f'expected one {kind} envelope, found {len(envelopes)}')
        return result
    envelope = envelopes[0]
    expected_order = K1_FIELD_ORDER if kind == 'K1' else PF1_FIELD_ORDER
    actual_order = tuple(field_node.name for field_node in envelope.fields)
    if actual_order != expected_order:
        result.errors.append(
            f'{kind} field order mismatch: expected '
            + '/'.join(expected_order)
            + ' actual '
            + '/'.join(actual_order)
        )

    model: dict[str, Any] = {}
    for field_node in envelope.fields:
        try:
            model[field_node.name] = value_to_python(field_node.value)
        except ContractValueError as exc:
            result.errors.append(f'{field_node.name}: {exc}')
    result.model = model
    if kind == 'K1':
        validate_k1(model, result)
    else:
        validate_pf1(model, result)
    _validate_digest(kind, model, result)
    if not result.errors:
        result.info.append(f'{kind} schema/order/type validation passed')
        result.info.append('definition remains non-executable and grants no authority')
    return result


def parse_bundle(text: str) -> tuple[RuntimeControlParseResult, RuntimeControlParseResult]:
    return parse_definition(text, 'K1'), parse_definition(text, 'PF1')


def canonical_projection(kind: str, model: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(model)
    identity = normalized.get('IDENTITY')
    if not isinstance(identity, dict):
        raise ValueError('IDENTITY must be a mapping/object for canonical projection')
    identity['digest'] = SELF_DIGEST
    return {kind.upper(): normalized}


def canonical_json(kind: str, model: dict[str, Any]) -> str:
    return json.dumps(
        canonical_projection(kind, model),
        ensure_ascii=False,
        separators=(',', ':'),
        sort_keys=False,
    )


def compute_digest(kind: str, model: dict[str, Any]) -> str:
    payload = canonical_json(kind, model).encode('utf-8')
    return 'sha256:' + hashlib.sha256(payload).hexdigest()


def validate_k1(model: dict[str, Any], result: RuntimeControlParseResult) -> None:
    _validate_top_level(model, K1_FIELD_ORDER, 'K1', result)
    _validate_mapping_orders(model, K1_MAPPING_ORDER, result)
    if model.get('SCHEMA') != K1_SCHEMA_ID:
        result.errors.append(f'SCHEMA must be {K1_SCHEMA_ID}')
    if model.get('STATUS') != K1_STATUS:
        result.errors.append(f'STATUS must be {K1_STATUS}')
    _validate_identity(model.get('IDENTITY'), result)

    applies = _mapping(model, 'APPLIES_TO')
    if applies is not None:
        _require_exact_list(applies, 'contract_schemas', CONTRACT_SCHEMAS, 'APPLIES_TO.contract_schemas', result)
        project_scope = applies.get('project_scope')
        valid_scope = isinstance(project_scope, str) and (
            project_scope == 'global'
            or (project_scope.startswith('repository:') and len(project_scope) > len('repository:'))
            or (project_scope.startswith('project:') and len(project_scope) > len('project:'))
        )
        if not valid_scope:
            result.errors.append('APPLIES_TO.project_scope must be global|repository:<exact>|project:<exact>')
        no_profile = _require_string_list(applies, 'no_profile_task_kinds', 'APPLIES_TO.no_profile_task_kinds', result)
        _validate_task_kinds(no_profile, 'APPLIES_TO.no_profile_task_kinds', result)

    state = _mapping(model, 'STATE_MODEL')
    if state is not None:
        _require_exact_list(state, 'required_states', REQUIRED_STATES, 'STATE_MODEL.required_states', result)
        _require_exact(state, 'executable_under_current_contract', False, 'STATE_MODEL.executable_under_current_contract', result)

    completion = _mapping(model, 'COMPLETION_POLICY')
    if completion is not None:
        for key in ('exact_identity_required', 'inference_prohibited', 'provenance_required'):
            _require_exact(completion, key, True, 'COMPLETION_POLICY.' + key, result)
        _require_exact(completion, 'cyclic_expansion', 'blocked', 'COMPLETION_POLICY.cyclic_expansion', result)
        _require_exact(completion, 'ambiguous_expansion', 'blocked', 'COMPLETION_POLICY.ambiguous_expansion', result)

    authority = _mapping(model, 'AUTHORITY_POLICY')
    if authority is not None:
        _require_exact_list(authority, 'rails', AUTHORITY_RAILS, 'AUTHORITY_POLICY.rails', result)
        _require_exact_list(authority, 'p1l_values', P1L_AUTHORITY_VALUES, 'AUTHORITY_POLICY.p1l_values', result)
        _require_exact(authority, 'non_widening', True, 'AUTHORITY_POLICY.non_widening', result)
        _require_exact(authority, 'missing_rail', 'blocked', 'AUTHORITY_POLICY.missing_rail', result)
        _require_exact(
            authority,
            'approval_reference_required_when_declared',
            True,
            'AUTHORITY_POLICY.approval_reference_required_when_declared',
            result,
        )

    capability = _mapping(model, 'CAPABILITY_POLICY')
    if capability is not None:
        _require_exact(capability, 'sufficient_claim', 'observed_current', 'CAPABILITY_POLICY.sufficient_claim', result)
        for key in ('inferred_claim', 'unverified_claim', 'stale_claim'):
            _require_exact(capability, key, 'insufficient', 'CAPABILITY_POLICY.' + key, result)
        _require_exact(capability, 'capability_is_permission', False, 'CAPABILITY_POLICY.capability_is_permission', result)

    _validate_fixed_mapping(
        model,
        'STOP_POLICY',
        {
            'continuation_is_authority': False,
            'active_for_requested_operation': 'blocked',
            'unknown_state': 'blocked',
        },
        result,
    )
    _validate_fixed_mapping(
        model,
        'VERIFY_POLICY',
        {'requirement_is_result': False, 'unavailable_is_pass': False, 'not_run_is_pass': False},
        result,
    )

    runtime = _mapping(model, 'RUNTIME_POLICY')
    if runtime is not None:
        _require_exact_list(runtime, 'pre_execution_values', PRE_EXECUTION_VALUES, 'RUNTIME_POLICY.pre_execution_values', result)
        _require_exact_list(runtime, 'result_values_reserved_for_r1', R1_RUNTIME_VALUES, 'RUNTIME_POLICY.result_values_reserved_for_r1', result)
        _require_exact(runtime, 'build_test_ci_is_rt_v', False, 'RUNTIME_POLICY.build_test_ci_is_rt_v', result)

    result_policy = _mapping(model, 'RESULT_POLICY')
    if result_policy is not None:
        _require_exact(result_policy, 'next_is_authority', False, 'RESULT_POLICY.next_is_authority', result)
        _require_exact(result_policy, 'commit_field_is_commit_authority', False, 'RESULT_POLICY.commit_field_is_commit_authority', result)
        _require_exact_list(result_policy, 'required_result_schema', RESULT_SCHEMAS, 'RESULT_POLICY.required_result_schema', result)

    _validate_fixed_mapping(
        model,
        'CONFLICT_POLICY',
        {
            'unknown_definition': 'blocked',
            'identity_mismatch': 'blocked',
            'category_mismatch': 'blocked',
            'protected_wording_weakening': 'blocked',
            'critical_exact_string_change': 'blocked',
        },
        result,
    )
    _validate_fixed_mapping(
        model,
        'BINDING_REQUIREMENTS',
        {
            'evidence_representation': 'external_content_addressed_record',
            'evidence_schema': 'kdsl-binding-evidence@0.1-draft',
            'reference_from_p1l_binding': 'required',
            'executable': False,
            'semantic_equivalence': 'not_proven',
            'execution_authority': 'none',
        },
        result,
    )


def validate_pf1(model: dict[str, Any], result: RuntimeControlParseResult) -> None:
    _validate_top_level(model, PF1_FIELD_ORDER, 'PF1', result)
    _validate_mapping_orders(model, PF1_MAPPING_ORDER, result)
    if model.get('SCHEMA') != PF1_SCHEMA_ID:
        result.errors.append(f'SCHEMA must be {PF1_SCHEMA_ID}')
    if model.get('STATUS') != PF1_STATUS:
        result.errors.append(f'STATUS must be {PF1_STATUS}')
    _validate_identity(model.get('IDENTITY'), result)

    kernel_ref = _mapping(model, 'KERNEL_REF')
    if kernel_ref is not None:
        _require_exact_string(kernel_ref, 'id', 'KERNEL_REF.id', result)
        _require_exact_string(kernel_ref, 'revision', 'KERNEL_REF.revision', result)
        _require_digest(kernel_ref.get('digest'), 'KERNEL_REF.digest', result)

    project = _mapping(model, 'PROJECT')
    if project is not None:
        _require_exact_string(project, 'id', 'PROJECT.id', result)
        repository = project.get('repository')
        if not isinstance(repository, str) or not repository:
            result.errors.append('PROJECT.repository must be an exact string or none')
        _require_exact_string(project, 'root_ref', 'PROJECT.root_ref', result)

    applies = _mapping(model, 'APPLIES_TO')
    if applies is not None:
        _require_exact_list(applies, 'contract_schemas', CONTRACT_SCHEMAS, 'APPLIES_TO.contract_schemas', result)
        task_kinds = _require_string_list(applies, 'task_kinds', 'APPLIES_TO.task_kinds', result)
        excluded = _require_string_list(applies, 'excluded_task_kinds', 'APPLIES_TO.excluded_task_kinds', result)
        _validate_task_kinds(task_kinds, 'APPLIES_TO.task_kinds', result)
        _validate_task_kinds(excluded, 'APPLIES_TO.excluded_task_kinds', result)
        if set(task_kinds) & set(excluded):
            result.errors.append('APPLIES_TO task_kinds/excluded_task_kinds conflict')

    defaults = _mapping(model, 'DEFAULTS')
    if defaults is not None:
        for key in ('guard', 'verify', 'stop', 'output'):
            _require_exact_string(defaults, key, 'DEFAULTS.' + key, result)
        if defaults.get('runtime_disposition') not in {*PRE_EXECUTION_VALUES, 'none'}:
            result.errors.append('DEFAULTS.runtime_disposition is unknown')
        if defaults.get('result_schema') not in {*RESULT_SCHEMAS, 'none'}:
            result.errors.append('DEFAULTS.result_schema is unknown')

    presets = _mapping(model, 'PRESETS')
    if presets is not None:
        _validate_presets(presets, result)
    _validate_aliases(model.get('ALIASES'), result)
    _validate_restrictions(model.get('RESTRICTIONS'), result)
    _validate_authority_ceiling(model.get('AUTHORITY_CEILING'), result)
    _validate_capability_requirements(model.get('CAPABILITY_REQUIREMENTS'), result)
    _validate_routes(model.get('ROUTING'), result)

    runtime = _mapping(model, 'RUNTIME_POLICY')
    if runtime is not None:
        for key in ('code_change_default', 'docs_only_default', 'state_only_default'):
            if runtime.get(key) not in PRE_EXECUTION_VALUES:
                result.errors.append('RUNTIME_POLICY.' + key + ' is unknown')

    result_policy = _mapping(model, 'RESULT_POLICY')
    if result_policy is not None:
        if result_policy.get('result_schema') not in RESULT_SCHEMAS:
            result.errors.append('RESULT_POLICY.result_schema is unknown')
        _require_string_list(result_policy, 'report_requirements', 'RESULT_POLICY.report_requirements', result)

    compatibility = _mapping(model, 'COMPATIBILITY')
    if compatibility is not None:
        for key in PF1_MAPPING_ORDER['COMPATIBILITY']:
            _require_string_list(compatibility, key, 'COMPATIBILITY.' + key, result)


def resolve_runtime_control(
    k1: RuntimeControlParseResult,
    pf1: RuntimeControlParseResult,
) -> RuntimeControlResolution:
    resolution = RuntimeControlResolution()
    if k1.errors:
        resolution.errors.extend('K1: ' + item for item in k1.errors)
    if pf1.errors:
        resolution.errors.extend('PF1: ' + item for item in pf1.errors)
    if resolution.errors or k1.model is None or pf1.model is None:
        return resolution

    k1_identity = k1.model['IDENTITY']
    pf1_identity = pf1.model['IDENTITY']
    kernel_ref = pf1.model['KERNEL_REF']
    if all(isinstance(item, dict) for item in (k1_identity, pf1_identity, kernel_ref)):
        resolution.identity_state = 'resolved'
    else:
        resolution.errors.append('identity records are not mappings')
        return resolution

    mismatches = []
    for key in ('id', 'revision', 'digest'):
        if kernel_ref.get(key) != k1_identity.get(key):
            mismatches.append(key)
    if mismatches:
        resolution.errors.append('PF1 KERNEL_REF mismatch: ' + ','.join(mismatches))
    else:
        resolution.kernel_ref_state = 'resolved'

    scope = k1.model['APPLIES_TO']['project_scope']
    project = pf1.model['PROJECT']
    if scope == 'global':
        resolution.project_scope_state = 'resolved'
    elif scope.startswith('repository:') and project.get('repository') == scope.split(':', 1)[1]:
        resolution.project_scope_state = 'resolved'
    elif scope.startswith('project:') and project.get('id') == scope.split(':', 1)[1]:
        resolution.project_scope_state = 'resolved'
    else:
        resolution.errors.append('PF1 PROJECT does not match K1 project_scope')

    k1_contracts = k1.model['APPLIES_TO']['contract_schemas']
    pf1_contracts = pf1.model['APPLIES_TO']['contract_schemas']
    if pf1_contracts != k1_contracts:
        resolution.errors.append('PF1 contract_schemas do not exactly match K1 contract_schemas')

    if not resolution.errors:
        resolution.runtime_control_state = 'valid'
        resolution.info.append('K1 identity and PF1 KERNEL_REF resolved exactly')
        resolution.info.append('project scope and contract schema compatibility resolved')
        resolution.info.append('resolution remains non-executable and grants no authority')
    return resolution


def emit_parse_result(result: RuntimeControlParseResult) -> int:
    status = 'fail' if result.errors else ('warn' if result.warnings else 'pass')
    schema = result.model.get('SCHEMA') if result.model else None
    stored_digest = result.model.get('IDENTITY', {}).get('digest') if result.model else None
    print('RUNTIME_CONTROL_RESULT:')
    print('STATUS: ' + status)
    print('KIND: ' + str(result.kind or 'none'))
    print('SCHEMA: ' + str(schema or 'none'))
    print('STORED_DIGEST: ' + str(stored_digest or 'none'))
    print('COMPUTED_DIGEST: ' + str(result.computed_digest or 'none'))
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


def emit_resolution(result: RuntimeControlResolution) -> int:
    print('RUNTIME_CONTROL_RESOLUTION:')
    print('STATUS: ' + ('blocked' if result.errors else 'valid'))
    print('IDENTITY_STATE: ' + result.identity_state)
    print('KERNEL_REF_STATE: ' + result.kernel_ref_state)
    print('PROJECT_SCOPE_STATE: ' + result.project_scope_state)
    print('RUNTIME_CONTROL_STATE: ' + result.runtime_control_state)
    print('EXECUTABLE: false')
    print('SEMANTIC_EQUIVALENCE: ' + result.semantic_equivalence)
    print('EXECUTION_AUTHORITY: ' + result.execution_authority)
    print('ERRORS:')
    for item in result.errors or ['none']:
        print('  - ' + item)
    print('INFO:')
    for item in result.info or ['none']:
        print('  - ' + item)
    return result.exit_code


def cli_definition(argv: list[str], expected: str) -> int:
    if len(argv) != 2:
        print(f'usage: python kdsl_{expected.lower()}.py <{expected.lower()}-file>')
        return 2
    return emit_parse_result(parse_definition(load_text(argv[1]), expected))


def cli_resolve(argv: list[str]) -> int:
    if len(argv) == 2:
        text = load_text(argv[1])
        k1, pf1 = parse_bundle(text)
    elif len(argv) == 3:
        k1 = parse_definition(load_text(argv[1]), 'K1')
        pf1 = parse_definition(load_text(argv[2]), 'PF1')
    else:
        print('usage: python kdsl_runtime_control_resolve.py <bundle-file> OR <k1-file> <pf1-file>')
        return 2
    return emit_resolution(resolve_runtime_control(k1, pf1))


def _validate_top_level(
    model: dict[str, Any],
    expected_order: tuple[str, ...],
    kind: str,
    result: RuntimeControlParseResult,
) -> None:
    missing = [key for key in expected_order if key not in model]
    extra = [key for key in model if key not in expected_order]
    if missing:
        result.errors.append('missing required fields: ' + ', '.join(missing))
    if extra:
        result.errors.append('unknown top-level fields: ' + ', '.join(extra))
    if tuple(model.keys()) != expected_order:
        result.errors.append(
            f'{kind} model field order mismatch: expected '
            + '/'.join(expected_order)
            + ' actual '
            + '/'.join(model.keys())
        )


def _validate_mapping_orders(
    model: dict[str, Any],
    mapping_order: dict[str, tuple[str, ...]],
    result: RuntimeControlParseResult,
) -> None:
    for field_name, expected_keys in mapping_order.items():
        value = model.get(field_name)
        if not isinstance(value, dict):
            result.errors.append(f'{field_name} must be a mapping/object')
            continue
        actual_keys = tuple(value.keys())
        if actual_keys != expected_keys:
            result.errors.append(
                f'{field_name} key order mismatch: expected '
                + '/'.join(expected_keys)
                + ' actual '
                + '/'.join(actual_keys)
            )


def _validate_identity(value: Any, result: RuntimeControlParseResult) -> None:
    if not isinstance(value, dict):
        return
    for key in ('id', 'revision', 'source_ref'):
        _require_exact_string(value, key, 'IDENTITY.' + key, result)
    if value.get('canonicalization') != C14N_ID:
        result.errors.append(f'IDENTITY.canonicalization must be {C14N_ID}')
    _require_digest(value.get('digest'), 'IDENTITY.digest', result)
    if value.get('digest') == SELF_DIGEST:
        result.errors.append('stored IDENTITY.digest must not be sha256:SELF')


def _validate_digest(kind: str, model: dict[str, Any], result: RuntimeControlParseResult) -> None:
    identity = model.get('IDENTITY')
    if not isinstance(identity, dict):
        return
    try:
        computed = compute_digest(kind, model)
    except (TypeError, ValueError) as exc:
        result.errors.append('canonical digest computation failed: ' + str(exc))
        return
    result.computed_digest = computed
    stored = identity.get('digest')
    if isinstance(stored, str) and SHA256_RE.match(stored) and stored != computed:
        result.errors.append('IDENTITY.digest mismatch')


def _validate_fixed_mapping(
    model: dict[str, Any],
    field_name: str,
    expected: dict[str, Any],
    result: RuntimeControlParseResult,
) -> None:
    value = _mapping(model, field_name)
    if value is None:
        return
    for key, expected_value in expected.items():
        _require_exact(value, key, expected_value, field_name + '.' + key, result)


def _validate_presets(presets: dict[str, Any], result: RuntimeControlParseResult) -> None:
    seen: set[str] = set()
    for category in PF1_MAPPING_ORDER['PRESETS']:
        records = presets.get(category)
        if not isinstance(records, list):
            result.errors.append('PRESETS.' + category + ' must be an array')
            continue
        for index, record in enumerate(records):
            path = f'PRESETS.{category}[{index}]'
            if not isinstance(record, dict):
                result.errors.append(path + ' must be an object')
                continue
            _require_record_order(record, ('id', 'category', 'expansion', 'ordered'), path, result)
            record_id = record.get('id')
            if not isinstance(record_id, str) or not record_id:
                result.errors.append(path + '.id must be exact non-empty string')
            elif record_id in seen:
                result.errors.append('duplicate preset id: ' + record_id)
            else:
                seen.add(record_id)
            if record.get('category') != category:
                result.errors.append(path + '.category mismatch')
            if not isinstance(record.get('expansion'), list):
                result.errors.append(path + '.expansion must be an array')
            if not isinstance(record.get('ordered'), bool):
                result.errors.append(path + '.ordered must be boolean')


def _validate_aliases(value: Any, result: RuntimeControlParseResult) -> None:
    if not isinstance(value, list):
        result.errors.append('ALIASES must be an array')
        return
    seen: set[str] = set()
    for index, record in enumerate(value):
        path = f'ALIASES[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        _require_record_order(record, ('id', 'category', 'expands_to'), path, result)
        alias_id = record.get('id')
        if not isinstance(alias_id, str) or not alias_id:
            result.errors.append(path + '.id must be exact non-empty string')
        elif alias_id in seen:
            result.errors.append('duplicate alias id: ' + alias_id)
        else:
            seen.add(alias_id)
        if record.get('category') not in ALIAS_CATEGORIES:
            result.errors.append(path + '.category is unknown')
        _require_exact_string(record, 'expands_to', path + '.expands_to', result)


def _validate_restrictions(value: Any, result: RuntimeControlParseResult) -> None:
    if not isinstance(value, list):
        result.errors.append('RESTRICTIONS must be an array')
        return
    seen: set[str] = set()
    for index, record in enumerate(value):
        path = f'RESTRICTIONS[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        _require_record_order(record, ('id', 'applies_to', 'effect', 'scope', 'protected_wording'), path, result)
        record_id = record.get('id')
        if not isinstance(record_id, str) or not record_id:
            result.errors.append(path + '.id must be exact non-empty string')
        elif record_id in seen:
            result.errors.append('duplicate restriction id: ' + record_id)
        else:
            seen.add(record_id)
        applies = record.get('applies_to')
        if not isinstance(applies, dict):
            result.errors.append(path + '.applies_to must be an object')
        else:
            _require_record_order(applies, ('task_kinds', 'rails'), path + '.applies_to', result)
            tasks = _require_string_list(applies, 'task_kinds', path + '.applies_to.task_kinds', result)
            _validate_task_kinds(tasks, path + '.applies_to.task_kinds', result)
            rails = _require_string_list(applies, 'rails', path + '.applies_to.rails', result)
            for rail in rails:
                if rail not in AUTHORITY_RAILS:
                    result.errors.append(path + '.applies_to.rails contains unknown rail: ' + rail)
        if record.get('effect') not in RESTRICTION_EFFECTS:
            result.errors.append(path + '.effect is unknown')
        _require_exact_string(record, 'scope', path + '.scope', result)
        _require_exact_string(record, 'protected_wording', path + '.protected_wording', result)


def _validate_authority_ceiling(value: Any, result: RuntimeControlParseResult) -> None:
    if not isinstance(value, dict):
        return
    if tuple(value.keys()) != tuple(AUTHORITY_RAILS):
        result.errors.append('AUTHORITY_CEILING rail order mismatch')
    for rail in AUTHORITY_RAILS:
        ceiling = value.get(rail)
        path = 'AUTHORITY_CEILING.' + rail
        if not isinstance(ceiling, dict):
            result.errors.append(path + ' must be an object')
            continue
        _require_record_order(ceiling, ('mode', 'scope', 'cardinality'), path, result)
        if ceiling.get('mode') not in CEILING_MODES:
            result.errors.append(path + '.mode is unknown')
        if ceiling.get('scope') not in CEILING_SCOPES:
            result.errors.append(path + '.scope is unknown')
        if ceiling.get('cardinality') not in CEILING_CARDINALITIES:
            result.errors.append(path + '.cardinality is unknown')


def _validate_capability_requirements(value: Any, result: RuntimeControlParseResult) -> None:
    if not isinstance(value, list):
        result.errors.append('CAPABILITY_REQUIREMENTS must be an array')
        return
    seen: set[str] = set()
    expected_order = (
        'id',
        'capability',
        'task_kinds',
        'scope',
        'max_age_seconds',
        'required_state',
        'invalidation',
    )
    for index, record in enumerate(value):
        path = f'CAPABILITY_REQUIREMENTS[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        _require_record_order(record, expected_order, path, result)
        record_id = record.get('id')
        if not isinstance(record_id, str) or not record_id:
            result.errors.append(path + '.id must be exact non-empty string')
        elif record_id in seen:
            result.errors.append('duplicate capability requirement id: ' + record_id)
        else:
            seen.add(record_id)
        _require_exact_string(record, 'capability', path + '.capability', result)
        tasks = _require_string_list(record, 'task_kinds', path + '.task_kinds', result)
        _validate_task_kinds(tasks, path + '.task_kinds', result)
        _require_exact_string(record, 'scope', path + '.scope', result)
        max_age = record.get('max_age_seconds')
        if not isinstance(max_age, int) or isinstance(max_age, bool) or max_age <= 0:
            result.errors.append(path + '.max_age_seconds must be a positive integer')
        if record.get('required_state') != 'observed':
            result.errors.append(path + '.required_state must be observed')
        invalidation = _require_string_list(record, 'invalidation', path + '.invalidation', result)
        unknown = [item for item in invalidation if item not in INVALIDATION_VALUES]
        if unknown:
            result.errors.append(path + '.invalidation contains unknown values: ' + ','.join(unknown))


def _validate_routes(value: Any, result: RuntimeControlParseResult) -> None:
    if not isinstance(value, list):
        result.errors.append('ROUTING must be an array')
        return
    seen: set[str] = set()
    expected_order = ('id', 'task_kinds', 'kind', 'target_id', 'revision', 'digest', 'immutable_ref')
    for index, record in enumerate(value):
        path = f'ROUTING[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        _require_record_order(record, expected_order, path, result)
        route_id = record.get('id')
        if not isinstance(route_id, str) or not route_id:
            result.errors.append(path + '.id must be exact non-empty string')
        elif route_id in seen:
            result.errors.append('duplicate route id: ' + route_id)
        else:
            seen.add(route_id)
        tasks = _require_string_list(record, 'task_kinds', path + '.task_kinds', result)
        _validate_task_kinds(tasks, path + '.task_kinds', result)
        if record.get('kind') not in ROUTE_KINDS:
            result.errors.append(path + '.kind is unknown')
        _require_exact_string(record, 'target_id', path + '.target_id', result)
        _require_exact_string(record, 'revision', path + '.revision', result)
        digest = record.get('digest')
        immutable_ref = record.get('immutable_ref')
        if digest != 'none':
            _require_digest(digest, path + '.digest', result)
        if immutable_ref != 'none' and (not isinstance(immutable_ref, str) or not immutable_ref):
            result.errors.append(path + '.immutable_ref must be exact string or none')
        if digest == 'none' and immutable_ref == 'none':
            result.errors.append(path + ' requires digest or immutable_ref')


def _mapping(model: dict[str, Any], field_name: str) -> dict[str, Any] | None:
    value = model.get(field_name)
    return value if isinstance(value, dict) else None


def _require_record_order(
    record: dict[str, Any],
    expected: tuple[str, ...],
    path: str,
    result: RuntimeControlParseResult,
) -> None:
    actual = tuple(record.keys())
    if actual != expected:
        result.errors.append(path + ' key order mismatch: expected ' + '/'.join(expected) + ' actual ' + '/'.join(actual))


def _require_exact(
    mapping: dict[str, Any],
    key: str,
    expected: Any,
    path: str,
    result: RuntimeControlParseResult,
) -> None:
    if mapping.get(key) != expected:
        result.errors.append(path + ' must be ' + repr(expected))


def _require_exact_string(
    mapping: dict[str, Any],
    key: str,
    path: str,
    result: RuntimeControlParseResult,
) -> None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value or value in {'unknown'}:
        result.errors.append(path + ' must be an exact non-empty string')


def _require_digest(value: Any, path: str, result: RuntimeControlParseResult) -> None:
    if not isinstance(value, str) or not SHA256_RE.match(value):
        result.errors.append(path + ' must be sha256:<64 lowercase hex>')


def _require_exact_list(
    mapping: dict[str, Any],
    key: str,
    expected: list[Any],
    path: str,
    result: RuntimeControlParseResult,
) -> None:
    if mapping.get(key) != expected:
        result.errors.append(path + ' must preserve canonical values/order')


def _require_string_list(
    mapping: dict[str, Any],
    key: str,
    path: str,
    result: RuntimeControlParseResult,
) -> list[str]:
    value = mapping.get(key)
    if not isinstance(value, list):
        result.errors.append(path + ' must be an array')
        return []
    if not all(isinstance(item, str) and item for item in value):
        result.errors.append(path + ' must contain exact non-empty strings')
        return [item for item in value if isinstance(item, str)]
    return value


def _validate_task_kinds(values: list[str], path: str, result: RuntimeControlParseResult) -> None:
    unknown = [item for item in values if item not in TASK_KINDS]
    if unknown:
        result.errors.append(path + ' contains unknown task kinds: ' + ','.join(unknown))


def _extract_scopes(text: str, marker: str) -> list[str]:
    normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = normalized.split('\n')
    starts = [index for index, line in enumerate(lines) if line.strip() == marker + ':']
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
            if index != start and stripped in {'K1:', 'PF1:'}:
                end = index
                break
        scopes.append('\n'.join(lines[start:end]).rstrip())
    return scopes
