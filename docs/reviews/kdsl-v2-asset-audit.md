# KDSL v2資産監査

```text
状態: 完了
監査日: 2026-07-18
監査対象: PR #1〜#145
差分範囲: 39a51b71950340b83f6e525dd1a76724530bb0df..031f11286526e77034da5d803e6b01bf0d61a60a
差分file: 309
目的: 漢字圧縮へ必要な機能だけを選別回収
```

## 判定基準

```text
採用:=漢字圧縮へ直接必要／有効
簡略移植:=機能核のみ有効、現architectureは過剰
Intl分離:=非漢字環境だけに必要
不採用:=漢字identityと競合／framework維持が主目的
履歴保存:=実装回収せずarchive参照のみ
```

実装済・CI成功・Phase完了だけを採用理由にしない。PR metadata全件、309-path差分、正本／代表実装／validator／templateを機能群単位で照合した。

## 全件範囲判定

| PR | 機能群 | 判定 | 処理 |
|---|---|---|---|
| #1 | v2直交軸／CompactPrompt／kanji lexicon／CP-Lift | 分割 | CompactPrompt用途のみ簡略移植。漢字optional化／英語KEY既定／CP-Liftによる漢字解除は不採用 |
| #2〜#3 | CompactPrompt validator／CI | 簡略移植 | 日本語構造KEY用の軽量lint／sample runner／CIへ再実装 |
| #4〜#5 | Safety Gate Registry導入 | 不採用 | 明示保護語だけCore／lintへ保持。Registry不採用 |
| #6〜#9 | R1C schema／validator | 不採用 | 別schema化せず最小日本語R1へ必要境界のみ統合 |
| #10〜#29 | Packet／Normalization／validator／property | 不採用 | KDSL本体外。archive参照のみ |
| #30 | Python生成物ignore | 採用 | `.gitignore`へ移植 |
| #31〜#44 | Safety semantics／inheritance／graph／parser | 不採用 | 汎用安全framework不採用。明示条件保持だけlint化 |
| #45〜#47 | R1C round-trip | 簡略移植 | 項目順／状態反転防止の考え方のみR1 lintへ移植 |
| #48〜#49 | Packet normalization round-trip | 不採用 | archive参照のみ |
| #50〜#54 | 公開guide／R1 quickstart／Ruleset記録 | 分割 | 簡潔guide概念を採用。Ruleset記録は運用証跡で仕様外 |
| #55〜#58 | 共通parser foundation | 不採用 | 英語envelope中心parserは不採用。軽量文書lintへ置換 |
| #59〜#62 | R1C optional block | 不採用 | 結果報告肥大化防止のため採用しない |
| #63〜#70 | Safety semantics validator／共通parser移行 | 不採用 | Registry依存のため不採用 |
| #71〜#78 | Packet semantic property／parser移行 | 不採用 | Packet本体と共に不採用 |
| #79〜#88 | parser v2／compatibility／migration | 不採用 | 旧framework互換維持を正規版へ持ち込まない |
| #89〜#105 | Packet normalization semantic properties | 不採用 | archive参照のみ |
| #106〜#117 | Safety／R1C／Packet parser統合完了 | 不採用 | 統合architecture自体を採用しない |
| #118 | Ruleset enforcement記録 | 履歴保存 | 正規branchの実設定は別途GitHub Rulesで設定 |
| #119〜#131 | P1／P1L schema／parser／Packet変換 | 再審査後不採用 | KDSL-DP→P1／P1L境界だけBridgeへ保持。schema実装は本体外 |
| #132〜#145 | K1／PF1／binding evidence／evaluator | 不採用 | 漢字圧縮へ直接不要。Issue／PR停止済み |

上表は#1〜#145を連続範囲で網羅し、未決範囲なし。

## Closeout／状態同期commit

各機能群に付随するcloseout、review、status同期、証跡修正commitは機能実装とは別採用しない。

```text
理由:
- KDSL_RESULT／状態文書の成果物化を再発させる
- 内部component単位Phaseを固定する
- 漢字圧縮へ直接価値を追加しない
```

必要な設計理由は本監査書と各正本へ統合し、旧closeout群はarchiveに保持する。

## 回収内容

```text
採用:
- CompactPrompt用途profile
- 漢字構造KEYによる軽量document lint
- 日本語KDSL_RESULT lint
- valid／invalid sample corpus
- GitHub Actions検証
- Python生成物ignore

既存Coreから保持:
- command／path／API名変換禁止
- 明示禁止／未確認／未実行の意味保持
- RT:v分離
- KDSL-DP直接実行禁止
- P1／P1L正規化境界
- validator非権威
```

## 不採用architecture

```text
lexicon:kanji-v1
KDSL-CP漢
英語KEY既定CompactPrompt
CP-Liftによる漢字表現解除
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser v2
P1／P1L canonical schema実装
K1／PF1
Binding Evidence
Authority Rail
大量closeout／status同期
```

これらは削除ではなく旧framework archiveへ保存し、将来必要性が漢字圧縮上で証明された場合だけ機能単位で再審査する。

## 完成判定

```text
採否未決: 0
PR範囲未監査: 0
正規版へ持込む旧framework依存: 0
必要移植: CompactPrompt／軽量lint／R1 lint／sample／CI／.gitignore
```

validator passは本監査の妥当性証明ではない。最終判定は正本整合、実用例、差分監査、U方針一致を併用する。
