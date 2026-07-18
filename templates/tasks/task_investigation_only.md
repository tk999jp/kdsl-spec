# Task Template: 調査のみ

```text
用途:=共有材／repo／log／差分をAgent確認し、実装せず判断材料を返す
```

## Agent展開

本template使用時、`templates/base/kdsl_base_dev.md`のP1L／P1／K1／PF1 blockを同一promptへ展開する。

```text
実行方式:=agent再帰
権限:=読取=可／編集=不可／試験={{必要時可}}／stage以降=対象外
```

## Instance

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

局面: {{調査名}}
目的: {{明らかにする事項}}
成功条件:
- 観測事実／推定／未確認を分離
- 原因候補を根拠付きで限定
- 実装／編集なし

根拠:
- {{共有file／log／screenshot／repo}}

正本:
- repo: {{repo}}
- branch: {{branch}}

権限: P1L参照
承認境界: 編集要求発生時

対象:
- {{調査対象}}

非対象:
- file編集
- commit／push／release
- 未依頼の改善設計

作業:
1. 共有材先読
2. 必要箇所だけrepo確認
3. 事実／推定／未確認整理
4. 依頼質問へ直接回答
5. K1未完=なしまで再帰

試験:
- {{必要時のみread-only検証}}

検証:
- 実行commandは実行欄へ限定記録
- 未実行検証→pass扱禁止
- 検索失敗→不存在断定禁止

停止条件:
- 対象資料取得不能
- 正本候補が相互矛盾し判断不能
- 編集／scope変更が必要

報告: R1
```

## 禁止

```text
調査を実装Phaseへ自動拡張禁止
潜在riskから追加課題生成禁止
Safety Registry追加禁止
K1更新による調査scope変更禁止
未確認→断定禁止
```
