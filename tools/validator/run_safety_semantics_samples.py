import contextlib
import io
import json
import tempfile
from pathlib import Path

import kdsl_safety_gate_graph
import kdsl_safety_semantics


def gate_doc(gate_id, state='hold', scope='file A', reason='pending', evidence='none', authority='none', guard=''):
    return f'''KDSL_PROMPT:
format: KDSL
profile: dev-prompt
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: {gate_id}
      state: {state}
      scope: {scope}
      reason: {reason}
      evidence: {evidence}
      authority: {authority}
Guard:
- {guard}
'''


def plain_gate(entries):
    out = 'SAFETY_GATES:\n  registry: kdsl-sg@0.1-draft\n  entries:\n'
    for entry in entries:
        out += f"    - id: {entry['id']}\n"
        for key in ('state', 'scope', 'reason', 'evidence', 'authority'):
            out += f"      {key}: {entry.get(key, 'none')}\n"
    return out


def run_main(fn, argv):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = fn(argv)
    return code, output.getvalue()


SEMANTIC_CASES = [
    ('design valid', 'SG-DESIGN', '未承認の設計変更は実装指示禁止。設計変更はU承認必須。', 0, 'semantic concept preserved'),
    ('design weakened', 'SG-DESIGN', '承認がなくても設計変更と実装が可能。', 2, 'protected concept weakened'),
    ('evidence valid', 'SG-EVIDENCE', '未確認を確認済扱禁止。観測/推論/未確認を分離する。', 0, 'semantic concept preserved'),
    ('evidence weakened', 'SG-EVIDENCE', '未確認でも確認済扱にしてよい。', 2, 'protected concept weakened'),
    ('runtime valid', 'SG-RUNTIME', 'RT:vは対象環境runtime確認済のみ。build/diff/lint/test/CI pass != RT:v。', 0, 'semantic concept preserved'),
    ('runtime weakened', 'SG-RUNTIME', 'CI passならRT:vとしてよい。', 2, 'protected concept weakened'),
    ('authority valid', 'SG-AUTHORITY', 'NEXTは実行許可扱禁止。COMMITは自動commit許可扱禁止。', 0, 'semantic concept preserved'),
    ('authority weakened', 'SG-AUTHORITY', 'NEXT提案は実行許可として扱う。', 2, 'protected concept weakened'),
    ('kdsl dp valid', 'SG-KDSL-DP', 'KDSL-DP直接実行禁止。P1/P1L正規化必須。', 0, 'semantic concept preserved'),
    ('kdsl dp weakened', 'SG-KDSL-DP', 'KDSL-DPは直接実行可能。P1/P1L正規化は不要。', 2, 'protected concept weakened'),
    ('public valid', 'SG-PUBLIC', 'public履歴改竄禁止。公開済tag移動禁止。Release Assets上書禁止。', 0, 'semantic concept preserved'),
    ('data valid', 'SG-DATA', 'data保護を優先し、backupとrollbackによる復旧を必須とする。', 0, 'semantic concept preserved'),
    ('scope valid', 'SG-SCOPE', '原因未確の広域修正禁止。対象/非対象を明示する。', 0, 'semantic concept preserved'),
    ('scope weakened', 'SG-SCOPE', '原因未確でも広域修正可能。', 2, 'protected concept weakened'),
    ('rollback valid', 'SG-ROLLBACK', 'rollback前にgit statusとdiffを確認し、patch退避とverifyを行う。', 0, 'semantic concept preserved'),
    ('rollback weakened', 'SG-ROLLBACK', 'rollbackは確認不要で即時実行可能。', 2, 'protected concept weakened'),
]


def entry(gate_id, state, scope, reason, evidence='none', authority='none'):
    return dict(id=gate_id, state=state, scope=scope, reason=reason, evidence=evidence, authority=authority)


