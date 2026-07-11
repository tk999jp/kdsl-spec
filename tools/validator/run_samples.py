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
    ok = proc.returncode == sample['expected']
    status = 'PASS' if ok else 'FAIL'
    command_text = 'python tools/validator/' + ' '.join(sample['command'])
    print(f"{status}: {sample['name']}")
    print(f"  cmd: {command_text}")
    print(f"  expected: {sample['expected']}")
    print(f"  actual: {proc.returncode}")
    if not ok:
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
