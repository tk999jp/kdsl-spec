from __future__ import annotations

import json
from typing import Any

from kdsl_binding_evidence_core import C14N_ID, SCHEMA_ID, STATUS, compute_digest
from kdsl_binding_evaluator_authority import evaluate_authority
from kdsl_binding_evaluator_context import capabilities, completion, preconditions, restrictions, stop
from kdsl_binding_evaluator_provenance import build_provenance

ZERO_DIGEST = 'sha256:' + '0' * 64


def build_evidence(contract: dict[str, Any], contract_kind: str, k1: dict[str, Any], pf1: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    completion_record = completion(contract, facts)
    restriction_record = restrictions(contract, pf1)
    authority, approvals, binding_conflicts = evaluate_authority(contract, pf1, restriction_record, facts)
    capability_record = capabilities(contract, pf1, facts)
    stop_record = stop(facts)
    precondition_record = preconditions(facts)

    blocked = (
        completion_record['state'] == 'blocked'
        or restriction_record['state'] in {'conflict', 'blocked'}
        or capability_record['state'] == 'blocked'
        or stop_record['state'] in {'unknown', 'blocked'}
        or precondition_record['state'] in {'unknown', 'blocked'}
        or bool(binding_conflicts)
    )
    binding_state = 'blocked' if blocked else 'bound'
    contract_schema = 'kdsl-p1l@0.1-draft' if contract_kind == 'P1L' else 'kdsl-p1@0.1-draft'
    provenance = build_provenance(
        contract, k1, pf1, restriction_record, approvals, capability_record, facts, binding_conflicts
    )

    model = {
        'SCHEMA': SCHEMA_ID,
        'STATUS': STATUS,
        'IDENTITY': {
            'id': facts['record_id'],
            'revision': facts['record_revision'],
            'canonicalization': C14N_ID,
            'digest': ZERO_DIGEST,
            'source_ref': facts['record_source_ref'],
        },
        'SUBJECT': {
            'contract_schema': contract_schema,
            'contract_id': contract['META']['contract_id'],
            'contract_digest': facts['contract_digest'],
            'project_id': pf1['PROJECT']['id'],
            'repository': pf1['PROJECT']['repository'],
            'task_kind': contract['TASK']['kind'],
        },
        'RUNTIME_CONTROL': {
            'k1_ref': _reference(k1['IDENTITY']),
            'pf1_state': 'resolved',
            'pf1_ref': _reference(pf1['IDENTITY']),
            'compatibility_state': 'valid',
        },
        'EVALUATION': {
            'evaluated_at': facts['evaluated_at'],
            'evaluator_ref': facts['evaluator_ref'],
            'repository_state_ref': facts['repository_state_ref'],
            'environment_state_ref': facts.get('environment_state_ref', 'none'),
        },
        'COMPLETION': completion_record,
        'RESTRICTIONS': restriction_record,
        'AUTHORITY': authority,
        'APPROVALS': approvals,
        'CAPABILITIES': capability_record,
        'STOP': stop_record,
        'PRECONDITIONS': precondition_record,
        'BINDING': {
            'state': binding_state,
            'identity_state': 'resolved',
            'profile_state': 'resolved',
            'completion_state': completion_record['state'],
            'restriction_state': restriction_record['state'],
            'authority_state': authority['state'],
            'capability_state': capability_record['state'],
            'stop_state': stop_record['state'],
            'precondition_state': precondition_record['state'],
            'executable': False,
            'semantic_equivalence': 'not_proven',
            'execution_authority': 'none',
        },
        'PROVENANCE': provenance,
    }
    model['IDENTITY']['digest'] = compute_digest(model)
    return model


def compact_reference(model: dict[str, Any]) -> str:
    identity = model['IDENTITY']
    value = {'schema': SCHEMA_ID, 'id': identity['id'], 'revision': identity['revision'], 'digest': identity['digest']}
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=False)


def _reference(identity: dict[str, Any]) -> dict[str, Any]:
    return {key: identity[key] for key in ('id', 'revision', 'digest', 'source_ref')}
