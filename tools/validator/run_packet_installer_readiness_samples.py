from __future__ import annotations

from pathlib import Path
from typing import Callable

from kdsl_parser_adapter_inventory import classify

ROOT = Path(__file__).resolve().parent


def inventory():
    paths = sorted(ROOT.glob('*.py'))
    return classify(paths, ROOT, repository_mode=True)


def check_inventory_has_no_errors() -> None:
    result = inventory()
    assert result.errors == []


def check_direct_installer_boundary() -> None:
    result = inventory()
    records = [
        (record.path, record.module, record.symbols)
        for record in result.direct_adapter
    ]
    assert records == [
        ('kdsl_packet.py', 'kdsl_parser_adapter', ('install_packet',)),
    ]


def check_no_packet_legacy_structural_consumers() -> None:
    result = inventory()
    records = [
        (record.path, record.symbols)
        for record in result.legacy_consumers
        if record.module == 'kdsl_packet'
    ]
    assert records == []


def check_nonstructural_consumers_and_block_reason() -> None:
    result = inventory()
    packet_consumers = {
        record.path: set(record.symbols)
        for record in result.semantic_consumers
        if record.module == 'kdsl_packet'
    }
    assert packet_consumers['kdsl_packet_normalize.py'] == {'load_text', 'unquote'}
    assert packet_consumers['kdsl_packet_semantic.py'] == {
        'AUTHORITY_RAILS',
        'KNOWN_SG_IDS',
        'SG_REGISTRY',
        'load_text',
        'unquote',
    }
    assert result.retirement_blocked is True
    assert result.legacy_consumers == [] or all(
        record.module != 'kdsl_packet' for record in result.legacy_consumers
    )


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('repository adapter inventory has no errors', check_inventory_has_no_errors),
    ('Packet direct installer boundary is exact', check_direct_installer_boundary),
    ('Packet legacy structural consumers are absent', check_no_packet_legacy_structural_consumers),
    ('Packet nonstructural consumers are separated and installer still blocks retirement', check_nonstructural_consumers_and_block_reason),
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
        'BOUNDARY: readiness pass != installer removal/semantic equivalence/'
        'safety proof/adapter retirement/U approval/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
