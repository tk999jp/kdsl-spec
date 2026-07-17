from __future__ import annotations

import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from kdsl_parser_adapter_inventory import classify, find_python_files
from kdsl_parser_adapter_matrix import build_matrix

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
ADAPTER = ROOT / 'kdsl_parser_adapter.py'
INSTALLERS = {
    'install_r1c',
    'install_packet',
    'install_normalization',
    'install_safety_gate',
}


def imports_from(path: Path, module: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == module:
                    imported.add(alias.name)
    return imported


def loaded_installer_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in INSTALLERS:
            found.add(node.id)
        elif isinstance(node, ast.Attribute) and node.attr in INSTALLERS:
            found.add(node.attr)
    return found


def defined_functions(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def record(name: str, ok: bool, detail: str = '') -> bool:
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    if detail:
        print('  ' + detail)
    return ok


def repository_snapshot(tmp: Path) -> Path:
    target = tmp / 'validator-root'
    target.mkdir()
    for source in ROOT.glob('*.py'):
        shutil.copy2(source, target / source.name)
    return target


def main() -> int:
    results: list[bool] = []

    adapter_functions = defined_functions(ADAPTER)
    results.append(
        record(
            'adapter file exposes only the known installer functions',
            adapter_functions == INSTALLERS,
            'functions=' + repr(sorted(adapter_functions)),
        )
    )

    top_level_files = sorted(ROOT.glob('*.py'))
    direct_importers = {
        path.name: sorted(imports_from(path, 'kdsl_parser_adapter'))
        for path in top_level_files
        if path != ADAPTER and imports_from(path, 'kdsl_parser_adapter')
    }
    results.append(
        record(
            'no top-level validator module imports kdsl_parser_adapter',
            not direct_importers,
            'importers=' + repr(direct_importers),
        )
    )

    installer_consumers = {
        path.name: sorted(loaded_installer_names(path))
        for path in top_level_files
        if path != ADAPTER and loaded_installer_names(path)
    }
    results.append(
        record(
            'no installer function is loaded outside the adapter module',
            not installer_consumers,
            'consumers=' + repr(installer_consumers),
        )
    )

    parity_files = sorted(ROOT.glob('*parity.py'))
    parity_importers = {
        path.name: sorted(imports_from(path, 'kdsl_parser_adapter'))
        for path in parity_files
        if imports_from(path, 'kdsl_parser_adapter')
    }
    results.append(
        record(
            'parity modules are independent of kdsl_parser_adapter',
            len(parity_files) >= 5 and not parity_importers,
            'parity_files=' + repr([path.name for path in parity_files])
            + ' importers=' + repr(parity_importers),
        )
    )

    with tempfile.TemporaryDirectory() as raw_tmp:
        snapshot = repository_snapshot(Path(raw_tmp))
        paths, root, repository_mode = find_python_files(snapshot)
        inventory = classify(paths, root, repository_mode)
        matrix = build_matrix(inventory)

    results.append(
        record(
            'repository inventory has no direct or legacy structural consumers',
            not inventory.errors
            and not inventory.direct_adapter
            and not inventory.legacy_consumers
            and not inventory.retirement_blocked,
            'errors=' + repr(inventory.errors)
            + ' direct=' + repr(inventory.direct_adapter)
            + ' legacy=' + repr(inventory.legacy_consumers),
        )
    )

    decisions = {item.decision for item in matrix.records}
    results.append(
        record(
            'consumer matrix has no blocking record and retains semantic APIs only',
            not matrix.errors
            and not matrix.blocking_records
            and bool(matrix.records)
            and decisions <= {'retain-semantic-api'},
            'errors=' + repr(matrix.errors)
            + ' decisions=' + repr(sorted(decisions))
            + ' blocking=' + repr(matrix.blocking_records),
        )
    )

    modules = [
        'r1_required_blocks',
        'r1_rt_basis',
        'r1_authority_guard',
        'kdsl_compact_prompt',
        'kdsl_r1c',
        'kdsl_r1c_optional',
        'kdsl_safety_gate',
        'kdsl_safety_semantics',
        'kdsl_safety_gate_inheritance',
        'kdsl_safety_gate_graph',
        'kdsl_packet',
        'kdsl_packet_normalization',
        'kdsl_packet_normalize',
        'kdsl_packet_semantic',
        'kdsl_packet_roundtrip',
        'kdsl_packet_property',
    ]
    guarded_code = '''
import builtins
original_import = builtins.__import__
def guarded(name, *args, **kwargs):
    if name == "kdsl_parser_adapter" or name.startswith("kdsl_parser_adapter."):
        raise RuntimeError("adapter import denied: " + name)
    return original_import(name, *args, **kwargs)
builtins.__import__ = guarded
for module in MODULES:
    __import__(module)
print("adapter-deny import guard: pass")
'''
    proc = subprocess.run(
        [
            sys.executable,
            '-c',
            'MODULES=' + repr(modules) + '\n' + guarded_code,
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    results.append(
        record(
            'key runtime modules import while adapter imports are denied',
            proc.returncode == 0 and 'adapter-deny import guard: pass' in proc.stdout,
            'exit=' + str(proc.returncode)
            + ' stdout=' + repr(proc.stdout.strip())
            + ' stderr=' + repr(proc.stderr.strip()),
        )
    )

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    print('RETIREMENT:')
    print('  state: ' + ('blocked' if failed else 'bounded-removal-trial-candidate'))
    print(
        'BOUNDARY: readiness pass != adapter deletion/post-deletion proof/'
        'semantic equivalence/complete safety proof/U approval/RT:v/authority/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
