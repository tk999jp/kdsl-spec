# KDSL Lexicon: kanji-v1 v0.1-draft

status: v2-draft
lexicon: kanji-v1
scope: KDSL-CP structural key aliases / Japanese compact prompts

## 1. Purpose

`kanji-v1` is a compact Japanese lexicon for KDSL-CP.

It is a vocabulary layer, not a profile or mode.

```text
profile:=用途
mode:=圧縮強度
lexicon:=使用語彙/alias集合
```

Recommended composition:

```text
format: KDSL
profile: compact-prompt
mode: dense
safety: lock-critical
lexicon: kanji-v1
```

Declared shorthand:

```text
KDSL-CP漢:
:= profile:compact-prompt + mode:dense + lexicon:kanji-v1
```

## 2. Structural key aliases

The following aliases are allowed at block-key position.

```text
役 = Role
目 = Goal
材 = Input
出 = Output
則 = Rules
守 = Guard
調 = Style
確 = Check
```

Usage:

```text
役: <role>
目: <goal>
材: <input>
出: <output>
則: <rules>
守: <guard>
調: <style>
確: <check>
```

Rules:

```text
構造alias:=KEY位置のみ使用
KEY意味変更禁止
unknown構造alias推測禁止
```

## 3. Minimal lexical aliases

The following lexical aliases may be used when declared and unambiguous.

```text
U   = ユーザー
材  = 入力材料/source
型  = 出力形式/format
推  = 推測
危  = リスク
代  = 代替案
条  = 条件
```

These aliases are optional. Full words are preferred when a one-character form could change safety meaning.

## 4. Reserved or restricted one-character forms

The following are not standard free-text aliases in `kanji-v1`.

```text
禁
不
実
要
```

Reasons:

```text
禁:
  Coreで「禁止→禁」短縮禁止

不:
  不明/不可/不一致/否定と衝突

実:
  事実/実行/実装/実機/実績と衝突

要:
  必須/要件/要約/必要と衝突
```

They may appear as normal Japanese characters inside words, but must not be interpreted as undeclared KDSL aliases.

## 5. Protected free-text words

The following must remain explicit in safety-critical free text.

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

Examples:

```text
推奨:
守:
- 入力外事実追加禁止
- 不明→断定禁止
- 推測→推測明記

非推奨:
守:
- 材外実追加禁止
- 不→断定禁止
```

## 6. Required and conditional keys

For KDSL-CP with `kanji-v1`:

```text
必須:
  目
  材
  出
  守
  確

条件付き:
  役
  則
  調
```

## 7. Non-application

`kanji-v1` does not automatically apply to:

```text
KDSL-Core canonical fields
KDSL_PROMPT
KDSL_RESULT
R1 full block names
KDSL-DP/P1/P1L
path
command
URL
repo名
branch名
tag名
file名
class/method/property/API名
```

Explicit file/path aliases require a separate alias table. Implicit transformation is prohibited.

## 8. Unknown alias policy

```text
unknown lexicon推測禁止
unknown alias推測禁止
alias意味変更禁止
未宣言alias使用禁止
lexicon未読→読了扱禁止
```

## 9. Compatibility

```text
構造alias追加→compatible candidate
既存alias意味変更→breaking
保護語を一字alias化→breaking / prohibited candidate
unknown alias推測許可→prohibited
```
