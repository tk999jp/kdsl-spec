from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
SOURCE = REPO_ROOT / 'examples/packet/packet-semantic-property.example.md'


def run(name: str, script: str, args: list[str], expected: int, contains: tuple[str, ...] = ()) -> bool:
    proc = subprocess.run(
        [sys.executable, str(ROOT / script), *args],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    ok = proc.returncode == expected and all(marker in proc.stdout for marker in contains)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    print('  expected: ' + str(expected))
    print('  actual: ' + str(proc.returncode))
    if not ok:
        print('  stdout:')
        print('\n'.join('    ' + line for line in proc.stdout.splitlines()))
        if proc.stderr:
            print('  stderr:')
            print('\n'.join('    ' + line for line in proc.stderr.splitlines()))
    return ok


def run_text(name: str, script: str, text: str, expected: int, contains: tuple[str, ...] = ()) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'input.md'
        path.write_text(text, encoding='utf-8')
        return run(name, script, [str(path)], expected, contains)


def generate_normalization(source_path: Path) -> str:
    proc = subprocess.run(
        [sys.executable, str(ROOT / 'kdsl_packet_normalize_semantic.py'), str(source_path)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode not in {0, 1}:
        raise RuntimeError(proc.stderr or proc.stdout)
    return proc.stdout


def run_property_text(
    name: str,
    source_text: str,
    normalization_text: str,
    expected: int,
    contains: tuple[str, ...] = (),
) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        source_path = Path(tmp) / 'source.md'
        normalization_path = Path(tmp) / 'normalization.md'
        source_path.write_text(source_text, encoding='utf-8')
        normalization_path.write_text(normalization_text, encoding='utf-8')
        return run(
            name,
            'kdsl_packet_property.py',
            [str(source_path), str(normalization_path)],
            expected,
            contains,
        )


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise AssertionError('mutation anchor not found: ' + old)
    return text.replace(old, new, 1)


def mutate_digest(text: str) -> str:
    match = re.search(r'sha256:([0-9a-f]{64})', text)
    if match is None:
        raise AssertionError('digest mutation anchor not found')
    digest = match.group(1)
    first = '0' if digest[0] != '0' else '1'
    mutated = first + digest[1:]
    return text[:match.start(1)] + mutated + text[match.end(1):]


def main() -> int:
    source = SOURCE.read_text(encoding='utf-8')
    normalization = generate_normalization(SOURCE)
    results: list[bool] = []

    results.append(run('repository Packet semantic pass', 'kdsl_packet_semantic.py', [str(SOURCE)], 0, ('STATUS: pass',)))
    results.append(run('wrapper packet-semantic pass', 'kdsl_validate.py', ['--target', 'packet-semantic', str(SOURCE)], 0, ('TARGET: packet-semantic',)))
    results.append(run('strict mapper pass', 'kdsl_packet_normalize_semantic.py', [str(SOURCE)], 0, ('NORMALIZATION_DRAFT:', 'KDSL_PROMPT_PREVIEW:')))
    results.append(run('generated property pass', 'kdsl_packet_property.py', [str(SOURCE)], 0, ('STATUS: property_pass',)))

    with tempfile.TemporaryDirectory() as tmp:
        normalization_path = Path(tmp) / 'normalization.md'
        normalization_path.write_text(normalization, encoding='utf-8')
        results.append(run('supplied property pass', 'kdsl_packet_property.py', [str(SOURCE), str(normalization_path)], 0, ('STATUS: property_pass',)))

    results.append(run_text('OBS classification prefix required', 'kdsl_packet_semantic.py', replace_once(source, 'observed: duplicate entry appears after refresh', 'duplicate entry appears after refresh'), 2, ('must use observed|inferred',)))
    results.append(run_text('OBS cross-class conflict rejected', 'kdsl_packet_semantic.py', replace_once(source, 'inferred: cache invalidation may be involved', 'inferred: duplicate entry appears after refresh'), 2, ('OBS classification conflict',)))
    results.append(run_text('SG unknown field rejected', 'kdsl_packet_semantic.py', replace_once(source, '      authority: "none"', '      authority: "none"\n      extra: "invalid"'), 2, ('unknown fields',)))
    results.append(run_text('SG missing scope rejected', 'kdsl_packet_semantic.py', replace_once(source, '      scope: "src/Example.cs"\n', ''), 2, ('missing fields: scope',)))
    results.append(run_text('SG unknown state rejected', 'kdsl_packet_semantic.py', replace_once(source, '      state: hold', '      state: cleared'), 2, ('unknown state',)))
    results.append(run_text('SG satisfied evidence required', 'kdsl_packet_semantic.py', replace_once(source, '      evidence: "KDSL-DP直接実行禁止 / P1/P1L正規化必須"', '      evidence: "none"'), 2, ('satisfied requires evidence',)))
    authority_satisfied = replace_once(source, '    - id: SG-AUTHORITY\n      state: hold', '    - id: SG-AUTHORITY\n      state: satisfied')
    authority_satisfied = replace_once(authority_satisfied, '      authority: "not_established"', '      authority: "none"')
    results.append(run_text('SG satisfied authority required', 'kdsl_packet_semantic.py', authority_satisfied, 2, ('satisfied requires authority reference',)))
    blocked_no_evidence = replace_once(source, '    - id: SG-RUNTIME\n      state: hold', '    - id: SG-RUNTIME\n      state: blocked')
    results.append(run_text('SG blocked evidence required', 'kdsl_packet_semantic.py', blocked_no_evidence, 2, ('blocked requires observed evidence',)))
    results.append(run_text('SG hold granting authority rejected', 'kdsl_packet_semantic.py', replace_once(source, '      authority: "not_established"', '      authority: "allow"'), 2, ('hold conflicts with granting authority',)))
    results.append(run_text('duplicate SG ID rejected', 'kdsl_packet_semantic.py', replace_once(source, '    - id: SG-RUNTIME', '    - id: SG-SCOPE'), 2, ('duplicate Packet Safety Gate ID',)))
    results.append(run_text('scope protected wording weakening rejected', 'kdsl_packet_semantic.py', replace_once(source, 'TGT外変更禁止', 'TGT外変更可能'), 2, ('protected concept weakened',)))
    results.append(run_text('evidence protected wording weakening rejected', 'kdsl_packet_semantic.py', replace_once(source, '未確認を確認済扱い禁止', '未確認を確認済扱い可能'), 2, ('protected concept weakened',)))
    results.append(run_text('runtime non-substitution weakening rejected', 'kdsl_packet_semantic.py', replace_once(source, 'build/diff/lint/test/CI pass != RT:v', 'build pass = RT:v'), 2, ('protected concept weakened',)))
    results.append(run_text('KDSL-DP direct execution weakening rejected', 'kdsl_packet_semantic.py', replace_once(source, 'KDSL-DP直接実行禁止', 'KDSL-DP直接実行可能'), 2, ('protected concept weakened',)))
    blocked_change = replace_once(source, '    - id: SG-RUNTIME\n      state: hold', '    - id: SG-RUNTIME\n      state: blocked')
    blocked_change = replace_once(blocked_change, '      evidence: "none"', '      evidence: "runtime failure observed"')
    results.append(run_text('blocked gate conflicts with FLOW-CHANGE', 'kdsl_packet_semantic.py', blocked_change, 2, ('blocked Safety Gate conflicts with FLOW-CHANGE',)))
    results.append(run_text('unconditional FLOW-CHANGE rejected without edit authority', 'kdsl_packet_semantic.py', replace_once(source, 'Change exact TGT only after approved normalization and SG-AUTHORITY satisfaction', 'Change exact TGT immediately'), 2, ('must remain explicitly conditional',)))
    results.append(run_text('FLOW-READ requires read authority', 'kdsl_packet_semantic.py', replace_once(source, '  read: target_only', '  read: not_requested'), 2, ('FLOW-READ requires explicit read authority',)))
    no_stop = source.replace('STOP:\n  - "Unexpected diff outside TGT"\n  - "Root cause remains unconfirmed"\n  - "Required authority remains unavailable"', 'STOP: []')
    results.append(run_text('hold gates require STOP entries', 'kdsl_packet_semantic.py', no_stop, 2, ('requires explicit STOP entries',)))
    results.append(run_text('VERIFY completed claim rejected', 'kdsl_packet_semantic.py', replace_once(source, '  - "relevant unit tests"', '  - "unit tests passed"'), 2, ('must describe a requirement',)))
    results.append(run_text('Packet normalized self-claim rejected', 'kdsl_packet_semantic.py', replace_once(source, '  state: not_normalized', '  state: normalized'), 2, ('base Packet checker failed',)))

    results.append(run_property_text('property digest mismatch detected', source, mutate_digest(normalization), 2, ('source digest mismatch',)))
    duplicate_map = replace_once(normalization, '    - source: STATUS', '    - source: SCHEMA\n      target: "duplicate"\n      mode: exact\n      evidence: "duplicate"\n    - source: STATUS')
    results.append(run_property_text('duplicate MAP source detected', source, duplicate_map, 2, ('duplicate MAP source entries',)))
    missing_map = normalization.replace('    - source: NORMALIZE\n      target: "normalization provenance"\n      mode: exact\n      evidence: "Phase 4 strict mapper preserves source field and reconstruction property"\n', '')
    results.append(run_property_text('missing MAP source detected', source, missing_map, 2, ('resolved target missing Packet field accounting: NORMALIZE',)))
    results.append(run_property_text('MAP mode policy mutation detected', source, replace_once(normalization, '    - source: SG\n      target: "Safety Gates/禁止"\n      mode: expanded', '    - source: SG\n      target: "Safety Gates/禁止"\n      mode: exact'), 2, ('MAP mode mismatch: SG',)))
    results.append(run_property_text('PRESERVE exact string loss detected', source, replace_once(normalization, '    - "src/Example.cs"\n', ''), 2, ('PRESERVE.exact_strings missing',)))
    protected_loss = replace_once(
        normalization,
        '  protected_wording:\n    - "TGT外変更禁止"\n',
        '  protected_wording:\n',
    )
    results.append(run_property_text('PRESERVE protected wording loss detected', source, protected_loss, 2, ('PRESERVE.protected_wording missing',)))
    results.append(run_property_text('PRESERVE ordered field mutation detected', source, replace_once(normalization, 'FLOW-READ>FLOW-ANALYZE>FLOW-GATE>FLOW-CHANGE>FLOW-VERIFY>FLOW-REPORT', 'FLOW-ANALYZE>FLOW-READ>FLOW-GATE>FLOW-CHANGE>FLOW-VERIFY>FLOW-REPORT'), 2, ('PRESERVE.ordered_fields missing or changed',)))
    results.append(run_property_text('preview Safety Gate record loss detected', source, replace_once(normalization, 'scope=src/Example.cs', 'scope=src/Other.cs'), 2, ('Safety Gate record not exactly represented',)))
    preview_flow_detail_loss = replace_once(
        normalization,
        '    - FLOW-READ: Inspect exact READ references',
        '    - FLOW-READ: Inspect references',
    )
    results.append(run_property_text('preview FLOW detail loss detected', source, preview_flow_detail_loss, 2, ('exact source strings missing from preview',)))
    flow_order_changed = replace_once(normalization, '    - FLOW-READ: Inspect exact READ references\n    - FLOW-ANALYZE: Separate observation from inference', '    - FLOW-ANALYZE: Separate observation from inference\n    - FLOW-READ: Inspect exact READ references')
    results.append(run_property_text('preview FLOW order mutation detected', source, flow_order_changed, 2, ('FLOW opcode/detail order changed',)))
    stop_order_changed = replace_once(normalization, '    - Unexpected diff outside TGT\n    - Root cause remains unconfirmed', '    - Root cause remains unconfirmed\n    - Unexpected diff outside TGT')
    results.append(run_property_text('preview STOP order mutation detected', source, stop_order_changed, 2, ('STOP order changed',)))
    verify_order_changed = replace_once(
        normalization,
        '    検証要求:\n    - git diff --check\n    - relevant unit tests',
        '    検証要求:\n    - relevant unit tests\n    - git diff --check',
    )
    results.append(run_property_text('preview VERIFY order mutation detected', source, verify_order_changed, 2, ('VERIFY order changed',)))
    results.append(run_property_text('preview authority widening detected', source, replace_once(normalization, '    - push: forbid', '    - push: allow'), 2, ('authority rail missing or widened',)))
    result_schema_loss = replace_once(
        normalization,
        '    報告形式:\n    - kdsl-r1c@0.1-draft',
        '    報告形式:\n    - canonical-r1',
    )
    results.append(run_property_text('preview result schema loss detected', source, result_schema_loss, 2, ('result schema missing from preview',)))
    results.append(run_property_text('executable preview marker rejected', source, replace_once(normalization, 'KDSL_PROMPT_PREVIEW:', 'KDSL_PROMPT:'), 2, ('normalization artifact failed base checker',)))
    results.append(run_property_text('semantic equivalence claim rejected', source, replace_once(normalization, 'semantic_equivalence: not_proven', 'semantic_equivalence: proven'), 2, ('normalization artifact failed base checker',)))

    p1_source = replace_once(source, '  id: BASE-KDSL-DEV', '  id: BASE-ADPS-P1')
    p1_source = replace_once(p1_source, '  target: full-kdsl-dev-prompt', '  target: P1')
    results.append(run_text('P1 target remains blocked', 'kdsl_packet_property.py', p1_source, 1, ('STATUS: blocked', 'P1/P1L remains blocked')))

    failed = sum(not result for result in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
