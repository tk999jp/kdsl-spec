format: KDSL
profile: compact-prompt
mode: min
safety: lock-critical
lexicon: standard

KDSL-CP:
Goal: article input→公開用メタ情報作成
Input: article_text
Output:
- 要約:120字以内
- SEOタイトル案:5件
Guard:
- 入力外事実追加禁止
- 不明→断定禁止
Check:
- 字数/件数確認
- Guard違反なし
