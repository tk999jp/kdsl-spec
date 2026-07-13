from __future__ import annotations

import ast
from pathlib import Path
from typing import Callable

from kdsl_packet_roundtrip import parse_normalization

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
ROUNDTRIP = ROOT / 'kdsl_packet_roundtrip.py'
VALID = ROOT / 'samples' / 'sample_normalization_valid.md'
BLOCKED = REPO_ROOT / 'examples' / 'packet' / 'normalization-p1-blocked.example.md'


def check_import_boundary() -> None:
    tree = ast.parse(ROUNDTRIP.read_text(encoding='utf-8'), filename=str(ROUNDTRIP))
    imports: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.setdefault(node.module, set()).update(alias.name for alias in node.names)

    assert 'kdsl_packet_normalization' not in imports
    assert imports.get('kdsl_parser_v2_normalization_compat') == {
        'NormalizationCompatibilityView'
    }


def check_valid_contract_after_migration() -> None:
    parsed = parse_normalization(VALID.read_text(encoding='utf-8'))
    assert parsed['values']['STATUS'] == 'non-executable'
    assert parsed['target']['executable'] == 'false'
    assert parsed['round_trip']['semantic_equivalence'] == 'not_proven'
    assert parsed['authority']['execution_authority'] == 'none'
    assert parsed['output']['executable'] == 'false'
    assert len(parsed['map_records']) == 17
    assert parsed['preview'].startswith('KDSL_PROMPT_PREVIEW:')


def check_blocked_contract_after_migration() -> None:
    parsed = parse_normalization(BLOCKED.read_text(encoding='utf-8'))
    assert parsed['target']['kind'] == 'P1'
    assert parsed['target']['resolution'] == 'blocked'
    assert parsed['target']['executable'] == 'false'
    assert parsed['round_trip']['semantic_equivalence'] == 'not_proven'
    assert parsed['authority']['execution_authority'] == 'none'
    assert parsed['output']['marker'] == 'none'
    assert parsed['preview'] == ''
    assert parsed['unresolved'][0]['impact'] == 'blocked'


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('legacy Normalization structural import removed', check_import_boundary),
    ('valid Normalization contract retained after migration', check_valid_contract_after_migration),
    ('blocked P1 contract retained after migration', check_blocked_contract_after_migration),
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
        'adapter retirement proof/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
