import re
from pathlib import Path

path = Path('.github/scripts/apply_packet_normalization_validator_closeout.py')
text = path.read_text(encoding='utf-8')

header_pattern = re.compile(
    r"""replace_once\(\n    'spec/lint/kdsl-packet-normalization-lint\.md',\n    'validator: first-slice integration pending',\n    'validator: first-slice integrated',\n\)\n"""
)
header_replacement = r"""replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'canonical: v2-draft\nvalidator: first-slice integration pending\nscope: kdsl-packet-normalization@0.1-draft',
    'canonical: v2-draft\nvalidator: first-slice integrated\nscope: kdsl-packet-normalization@0.1-draft',
)
"""
text, count = header_pattern.subn(lambda _: header_replacement, text, count=1)
if count != 1:
    raise SystemExit(f'normalization lint closeout header block count: {count}')

path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_normalization_validator_closeout.py').unlink()
