# Task Template: Docs／State Closeout

```text
用途:=Uが明示した完成機能の状態だけをdocs／stateへAgent反映
非用途:=独立Phase生成／追加review／新規roadmap作成
```

通常は `KDSL_PROMPT＋K1` の最小構成を使用する。

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

局面: {{完成機能}}
目的: {{確認済み結果を指定docs／stateへ反映}}
成功条件: 観測済み内容だけ記録／未確認反転なし／code変更なし
根拠: {{実装commit／test結果／U実機観測}}
正本: {{repo／branch／baseline}}
権限: 読取／対象docs編集=可、commit／push={{可否または承認待}}
承認境界: {{必要操作の境界}}
対象: {{更新対象docs／state}}
非対象: code／新規仕様／次Phase設計／未依頼hardening
作業: 根拠確認→対象docs更新→diff確認→K1未完=なしまで再帰
試験: git diff --check／git diff --name-status
検証: 対象外差分なし／未観測事項なし／build・test pass != RT:v
停止条件: baseline不一致／根拠不足／code・仕様変更必要／必要権限なし
報告: R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完: 根拠確認／docs更新／diff確認
検証: 未実行
実機: 不要
次: 根拠確認
停止理由: なし
```

```text
closeoutだけを独立Phase化禁止
成果報告修正だけの再run禁止
K1更新→scope／課題追加禁止
未観測事項を確認済扱禁止
次期roadmap自動追加禁止
```