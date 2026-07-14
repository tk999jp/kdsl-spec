from __future__ import annotations

from pathlib import Path
from typing import Callable

from kdsl_packet_semantic import parse_packet

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE = REPO_ROOT / 'examples' / 'packet' / 'packet-semantic-property.example.md'


def read() -> str:
    return SOURCE.read_text(encoding='utf-8')


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise AssertionError('mutation anchor not found: ' + old)
    return text.replace(old, new, 1)


def check_return_surface() -> None:
    data = parse_packet(read())
    assert set(data) == {
        'scope',
        'duplicates',
        'values',
        'blocks',
        'authority',
        'normalize',
        'obs',
        'stop',
        'verify',
        'sg_records',
        'flow_records',
    }
    assert data['values']['SCHEMA'] == 'kdsl-packet@0.1-draft'
    assert data['values']['STATUS'] == 'non-executable'


def check_scope_boundary() -> None:
    data = parse_packet(read())
    scope = data['scope']
    assert scope[0] == 'PACKET_DRAFT:'
    assert '```' not in scope
    nonblank = [line for line in scope if line.strip()]
    assert nonblank[-1] == '  state: not_normalized'


def check_sequence_order() -> None:
    data = parse_packet(read())
    assert data['obs'] == [
        'observed: duplicate entry appears after refresh',
        'inferred: cache invalidation may be involved',
        'unverified: root cause is not confirmed',
    ]
    assert data['stop'] == [
        'Unexpected diff outside TGT',
        'Root cause remains unconfirmed',
        'Required authority remains unavailable',
    ]
    assert data['verify'] == [
        'git diff --check',
        'relevant unit tests',
        'target runtime remains not_run',
    ]


def check_safety_gate_record_order() -> None:
    data = parse_packet(read())
    records = data['sg_records']
    assert [record.get('id') for record in records] == [
        'SG-SCOPE',
        'SG-EVIDENCE',
        'SG-RUNTIME',
        'SG-AUTHORITY',
        'SG-KDSL-DP',
        'SG-STOP',
    ]
    assert records[0]['state'] == 'hold'
    assert records[0]['scope'] == 'src/Example.cs'
    assert records[-1]['state'] == 'satisfied'
    assert records[-1]['evidence'] == 'STOP entries present'


def check_flow_record_order() -> None:
    data = parse_packet(read())
    records = data['flow_records']
    assert [record.get('op') for record in records] == [
        'FLOW-READ',
        'FLOW-ANALYZE',
        'FLOW-GATE',
        'FLOW-CHANGE',
        'FLOW-VERIFY',
        'FLOW-REPORT',
    ]
    assert records[3]['detail'] == (
        'Change exact TGT only after approved normalization and SG-AUTHORITY satisfaction'
    )


def check_authority_and_normalize_contract() -> None:
    data = parse_packet(read())
    assert data['authority'] == {
        'read': 'target_only',
        'edit': 'not_requested',
        'stage': 'not_requested',
        'commit': 'propose_only',
        'push': 'forbid',
        'release': 'forbid',
    }
    assert data['normalize'] == {
        'required': 'true',
        'target': 'full-kdsl-dev-prompt',
        'state': 'not_normalized',
    }


def check_top_level_duplicate_last_wins() -> None:
    text = replace_once(
        read(),
        'STATUS: non-executable\n',
        'STATUS: non-executable\nSTATUS: executable\n',
    )
    data = parse_packet(text)
    assert data['duplicates'] == ['STATUS']
    assert data['values']['STATUS'] == 'executable'


def check_nested_duplicate_last_wins() -> None:
    text = replace_once(
        read(),
        '  edit: not_requested\n',
        '  edit: not_requested\n  edit: allow\n',
    )
    data = parse_packet(text)
    assert data['authority']['edit'] == 'allow'


def check_boundary_mutations_are_not_coerced() -> None:
    text = read()
    text = replace_once(text, 'STATUS: non-executable', 'STATUS: executable')
    text = replace_once(text, '  state: not_normalized', '  state: normalized')
    text = replace_once(
        text,
        '  - "observed: duplicate entry appears after refresh"',
        '  - "duplicate entry appears after refresh"',
    )
    data = parse_packet(text)
    assert data['values']['STATUS'] == 'executable'
    assert data['normalize']['state'] == 'normalized'
    assert data['obs'][0] == 'duplicate entry appears after refresh'


def check_missing_envelope_contract() -> None:
    try:
        parse_packet('SCHEMA: kdsl-packet@0.1-draft\n')
    except ValueError as exc:
        assert str(exc) == 'PACKET_DRAFT block not found'
        return
    raise AssertionError('missing PACKET_DRAFT did not raise ValueError')


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('Packet semantic return surface', check_return_surface),
    ('Packet semantic scope boundary', check_scope_boundary),
    ('Packet semantic sequence order', check_sequence_order),
    ('Packet semantic Safety Gate record order', check_safety_gate_record_order),
    ('Packet semantic FLOW record order', check_flow_record_order),
    ('Packet semantic authority and normalize contract', check_authority_and_normalize_contract),
    ('Packet semantic top-level duplicate last-wins', check_top_level_duplicate_last_wins),
    ('Packet semantic nested duplicate last-wins', check_nested_duplicate_last_wins),
    ('Packet semantic boundary mutation extraction fidelity', check_boundary_mutations_are_not_coerced),
    ('Packet semantic missing-envelope error contract', check_missing_envelope_contract),
)


def main() -> int:
    failed = 0
    for name, case in CASES:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - corpus reports exact assertion/runtime failure
            failed += 1
            print('FAIL: ' + name)
            print('  ' + type(exc).__name__ + ': ' + str(exc))
        else:
            print('PASS: ' + name)

    print('SUMMARY:')
    print('  total: ' + str(len(CASES)))
    print('  failed: ' + str(failed))
    print(
        'BOUNDARY: contract pass != consumer migration/semantic equivalence/'
        'safety proof/Packet execution/adapter retirement/U approval/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
