# KDSL Prompt Template Inheritance Example

status: draft-example
example_type: KDSL_PROMPT
core_spec: no

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

use_template:
  - templates/base/kdsl_base_dev.md

source_template:templates/base/kdsl_base_dev.md
expanded_from:templates/base/kdsl_base_dev.md

template_rules:
  - template_unreadable -> stop
  - unknown template / alias / preset -> 推測禁止
  - template参照のみで読了扱禁止

目的:
  - demonstrate explicit template inheritance

AUTHORITY:
  - U承認なしにrelease/public/tag/Release Assets操作しない

禁止:
  - KDSL-DP直接実行禁止
  - P1/P1L正規化前の実装指示扱い禁止
  - 未確認を確認済みにしない

停止条件:
  - referenced template unreadable
  - inherited rule cannot be confirmed

検証:
  - run template reference checker
  - run template expansion checker

KDSL_RESULT要求:
  - report with R1 fields
```
