from __future__ import annotations

import json
from typing import Any

from kdsl_binding_evidence_core import FIELD_ORDER, parse_definition as parse_evidence
from kdsl_binding_evaluator_model import build_evidence
from kdsl_p1_contract import parse_contract
from kdsl_runtime_control import SHA256_RE, parse_definition, resolve_runtime_control

REQUIRED_FACTS = (
    'record_id', 'record_revision', 'record_source_ref', 'contract_digest',
    'contract_source_ref', 'evaluated_at', 'evaluator_ref', 'evaluator_source_ref',
    'repository_state_ref', 'stop', 'preconditions',
)


def evaluate_inputs(contract_text: str, k1_text: str, pf1_text: str, facts: dict[str, Any]) -> tuple[dict[str, Any] | None, str, list[str]]:
    errors: list[str] = []
    contract = parse_contract(contract_text)
    k1 = parse_definition(k1_text, 'K1')
    pf1 = parse_definition(pf1_text, 'PF1')
    errors += ['contract: ' + item for item in contract.errors]
    errors += ['K1: ' + item for item in k1.errors]
    errors += ['PF1: ' + item for item in pf1.errors]
    if errors or contract.model is None or k1.model is None or pf1.model is None:
        return None, '', errors

    compatibility = resolve_runtime_control(k1, pf1)
    errors += ['runtime-control: ' + item for item in compatibility.errors]
    for key in REQUIRED_FACTS:
        if key not in facts:
            errors.append('facts missing required key: ' + key)
    digest = facts.get('contract_digest')
    if not isinstance(digest, str) or not SHA256_RE.match(digest):
        errors.append('facts.contract_digest must be sha256:<64 lowercase hex>')
    for key in ('stop', 'preconditions'):
        value = facts.get(key)
        if not isinstance(value, dict) or not isinstance(value.get('source_record'), dict):
            errors.append('facts.' + key + '.source_record is required')

    profile = contract.model['PROFILE']
    identity = pf1.model['IDENTITY']
    if any(profile.get(key) != identity.get(key) for key in ('id', 'revision', 'digest')):
        errors.append('contract PROFILE does not exactly match PF1 identity')
    task_kind = contract.model['TASK']['kind']
    applies = pf1.model['APPLIES_TO']
    if applies['task_kinds'] and task_kind not in applies['task_kinds']:
        errors.append('contract task kind is not included by PF1')
    if task_kind in applies['excluded_task_kinds']:
        errors.append('contract task kind is excluded by PF1')
    if contract.model['NORMALIZATION']['state'] in {'lossy', 'blocked'}:
        errors.append('lossy or blocked contract cannot enter binding evaluation')
    if errors:
        return None, '', errors

    try:
        model = build_evidence(contract.model, contract.kind or 'P1L', k1.model, pf1.model, facts)
    except (KeyError, TypeError, ValueError) as exc:
        return None, '', ['binding evidence generation blocked: ' + str(exc)]
    text = render(model)
    generated = parse_evidence(text)
    if generated.errors:
        return None, '', ['generated record: ' + item for item in generated.errors]
    return model, text, []


def render(model: dict[str, Any]) -> str:
    lines = ['BINDING_EVIDENCE:']
    for key in FIELD_ORDER:
        lines.append(key + ': ' + json.dumps(model[key], ensure_ascii=False, separators=(',', ':')))
    return '\n'.join(lines) + '\n'
