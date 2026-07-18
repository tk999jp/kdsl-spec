# Task Template: Docs／State Closeout

```text
用途:=Uが明示した完成機能の状態だけをdocs／stateへAgent反映
非用途:=独立Phase生成／追加review／新規roadmap作成
```

## Agent展開

本template使用時、`templates/base/kdsl_base_dev.md`のP1L／P1／K1／PF1 blockを同一promptへ展開する。

```text
実行方式:=agent再帰
権限:=読取／編集／試験=可、stage以降=U／PF1明示値
対象:=指定docs／stateのみ
```

## Instance

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

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

権限: P1L参照
承認境界: {{commit／push等の境界}}

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
4. K1未完=なしまで再帰

試験:
- git diff --check
- git diff --name-status

検証:
- 対象外差分なし
- 未観測事項なし
- build／test pass != RT:v

停止条件:
- baseline不一致
- 根拠不足で完成状態を記録不能
- code／仕様変更が必要
- 必要操作権限=承認待／不可

報告: R1
```

## 禁止

```text
closeoutだけを独立Phase化禁止
成果報告修正だけの再run禁止
K1更新によるscope／課題追加禁止
未観測事項を確認済扱禁止
次期roadmap自動追加禁止
```
