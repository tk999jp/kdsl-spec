# KDSL Modes v1.1

目的: KDSLのmode / safety / profile / high-risk運用を定義する  
参照正本: `kdsl-spec.md`

## mode

### mode:readable
人間レビュー重視。仕様書/共有/記事化向け。

### mode:min
実運用向け中密度圧縮。ChatGPT/Codex project prompt向け。通常既定。

### mode:dense
高密度圧縮。AI直投入/Project file圧縮/文字数削減向け。  
章見出し最小、箇条書き最小、章本文1〜3行目安。  
safety checkは本文外。

### mode:lock
高risk箇所の意味保持重視。D禁止/rollback/未確認/承認gate/public tag/Release Assets向け。

廃止:
```text
mode:converter
```
converterは用途であり、`profile: converter` に統合する。

## safety

### safety:normal
低risk用途。

### safety:lock-critical
高risk箇所のみlock適用。dev-prompt標準。

### safety:lock-all
全文lock寄り。破壊操作/migration/rollback周辺向け。

## 優先順位

```text
safety > high-risk判定 > mode > profile
```

## 推奨組合せ

| mode | safety | 用途 |
|---|---|---|
| readable | normal | 共有/説明 |
| min | lock-critical | 標準運用 |
| dense | lock-critical | 高密度、high-riskはdense-lock-lite |
| dense | lock-all | 保守的dense |
| lock | lock-all | 検査/保守/破壊操作 |

## 補助用語

```text
dense-safe = mode:dense + safety:lock-critical
dense-lock = mode:dense + safety:lock-all相当
dense-lock-lite = mode:dense内のhigh-risk箇所だけを短く保護
```

注意:
- dense-safe/dense-lock/dense-lock-liteは正式mode名ではなく運用呼称
- 指定値としては使わない

## high-risk

high-risk:
```text
D禁止
rollback/revert
未確認/未実行
承認gate
実機確認分離
public履歴/公開済tag/Release Assets
data migration
正本変更
UI契約変更
破壊操作
KDSL-DP直接実行
RT:v
KDSL_RESULT NEXT
KDSL_RESULT COMMIT
```

判定順:
```text
[high-risk]明示 > high-risk語を含む行 > high-risk章 > safety指定
```

過検出抑制:
```text
high-risk語が例示/辞書定義のみ→note扱
実装/変更/削除/承認/rollback文脈→high-risk扱
```

## mode:dense時の安全規則

mode:denseでも以下は短縮弱化しない。

```text
禁止→禁 への短縮禁止
未確認→未確 への短縮禁止
未実行→未実 への短縮禁止
承認待→承待 への短縮禁止
実行済扱→実済扱 への短縮禁止
確認済扱→確済扱 への短縮禁止
成功扱→成扱 への短縮禁止
断定禁止→断禁 への短縮禁止
KDSL-DP直接実行禁止保持
RT:v条件保持
KDSL_RESULT NEXT/COMMIT条件保持
```
