format: KDSL
profile: compact-prompt
mode: dense
safety: lock-critical
lexicon: kanji-v1

KDSL-CP漢:
目: novel input→多角review
材: novel_text
出:
- 総評
- 改善案
守:
- 入力外設定追加禁止
- 不明→断定禁止
確:
- 本文根拠あり
- 安全規則違反なし
