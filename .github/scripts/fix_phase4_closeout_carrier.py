from pathlib import Path

path = Path('.github/scripts/apply_phase4_closeout.py')
text = path.read_text(encoding='utf-8')
old = '''replace_once(
    'docs/project-status.md',
    '    - packet\\n    - normalization',
    '    - packet\\n    - packet-semantic\\n    - normalization',
)
'''
new = '''replace_once(
    'docs/project-status.md',
    '    - safety-semantics\\n    - r1c\\n    - packet\\n    - normalization\\n    - all',
    '    - safety-semantics\\n    - r1c\\n    - packet\\n    - packet-semantic\\n    - normalization\\n    - all',
)
'''
if text.count(old) != 1:
    raise SystemExit('wrapper-target carrier anchor count mismatch: ' + str(text.count(old)))
path.write_text(text.replace(old, new, 1), encoding='utf-8')
