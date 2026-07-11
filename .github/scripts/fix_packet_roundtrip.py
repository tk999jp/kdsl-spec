import re
from pathlib import Path

path = Path('.github/scripts/apply_packet_roundtrip.py')
text = path.read_text(encoding='utf-8')

pattern = re.compile(
    r"""replace_once\(\n    'docs/project-status\.md',\n    'Normalization round-trip/property proofなし',\n    'Normalization structural round-trip first slice:=integration pending\\nNormalization semantic/property proofなし',\n\)\n"""
)
replacement = r"""replace_once(
    'docs/project-status.md',
    'Packet Safety Gate state/evidence deep lint\nNormalization round-trip/property proofなし\nPacket Safety Gate completeness/inheritance proof',
    'Packet Safety Gate state/evidence deep lint\nNormalization structural round-trip first slice:=integration pending\nNormalization semantic/property proofなし\nPacket Safety Gate completeness/inheritance proof',
)
replace_once(
    'docs/project-status.md',
    'Packet full YAML/semantic parserなし\nNormalization round-trip/property proofなし\nPacket Safety Gate completeness/inheritance proofなし',
    'Packet full YAML/semantic parserなし\nNormalization structural round-trip first slice:=integration pending\nNormalization semantic/property proofなし\nPacket Safety Gate completeness/inheritance proofなし',
)
"""
text, count = pattern.subn(lambda _: replacement, text, count=1)
if count != 1:
    raise SystemExit(f'round-trip project-status gap block count: {count}')

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_roundtrip.py').unlink()
