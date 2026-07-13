from __future__ import annotations

from pathlib import Path
from typing import Callable

from kdsl_packet_normalize import collect_data

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
VALID = ROOT / 'samples' / 'sample_packet_valid.md'
FENCED = REPO_ROOT / 'examples' / 'packet' / 'packet-design.example.md'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def check_valid_scalars() -> None:
    data = collect_data(read(VALID))
    assert data['values']['SCHEMA'] == 'kdsl-packet@0.1-draft'
    assert data['values']['STATUS'] == 'non-executable'
    assert data['base_id'] == 'BASE-KDSL-DEV'
    assert data['task_id'] == 'TASK-CHANGE'
    assert data['goal'] == 'Apply the smallest safe correction'
    assert data['normalize_target'] == 'full-kdsl-dev-prompt'
    assert data['result_schema'] == 'kdsl-r1c@0.1-draft'


def check_sequence_order() -> None:
    data = collect_data(read(VALID))
    assert data['src'] == ['repository: tk999jp/example']
    assert data['read'] == ['src/Example.cs']
    assert data['tgt'] == ['src/Example.cs']
    assert data['obs'] == ['Duplicate entry observed']
    assert data['non'] == ['Broad refactor prohibited']
    assert data['stop'] == ['Unexpected diff']
    assert data['verify'] == ['git diff --check']


def check_safety_gate_order() -> None:
    data = collect_data(read(VALID))
    assert [record.get('id') for record in data['sg_records']] == [
        'SG-SCOPE',
        'SG-EVIDENCE',
        'SG-AUTHORITY',
        'SG-STOP',
    ]
    assert data['sg_records'][0]['state'] == 'hold'
    assert data['sg_records'][-1]['state'] == 'satisfied'


def check_flow_order() -> None:
    data = collect_data(read(VALID))
    assert [record.get('op') for record in data['flow_records']] == [
        'FLOW-READ',
        'FLOW-ANALYZE',
        'FLOW-GATE',
        'FLOW-CHANGE',
        'FLOW-VERIFY',
        'FLOW-REPORT',
    ]
    assert data['flow_records'][3]['detail'] == 'Change after normalization'


def check_authority_contract() -> None:
    data = collect_data(read(VALID))
    assert data['authority'] == {
        'read': 'target_only',
        'edit': 'not_requested',
        'stage': 'not_requested',
        'commit': 'propose_only',
        'push': 'forbid',
        'release': 'forbid',
    }


def check_fenced_repository_example() -> None:
    data = collect_data(read(FENCED))
    assert data['base_id'] == 'BASE-KDSL-DEV'
    assert data['task_id'] == 'TASK-CHANGE'
    assert data['src'] == ['repository: tk999jp/example', 'branch: main']
    assert data['read'] == ['src/Example.cs', 'tests/ExampleTests.cs']
    assert data['values']['STATUS'] == 'non-executable'


def check_missing_envelope() -> None:
    try:
        collect_data('SCHEMA: kdsl-packet@0.1-draft\n')
    except ValueError as exc:
        assert str(exc) == 'PACKET_DRAFT block not found'
        return
    raise AssertionError('missing PACKET_DRAFT did not raise ValueError')


def check_duplicate_nested_scalar_last_wins() -> None:
    text = read(VALID).replace(
        '  id: BASE-KDSL-DEV\n',
        '  id: BASE-KDSL-DEV\n  id: BASE-DESIGN-ONLY\n',
        1,
    )
    data = collect_data(text)
    assert data['base_id'] == 'BASE-DESIGN-ONLY'


def check_sequence_order_mutation() -> None:
    text = read(VALID).replace(
        'SRC:\n  - "repository: tk999jp/example"\n',
        'SRC:\n  - "first"\n  - "repository: tk999jp/example"\n  - "last"\n',
        1,
    )
    data = collect_data(text)
    assert data['src'] == ['first', 'repository: tk999jp/example', 'last']


def check_boundary_mutations_are_not_coerced() -> None:
    text = read(VALID)
    text = text.replace('STATUS: non-executable', 'STATUS: executable', 1)
    text = text.replace('  edit: not_requested', '  edit: allow', 1)
    text = text.replace('  target: full-kdsl-dev-prompt', '  target: P1L', 1)
    text = text.replace('  state: not_normalized', '  state: normalized', 1)
    data = collect_data(text)
    assert data['values']['STATUS'] == 'executable'
    assert data['authority']['edit'] == 'allow'
    assert data['normalize_target'] == 'P1L'


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('valid Packet scalar contract', check_valid_scalars),
    ('Packet sequence order contract', check_sequence_order),
    ('Safety Gate record order contract', check_safety_gate_order),
    ('FLOW record order contract', check_flow_order),
    ('Packet authority contract', check_authority_contract),
    ('fenced repository Packet contract', check_fenced_repository_example),
    ('missing Packet envelope error contract', check_missing_envelope),
    ('duplicate nested scalar last-wins contract', check_duplicate_nested_scalar_last_wins),
    ('Packet sequence mutation order contract', check_sequence_order_mutation),
    ('Packet boundary mutation extraction fidelity', check_boundary_mutations_are_not_coerced),
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
        'BOUNDARY: consumer contract pass != migration/semantic equivalence/'
        'safety proof/adapter retirement proof/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
