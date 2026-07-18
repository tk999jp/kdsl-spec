# KDSL Project Status

```text
status: canonical
updated: 2026-07-19
branch: canonical/kdsl-kanji
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

## Agent使用

```text
Codex開発作業→Agent駆動
通常run→KDSL_PROMPT＋K1
中断再開／複数agent handoff／複雑承認→PF1参照＋P1L＋識別付きK1
P1使用→P1Lと併記禁止
```

## 検証状態

```text
validator compile: pass
identity lint: pass
Agent contract lint: pass
Agent運用状態遷移回帰: pass
- 通常run完了収束: pass
- 承認境界直前停止: pass
- 中断再開識別／未完継続: pass
canonical regression: pass
Codex実run再帰完走: 未確認
Codex実run中断再開: 未確認
Codex実run承認境界停止: 未確認
```

運用回帰passは状態遷移契約の自動確認。形式／自動回帰成功だけでCodex Agent実効性を確認済扱いしない。

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
GitHub default branch: canonical/kdsl-kanji／確認済
canonical branch rules: U設定済
stable tag／release: 対象外／別途U承認必須
```
