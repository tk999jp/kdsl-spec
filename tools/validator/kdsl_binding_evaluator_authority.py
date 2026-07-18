from __future__ import annotations

from typing import Any

from kdsl_runtime_control import AUTHORITY_RAILS

OPERATIONAL = {'allow', 'target_only', 'allow_once'}


def evaluate_authority(contract: dict[str, Any], pf1: dict[str, Any], facts: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rails: dict[str, Any] = {}
    approval_by_rail = facts.get('approval_by_rail', {})
    operation_instances = facts.get('operation_instances', {})
    targets = contract['SCOPE']['target']
    required_approvals = []
    accepted_approvals = []

    for rail in AUTHORITY_RAILS:
        requested = contract['AUTHORITY'][rail]
        ceiling = pf1['AUTHORITY_CEILING'][rail]
        mode = ceiling['mode']
        approval = approval_by_rail.get(rail)
        approval_required = mode == 'approval_required' and requested in OPERATIONAL
        approval_ok = isinstance(approval, dict) and approval.get('content_state') == 'valid' and approval.get('trust_state') == 'verified'
        if approval_required:
            required_approvals.append({'rail': rail, 'operation': rail, 'scope': targets})
            if approval_ok:
                accepted_approvals.append(approval)

        effective = requested
        rail_state = 'sufficient'
        if requested == 'forbid':
            effective = 'forbid'
        elif requested == 'not_requested':
            effective = 'blocked' if mode == 'not_applicable_only' else 'not_requested'
        elif requested == 'not_applicable':
            effective = 'not_applicable'
        elif requested == 'propose_only':
            effective = 'forbid' if mode == 'forbid' else ('blocked' if mode == 'not_applicable_only' else 'propose_only')
        elif mode == 'propose_only_max':
            effective = 'propose_only'
        elif mode == 'forbid':
            effective = 'forbid'
        elif mode == 'not_applicable_only':
            effective = 'blocked'
        elif mode == 'approval_required' and not approval_ok:
            effective = 'blocked'
            rail_state = 'insufficient'

        scoped = requested == 'target_only' or ceiling['scope'] == 'target_only'
        once = requested == 'allow_once' or ceiling['cardinality'] == 'once'
        operation_instance = operation_instances.get(rail, 'none')
        if effective in OPERATIONAL and scoped and not targets:
            effective = 'blocked'
            rail_state = 'blocked'
        if effective in OPERATIONAL and once and operation_instance == 'none':
            effective = 'blocked'
            rail_state = 'blocked'
        if effective == 'blocked' and rail_state == 'sufficient':
            rail_state = 'blocked'

        active = effective in OPERATIONAL
        rails[rail] = {
            'requested': requested,
            'k1_disposition': 'preserve',
            'pf1_mode': mode,
            'pf1_scope': ceiling['scope'],
            'pf1_cardinality': ceiling['cardinality'],
            'approval_requirement': 'required' if approval_required else 'not_required',
            'approval_evidence_id': approval.get('id', 'none') if approval_ok else 'none',
            'targets': list(targets),
            'operation_instance': operation_instance,
            'effective_value': effective,
            'effective_scope': ('target_only' if scoped else 'any') if active else ('blocked' if effective == 'blocked' else 'none'),
            'effective_cardinality': ('once' if once else 'any') if active else ('blocked' if effective == 'blocked' else 'none'),
            'state': rail_state,
        }

    states = {item['state'] for item in rails.values()}
    authority_state = 'blocked' if 'blocked' in states else ('insufficient' if 'insufficient' in states else 'sufficient')
    approval_state = 'not_required' if not required_approvals else ('sufficient' if len(accepted_approvals) == len(required_approvals) else 'insufficient')
    return {'state': authority_state, 'rails': rails}, {'state': approval_state, 'requirements': required_approvals, 'evidence': accepted_approvals}
