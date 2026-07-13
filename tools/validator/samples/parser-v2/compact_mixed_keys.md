format: KDSL
profile: compact-prompt
mode: min
safety: lock-critical
lexicon: standard

KDSL-CP:
Goal: mixed-key warning case
Input: source_text
Output:
- concise summary
Guard:
- 入力外事実追加禁止
Check:
- required blocks present
目: kanji structural key retained for warning
