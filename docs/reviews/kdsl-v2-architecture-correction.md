# KDSL v2 Architecture Correction Review

status: reviewed-and-merged
review_date: 2026-07-10
integration_date: 2026-07-10
source_branch: feature/kdsl-v2-compact-prompt
base: main
pull_request: 1
merge_method: squash
merge_status: merged
squash_commit: ae55f845018c0e8208d9e07c9814bc48035b2ef8
status_sync_commit: c25c618b335e39d7ed9f14ffb988ff89fcee1907

## 1. Review purpose

Re-evaluate the CompactPrompt draft after the model transition, correct structural issues, and verify the result before integration into `main`.

## 2. Initial findings

```text
P0-1: v2 priority reversed Core meaning/safety order
P0-2: CP:dense-ja looked like a new formal mode
P0-3: kanji aliases mixed profile/mode/lexicon responsibilities
P0-4: one-character free-text aliases weakened clarity
P0-5: PKT:v1 looked executable before Packet schema/registry existed
P0-6: examples/README required KDSL_PROMPT for all examples, conflicting with standalone KDSL-CP
P0-7: README/manifest/CHANGELOG license state conflicted with MIT state canonical
P0-8: v1.1 stable candidate and v2 breaking redesign were presented in parallel
```

## 3. Corrections applied

### Architecture axes

```text
format
profile
mode
safety
lexicon
envelope
```

Named compositions are now axis combinations rather than separate languages.

### Priority

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 出力安定 > 圧縮率
```

### CompactPrompt

```text
KDSL-CP:=profile:compact-prompt
required:=Goal/Input/Output/Guard/Check
conditional:=Role/Rules/Style
```

### Kanji lexicon

```text
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1
structural keys:=役/目/材/出/則/守/調/確
structural keys:=KEY位置のみ
```

Restricted free-text forms:

```text
材/出/守/確/禁/不/実/要
```

### CP-Lift / Packet

```text
current lift target:=Full KDSL profile:dev-prompt
KDSL-Packet:=draft-non-executable
PKT:v1使用禁止
registry未定義→実行禁止
```

### Examples

```text
KDSL-CP examples:=standalone general LLM use
AI coding examples:=KDSL_PROMPTへ正規化必須
CP-Lift条件該当→KDSL-CP単体使用禁止
```

### License/release

```text
license:=MIT
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=hold
v2-draft:=mainへ統合
```

## 4. Files added

```text
spec/lexicons/kdsl-lexicon-kanji-v1.md
spec/lint/kdsl-compact-prompt-lint.md
spec/glossary-v2-draft.md
docs/reviews/kdsl-v2-architecture-correction.md
```

## 5. Files replaced or revised

```text
docs/design/kdsl-v2-direction.md
spec/profiles/kdsl-profile-compact-prompt.md
spec/bridge/kdsl-cp-packet-bridge.md
spec/manifest.md
README.md
CHANGELOG.md
docs/project-status.md
examples/README.md
examples/compact-prompt/*
```

Removed:

```text
spec/profiles/kdsl-compact-kanji-aliases.md
```

Reason:

```text
漢字aliasはProfileではなくLexicon責務
```

## 6. Safety verification

```text
Core保護語変更なし
KDSL_PROMPT/KDSL_RESULT固定語変更なし
RT:v意味変更なし
NEXT/COMMIT権限意味変更なし
KDSL-DP/P1/P1L境界変更なし
public履歴/tag/Release Assets操作なし
```

## 7. Integration result

```text
PR:#1
source:feature/kdsl-v2-compact-prompt
base:main
source commits:36
merge method:squash
squash commit:ae55f845018c0e8208d9e07c9814bc48035b2ef8
status sync commit:c25c618b335e39d7ed9f14ffb988ff89fcee1907
merged:true
```

Notes:

```text
36 branch commits→1 squash commitへ統合
merge後状態正本同期→別commit
main履歴rewrite/force pushなし
```

## 8. Post-merge lint result

Checked:

```text
old alias path reference
dense-ja formal-mode usage
license pending state
not_merged state
PKT:v1 execution-like usage
```

Judgment:

```text
old alias path:=CHANGELOG/review履歴記録のみ
mode:dense-ja:=禁止例/lint説明のみ
license:pending:=current filesなし
PKT:v1:=禁止規則/履歴説明のみ
not_merged:=this review metadata was stale and is corrected here
```

## 9. Remaining gaps

```text
CompactPrompt validator実装なし
Packet schema未定義
BASE/TASK/FLOW/SG registry未定義
R1C schema未定義
v2 public-facing introduction未確定
GitHub Actions未構成
full parserなし
```

## 10. Final review judgment

```text
direction: pass
architecture correction: pass
safety boundary: pass with draft limitations
examples: pass
manual post-merge lint: pass
validator implementation: not_run / not_implemented
integration: completed
stable readiness: not_ready
```

## 11. Explicit non-actions

```text
tag操作なし
release操作なし
Release Assets操作なし
stable化なし
validator pass扱いなし
RT:v扱いなし
source branch削除なし
public履歴rewriteなし
```
