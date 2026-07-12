import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from kdsl_r1c_roundtrip import compare_models, parse_model, project_to_full_r1, reconstruct_r1c

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
DEEP_EXAMPLE = REPO_ROOT / 'examples/r1c/r1c-deep-optional.example.md'

BASE = '''KDSL_RESULT:
SCHEMA:kdsl-r1c@0.1-draft
STATUS:success
PHASE:Phase 3 optional-block validation
S:deep optional block validation candidate
FILES:["docs/project-status.md"]
WHY:optional Evidence Authority Safety Gatesの可逆性と境界を検証するため
CMD:[]
VERIFY:{"pass":["KDSL Validation total 181 / failed 0"],"fail":[],"not_run":["local runtime"]}
RT:{"state":"na","basis":"spec/validator only; runtime対象なし"}
RISK:["semantic equivalence proofなし"]
NEXT:{"proposal":"Phase 4 Packet proof","authority":"proposal_only"}
COMMIT:{"actual":null,"proposed":"Validator: add R1C deep optional blocks","permission_basis":"none"}
'''

FULL_AUTHORITY = {
    'read': 'allow',
    'edit': 'target_only',
    'stage': 'not_requested',
    'commit': 'propose_only',
    'push': 'forbid',
    'release': 'forbid',
}

VALID_EVIDENCE = {
    'observed': ['KDSL Validation total 181 / failed 0'],
    'inferred': [],
    'not_observed': [],
    'unverified': ['local runtime'],
}

