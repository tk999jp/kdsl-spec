# KDSL Modes v2.1-kanji-canonical

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
本文漢字語幹化必須
重複／同義統合必須
同一長値・固定条件→正本一回定義→短名参照
安全に記号化可能な条件→記号化
自然文残留を必要最小化
修正可能性維持
```

### dense

```text
min成立条件を全保持
章／箇条書き最小
同義説明強統合
条件／遷移記号化強化
正本参照を積極使用
非識別子制御英語→安定漢字語へ圧縮
技術識別子保持
```

```text
dense非膨張:
意味保持可能範囲でdense本文<=min本文
説明追加／section独立可読性目的の増量禁止
不可侵意味保持に必要な増量のみ例外
```

`<=`は文字数そのものを唯一基準にせず、実投入量の非膨張原則を示す。token断定は対象model tokenizer確認時のみ。

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
