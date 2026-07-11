import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent


def baseline_doc(extra_entry='', extra_guard=''):
    text = """KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: satisfied
      scope: exact target and non-target
      reason: exact target and non-target confirmed
      evidence: preflight verified
      authority: not_required
    - id: SG-EVIDENCE
      state: satisfied
      scope: reported evidence
      reason: executed evidence separated from inference
      evidence: command output verified
      authority: not_required
    - id: SG-AUTHORITY
      state: satisfied
      scope: edit target files only
      reason: exact edit authority confirmed
      evidence: authority record verified
      authority: target_only
    - id: SG-STOP
      state: satisfied
      scope: stop conditions
      reason: stop conditions reviewed and no mismatch observed
      evidence: preflight verified
      authority: not_required
"""
    if extra_entry:
        text += extra_entry.rstrip() + '\n'
    text += '\nGuard:\n- 未確認→確認済扱禁止\n'
    if extra_guard:
        text += extra_guard.rstrip() + '\n'
    return text


def gate_doc(entries):
    text = 'SAFETY_GATES:\n  registry: kdsl-sg@0.1-draft\n  entries:\n'
    for entry in entries:
        text += f"    - id: {entry['id']}\n"
        for key in ('state', 'scope', 'reason', 'evidence', 'authority'):
            if key in entry:
                text += f'      {key}: {entry[key]}\n'
    return text


RUNTIME_ENTRY = """    - id: SG-RUNTIME
      state: hold
      scope: target runtime
      reason: pending
      evidence: none
      authority: none"""
KDSL_DP_ENTRY = """    - id: SG-KDSL-DP
      state: hold
      scope: authoring input
      reason: pending normalization
      evidence: none
      authority: none"""
NA_RUNTIME_ENTRY = """    - id: SG-RUNTIME
      state: na
      scope: target runtime
      reason: marked non-applicable
      evidence: none
      authority: not_required"""
AGGREGATE_BLOCKED = """SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-EVIDENCE
      state: blocked
      scope: report
      reason: unverified claim observed
      evidence: report claims success without command output
      authority: none
    - id: SG-STOP
      state: satisfied
      scope: stop declaration
      reason: stop condition recorded
      evidence: record
      authority: not_required
"""

PARENT_HOLD = gate_doc([
    dict(id='SG-EVIDENCE', state='hold', scope='report', reason='evidence pending', evidence='none', authority='none')
])
CHILD_HOLD = gate_doc([
    dict(id='SG-EVIDENCE', state='hold', scope='report', reason='evidence still pending', evidence='none', authority='none')
])
PARENT_BLOCKED = gate_doc([
    dict(id='SG-STOP', state='blocked', scope='preflight', reason='mismatch observed', evidence='unexpected diff', authority='none')
])
CHILD_BLOCKED = gate_doc([
    dict(id='SG-STOP', state='blocked', scope='preflight', reason='mismatch remains', evidence='unexpected diff remains', authority='none')
])
CHILD_MISSING = gate_doc([
    dict(id='SG-SCOPE', state='satisfied', scope='target', reason='confirmed', evidence='record', authority='not_required')
])
CHILD_BLOCKED_TO_SATISFIED = gate_doc([
    dict(id='SG-STOP', state='satisfied', scope='preflight', reason='ready', evidence='new record', authority='not_required')
])
CHILD_BLOCKED_TO_HOLD_RESOLVED = gate_doc([
    dict(id='SG-STOP', state='hold', scope='preflight', reason='cause resolved; re-evaluation pending', evidence='resolution log verified', authority='none')
])
PARENT_HOLD_AUTHORITY = gate_doc([
    dict(id='SG-AUTHORITY', state='hold', scope='commit', reason='approval pending', evidence='none', authority='none')
])
CHILD_HOLD_TO_SATISFIED_WITHOUT_BASIS = gate_doc([
    dict(id='SG-AUTHORITY', state='satisfied', scope='commit', reason='ready', evidence='ticket 123', authority='allow_once')
])
PARENT_NA = gate_doc([
    dict(id='SG-PUBLIC', state='na', scope='local docs', reason='no public operation', evidence='none', authority='not_required')
])
CHILD_NA_SAME = gate_doc([
    dict(id='SG-PUBLIC', state='na', scope='local docs', reason='no public operation', evidence='none', authority='not_required')
])
PARENT_SATISFIED = gate_doc([
    dict(id='SG-SCOPE', state='satisfied', scope='file A', reason='confirmed', evidence='preflight verified', authority='not_required')
])
CHILD_SATISFIED_SCOPE_CHANGED = gate_doc([
    dict(id='SG-SCOPE', state='satisfied', scope='file A and B', reason='confirmed', evidence='preflight verified', authority='not_required')
])
CHILD_BLOCKED_TO_NA = gate_doc([
    dict(id='SG-STOP', state='na', scope='preflight', reason='not applicable', evidence='none', authority='not_required')
])

