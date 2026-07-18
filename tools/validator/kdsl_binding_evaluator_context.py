from __future__ import annotations

from datetime import datetime
from typing import Any


def completion(contract: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    profile = contract['PROFILE']
    normalization = contract['NORMALIZATION']['state']
    state = profile['completion']
    if normalization in {'lossy', 'blocked'} or state == 'blocked':
        state = 'blocked'
    return {
        'state': state,
        'completed_fields': list(profile['completed_fields']),
        'expansions': list(facts.get('expansions', [])),
        'unresolved': list(contract['NORMALIZATION']['unresolved']),
    }


def restrictions(contract: dict[str, Any], pf1: dict[str, Any]) -> dict[str, Any]:
    task_kind = contract['TASK']['kind']
    applied = []
    for record in pf1['RESTRICTIONS']:
        tasks = record['applies_to']['task_kinds']
        if not tasks or task_kind in tasks:
            applied.append({
                'id': record['id'],
                'source_revision': pf1['IDENTITY']['revision'],
                'source_digest': pf1['IDENTITY']['digest'],
                'effect': record['effect'],
                'rails': list(record['applies_to']['rails']),
                'task_kinds': list(tasks),
                'scope': record['scope'],
            })
    return {'state': 'applied', 'applied': applied, 'conflicts': []}


def capabilities(pf1: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    requirements = pf1['CAPABILITY_REQUIREMENTS']
    observations = facts.get('capability_observations', [])
    if not requirements:
        return {'state': 'not_required', 'requirements': [], 'observations': []}
    matched = []
    states = []
    evaluated_at = _time(facts.get('evaluated_at'))
    for requirement in requirements:
        candidate = next((item for item in observations if item.get('capability') == requirement['capability'] and item.get('scope') == requirement['scope']), None)
        if candidate is None:
            states.append('insufficient')
            continue
        matched.append(candidate)
        if candidate.get('state') != 'observed':
            states.append('unverified')
        elif candidate.get('current_state') != 'current' or _time(candidate.get('valid_until')) < evaluated_at:
            states.append('stale')
        else:
            states.append('sufficient')
    state = 'insufficient'
    if 'unverified' in states:
        state = 'unverified'
    elif 'stale' in states:
        state = 'stale'
    elif states and all(item == 'sufficient' for item in states):
        state = 'sufficient'
    return {'state': state, 'requirements': list(requirements), 'observations': matched}


def stop(facts: dict[str, Any]) -> dict[str, Any]:
    value = facts.get('stop')
    if not isinstance(value, dict):
        return {'state': 'blocked', 'rules_checked': [], 'matches': ['missing supplied Stop facts']}
    return {
        'state': value.get('state', 'blocked'),
        'rules_checked': list(value.get('rules_checked', [])),
        'matches': list(value.get('matches', [])),
    }


def preconditions(facts: dict[str, Any]) -> dict[str, Any]:
    value = facts.get('preconditions')
    if not isinstance(value, dict):
        return {'state': 'blocked', 'requirements': [], 'evidence': []}
    return {
        'state': value.get('state', 'blocked'),
        'requirements': list(value.get('requirements', [])),
        'evidence': list(value.get('evidence', [])),
    }


def _time(value: Any) -> datetime:
    if not isinstance(value, str):
        return datetime.min
    return datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=None)
