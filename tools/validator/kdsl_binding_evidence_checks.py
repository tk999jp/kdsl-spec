from __future__ import annotations

from typing import Any

from kdsl_binding_evidence_core import EVALUATOR_REF_ORDER, RAIL_ORDER, REF_ORDER, BindingEvidenceResult
from kdsl_runtime_control import SHA256_RE


def mapping(model: dict[str, Any], field_name: str) -> dict[str, Any] | None:
    value = model.get(field_name)
    return value if isinstance(value, dict) else None


def order(value: dict[str, Any], expected: tuple[str, ...], path: str, result: BindingEvidenceResult) -> None:
    actual = tuple(value.keys())
    if actual != expected:
        result.errors.append(path + ' key order mismatch: expected ' + '/'.join(expected) + ' actual ' + '/'.join(actual))


def nonempty(value: dict[str, Any], keys: tuple[str, ...], path: str, result: BindingEvidenceResult) -> None:
    for key in keys:
        if not isinstance(value.get(key), str) or not value[key]:
            result.errors.append(path + '.' + key + ' must be an exact non-empty string')


def digest(value: Any, path: str, result: BindingEvidenceResult) -> None:
    if not isinstance(value, str) or not SHA256_RE.match(value):
        result.errors.append(path + ' must be sha256:<64 lowercase hex>')


def reference(value: Any, path: str, allow_none: bool, result: BindingEvidenceResult) -> None:
    if not isinstance(value, dict):
        result.errors.append(path + ' must be an object')
        return
    order(value, REF_ORDER, path, result)
    if allow_none and all(value.get(key) == 'none' for key in REF_ORDER):
        return
    nonempty(value, ('id', 'revision', 'source_ref'), path, result)
    digest(value.get('digest'), path + '.digest', result)


def evaluator_reference(value: Any, path: str, result: BindingEvidenceResult) -> None:
    if not isinstance(value, dict):
        result.errors.append(path + ' must be an object')
        return
    order(value, EVALUATOR_REF_ORDER, path, result)
    nonempty(value, ('id', 'revision'), path, result)
    digest_value = value.get('digest')
    immutable_ref = value.get('immutable_ref')
    if digest_value == 'none' and immutable_ref == 'none':
        result.errors.append(path + ' requires digest or immutable_ref')
    if digest_value != 'none':
        digest(digest_value, path + '.digest', result)
    if not isinstance(immutable_ref, str) or not immutable_ref:
        result.errors.append(path + '.immutable_ref must be exact string or none')


def state(model: dict[str, Any], field_name: str, allowed: set[str], result: BindingEvidenceResult) -> None:
    value = mapping(model, field_name)
    if value and value.get('state') not in allowed:
        result.errors.append(field_name + '.state is unknown')


def list_fields(model: dict[str, Any], fields: tuple[str, ...], result: BindingEvidenceResult) -> None:
    for field_name in fields:
        value = mapping(model, field_name)
        if value:
            for key, item in value.items():
                if key not in {'state', 'generated_at'} and not isinstance(item, list):
                    result.errors.append(f'{field_name}.{key} must be an array')


def rail(value: Any, path: str, result: BindingEvidenceResult) -> None:
    if not isinstance(value, dict):
        result.errors.append(path + ' must be an object')
        return
    order(value, RAIL_ORDER, path, result)
    allowed = {
        'requested': {'allow', 'forbid', 'target_only', 'allow_once', 'propose_only', 'not_requested', 'not_applicable'},
        'k1_disposition': {'preserve', 'forbid', 'blocked'},
        'pf1_mode': {'allow_max', 'propose_only_max', 'forbid', 'approval_required', 'not_applicable_only'},
        'pf1_scope': {'any', 'target_only'},
        'pf1_cardinality': {'any', 'once'},
        'approval_requirement': {'required', 'not_required'},
        'effective_value': {'allow', 'forbid', 'target_only', 'allow_once', 'propose_only', 'not_requested', 'not_applicable', 'blocked'},
        'effective_scope': {'any', 'target_only', 'none', 'blocked'},
        'effective_cardinality': {'any', 'once', 'none', 'blocked'},
        'state': {'sufficient', 'insufficient', 'conflict', 'blocked'},
    }
    for key, values in allowed.items():
        if value.get(key) not in values:
            result.errors.append(path + '.' + key + ' is unknown')
    if not isinstance(value.get('targets'), list):
        result.errors.append(path + '.targets must be an array')
    for key in ('approval_evidence_id', 'operation_instance'):
        if not isinstance(value.get(key), str) or not value[key]:
            result.errors.append(path + '.' + key + ' must be exact string or none')
