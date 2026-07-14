from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path
from typing import Callable

from kdsl_parser_adapter_inventory import classify

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
PACKET = ROOT / 'kdsl_packet.py'
VALID = ROOT / 'samples' / 'sample_packet_valid.md'
SEMANTIC = REPO_ROOT / 'examples' / 'packet' / 'packet-semantic-property.example.md'


def run(script: str, target: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(ROOT / script)]
    if target is not None:
        command.append(str(target))
    return subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )


def check_packet_installer_import_and_call_absent() -> None:
    tree = ast.parse(PACKET.read_text(encoding='utf-8'), filename=str(PACKET))
    adapter_imports: list[tuple[str, ...]] = []
    installer_calls = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == 'kdsl_parser_adapter':
            adapter_imports.append(tuple(alias.name for alias in node.names))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'install_packet':
            installer_calls += 1
    assert adapter_imports == []
    assert installer_calls == 0


def check_repository_inventory_has_no_direct_installer() -> None:
    paths = sorted(ROOT.glob('*.py'))
    result = classify(paths, ROOT, repository_mode=True)
    assert result.errors == []
    assert result.direct_adapter == []
    assert [record for record in result.legacy_consumers if record.module == 'kdsl_packet'] == []


def check_packet_base_checker_after_removal() -> None:
    proc = run('kdsl_packet.py', VALID)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert 'STATUS: pass' in proc.stdout
    assert 'Packet parser parity guard: pass' in proc.stdout
    assert 'Packet structural extraction: AST v2 compatibility view' in proc.stdout
    assert 'non-executable normalization boundary checked' in proc.stdout


def check_packet_consumer_and_property_paths_after_removal() -> None:
    normalize = run('kdsl_packet_normalize.py', VALID)
    assert normalize.returncode == 0, normalize.stdout + normalize.stderr
    assert 'NORMALIZATION_DRAFT:' in normalize.stdout
    assert 'STATUS: non-executable' in normalize.stdout
    assert 'execution_authority: none' in normalize.stdout

    semantic = run('kdsl_packet_semantic.py', SEMANTIC)
    assert semantic.returncode == 0, semantic.stdout + semantic.stderr
    assert 'PACKET_SEMANTIC_RESULT:' in semantic.stdout
    assert 'STATUS: pass' in semantic.stdout
    assert 'EXECUTION_AUTHORITY: none' in semantic.stdout

    prop = run('run_packet_semantic_property_samples.py')
    assert prop.returncode == 0, prop.stdout + prop.stderr
    assert 'failed: 0' in prop.stdout


CASES: tuple[tuple[str, Callable[[], None]], ...] = (
    ('Packet adapter installer import and call are absent', check_packet_installer_import_and_call_absent),
    ('repository inventory has no direct adapter installer', check_repository_inventory_has_no_direct_installer),
    ('Packet base checker remains valid after installer removal', check_packet_base_checker_after_removal),
    ('Packet normalize semantic and property paths remain valid', check_packet_consumer_and_property_paths_after_removal),
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
        'BOUNDARY: removal pass != semantic equivalence/safety proof/'
        'adapter file retirement/U approval/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
