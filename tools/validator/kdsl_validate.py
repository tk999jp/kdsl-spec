import subprocess
import sys
from pathlib import Path

from kdsl_parser import DiagnosticBag, DocumentNode, load_text

CHECKER_SETS = {
    'r1': ['r1_required_blocks.py', 'r1_rt_basis.py', 'r1_authority_guard.py'],
    'prompt': ['kdsl_template_refs.py', 'kdsl_template_expansion.py'],
    'compact': ['kdsl_compact_prompt.py'],
    'safety-gate': ['kdsl_safety_gate.py'],
    'safety-semantics': ['kdsl_safety_semantics.py'],
    'r1c': ['kdsl_r1c.py', 'kdsl_r1c_optional.py'],
    'p1l': ['kdsl_p1l.py'],
    'p1': ['kdsl_p1.py'],
    'p1-contract': ['kdsl_p1_auto.py'],
    'packet': ['kdsl_packet.py'],
    'packet-semantic': ['kdsl_packet.py', 'kdsl_packet_semantic.py'],
    'normalization': ['kdsl_packet_normalization.py'],
    'all': [
        'r1_required_blocks.py',
        'r1_rt_basis.py',
        'r1_authority_guard.py',
        'kdsl_template_refs.py',
        'kdsl_template_expansion.py',
        'kdsl_compact_prompt.py',
        'kdsl_safety_gate.py',
        'kdsl_safety_semantics.py',
        'kdsl_r1c.py',
        'kdsl_r1c_optional.py',
        'kdsl_packet.py',
        'kdsl_packet_normalization.py',
    ],
}

TARGET_MARKERS = {
    'r1': ('KDSL_RESULT',),
    'r1c': ('KDSL_RESULT',),
    'safety-gate': ('SAFETY_GATES',),
    'safety-semantics': ('SAFETY_GATES',),
    'p1l': (),
    'p1': (),
    'p1-contract': (),
    'packet': ('PACKET_DRAFT',),
    'packet-semantic': ('PACKET_DRAFT',),
    'normalization': ('NORMALIZATION_DRAFT',),
    'all': ('KDSL_RESULT', 'SAFETY_GATES', 'PACKET_DRAFT', 'NORMALIZATION_DRAFT'),
}

TARGETS = (
    'r1, prompt, compact, safety-gate, safety-semantics, r1c, '
    'p1l, p1, p1-contract, packet, packet-semantic, normalization, all'
)


def parse_args(argv):
    target_mode = 'all'
    path = None
    index = 1
    while index < len(argv):
        arg = argv[index]
        if arg == '--target':
            if index + 1 >= len(argv):
                raise ValueError('--target requires one of: ' + TARGETS)
            target_mode = argv[index + 1]
            index += 2
            continue
        if path is None:
            path = arg
            index += 1
            continue
        raise ValueError('unexpected argument: ' + arg)
    if path is None:
        raise ValueError(
            'usage: python kdsl_validate.py [--target r1|prompt|compact|safety-gate|safety-semantics|r1c|p1l|p1|p1-contract|packet|packet-semantic|normalization|all] <file>'
        )
    if target_mode not in CHECKER_SETS:
        raise ValueError('unknown target: ' + target_mode)
    return target_mode, path


def run_parser_preflight(target_mode, target):
    markers = TARGET_MARKERS.get(target_mode, ())
    if not markers:
        return 0

    text = load_text(target)
    document = DocumentNode.parse(text)
    bag = DiagnosticBag()
    for issue in document.issues:
        bag.add_issue(issue)

    found = []
    for marker in markers:
        envelope = document.find_envelope(marker)
        if envelope is None:
            continue
        found.append(marker)
        for issue in envelope.issues:
            bag.add_issue(issue)

    print('PARSER_PREFLIGHT:')
    print('  target: ' + target_mode)
    print('  envelopes: ' + (','.join(found) if found else 'none'))
    print('  status: ' + ('fail' if bag.errors else ('warn' if bag.warnings else 'pass')))
    for item in bag.errors:
        print('  error: ' + item)
    for item in bag.warnings:
        print('  warning: ' + item)
    return bag.exit_code


def run_checker(root, checker, target):
    script = root / checker
    print('CHECK: ' + checker)
    proc = subprocess.run(
        [sys.executable, str(script), target],
        text=True,
        capture_output=True,
    )
    if proc.stdout:
        print(proc.stdout.rstrip())
    if proc.stderr:
        print('STDERR:')
        print(proc.stderr.rstrip())
    return proc.returncode


def main(argv):
    try:
        target_mode, target = parse_args(argv)
    except ValueError as exc:
        print(str(exc))
        return 2

    root = Path(__file__).resolve().parent
    final_code = run_parser_preflight(target_mode, target)

    print('TARGET: ' + target_mode)
    for checker in CHECKER_SETS[target_mode]:
        code = run_checker(root, checker, target)
        if code > final_code:
            final_code = code

    return final_code


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
