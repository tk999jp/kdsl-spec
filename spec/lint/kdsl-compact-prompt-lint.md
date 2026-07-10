# KDSL CompactPrompt Lint v0.1-draft

status: v2-draft
scope: KDSL-CP / kanji-v1 / CP-Lift
canonical: no

## 1. Purpose

This checklist evaluates KDSL-CP prompts for meaning retention, safety-gate retention, structural completeness, lexicon safety, and CP-Lift requirements.

```text
priority: 意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 出力安定 > 圧縮率
```

## 2. Profile and axes

Check:

```text
format:KDSL or declared KDSL-CP shorthand
profile:compact-prompt
mode:=readable|min|dense|lock only
safety:=normal|lock-critical|lock-all
lexicon:=standard|kanji-v1
unknown profile/mode/safety/lexicon推測なし
```

Fail:

```text
mode:dense-ja
CP:dense-jaを正式mode扱い
unknown lexiconを類似名から推測
```

## 3. Required blocks

Standard keys:

```text
required: Goal/Input/Output/Guard/Check
conditional: Role/Rules/Style
```

Kanji-v1 keys:

```text
required: 目/材/出/守/確
conditional: 役/則/調
```

Fail:

```text
required block欠落
required block空欄で省略扱い
OutputとCheckの混同
GuardとCheckの混同
```

## 4. Guard retention

Check as applicable:

```text
入力外事実追加禁止
不明→断定禁止
推測→推測明記
不足→確認質問 or 仮定明記
指定形式外出力禁止
高risk領域の適切な制約
```

Fail:

```text
不明を事実扱い
推測を断定
入力外情報を無条件追加
Guard削除
禁止文型弱化
```

## 5. Check block

Check should be final output lint, not reasoning disclosure.

```text
出力形式一致
件数/文字数確認
入力外事実なし
不明の断定なし
推測明記
Guard違反なし
Output欠落なし
```

Fail:

```text
Checkなし
Checkが抽象的な「確認する」のみ
思考過程/chain-of-thought開示要求へ変質
```

## 6. Lexicon: kanji-v1

Structural aliases allowed at key position:

```text
役/目/材/出/則/守/調/確
```

Restricted free-text aliases:

```text
禁
不
実
要
```

Check:

```text
lexicon:kanji-v1宣言あり or KDSL-CP漢 shorthand使用
構造aliasはKEY位置のみ
unknown aliasなし
保護語を全文保持
```

Fail examples:

```text
不→断定禁止
材外実追加禁止
禁: <禁止内容>
要:=必須/要約を文脈推測
```

Pass examples:

```text
守:
- 入力外事実追加禁止
- 不明→断定禁止
- 推測→推測明記
```

## 7. Protected words

Do not weaken:

```text
禁止
必須
不明
事実
未確認
未実行
承認
承認待
停止条件
正本
rollback
revert
実行済扱禁止
確認済扱禁止
成功扱禁止
断定禁止
実機確認分離
public履歴
公開済tag
Release Assets
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v
KDSL_RESULT NEXT
KDSL_RESULT COMMIT
```

## 8. CP-Lift check

Lift triggers:

```text
実装/改修/削除
repo/path/branch/commit操作
file/API/command変更
rollback/revert
未push破棄
RT:v/実機確認
public履歴/tag/Release Assets
data migration
正本変更
AI coding toolへ渡す場合
```

If any trigger is present:

```text
KDSL-CP単体実装指示禁止
Full KDSL profile:dev-promptへ昇格
Packet registry未定義→KDSL-Packet直接実行禁止
```

## 9. Packet draft check

Fail:

```text
PKT:v1を現行正式schema扱い
BASE/TASK/FLOW/SG/R1Cを未定義のまま実行
PACKET_DRAFTをAI coding toolへ直接投入
unknown registry推測
```

Allowed:

```text
PACKET_DRAFT:
status: non-executable
schema: undefined
```

## 10. Result

```text
PASS:
  required blocks保持
  Guard/Check保持
  lexicon安全
  CP-Lift不要 or 適切に昇格

CONDITIONAL:
  軽微な語彙/可読性問題のみ
  安全gate弱化なし

FAIL:
  意味変化
  safety gate弱化
  required block欠落
  restricted alias使用
  CP-Lift漏れ
  未定義Packet直接実行
```
