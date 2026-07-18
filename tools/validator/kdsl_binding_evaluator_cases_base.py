from __future__ import annotations

import copy

from kdsl_binding_evidence_core import match_reference, parse_reference
from kdsl_binding_evaluator_input import evaluate_inputs
from kdsl_binding_evaluator_model import compact_reference
from kdsl_binding_evaluator_sample_data import base_inputs, rebind
from run_runtime_control_samples import render_envelope


def check(results: list[bool], name: str, value: bool) -> None:
    results.append(bool(value))
    print(('PASS: ' if value else 'FAIL: ') + name)


def run_base_cases() -> list[bool]:
    results: list[bool] = []
    contract_text, k1_text, pf1_text, facts, contract, pf1 = base_inputs()
    model, _, errors = evaluate_inputs(contract_text, k1_text, pf1_text, facts)
    check(results, 'base evaluation generated', model is not None and not errors)
    if model is None:
        return results
    check(results, 'base binding is bound', model['BINDING']['state'] == 'bound')
    check(results, 'fixed non-executable boundary', model['BINDING']['executable'] is False and model['BINDING']['execution_authority'] == 'none')
    check(results, 'read remains target_only', model['AUTHORITY']['rails']['read']['effective_value'] == 'target_only')
    reference, ref_errors = parse_reference(compact_reference(model))
    check(results, 'generated compact reference matches', reference is not None and not ref_errors and not match_reference(reference, model))

    changed_contract = copy.deepcopy(contract)
    changed_contract['PROFILE']['digest'] = 'sha256:' + 'f' * 64
    _, _, errors = evaluate_inputs(render_envelope('P1L', changed_contract), k1_text, pf1_text, facts)
    check(results, 'profile mismatch blocked', bool(errors))

    changed_contract = copy.deepcopy(contract)
    changed_contract['NORMALIZATION']['state'] = 'lossy'
    _, _, errors = evaluate_inputs(render_envelope('P1L', changed_contract), k1_text, pf1_text, facts)
    check(results, 'lossy contract blocked', bool(errors))

    changed_contract = copy.deepcopy(contract)
    changed_pf1 = copy.deepcopy(pf1)
    changed_facts = copy.deepcopy(facts)
    changed_pf1['AUTHORITY_CEILING']['read']['mode'] = 'approval_required'
    changed_text = rebind(changed_contract, changed_pf1)
    changed_pf1_text = render_envelope('PF1', changed_pf1)
    model, _, errors = evaluate_inputs(changed_text, k1_text, changed_pf1_text, changed_facts)
    check(results, 'missing approval is insufficient but bound', model is not None and not errors and model['AUTHORITY']['state'] == 'insufficient' and model['BINDING']['state'] == 'bound')

    changed_facts['approval_by_rail'] = {'read': {'id': 'approval-1', 'content_state': 'valid', 'trust_state': 'verified'}}
    model, _, errors = evaluate_inputs(changed_text, k1_text, changed_pf1_text, changed_facts)
    check(results, 'supplied trusted approval satisfies rail', model is not None and not errors and model['AUTHORITY']['state'] == 'sufficient')
    return results
