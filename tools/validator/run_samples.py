import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent

SAMPLES = [
    {
        'name': 'r1 required blocks ok',
        'command': ['r1_required_blocks.py', 'samples/sample_r1_ok.md'],
        'expected': 0,
    },
    {
        'name': 'r1 required blocks missing block',
        'command': ['r1_required_blocks.py', 'samples/sample_r1_missing_block.md'],
        'expected': 2,
    },
    {
        'name': 'rt v valid field-scoped basis',
        'command': ['r1_rt_basis.py', 'samples/sample_rt_v_valid.md'],
        'expected': 0,
    },
    {
        'name': 'rt v invalid basis',
        'command': ['r1_rt_basis.py', 'samples/sample_rt_v_invalid_basis.md'],
        'expected': 2,
    },
    {
        'name': 'rt v no basis',
        'command': ['r1_rt_basis.py', 'samples/sample_rt_v_no_basis.md'],
        'expected': 2,
    },
    {
        'name': 'authority ok',
        'command': ['r1_authority_guard.py', 'samples/sample_authority_ok.md'],
        'expected': 0,
    },
    {
        'name': 'authority warn',
        'command': ['r1_authority_guard.py', 'samples/sample_authority_warn.md'],
        'expected': 1,
    },
    {
        'name': 'authority fail',
        'command': ['r1_authority_guard.py', 'samples/sample_authority_fail.md'],
        'expected': 2,
    },
    {
        'name': 'template refs ok',
        'command': ['kdsl_template_refs.py', 'samples/sample_template_ref_ok.md'],
        'expected': 0,
    },
    {
        'name': 'template refs missing gate',
        'command': ['kdsl_template_refs.py', 'samples/sample_template_ref_missing_gate.md'],
        'expected': 2,
    },
    {
        'name': 'template expansion evidence ok',
        'command': ['kdsl_template_expansion.py', 'samples/sample_template_expansion_ok.md'],
        'expected': 0,
    },
    {
        'name': 'template expansion evidence warn',
        'command': ['kdsl_template_expansion.py', 'samples/sample_template_expansion_warn.md'],
        'expected': 1,
    },
    {
        'name': 'template expansion evidence fail',
        'command': ['kdsl_template_expansion.py', 'samples/sample_template_expansion_fail.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target r1 valid',
        'command': ['kdsl_validate.py', '--target', 'r1', 'samples/sample_rt_v_valid.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target prompt expansion ok',
        'command': ['kdsl_validate.py', '--target', 'prompt', 'samples/sample_template_expansion_ok.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target prompt ref only fails expansion evidence',
        'command': ['kdsl_validate.py', '--target', 'prompt', 'samples/sample_template_ref_ok.md'],
        'expected': 2,
    },
    {
        'name': 'compact standard ok',
        'command': ['kdsl_compact_prompt.py', 'samples/sample_cp_standard_ok.md'],
        'expected': 0,
    },
    {
        'name': 'compact kanji ok',
        'command': ['kdsl_compact_prompt.py', 'samples/sample_cp_kanji_ok.md'],
        'expected': 0,
    },
    {
        'name': 'compact missing block',
        'command': ['kdsl_compact_prompt.py', 'samples/sample_cp_missing_block.md'],
        'expected': 2,
    },
    {
        'name': 'compact restricted alias',
        'command': ['kdsl_compact_prompt.py', 'samples/sample_cp_restricted_alias.md'],
        'expected': 2,
    },
    {
        'name': 'compact CP-Lift required',
        'command': ['kdsl_compact_prompt.py', 'samples/sample_cp_lift_required.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target compact valid',
        'command': ['kdsl_validate.py', '--target', 'compact', 'samples/sample_cp_standard_ok.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target compact invalid',
        'command': ['kdsl_validate.py', '--target', 'compact', 'samples/sample_cp_restricted_alias.md'],
        'expected': 2,
    },
    {
        'name': 'safety gate valid baseline',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_valid.md'],
        'expected': 0,
    },
    {
        'name': 'safety gate repository example valid',
        'command': ['kdsl_safety_gate.py', 'examples/safety-gates/dev-prompt-safety-gates.example.md'],
        'expected': 0,
    },
    {
        'name': 'safety gate unknown registry',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_unknown_registry.md'],
        'expected': 2,
    },
    {
        'name': 'safety gate unknown id and state',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_unknown_id_state.md'],
        'expected': 2,
    },
    {
        'name': 'safety gate missing required field',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_missing_field.md'],
        'expected': 2,
    },
    {
        'name': 'safety gate satisfied missing basis',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_satisfied_missing_basis.md'],
        'expected': 2,
    },
    {
        'name': 'safety gate na missing reason',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_na_missing_reason.md'],
        'expected': 2,
    },
    {
        'name': 'safety gate dev-prompt baseline missing',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_baseline_missing.md'],
        'expected': 2,
    },
    {
        'name': 'safety gate rollback composition missing',
        'command': ['kdsl_safety_gate.py', 'samples/sample_sg_composition_missing.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target safety gate valid',
        'command': ['kdsl_validate.py', '--target', 'safety-gate', 'samples/sample_sg_valid.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target safety gate invalid',
        'command': ['kdsl_validate.py', '--target', 'safety-gate', 'samples/sample_sg_composition_missing.md'],
        'expected': 2,
    },
    {
        'name': 'r1c repository success example valid',
        'command': ['kdsl_r1c.py', 'examples/r1c/r1c-success.example.md'],
        'expected': 0,
    },
    {
        'name': 'r1c repository blocked example valid',
        'command': ['kdsl_r1c.py', 'examples/r1c/r1c-blocked.example.md'],
        'expected': 0,
    },
    {
        'name': 'r1c repository needs-user example valid',
        'command': ['kdsl_r1c.py', 'examples/r1c/r1c-needs-user.example.md'],
        'expected': 0,
    },
    {
        'name': 'r1c unknown schema',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_unknown_schema.md'],
        'expected': 2,
    },
    {
        'name': 'r1c missing required field',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_missing_field.md'],
        'expected': 2,
    },
    {
        'name': 'r1c short alias rejected',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_alias.md'],
        'expected': 2,
    },
    {
        'name': 'r1c invalid structured JSON',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_invalid_json.md'],
        'expected': 2,
    },
    {
        'name': 'r1c invalid RT v basis',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_invalid_rt.md'],
        'expected': 2,
    },
    {
        'name': 'r1c invalid NEXT authority',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_invalid_next.md'],
        'expected': 2,
    },
    {
        'name': 'r1c invalid COMMIT authority',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_invalid_commit.md'],
        'expected': 2,
    },
    {
        'name': 'r1c VERIFY contradiction',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_verify_contradiction.md'],
        'expected': 2,
    },
    {
        'name': 'r1c required field order mismatch',
        'command': ['kdsl_r1c.py', 'samples/sample_r1c_order_mismatch.md'],
        'expected': 2,
    },
    {
        'name': 'r1c Full R1 fallback out of scope',
        'command': ['kdsl_r1c.py', 'samples/sample_r1_ok.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target r1c valid',
        'command': ['kdsl_validate.py', '--target', 'r1c', 'examples/r1c/r1c-success.example.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target r1c invalid',
        'command': ['kdsl_validate.py', '--target', 'r1c', 'samples/sample_r1c_invalid_rt.md'],
        'expected': 2,
    },
    {
        'name': 'packet repository design example valid',
        'command': ['kdsl_packet.py', 'examples/packet/packet-design.example.md'],
        'expected': 0,
    },
    {
        'name': 'packet baseline valid',
        'command': ['kdsl_packet.py', 'samples/sample_packet_valid.md'],
        'expected': 0,
    },
    {
        'name': 'packet unknown schema',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_schema.md'],
        'expected': 2,
    },
    {
        'name': 'packet executable status rejected',
        'command': ['kdsl_packet.py', 'samples/sample_packet_executable_status.md'],
        'expected': 2,
    },
    {
        'name': 'packet missing required READ field',
        'command': ['kdsl_packet.py', 'samples/sample_packet_missing_read.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown BASE ID',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_base.md'],
        'expected': 2,
    },
    {
        'name': 'packet BASE target mismatch',
        'command': ['kdsl_packet.py', 'samples/sample_packet_target_mismatch.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown TASK ID',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_task.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown SG registry',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_sg_registry.md'],
        'expected': 2,
    },
    {
        'name': 'packet TASK minimum gate missing',
        'command': ['kdsl_packet.py', 'samples/sample_packet_missing_gate.md'],
        'expected': 2,
    },
    {
        'name': 'packet unknown FLOW opcode',
        'command': ['kdsl_packet.py', 'samples/sample_packet_unknown_flow.md'],
        'expected': 2,
    },
    {
        'name': 'packet FLOW-CHANGE before FLOW-GATE',
        'command': ['kdsl_packet.py', 'samples/sample_packet_flow_order.md'],
        'expected': 2,
    },
    {
        'name': 'packet missing authority rail',
        'command': ['kdsl_packet.py', 'samples/sample_packet_missing_authority.md'],
        'expected': 2,
    },
    {
        'name': 'packet normalized state rejected',
        'command': ['kdsl_packet.py', 'samples/sample_packet_normalized.md'],
        'expected': 2,
    },
    {
        'name': 'packet PKT v1 rejected',
        'command': ['kdsl_packet.py', 'samples/sample_packet_pkt_v1.md'],
        'expected': 2,
    },
    {
        'name': 'packet broad push authority warning',
        'command': ['kdsl_packet.py', 'samples/sample_packet_authority_warn.md'],
        'expected': 1,
    },
    {
        'name': 'packet out of scope document',
        'command': ['kdsl_packet.py', 'samples/sample_packet_out_of_scope.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target packet valid',
        'command': ['kdsl_validate.py', '--target', 'packet', 'samples/sample_packet_valid.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target packet invalid',
        'command': ['kdsl_validate.py', '--target', 'packet', 'samples/sample_packet_normalized.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target all Packet valid',
        'command': ['kdsl_validate.py', '--target', 'all', 'samples/sample_packet_valid.md'],
        'expected': 0,
    },
    {
        'name': 'normalization repository Full KDSL preview valid',
        'command': ['kdsl_packet_normalization.py', 'examples/packet/normalization-full-kdsl.example.md'],
        'expected': 0,
    },
    {
        'name': 'normalization repository P1 blocked valid',
        'command': ['kdsl_packet_normalization.py', 'examples/packet/normalization-p1-blocked.example.md'],
        'expected': 0,
    },
    {
        'name': 'normalization repository critical-loss blocked valid',
        'command': ['kdsl_packet_normalization.py', 'examples/packet/normalization-lossy-blocked.example.md'],
        'expected': 0,
    },
    {
        'name': 'normalization baseline valid',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_valid.md'],
        'expected': 0,
    },
    {
        'name': 'normalization unknown schema',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_unknown_schema.md'],
        'expected': 2,
    },
    {
        'name': 'normalization executable status rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_executable_status.md'],
        'expected': 2,
    },
    {
        'name': 'normalization target executable rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_target_executable.md'],
        'expected': 2,
    },
    {
        'name': 'normalization semantic equivalence claim rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_semantic_claim.md'],
        'expected': 2,
    },
    {
        'name': 'normalization execution authority rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_authority.md'],
        'expected': 2,
    },
    {
        'name': 'normalization P1 resolved rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_p1_resolved.md'],
        'expected': 2,
    },
    {
        'name': 'normalization executable KDSL prompt marker rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_executable_marker.md'],
        'expected': 2,
    },
    {
        'name': 'normalization source normalized state rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_source_normalized.md'],
        'expected': 2,
    },
    {
        'name': 'normalization missing digest rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_missing_digest.md'],
        'expected': 2,
    },
    {
        'name': 'normalization critical loss with resolved target rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_critical_resolved.md'],
        'expected': 2,
    },
    {
        'name': 'normalization authority rails false without blocked critical loss rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_rails_false.md'],
        'expected': 2,
    },
    {
        'name': 'normalization malformed digest rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_bad_digest.md'],
        'expected': 2,
    },
    {
        'name': 'normalization blocked target with preview rejected',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_blocked_preview.md'],
        'expected': 2,
    },
    {
        'name': 'normalization out of scope document',
        'command': ['kdsl_packet_normalization.py', 'samples/sample_normalization_out_of_scope.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target normalization valid',
        'command': ['kdsl_validate.py', '--target', 'normalization', 'samples/sample_normalization_valid.md'],
        'expected': 0,
    },
    {
        'name': 'wrapper target normalization invalid',
        'command': ['kdsl_validate.py', '--target', 'normalization', 'samples/sample_normalization_semantic_claim.md'],
        'expected': 2,
    },
    {
        'name': 'wrapper target all normalization valid',
        'command': ['kdsl_validate.py', '--target', 'all', 'samples/sample_normalization_valid.md'],
        'expected': 0,
    },
    {
        'name': 'normalization mapper Full KDSL preview',
        'command': ['kdsl_packet_normalize.py', 'examples/packet/normalization-source.example.md'],
        'expected': 0,
        'stdout_contains': [
            'NORMALIZATION_DRAFT:',
            'SCHEMA: kdsl-packet-normalization@0.1-draft',
            'KDSL_PROMPT_PREVIEW:',
            'semantic_equivalence: not_proven',
            'execution_authority: none',
            'TARGET:',
            '  executable: false',
        ],
        'stdout_not_contains': ['\nKDSL_PROMPT:', '\nSTATUS: executable'],
    },
    {
        'name': 'normalization mapper P1 blocked',
        'command': ['kdsl_packet_normalize.py', 'examples/packet/normalization-p1-source.example.md'],
        'expected': 1,
        'stdout_contains': [
            'NORMALIZATION_DRAFT:',
            '  kind: P1',
            '  resolution: blocked',
            '  marker: none',
            'execution_authority: none',
        ],
        'stdout_not_contains': ['\nP1:', '\nKDSL_PROMPT:'],
    },
    {
        'name': 'normalization mapper invalid Packet rejected',
        'command': ['kdsl_packet_normalize.py', 'samples/sample_packet_normalized.md'],
        'expected': 2,
        'stdout_not_contains': ['NORMALIZATION_DRAFT:', 'KDSL_PROMPT_PREVIEW:'],
    },
    {
        'name': 'round-trip generated Full KDSL structural pass',
        'command': ['kdsl_packet_roundtrip.py', 'examples/packet/normalization-source.example.md'],
        'expected': 0,
        'stdout_contains': [
            'STRUCTURAL_ROUND_TRIP_RESULT:',
            'STATUS: structural_pass',
            'EXECUTABLE: no',
            'SEMANTIC_EQUIVALENCE: not_proven',
            'EXECUTION_AUTHORITY: none',
        ],
        'stdout_not_contains': ['\nKDSL_PROMPT:', '\nP1:', '\nP1L:'],
    },
    {
        'name': 'round-trip generated P1 blocked',
        'command': ['kdsl_packet_roundtrip.py', 'examples/packet/normalization-p1-source.example.md'],
        'expected': 1,
        'stdout_contains': [
            'STATUS: blocked',
            'EXECUTABLE: no',
            'SEMANTIC_EQUIVALENCE: not_proven',
            'P1/P1L unresolved target remains blocked',
        ],
        'stdout_not_contains': ['\nKDSL_PROMPT:', '\nP1:'],
    },
    {
        'name': 'round-trip invalid Packet rejected',
        'command': ['kdsl_packet_roundtrip.py', 'tools/validator/samples/sample_packet_normalized.md'],
        'expected': 2,
        'stdout_contains': ['STATUS: fail'],
        'stdout_not_contains': ['STATUS: structural_pass'],
    },
    {
        'name': 'round-trip provided normalization structural pass',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_normalization_valid.md',
        ],
        'expected': 0,
        'stdout_contains': ['STATUS: structural_pass', 'all Packet fields accounted in MAP'],
    },
    {
        'name': 'round-trip source mutation detects digest mismatch',
        'command': [
            'kdsl_packet_roundtrip.py',
            'samples/sample_roundtrip_source_mutated.md',
            'samples/sample_roundtrip_normalization_valid.md',
        ],
        'expected': 2,
        'stdout_contains': ['source digest mismatch'],
    },
    {
        'name': 'round-trip malformed digest rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_bad_digest.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
    },
    {
        'name': 'round-trip exact string loss detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_missing_exact.md',
        ],
        'expected': 2,
        'stdout_contains': ['exact strings missing from PRESERVE'],
    },
    {
        'name': 'round-trip protected wording loss detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_missing_protected.md',
        ],
        'expected': 2,
        'stdout_contains': ['protected wording missing from PRESERVE'],
    },
    {
        'name': 'round-trip preserved order mutation detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_order_changed.md',
        ],
        'expected': 2,
        'stdout_contains': ['ordered fields missing or changed'],
    },
    {
        'name': 'round-trip preview FLOW order mutation detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_preview_order_changed.md',
        ],
        'expected': 2,
        'stdout_contains': ['FLOW order changed in preview'],
    },
    {
        'name': 'round-trip authority widening detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_authority_widened.md',
        ],
        'expected': 2,
        'stdout_contains': ['authority rail missing or widened in preview: push'],
    },
    {
        'name': 'round-trip MAP omission rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_map_omission.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
    },
    {
        'name': 'round-trip result schema loss detected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_result_schema_lost.md',
        ],
        'expected': 2,
        'stdout_contains': ['result schema missing from preview'],
    },
    {
        'name': 'round-trip semantic equivalence claim rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_semantic_claim.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
    },
    {
        'name': 'round-trip executable marker rejected',
        'command': [
            'kdsl_packet_roundtrip.py',
            'examples/packet/normalization-source.example.md',
            'samples/sample_roundtrip_executable_marker.md',
        ],
        'expected': 2,
        'stdout_contains': ['normalization artifact failed checker'],
        'stdout_not_contains': ['STATUS: structural_pass'],
    },
]


