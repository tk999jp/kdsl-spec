from pathlib import Path

path = Path('.github/scripts/apply_packet_normalization_ownership.py')
text = path.read_text(encoding='utf-8')

redundant = """replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'semantic_equivalence:not_proven固定 in v0.1 candidate',
    'semantic_equivalence:not_proven固定 in v0.1 draft',
)
"""
count = text.count(redundant)
if count != 1:
    raise SystemExit(f'redundant wording replacement block count: {count}')
text = text.replace(redundant, '')

old_manifest = """replace_once(
    'spec/manifest.md',
    'Packet validator実装/期待結果\nnormalization round-trip証拠',
    'Packet validator実装/期待結果\nnormalization contract/lint ownership整合\nnormalization validator/mapper/round-trip証拠',
)
"""
new_manifest = """replace_once(
    'spec/manifest.md',
    'sample expectation runner確認\npublic-facing guide確定',
    'sample expectation runner確認\nPacket validator実装/期待結果\nnormalization contract/lint ownership整合\nnormalization validator/mapper/round-trip証拠\npublic-facing guide確定',
)
"""
count = text.count(old_manifest)
if count != 1:
    raise SystemExit(f'manifest stable-dependency block count: {count}')
text = text.replace(old_manifest, new_manifest)

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_normalization_ownership.py').unlink()