CASES = [
    dict(name='protected repository example valid', command=['kdsl_safety_gate.py', str(REPO_ROOT / 'examples/safety-gates/dev-prompt-safety-gates.example.md')], expected=0, contains=['aggregate state: hold', 'protected wording checked']),
    dict(name='runtime protected wording missing', files={'input.md': baseline_doc(RUNTIME_ENTRY)}, command=['kdsl_safety_gate.py', 'input.md'], expected=2, contains=['SG-RUNTIME: protected wording group missing']),
    dict(name='KDSL-DP protected wording missing', files={'input.md': baseline_doc(KDSL_DP_ENTRY)}, command=['kdsl_safety_gate.py', 'input.md'], expected=2, contains=['SG-KDSL-DP: protected wording group missing']),
    dict(name='trigger-present na bypass rejected', files={'input.md': baseline_doc(NA_RUNTIME_ENTRY, '- RT:v claim exists\n- Runtime未確認→RT:p|RT:u')}, command=['kdsl_safety_gate.py', 'input.md'], expected=2, contains=['trigger-present gate cannot use state:na: SG-RUNTIME']),
    dict(name='aggregate blocked', files={'input.md': AGGREGATE_BLOCKED}, command=['kdsl_safety_gate.py', 'input.md'], expected=0, contains=['aggregate state: blocked']),
    dict(name='inheritance hold preserved', files={'parent.md': PARENT_HOLD, 'child.md': CHILD_HOLD}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=0),
    dict(name='inheritance blocked preserved', files={'parent.md': PARENT_BLOCKED, 'child.md': CHILD_BLOCKED}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=0),
    dict(name='inherited hold missing', files={'parent.md': PARENT_HOLD, 'child.md': CHILD_MISSING}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=2, contains=['parent hold gate missing from child']),
    dict(name='blocked downgrade without resolution rejected', files={'parent.md': PARENT_BLOCKED, 'child.md': CHILD_BLOCKED_TO_SATISFIED}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=2, contains=['blocked->satisfied requires explicit resolution evidence']),
    dict(name='blocked to hold with resolution accepted', files={'parent.md': PARENT_BLOCKED, 'child.md': CHILD_BLOCKED_TO_HOLD_RESOLVED}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=0),
    dict(name='hold satisfaction without basis rejected', files={'parent.md': PARENT_HOLD_AUTHORITY, 'child.md': CHILD_HOLD_TO_SATISFIED_WITHOUT_BASIS}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=2, contains=['hold->satisfied requires explicit satisfaction basis']),
    dict(name='parent na copied warning', files={'parent.md': PARENT_NA, 'child.md': CHILD_NA_SAME}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=1, contains=['parent na must be re-evaluated in child']),
    dict(name='satisfied scope change warning', files={'parent.md': PARENT_SATISFIED, 'child.md': CHILD_SATISFIED_SCOPE_CHANGED}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=1, contains=['satisfied scope changed; re-evaluate evidence and authority']),
    dict(name='blocked to na rejected', files={'parent.md': PARENT_BLOCKED, 'child.md': CHILD_BLOCKED_TO_NA}, command=['kdsl_safety_gate_inheritance.py', 'parent.md', 'child.md'], expected=2, contains=['inherited blocked gate cannot transition to na']),
]


def run_case(case):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for name, content in case.get('files', {}).items():
            (tmp_path / name).write_text(content, encoding='utf-8')
        command = [sys.executable, str(ROOT / case['command'][0])]
        for arg in case['command'][1:]:
            if arg.endswith('.md') and not Path(arg).is_absolute():
                command.append(str(tmp_path / arg))
            else:
                command.append(arg)
        result = subprocess.run(command, capture_output=True, text=True)
        ok = result.returncode == case['expected']
        for marker in case.get('contains', []):
            if marker not in result.stdout:
                ok = False
        label = 'PASS' if ok else 'FAIL'
        print(f"{label}: {case['name']}")
        print('  cmd: ' + ' '.join(command))
        print(f"  expected: {case['expected']}")
        print(f"  actual: {result.returncode}")
        if not ok:
            if result.stdout:
                print('  stdout:')
                print('\n'.join('    ' + line for line in result.stdout.splitlines()))
            if result.stderr:
                print('  stderr:')
                print('\n'.join('    ' + line for line in result.stderr.splitlines()))
        return ok


def main():
    failed = sum(not run_case(case) for case in CASES)
    print('SUMMARY:')
    print(f'  total: {len(CASES)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