def resolve_command(command):
    script = ROOT / command[0]
    args = []
    for item in command[1:]:
        if item.startswith('samples/'):
            args.append(str(ROOT / item))
        elif item.startswith('examples/'):
            args.append(str(REPO_ROOT / item))
        else:
            args.append(item)
    return [sys.executable, str(script), *args]


def run_sample(sample):
    proc = subprocess.run(
        resolve_command(sample['command']),
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
    )
    expected_code = proc.returncode == sample['expected']
    contains = sample.get('stdout_contains', [])
    excludes = sample.get('stdout_not_contains', [])
    contains_ok = all(value in proc.stdout for value in contains)
    excludes_ok = all(value not in proc.stdout for value in excludes)
    ok = expected_code and contains_ok and excludes_ok
    status = 'PASS' if ok else 'FAIL'
    command_text = 'python tools/validator/' + ' '.join(sample['command'])
    print(f"{status}: {sample['name']}")
    print(f"  cmd: {command_text}")
    print(f"  expected: {sample['expected']}")
    print(f"  actual: {proc.returncode}")
    if contains:
        print(f"  stdout_contains: {contains}")
    if excludes:
        print(f"  stdout_not_contains: {excludes}")
    if not ok:
        missing = [value for value in contains if value not in proc.stdout]
        present = [value for value in excludes if value in proc.stdout]
        if missing:
            print(f"  missing stdout values: {missing}")
        if present:
            print(f"  prohibited stdout values: {present}")
        if proc.stdout:
            print('  stdout:')
            print(indent(proc.stdout.rstrip()))
        if proc.stderr:
            print('  stderr:')
            print(indent(proc.stderr.rstrip()))
    return ok


def indent(text):
    return '\n'.join('    ' + line for line in text.splitlines())


def main():
    failed = 0
    for sample in SAMPLES:
        if not run_sample(sample):
            failed += 1
    print('SUMMARY:')
    print(f'  total: {len(SAMPLES)}')
    print(f'  failed: {failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
