from __future__ import annotations

import copy

from kdsl_binding_evaluator_cases_base import check
from kdsl_binding_evaluator_input import evaluate_inputs
from kdsl_binding_evaluator_sample_data import HEX_D, base_inputs, rebind
from run_runtime_control_samples import render_envelope


def observation(current_state: str = 'current', valid_until: str = '2026-07-19T00:00:00Z') -> dict:
    return {
        'id': 'obs-1',
        'revision': '0.1',
        'digest': HEX_D,
        'capability': 'repo-read',
        'state': 'observed',
        'scope': 'repository:tk999jp/kdsl-spec',
        'observed_at': '2026-07-17T23:30:00Z',
        'valid_until': valid_until,
        'environment_digest': HEX_D,
        'evidence_ref': 'generated:evaluator-corpus/capability',
        'invalidation': [],
        'current_state': current_state,
    }


def run_state_cases() -> list[bool]:
    results: list[bool] = []
    contract_text, k1_text, pf1_text, facts, contract, pf1 = base_inputs()

    changed_contract = copy.deepcopy(contract)
    changed_pf1 = copy.deepcopy(pf1)
    changed_facts = copy.deepcopy(facts)
    changed_pf1['CAPABILITY_REQUIREMENTS'] = [{
        'id': 'cap-1',
        'capability': 'repo-read',
        'task_kinds': ['review'],
        'scope': 'repository:tk999jp/kdsl-spec',
        'max_age_seconds': 3600,
        'required_state': 'observed',
        'invalidation': ['time_expired'],
    }]
    changed_text = rebind(changed_contract, changed_pf1)
    changed_pf1_text = render_envelope('PF1', changed_pf1)
    model, _, errors = evaluate_inputs(changed_text, k1_text, changed_pf1_text, changed_facts)
    check(results, 'missing capability is insufficient but bound', model is not None and not errors and model['CAPABILITIES']['state'] == 'insufficient' and model['BINDING']['state'] == 'bound')

    changed_facts['capability_observations'] = [observation(current_state='stale')]
    model, _, errors = evaluate_inputs(changed_text, k1_text, changed_pf1_text, changed_facts)
    check(results, 'stale capability remains bound', model is not None and not errors and model['CAPABILITIES']['state'] == 'stale' and model['BINDING']['state'] == 'bound')

    changed_facts['capability_observations'] = [observation()]
    model, _, errors = evaluate_inputs(changed_text, k1_text, changed_pf1_text, changed_facts)
    check(results, 'current capability becomes sufficient without authority effect', model is not None and not errors and model['CAPABILITIES']['state'] == 'sufficient' and model['AUTHORITY']['state'] == 'sufficient')

    changed_facts = copy.deepcopy(facts)
    changed_facts['stop']['state'] = 'active'
    model, _, errors = evaluate_inputs(contract_text, k1_text, pf1_text, changed_facts)
    check(results, 'active Stop remains bound', model is not None and not errors and model['STOP']['state'] == 'active' and model['BINDING']['state'] == 'bound')

    changed_facts['stop']['state'] = 'unknown'
    model, _, errors = evaluate_inputs(contract_text, k1_text, pf1_text, changed_facts)
    check(results, 'unknown Stop blocks binding', model is not None and not errors and model['BINDING']['state'] == 'blocked')

    changed_facts = copy.deepcopy(facts)
    changed_facts['preconditions']['state'] = 'unsatisfied'
    model, _, errors = evaluate_inputs(contract_text, k1_text, pf1_text, changed_facts)
    check(results, 'unsatisfied precondition remains bound', model is not None and not errors and model['BINDING']['state'] == 'bound')

    changed_facts['preconditions']['state'] = 'unknown'
    model, _, errors = evaluate_inputs(contract_text, k1_text, pf1_text, changed_facts)
    check(results, 'unknown precondition blocks binding', model is not None and not errors and model['BINDING']['state'] == 'blocked')
    return results
