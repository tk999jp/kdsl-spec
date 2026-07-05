# KDSL Lint Checklist v1.1

目的: KDSL圧縮後の意味欠落 / safety gate欠落 / 危険短縮 / ADPS境界破損を検出する  
対象: KDSL mode:min / mode:dense / profile:dev-prompt / converter出力 / KDSL_PROMPT / KDSL_RESULT要求

## 判定値

```text
保持: 意味が十分残る
弱化: 意味は残るが, 条件/対象/禁止動作が薄い
欠落: 元promptのsafety gateが消失
該当なし: 元promptに該当規則なし
```

弱化/欠落時:
```text
完成扱い禁止
意味変化riskへ記録
修正案を出す
```

## 必須保持check

```text
D禁止保持
D禁保持
rollback/revert保持
未確認→確認済扱禁止保持
未実行→実行済扱禁止保持
未確認→成功扱禁止保持
未確認→断定禁止保持
実機確認分離保持
U観測>AI推測保持
共有材先読保持
AI丸投禁止保持
原因未確→広域修正禁止保持
public履歴/公開済tag/Release Assets保護保持
state/docs固定保持
LocalBuild/Runtime未実行→実行済扱禁止保持
operator/abbrev宣言必要性確認
command/path/code/API名保持
KDSL-DP直接実行禁止保持
P1/P1L正規化必須保持
unknown profile/alias/preset推測禁止保持
RT:v条件保持
build/diff/lint/test pass != RT:v保持
KDSL_RESULT NEXT実行許可扱禁止保持
KDSL_RESULT COMMIT自動commit許可扱禁止保持
```

## KDSL_PROMPT check

```text
KDSL_PROMPT先頭固定
KDSL_PROMPT前自然文なし
format/profile/mode/safety保持
Phase保持
目的/前提/対象Slice/非対象/変更対象保持
禁止/停止条件保持
検証保持
報告形式保持
KDSL_RESULT skeleton保持
D禁止時KDSL_PROMPT出力なし
```

## KDSL_RESULT check

```text
KDSL_RESULT先頭固定要求あり
STATUS/PHASE/S/FILES/WHY/CMD/VERIFY/RT/RISK/NEXT/COMMIT保持
未実行cmd→CMD記載禁止保持
未実行verify→pass扱禁止保持
RT:v条件保持
NEXT:=提案保持
COMMIT:=推奨message保持
```

## 危険短縮

```text
禁止対象のみで禁止動作なし
状態のみで扱禁止なし
承認語削除
未確認語削除
rollback条件削除
実機確認分離削除
或 使用
止安全 使用
高risk箇所で禁のみ使用
command/path/code誤変換
英語技術語の不自然漢字化
= を扱/状態指定に使用
KDSL-DPを実行指示へ短絡
RT:vをbuild pass扱い
NEXTを許可扱い
```

## 危険短縮例

NG:
```text
Runtime確認未確認
AI禁止
方針変注意
AI tool或U確認
止安全より安全進行
git 状態 --短
build成功→RT:v
NEXT→次実行
KDSL-DP→Codex実装
```

OK:
```text
Runtime未確認→確認済扱禁止
共有材判可→AI丸投禁止
方針変含→実装指示禁止, 承認待
AI tool/U確認
停止偏重禁止, 安全進行優先
git status --short
build pass != RT:v
KDSL_RESULT NEXT:=提案, 実行許可扱禁止
KDSL-DP→P1/P1L正規化必須
```

## 合格条件

合格:
```text
必須保持checkが保持または該当なし
high-risk箇所に弱化なし
欠落なし
危険短縮なし
KDSL_PROMPT/KDSL_RESULT要求が必要時保持
```

条件付き合格:
```text
低risk箇所のみ弱化あり
意味変化riskへ記録済
修正案あり
```

不合格:
```text
D禁止欠落
rollback/revert欠落
未確認/未実行扱禁止欠落
実機確認分離欠落
承認gate欠落
public履歴/公開済tag/Release Assets保護欠落
high-risk箇所で禁止動作不明
KDSL-DP直接実行禁止欠落
RT:v条件欠落
KDSL_RESULT NEXT/COMMIT条件欠落
```

## 自然文再展開一致判定

```text
一致: 条件/対象/禁止動作が同じ
弱一致: safety側に強化, 元意味維持
不一致: 条件/対象/禁止動作が変化
```
