from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kdsl_p1_contract import ContractValueError, value_to_python
from kdsl_parser_v2 import DocumentNodeV2
from kdsl_runtime_control import AUTHORITY_RAILS, C14N_ID, SELF_DIGEST, SHA256_RE

SCHEMA_ID = 'kdsl-binding-evidence@0.1-draft'
STATUS = 'external-content-addressed-record'
FIELD_ORDER = (
    'SCHEMA', 'STATUS', 'IDENTITY', 'SUBJECT', 'RUNTIME_CONTROL', 'EVALUATION',
    'COMPLETION', 'RESTRICTIONS', 'AUTHORITY', 'APPROVALS', 'CAPABILITIES',
    'STOP', 'PRECONDITIONS', 'BINDING', 'PROVENANCE',
)
MAPPING_ORDER = {
    'IDENTITY': ('id', 'revision', 'canonicalization', 'digest', 'source_ref'),
    'SUBJECT': ('contract_schema', 'contract_id', 'contract_digest', 'project_id', 'repository', 'task_kind'),
    'RUNTIME_CONTROL': ('k1_ref', 'pf1_state', 'pf1_ref', 'compatibility_state'),
    'EVALUATION': ('evaluated_at', 'evaluator_ref', 'repository_state_ref', 'environment_state_ref'),
    'COMPLETION': ('state', 'completed_fields', 'expansions', 'unresolved'),
    'RESTRICTIONS': ('state', 'applied', 'conflicts'),
    'AUTHORITY': ('state', 'rails'),
    'APPROVALS': ('state', 'requirements', 'evidence'),
    'CAPABILITIES': ('state', 'requirements', 'observations'),
    'STOP': ('state', 'rules_checked', 'matches'),
    'PRECONDITIONS': ('state', 'requirements', 'evidence'),
    'BINDING': (
        'state', 'identity_state', 'profile_state', 'completion_state', 'restriction_state',
        'authority_state', 'capability_state', 'stop_state', 'precondition_state',
        'executable', 'semantic_equivalence', 'execution_authority',
    ),
    'PROVENANCE': ('generated_at', 'source_records', 'notes'),
}
REF_ORDER = ('id', 'revision', 'digest', 'source_ref')
EVALUATOR_REF_ORDER = ('id', 'revision', 'digest', 'immutable_ref')
RAIL_ORDER = (
    'requested', 'k1_disposition', 'pf1_mode', 'pf1_scope', 'pf1_cardinality',
    'approval_requirement', 'approval_evidence_id', 'targets', 'operation_instance',
    'effective_value', 'effective_scope', 'effective_cardinality', 'state',
)


@dataclass
class BindingEvidenceResult:
    model: dict[str, Any] | None = None
    computed_digest: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 2 if self.errors else (1 if self.warnings else 0)


def load_text(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8')


def parse_definition(text: str) -> BindingEvidenceResult:
    from kdsl_binding_evidence_records import validate_model

    result = BindingEvidenceResult()
    document = DocumentNodeV2.parse(text, context='raw-envelope')
    result.errors.extend(issue.format() for issue in document.errors)
    result.warnings.extend(issue.format() for issue in document.warnings)
    envelopes = document.envelopes('BINDING_EVIDENCE')
    if len(envelopes) != 1:
        result.errors.append(f'expected one BINDING_EVIDENCE envelope, found {len(envelopes)}')
        return result
    envelope = envelopes[0]
    actual = tuple(node.name for node in envelope.fields)
    if actual != FIELD_ORDER:
        result.errors.append('field order mismatch: expected ' + '/'.join(FIELD_ORDER) + ' actual ' + '/'.join(actual))
    model: dict[str, Any] = {}
    for node in envelope.fields:
        try:
            model[node.name] = value_to_python(node.value)
        except ContractValueError as exc:
            result.errors.append(f'{node.name}: {exc}')
    result.model = model
    validate_model(model, result)
    _validate_digest(model, result)
    if not result.errors:
        result.info.extend([
            'binding-evidence schema/order/type validation passed',
            'record remains non-executable and grants no execution authority',
        ])
    return result


def canonical_json(model: dict[str, Any]) -> str:
    normalized = copy.deepcopy(model)
    identity = normalized.get('IDENTITY')
    if not isinstance(identity, dict):
        raise ValueError('IDENTITY must be an object')
    identity['digest'] = SELF_DIGEST
    return json.dumps({'BINDING_EVIDENCE': normalized}, ensure_ascii=False, separators=(',', ':'), sort_keys=False)


def compute_digest(model: dict[str, Any]) -> str:
    return 'sha256:' + hashlib.sha256(canonical_json(model).encode('utf-8')).hexdigest()


def parse_reference(value: str) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    try:
        reference = json.loads(value)
    except json.JSONDecodeError as exc:
        return None, [f'runtime_control reference is not compact JSON: {exc.msg}']
    if not isinstance(reference, dict):
        return None, ['runtime_control reference must be a JSON object']
    expected = ('schema', 'id', 'revision', 'digest')
    if tuple(reference.keys()) != expected:
        errors.append('runtime_control reference key order mismatch')
    if reference.get('schema') != SCHEMA_ID:
        errors.append(f'runtime_control reference schema must be {SCHEMA_ID}')
    for key in ('id', 'revision'):
        if not isinstance(reference.get(key), str) or not reference[key]:
            errors.append(f'runtime_control reference {key} must be exact non-empty string')
    digest = reference.get('digest')
    if not isinstance(digest, str) or not SHA256_RE.match(digest):
        errors.append('runtime_control reference digest must be sha256:<64 lowercase hex>')
    if json.dumps(reference, ensure_ascii=False, separators=(',', ':'), sort_keys=False) != value:
        errors.append('runtime_control reference must use compact canonical JSON')
    return reference, errors


def match_reference(reference: dict[str, Any], model: dict[str, Any]) -> list[str]:
    identity = model.get('IDENTITY')
    if not isinstance(identity, dict):
        return ['IDENTITY is unavailable for reference matching']
    mismatches = [key for key in ('id', 'revision', 'digest') if reference.get(key) != identity.get(key)]
    return ['runtime_control reference mismatch: ' + ','.join(mismatches)] if mismatches else []


def _validate_digest(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    identity = model.get('IDENTITY')
    if not isinstance(identity, dict):
        return
    try:
        result.computed_digest = compute_digest(model)
    except (TypeError, ValueError) as exc:
        result.errors.append('canonical digest computation failed: ' + str(exc))
        return
    stored = identity.get('digest')
    if isinstance(stored, str) and SHA256_RE.match(stored) and stored != result.computed_digest:
        result.errors.append('IDENTITY.digest mismatch')


def emit(result: BindingEvidenceResult) -> int:
    print('BINDING_EVIDENCE_RESULT:')
    print('STATUS: ' + ('fail' if result.errors else ('warn' if result.warnings else 'pass')))
    print('SCHEMA: ' + str(result.model.get('SCHEMA') if result.model else 'none'))
    print('STORED_DIGEST: ' + str(result.model.get('IDENTITY', {}).get('digest') if result.model else 'none'))
    print('COMPUTED_DIGEST: ' + str(result.computed_digest or 'none'))
    print('EXECUTABLE: false')
    print('SEMANTIC_EQUIVALENCE: not_proven')
    print('EXECUTION_AUTHORITY: none')
    for label, items in (('ERRORS', result.errors), ('WARNINGS', result.warnings), ('INFO', result.info)):
        print(label + ':')
        for item in items or ['none']:
            print('  - ' + item)
    return result.exit_code
