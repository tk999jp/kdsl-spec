from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path
from typing import Callable

import kdsl_packet_normalization as normalization

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
CHECKER = ROOT / 'kdsl_packet_normalization.py'
VALID = ROOT / 'samples' / 'sample_normalization_valid.md'
PROPERTY_SOURCE = REPO_ROOT / 'examples' / 'packet' / 'packet-semantic-property.example.md'


def run_script(script: str, args: list[str], expected: int, markers: tuple[str, ...]) -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / script), *args],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    assert proc.returncode == expected, proc.stdout + '\n' + proc.stderr
    for marker in markers:
        assert marker in proc.stdout, marker + ' not found in:\n' + proc.stdout


def check_direct_installer_removed() -> None:
    tree = ast.parse(CHECKER.read_text(encoding='utf-8'), filename=str(CHECKER))
    imports: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.setdefault(node.module, set()).update(alias.name for alias in node.names)
    assert 'kdsl_parser_adapter' not in imports


def check_local_parity_helpers_retained() -> None:
    for name in (
        'extract_scope',
        'parse_top_level',
        'blocks_from_entries',
        'parse_nested_scalars',
        'parse_list_records',
        'parse_nested_lists',
        'extract_multiline',
    ):
        assert callable(getattr(normalization, name, None)), name


def check_valid_checker_without_installer() -> None:
    run_script(
        'kdsl_packet_normalization.py',
        [str(VALID)],
        0,
        (
            'STATUS: pass',
            'Normalization parser parity guard: pass',
            'Normalization structural extraction: AST v2 compatibility view',
            'execution authority boundary checked',
        ),
    )


def check_property_path_without_installer() -> None:
    run_script(
        'kdsl_packet_property.py',
        [str(PROPERTY_SOURCE)],
        0,
        (
            'STATUS: property_pass',
            'EXECUTABLE: no',
            'SEMANTIC_EQUIVALENCE: not_proven',
            'EXECUTION_AUTHORITY: none',
        ),
    )


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('Normalization direct adapter installer removed', check_direct_installer_removed),
    ('Normalization local parity helpers retained', check_local_parity_helpers_retained),
    ('Normalization checker passes without installer', check_valid_checker_without_installer),
    ('Normalization property path passes without installer', check_property_path_without_installer),
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
        'BOUNDARY: installer removal pass != semantic equivalence/safety proof/'
        'adapter retirement proof/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
