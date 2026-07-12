from pathlib import Path

path = Path('.github/scripts/apply_phase4_closeout.py')
text = path.read_text(encoding='utf-8')

patches = [
    (
        '''replace_once(
    'docs/project-status.md',
    '    - packet\\n    - normalization',
    '    - packet\\n    - packet-semantic\\n    - normalization',
)
''',
        '''replace_once(
    'docs/project-status.md',
    '    - safety-semantics\\n    - r1c\\n    - packet\\n    - normalization\\n    - all',
    '    - safety-semantics\\n    - r1c\\n    - packet\\n    - packet-semantic\\n    - normalization\\n    - all',
)
''',
        'wrapper-target carrier anchor',
    ),
    (
        "replace_once('spec/lint/kdsl-packet-lint.md', 'validator: not implemented', 'validator: Phase 4 strict first slice integrated')\n",
        '''replace_once(
    'spec/lint/kdsl-packet-lint.md',
    'status: v2-draft adopted\\ncanonical: v2-draft\\nvalidator: not implemented\\nscope: kdsl-packet@0.1-draft / BASE / TASK / FLOW',
    'status: v2-draft adopted\\ncanonical: v2-draft\\nvalidator: Phase 4 strict first slice integrated\\nscope: kdsl-packet@0.1-draft / BASE / TASK / FLOW',
)
''',
        'Packet lint metadata carrier anchor',
    ),
]

for old, new, label in patches:
    if text.count(old) != 1:
        raise SystemExit(label + ' count mismatch: ' + str(text.count(old)))
    text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
