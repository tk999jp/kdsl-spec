format: KDSL
profile: compact-prompt
mode: min
safety: lock-critical
lexicon: standard

KDSL-CP:
Goal: first goal
Goal: second goal
Input: source_text
Output:
- concise summary
Guard:
- 入力外事実追加禁止
Check:
- required blocks present
