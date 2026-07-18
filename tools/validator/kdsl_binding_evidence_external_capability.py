from __future__ import annotations

from datetime import datetime
from typing import Any

from kdsl_binding_evidence_checks import digest, mapping, order
from kdsl_binding_evidence_core import BindingEvidenceResult

REQUIREMENT_ORDER = ('id', 'capability', 'scope', 'max_age_seconds', 'required_state')
OBSERVATION_ORDER = (
    'id', 'revision', 'digest', 'capability', 'state', 'scope', 'observed_at',
    'valid_until', 'environment_digest', 'evidence_ref', 'invalidation', 'current_state',
)


def validate_capabilities(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    section = mapping(model, 'CAPABILITIES')
    if not section:
        return
    requirements = section.get('requirements')
    observations = section.get('observations')
    if not isinstance(requirements, list) or not isinstance(observations, list):
        return
    for index, record in enumerate(requirements):
        path = f'CAPABILITIES.requirements[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        order(record, REQUIREMENT_ORDER, path, result)
        for key in ('id', 'capability', 'scope'):
            if not isinstance(record.get(key), str) or not record[key]:
                result.errors.append(path + '.' + key + ' must be exact non-empty string')
        if not isinstance(record.get('max_age_seconds'), int) or record['max_age_seconds'] <= 0:
            result.errors.append(path + '.max_age_seconds must be positive integer')
        if record.get('required_state') != 'observed':
            result.errors.append(path + '.required_state must be observed')

    for index, record in enumerate(observations):
        path = f'CAPABILITIES.observations[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        order(record, OBSERVATION_ORDER, path, result)
        for key in ('id', 'revision', 'capability', 'scope', 'observed_at', 'valid_until', 'evidence_ref'):
            if not isinstance(record.get(key), str) or not record[key]:
                result.errors.append(path + '.' + key + ' must be exact non-empty string')
        digest(record.get('digest'), path + '.digest', result)
        digest(record.get('environment_digest'), path + '.environment_digest', result)
        if record.get('state') not in {'observed', 'inferred', 'unverified', 'not_available'}:
            result.errors.append(path + '.state is unknown')
        if record.get('current_state') not in {'current', 'stale', 'invalidated', 'blocked'}:
            result.errors.append(path + '.current_state is unknown')
        if not isinstance(record.get('invalidation'), list):
            result.errors.append(path + '.invalidation must be an array')
        _timestamp(record.get('observed_at'), path + '.observed_at', result)
        _timestamp(record.get('valid_until'), path + '.valid_until', result)

    state = section.get('state')
    if state == 'not_required' and (requirements or observations):
        result.errors.append('CAPABILITIES.not_required requires empty requirements/observations')
    if state == 'sufficient' and len(observations) < len(requirements):
        result.errors.append('CAPABILITIES.sufficient lacks matching observations')


def _timestamp(value: Any, path: str, result: BindingEvidenceResult) -> None:
    if not isinstance(value, str):
        result.errors.append(path + ' must be UTC RFC3339 string')
        return
    try:
        datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        result.errors.append(path + ' must be UTC RFC3339 string')
