import re
from pathlib import Path

path = Path('.github/scripts/apply_packet_normalization_validator.py')
text = path.read_text(encoding='utf-8')
pattern = re.compile(
    r"""replace_once\(\n    'spec/lint/kdsl-packet-normalization-lint\.md',\n    'validator: not implemented',\n    'validator: first-slice integration pending',\n\)\n"""
)
replacement = r"""replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'canonical: v2-draft\nvalidator: not implemented\nscope: kdsl-packet-normalization@0.1-draft',
    'canonical: v2-draft\nvalidator: first-slice integration pending\nscope: kdsl-packet-normalization@0.1-draft',
)
"""
text, count = pattern.subn(lambda _: replacement, text, count=1)
if count != 1:
    raise SystemExit(f'normalization lint status block count: {count}')
path.write_text(text, encoding='utf-8')
Path('.github/scripts/fix_packet_normalization_validator.py').unlink()
