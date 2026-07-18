from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from kdsl_p1_contract import parse_contract
from kdsl_runtime_control import compute_digest, parse_definition
from run_runtime_control_samples import build_pf1_model, render_envelope

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
P1L_SAMPLE = REPO / 'examples/adps/p1l-investigate.example.md'
K1_SAMPLE = REPO / 'examples/runtime/k1-canonical.example.md'
HEX_D = 'sha256:' + 'd' * 64


def base_inputs() -> tuple[str, str, str, dict[str, Any], dict[str, Any], dict[str, Any]]:
    k1_text = K1_SAMPLE.read_text(encoding='utf-8')
    k1 = parse_definition(k1_text, 'K1')
    if k1.model is None or k1.errors:
        raise RuntimeError('canonical K1 sample unavailable')
    pf1_model = build_pf1_model(k1.model)

    parsed = parse_contract(P1L_SAMPLE.read_text(encoding='utf-8'), expected='P1L')
    if parsed.model is None:
        raise RuntimeError('P1L sample unavailable')
    contract = copy.deepcopy(parsed.model)
    contract['PROFILE'] = {
        'id': pf1_model['IDENTITY']['id'],
        'revision': pf1_model['IDENTITY']['revision'],
        'digest': pf1_model['IDENTITY']['digest'],
        'completion': 'explicit',
        'completed_fields': [],
    }
    contract['TASK'] = {'kind': 'review', 'declared': 'review'}
    contract['SCOPE']['target'] = ['spec/runtime/kdsl-binding-evidence-schema.md']
    contract['SCOPE']['read'] = list(contract['SCOPE']['target'])
    contract['AUTHORITY'] = {
        'read': 'target_only',
        'edit': 'forbid',
        'stage': 'forbid',
        'commit': 'forbid',
        'push': 'forbid',
        'release': 'forbid',
        'public_repo': 'forbid',
        'destructive_ops': 'forbid',
    }
    contract['NORMALIZATION']['state'] = 'explicit'
    contract['BINDING'] = {'runtime_control': 'unresolved', 'state': 'unbound', 'executable': False}
    contract_text = render_envelope('P1L', contract)
    contract_digest = 'sha256:' + hashlib.sha256(
        json.dumps(contract, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    ).hexdigest()

    facts = {
        'record_id': 'kdsl.reference.binding.review',
        'record_revision': '0.1.0',
        'record_source_ref': 'generated:evaluator-corpus',
        'contract_digest': contract_digest,
        'contract_source_ref': 'generated:evaluator-corpus/contract',
        'evaluated_at': '2026-07-18T00:00:00Z',
        'evaluator_ref': {'id': 'kdsl.reference.evaluator', 'revision': '0.1.0', 'digest': HEX_D, 'immutable_ref': 'none'},
        'evaluator_source_ref': 'tools/validator/kdsl_binding_evaluator.py',
        'repository_state_ref': 'commit:031f11286526e77034da5d803e6b01bf0d61a60a',
        'environment_state_ref': 'none',
        'environment_digest': HEX_D,
        'stop': {
            'state': 'clear', 'rules_checked': [], 'matches': [],
            'source_record': {'kind': 'stop', 'id': 'stop-facts-1', 'revision': '0.1', 'digest': HEX_D, 'source_ref': 'generated:evaluator-corpus/stop'},
        },
        'preconditions': {
            'state': 'satisfied', 'requirements': [], 'evidence': [],
            'source_record': {'kind': 'precondition', 'id': 'precondition-facts-1', 'revision': '0.1', 'digest': HEX_D, 'source_ref': 'generated:evaluator-corpus/preconditions'},
        },
    }
    return contract_text, k1_text, render_envelope('PF1', pf1_model), facts, contract, pf1_model


def rebind(contract: dict[str, Any], pf1: dict[str, Any]) -> str:
    pf1['IDENTITY']['digest'] = compute_digest('PF1', pf1)
    contract['PROFILE']['digest'] = pf1['IDENTITY']['digest']
    return render_envelope('P1L', contract)