GRAPH_CASES = [
    (
        'linear hold preserved',
        {
            'p': plain_gate([entry('SG-EVIDENCE', 'hold', 'report', 'pending')]),
            'c': plain_gate([entry('SG-EVIDENCE', 'hold', 'report', 'still pending')]),
            'g': plain_gate([entry('SG-EVIDENCE', 'hold', 'report', 'still pending')]),
        },
        [['p', 'c'], ['c', 'g']],
        0,
        'topological order',
    ),
    (
        'grandchild missing inherited hold',
        {
            'p': plain_gate([entry('SG-EVIDENCE', 'hold', 'report', 'pending')]),
            'c': plain_gate([entry('SG-EVIDENCE', 'hold', 'report', 'still pending')]),
            'g': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A', 'confirmed', 'verified', 'not_required')]),
        },
        [['p', 'c'], ['c', 'g']],
        2,
        'inherited hold gate missing',
    ),
    (
        'blocked chain preserved',
        {
            'p': plain_gate([entry('SG-STOP', 'blocked', 'preflight', 'mismatch', 'diff', 'none')]),
            'c': plain_gate([entry('SG-STOP', 'blocked', 'preflight', 'mismatch remains', 'diff', 'none')]),
            'g': plain_gate([entry('SG-STOP', 'blocked', 'preflight', 'mismatch remains', 'diff', 'none')]),
        },
        [['p', 'c'], ['c', 'g']],
        0,
        'aggregate state: blocked',
    ),
    (
        'blocked downgrade missing resolution',
        {
            'p': plain_gate([entry('SG-STOP', 'blocked', 'preflight', 'mismatch', 'diff', 'none')]),
            'c': plain_gate([entry('SG-STOP', 'satisfied', 'preflight', 'ready', 'new record', 'not_required')]),
        },
        [['p', 'c']],
        2,
        'requires explicit resolution evidence',
    ),
    (
        'blocked hold satisfied chain',
        {
            'p': plain_gate([entry('SG-STOP', 'blocked', 'preflight', 'mismatch', 'diff', 'none')]),
            'c': plain_gate([entry('SG-STOP', 'hold', 'preflight', 'cause resolved; re-evaluation pending', 'resolution verified', 'none')]),
            'g': plain_gate([entry('SG-STOP', 'satisfied', 'preflight', 're-evaluated and confirmed', 'verified record', 'not_required')]),
        },
        [['p', 'c'], ['c', 'g']],
        0,
        'topological order',
    ),
    (
        'cycle rejected',
        {
            'p': plain_gate([entry('SG-STOP', 'hold', 'x', 'pending')]),
            'c': plain_gate([entry('SG-STOP', 'hold', 'x', 'pending')]),
        },
        [['p', 'c'], ['c', 'p']],
        2,
        'contains a cycle',
    ),
    (
        'unknown node rejected',
        {'p': plain_gate([entry('SG-STOP', 'hold', 'x', 'pending')])},
        [['p', 'missing']],
        2,
        'unknown node',
    ),
    (
        'multi parent blocked conflict rejected',
        {
            'p1': plain_gate([entry('SG-AUTHORITY', 'blocked', 'commit', 'denied', 'record', 'none')]),
            'p2': plain_gate([entry('SG-AUTHORITY', 'satisfied', 'commit', 'confirmed', 'record', 'allow_once')]),
            'c': plain_gate([entry('SG-AUTHORITY', 'satisfied', 'commit', 'confirmed', 'record', 'allow_once')]),
        },
        [['p1', 'c'], ['p2', 'c']],
        2,
        'blocked->satisfied requires explicit resolution evidence',
    ),
    (
        'multi parent blocked child preserved',
        {
            'p1': plain_gate([entry('SG-AUTHORITY', 'blocked', 'commit', 'denied', 'record', 'none')]),
            'p2': plain_gate([entry('SG-AUTHORITY', 'satisfied', 'commit', 'confirmed', 'record', 'allow_once')]),
            'c': plain_gate([entry('SG-AUTHORITY', 'blocked', 'commit', 'denial remains', 'record', 'none')]),
        },
        [['p1', 'c'], ['p2', 'c']],
        0,
        'aggregate state: blocked',
    ),
    (
        'satisfied widened without reevaluation',
        {
            'p': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A', 'confirmed', 'verified', 'not_required')]),
            'c': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A and file B', 'confirmed', 'verified', 'not_required')]),
        },
        [['p', 'c']],
        2,
        'explicit re-evaluation required',
    ),
    (
        'satisfied widened with reevaluation',
        {
            'p': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A', 'confirmed', 'verified', 'not_required')]),
            'c': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A and file B', 'scope re-evaluated and confirmed', 'new scope verified', 'not_required')]),
        },
        [['p', 'c']],
        0,
        'scope widened re-evaluated',
    ),
    (
        'satisfied narrowed',
        {
            'p': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A and file B', 'confirmed', 'verified', 'not_required')]),
            'c': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A', 'confirmed', 'verified', 'not_required')]),
        },
        [['p', 'c']],
        0,
        'scope narrowed',
    ),
    (
        'satisfied disjoint without reevaluation',
        {
            'p': plain_gate([entry('SG-SCOPE', 'satisfied', 'file A', 'confirmed', 'verified', 'not_required')]),
            'c': plain_gate([entry('SG-SCOPE', 'satisfied', 'file C', 'confirmed', 'verified', 'not_required')]),
        },
        [['p', 'c']],
        2,
        'scope disjoint',
    ),
    (
        'parent na copied warning',
        {
            'p': plain_gate([entry('SG-PUBLIC', 'na', 'local docs', 'no public operation', 'none', 'not_required')]),
            'c': plain_gate([entry('SG-PUBLIC', 'na', 'local docs', 'no public operation', 'none', 'not_required')]),
        },
        [['p', 'c']],
        1,
        'independently re-evaluated',
    ),
    (
        'aggregate blocked reported',
        {
            'p': plain_gate([
                entry('SG-EVIDENCE', 'blocked', 'report', 'bad claim', 'log', 'none'),
                entry('SG-STOP', 'satisfied', 'stop', 'confirmed', 'record', 'not_required'),
            ])
        },
        [],
        0,
        'p aggregate state: blocked',
    ),
    (
        'duplicate node rejected',
        [
            ('p', plain_gate([entry('SG-STOP', 'hold', 'x', 'pending')])),
            ('p', plain_gate([entry('SG-STOP', 'hold', 'x', 'pending')])),
        ],
        [],
        2,
        'duplicate graph node id',
    ),
]


