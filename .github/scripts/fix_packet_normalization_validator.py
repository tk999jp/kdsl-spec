import re
from pathlib import Path

path = Path('.github/scripts/apply_packet_normalization_validator.py')
text = path.read_text(encoding='utf-8')

status_pattern = re.compile(
    r"""replace_once\(\n    'spec/lint/kdsl-packet-normalization-lint\.md',\n    'validator: not implemented',\n    'validator: first-slice integration pending',\n\)\n"""
)
status_replacement = r"""replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'canonical: v2-draft\nvalidator: not implemented\nscope: kdsl-packet-normalization@0.1-draft',
    'canonical: v2-draft\nvalidator: first-slice integration pending\nscope: kdsl-packet-normalization@0.1-draft',
)
"""
text, count = status_pattern.subn(lambda _: status_replacement, text, count=1)
if count != 1:
    raise SystemExit(f'normalization lint status block count: {count}')

readme_pattern = re.compile(
    r"""replace_once\(\n    'README\.md',\n    'Normalization validator/mapper未実装\\nNormalization round-trip/property proofなし',\n    'Normalization validator/mapper first slice:=integration pending\\nNormalization round-trip/property proofなし',\n\)\n"""
)
readme_replacement = r"""replace_once(
    'README.md',
    'Packet normalization validator/mapper/round-trip proofなし',
    'Packet normalization validator/mapper first slice:=integration pending\nPacket normalization round-trip/property proofなし',
)
"""
text, count = readme_pattern.subn(lambda _: readme_replacement, text, count=1)
if count != 1:
    raise SystemExit(f'normalization README gap block count: {count}')

status_gap_pattern = re.compile(
    r"""replace_once\(\n    'docs/project-status\.md',\n    'Normalization validator/mapper未実装\\nNormalization round-trip/property proofなし',\n    'Normalization validator/mapper first slice:=integration pending\\nNormalization round-trip/property proofなし',\n\)\n"""
)
status_gap_replacement = r"""replace_once(
    'docs/project-status.md',
    'Packet Safety Gate state/evidence deep lint\nNormalization validator/mapper未実装\nNormalization round-trip/property proofなし\nPacket Safety Gate completeness/inheritance proof',
    'Packet Safety Gate state/evidence deep lint\nNormalization validator/mapper first slice:=integration pending\nNormalization round-trip/property proofなし\nPacket Safety Gate completeness/inheritance proof',
)
replace_once(
    'docs/project-status.md',
    'Packet full YAML/semantic parserなし\nNormalization validator/mapper未実装\nNormalization round-trip/property proofなし\nPacket Safety Gate completeness/inheritance proofなし',
    'Packet full YAML/semantic parserなし\nNormalization validator/mapper first slice:=integration pending\nNormalization round-trip/property proofなし\nPacket Safety Gate completeness/inheritance proofなし',
)
"""
text, count = status_gap_pattern.subn(lambda _: status_gap_replacement, text, count=1)
if count != 1:
    raise SystemExit(f'project-status normalization-gap block count: {count}')

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_normalization_validator.py').unlink()
