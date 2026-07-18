from __future__ import annotations

from typing import Any

from kdsl_binding_authority_rail import evaluate_rail
from kdsl_runtime_control import AUTHORITY_RAILS


def evaluate_authority(
    contract: dict[str, Any],
    pf1: dict[str, Any],
    restrictions: dict[str, Any],
    facts: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    rails: dict[str, Any] = {}
    requirements = []
    evidence = []
    approval_states = []
    conflicts = list(restrictions.get('conflicts', []))
    supplied = facts.get('approval_by_rail', {})
    instances = facts.get('operation_instances', {})

    for rail in AUTHORITY_RAILS:
        effects = {
            item['effect'] for item in restrictions.get('applied', [])
            if rail in item.get('rails', [])
        }
        record, approval, approval_state, rail_conflicts = evaluate_rail(
            contract,
            rail,
            pf1['AUTHORITY_CEILING'][rail],
            effects,
            supplied.get(rail),
            instances.get(rail, 'none'),
            facts['evaluated_at'],
        )
        rails[rail] = record
        conflicts.extend(rail_conflicts)
        if record['approval_requirement'] == 'required':
            requirements.append({
                'rail': rail,
                'operation': rail,
                'scope': _scope(record['targets']),
            })
            approval_states.append(approval_state)
            if approval is not None:
                evidence.append(approval)

    states = {item['state'] for item in rails.values()}
    if 'conflict' in states:
        authority_state = 'conflict'
    elif 'blocked' in states:
        authority_state = 'blocked'
    else:
        authority_state = 'sufficient'

    if not requirements:
        approval_state = 'not_required'
    elif 'conflict' in approval_states or 'blocked' in approval_states:
        approval_state = 'blocked'
    elif 'unverified' in approval_states:
        approval_state = 'unverified'
    elif 'missing' in approval_states:
        approval_state = 'insufficient'
    else:
        approval_state = 'sufficient'

    authority = {'state': authority_state, 'rails': rails}
    approvals = {'state': approval_state, 'requirements': requirements, 'evidence': evidence}
    return authority, approvals, conflicts


def _scope(targets: list[str]) -> str:
    from kdsl_binding_evaluator_approval import scope_text
    return scope_text(targets)
