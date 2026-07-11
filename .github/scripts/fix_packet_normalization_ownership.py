from pathlib import Path

path = Path('.github/scripts/apply_packet_normalization_ownership.py')
text = path.read_text(encoding='utf-8')
old = """replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'semantic_equivalence:not_proven固定 in v0.1 candidate',
    'semantic_equivalence:not_proven固定 in v0.1 draft',
)
"""
count = text.count(old)
if count != 1:
    raise SystemExit(f'redundant wording replacement block count: {count}')
path.write_text(text.replace(old, ''), encoding='utf-8')
Path('.github/scripts/fix_packet_normalization_ownership.py').unlink()
