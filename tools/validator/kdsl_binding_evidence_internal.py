from __future__ import annotations

from typing import Any

from kdsl_binding_evidence_checks import digest, mapping, order
from kdsl_binding_evidence_core import BindingEvidenceResult

EXPANSION_ORDER = (
    'field_path', 'source_kind', 'source_id', 'source_revision', 'source_digest',
    'category', 'ordered', 'expanded_value_digest',
)
RESTRICTION_ORDER = (
    'id', 'source_revision', 'source_digest', 'effect', 'rails', 'task_kinds', 'scope',
)
SOURCE_ORDER = ('kind', 'id', 'revision', 'digest', 'source_ref')
SOURCE_KINDS = {
    'contract', 'k1', 'pf1', 'preset', 'alias', 'restriction', 'approval',
    'capability', 'stop', 'precondition', 'evaluator',
}


def validate_internal(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    _completion(model, result)
    _restrictions(model, result)
    _provenance(model, result)
    _binding_consistency(model, result)


def _completion(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    section = mapping(model, 'COMPLETION')
    if not section:
        return
    completed = section.get('completed_fields', [])
    expansions = section.get('expansions', [])
    for index, record in enumerate(expansions):
        path = f'COMPLETION.expansions[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        order(record, EXPANSION_ORDER, path, result)
        for key in ('field_path', 'source_id', 'source_revision'):
            if not isinstance(record.get(key), str) or not record[key]:
                result.errors.append(path + '.' + key + ' must be exact non-empty string')
        if record.get('source_kind') not in {'default', 'preset', 'alias'}:
            result.errors.append(path + '.source_kind is unknown')
        if record.get('category') not in {'guard', 'verify', 'stop', 'output', 'runtime', 'task', 'strategy', 'route'}:
            result.errors.append(path + '.category is unknown')
        if not isinstance(record.get('ordered'), bool):
            result.errors.append(path + '.ordered must be boolean')
        digest(record.get('source_digest'), path + '.source_digest', result)
        digest(record.get('expanded_value_digest'), path + '.expanded_value_digest', result)
    if section.get('state') == 'profile_completed':
        paths = {item.get('field_path') for item in expansions if isinstance(item, dict)}
        if not completed or any(item not in paths for item in completed):
            result.errors.append('profile_completed requires exact expansion for every completed field')


def _restrictions(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    section = mapping(model, 'RESTRICTIONS')
    if not section:
        return
    for index, record in enumerate(section.get('applied', [])):
        path = f'RESTRICTIONS.applied[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        order(record, RESTRICTION_ORDER, path, result)
        for key in ('id', 'source_revision', 'scope'):
            if not isinstance(record.get(key), str) or not record[key]:
                result.errors.append(path + '.' + key + ' must be exact non-empty string')
        digest(record.get('source_digest'), path + '.source_digest', result)
        if record.get('effect') not in {'forbid', 'approval_required', 'stop'}:
            result.errors.append(path + '.effect is unknown')
        for key in ('rails', 'task_kinds'):
            if not isinstance(record.get(key), list):
                result.errors.append(path + '.' + key + ' must be an array')
    conflicts = section.get('conflicts', [])
    if section.get('state') == 'applied' and conflicts:
        result.errors.append('RESTRICTIONS.applied cannot contain conflicts')
    if section.get('state') == 'conflict' and not conflicts:
        result.errors.append('RESTRICTIONS.conflict requires conflict evidence')


def _provenance(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    section = mapping(model, 'PROVENANCE')
    if not section:
        return
    records = section.get('source_records', [])
    identities = set()
    for index, record in enumerate(records):
        path = f'PROVENANCE.source_records[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        order(record, SOURCE_ORDER, path, result)
        if record.get('kind') not in SOURCE_KINDS:
            result.errors.append(path + '.kind is unknown')
        for key in ('id', 'revision', 'digest', 'source_ref'):
            if not isinstance(record.get(key), str) or not record[key]:
                result.errors.append(path + '.' + key + ' must be exact string or none')
        if record.get('digest') != 'none':
            digest(record.get('digest'), path + '.digest', result)
        identities.add((record.get('kind'), record.get('id')))
    for required in ('contract', 'k1', 'evaluator', 'stop', 'precondition'):
        if not any(kind == required for kind, _ in identities):
            result.errors.append('PROVENANCE missing required source kind: ' + required)
    runtime = mapping(model, 'RUNTIME_CONTROL')
    if runtime and runtime.get('pf1_state') == 'resolved' and not any(kind == 'pf1' for kind, _ in identities):
        result.errors.append('PROVENANCE missing PF1 source')
    for item in mapping(model, 'RESTRICTIONS').get('applied', []) if mapping(model, 'RESTRICTIONS') else []:
        if ('restriction', item.get('id')) not in identities:
            result.errors.append('PROVENANCE missing restriction source: ' + str(item.get('id')))


def _binding_consistency(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    binding = mapping(model, 'BINDING')
    if not binding:
        return
    pairs = {
        'completion_state': ('COMPLETION', 'state'),
        'restriction_state': ('RESTRICTIONS', 'state'),
        'authority_state': ('AUTHORITY', 'state'),
        'capability_state': ('CAPABILITIES', 'state'),
        'stop_state': ('STOP', 'state'),
        'precondition_state': ('PRECONDITIONS', 'state'),
    }
    for key, (section_name, state_key) in pairs.items():
        section = mapping(model, section_name)
        if section and binding.get(key) != section.get(state_key):
            result.errors.append('BINDING.' + key + ' does not match ' + section_name + '.state')
    runtime = mapping(model, 'RUNTIME_CONTROL')
    if runtime and binding.get('profile_state') != runtime.get('pf1_state'):
        result.errors.append('BINDING.profile_state does not match RUNTIME_CONTROL.pf1_state')
    if binding.get('state') == 'bound':
        if binding.get('identity_state') != 'resolved':
            result.errors.append('bound record requires resolved identity')
        if binding.get('completion_state') == 'blocked' or binding.get('restriction_state') != 'applied':
            result.errors.append('bound record contains completion/restriction conflict')
        if binding.get('capability_state') == 'blocked':
            result.errors.append('bound record contains blocked capability evidence')
        if binding.get('stop_state') in {'unknown', 'blocked'} or binding.get('precondition_state') in {'unknown', 'blocked'}:
            result.errors.append('bound record contains unknown critical Stop/precondition')
