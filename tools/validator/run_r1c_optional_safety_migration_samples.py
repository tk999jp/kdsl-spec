from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import kdsl_r1c_optional

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


def safety_value(entries: list[dict[str, str]]) -> str:
    lines = [
        'registry: kdsl-sg@0.1-draft',
        'entries:',
    ]
    for entry in entries:
        lines.append('  - id: ' + entry['id'])
        for key in ('state', 'scope', 'reason', 'evidence', 'authority'):
            if key in entry:
                lines.append('    ' + key + ': ' + entry[key])
    return '\n'.join(lines)


def entry(
    gate_id: str,
    state: str,
    *,
    scope: str = 'target',
    reason: str = 'pending',
    evidence: str = 'none',
    authority: str = 'none',
) -> dict[str, str]:
    return {
        'id': gate_id,
        'state': state,
        'scope': scope,
        'reason': reason,
        'evidence': evidence,
        'authority': authority,
    }


def main() -> int:
    results: list[bool] = []
    source = ROOT / 'kdsl_r1c_optional.py'

    gate_imports = imports_from(source, 'kdsl_safety_gate')
    compat_imports = imports_from(source, 'kdsl_parser_v2_safety_gate_compat')
    results.append(
        record(
            'R1C optional Safety Gate parsing migrated to CompatibilityView',
            'parse_registry' not in gate_imports
            and compat_imports == {'SafetyGateCompatibilityView'},
            'gate=' + repr(sorted(gate_imports)) + ' compat=' + repr(sorted(compat_imports)),
        )
    )

    valid_entries = [
        entry('SG-EVIDENCE', 'hold', scope='evidence', reason='not proven'),
        entry(
            'SG-AUTHORITY',
            'satisfied',
            scope='proposal only',
            reason='confirmed',
            evidence='authority record verified',
            authority='not_required',
        ),
    ]
    model = kdsl_r1c_optional.parse_safety_gates_model(safety_value(valid_entries))
    expected_order = [
        ['id', 'state', 'scope', 'reason', 'evidence', 'authority'],
        ['id', 'state', 'scope', 'reason', 'evidence', 'authority'],
    ]
    results.append(
        record(
            'CompatibilityView preserves R1C optional model shape and field order',
            model['registry'] == 'kdsl-sg@0.1-draft'
            and model['entries'] == valid_entries
            and model['entry_field_order'] == expected_order,
            'model=' + repr(model),
        )
    )

    duplicate_entries = [
        entry('SG-EVIDENCE', 'hold', scope='first'),
        entry('SG-EVIDENCE', 'blocked', scope='second', evidence='observed'),
    ]
    duplicate_model = kdsl_r1c_optional.parse_safety_gates_model(
        safety_value(duplicate_entries)
    )
    results.append(
        record(
            'CompatibilityView preserves duplicate entry order for semantic rejection',
            [item.get('id') for item in duplicate_model['entries']]
            == ['SG-EVIDENCE', 'SG-EVIDENCE']
            and [item.get('scope') for item in duplicate_model['entries']]
            == ['first', 'second'],
            'entries=' + repr(duplicate_model['entries']),
        )
    )

    example = REPO_ROOT / 'examples/r1c/r1c-deep-optional.example.md'
    proc = subprocess.run(
        [sys.executable, str(source), str(example)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    results.append(
        record(
            'repository deep optional example remains valid',
            proc.returncode == 0
            and 'STATUS: pass' in proc.stdout
            and 'optional SAFETY_GATES deep lint checked' in proc.stdout
            and 'SEMANTIC_EQUIVALENCE: not_proven' in proc.stdout
            and 'EXECUTION_AUTHORITY: none' in proc.stdout,
            'exit=' + str(proc.returncode),
        )
    )

    unknown_errors: list[str] = []
    unknown_warnings: list[str] = []
    kdsl_r1c_optional.validate_safety_gates(
        safety_value([entry('SG-EVIDENCE', 'pending')]),
        unknown_errors,
        unknown_warnings,
    )
    results.append(
        record(
            'unknown Safety Gate state remains rejected',
            any('unknown Safety Gate state: pending' in item for item in unknown_errors),
            'errors=' + repr(unknown_errors),
        )
    )

    basis_errors: list[str] = []
    basis_warnings: list[str] = []
    missing_basis_entry = entry(
        'SG-AUTHORITY',
        'satisfied',
        reason='confirmed',
        evidence='',
        authority='none',
    )
    kdsl_r1c_optional.validate_safety_gates(
        safety_value([missing_basis_entry]),
        basis_errors,
        basis_warnings,
    )
    results.append(
        record(
            'satisfied gate still requires evidence and verified authority',
            any('state:satisfied requires evidence' in item for item in basis_errors)
            and any(
                'state:satisfied requires verified authority or not_required' in item
                for item in basis_errors
            ),
            'errors=' + repr(basis_errors),
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
