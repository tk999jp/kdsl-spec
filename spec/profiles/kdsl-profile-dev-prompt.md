# KDSL Profile: dev-prompt v3.1-kanji-agent

## 目的

ChatGPT／Codex／AI coding tool向け開発promptを、漢字圧縮identityを維持し、明示scopeをAgent完走させる。

```text
Agent goal:=U明示scopeを必要最小契約で調査→実装→検証→完了
```

## 既定

```text
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required
language: ja
```

優先:

```text
漢字圧縮 > 要件保持 > Agent完走 > 判断安定 > 明示scope完走 > 誤実装防止 > 必要最小限安全
```

## KDSL_PROMPT

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
未完:
検証: 未実行
実機: 不要|未確認
次: 調査
停止理由: なし
```

通常投入は `KDSL_PROMPT＋K1`。本文も漢字語幹／記号／最小制御語へ圧縮する。

## 厳密契約

次の場合だけP1L／PF1を追加する。

```text
中断再開
複数agent handoff
長時間run
複雑承認境界
project既定再利用
U明示
```

```text
PF1参照→P1L生成→K1初期化
```

P1は任意短縮。P1Lと同時記載しない。可逆性実装前は正本扱いしない。

## Agent再帰

```text
K1確認
→未完選択
→明示権限照合
→実行
→検証
→K1更新
→完了条件判定
→未完ありなら再帰
```

明示scope内:

```text
調査→実装→targeted test→必要broader test→runtime候補提示
```

途中の内部Slice完了、file数、test数、作業量、途中commitを停止理由にしない。

## 停止

```text
明示停止条件成立
必要操作権限=承認待／不可
要件両立不能
必要正本なし
baseline破棄必須
明示scope変更必須
```

必要操作が承認待なら境界直前まで進めてK1を更新する。

## K1完了

```text
状態=完了
→未完=なし
→検証=成功
→実機要否=不要なら実機=不要
→実機要否=要なら実機=確認済
```

中断再開／handoff時だけ `run／契約／baseline／PF1` をK1へ追加する。

## 安全契機

```text
明示criticalのみ保持
U未指定gate追加禁止
追加hardening混入禁止
安全理由scope拡張禁止
安全理由Phase細分化禁止
K1更新による未依頼課題追加禁止
```

## D禁止限定

D禁止は、要件変更・方針反転・rollback／revert・未push破棄・public履歴改変・破壊的data変更に限定する。

通常bug修正、既存仕様内補正、targeted test、内部整理、明示scope内完成をD禁止へ自動昇格しない。

## KDSL_RESULT

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

KDSL_RESULTは簡潔な一時報告。Agent契約複製、成果物、引継書、roadmap、新規課題発見装置ではない。

```text
未実行command→実行欄記載禁止
未実行verify→pass扱禁止
build／lint／test／CI pass != RT:v
次:=提案
自動commit許可扱い禁止
```

## 検証境界

```text
形式lint pass!=Codex Agent実効性
Codex再帰／再開／承認停止未確認→未証明
```