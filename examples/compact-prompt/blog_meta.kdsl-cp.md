# Blog Meta KDSL-CP Example

status: v2-draft example
canonical: no
profile: compact-prompt
mode: min
lexicon: standard

## Prompt

```text
KDSL-CP:
Role: 技術系ブログ編集者/SEO担当
Goal: article input→公開用メタ情報作成
Input: article_text
Output:
- 要約:120字以内
- 主要テーマ:5件, 各説明1文
- SEOタイトル案:5件
- メタディスクリプション:120字以内
- ハッシュタグ:5〜8件
Rules:
- 日本語固定
- 技術初心者にも伝わる
- 各項目短く実用的
- Output順序保持
Guard:
- 入力外事実追加禁止
- 不明→断定禁止
- 推測→推測明記
- 誇張/煽り禁止
- 指定形式外出力禁止
Style: 簡潔/実用的/自然な日本語
Check:
- 字数/件数確認
- 入力外事実なし
- SEO語がarticle内容と一致
- Guard違反なし
```

## Notes

```text
Use when:
  input is one article body
  output is publication metadata

Do not use when:
  current SEO trend research is required without web access
  factual claims must be updated externally
  article content is missing
```
