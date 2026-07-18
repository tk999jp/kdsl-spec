from __future__ import annotations

from typing import Any

from kdsl_binding_evaluator_capability import evaluate_capabilities


def completion(contract: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    profile = contract['PROFILE']
    normalization = contract['NORMALIZATION']
    state = profile['completion']
    expansions = list(facts.get('expansions', []))
    completed_fields = list(profile['completed_fields'])
    if normalization['state'] in {'lossy', 'blocked'} or state == 'blocked':
        state = 'blocked'
    if state == 'profile_completed':
        expanded_paths = {item.get('field_path') for item in expansions if isinstance(item, dict)}
        if not completed_fields or any(field not in expanded_paths for field in completed_fields):
            state = 'blocked'
    return {
        'state': state,
        'completed_fields': completed_fields,
        'expansions': expansions,
        'unresolved': list(normalization['unresolved']),
    }


def restrictions(contract: dict[str, Any], pf1: dict[str, Any]) -> dict[str, Any]:
    task_kind = contract['TASK']['kind']
    exact_scopes = set(contract['SCOPE']['source'] + contract['SCOPE']['read'] + contract['SCOPE']['target'])
    exact_scopes.update({
        pf1['PROJECT']['id'],
        pf1['PROJECT']['repository'],
        'project:' + pf1['PROJECT']['id'],
        'repository:' + pf1['PROJECT']['repository'],
    })
    protected = set(contract['GUARD']['protected_wording'] + contract['GUARD']['constraints'] + contract['GUARD']['safety_gates'])
    applied = []
    conflicts = []
    for record in pf1['RESTRICTIONS']:
        tasks = record['applies_to']['task_kinds']
        if tasks and task_kind not in tasks:
            continue
        rails = list(record['applies_to']['rails'])
        scope = record['scope']
        if scope != 'any' and scope not in exact_scopes:
            conflicts.append(record['id'] + ':scope')
        if record['effect'] in {'forbid', 'approval_required'} and not rails:
            conflicts.append(record['id'] + ':rails')
        wording = record['protected_wording']
        if wording and wording not in protected:
            conflicts.append(record['id'] + ':protected_wording')
        applied.append({
            'id': record['id'],
            'source_revision': pf1['IDENTITY']['revision'],
            'source_digest': pf1['IDENTITY']['digest'],
            'effect': record['effect'],
            'rails': rails,
            'task_kinds': list(tasks),
            'scope': scope,
        })
    return {'state': 'conflict' if conflicts else 'applied', 'applied': applied, 'conflicts': conflicts}


def capabilities(contract: dict[str, Any], pf1: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    return evaluate_capabilities(contract, pf1, facts)


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
