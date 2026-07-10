# Examples

KDSL / R1 の変換例・運用例置き場。

## 1. Current groups

```text
examples/
  compact-prompt/
    general LLM / Project files / single prompt examples

  midfd/
    AI coding tool / KDSL_PROMPT / R1 examples

  public/
    public-facing experimental examples
```

## 2. CompactPrompt examples

```text
examples/compact-prompt/README.md
examples/compact-prompt/blog_meta.kdsl-cp.md
examples/compact-prompt/blog_meta.kdsl-cp-kanji.md
examples/compact-prompt/novel_review.kdsl-cp-kanji.md
examples/compact-prompt/prompt_improver.kdsl-cp.md
examples/compact-prompt/cp_lift_example.md
```

Handling:

```text
KDSL-CP example:=一般LLMへ単体直投入可
kanji example:=lexicon:kanji-v1 rules適用
CP-Lift条件該当→KDSL-CP単体使用禁止
現行lift先:=Full KDSL profile:dev-prompt
未定義Packet直接実行禁止
```

## 3. MidFD AI coding examples

Purpose:

```text
長文KDSL_PROMPT beforeをtemplate適用後のafterへ整理し、R1結果例で検収可能性を示す。
```

Files:

```text
docs_state_closeout.before.md:
  共通安全規則/今回固有観測/停止条件/R1報告要求がフル展開された長文例

docs_state_closeout.after.md:
  templates/base + templates/tasks + templates/resultを使いinstance固有情報だけに圧縮した例

r1_result.example.md:
  OBSERVED/INFERRED/NOT_OBSERVED/UNVERIFIEDとAUTHORITYを分離したKDSL_RESULT例
```

Handling:

```text
AI coding exampleを実運用する場合→KDSL_PROMPTへ正規化必須
repo/path/branch/runtime情報を現行状態として流用禁止
```

## 4. Common rules

```text
examplesは正本ではない
Core/Profile/R1/Lint/Bridge/Lexiconの理解補助
example内の値を現行repo状態として扱うこと禁止
保護語弱化禁止
unknown profile/lexicon/schema推測禁止
```
