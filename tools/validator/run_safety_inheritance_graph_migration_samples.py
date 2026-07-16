from __future__ import annotations

import ast
import contextlib
import io
import json
import tempfile
from pathlib import Path

import kdsl_safety_gate_graph
import kdsl_safety_gate_inheritance

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


def run_main(fn, argv: list[str]) -> tuple[int, str]:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = fn(argv)
    return code, output.getvalue()


def gate_doc(entries: list[dict[str, str]]) -> str:
    lines = [
        'KDSL_PROMPT:',
        'format: KDSL',
        'profile: dev-prompt',
        'SAFETY_GATES:',
        '  registry: kdsl-sg@0.1-draft',
        '  entries:',
    ]
    for entry in entries:
        lines.append('    - id: ' + entry['id'])
        for key in ('state', 'scope', 'reason', 'evidence', 'authority'):
            lines.append('      ' + key + ': ' + entry.get(key, 'none'))
    return '\n'.join(lines) + '\n'


def entry(
    gate_id: str,
    state: str,
    *,
    scope: str = 'file A',
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


def write_graph(tmp: Path, nodes: dict[str, str], edges: list[list[str]]) -> Path:
    for node_id, text in nodes.items():
        (tmp / (node_id + '.md')).write_text(text, encoding='utf-8')
    manifest = {
        'nodes': [
            {'id': node_id, 'file': node_id + '.md'}
            for node_id in nodes
        ],
        'edges': edges,
    }
    path = tmp / 'graph.json'
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return path


def main() -> int:
    results: list[bool] = []

    migrated_files = (
        ROOT / 'kdsl_safety_gate_inheritance.py',
        ROOT / 'kdsl_safety_gate_graph.py',
    )
    import_ok = True
    import_detail: list[str] = []
    for path in migrated_files:
        gate_imports = imports_from(path, 'kdsl_safety_gate')
        compat_imports = imports_from(path, 'kdsl_parser_v2_safety_gate_compat')
        legacy_structural = gate_imports & {'extract_gate_block', 'parse_registry'}
        if legacy_structural or compat_imports != {'SafetyGateCompatibilityView'}:
            import_ok = False
        import_detail.append(
            path.name
            + ': legacy=' + repr(sorted(legacy_structural))
            + ' compat=' + repr(sorted(compat_imports))
        )
    results.append(
        record(
            'inheritance and graph structural imports migrated to CompatibilityView',
            import_ok,
            '; '.join(import_detail),
        )
    )

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        parent = tmp / 'parent.md'
        child = tmp / 'child.md'
        parent.write_text(
            gate_doc([entry('SG-EVIDENCE', 'hold', reason='pending evidence')]),
            encoding='utf-8',
        )
        child.write_text(
            gate_doc([entry('SG-EVIDENCE', 'hold', reason='still pending')]),
            encoding='utf-8',
        )
        code, output = run_main(
            kdsl_safety_gate_inheritance.main,
            ['kdsl_safety_gate_inheritance.py', str(parent), str(child)],
        )
    results.append(
        record(
            'inheritance hold state remains preserved',
            code == 0
            and 'STATUS: pass' in output
            and 'parent aggregate state: hold' in output
            and 'child aggregate state: hold' in output
            and 'inheritance does not grant execution authority' in output,
            'exit=' + str(code),
        )
    )

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        parent = tmp / 'parent.md'
        child = tmp / 'child.md'
        parent.write_text(
            gate_doc([entry('SG-AUTHORITY', 'hold', reason='pending approval')]),
            encoding='utf-8',
        )
        child.write_text(
            gate_doc(
                [
                    entry(
                        'SG-AUTHORITY',
                        'satisfied',
                        reason='confirmed',
                        evidence='none',
                        authority='none',
                    )
                ]
            ),
            encoding='utf-8',
        )
        code, output = run_main(
            kdsl_safety_gate_inheritance.main,
            ['kdsl_safety_gate_inheritance.py', str(parent), str(child)],
        )
    results.append(
        record(
            'inheritance hold to satisfied still requires evidence and authority',
            code == 2
            and 'STATUS: fail' in output
            and 'hold->satisfied requires evidence' in output
            and 'hold->satisfied requires verified authority or not_required' in output,
            'exit=' + str(code),
        )
    )

    repository_graph = REPO_ROOT / 'examples/safety-gates/multigeneration/graph.json'
    code, output = run_main(
        kdsl_safety_gate_graph.main,
        ['kdsl_safety_gate_graph.py', str(repository_graph)],
    )
    results.append(
        record(
            'repository multi-generation graph remains valid',
            code == 0
            and 'STATUS: pass' in output
            and 'topological order: phase0>phase1>phase2' in output
            and 'FULL_SAFETY_PROOF: not_proven' in output
            and 'EXECUTION_AUTHORITY: none' in output,
            'exit=' + str(code),
        )
    )

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        graph = write_graph(
            tmp,
            {
                'a': gate_doc([entry('SG-EVIDENCE', 'hold')]),
                'b': gate_doc([entry('SG-EVIDENCE', 'hold')]),
            },
            [['a', 'b'], ['b', 'a']],
        )
        code, output = run_main(
            kdsl_safety_gate_graph.main,
            ['kdsl_safety_gate_graph.py', str(graph)],
        )
    results.append(
        record(
            'inheritance graph cycle remains rejected',
            code == 2
            and 'STATUS: fail' in output
            and 'inheritance graph contains a cycle' in output
            and 'EXECUTION_AUTHORITY: none' in output,
            'exit=' + str(code),
        )
    )

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        graph = write_graph(
            tmp,
            {
                'parent': gate_doc([entry('SG-EVIDENCE', 'hold')]),
                'child': gate_doc([entry('SG-AUTHORITY', 'hold')]),
            },
            [['parent', 'child']],
        )
        code, output = run_main(
            kdsl_safety_gate_graph.main,
            ['kdsl_safety_gate_graph.py', str(graph)],
        )
    results.append(
        record(
            'graph missing inherited hold gate remains rejected',
            code == 2
            and 'STATUS: fail' in output
            and 'child/SG-EVIDENCE: inherited hold gate missing' in output
            and 'EXECUTION_AUTHORITY: none' in output,
            'exit=' + str(code),
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
