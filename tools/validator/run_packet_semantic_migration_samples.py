from __future__ import annotations

import ast
from pathlib import Path
from typing import Callable

from kdsl_packet_semantic import parse_packet, validate_packet_semantics

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE = REPO_ROOT / 'examples' / 'packet' / 'packet-semantic-property.example.md'
MODULE = ROOT / 'kdsl_packet_semantic.py'


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
    assert imported_symbols('kdsl_packet') == {
        'AUTHORITY_RAILS',
        'KNOWN_SG_IDS',
        'SG_REGISTRY',
        'load_text',
        'unquote',
    }


def check_packet_view_import_present() -> None:
    assert imported_symbols('kdsl_parser_v2_packet_compat') == {'PacketCompatibilityView'}


def check_return_contract_after_migration() -> None:
    data = parse_packet(read(SOURCE))
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
    assert data['values']['STATUS'] == 'non-executable'
    assert data['normalize']['state'] == 'not_normalized'
    assert [record.get('id') for record in data['sg_records']] == [
        'SG-SCOPE',
        'SG-EVIDENCE',
        'SG-RUNTIME',
        'SG-AUTHORITY',
        'SG-KDSL-DP',
        'SG-STOP',
    ]


def check_semantic_results_after_migration() -> None:
    source = read(SOURCE)
    errors, warnings, info = validate_packet_semantics(source)
    assert errors == []
    assert warnings == []
    assert 'Packet remains non-executable and not_normalized' in info

    mutated = source.replace('  state: not_normalized', '  state: normalized', 1)
    errors, _, _ = validate_packet_semantics(mutated)
    assert 'Packet semantic surface requires NORMALIZE.state:not_normalized' in errors


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('legacy Packet structural imports removed', check_legacy_structural_imports_removed),
    ('PacketCompatibilityView import present', check_packet_view_import_present),
    ('Packet semantic return contract retained', check_return_contract_after_migration),
    ('Packet semantic pass/fail results retained', check_semantic_results_after_migration),
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
