# KDSL Lint Checklist v3.3-kanji-agent

## 合格必須

```text
漢字圧縮が第一
英語KEYへ退行なし
KEY翻訳だけで終了していない
本文が漢字語幹／記号／最小制御語化
同一長値／固定条件の不要再掲なし
元意味保持
明示禁止保持
未確認／未実行の反転なし
command／path／API名保持
AI推測安全条件追加なし
scope拡張なし
後発確定保持／撤回済判断復活なし
状態観測の契約正本昇格なし
対象外観測可能意味変更の許可なし
契約変更と契約違反復元の混同なし
契約test弱体化許可なし
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
本文自然文維持＋日本語KEY化だけ
KDSL_PROMPT／P1L／P1で同一内容を多重記載
```

正本参照不足:

```text
同一hash／version／path／tag／Asset名／固定状態を複数sectionへ長値再掲
成功条件／検証／保持／停止条件で同一成立状態を全文再説明
section単独可読性目的で正本値を再掲
意味明確な短名で参照可能なのに長値反復
```

自然文残留候補:

```text
「場合／なら／とき」等が安全に→化可能なのに長文維持
「確認する／維持する／変更しない」等の同義句反復
非識別子のCandidate／baseline／read-only／exact／unrelated／fallback等を一般制御語として過剰残存
```

mode:

```text
min→重複統合／長値正本参照／本文漢字語幹化が不足
 dense→min成立条件未達
 dense→説明追加／section再掲で不必要にminより膨張
```

`dense>min`は即意味違反ではない。不可侵意味保持に必要な増量は許容し、説明追加・再掲による増量を圧縮不足として扱う。

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

## 契約保持

```text
同一事項競合→後発確定が保持されている
直近記述だけを確定扱いしていない
撤回済／置換済判断が復活していない
仮説／提案／状態観測が確定契約へ昇格していない
source／test／Docs／State／KDSL_RESULTが明示なしに正本化されていない
AI判断をU確定扱いしていない
source／test／Docs／State相互一致だけを契約変更根拠にしていない
下位情報が上位契約を上書きしていない
対象外の観測可能意味変更を許可していない
契約変更と現実装の契約違反復元を混同していない
確定契約testの削除／反転／弱体化を許可していない
期待値変更が現実装追従だけで正当化されていない
test passを契約適合扱いしていない
```

意味変更例:

```text
集合演算／追加／置換／結合／clear
保存／復元範囲
routing／fallback
default値
UI操作結果
副作用範囲
```

内部rename／refactorは対象外動作同値を保つ場合だけ許可する。

## KDSL_PROMPT

```text
先頭KDSL_PROMPT:
日本語構造KEY
本文漢字圧縮
成功条件／対象／非対象／検証保持
停止条件限定
報告R1
正本定義済み長値のsection再掲なし
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
zero-delta報告増殖なし
契約変更候補は発生時のみ既存欄へ簡潔記載
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
