from __future__ import annotations

from typing import Any

SOURCE_KINDS = {
    'contract', 'k1', 'pf1', 'preset', 'alias', 'restriction', 'approval',
    'capability', 'stop', 'precondition', 'evaluator',
}


def build_provenance(
    contract: dict[str, Any],
    k1: dict[str, Any],
    pf1: dict[str, Any],
    restrictions: dict[str, Any],
    approvals: dict[str, Any],
    capabilities: dict[str, Any],
    facts: dict[str, Any],
    conflicts: list[str],
) -> dict[str, Any]:
    records = [
        _source('contract', contract['META']['contract_id'], contract['META']['contract_rev'], facts['contract_digest'], facts['contract_source_ref']),
        _identity_source('k1', k1['IDENTITY']),
        _identity_source('pf1', pf1['IDENTITY']),
        _source(
            'evaluator',
            facts['evaluator_ref']['id'],
            facts['evaluator_ref']['revision'],
            facts['evaluator_ref'].get('digest', 'none'),
            facts['evaluator_source_ref'],
        ),
    ]
    for item in restrictions.get('applied', []):
        records.append(_source('restriction', item['id'], item['source_revision'], item['source_digest'], pf1['IDENTITY']['source_ref']))
    for item in approvals.get('evidence', []):
        records.append(_source('approval', item['id'], item['revision'], item['digest'], item['source_ref']))
    for item in capabilities.get('observations', []):
        records.append(_source('capability', item['id'], item['revision'], item['digest'], item['evidence_ref']))
    records.append(_normalize_source(facts['stop']['source_record'], 'stop'))
    records.append(_normalize_source(facts['preconditions']['source_record'], 'precondition'))
    for item in facts.get('source_records', []):
        records.append(_normalize_source(item, None))

    unique = []
    seen = set()
    for item in records:
        key = (item['kind'], item['id'], item['revision'], item['digest'], item['source_ref'])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    notes = list(facts.get('notes', []))
    notes.extend('binding_conflict:' + item for item in conflicts)
    return {'generated_at': facts['evaluated_at'], 'source_records': unique, 'notes': notes}


def _identity_source(kind: str, identity: dict[str, Any]) -> dict[str, Any]:
    return _source(kind, identity['id'], identity['revision'], identity['digest'], identity['source_ref'])


def _source(kind: str, source_id: str, revision: str, digest: str, source_ref: str) -> dict[str, Any]:
    return {'kind': kind, 'id': source_id, 'revision': revision, 'digest': digest, 'source_ref': source_ref}


def _normalize_source(value: Any, expected_kind: str | None) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError('source_record must be an object')
    kind = value.get('kind')
    if kind not in SOURCE_KINDS or (expected_kind is not None and kind != expected_kind):
        raise ValueError('source_record kind mismatch')
    return _source(kind, value['id'], value['revision'], value['digest'], value['source_ref'])
