# Validator Design

目的: KDSL / R1 / Template をPython等で機械検査するための設計置き場。

status: design-draft
implementation: not_started

## 位置づけ

```text
Validator:=形式/整合性/欠落/権限衝突を検査する補助器
Validator != 承認者
Validator != Runtime確認者
Validator != 要件判断者
Validator != D禁止解除者
```

## 目的

```text
KDSL_PROMPTの必須要素欠落検出
Template参照の未読/未定義検出
R1/KDSL_RESULTの必須block欠落検出
RT:v根拠の不正検出
NEXT/COMMIT権限混同検出
EVIDENCEの観測/推論/未観測/未確認分離検査
AUTHORITYのcommit/push/release衝突検査
```

## 非目的

```text
AIの判断を代行しない
ユーザー承認を代行しない
実機Runtime確認を代行しない
仕様変更の可否を判断しない
D禁止を解除しない
曖昧ログの意味を断定しない
```

## 想定構成

```text
tools/validator/
  README.md
  r1-validator-design.md
  kdsl-template-lint-design.md
```

## 設計方針

```text
最初は実装しない
検査項目を仕様として固定しすぎない
R1 validatorを優先
Template lintは未読/未定義/権限衝突を優先
KDSL parserは過剰に厳密化しない
Markdown + code block + key-value風blockの軽量検査から始める
```

## 検査レベル

```text
ERROR: safety gate破損/権限事故/RT:v誤認/必須block欠落
WARN: 曖昧/弱化/推奨block欠落
INFO: 任意改善/表記揺れ
```

## Safety first

```text
validator未実行→pass扱禁止
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
validator failure時→該当箇所を修正またはU確認
```