VALID_SAFETY = '''SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-EVIDENCE
      state: hold
      scope: optional evidence proof
      reason: semantic equivalence not proven
      evidence: none
      authority: none
    - id: SG-AUTHORITY
      state: satisfied
      scope: proposed commit only
      reason: proposal boundary confirmed
      evidence: authority rail record verified
      authority: not_required
'''


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def document(*, evidence=None, authority=None, safety=None, annunciator=None, files=None, commands=None, verify=None, rt=None, commit=None):
    text = BASE
    replacements = {
        'FILES:["docs/project-status.md"]': 'FILES:' + compact(files if files is not None else ['docs/project-status.md']),
        'CMD:[]': 'CMD:' + compact(commands if commands is not None else []),
        'VERIFY:{"pass":["KDSL Validation total 181 / failed 0"],"fail":[],"not_run":["local runtime"]}': 'VERIFY:' + compact(verify if verify is not None else {'pass': ['KDSL Validation total 181 / failed 0'], 'fail': [], 'not_run': ['local runtime']}),
        'RT:{"state":"na","basis":"spec/validator only; runtime対象なし"}': 'RT:' + compact(rt if rt is not None else {'state': 'na', 'basis': 'spec/validator only; runtime対象なし'}),
        'COMMIT:{"actual":null,"proposed":"Validator: add R1C deep optional blocks","permission_basis":"none"}': 'COMMIT:' + compact(commit if commit is not None else {'actual': None, 'proposed': 'Validator: add R1C deep optional blocks', 'permission_basis': 'none'}),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    if evidence is not None:
        text += 'EVIDENCE:' + (evidence if isinstance(evidence, str) else compact(evidence)) + '\n'
    if authority is not None:
        text += 'AUTHORITY:' + compact(authority) + '\n'
    if annunciator is not None:
        text += 'ANNUNCIATOR:' + compact(annunciator) + '\n'
    if safety is not None:
        text += safety.rstrip() + '\n'
    return text


def run_case(name, text, command, expected, contains=()):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'input.md'
        path.write_text(text, encoding='utf-8')
        args = [sys.executable, str(ROOT / command[0]), *command[1:], str(path)]
        result = subprocess.run(args, capture_output=True, text=True)
    ok = result.returncode == expected and all(marker in result.stdout for marker in contains)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    print('  expected: ' + str(expected))
    print('  actual: ' + str(result.returncode))
    if not ok:
        print('  stdout:')
        print('\n'.join('    ' + line for line in result.stdout.splitlines()))
        if result.stderr:
            print('  stderr:')
            print('\n'.join('    ' + line for line in result.stderr.splitlines()))
    return ok


def mutate_optional_property(name, text, mutate, marker):
    source = parse_model(text)
    projection = project_to_full_r1(source)
    mutate(projection)
    mismatches = compare_models(source, reconstruct_r1c(projection))
    ok = any(marker in item for item in mismatches)
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    if not ok:
        print('  mismatches: ' + repr(mismatches))
    return ok


def main():
    results = []
    results.append(run_case('deep optional repository checker pass', DEEP_EXAMPLE.read_text(encoding='utf-8'), ['kdsl_r1c_optional.py'], 0, ('optional SAFETY_GATES deep lint checked',)))
    results.append(run_case('deep optional repository wrapper pass', DEEP_EXAMPLE.read_text(encoding='utf-8'), ['kdsl_validate.py', '--target', 'r1c'], 0, ('CHECK: kdsl_r1c_optional.py',)))
    results.append(run_case('deep optional repository round-trip pass', DEEP_EXAMPLE.read_text(encoding='utf-8'), ['kdsl_r1c_roundtrip.py'], 0, ('optional SAFETY_GATES registry/entry/order preserved',)))

    multiline_evidence = json.dumps(VALID_EVIDENCE, ensure_ascii=False, indent=2)
    results.append(run_case('multiline EVIDENCE pass', document(evidence='\n' + multiline_evidence, authority=FULL_AUTHORITY), ['kdsl_r1c_optional.py'], 0))

    missing = copy.deepcopy(VALID_EVIDENCE); missing.pop('unverified')
    results.append(run_case('EVIDENCE missing class rejected', document(evidence=missing), ['kdsl_r1c_optional.py'], 2, ('EVIDENCE required subkey missing: unverified',)))
    unknown = copy.deepcopy(VALID_EVIDENCE); unknown['confirmed'] = []
    results.append(run_case('EVIDENCE unknown class rejected', document(evidence=unknown), ['kdsl_r1c_optional.py'], 2, ('EVIDENCE unknown subkey: confirmed',)))
    wrong = copy.deepcopy(VALID_EVIDENCE); wrong['observed'] = 'CI success'
    results.append(run_case('EVIDENCE non-array rejected', document(evidence=wrong), ['kdsl_r1c_optional.py'], 2, ('EVIDENCE.observed must be a JSON array',)))
    duplicate = copy.deepcopy(VALID_EVIDENCE); duplicate['observed'] = ['same', 'same']
    results.append(run_case('EVIDENCE duplicate rejected', document(evidence=duplicate), ['kdsl_r1c_optional.py'], 2, ('EVIDENCE.observed duplicate item',)))
    overlap = copy.deepcopy(VALID_EVIDENCE); overlap['observed'] = ['same']; overlap['inferred'] = ['same']
    results.append(run_case('EVIDENCE observed inferred overlap rejected', document(evidence=overlap), ['kdsl_r1c_optional.py'], 2, ('classification overlap between observed and inferred',)))
    overlap2 = copy.deepcopy(VALID_EVIDENCE); overlap2['observed'] = ['same']; overlap2['unverified'] = ['same']
    results.append(run_case('EVIDENCE observed unverified overlap rejected', document(evidence=overlap2), ['kdsl_r1c_optional.py'], 2, ('classification overlap between observed and unverified',)))
    verify_conflict = {'pass': ['local runtime'], 'fail': [], 'not_run': []}
    results.append(run_case('VERIFY pass unverified conflict rejected', document(evidence=VALID_EVIDENCE, verify=verify_conflict), ['kdsl_r1c_optional.py'], 2, ('VERIFY.pass conflicts with EVIDENCE.unverified',)))
    rt_evidence = copy.deepcopy(VALID_EVIDENCE); rt_evidence['unverified'] = ['runtime log pending']
    results.append(run_case('RT v unverified basis conflict rejected', document(evidence=rt_evidence, rt={'state': 'v', 'basis': 'runtime log pending'}), ['kdsl_r1c_optional.py'], 2, ('RT:v basis conflicts with EVIDENCE.unverified',)))

    results.append(run_case('AUTHORITY full rails pass', document(authority=FULL_AUTHORITY), ['kdsl_r1c_optional.py'], 0))
    missing_rail = copy.deepcopy(FULL_AUTHORITY); missing_rail.pop('release')
    results.append(run_case('AUTHORITY missing rail rejected', document(authority=missing_rail), ['kdsl_r1c_optional.py'], 2, ('AUTHORITY required subkey missing: release',)))
    unknown_rail = copy.deepcopy(FULL_AUTHORITY); unknown_rail['deploy'] = 'forbid'
    results.append(run_case('AUTHORITY unknown rail rejected', document(authority=unknown_rail), ['kdsl_r1c_optional.py'], 2, ('AUTHORITY unknown subkey: deploy',)))
    unknown_value = copy.deepcopy(FULL_AUTHORITY); unknown_value['push'] = 'yes'
    results.append(run_case('AUTHORITY unknown value rejected', document(authority=unknown_value), ['kdsl_r1c_optional.py'], 2, ('AUTHORITY.push unknown value: yes',)))
    edit_forbid = copy.deepcopy(FULL_AUTHORITY); edit_forbid['edit'] = 'forbid'
    results.append(run_case('AUTHORITY edit forbid conflicts with FILES', document(authority=edit_forbid), ['kdsl_r1c_optional.py'], 2, ('conflicts with non-empty FILES',)))
    results.append(run_case('AUTHORITY stage not requested conflicts with git add', document(authority=FULL_AUTHORITY, commands=['git add docs/project-status.md']), ['kdsl_r1c_optional.py'], 2, ('AUTHORITY.stage=not_requested conflicts',)))
    results.append(run_case('AUTHORITY commit propose only conflicts with git commit', document(authority=FULL_AUTHORITY, commands=['git commit -m test']), ['kdsl_r1c_optional.py'], 2, ('AUTHORITY.commit=propose_only conflicts',)))
    actual_none_basis = {'actual': 'abc123 commit', 'proposed': None, 'permission_basis': 'none'}
    results.append(run_case('AUTHORITY propose only actual without basis rejected', document(authority=FULL_AUTHORITY, commit=actual_none_basis), ['kdsl_r1c_optional.py'], 2, ('requires separate permission_basis',)))
    actual_basis = {'actual': 'abc123 commit', 'proposed': None, 'permission_basis': 'U承認'}
    results.append(run_case('AUTHORITY propose only actual with separate basis warns', document(authority=FULL_AUTHORITY, commit=actual_basis), ['kdsl_r1c_optional.py'], 1, ('uses separate permission_basis',)))
    results.append(run_case('AUTHORITY push forbid conflicts with git push', document(authority=FULL_AUTHORITY, commands=['git push origin main']), ['kdsl_r1c_optional.py'], 2, ('AUTHORITY.push=forbid conflicts',)))
    results.append(run_case('AUTHORITY release forbid conflicts with git tag', document(authority=FULL_AUTHORITY, commands=['git tag v2.0.0']), ['kdsl_r1c_optional.py'], 2, ('AUTHORITY.release=forbid conflicts',)))

    results.append(run_case('SAFETY_GATES valid pass', document(safety=VALID_SAFETY), ['kdsl_r1c_optional.py'], 0))
    bad_registry = VALID_SAFETY.replace('kdsl-sg@0.1-draft', 'kdsl-sg@9')
    results.append(run_case('SAFETY_GATES unknown registry rejected', document(safety=bad_registry), ['kdsl_r1c_optional.py'], 2, ('unknown or missing registry',)))
    bad_id = VALID_SAFETY.replace('SG-EVIDENCE', 'SG-UNKNOWN', 1)
    results.append(run_case('SAFETY_GATES unknown id rejected', document(safety=bad_id), ['kdsl_r1c_optional.py'], 2, ('unknown Safety Gate ID',)))
    missing_scope = VALID_SAFETY.replace('      scope: optional evidence proof\n', '', 1)
    results.append(run_case('SAFETY_GATES missing field rejected', document(safety=missing_scope), ['kdsl_r1c_optional.py'], 2, ('required field missing or empty: scope',)))
    missing_evidence = VALID_SAFETY.replace('      evidence: authority rail record verified\n', '', 1)
    results.append(run_case('SAFETY_GATES satisfied missing evidence rejected', document(safety=missing_evidence), ['kdsl_r1c_optional.py'], 2, ('state:satisfied requires evidence',)))
    duplicate_gate = VALID_SAFETY + '''    - id: SG-EVIDENCE
      state: hold
      scope: duplicate
      reason: duplicate
      evidence: none
      authority: none
'''
    results.append(run_case('SAFETY_GATES duplicate id rejected', document(safety=duplicate_gate), ['kdsl_r1c_optional.py'], 2, ('duplicate Safety Gate ID',)))
    unknown_state = VALID_SAFETY.replace('state: hold', 'state: pending', 1)
    results.append(run_case('SAFETY_GATES unknown state rejected', document(safety=unknown_state), ['kdsl_r1c_optional.py'], 2, ('unknown Safety Gate state',)))

    ann = {'STATUS': 'success', 'PHASE': 'Phase 3', 'AUTHORITY': 'locked', 'RT': 'na', 'PUBLIC_OPS': 'locked', 'DESTRUCTIVE_OPS': 'locked'}
    results.append(run_case('ANNUNCIATOR canonical keys structural pass', document(annunciator=ann), ['kdsl_r1c_optional.py'], 0))
    ann_bad = copy.deepcopy(ann); ann_bad['UNKNOWN'] = 'x'
    results.append(run_case('ANNUNCIATOR unknown key rejected', document(annunciator=ann_bad), ['kdsl_r1c_optional.py'], 2, ('ANNUNCIATOR unknown subkey: UNKNOWN',)))

    safety_text = document(evidence=VALID_EVIDENCE, authority=FULL_AUTHORITY, safety=VALID_SAFETY)
    def mutate_safety(projection):
        for index, (key, value) in enumerate(projection['optional']):
            if key == 'SAFETY_GATES':
                changed = copy.deepcopy(value)
                changed['entries'][0]['state'] = 'satisfied'
                projection['optional'][index] = (key, changed)
                return
    results.append(mutate_optional_property('SAFETY_GATES mutation detected', safety_text, mutate_safety, 'optional field changed: SAFETY_GATES'))

    def mutate_optional_order(projection):
        projection['optional_order'] = list(reversed(projection['optional_order']))
    results.append(mutate_optional_property('optional field order mutation detected', safety_text, mutate_optional_order, 'optional field order changed'))

    failed = sum(not item for item in results)
    print('SUMMARY:')
    print('  total: ' + str(len(results)))
    print('  failed: ' + str(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
