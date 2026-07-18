# KDSL Lint Checklist v3.1-kanji-agent

## 合格必須

```text
漢字圧縮が第一
英語KEYへ退行なし
KEY翻訳だけで終了していない
本文が漢字語幹／記号／最小制御語化
元意味保持
明示禁止保持
未確認／未実行の反転なし
command／path／API名保持
AI推測安全条件追加なし
scope拡張なし
Phase／報告肥大化なし
```

## identity違反

```text
KDSLを言語中立frameworkとして再定義
漢字をoptional lexicon化
standard／Englishを無指定既定化
KDSL-Intlを本体化
安全契機を第一目的化
dev-promptで漢字圧縮解除
KDSL_PROMPTへ英語構造KEY必須化
Agent層をKDSL Coreより上位化
```

## 圧縮不足

```text
自然文の助詞・重複が大量残存
同義block重複
長い安全説明の再掲
GOAL→目的等のKEY翻訳だけ
KDSL_PROMPT／P1L／P1で同一内容を多重記載
```

## 安全過剰

```text
入力外risk追加
U未指定承認gate
通常改修high-risk化
安全理由scope拡張
安全理由Phase細分化
追加hardening完成条件化
未使用release／public履歴／破壊操作railの定型列挙
```

## KDSL_PROMPT

```text
先頭KDSL_PROMPT:
日本語構造KEY
本文漢字圧縮
成功条件／対象／非対象／検証保持
停止条件限定
報告R1
```

## Agent

`agent: required`時:

```text
標準:=KDSL_PROMPT＋K1
K1更新→目的／対象／権限変更なし
K1完了→未完なし／検証成功／実機確定
```

条件付き:

```text
中断再開／handoff→P1L＋識別付きK1
継続project既定→PF1参照
短縮転送→P1またはP1Lの一方
```

禁止:

```text
P1L／P1同時記載
P1可逆性偽装
P1L／P1／PF1全量の毎回必須化
全権限rail列挙強制
K1でscope追加
PF1でU禁止反転／権限拡張
Agent状態をR1へ全複製
Safety Gate Registry／Packet／Binding Evidence必須依存
```

詳細は `spec/lint/kdsl-agent-lint.md`。

## KDSL_RESULT

```text
状態／局面／要約／変更／理由／実行／検証／実機／危険／次／commit
未実行偽装なし
RT:v偽装なし
roadmap化なし
Agent契約複製なし
```

## validator

```text
validator未実行→pass扱禁止
validator pass != 意味同等
validator pass != 漢字圧縮品質
validator pass != Agent実効性
validator pass != safety proof
validator pass != 実行許可
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
```