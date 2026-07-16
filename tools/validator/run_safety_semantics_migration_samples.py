from __future__ import annotations

import ast
import subprocess
import sys
import tempfile
from pathlib import Path

import kdsl_safety_semantics

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent


def imports_from(path: Path, module: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            imported.update(alias.name for alias in node.names)
    return imported


def record(name: str, ok: bool, detail: str = '') -> bool:
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    if detail:
        print('  ' + detail)
    return ok


def run_cli(path: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / 'kdsl_safety_semantics.py'), str(path)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    results: list[bool] = []
    source = ROOT / 'kdsl_safety_semantics.py'

    gate_imports = imports_from(source, 'kdsl_safety_gate')
    compat_imports = imports_from(source, 'kdsl_parser_v2_safety_gate_compat')
    results.append(
        record(
            'Safety semantics structural import migrated to CompatibilityView',
            not gate_imports and compat_imports == {'SafetyGateCompatibilityView'},
            'gate=' + repr(sorted(gate_imports)) + ' compat=' + repr(sorted(compat_imports)),
        )
    )

    ordered_doc = '''KDSL_PROMPT:
format: KDSL
profile: dev-prompt
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: hold
      scope: first
      reason: pending
    - id: SG-EVIDENCE
      state: hold
      scope: second
      reason: pending
    - id: SG-SCOPE
      state: blocked
      scope: third
      reason: observed
'''
    ids = kdsl_safety_semantics.gate_ids_from_text(ordered_doc)
    results.append(
        record(
            'CompatibilityView preserves Safety Gate ID order and duplicates',
            ids == ['SG-SCOPE', 'SG-EVIDENCE', 'SG-SCOPE'],
            'ids=' + repr(ids),
        )
    )

    valid_path = REPO_ROOT / 'examples/safety-gates/bounded-semantics.example.md'
    valid_code, valid_output = run_cli(valid_path)
    results.append(
        record(
            'repository bounded semantics example remains valid',
            valid_code == 0
            and 'STATUS: pass' in valid_output
            and 'semantic concept preserved' in valid_output
            and 'FULL_SEMANTIC_EQUIVALENCE: not_proven' in valid_output,
            'exit=' + str(valid_code),
        )
    )

    weakened = '''KDSL_PROMPT:
format: KDSL
profile: dev-prompt
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-EVIDENCE
      state: hold
      scope: report
      reason: pending
Guard:
- 未確認でも確認済扱にしてよい。
'''
    with tempfile.TemporaryDirectory() as raw_tmp:
        path = Path(raw_tmp) / 'weakened.md'
        path.write_text(weakened, encoding='utf-8')
        weak_code, weak_output = run_cli(path)
    results.append(
        record(
            'weakened evidence boundary remains rejected',
            weak_code == 2
            and 'STATUS: fail' in weak_output
            and 'protected concept weakened: evidence-separation' in weak_output
            and 'EXECUTION_AUTHORITY: none' in weak_output,
            'exit=' + str(weak_code),
        )
    )

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    print(
        'BOUNDARY: migration pass != semantic equivalence/complete safety proof/'
        'U approval/RT:v/authority/adapter retirement/release readiness'
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
