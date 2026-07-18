from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from kdsl_runtime_control import SHA256_RE

OBSERVATION_ORDER = (
    'id', 'revision', 'digest', 'capability', 'state', 'scope', 'observed_at',
    'valid_until', 'environment_digest', 'evidence_ref', 'invalidation', 'current_state',
)


def evaluate_capabilities(
    contract: dict[str, Any],
    pf1: dict[str, Any],
    facts: dict[str, Any],
) -> dict[str, Any]:
    task_kind = contract['TASK']['kind']
    requirements = [
        item for item in pf1['CAPABILITY_REQUIREMENTS']
        if not item['task_kinds'] or task_kind in item['task_kinds']
    ]
    if not requirements:
        return {'state': 'not_required', 'requirements': [], 'observations': []}

    observations = facts.get('capability_observations', [])
    evaluated_at = _time(facts.get('evaluated_at'))
    environment_digest = facts.get('environment_digest')
    matched: list[dict[str, Any]] = []
    states: list[str] = []

    for requirement in requirements:
        candidate = next(
            (
                item for item in observations
                if item.get('capability') == requirement['capability']
                and item.get('scope') == requirement['scope']
            ),
            None,
        )
        if candidate is None:
            states.append('insufficient')
            continue
        matched.append(candidate)
        states.append(_classify(candidate, requirement, evaluated_at, environment_digest))

    if 'blocked' in states:
        state = 'blocked'
    elif 'unverified' in states:
        state = 'unverified'
    elif 'stale' in states:
        state = 'stale'
    elif 'insufficient' in states:
        state = 'insufficient'
    else:
        state = 'sufficient'
    return {'state': state, 'requirements': requirements, 'observations': matched}


def _classify(
    record: dict[str, Any],
    requirement: dict[str, Any],
    evaluated_at: datetime,
    current_environment_digest: Any,
) -> str:
    if tuple(record.keys()) != OBSERVATION_ORDER:
        return 'blocked'
    for key in ('id', 'revision', 'capability', 'scope', 'observed_at', 'valid_until', 'evidence_ref', 'current_state'):
        if not isinstance(record.get(key), str) or not record[key]:
            return 'blocked'
    for key in ('digest', 'environment_digest'):
        value = record.get(key)
        if not isinstance(value, str) or not SHA256_RE.match(value):
            return 'blocked'
    if not isinstance(record.get('invalidation'), list):
        return 'blocked'
    if record['state'] in {'inferred', 'unverified'}:
        return 'unverified'
    if record['state'] == 'not_available':
        return 'insufficient'
    if record['state'] != 'observed':
        return 'blocked'
    if record['current_state'] == 'blocked':
        return 'blocked'
    if record['current_state'] in {'stale', 'invalidated'} or record['invalidation']:
        return 'stale'
    try:
        observed_at = _time(record['observed_at'])
        valid_until = _time(record['valid_until'])
    except ValueError:
        return 'blocked'
    if observed_at + timedelta(seconds=requirement['max_age_seconds']) < evaluated_at:
        return 'stale'
    if valid_until < evaluated_at:
        return 'stale'
    if not isinstance(current_environment_digest, str) or current_environment_digest != record['environment_digest']:
        return 'stale'
    return 'sufficient'


def _time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError('timestamp must be string')
    return datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=None)
