# KDSL CompactPrompt Kanji Aliases v0.1-draft

status: v2-draft
scope: KDSL-CP dense-ja / Japanese compact prompt aliases

## 1. Purpose

This document defines kanji aliases for KDSL-CP.

The goal is to increase compression while keeping the prompt understandable for Japanese LLM and Project file use.

```text
目的: 高圧縮 + safety gate保持 + 低学習cost
```

These aliases are for KDSL-CP dense-ja. They do not automatically replace KDSL-Core canonical field names or protected words.

## 2. Standard block aliases

```text
KDSL-CP:min:
  Role / Goal / Input / Output / Rules / Guard / Style / Check

KDSL-CP:dense-ja:
  役 / 目 / 材 / 出 / 則 / 守 / 調 / 確
```

Definitions:

```text
役 = Role
目 = Goal
材 = Input / source material
出 = Output
則 = Rules
守 = Guard / safety rules
調 = Style / tone / audience / language
確 = Check / final self-lint
```

## 3. Minimal kanji vocabulary

```text
U   = ユーザー
材  = 入力材料 / source
出  = 出力 / output
型  = 形式 / format
要  = 必須 / 要件
禁  = 禁止カテゴリ
不  = 不明 / unknown
推  = 推測 / estimation
実  = 事実 / fact
危  = リスク / risk
代  = 代替案 / alternative
条  = 条件 / condition
確  = 確認 / check
```

## 4. Safety constraints

Kanji aliases must not weaken protected words.

Do not shorten these:

```text
禁止
必須
未確認
未実行
承認
承認待
断定禁止
確認済扱禁止
実行済扱禁止
成功扱禁止
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v
KDSL_RESULT NEXT
KDSL_RESULT COMMIT
```

Important distinctions:

```text
禁 = 禁止カテゴリ名として可
禁止 = 禁止文型では保持推奨

不 = 不明
未確認 = 未確認のまま保持
未実行 = 未実行のまま保持

実 = 事実
実行 = 実行として保持

U = ユーザー
者 = 非推奨。第三者/対象者/行為者と混同しやすい。
```

## 5. Recommended dense-ja form

```text
KDSL-CP漢:
役:
目:
材:
出:
則:
守:
調:
確:
```

Example:

```text
KDSL-CP漢:
役: 技術系ブログ編集者/SEO担当
目: 記事材→公開用メタ情報作成
材: article_text
出:
- 要約:120字以内
- 主要テーマ:5件
- SEOタイトル案:5件
則:
- 日本語固定
- 技術初心者にも伝わる
守:
- 材外実追加禁止
- 不→断定禁止
- 誇張/煽り禁止
調: 簡潔/実用的/自然な日本語
確:
- 字数/件数確認
- 材外実なし
- 守違反なし
```

## 6. Unknown alias policy

```text
unknown漢字alias推測禁止
alias意味変更禁止
Project filesでは語彙表または本file参照必須
単体promptでは必要aliasのみinline定義可
```

## 7. Non-application

These aliases do not automatically apply to:

```text
KDSL-Core canonical fields
KDSL_PROMPT
KDSL_RESULT
R1 full block names
path / command / URL / repo名 / branch名 / tag名 / file名 / API名
```

For path/file aliases, define explicit alias tables separately. Do not transform paths or file names implicitly.
