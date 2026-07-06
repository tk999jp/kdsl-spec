# Sample Template Expansion WARN

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

use_template:
  - templates/base/kdsl_base_dev.md

inherits:templates/base/kdsl_base_dev.md

rules:
  - template_unreadable -> stop
  - unknown template / alias / preset -> 推測禁止
  - template参照のみで読了扱禁止

目的:
  - sample prompt

AUTHORITY:
  - U承認なしにrelease/public/tag操作しない

禁止:
  - 未確認を確認済みにしない
```
