# KDSL Modes v2.0-kanji-canonical

## mode

```text
readable:=人間review重視
min:=実運用標準／中密度
dense:=AI直投入／高密度
lock:=明示critical箇所の意味保持重視
```

全modeで漢字圧縮identityを維持する。

### min

```text
短い日本語構造KEY
本文の漢字語幹化
重複統合
修正可能性維持
```

### dense

```text
章最小
箇条書き最小
同義説明統合
条件／遷移記号化
技術識別子保持
```

## safety

```text
normal:=明示条件のみ保持
lock-critical:=明示critical箇所だけ強保護
lock-all:=Uが全文保護を明示した場合のみ
```

既定:

```text
safety: normal
```

禁止:

```text
critical語1件→全文lock化禁止
潜在risk推測→gate追加禁止
safetyをmode／profile／漢字圧縮より上位目的化禁止
安全理由scope／Phase／architecture拡張禁止
```

## high-risk限定

high-riskは次の明示文脈だけ。

```text
U要件変更
rollback／revert
未push差分破棄
public履歴改変
公開済tag／Release Assets変更
data schema／保存形式の破壊的変更
KDSL-DP直接実行
RT:v偽装
```

通常bug修正・targeted test・内部整理・明示scope内完成はhigh-riskへ自動昇格しない。

## dense時保護

```text
禁止
未確認
未実行
承認待
RT:v
KDSL-DP直接実行禁止
```

は意味を弱化しない。ただし保護語を理由に追加条件を生成しない。