def run_semantic(case):
    name, gate_id, guard, expected, marker = case
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'input.md'
        path.write_text(gate_doc(gate_id, guard=guard), encoding='utf-8')
        code, output = run_main(
            kdsl_safety_semantics.main,
            ['kdsl_safety_semantics.py', str(path)],
        )
    return name, code == expected and marker in output, code, output, expected


def run_graph(case):
    name, nodes, edges, expected, marker = case
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        node_items = []
        iterable = nodes if isinstance(nodes, list) else list(nodes.items())
        for index, (node_id, content) in enumerate(iterable):
            file_name = f'n{index}.md'
            (root / file_name).write_text(content, encoding='utf-8')
            node_items.append({'id': node_id, 'file': file_name})
        manifest = root / 'graph.json'
        manifest.write_text(json.dumps({'nodes': node_items, 'edges': edges}), encoding='utf-8')
        code, output = run_main(
            kdsl_safety_gate_graph.main,
            ['kdsl_safety_gate_graph.py', str(manifest)],
        )
    return name, code == expected and marker in output, code, output, expected


def main():
    failed = 0
    for case in SEMANTIC_CASES:
        name, ok, code, output, expected = run_semantic(case)
        print(('PASS' if ok else 'FAIL') + ': ' + name)
        if not ok:
            failed += 1
            print(f'  expected: {expected}')
            print(f'  actual: {code}')
            print(output)
    for case in GRAPH_CASES:
        name, ok, code, output, expected = run_graph(case)
        print(('PASS' if ok else 'FAIL') + ': ' + name)
        if not ok:
            failed += 1
            print(f'  expected: {expected}')
            print(f'  actual: {code}')
            print(output)
    total = len(SEMANTIC_CASES) + len(GRAPH_CASES)
    print('SUMMARY:')
    print('  total: ' + str(total))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
