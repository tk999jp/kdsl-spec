# KDSL v2資産監査

```text
状態: 完了／Agent再審査・阻害除去反映済
初回監査日: 2026-07-18
Agent再審査日: 2026-07-19
監査対象: PR #1〜#145
差分範囲: 39a51b71950340b83f6e525dd1a76724530bb0df..031f11286526e77034da5d803e6b01bf0d61a60a
差分file: 309
目的: 漢字圧縮と現行Agent完走へ必要な機能だけを選別回収
```

## 判定基準

```text
採用:=漢字圧縮またはAgent完走へ直接必要／有効
簡略移植:=機能核のみ有効、現architectureは過剰
Intl分離:=非漢字環境だけに必要
不採用:=漢字identityと競合／framework維持が主目的
履歴保存:=実装回収せずarchive参照のみ
```

実装済・CI成功・Phase完了だけを採用理由にしない。

## 全件範囲判定

| PR | 機能群 | 判定 | 処理 |
|---|---|---|---|
| #1 | CompactPrompt／kanji lexicon／CP-Lift | 分割 | CompactPrompt用途のみ簡略移植。漢字optional化／英語KEY既定は不採用 |
| #2〜#3 | CompactPrompt validator／CI | 簡略移植 | 軽量lint／sample runner／CIへ再実装 |
| #4〜#5 | Safety Gate Registry | 不採用 | 明示保護語だけ保持 |
| #6〜#9 | R1C | 不採用 | 最小日本語R1へ必要境界のみ統合 |
| #10〜#29 | Packet／Normalization | 不採用 | KDSL本体・Agent層外 |
| #30 | Python生成物ignore | 採用 | `.gitignore`へ移植 |
| #31〜#44 | Safety semantics／graph／parser | 不採用 | 汎用安全framework不採用 |
| #45〜#47 | R1C round-trip | 簡略移植 | 状態反転防止だけR1 lintへ移植 |
| #48〜#49 | Packet round-trip | 不採用 | archive参照のみ |
| #50〜#54 | guide／R1 quickstart／Ruleset記録 | 分割 | 簡潔guide概念だけ採用 |
| #55〜#58 | 共通parser foundation | 不採用 | 軽量文書lintへ置換 |
| #59〜#62 | R1C optional block | 不採用 | 結果報告肥大化防止 |
| #63〜#78 | Safety／Packet semantic parser | 不採用 | Registry／Packet依存のため不採用 |
| #79〜#117 | parser v2／compatibility／統合architecture | 不採用 | 旧framework互換を持ち込まない |
| #118 | Ruleset enforcement記録 | 履歴保存 | GitHub Rulesで管理 |
| #119〜#131 | P1／P1L schema／parser | 機能核再定義 | P1Lを条件付き厳密契約、P1を任意短縮へ再定義。旧schema／parser／可逆性主張は不採用 |
| #132〜#145 | K1／PF1／Binding Evidence／evaluator | 機能核再定義 | K1最小run状態、PF1 project既定だけ再実装。digest／Binding Evidence／evaluatorは不採用 |

未決範囲なし。

## Agent再審査

```text
維持:
KDSL本体:=漢字圧縮
Agent層:=KDSL Core下位

Agent goal:
U明示scopeを必要最小契約で調査→実装→検証→完了

標準:
KDSL_PROMPT＋K1

条件付き:
P1L:=厳密handoff／中断再開
PF1:=継続project既定
P1:=任意短縮／P1Lと併記禁止／可逆性保証なし
```

## 阻害除去

```text
同一内容三重化→P1L／P1毎回必須を廃止
P1可逆性未実装→可逆性保証を削除
PF1適用順矛盾→PF1参照後P1L生成へ統一
中断再開識別不足→K1へrun／契約／baseline条件追加
実例初期K1完了済→計画状態へ修正
全権限rail定型列挙→今回run関連操作だけへ限定
形式pass=実効性扱い→Codex runtime未確認を分離
```

## 回収内容

```text
CompactPrompt用途profile
漢字document lint
日本語R1 lint
valid／invalid corpus
GitHub Actions
.gitignore
K1最小run状態
P1L条件付き厳密契約
P1任意短縮
PF1 project既定
Agent lint／回帰例
```

## 不採用architecture

```text
lexicon:kanji-v1
KDSL-CP漢
英語KEY既定CompactPrompt
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser v2
旧P1／P1L canonical JSON schema
旧K1／PF1 canonicalization／digest
Binding Evidence
Authority Rail registry化
runtime evaluator
大量closeout／status同期
```

## 完成判定

```text
採否未決: 0
PR範囲未監査: 0
正規版へ持込む旧framework依存: 0
Agent設計阻害: 修正済
Codex実run再帰／再開／承認停止: 未確認
```

validator passは本監査の妥当性・Agent実効性を証明しない。