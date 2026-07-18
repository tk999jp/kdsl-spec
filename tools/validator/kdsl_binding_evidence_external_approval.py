from __future__ import annotations

from datetime import datetime
from typing import Any

from kdsl_binding_evidence_checks import digest, mapping, order
from kdsl_binding_evidence_core import BindingEvidenceResult

APPROVAL_ORDER = (
    'id', 'revision', 'digest', 'source_ref', 'issuer', 'issued_at', 'operation',
    'scope', 'valid_until', 'revoked', 'content_state', 'trust_state', 'trust_policy_ref',
)


def validate_approvals(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    section = mapping(model, 'APPROVALS')
    if not section:
        return
    evidence = section.get('evidence')
    requirements = section.get('requirements')
    if not isinstance(evidence, list) or not isinstance(requirements, list):
        return
    for index, record in enumerate(evidence):
        path = f'APPROVALS.evidence[{index}]'
        if not isinstance(record, dict):
            result.errors.append(path + ' must be an object')
            continue
        order(record, APPROVAL_ORDER, path, result)
        for key in ('id', 'revision', 'source_ref', 'issuer', 'issued_at', 'operation', 'scope', 'valid_until', 'trust_policy_ref'):
            if not isinstance(record.get(key), str) or not record[key]:
                result.errors.append(path + '.' + key + ' must be exact non-empty string')
        digest(record.get('digest'), path + '.digest', result)
        if not isinstance(record.get('revoked'), bool):
            result.errors.append(path + '.revoked must be boolean')
        if record.get('content_state') not in {'valid', 'invalid', 'blocked'}:
            result.errors.append(path + '.content_state is unknown')
        if record.get('trust_state') not in {'verified', 'unverified', 'blocked'}:
            result.errors.append(path + '.trust_state is unknown')
        _timestamp(record.get('issued_at'), path + '.issued_at', False, result)
        _timestamp(record.get('valid_until'), path + '.valid_until', True, result)

    state = section.get('state')
    if state == 'not_required' and (requirements or evidence):
        result.errors.append('APPROVALS.not_required requires empty requirements/evidence')
    if state == 'sufficient' and any(
        item.get('content_state') != 'valid' or item.get('trust_state') != 'verified' or item.get('revoked')
        for item in evidence if isinstance(item, dict)
    ):
        result.errors.append('APPROVALS.sufficient contains unsatisfied evidence')
    if state == 'unverified' and evidence and not any(
        item.get('trust_state') == 'unverified' for item in evidence if isinstance(item, dict)
    ):
        result.errors.append('APPROVALS.unverified lacks unverified evidence')


def _timestamp(value: Any, path: str, allow_none: bool, result: BindingEvidenceResult) -> None:
    if allow_none and value == 'none':
        return
    if not isinstance(value, str):
        result.errors.append(path + ' must be UTC RFC3339 string')
        return
    try:
        datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        result.errors.append(path + ' must be UTC RFC3339 string')
