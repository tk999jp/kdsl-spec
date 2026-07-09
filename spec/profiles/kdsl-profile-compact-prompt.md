# KDSL Profile: CompactPrompt v0.1-draft

status: v2-draft
profile: compact-prompt
scope: general LLM prompts / Project files / single prompt instructions

## 1. Purpose

KDSL-CP is a lightweight subset of KDSL for general LLM prompts and Project files.

It keeps the KDSL safety-gate-preserving philosophy while avoiding the heavier AI coding tool contract machinery used by KDSL-Packet / R1 / SG.

```text
priority: safety gate保持 > 意味保持 > 出力安定 > 圧縮率 > 人間可読性
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
  repo操作
  branch/commit操作
  rollback/revert
  public tag / Release Assets
  data migration
  R1検収
```

When non-target conditions are included, use CP-Lift and convert to KDSL-Packet or Full KDSL.

## 3. Header

Recommended standalone header:

```text
format: KDSL
profile: compact-prompt
mode: min|dense
safety: lock-critical
```

For Project files where KDSL-CP is already declared, a shorter block is allowed.

```text
KDSL-CP:
```

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
Role:
  LLMの役割

Goal:
  達成目的

Input:
  入力材料 / 前提 / 任意情報

Output:
  出力形式 / 項目 / 件数 / 文字数

Rules:
  必須処理 / 判断手順

Guard:
  禁止 / 未確認扱い / safety gate

Style:
  文体 / 粒度 / 読者 / 言語

Check:
  出力前self-lint
```

## 5. Minimal common vocabulary

KDSL-CP does not require an external registry, but it has a minimal shared vocabulary to avoid project-to-project interpretation drift.

```text
U      = ユーザー
src    = 入力材料 / source text
out    = 出力
fmt    = 出力形式
req    = 必須
NG     = 禁止カテゴリ
unk    = 不明 / 未確認ではない
est    = 推測
fact   = 入力または根拠で確認できる事実
risk   = リスク
alt    = 代替案
cond   = 条件
chk    = 出力前確認
```

Rules:

```text
未定義略語の使用禁止
略語の意味変更禁止
安全gate語の過剰短縮禁止
Project files内では最初に語彙表を置く
単体promptでは必要語彙のみinline定義可
```

Do not shorten the following protected words in KDSL-CP.

```text
禁止
必須
未確認
未実行
承認
承認待
断定禁止
確認済扱禁止
実行済扱禁止
成功扱禁止
```

## 6. Standard Guard

General-purpose Guard:

```text
Guard:
- src外事実追加禁止
- unk→断定禁止
- est→推測明記
- 不足→確認質問 or 仮定明記
- 指定fmt外出力禁止
- 高risk領域→一般情報+専門確認促し
```

Project files may add:

```text
- U意図>AI補完
- fact/est/alt分離
- 根拠不明情報をfact扱禁止
- 不要な長文化禁止
```

## 7. Check block

Check is a required-grade block for KDSL-CP. It is the final output lint, not a reasoning disclosure request.

Standard Check:

```text
Check:
- fmt一致
- 件数/文字数確認
- src外事実なし
- unk→断定禁止
- est→推測明記
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
- 最新性必要ならweb確認
- fact/est分離
- A/B比較の条件差明記

メタ情報生成:
- 字数確認
- 煽り/誇張なし
- SEO語が本文内容と一致
```

## 8. Modes

```text
CP:min:
  可読性重視。Project files標準。

CP:dense:
  高圧縮。一般LLM直投入向け。

CP:dense-ja:
  漢字alias高圧縮。日本語Project files / 日本語LLM向け。

CP:lock:
  事実確認/調査/高risk話題向け。Guard/Checkを厚めに保持。
```

These are operational names for KDSL-CP. They do not replace the Core `mode` values unless adopted by Core later.

## 9. Example: min

```text
KDSL-CP:
Role: 技術系ブログ編集者/SEO担当
Goal: article src→公開用メタ情報作成
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
- src外事実追加禁止
- unk→断定禁止
- 誇張/煽り禁止
- fmt外出力禁止
Style: 簡潔/実用的/自然な日本語
Check:
- 字数/件数確認
- src外情報なし
- Guard違反なし
```

## 10. Non-goals

```text
AI coding tool向け安全契約の代替
D禁止の軽量化
R1/KDSL_RESULT検収の代替
RT:v条件の緩和
KDSL-DP/P1/P1L境界の変更
```
