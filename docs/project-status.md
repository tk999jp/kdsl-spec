# KDSL Project Status

```text
status: canonical
updated: 2026-07-19
branch: canonical/kdsl-kanji
historical-base: 39a51b71950340b83f6e525dd1a76724530bb0df
framework-head: 031f11286526e77034da5d803e6b01bf0d61a60a
framework-archive: archive/kdsl-framework-20260718
agent-layer: kdsl-agent@1
```

## 完了

```text
漢字圧縮identity復元: 完了
PR #1〜#145機能群監査: 完了
旧Core以降309-path監査: 完了
必要機能選別回収: 完了
Core／Profile／Template／R1／Lint／Bridge整合: 完了
Agent必要性再審査: 完了
P1L／P1最小契約: 完了
K1 run状態: 完了
PF1 project既定: 完了
Agent lint／回帰例: 完了
validator compile: pass候補
identity lint: pass候補
canonical regression: pass候補
```

最終passはPR CI成功後に確定する。

## 正本

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=派生subset
Agent層:=KDSL Core下位
P1L:=agent実行契約長形式
P1:=P1L可逆短縮
K1:=agent run状態
PF1:=project既定
安全契機:=明示重大条件の限定保護
R1:=簡潔一時報告
validator:=非権威
```

## Agent使用

```text
repo書込／複数step実装／再帰完走／複数tool／中断再開
→Agent層必須

通常会話／単発回答／変換のみ
→Agent層省略可
```

## 回収

```text
CompactPrompt用途profile
漢字document lint
日本語R1 lint
valid／invalid回帰corpus
GitHub Actions
.gitignore
P1L／P1機能核
K1／PF1機能核
```

## 不採用

```text
漢字optional lexicon／英語KEY既定／旧CompactPrompt漢字別名
Safety Gate Registry／R1C／Packet／Normalization
共通AST／semantic parser v2
旧P1／K1 canonical JSON／digest
Binding Evidence／runtime evaluator
closeout／status同期の自己増殖
```

詳細: `docs/reviews/kdsl-v2-asset-audit.md`

## 旧系統

```text
main:=frozen legacy framework
archive/kdsl-framework-20260718:=回収元保存
旧roadmap:=停止
```

Phase 9E PR #145は未mergeで閉鎖。Issue #132／#144も旧roadmapとして閉鎖済み。

## Repository管理

```text
GitHub default branch: canonical/kdsl-kanji／確認済
canonical branch rules: U設定済
stable tag／release: 対象外／別途U承認必須
```

Agent層は1Phaseで実装・回帰・CI・mergeまで完了させる。stable tag／releaseは今回scope外。
