# KDSL Profile — dev-prompt

## 既定

```text
format: KDSL
profile: dev-prompt
mode: min
safety: normal
language: ja
```

AI coding tool向けpromptは`KDSL_PROMPT:`を先頭とする。Agentの状態管理はKDSL言語本体と分離し、必要な実行環境でだけ追加する。

## 最小例

```text
KDSL_PROMPT:
局面: 表示単位修正
目的: Bytes選択→実byte数表示
成功条件: KB／MB計算・表示・切替不変
対象: 表示処理／関連test
作業: 原因特定→必要実装・test補正→対象test
検証: 対象test実行／結果報告
```

`目的／成功条件／対象／作業／検証`以外は、依頼内容に必要な場合だけ追加する。明示された禁止／権限／停止／実機条件は保持する。作業に無関係な承認gate、Phase、hardeningを追加しない。

## Agent補助（必要時）

```text
K1:
状態: 計画|実行中|検証中|実機待|完了|停止|失敗
未完:
検証: 未実行|一部|成功|失敗
実機: 不要|未確認|確認済
次:
```

通常の短い変換ではK1不要。中断再開・複数Agent引継・長時間実行等で状態共有が実際に必要な場合のみ使用。K1更新で目的／対象／権限を変更しない。作業一覧の重複展開を避け、初期値は`未完: 作業全件`などの意味参照可。

## 限定D禁止

U要件変更／明示方針反転／rollback・revert／未push差分破棄／public履歴改変／公開済tag・Release Assets変更／破壊的data形式変更に限り、必要なら現行維持案と変更案を示しU判断待。通常bug修正／targeted test／内部整理は自動昇格しない。

## 報告

`報告: R1`で十分な場合は長い出力契約の再記述をしない。R1は簡潔結果であり、roadmapや実行許可ではない。
