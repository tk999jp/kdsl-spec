# Task Template: 修正実装

```text
用途:=明示scope内の不具合修正を調査→実装→試験→検証まで同一PhaseでAgent完走
```

## Agent展開

本template使用時、`templates/base/kdsl_base_dev.md`のP1L／P1／K1／PF1 blockを同一promptへ展開し、placeholderを全て確定する。

```text
実行方式:=agent再帰
標準権限:=読取／編集／試験=可
stage／commit／push／release:=U／PF1明示値
public履歴／破壊操作:=U明示なしなら不可
```

## Instance

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

局面: {{機能名／修正名}}
目的: {{U価値としての完成状態}}
成功条件:
- {{実際に成立すべき動作}}
- {{既存正常動作を維持}}

根拠:
- {{U観測／log／code／diff}}

正本:
- repo: {{repo}}
- branch: {{branch}}
- baseline: {{HEADまたは確認方法}}

権限: P1L参照
承認境界: {{commit／push等の境界}}

対象:
- {{file／機能／操作}}

非対象:
- {{明示除外}}

作業:
1. 共有材／現実装確認→原因限定
2. 明示scope内で実装
3. targeted test追加／更新
4. 必要なbroader test実行
5. 差分再確認→不足時は同一Phase内で補正
6. K1未完=なしまで再帰

試験:
- {{targeted test}}
- {{必要なbroader test}}

検証:
- {{成功条件との対応}}
- 未実行項目→pass扱禁止
- build／test pass != RT:v

停止条件:
- 正本／branch／baselineが指定と競合
- U要件同士が両立不能
- 明示scope外の仕様変更が不可避
- 必要操作権限=承認待／不可

報告: R1
```

## 禁止

```text
内部component別Phase化禁止
未依頼hardening追加禁止
安全理由scope拡張禁止
通常bug修正を承認待へ自動昇格禁止
K1更新によるscope／権限変更禁止
未確認→確認済扱禁止
command／path／API名変換禁止
```
