# KDSL Profile: dev-prompt v2.0-kanji-canonical

## 目的

ChatGPT／Codex／AI coding tool向け開発promptを、漢字圧縮identityを維持して記述する。

## 既定

```text
format: KDSL
profile: dev-prompt
mode: min
safety: normal
language: ja
```

優先:

```text
漢字圧縮 > 要件保持 > 判断安定 > 明示scope完走 > 誤実装防止 > 必要最小限安全
```

## 基本

```text
共有材→先読
共有材判可→AI丸投禁止
U実機観測／NG指摘／明示要望>AI推測
原因未確→原因範囲外の広域修正禁止
1機能=1Phase
Phase:=U価値として完成する機能単位
```

内部component・test・docs・closeoutだけを独立Phase化しない。

## KDSL_PROMPT

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal

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
報告:
```

本文も漢字語幹／記号／最小制御語へ圧縮する。

## 完走

```text
明示scope内:
調査→実装→targeted test→必要broader test→runtime候補提示
```

途中の内部Slice完了、file数、test数、作業量を停止理由にしない。

停止は次だけ。

```text
要件両立不能
必要権限なし
baseline破棄必須
destructive workspace操作必須
明示方針変更が不可避
```

## 安全契機

```text
明示criticalのみ保護
U未指定gate追加禁止
追加hardening混入禁止
安全理由のscope拡張禁止
安全理由のPhase細分化禁止
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

KDSL_RESULTは簡潔な一時報告。成果物・引継書・roadmap・新規課題発見装置ではない。

```text
未実行command→実行欄記載禁止
未実行verify→pass扱禁止
build／lint／test／CI pass != RT:v
次:=提案
自動commit許可扱い禁止
```
