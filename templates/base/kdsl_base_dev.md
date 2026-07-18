# KDSL Base Dev Prompt Template v3.1-kanji-agent

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

局面:
目的:
成功条件:
根拠:
正本:
権限:
承認境界:
対象:
非対象:
作業:
試験:
検証:
停止条件:
報告: R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完: {{作業一覧}}
検証: 未実行
実機: {{不要|未確認}}
次: 調査
停止理由: なし
```

基本:

```text
不可侵:=意味保持／要件保持／明示制約保持
最適化:=漢字圧縮>Agent完走>明示scope完走>必要最小限安全
共有材判可→AI丸投禁止
U観測>AI推測
1機能=1Phase
内部Slice完了→停止理由禁止
```

Agent:

```text
K1確認→未完選択→明示権限照合→実行→検証→K1更新→未完ありなら再帰
K1更新→目的／対象／権限変更禁止
必要操作=承認待→境界直前まで実行
```

厳密handoff／中断再開時のみ:

```text
PF1参照→P1L生成→K1へrun／契約／baseline追加
P1:=任意短縮／P1Lと併記禁止
```

安全:

```text
明示criticalのみ保持
U未指定gate追加禁止
安全理由scope／Phase／architecture拡張禁止
追加hardening混入禁止
```

報告:

```text
KDSL_RESULT:
状態:
局面:
要約:
変更:
理由:
実行:
検証:
実機:
危険:
次:
commit:
```
