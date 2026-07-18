# Task Template: 調査のみ

```text
用途:=共有材／repo／log／差分をAgent確認し、実装せず判断材料を返す
```

通常は `KDSL_PROMPT＋K1` の最小構成を使用する。中断再開／handoff時だけP1Lを追加する。

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

局面: {{調査名}}
目的: {{明らかにする事項}}
成功条件: 観測事実／推定／未確認分離／原因候補限定／実装なし
根拠: {{共有file／log／screenshot／repo}}
正本: {{repo／branch／baseline}}
権限: 読取=可／編集=不可／試験={{必要時可}}
承認境界: 編集要求発生時
対象: {{調査対象}}
非対象: file編集／commit／push／release／未依頼改善設計
作業: 共有材先読→必要箇所確認→事実整理→質問へ直接回答
試験: {{必要時のみread-only検証}}
検証: 未実行検証をpass扱禁止／検索失敗で不存在断定禁止
停止条件: 資料取得不能／正本矛盾／編集またはscope変更必須
報告: R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完: 共有材確認／必要箇所確認／事実整理／報告
検証: 未実行
実機: 不要
次: 共有材確認
停止理由: なし
```

```text
調査→実装へ自動拡張禁止
潜在risk→追加課題生成禁止
K1更新→調査scope変更禁止
未確認→断定禁止
```