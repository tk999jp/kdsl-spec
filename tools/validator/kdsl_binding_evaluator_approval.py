from __future__ import annotations

import copy
import json
from datetime import datetime
from typing import Any

from kdsl_runtime_control import SHA256_RE

APPROVAL_ORDER = (
    'id', 'revision', 'digest', 'source_ref', 'issuer', 'issued_at', 'operation',
    'scope', 'valid_until', 'revoked', 'content_state', 'trust_state', 'trust_policy_ref',
)


def rail_targets(contract: dict[str, Any], rail: str) -> list[str]:
    source = contract['SCOPE']['read'] if rail == 'read' else contract['SCOPE']['target']
    return list(source)


def scope_text(targets: list[str]) -> str:
    if not targets:
        return 'none'
    if len(targets) == 1:
        return targets[0]
    return json.dumps(targets, ensure_ascii=False, separators=(',', ':'))


def classify_approval(
    supplied: Any,
    rail: str,
    targets: list[str],
    evaluated_at: str,
) -> tuple[dict[str, Any] | None, str, bool]:
    if not isinstance(supplied, dict):
        return None, 'missing', False
    record = copy.deepcopy(supplied)
    structural = tuple(record.keys()) == APPROVAL_ORDER
    for key in ('id', 'revision', 'source_ref', 'issuer', 'issued_at', 'operation', 'scope', 'valid_until', 'trust_policy_ref'):
        structural = structural and isinstance(record.get(key), str) and bool(record[key])
    structural = structural and isinstance(record.get('digest'), str) and bool(SHA256_RE.match(record['digest']))
    structural = structural and isinstance(record.get('revoked'), bool)
    if not structural:
        record['content_state'] = 'blocked'
        return record, 'blocked', True

    operation_match = record['operation'] == rail
    scope_match = record['scope'] == scope_text(targets)
    if not operation_match or not scope_match:
        record['content_state'] = 'invalid'
        return record, 'conflict', True

    try:
        evaluation_time = _time(evaluated_at)
        issued_at = _time(record['issued_at'])
        valid_until = None if record['valid_until'] == 'none' else _time(record['valid_until'])
    except ValueError:
        record['content_state'] = 'invalid'
        return record, 'blocked', False

    time_valid = issued_at <= evaluation_time and (valid_until is None or valid_until >= evaluation_time)
    if record['revoked'] or not time_valid or record.get('content_state') != 'valid':
        record['content_state'] = 'invalid'
        return record, 'blocked', False
    if record.get('trust_state') != 'verified':
        return record, 'unverified', False
    return record, 'accepted', False


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=None)
