from pathlib import Path


def insert_once(path: str, anchor: str, insertion: str) -> None:
    target = Path(path)
    text = target.read_text(encoding='utf-8')
    count = text.count(anchor)
    if count != 1:
        raise SystemExit(f'{path}: expected one anchor, got {count}: {anchor!r}')
    target.write_text(text.replace(anchor, insertion + anchor), encoding='utf-8')


insert_once(
    'tools/validator/kdsl_r1c.py',
    '\ndef main(argv):',
    '''\n\n# Phase 1 common parser adapter. Semantic validation remains in this module.\nfrom kdsl_parser_adapter import install_r1c\ninstall_r1c(globals())\n''',
)
insert_once(
    'tools/validator/kdsl_packet.py',
    '\ndef main(argv):',
    '''\n\n# Phase 1 common parser adapter. Semantic validation remains in this module.\nfrom kdsl_parser_adapter import install_packet\ninstall_packet(globals())\n''',
)
insert_once(
    'tools/validator/kdsl_packet_normalization.py',
    '\ndef main(argv):',
    '''\n\n# Phase 1 common parser adapter. Semantic validation remains in this module.\nfrom kdsl_parser_adapter import install_normalization\ninstall_normalization(globals())\n''',
)
insert_once(
    'tools/validator/kdsl_safety_gate.py',
    '\ndef main(argv):',
    '''\n\n# Phase 1 common parser adapter. Semantic validation remains in this module.\nfrom kdsl_parser_adapter import install_safety_gate\ninstall_safety_gate(globals())\n''',
)

review = Path('docs/reviews/kdsl-phase1-common-parser.md')
text = review.read_text(encoding='utf-8')
text = text.replace('status: implementation-candidate', 'status: branch-validation-pending', 1)
review.write_text(text, encoding='utf-8')

Path('.github/scripts/apply_phase1_parser.py').unlink()
