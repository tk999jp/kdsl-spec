from __future__ import annotations

import ast
from pathlib import Path
from typing import Callable

from kdsl_packet_normalize import collect_data

ROOT = Path(__file__).resolve().parent
VALID = ROOT / 'samples' / 'sample_packet_valid.md'
MODULE = ROOT / 'kdsl_packet_normalize.py'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def imported_symbols(module: str) -> set[str]:
    tree = ast.parse(read(MODULE), filename=str(MODULE))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            result.update(alias.name for alias in node.names)
    return result


def check_legacy_structural_imports_removed() -> None:
    assert imported_symbols('kdsl_packet') == {'load_text', 'unquote'}


def check_packet_view_import_present() -> None:
    assert imported_symbols('kdsl_parser_v2_packet_compat') == {'PacketCompatibilityView'}


def check_valid_contract_after_migration() -> None:
    data = collect_data(read(VALID))
    assert data['values']['SCHEMA'] == 'kdsl-packet@0.1-draft'
    assert data['values']['STATUS'] == 'non-executable'
    assert data['base_id'] == 'BASE-KDSL-DEV'
    assert data['task_id'] == 'TASK-CHANGE'
    assert data['src'] == ['repository: tk999jp/example']
    assert [record.get('id') for record in data['sg_records']] == [
        'SG-SCOPE',
        'SG-EVIDENCE',
        'SG-AUTHORITY',
        'SG-STOP',
    ]
    assert [record.get('op') for record in data['flow_records']] == [
        'FLOW-READ',
        'FLOW-ANALYZE',
        'FLOW-GATE',
        'FLOW-CHANGE',
        'FLOW-VERIFY',
        'FLOW-REPORT',
    ]
    assert data['authority']['edit'] == 'not_requested'
    assert data['normalize_target'] == 'full-kdsl-dev-prompt'


def check_missing_envelope_contract_after_migration() -> None:
    try:
        collect_data('SCHEMA: kdsl-packet@0.1-draft\n')
    except ValueError as exc:
        assert str(exc) == 'PACKET_DRAFT block not found'
        return
    raise AssertionError('missing PACKET_DRAFT did not raise ValueError')


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('legacy Packet structural imports removed', check_legacy_structural_imports_removed),
    ('PacketCompatibilityView import present', check_packet_view_import_present),
    ('valid Packet contract retained after migration', check_valid_contract_after_migration),
    ('missing Packet envelope contract retained after migration', check_missing_envelope_contract_after_migration),
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
        'BOUNDARY: migration pass != semantic equivalence/safety proof/'
        'Packet execution/adapter retirement/U approval/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
