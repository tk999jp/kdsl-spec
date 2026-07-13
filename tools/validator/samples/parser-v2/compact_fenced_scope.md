# CompactPrompt fenced-scope fixture

```text
format: KDSL
profile: compact-prompt
mode: min
safety: lock-critical
lexicon: standard

KDSL-CP:
Goal: fenced CompactPrompt scope
Input: source_text
Output:
- concise summary
Guard:
- 入力外事実追加禁止
Check:
- required blocks present
```

## Notes

This note mentions repository branch commit push implementation and must remain outside the CompactPrompt scope.
