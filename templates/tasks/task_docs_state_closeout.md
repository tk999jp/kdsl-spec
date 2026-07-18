# Task Template: Docs／State Closeout

```text
用途:=Uが明示した完成機能の状態だけをdocs／stateへ反映
非用途:=独立Phase生成／追加review／新規roadmap作成
```

## Instance

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal

局面: {{完成機能}}
目的: {{確認済み結果を指定docs／stateへ反映}}
成功条件:
- 観測済み内容だけ記録
- 未確認／未実行を反転しない
- code変更なし

根拠:
- {{実装commit／test結果／U実機観測}}

正本:
- repo: {{repo}}
- branch: {{branch}}
- baseline: {{HEAD}}

対象:
- {{更新対象docs／state}}

非対象:
- code
- 新規仕様
- 次Phase設計
- 未依頼hardening

作業:
1. 根拠確認
2. 対象docs／stateだけ更新
3. diff確認
4. KDSL_RESULTで簡潔報告

検証:
- git diff --check
- git diff --name-status
- 対象外差分なし
- build／test pass != RT:v

停止条件:
- baseline不一致
- 根拠不足で完成状態を記録不能
- code／仕様変更が必要
```

## 禁止

```text
closeoutだけを独立Phase化禁止
成果報告修正だけの再run禁止
未観測事項を確認済扱禁止
次期roadmap自動追加禁止
```
