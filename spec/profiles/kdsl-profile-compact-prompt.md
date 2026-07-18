# KDSL Profile: compact-prompt

## 目的

一般LLM、Project instructions、単体instruction向けpromptを、漢字圧縮を維持したまま短く再構成する。

```text
format: KDSL
profile: compact-prompt
mode: min
safety: normal
language: ja
```

## 標準構造

```text
目的:
材料:
出力:
規則:
確認:
```

一字aliasは既定にしない。本文も助詞削減・重複統合・漢字語幹化・条件記号化する。

## 既定

```text
漢字圧縮:=維持
英語KEY:=無指定時禁止
KDSL-Intl:=明示指定時のみ
安全契機:=入力で明示された重大条件だけ保持
```

## 開発promptとの境界

実装、repo操作、runtime確認、複数file変更を含む場合は `profile: dev-prompt` を使用する。ただしprofile変更で漢字圧縮を解除しない。

```text
compact-prompt→dev-prompt
変更:=作業情報量／構造KEY
不変:=漢字圧縮identity
```

## 変換例

```text
目的:
技術記事から公開meta生成

材料:
記事本文のみ

出力:
120字要約／主要テーマ3件／SEO title3件

規則:
本文外事実追加禁止／誇張禁止／日本語

確認:
指定形式のみ／各項目短文
```

## lint

```text
目的／材料／出力／規則／確認の欠落なし
英語構造KEY既定化なし
漢字optional化なし
旧CompactPrompt漢字別名なし
本文漢字圧縮あり
安全条件自動追加なし
```
