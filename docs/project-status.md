# KDSL Project Status

```text
status: canonical
updated: 2026-08-04
branch: main
historical-base: 39a51b71950340b83f6e525dd1a76724530bb0df
framework-head: 031f11286526e77034da5d803e6b01bf0d61a60a
framework-archive: archive/kdsl-framework-20260718
agent-layer: kdsl-agent@1.1
```

## 完了

```text
漢字圧縮identity復元: 完了
PR #1〜#145機能群監査: 完了
旧Core以降309-path監査: 完了
必要機能選別回収: 完了
Agent必要性再審査: 完了
Agent goal明確化: 完了
標準経路KDSL_PROMPT＋K1化: 完了
P1L／PF1条件付き化: 完了
P1可逆性偽装除去: 完了
PF1適用順補正: 完了
K1再開識別条件追加: 完了
Agent lint／回帰例: 完了
Agent運用状態遷移回帰: 完了
Codex実run三経路確認: 完了
RunChanged契約／R1変更file帰属: 検証完了
漢字圧縮定量評価: 完了
単独Project用compiled converter: 完了
standalone専用lint／CI統合: 完了
```

## 正本

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=派生subset
Agent目的:=U明示scopeを必要最小契約で完走
標準Agent:=KDSL_PROMPT＋K1
P1L:=厳密handoff／中断再開時のみ
P1:=任意短縮／可逆性保証なし
K1:=agent run状態
PF1:=project既定／P1L生成前参照
安全契機:=明示重大条件の限定保護
R1:=簡潔一時報告
validator:=非権威
```

## 配布用compiled prompt

```text
path: prompts/kdsl-converter-standalone.md
用途: ChatGPT Project instructions／単独instruction
状態: 非正本／配布・投入用
生成元: identity＋Core＋mode＋converter＋lint
競合: spec/正本優先
検査: tools/validator/kdsl_standalone_lint.py
```

## Agent使用

```text
Codex開発作業→Agent駆動
通常run→KDSL_PROMPT＋K1
中断再開／複数agent handoff／複雑承認→PF1参照＋P1L＋識別付きK1
P1使用→P1Lと併記禁止
```

## 検証状態

```text
validator compile: CI対象
identity lint: CI対象
standalone converter lint: CI対象
Agent contract lint: CI対象
Agent運用状態遷移回帰: pass
- 通常run完了収束: pass
- 承認境界直前停止: pass
- 中断再開識別／未完継続: pass
- RunChanged算出規則: pass
Git repository RunChanged回帰: pass
- 開始clean変更: pass
- 開始dirty追加変更／不変分離: pass
- pre-existing untracked変更／不変分離: pass
- create／delete／rename: pass
- 開始状態復元除外: pass
- test直接編集／実行のみ分離: pass
- InitialHEAD／FinalHEAD commit差分: pass
圧縮定量評価: pass
canonical regression: pass
Codex実run再帰完走: verified
Codex実run承認境界停止: verified
Codex実run中断再開: verified
```

`CI対象`はworkflow登録状態を示し、特定commitのcheck成功を意味しない。運用回帰passは状態遷移契約の自動確認。Git repository回帰は一時repositoryで実Git操作とBaselineState／FinalState比較を確認する。これらの成功だけで、任意Agentが対象repositoryのbaselineを漏れなく取得することやCodex Agent実効性を一般保証しない。

## 圧縮定量評価

```text
確認日: 2026-07-20
対象: AI coding／業務blog meta／創作seed
尺度: 空白除外Unicode文字数
min本文: 45.1%削減
min投入全体: 30.5%削減
dense本文: 48.0%削減
dense投入全体: 32.3%削減
概念marker: 21/21 pass
script: tools/validator/kdsl_compression_evaluation.py
CI: KDSL Validationへ統合
```

```text
通常運用:=mode:min
dense:=minより実投入量減少時／AI直投入密度優先時
marker pass!=完全意味同等／応答品質証明
```

## Codex実run確認範囲

```text
確認日: 2026-07-19
環境: Codex／Windows
対象repository: MidFD
baseline: 879cd4c415584830e2cad181a9139dc07134cf7d
検証Task: Breadcrumb drive-root表示判定の内部helper抽出
通常完走: verified
承認境界停止: verified
中断再開: verified
対象test: BreadcrumbPathModelTests 12/12 pass
diff check: pass
stage／commit／push: 未実行
検証worktree／local branch: cleanup済み
```

上記verifiedは当該環境／repository／Taskでの実測。全model／全environment／全repositoryへの一般保証ではない。

## RunChanged検証範囲

```text
確認日: 2026-07-20
方式: 一時Git repository自動生成
script: tools/validator/kdsl_run_changed_git_regression.py
候補: 11
RunChanged: 9
除外確認: 4
CI: KDSL Validationへ統合
```

確認済:

```text
開始時clean file変更
開始時dirty fileの追加変更
開始時dirty不変file除外
pre-existing untracked変更／不変分離
新規作成／削除／rename旧新path
編集後に開始状態へ復元したfile除外
test直接編集を採用
test実行のみを除外
run中commit差分を採用
```

未証明:

```text
任意Agentが実対象repositoryで開始状態を漏れなく採取すること
全platform／全Git設定での一般成立
```

## 不採用

```text
漢字optional lexicon／英語KEY既定／旧CompactPrompt漢字別名
Safety Gate Registry／R1C／Packet／Normalization
共通AST／semantic parser v2
旧P1／K1 canonical JSON／digest
Binding Evidence／runtime evaluator
全schema毎回展開
closeout／status同期の自己増殖
```

## Repository管理

```text
GitHub default branch: main／確認済
main branch rules: U設定済
framework archive: archive/kdsl-framework-20260718
stable tag／release: 対象外／別途U承認必須
```
