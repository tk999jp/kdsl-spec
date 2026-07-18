from __future__ import annotations

from typing import Any

from kdsl_binding_evidence_checks import list_fields, mapping, order, rail, state
from kdsl_binding_evidence_core import BindingEvidenceResult
from kdsl_runtime_control import AUTHORITY_RAILS


def validate_state_sections(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    state(model, 'COMPLETION', {'explicit', 'profile_completed', 'blocked'}, result)
    state(model, 'RESTRICTIONS', {'applied', 'conflict', 'blocked'}, result)
    state(model, 'APPROVALS', {'sufficient', 'insufficient', 'unverified', 'not_required', 'blocked'}, result)
    state(model, 'CAPABILITIES', {'sufficient', 'insufficient', 'stale', 'unverified', 'not_required', 'blocked'}, result)
    state(model, 'STOP', {'clear', 'active', 'unknown', 'blocked'}, result)
    state(model, 'PRECONDITIONS', {'satisfied', 'unsatisfied', 'unknown', 'blocked'}, result)

    authority = mapping(model, 'AUTHORITY')
    if authority:
        if authority.get('state') not in {'sufficient', 'insufficient', 'conflict', 'blocked'}:
            result.errors.append('AUTHORITY.state is unknown')
        rails = authority.get('rails')
        if not isinstance(rails, dict):
            result.errors.append('AUTHORITY.rails must be an object')
        else:
            order(rails, tuple(AUTHORITY_RAILS), 'AUTHORITY.rails', result)
            for rail_name in AUTHORITY_RAILS:
                rail(rails.get(rail_name), 'AUTHORITY.rails.' + rail_name, result)

    binding = mapping(model, 'BINDING')
    if binding:
        fixed = {'executable': False, 'semantic_equivalence': 'not_proven', 'execution_authority': 'none'}
        for key, expected in fixed.items():
            if binding.get(key) != expected:
                result.errors.append('BINDING.' + key + ' must be ' + repr(expected))
        if binding.get('state') not in {'unbound', 'bound', 'blocked'}:
            result.errors.append('BINDING.state is unknown')

    list_fields(model, ('COMPLETION', 'RESTRICTIONS', 'APPROVALS', 'CAPABILITIES', 'STOP', 'PRECONDITIONS', 'PROVENANCE'), result)
