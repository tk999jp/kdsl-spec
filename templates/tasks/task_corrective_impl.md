# Task Template: 修正実装

```text
用途:=明示scope内の不具合修正を調査→実装→試験→検証まで同一Phaseで完走
```

## Instance

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal

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

検証:
- {{targeted test}}
- {{必要なbuild／broader test}}
- 未実行項目→pass扱禁止
- build／test pass != RT:v

停止条件:
- 正本／branch／baselineが指定と競合
- U要件同士が両立不能
- 明示scope外の仕様変更が不可避

報告:
KDSL_RESULTで依頼scope内の結果だけを簡潔報告
```

## 禁止

```text
内部component別Phase化禁止
未依頼hardening追加禁止
安全理由scope拡張禁止
通常bug修正を承認待へ自動昇格禁止
未確認→確認済扱禁止
command／path／API名変換禁止
```
