import re
from pathlib import Path

path = Path('.github/scripts/apply_packet_normalization_ownership.py')
text = path.read_text(encoding='utf-8')

redundant_pattern = re.compile(
    r"""replace_once\(\n    'spec/packet/kdsl-packet-normalization-contract\.md',\n    'semantic_equivalence:not_proven固定 in v0\.1 candidate',\n    'semantic_equivalence:not_proven固定 in v0\.1 draft',\n\)\n"""
)
text, count = redundant_pattern.subn('', text, count=1)
if count != 1:
    raise SystemExit(f'redundant wording replacement block count: {count}')

manifest_pattern = re.compile(
    r"""replace_once\(\n    'spec/manifest\.md',\n    'Packet validator実装/期待結果\\nnormalization round-trip証拠',\n    'Packet validator実装/期待結果\\nnormalization contract/lint ownership整合\\nnormalization validator/mapper/round-trip証拠',\n\)\n"""
)
manifest_replacement = r"""replace_once(
    'spec/manifest.md',
    'sample expectation runner確認\npublic-facing guide確定',
    'sample expectation runner確認\nPacket validator実装/期待結果\nnormalization contract/lint ownership整合\nnormalization validator/mapper/round-trip証拠\npublic-facing guide確定',
)
"""
text, count = manifest_pattern.subn(lambda _: manifest_replacement, text, count=1)
if count != 1:
    raise SystemExit(f'manifest stable-dependency block count: {count}')

readme_pattern = re.compile(
    r"""replace_once\(\n    'README\.md',\n    'Packet full YAML/semantic parser\\nPacket normalization transformer/round-trip proof',\n    'Packet full YAML/semantic parser\\nPacket normalization validator/mapper/round-trip proof',\n\)\n"""
)
readme_replacement = r"""replace_once(
    'README.md',
    'Packet full YAML/semantic parserなし\nPacket normalization transformer/round-trip proofなし',
    'Packet full YAML/semantic parserなし\nPacket normalization validator/mapper/round-trip proofなし',
)
"""
text, count = readme_pattern.subn(lambda _: readme_replacement, text, count=1)
if count != 1:
    raise SystemExit(f'README normalization-gap block count: {count}')

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_normalization_ownership.py').unlink()
