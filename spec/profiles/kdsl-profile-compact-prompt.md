# KDSL Profile: CompactPrompt v0.2-draft

status: v2-draft
profile: compact-prompt
scope: general LLM prompts / Project files / single prompt instructions

## 1. Purpose

KDSL-CP is a lightweight KDSL profile for general LLM prompts and Project files.

It keeps KDSL meaning and safety gates while avoiding the heavier AI coding work-contract machinery used by dev-prompt / KDSL_PROMPT / R1.

```text
priority: 意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 出力安定 > 圧縮率 > 人間可読性
```

## 2. Target use

```text
対象:
  文章生成
  要約
  翻訳
  レビュー
  比較
  調査
  構成案
  メタ情報生成
  prompt改善
  Project files向け単体prompt

非対象:
  AI coding tool実装指示
  repo/path/branch/commit操作
  rollback/revert
  runtime verification
  public tag / Release Assets
  data migration
  R1検収
```

Non-target conditions trigger CP-Lift to `profile:dev-prompt` or, after future canonicalization, KDSL-Packet.

## 3. Axes and header

KDSL-CP is a profile, not a separate format.

Recommended standalone header:

```text
format: KDSL
profile: compact-prompt
mode: min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
```

Rules:

```text
mode値はCore正本 readable|min|dense|lock のみ
lexiconはmodeではない
unknown lexicon推測禁止
Project fileで既定宣言済み→短縮header可
```

Short form:

```text
KDSL-CP:
```

Kanji shorthand:

```text
KDSL-CP漢:
:= profile:compact-prompt + mode:dense + lexicon:kanji-v1
```

`KDSL-CP漢:` is a declared composition shorthand, not a new mode.

## 4. Standard blocks

```text
KDSL-CP:
Role:
Goal:
Input:
Output:
Rules:
Guard:
Style:
Check:
```

Responsibilities:

```text
Role:=LLMの役割
Goal:=達成目的
Input:=入力材料/前提/任意情報
Output:=出力形式/項目/件数/文字数
Rules:=必須処理/判断手順
Guard:=禁止/未確認扱い/safety gate
Style:=文体/粒度/読者/言語
Check:=出力前self-lint
```

## 5. Required and conditional blocks

Required:

```text
Goal
Input
Output
Guard
Check
```

Conditional:

```text
Role:=役割指定が出力安定に必要な場合
Rules:=処理順/判断条件が必要な場合
Style:=言語/文体/読者/粒度指定が必要な場合
```

Kanji-v1:

```text
必須: 目/材/出/守/確
条件付き: 役/則/調
```

Empty required blocks are not valid omission substitutes.

## 6. Minimal common vocabulary

KDSL-CP does not require an external registry, but it has a minimal shared vocabulary.

```text
U      = ユーザー
src    = 入力材料/source text
out    = 出力
fmt    = 出力形式
req    = 必須
unk    = 不明
est    = 推測
fact   = 入力または根拠で確認できる事実
risk   = リスク
alt    = 代替案
cond   = 条件
chk    = 出力前確認
```

Rules:

```text
未定義略語使用禁止
略語意味変更禁止
安全gate語の過剰短縮禁止
単体prompt→必要語彙のみinline定義可
Project files→profile/lexicon参照または語彙宣言必須
```

Protected words remain explicit:

```text
禁止
必須
不明
事実
未確認
未実行
承認
承認待
断定禁止
確認済扱禁止
実行済扱禁止
成功扱禁止
```

## 7. Standard Guard

Recommended general-purpose Guard:

```text
Guard:
- 入力外事実追加禁止
- 不明→断定禁止
- 推測→推測明記
- 不足→確認質問 or 仮定明記
- 指定形式外出力禁止
- 高risk領域→一般情報+専門確認促し
```

Project files may add:

```text
- U意図>AI補完
- 事実/推測/代替案分離
- 根拠不明情報を事実扱禁止
- 不要な長文化禁止
```

Safety-critical free text should prefer full words over one-character aliases.

## 8. Check block

Check is required-grade final output lint, not a reasoning disclosure request.

```text
Check:
- 出力形式一致
- 件数/文字数確認
- 入力外事実なし
- 不明の断定なし
- 推測明記
- Guard違反なし
- Output欠落なし
```

Use-case examples:

```text
レビュー:
- 良点/問題点/改善案を分離
- 抽象論のみ禁止
- 本文根拠あり

調査:
- 最新性必要→web確認
- 事実/推測分離
- A/B比較の条件差明記

メタ情報生成:
- 字数確認
- 煽り/誇張なし
- SEO語が本文内容と一致
```

## 9. Modes

KDSL-CP uses Core mode values without defining new modes.

```text
mode:readable
  人間レビュー/共有重視

mode:min
  Project files標準

mode:dense
  高圧縮/一般LLM直投入

mode:lock
  事実確認/高risk話題/Guard保持重視
```

Kanji aliases are selected by `lexicon:kanji-v1`, not by `mode:dense-ja`.

## 10. Example

```text
format: KDSL
profile: compact-prompt
mode: min
safety: lock-critical
lexicon: standard

KDSL-CP:
Role: 技術系ブログ編集者/SEO担当
Goal: article input→公開用メタ情報作成
Input: article_text
Output:
- 要約:120字以内
- 主要テーマ:5件
- SEOタイトル案:5件
- メタディスクリプション:120字以内
- ハッシュタグ:5〜8件
Rules:
- 日本語固定
- 技術初心者にも伝わる
- 各項目短く実用的
Guard:
- 入力外事実追加禁止
- 不明→断定禁止
- 誇張/煽り禁止
- 指定形式外出力禁止
Style: 簡潔/実用的/自然な日本語
Check:
- 字数/件数確認
- 入力外事実なし
- Guard違反なし
```

## 11. CP-Lift

The following conditions require lift from KDSL-CP.

```text
実装/改修/削除
repo/path/branch/commit操作
file/API/command変更
rollback/revert
runtime verification
public履歴/tag/Release Assets
data migration
正本変更
AI coding toolへ渡す場合
```

Current lift target is Full KDSL `profile:dev-prompt`. Future KDSL-Packet cannot be executed until its registry and schema become canonical.

## 12. Non-goals

```text
AI coding tool向け安全契約の代替
D禁止の軽量化
R1/KDSL_RESULT検収の代替
RT:v条件緩和
KDSL-DP/P1/P1L境界変更
未定義Packet直接実行
```
