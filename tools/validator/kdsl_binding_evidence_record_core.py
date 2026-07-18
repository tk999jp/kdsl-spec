from __future__ import annotations

from typing import Any

from kdsl_binding_evidence_checks import digest, evaluator_reference, mapping, nonempty, order, reference
from kdsl_binding_evidence_core import FIELD_ORDER, MAPPING_ORDER, SCHEMA_ID, STATUS, BindingEvidenceResult
from kdsl_binding_evidence_record_state import validate_state_sections
from kdsl_runtime_control import C14N_ID, SELF_DIGEST


def validate_model(model: dict[str, Any], result: BindingEvidenceResult) -> None:
    order(model, FIELD_ORDER, 'BINDING_EVIDENCE', result)
    if model.get('SCHEMA') != SCHEMA_ID:
        result.errors.append(f'SCHEMA must be {SCHEMA_ID}')
    if model.get('STATUS') != STATUS:
        result.errors.append(f'STATUS must be {STATUS}')
    for field_name, expected in MAPPING_ORDER.items():
        value = model.get(field_name)
        if not isinstance(value, dict):
            result.errors.append(field_name + ' must be an object')
        else:
            order(value, expected, field_name, result)

    identity = mapping(model, 'IDENTITY')
    if identity:
        nonempty(identity, ('id', 'revision', 'source_ref'), 'IDENTITY', result)
        if identity.get('canonicalization') != C14N_ID:
            result.errors.append(f'IDENTITY.canonicalization must be {C14N_ID}')
        digest(identity.get('digest'), 'IDENTITY.digest', result)
        if identity.get('digest') == SELF_DIGEST:
            result.errors.append('stored IDENTITY.digest must not be sha256:SELF')

    subject = mapping(model, 'SUBJECT')
    if subject:
        if subject.get('contract_schema') not in {'kdsl-p1l@0.1-draft', 'kdsl-p1@0.1-draft'}:
            result.errors.append('SUBJECT.contract_schema is unknown')
        nonempty(subject, ('contract_id', 'project_id', 'repository', 'task_kind'), 'SUBJECT', result)
        digest(subject.get('contract_digest'), 'SUBJECT.contract_digest', result)

    runtime = mapping(model, 'RUNTIME_CONTROL')
    if runtime:
        reference(runtime.get('k1_ref'), 'RUNTIME_CONTROL.k1_ref', False, result)
        pf1_state = runtime.get('pf1_state')
        if pf1_state not in {'resolved', 'not_applicable', 'blocked'}:
            result.errors.append('RUNTIME_CONTROL.pf1_state is unknown')
        reference(runtime.get('pf1_ref'), 'RUNTIME_CONTROL.pf1_ref', pf1_state == 'not_applicable', result)
        if runtime.get('compatibility_state') not in {'valid', 'blocked'}:
            result.errors.append('RUNTIME_CONTROL.compatibility_state is unknown')

    evaluation = mapping(model, 'EVALUATION')
    if evaluation:
        nonempty(evaluation, ('evaluated_at', 'repository_state_ref', 'environment_state_ref'), 'EVALUATION', result)
        evaluator_reference(evaluation.get('evaluator_ref'), 'EVALUATION.evaluator_ref', result)

    validate_state_sections(model, result)
