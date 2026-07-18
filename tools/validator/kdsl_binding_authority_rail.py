from __future__ import annotations

from typing import Any

from kdsl_binding_evaluator_approval import classify_approval, rail_targets, scope_text

OPERATIONAL = {'allow', 'target_only', 'allow_once'}


def evaluate_rail(
    contract: dict[str, Any],
    rail: str,
    ceiling: dict[str, Any],
    restriction_effects: set[str],
    supplied_approval: Any,
    operation_instance: str,
    evaluated_at: str,
) -> tuple[dict[str, Any], dict[str, Any] | None, str, list[str]]:
    requested = contract['AUTHORITY'][rail]
    targets = rail_targets(contract, rail)
    mode = ceiling['mode']
    restriction_forbid = 'forbid' in restriction_effects
    approval_required = requested in OPERATIONAL and (
        mode == 'approval_required' or 'approval_required' in restriction_effects
    )
    approval, approval_state, approval_conflict = classify_approval(
        supplied_approval, rail, targets, evaluated_at
    )
    conflicts = ['approval:' + rail] if approval_conflict else []

    effective = requested
    state = 'sufficient'
    if requested == 'forbid':
        effective = 'forbid'
    elif requested == 'not_requested':
        effective = 'blocked' if mode == 'not_applicable_only' else 'not_requested'
    elif requested == 'not_applicable':
        effective = 'not_applicable'
    elif requested == 'propose_only':
        if restriction_forbid or mode == 'forbid':
            effective = 'forbid'
        elif mode == 'not_applicable_only':
            effective = 'blocked'
    elif restriction_forbid or mode == 'forbid':
        effective = 'forbid'
    elif mode == 'propose_only_max':
        effective = 'propose_only'
    elif mode == 'not_applicable_only':
        effective = 'blocked'
    elif approval_required and approval_state != 'accepted':
        effective = 'blocked'
        state = 'conflict' if approval_conflict else 'blocked'

    scoped = requested == 'target_only' or ceiling['scope'] == 'target_only'
    once = requested == 'allow_once' or ceiling['cardinality'] == 'once'
    if effective in OPERATIONAL and scoped and not targets:
        effective = 'blocked'
        state = 'blocked'
        conflicts.append('target:' + rail)
    if effective in OPERATIONAL and once and operation_instance == 'none':
        effective = 'blocked'
        state = 'blocked'
        conflicts.append('operation_instance:' + rail)
    if effective == 'blocked' and state == 'sufficient':
        state = 'blocked'

    active = effective in OPERATIONAL
    record = {
        'requested': requested,
        'k1_disposition': 'preserve',
        'pf1_mode': mode,
        'pf1_scope': ceiling['scope'],
        'pf1_cardinality': ceiling['cardinality'],
        'approval_requirement': 'required' if approval_required else 'not_required',
        'approval_evidence_id': approval['id'] if approval_required and approval_state == 'accepted' and approval else 'none',
        'targets': targets,
        'operation_instance': operation_instance,
        'effective_value': effective,
        'effective_scope': ('target_only' if scoped else 'any') if active else ('blocked' if effective == 'blocked' else 'none'),
        'effective_cardinality': ('once' if once else 'any') if active else ('blocked' if effective == 'blocked' else 'none'),
        'state': state,
    }
    requirement = {
        'rail': rail,
        'operation': rail,
        'scope': scope_text(targets),
    } if approval_required else None
    return record, approval, approval_state, conflicts
