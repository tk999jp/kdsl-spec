from pathlib import Path

path = Path('.github/scripts/apply_r1c_roundtrip_closeout.py')
text = path.read_text(encoding='utf-8')
old = """replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    'status: review-candidate\\ncanonical: no',
    'status: v2-draft adopted\\ncanonical: v2-draft subordinate',
)
"""
new = """replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    '# R1C Compact Result Schema v0.1 Draft\\n\\nstatus: review-candidate\\ncanonical: no',
    '# R1C Compact Result Schema v0.1 Draft\\n\\nstatus: v2-draft adopted\\ncanonical: v2-draft subordinate',
)
"""
count = text.count(old)
if count != 1:
    raise SystemExit(f'R1C schema header replacement block count: {count}')
path.write_text(text.replace(old, new), encoding='utf-8')
Path('.github/scripts/fix_r1c_roundtrip_closeout.py').unlink()
