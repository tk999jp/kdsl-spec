# Task Template: 調査のみ

```text
用途:=共有材／repo／log／差分を確認し、実装せず判断材料を返す
```

## Instance

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal

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

検証:
- 実行commandは実行欄へ限定記録
- 未実行検証→pass扱禁止
- 検索失敗→不存在断定禁止

停止条件:
- 対象資料取得不能
- 正本候補が相互矛盾し判断不能

報告:
KDSL_RESULTで調査結果を簡潔報告
```

## 禁止

```text
調査を実装Phaseへ自動拡張禁止
潜在riskから追加課題生成禁止
AUTHORITY／Safety Registry追加禁止
未確認→断定禁止
```
